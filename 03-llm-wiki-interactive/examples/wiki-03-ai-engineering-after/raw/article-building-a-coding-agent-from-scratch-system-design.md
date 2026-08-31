---
title: "Building a Coding Agent From Scratch"
subtitle: "Designing the harness around the model, from the agent loop to a remote swarm."
authors: ["Paul Iusztin"]
published_date: "2026-07-22T11:04:24+00:00"
source_url: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
origin: article
fetched: 2026-08-29T17:00:54Z
---

# Building a Coding Agent From Scratch

*Designing the harness around the model, from the agent loop to a remote swarm.*
# Building a Coding Agent From Scratch

### Designing the harness around the model, from the agent loop to a remote swarm.

[![Paul Iusztin's avatar](https://substackcdn.com/image/fetch/$s_!pQz0!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0714d360-396c-4b41-a676-1b58dc1dc5f3_1470x1470.jpeg)](https://substack.com/@pauliusztin)

[Paul Iusztin](https://substack.com/@pauliusztin)

Jul 22, 2026

In LangChain’s Terminal-Bench experiment, changing only the harness (with the same model) moved a coding agent from ~30th place into the top 5: the harness, not the model, is what makes a coding agent good.

In the **open-source course** **[Building a Coding Agent From Scratch](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, you’ll build that harness from scratch in Python: **Decode**, a complete coding agent that grows lesson by lesson from a bare agent loop into a swarm of remote agents running in parallel in the cloud.

**Why?** You’ll be able to engineer custom harnesses for your own AI products (the skill behind that leaderboard jump), and you’ll understand what Claude Code and Codex actually do under the hood, turning you into a power user.

[![](https://substackcdn.com/image/fetch/$s_!ge05!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)](https://substackcdn.com/image/fetch/$s_!ge05!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)

**Lessons:**

1. **Building a Coding Agent From Scratch ←** ***you are here***
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)
4. [Context Engineering for Coding Agents](https://www.decodingai.com/p/context-engineering-for-coding-agents)
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

[Full open-source course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

# Lesson 1: Building a Coding Agent From Scratch

[![The model is the smallest part. The machine around it is what you're about to build.](https://substackcdn.com/image/fetch/$s_!yVLk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15bedf6a-82c7-467b-a260-9a084c6d2b5a_1376x768.png "The model is the smallest part. The machine around it is what you're about to build.")](https://substackcdn.com/image/fetch/$s_!yVLk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15bedf6a-82c7-467b-a260-9a084c6d2b5a_1376x768.png)

In a [test run by LangChain on Terminal-Bench](https://blog.langchain.com/the-anatomy-of-an-agent-harness/), changing only the harness (same model throughout) moved a coding agent from roughly 30th place into the top 5. The model isn’t what makes a coding agent good. The harness is. So that’s what we’ll build from scratch. A coding agent harness.

When I first started digging into coding agents, I couldn’t tell where the agent ended and the harness began. I wanted past that black box, so in the past months I’ve researched how the most popular coding agent tools work under the hood: Claude Code (via its leaked source), [OpenCode](https://github.com/anomalyco/opencode), [Pi](https://github.com/earendil-works/pi), and [Aider](https://github.com/aider-ai/aider).

That harness is the only layer you can actually engineer. And that’s why I think building your own coding agent harness from scratch is the best way to understand both how to better use coding agents to become a power user and how to build your own custom harnesses for AI agents.

*During my research, I’ve built my own replica: **“Decode: The Coding Agent”**. Now, I want to **show you how to build your own.***

[![](https://substackcdn.com/image/fetch/$s_!a09O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0acc2c8-d4bb-4730-88d1-9fa2db966e6f_1815x986.png)](https://substackcdn.com/image/fetch/$s_!a09O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0acc2c8-d4bb-4730-88d1-9fa2db966e6f_1815x986.png)

Decode: The Coding Agent - Planning

I don’t mean a simple LLM with some tools in a loop, which is just the good old ReAct pattern. I mean building the whole coding harness from scratch. Build a coding agent once, and you’re equipped to build a custom agent for any use case.

The truth is that to add custom business logic to existing open-source harnesses such as [Pi](https://github.com/earendil-works/pi), [DeepAgents](https://github.com/langchain-ai/deepagents) by LangChain, or [Pydantic AI Harness](https://github.com/pydantic/pydantic-ai-harness) is not that hardcore. But to know what to add based on the internals of these harnesses is extremely important. That’s fundamentals. The secret sauce that still makes AI Engineers valuable.

In this **8-lesson series**, you’ll build a complete coding agent called **Decode**, from scratch, in Python. It runs as a CLI via `decode` for interactive use, or as a remote headless agent that lets you run a swarm of agents in parallel on a cloud platform for automation such as picking up tasks from the backlog or PR reviews.

You’ll learn how to implement all of that in 3 escalating phases. First, build: the agent loop via Pydantic AI, powered by open-source models on [Modal](https://modal.com/?source=decodingai&campaign=harnesseng) or [OpenRouter](https://openrouter.ai/).

Then building the harness around the loop: durable execution with [Kitaru](https://www.zenml.io/product/kitaru?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=brand), context engineering, memory, the permission layer, sandboxing in Docker and Modal, and the agent catalog of planners, builders, explorers, and subagents. All the good stuff.

Finally, the boring stuff that makes you a senior AI engineer: a custom benchmark similar to [Terminal-Bench](https://www.tbench.ai/leaderboard), AI Evals for regressions, observability via [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course), and deployment to GCP running a swarm of agents in parallel.

Before getting into the implementation, I want to kick off this lesson with the most fun part: **the system design of the coding agent.**

Let’s trace the architecture end to end, following one request through every component.

[![](https://substackcdn.com/image/fetch/$s_!5g74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc58beb8-0171-4fe3-a109-c13ddd5f0145_1816x855.png)](https://substackcdn.com/image/fetch/$s_!5g74!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc58beb8-0171-4fe3-a109-c13ddd5f0145_1816x855.png)

Decode: The Coding Agent - Demos as **.decode/skills** you can run yourself

## The High-Level System Design

You pass a coding agent a request — “fix the bugs that make the unit tests fail” — and it loops: explore the codebase, run the tests, read the feedback, edit the code, repeat. The input is your request, while the repository is the state of the codebase. The output is tested changes done to the repo. Everything in between is the harness.

We are pretty familiar with this process. **But how does it work?**

At the center sits the headless harness: no interface of its own. It exposes a module that interfaces connect to. At the core, it runs the agent loop every harness shares: the LLM picks an action (a tool call — run the failing test suite), the tool executes and returns an observation (2 failing tests, expected vs actual), and the loop feeds it back. Everything reads from and writes to the context window (the state of the LLM).

To highlight that the harness is independent from the LLM, we wanted to implement multiple LLM providers. The loop is powered by an LLM provider module that to support open-source models we implemented it with Modal (for self-hosting) and OpenRouter (for APIs). Also, we added support for Gemini for their free tier. [Modal](https://modal.com/?source=decodingai&campaign=harnesseng) is the most interesting as it allows us to either host standard open-source models or easily host our own fine-tuned models on top of their serverless infrastructure.

That cycle lets the agent correct itself: implement the code, run or compile it, read the error, fix it — or catch the mistake before anything runs, with a Language Server Protocol (LSP) server flagging broken syntax the moment an edit happens. The tighter these feedback loops, the faster the agent converges on working code. The LSP server (we used ty - made by Astral’s - the guys behind uv and ruff) is the cheapest way to get feedback on code changes.

Along with the LLM providers and LSP server, the harness contains 4 more essential modules: Memory, Skills, Sandbox, and Permissions. Essential for context engineering and security.

The context window of the LLM is a budget. The conversation accumulates in the window until it stops fitting or performance degrades. Remember that too much context confuses the model, known as context decay. Every observation the loop feeds back [spends from the same finite budget](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Hence, the harness needs to implement compaction techniques such as summarization, truncation, or just clearing the window.

How do we interact with the headless harness? It has two core interfaces: interactive mode, a terminal user interface (TUI) wired to one live session, and remote mode, where an agent runtime ([Kitaru](https://www.zenml.io/product/kitaru?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=brand)) runs N headless harnesses in parallel on a server.

On top of everything, we have the AI evals & observability layer, powered by [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course), that records every model call and tool call, and turns a bad prompt tweak into a failing regression score before your users feel it in production.

[![](https://substackcdn.com/image/fetch/$s_!89g-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff098d70e-2956-40be-9311-7c133d096cf6_1200x1200.png)](https://substackcdn.com/image/fetch/$s_!89g-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff098d70e-2956-40be-9311-7c133d096cf6_1200x1200.png)

The architecture of a coding-agent harness

Here is how all the components fit together:

You type the request into the TUI. The input goes into the steering queue through the priority gate into the session’s context window. The loop sends the window (with the available tools) to the model through the LLM provider. The model answers with an action — grep for the failing assertion, then edit `stats.py`. Permissions checks if it can execute the tool, the tool executes inside the Sandbox, and the observation is added back into the context window. The loop repeats until the model stops calling tools. During the loop execution, events are streaming back to your terminal in real-time via an async generator (or SSE for remote streaming events).

Next, let’s zoom into the agent loop, where the agent ends and the harness begins, the boundary that defines this entire series.

## The Headless Harness & The Agent Loop

The agent itself is a Pydantic AI agent. A ~20 line definition that composes the model, the tools, the output type and iterates until the model stops calling them. The snippet below is the distilled version of Decode’s loop:

```
from dataclasses import dataclass
from pydantic_ai import Agent, DeferredToolRequests

@dataclass
class AgentDeps:                # the harness state injected into every tool call
    cwd: Path                   # the repo the tools operate on
    emit: EventSink             # streams events to whatever interface is attached
    gate: PermissionGate        # allow / ask / deny, per tool call
    resolve_permission: PermissionResolver  # asks the human when the gate says "ask"

agent = Agent(
    build_model(settings.llm_provider),       # gemini | openrouter | modal
    deps_type=AgentDeps,
    output_type=[str, DeferredToolRequests],   # a turn ends as a final answer (str),
)                                              # or as tool calls paused for approval
register_tools(agent)                          # read, edit, bash, grep, ...

async with agent.iter(prompt, message_history=history) as run:
    async for node in run:                     # model request → tool calls → repeat
        stream_events(node)                    # everything else is the harness
```

Through the `AgentDeps` dataclass we inject harness related components into the loop. The tools are never aware of the interface: TUI or headless. This is what I like to call “a practical clean architecture”, where you are obsessive about separating the serving and infrastructure layers from your core business logic via interfaces and composition.

`output_type` names the only 2 ways a turn can end: a final answer, or tool calls suspended mid-turn waiting for human input.

We will go into all the details about the agent loop, explaining how we hook multiple closed-source/open-source models, the tools and other deps into the loop, in the next article.

These ~20 lines are the *entire* tool-calling LLM agent. The thing people call “the agent” ends here. Everything we build on top of it across 8 lessons is the **coding harness**.

[![The boundary: a tiny tool-calling agent inside a much larger harness.](https://substackcdn.com/image/fetch/$s_!IJV9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0db84995-d395-4854-a4c0-65be5f8915c5_1400x828.png "The boundary: a tiny tool-calling agent inside a much larger harness.")](https://substackcdn.com/image/fetch/$s_!IJV9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0db84995-d395-4854-a4c0-65be5f8915c5_1400x828.png)

Pydantic AI is a thin layer over the model APIs: typed tool definitions, streaming, structured outputs, with no heavy framework between us and our own logic. What makes this a *coding* agent is the tools: read and edit files, run bash, search the codebase, manage a task list, fetch the web, ask the user a question, and spawn subagents. Plus, the LLM specializes in coding. Anthropic is well known for continually optimizing their models for coding tasks. That’s why with every release their models get worse and worse at writing, while better and better at coding.

Still, almost everyone already uses coding agents such as Claude Code or Codex for completely different use cases (including myself): productivity, content creation, finance, sales, marketing. The line between a coding agent and a general-purpose agent is blurry, as any agent needs to natively interact with your computer. How would a harness specialized in writing look? Other than making the LLM sound better. Which is not the harness!

On top of the agent loop, we have 6 modules + compaction that transform the agent loop into a headless harness.

### The Six Modules + Compaction

**LLM Providers** — Decode ships with 3: Modal to serve any type of open-source models (pre-configured or your own fine-tuned version), deployed as **[Modal endpoints](https://modal.com/docs/guide/endpoints?source=decodingai&campaign=harnesseng)** — serverless GPU web endpoints that put the model behind a URL the harness calls like any hosted API, OpenRouter to reach any hosted model behind one API, and Gemini for Google’s free tier for following along. Also, by implementing three providers we can showcase how to swap the model only with a config change, not a rewrite. The loop should never know which model is powering the harness. Clean architecture, remember?

**Sandbox** — an agent that runs bash can break things. We wrap the bash and file-I/O tools to execute inside a sandbox (Docker locally, **[Modal Sandboxes](https://modal.com/docs/guide/sandboxes?source=decodingai&campaign=harnesseng)** remotely) instead of on your machine.

**Permissions** — the permission layer is the most important guardrail: it asks you before running every action, or only the risky ones, depending on the mode. For example, it pauses before a destructive bash command like `rm -rf` and waits for your approval. This is similar to Claude Code’s default, edit, and auto modes.

**Memory** — the iconic AGENTS.md that carries your project instructions plus a MEMORY.md that encodes what the agent learns (e.g. “run the tests with `pytest -x`, never the full suite”). Plain files, deliberately no memory database and no codebase index: the repo is explored dynamically with grep. Just-in-time reads beat a stale heavy index.

**Skills** — the omnipresent skills feature that encodes reusable workflows loaded only when invoked, so the context window doesn’t get bloated with all your instructions at once. The repo already ships a set of skills under `.decode/skills/` that you can try out of the box.

**LSP Server** — a key component of a coding agent. It keeps an index of all your variables and functions. The loop gets syntax and semantic information about the codebase through 2 channels instead of brute-forcing through it or waiting for the code to run. On demand, the model asks where a symbol is defined, who calls it, what its real contract is, and what’s broken in a file. The model gets 1 precise `file:line` answer. After each edit, a fast syntax checker feeds its findings back into the loop. The agent fixes a type error in the same turn, before running/compiling any code. The cheapest feedback loop in the system.

**Compaction** — not a module but a behavior of the harness itself that helps keep the context window as small as possible. The most iconic strategy is to compact the window once it goes over a threshold, squashing the window’s old head into a summary + keeping the recent interactions fresh: `[summary, *tail]`. You can also call this manually via `/compact` or simply clean the whole context window via `/clear`.

That’s the headless harness. Now, let’s plug it into the interfaces you use every day.

## The Interactive Mode

The first is the **TUI**: the interactive mode, a terminal interface wired directly to one live session of the headless harness, in memory, in the same process.

We built it in Python, where `prompt_toolkit` handles input and `Rich` handles output of the terminal experience. It’s append-style, like a conversation log, rather than a full-screen app. Keystrokes go in, and the session’s event stream comes back in real-time via Python generators: streamed text, tool calls, approval prompts.

[![The TUI: an append-style conversation log streamed live from one harness session.](https://substackcdn.com/image/fetch/$s_!GNsc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46cc8b77-6896-405b-ad08-feac403ea3b7_1815x986.png "The TUI: an append-style conversation log streamed live from one harness session.")](https://substackcdn.com/image/fetch/$s_!GNsc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46cc8b77-6896-405b-ad08-feac403ea3b7_1815x986.png)

*The TUI that we will build*

**Why Python?** To be honest, we picked it mostly for teaching purposes.

From my recent poll, I realized that all my audience knows Python. So this makes it accessible to you. But if I were to ship this for real, I’d reach for TypeScript (the language claude-code, OpenCode, and Pi chose) or Go, which compiles to one tidy binary. Still, Aider proves Python can carry a serious coding agent.

And in this series we will focus on the “why”, the design and architecture decisions. Thus, the programming language is not that important and you can easily swap it out for another language.

### The steering queue

What happens when you send a new command and the agent is already mid-task?

Injecting it the moment it’s sent would corrupt a tool call already in flight. Ignoring it makes the agent unsteerable. Every serious harness hits this: Pi drains steering messages mid-turn but follow-ups only at the turn boundary, and claude-code ranks queued input so user messages never starve.

Decode’s answer is the **steering queue + priority gate**. Input is buffered the instant it arrives into the steering queue and injected only at a safe boundary: before the next model call, never mid-tool-call. The gate decides how to process the messages from the queue: steer now, answer later, or abort.

The steering queue can be a simple in memory FIFO queue. No need for a complex queue infrastructure like RabbitMQ.

[![Mid-turn input: buffered in the steering queue, injected only at a safe boundary.](https://substackcdn.com/image/fetch/$s_!_MJf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f58d9ed-d1d9-4550-a8ae-bb08f071e682_2100x735.png "Mid-turn input: buffered in the steering queue, injected only at a safe boundary.")](https://substackcdn.com/image/fetch/$s_!_MJf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f58d9ed-d1d9-4550-a8ae-bb08f071e682_2100x735.png)

*Steering without corruption*

You can already clone the [Decode repository](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course) and try it out for yourself.

You have all the setup instructions in the repo. There are 0 *costs* *to* *try* *it* *out*. *We* *recommend* *starting* *it* *with* *Modal*, *which* *offers*30 in free credit every month.

The experience is similar to what you already know: you run `decode` in any repo and the TUI opens as a fresh session.

We bundled together a few demo’s as skills under `.decode/skills/`, so you can easily try out the coding agent with 0 friction:

[![The demo skills bundled under .decode/skills/, listed inside the TUI.](https://substackcdn.com/image/fetch/$s_!TsnR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92c62af5-78c3-4009-99f3-759c7beba3ed_1816x855.png "The demo skills bundled under .decode/skills/, listed inside the TUI.")](https://substackcdn.com/image/fetch/$s_!TsnR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92c62af5-78c3-4009-99f3-759c7beba3ed_1816x855.png)

*The demo skills bundled under* `.decode/skills/`*, listed inside the TUI.*

Such as creating a snake game:

[![The snake game skill, built and running from a single prompt.](https://substackcdn.com/image/fetch/$s_!irfj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa73cc86c-8e1c-4c1c-ac42-7299fb9cede9_854x819.png "The snake game skill, built and running from a single prompt.")](https://substackcdn.com/image/fetch/$s_!irfj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa73cc86c-8e1c-4c1c-ac42-7299fb9cede9_854x819.png)

Fetching data from a GitHub repo and rendering a web page:

[![GitHub repo data fetched by the agent and rendered into a web page.](https://substackcdn.com/image/fetch/$s_!4v2q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9fe14a6-8adb-4c85-ac6f-8aafbc64ae9e_2328x1902.png "GitHub repo data fetched by the agent and rendered into a web page.")](https://substackcdn.com/image/fetch/$s_!4v2q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9fe14a6-8adb-4c85-ac6f-8aafbc64ae9e_2328x1902.png)

Or something more complex like scraping data from the internet, extracting a knowledge graph of entities and topics and rendering them into a cool visualization:

[![A knowledge graph of entities and topics, scraped from the web and rendered into a visualization.](https://substackcdn.com/image/fetch/$s_!c6fZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0abc6ad-61e0-4594-84c2-2f289327f8a1_3324x1934.png "A knowledge graph of entities and topics, scraped from the web and rendered into a visualization.")](https://substackcdn.com/image/fetch/$s_!c6fZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0abc6ad-61e0-4594-84c2-2f289327f8a1_3324x1934.png)

What if we want to run the agent remotely?

## The Remote Mode

Remote mode keeps the harness headless and runs it on a server through an agent runtime. We use **[Kitaru](https://www.zenml.io/product/kitaru?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=brand)**, the agent runtime built by ZenML, which provides durability, replay and distributed HITL features. Then we ship the Kitaru control plane to GCP via its open-source option. From there, it orchestrates and scales the remote agents, which run on Modal.

This setup lets you run background jobs, scheduled tasks, and full automation pipelines: grab a ticket from Linear, launch 5 to 10 implementations in parallel (each with its own PR), and let a frontier foundation model judge the candidates and rank them for you.

A runtime gives the headless harness [a control plane](https://docs.zenml.io/kitaru/core-concepts/harness-runtime-platform?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=docs): deploy it once, then trigger, monitor, and feed it input remotely, without building any of that plumbing yourself.

[![The Kitaru runtime — the control plane that orchestrates the remote headless agents.](https://substackcdn.com/image/fetch/$s_!HGOX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c126ea-2eeb-480c-89fd-7397a81b6ade_3344x1938.png "The Kitaru runtime — the control plane that orchestrates the remote headless agents.")](https://substackcdn.com/image/fetch/$s_!HGOX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c126ea-2eeb-480c-89fd-7397a81b6ade_3344x1938.png)

*The Kitaru runtime: the control plane that orchestrates the remote headless agents.*

The infrastructure’s moving pieces can get confusing. There are 3 main pieces:

* **The Control Plane**: The runtime that coordinates the headless agents. Powered by Kitaru. Super similar to orchestrators such as ZenML, Prefect or Temporal. That’s why ZenML created Kitaru, specialized in running agentic workflows. Using Kitaru’s open-source Docker image, we will deploy it to GCP.
* **The Execution**: Where the headless agents run: Python environment (local) and Modal (remote).
* **The Sandbox**: Where the tools execute: Docker (local) and Modal (remote).

The runtime [records the run’s progress step by step](https://docs.zenml.io/kitaru/core-concepts/how-it-works?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=docs), so when a sandbox dies mid-task, the run resumes from its last recorded step instead of restarting.

Same reasoning for human input: [the run freezes at a question](https://docs.zenml.io/kitaru/core-concepts/wait-and-input?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=docs), consuming no compute while it waits, and resumes the moment you answer, hours later or from another terminal.

Because every step is recorded, a finished run can be **[replayed](https://docs.zenml.io/kitaru/core-concepts/harness-runtime-platform?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=docs)** with one thing changed (a different model, a fixed prompt) against the original as the baseline.

[![The three planes of a remote run: control, progress record, execution.](https://substackcdn.com/image/fetch/$s_!888f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fce1c73-27d4-4b0d-aca4-1f54916bc228_987x609.png "The three planes of a remote run: control, progress record, execution.")](https://substackcdn.com/image/fetch/$s_!888f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fce1c73-27d4-4b0d-aca4-1f54916bc228_987x609.png)

*The runtime split*

### Try it out

You can run the remote version by going to the [course repo](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course), typing `decode run <your_command>` in your terminal, and opening Kitaru to watch the agent work.

[![Watching a remote run step by step in Kitaru after decode run.](https://substackcdn.com/image/fetch/$s_!uDnx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36c8a3a2-9a7a-4871-b037-8baa7d6dd1ee_3330x1912.png "Watching a remote run step by step in Kitaru after decode run.")](https://substackcdn.com/image/fetch/$s_!uDnx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36c8a3a2-9a7a-4871-b037-8baa7d6dd1ee_3330x1912.png)

*Watching a remote run step by step in Kitaru after* `decode run`*.*

Two modes, one core. That raises the obvious question: why not both at once?

## All the Modes, One Message Bus

We keep Decode simple by keeping the headless harness as the core business logic that can be served in two modes: local and remote.

But you can take this further. OpenCode uses a message bus between the headless harness and every interface to synchronize sessions across their TUI, IDE, WhatsApp, web app, mobile clients. So they all drive the *same* live session: when one interface publishes a message, all the other ones are instantly synced.

[![One remote session, many interfaces, one message bus.](https://substackcdn.com/image/fetch/$s_!JnP3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03e2a9fb-ca73-42c3-a243-33753a725abc_1400x640.png "One remote session, many interfaces, one message bus.")](https://substackcdn.com/image/fetch/$s_!JnP3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03e2a9fb-ca73-42c3-a243-33753a725abc_1400x640.png)

*The topology we explained, but won’t build: one remote session behind a bus, every interface a thin subscriber.*

Whichever mode runs it, one question decides whether any of this is real engineering: can you prove the agent works?

## The Observability and AI Evals Layer

The evals layer answers 3 questions, each with its own mechanism.

[![Three questions, three eval mechanisms, one timeline.](https://substackcdn.com/image/fetch/$s_!_f1O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0300419f-aac0-4e7e-b532-d81835784777_1200x395.png "Three questions, three eval mechanisms, one timeline.")](https://substackcdn.com/image/fetch/$s_!_f1O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0300419f-aac0-4e7e-b532-d81835784777_1200x395.png)

*The evals layer answers three different questions*

Internal benchmarks answer *does it work?* These are the metrics you try to beat with every new feature. You can use public benchmarks such as [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) to compare your agent’s performance against others. But the real deal is to build a custom benchmark suite from your own tasks that optimizes for your specific use case.

Each case is a task instruction, a fresh sandboxed environment, and a hidden oracle test that decides pass or fail. One example case is *“add a* `--json` *flag to* `decode run`*“*, with a hidden pytest asserting the output parses. It’s the same pattern [SWE-bench](https://github.com/swe-bench/SWE-bench) applies to real GitHub issues and [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) applies to terminal tasks.

Your own tasks predict your agent’s usefulness better than any leaderboard.

Regression tests answer *does it still work?* Every new feature re-runs a regression suite and compares scores against the baseline, so a prompt tweak or a new tool can’t silently make the agent worse.

Production evals answer *does it keep working?* Every session is traced with **[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course)**, Comet’s open-source LLM observability platform: each model call, tool call, and token count is a trace, while the conversation is logged as a thread. Live scoring tracks quality in production, where you run a bunch of AI Evals metrics on sampled traces to detect unwanted behavior to create warnings or alarms.

We will also use Opik as our evaluation harness to track our eval datasets and run a coding agent on all the scenarios from the benchmark and regression tests.

[![Opik threads — every session logged as a thread, every model and tool call as a trace.](https://substackcdn.com/image/fetch/$s_!AKa3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40da9e96-3e12-46f9-97eb-4651da6e3e46_3262x1922.png "Opik threads — every session logged as a thread, every model and tool call as a trace.")](https://substackcdn.com/image/fetch/$s_!AKa3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40da9e96-3e12-46f9-97eb-4651da6e3e46_3262x1922.png)

## Next Steps

You’ve seen a bird’s-eye view of what a coding agent looks like: one headless core, a small tool-calling agent inside a much larger harness, 2 modes, and an evals layer that measures performance.

🧑‍💻 We encourage you to **clone our [course repo](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, open your terminal, type **decode** and test out the coding agent.

In the next lesson, we get into the code and start building the agent loop hooked into the TUI.

Here is the **course roadmap,** lesson by lesson *([see all in GitHub](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-course-outline)*):

1. **Building a Coding Agent From Scratch ←** ***you are here***
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)
4. [Context Engineering for Coding Agents](https://www.decodingai.com/p/context-engineering-for-coding-agents)
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

Or the **video** lecture **supporting** **the** **first two lessons**:

*But here is what I’m wondering:*

> ***Which part of your daily coding agent is still a black box to you: the loop, the sandbox, the memory, or something else?***

*Click the button below and tell me. I read every response.*

[Leave a comment](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design/comments)

---

*Enjoyed the article? The most sincere compliment is to restack this for your readers.*

[Share](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

*Special thanks to **[Modal](https://modal.com?source=decodingai&campaign=harnesseng)**, **[Opik (by Comet)](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course)**, and **[Kitaru (by ZenML)](https://www.zenml.io/product/kitaru?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=brand)** for sponsoring this open-source course and keeping it free!*

[![](https://substackcdn.com/image/fetch/$s_!Uq-1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98999460-8389-40b0-9dda-73f934bbf55a_1200x400.png)](https://substackcdn.com/image/fetch/$s_!Uq-1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98999460-8389-40b0-9dda-73f934bbf55a_1200x400.png)

---

#### Whenever you’re ready, here is how I can help you

*Go from agent user to agent builder.* Master the foundations of AI agents and turn fragile demo code into reliable, production-ready systems with my course, **[Agent Engineering: Building Multi-Agent Systems](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)** (made with Towards AI).

35 lessons. Pure foundations from scratch. 4 mini-projects. 2 production systems. A certificate and direct access to me & industry experts in our Discord.

Built for software and data professionals transitioning into AI engineering. *Rated 5/5 with 300+ students. The first 7 lessons are free:*

[Start here](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)

*Not ready to commit?* Start with our **[free Agent AI Engineering Guide](https://email-course.towardsai.net/?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)**, a 6-day email course on the mistakes that silently break AI agents in production.

---

## Images

If not otherwise stated, all images are created by the author.
