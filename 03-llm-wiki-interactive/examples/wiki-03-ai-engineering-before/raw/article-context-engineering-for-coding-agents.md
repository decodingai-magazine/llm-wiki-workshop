---
title: "Context Engineering for Coding Agents"
subtitle: "The 4 harness components that keep your context window high-signal."
authors: ["Paul Iusztin"]
published_date: "2026-08-25T05:01:37+00:00"
source_url: https://www.decodingai.com/p/context-engineering-for-coding-agents
origin: article
fetched: 2026-08-29T17:01:12Z
---

# Context Engineering for Coding Agents

*The 4 harness components that keep your context window high-signal.*
# Context Engineering for Coding Agents

### The 4 harness components that keep your context window high-signal.

[![Paul Iusztin's avatar](https://substackcdn.com/image/fetch/$s_!pQz0!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0714d360-396c-4b41-a676-1b58dc1dc5f3_1470x1470.jpeg)](https://substack.com/@pauliusztin)

[Paul Iusztin](https://substack.com/@pauliusztin)

Aug 25, 2026

***Every AI application that wraps an agent is a harness!***

In LangChain’s Terminal-Bench experiment, changing only the harness (with the same model) moved a coding agent from ~30th place into the top 5: the harness, not the model, is what makes a coding agent good.

In the **open-source course** **[Building a Coding Agent From Scratch](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, you’ll build that harness from scratch in Python: **Decode**, a complete coding agent that grows lesson by lesson from a bare agent loop into a swarm of remote agents running in parallel in the cloud.

**Why?** You’ll be able to engineer custom harnesses for your own AI products (the skill behind that leaderboard jump), and you’ll understand what Claude Code and Codex actually do under the hood, turning you into a power user.

[![](https://substackcdn.com/image/fetch/$s_!ge05!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)](https://substackcdn.com/image/fetch/$s_!ge05!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)

**Lessons:**

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)
4. **Context Engineering for Coding Agents** **←** ***You are here***
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

[Full open-source course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

# Lesson 4: Context Engineering for Coding Agents

[![What you carry is what you can move with. The craft is in what you leave on the bench.](https://substackcdn.com/image/fetch/$s_!7tX-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544e7250-15d4-4cc8-bc3d-b30f3e8e16db_1376x768.png "What you carry is what you can move with. The craft is in what you leave on the bench.")](https://substackcdn.com/image/fetch/$s_!7tX-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544e7250-15d4-4cc8-bc3d-b30f3e8e16db_1376x768.png)

I got hooked on running Claude Code agents 24/7. Getting things done while answering emails, cooking, or watching a movie. Until my subscription maxed out mid-turn with the agent halfway through a feature. Sounds familiar?

Complaining to your employer, buying a bigger subscription, changing the model, or switching harnesses only treats the symptom. Doesn’t solve the root cause. You spend money while the window stays noisy, degrading output no matter whose model is behind it.

The actual solution is to better understand harnesses and the context engineering behind them. Improve planning, develop stronger skills and memory, and know when to drop your context.

So far in the course, we have focused on harness engineering and building a sandboxed agent loop. Now it’s finally time for some context engineering for coding agents: memory, skills, LSP servers and compaction.

The whole problem resolves to what to put into context, what not to put, how to trim it down, plus creating as many feedback loops as possible for the agent, as Anthropic frames it as [finding the smallest possible set of high-signal tokens](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

You will walk away understanding and building from scratch:

* What the agent should carry between sessions.
* How skills load nothing until needed.
* The cheapest feedback loop in the system.
* How the window gets trimmed before it rots.

## The context lifecycle of a session

To see how the 4 components cooperate, look at the `demo-5-sandbox-feature-pr` skill from the course repo (`.decode/skills/demo-5-sandbox-feature-pr`), where we encoded a demo where **Decode** writes a new feature into Decode by spinning up a background sandboxed session, where the host agent acts as the orchestrator and the sandboxed one as the feature executor. The final artifact from the demo will be a PR containing the new feature.

Go to [repository](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course), run `decode`, type `/demo-5-sandbox-feature-pr`, and enter. Let Decode do the rest of the work.

[![skill demo](https://substackcdn.com/image/fetch/$s_!U0HN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa54ad14-87da-4731-bd5e-b3e2d310f634_1200x374.png "skill demo")](https://substackcdn.com/image/fetch/$s_!U0HN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa54ad14-87da-4731-bd5e-b3e2d310f634_1200x374.png)

Here is a snapshot of the skill, where Decode spawns another Decode subagent:

```
...

## 1. Launch decode against a sandboxed clone of the course repo

Launch the local Docker run (Docker must be running):

"""
SANDBOX_MODE=docker decode --repo git@github.com:decodingai-magazine/building-a-coding-agent-from-scratch-course.git
"""

...
```

At session start, the system prompt is assembled from four parts: the base prompt, the active agent’s prompt, memory files (`AGENTS.md` + `.decode/MEMORY.md`), and the skills catalog (one line per skill). Pydantic AI adds each tool’s schema, paying off [Lesson 2’s warning](https://www.decodingai.com/p/the-coding-agent-loop) that every tool costs tokens. This assembled prompt enters context, shaping the probabilities of the model’s next steps.

The run fills the window. Invoking the skill loads its `SKILL.md` body (tier 2 of progressive disclosure). Plan mode dumps repo files as `read` outputs. During the build loop, each `edit` lands, the Diagnostics Enricher appends type errors for free, and `bash` runs tests until green output signals completion.

*Now, from the context window point of view, what happens within the harness?*

As in the image below, as soon as we open the agent, the context window is filled with its system prompt, tool and skill descriptions and memory files. After invoking the `/demo-5-sandbox-feature-pr` skill, it gets filled with tool inputs and outputs, plus the SKILL.md file containing the specific instructions.

Next, through progressive disclosure, the agent begins reading the relevant files and scripts associated with the skills. Ultimately, it starts writing new Python files or editing existing ones that are statically checked for syntax issues via our `ty` Language Server Protocol (LSP) server.

[![The context lifecycle — what each iteration of one session appends to the window.](https://substackcdn.com/image/fetch/$s_!pnf_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc59b6055-6ca8-49b1-b716-c8a8f023f987_1200x455.png "The context lifecycle — what each iteration of one session appends to the window.")](https://substackcdn.com/image/fetch/$s_!pnf_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc59b6055-6ca8-49b1-b716-c8a8f023f987_1200x455.png)

The context lifecycle of a coding agent

On Modal’s self-hosted `Qwen3.6-35B`, the window is 262,144 tokens. Usually, microcompaction fires at 60%, while full compaction is at 80%. After compaction, usage drops back to roughly 5–10%, so the session continues instead of crashing.

In the video below, you can see part of the 219 spans trace in [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course), clearly monitoring the LLM tool calls, token counts, and latency of the harness and LLM calls:

Every component in this lifecycle has specific mechanics: memory, skills, the LSP server, and compaction. Let’s explore each.

## Memory: Stop repeating your instructions

In my early agent runs, the agent kept writing naive datetime objects instead of timezone-aware ones and added type hints inconsistently, forcing me to retype the same corrections session after session. The fix was to write the preference down once into the `AGENTS.md`, where the agent reads it every turn.

[![The two memory files — one you write by hand, one that writes itself.](https://substackcdn.com/image/fetch/$s_!mNNY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5fa3410-408d-4668-a13b-5bdeb47650f5_1200x600.png "The two memory files — one you write by hand, one that writes itself.")](https://substackcdn.com/image/fetch/$s_!mNNY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5fa3410-408d-4668-a13b-5bdeb47650f5_1200x600.png)

`AGENTS.md` *(the one you write by hand) vs.* `.decode/MEMORY.md` *(the one the agent extracts from each session).*

`AGENTS.md` injects project context: business logic, why components exist, the tech stack, and the processes around it (docs, deploy, review, testing). The code is the source of truth, so avoid duplicating it. Add metadata and references the agent can discover without heavy reasoning.

Keep it under 300 lines, with a guardrail of around 600 lines. Write each line in response to an observed mistake so the agent avoids repeating it, following [Mitchell Hashimoto’s rule](https://mitchellh.com/writing/my-ai-adoption-journey).

Decode recursively looks within all the project directories for `AGENTS.md` files (root-most first, so the nearest file takes precedence), appends `.decode/MEMORY.md` last, stamps each with a `# From <path>` provenance header, and dumps the result into the system prompt.

If `AGENTS.md` is what you manually define, `.decode/MEMORY.md` is what the agent automatically extracts from your conversations, replicating Claude Code’s auto-memory

At the end of each session — on quit and on `/clear` — one cheap LLM call summarizes the session into a single plain sentence, appended as a dated bullet (`- 2026-06-26: …`), as an append-only log. As this can grow big fast, the file has a hard cap of 200 lines or 25,000 bytes, dropping the oldest lines first.

*From [src/decode/memory/extract.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/memory/extract.py):*

```
async def extract_on_exit(messages: list[ModelMessage], cwd: Path) -> None:
    summary = await summarize_session(messages, model_or_settings=settings)
    append_session_summary(cwd, summary, now=_utc_now())

    if settings.memory_compression_enabled:
        await compress_memory_file(cwd, model_or_settings=settings)
```

`summarize_session` is the single LLM call that distills the conversation into one sentence (or `None` if it’s not worth saving). `append_session_summary` writes that sentence into `.decode/MEMORY.md` and enforces the hard cap.

`compress_memory_file` runs **Memory Compression** to rewrite the file in place, merging duplicate or superseded notes while preserving dated bullets.

## Skills: Never load what you can reference

My Python testing and PR conventions used to live directly in my memory file, bloating the context of every session. Moving them into skills left behind just a few lines, as references, that specify when to access each one.

Skills prevent context rot from 2 directions. On the tools side, upfront schemas burn budget: [Mario Zechner measured that popular MCP servers consume 7–9% of the context window](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/) before any work begins. On the memory side, stuffing review guides and workflow templates into `AGENTS.md` pollutes every turn. Skills solve both: each phase-specific behavior lives in its own skill, referenced from a one-line catalog entry, and loads only when that workflow phase runs.

[![The three tiers of progressive disclosure, seen inside the context window.](https://substackcdn.com/image/fetch/$s_!zEr0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d0163ba-5206-4477-a774-4a2593499b42_1200x600.png "The three tiers of progressive disclosure, seen inside the context window.")](https://substackcdn.com/image/fetch/$s_!zEr0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d0163ba-5206-4477-a774-4a2593499b42_1200x600.png)

The 3 tiers of loading a skill and its bundled files into the context window

Skills follow the [Agent Skills standard](https://agentskills.io/home). In Decode, skills live in `.decode/skills/`, or you can open the TUI, type `/`, and pick one. A separate public registry lives at [skills.sh](https://www.skills.sh/) (`npx skills install <skill>`):

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

**Progressive disclosure** operates across **3 tiers**. In **tier 1**, only the skills catalog stays in context: one `name + description` line per skill. As your library grows, an optional guard can cap the catalog at ~1% of the context window.

[![The tier-1 skills pipeline — descriptions gathered into a catalog, optionally capped, wrapped into the system prompt.](https://substackcdn.com/image/fetch/$s_!xhAh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd4e626a-873a-40a9-8ca8-9255652381cb_1200x292.png "The tier-1 skills pipeline — descriptions gathered into a catalog, optionally capped, wrapped into the system prompt.")](https://substackcdn.com/image/fetch/$s_!xhAh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd4e626a-873a-40a9-8ca8-9255652381cb_1200x292.png)

*Loading the skills catalog into the system prompt.*

A common strategy Decode doesn’t have yet is user-invocable-only skills, where you flag a skill as callable only. This means you can remove its name and description from the catalog, leaving it with zero context until explicitly invoked by the user.

In **tier 2**, invoking a skill via the `skill` **dispatcher tool** or `/<skill-name>` loads only its `SKILL.md` body and any other files packed within the skill.

*From [src/decode/tools/skills.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/skills.py):*

```
async def skill(ctx: RunContext[AgentDeps], name: str) -> str:
    home = ctx.deps.harness_home or ctx.deps.cwd
    catalog = load_skills(home)
    found = catalog.get(name)

    return format_skill_payload(found, cwd=home)
```

In **tier 3**, because within `format_skill_payload` we properly format and expose all the available resources (files, scripts, docs, assets) from a skill to the agent, if it considers them necessary, it will load them via its read tool or execute the containing scripts via the bash tool.

This is the core idea of progressive disclosure. It’s mostly just exposing a manifest of bundled files with exact cwd-relative paths, making it super clear to the agent how to access them. The key here is that the LLM is properly trained for tool calling to make the right decisions about whether to call read or bash tools.

*From [src/decode/skills/payload.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/skills/payload.py):*

```
def format_skill_payload(skill: SkillDef, *, cwd: Path) -> str:
    if skill.resource_dir is None:
        return f"{skill.body}\n\n{_OUTPUTS_TRAILER}"
    rel_dir = os.path.relpath(skill.resource_dir, cwd)
    files = _bundled_files(skill.resource_dir)
    
    listing = "\n".join(f"- {rel_dir}/{name}" for name in files)
    trailer = (
        f"Bundled files for this skill (all under `{rel_dir}/` — use these EXACT paths):\n"
        f"{listing}\n"
        "Read them with the `read` tool; run `scripts/` files with `bash`."
    )

    return f"{skill.body}\n\n{trailer}\n\n{_OUTPUTS_TRAILER}"
```

Now let’s look at the cheapest feedback loop in the whole coding agent.

## The LSP server: Replace guessing with precision

In my multi-agent setup, each turn between the engineer and tester agents re-ran the linter, type checker, formatter, and test suite. My Prefect orchestrator integration tests took 15 minutes on their own, so I split them to speed up the feedback loop.

The takeaway was clear: the most important part of your agentic flow is to always give as many feedback loops as possible. **The LSP server is the fastest way to feed in code-related signal.**

An LSP server is one of the most underrated components, particularly for coding harnesses. It maintains a live index of symbols across your codebase: variables, functions, classes, definitions, references, and type errors. Your IDE already runs one per language. You need one for each programming language. Decode uses [ty by Astral](https://github.com/astral-sh/ty), an extremely fast type checker and language server written in Rust, to support Python. Made by the same guys behind uv and ruff.

The server feeds the agent signal through 2 channels.

[![Two ways into one LSP server — the agent asks, or the edit asks on its behalf.](https://substackcdn.com/image/fetch/$s_!N2P_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffa5c0a8-ed47-4023-8ba1-6537bf9ba0a3_1200x515.png "Two ways into one LSP server — the agent asks, or the edit asks on its behalf.")](https://substackcdn.com/image/fetch/$s_!N2P_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffa5c0a8-ed47-4023-8ba1-6537bf9ba0a3_1200x515.png)

*The two LSP channels. 1. The agent queries the* `lsp` *tool on demand 2. Every Python edit/write passively pulls diagnostics.*

**Channel 1** is the `lsp` **tool**, which handles active queries with 4 ops: `definition`, `references`, `hover`, and `diagnostics`. One call returns a precise `file:line:column` answer instead of 3 speculative file reads. It’s read-only, so the permission gate auto-allows it across all modes.

*From [src/decode/tools/lsp.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/lsp.py):*

```
async def lsp(
    ctx: RunContext[AgentDeps],
    op: str,
    path: str,
    line: int | None = None,
    column: int | None = None,
) -> str:
    if op == "definition":
        return await _run_definition(ctx, path, line, column)
    if op == "references":
        return await _run_references(ctx, path, line, column)
    if op == "hover":
        return await _run_hover(ctx, path, line, column)
        
    return await _run_diagnostics(ctx, path)

async def _run_definition(ctx: RunContext[AgentDeps], path: str, line: int, column: int) -> str:
    result = await lsp_service.definition(ctx.deps.cwd, path, line, column)

    return _format_location(result)
```

The server runs as a background process at each project root, communicating via JSON-RPC (a plain request/response protocol over standard input/output). Decode’s `LspClient` initializes the session, negotiates capabilities, and sends requests:

*From [src/decode/services/lsp/service.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/services/lsp/service.py):*

```
from decode.services.lsp.client import LspClient


process = await asyncio.create_subprocess_exec(
    "ty", "server",
    stdin=PIPE, stdout=PIPE, cwd=root,
)
client = LspClient(process, root)
await client.initialize()
```

In the `demo-5` session, the agent resolves the entry point via `lsp("definition", "src/decode/cli.py", <line>, <column>)` over JSON-RPC `textDocument/definition`. On the next turn, the model targets its edit tool call at that exact location, rather than blindly exploring the codebase first.

**Channel 2** is the **Diagnostics Enricher**, which runs passively on every successful `.py` write or edit to append an errors-only block to the tool result. It displays at most 10 errors, and stays silent on clean files or when the server is unavailable, matching the pattern in [OpenCode](https://github.com/anomalyco/opencode).

`_enrich` wraps the return value of file modification tools without requiring extra turns or tools.

*From [src/decode/tools/files.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/files.py):*

```
def _enrich(base: str, cwd: Path, path: str) -> str:
    summary = _format_lsp_errors(lsp_service.diagnostics_on_edit(cwd, path))
    if summary is None:
        return base
    return f"{base}\n\n{summary}"

def _format_lsp_errors(diagnostics: list[Diagnostic] | None) -> str | None:
    ...
    errors = [d for d in diagnostics if d.severity == _LSP_ERROR_SEVERITY]
    shown = errors[:_LSP_DIAGNOSTICS_LIMIT]
    lines = [f"LSP diagnostics ({settings.lsp_server_command}) — fix these:"]
    ...
    return "\n".join(lines)
```

In the `demo-5` session, when the agent updates `src/decode/cli.py` with an unimported reference, the file writes successfully, but the enricher appends `LSP diagnostics (ty) — fix these: ...` with the error details. The model sees this feedback immediately and fixes the import on the next `edit` before running any tests.

In the video below, you can clearly see in [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course) how the LLM outputs LSP tool calls and how they are executed in the harness:

Memory, skills, and the LSP all shape what enters the window. Now let’s see how we can trim it down.

## Compaction: Delete before the window rots

Back in Nov 2025, when building the writing agent for my agent engineering course, requests started degrading around 180,000 input tokens on Gemini Pro, taking>3 minutes per request or directly returning timeout errors and disconnections. Considering that on paper Gemini handles up to 1M input tokens.

A full window degrades model performance and reliability long before hitting the hard token ceiling, following the [degradation curves documented by Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). That’s why you need compaction to continually reduce your context window while minimizing context loss.

Compaction handles this in 3 ways. The simplest is `/clear`, which wipes the entire window after running the on-exit memory write-back so key learnings persist in `.decode/MEMORY.md`.

[![The three compaction modes and what each one leaves in the window.](https://substackcdn.com/image/fetch/$s_!apDX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63c3ab58-49a6-4264-a317-249b97680134_1200x815.png "The three compaction modes and what each one leaves in the window.")](https://substackcdn.com/image/fetch/$s_!apDX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63c3ab58-49a6-4264-a317-249b97680134_1200x815.png)

*The three compaction modes:* `/clear` *keeps only the system prompt,* `/compaction` *rebuilds it as summary plus tail, and* `/microcompaction` *swaps old tool outputs for placeholders in place.*

The second option is **full compaction**, triggered automatically at 80% capacity or manually via `/compact`. An LLM summarizes the conversations into a six-part template (goal, constraints & preferences, progress, key decisions, next steps, critical context), and older messages are dropped. The window becomes `[system prompt] + [summary] + [recent tail]`, where the tail retains ≈20,000 tokens of recent messages snapped cleanly to a **Compaction Boundary** so tool calls remain paired with their results, matching [Pi’s implementation](https://github.com/earendil-works/pi).

Both tiers evaluate `should_compact` using the provider’s reported token window against reserve thresholds (80% full compaction ->20% empty, 60% microcompaction -> 40% empty):

*From [src/decode/context/compaction.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/context/compaction.py):*

```
def should_compact(usage: RunUsage, *, window: int, reserve: float, enabled: bool) -> bool:
    if not enabled:
        return False
    if usage.input_tokens <= 0:
        return False
    return usage.input_tokens >= reserve_threshold(window, reserve)
```

Everything happens within the `compact()` method from `AgentTurnHandler`. `split_tail` walks backward through message history estimating token counts to locate the Compaction Boundary. `summarize_for_compaction` generates the summary, `build_summary_message` wraps it as a synthetic user message that is itself part of the history the next compaction summarizes (so successive compactions merge for free), and the handler sends `[summary_message, *tail]` on the next loop iteration. The harness owns the list it feeds the model, so replacing the list IS the compaction:

*From [src/decode/agent/loop.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/agent/loop.py):*

```
class AgentTurnHandler:
    ...

    async def compact(self) -> CompactOutcome:
        split = split_tail(
            self.message_history, keep_recent_tokens=settings.compaction_keep_recent_tokens
        )
        skeleton = await summarize_for_compaction(
            self.message_history, model=self._compaction_model
        )

        before_tokens = self._last_input_tokens
        summary_message = build_summary_message(skeleton)
        tail = self.message_history[split:]

        self.message_history = [summary_message, *tail]

        return CompactOutcome.COMPACTED
```

The 3rd and last option is **microcompaction**, which runs without LLM calls at 60% capacity. It replaces tool outputs outside the recent tail with a placeholder string by inspecting each `ToolReturnPart` (the message part that holds a tool’s output). Because tool outputs are consumed each turn, conclusions live on in subsequent messages. Nothing is lost because the tool input remains available in the messages, allowing the agent to rerun the tool if necessary. That is why [Anthropic calls tool-result clearing the safest, lightest touch of compaction](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

After every completed turn, the handler checks the same number against both thresholds: full compaction first, then `microcompact`, replacing `message_history` through the same reassignment.

*From [src/decode/context/compaction.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/context/compaction.py):*

```
_MICRO_PLACEHOLDER = "[tool output elided by microcompaction]"

def microcompact(
    messages: list[ModelMessage],
    *,
    keep_recent_tokens: int,
    placeholder: str = _MICRO_PLACEHOLDER,
) -> list[ModelMessage]:
    boundary = split_tail(messages, keep_recent_tokens=keep_recent_tokens)

    new_messages: list[ModelMessage] = []
    for index, message in enumerate(messages):
        if index >= boundary or not isinstance(message, ModelRequest):
            new_messages.append(message)
            continue

        new_parts = list(message.parts)
        changed = False
        for position, part in enumerate(message.parts):
            if not isinstance(part, ToolReturnPart | RetryPromptPart):
                continue
            new_parts[position] = dataclasses.replace(part, content=placeholder)

        new_messages.append(dataclasses.replace(message, parts=new_parts))

    return new_messages
```

When saving the session to JSONL files, there is no compaction. The file is a simple snapshot of the entire message history. To save a compacted session, you either have to run it before exiting the session or resume, run it and then exit.

In the image below, you can see how the `/compact` command reduced the context window from `◑ 57%` (~149539) to 8% of the context window.

[![](https://substackcdn.com/image/fetch/$s_!_ExA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa16b6e09-7ab9-48e7-a208-c20bb0ac32e4_1173x445.png)](https://substackcdn.com/image/fetch/$s_!_ExA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa16b6e09-7ab9-48e7-a208-c20bb0ac32e4_1173x445.png)

## Next steps

There are other components we haven’t touched on in this article, such as an MCP client or an auto-mode permission layer. Still, these are the 4 harness components that are omnipresent in every coding harness you will use. Maybe Pi, with its minimalist design, is the only exception.

🧑‍💻 We encourage you to **clone our [course repo](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, open your terminal, type **”decode”**,and test out the coding agent.

Within the next lesson, we will add the final harness piece to the puzzle: creating an agent’s catalog used to fan out subagents whose work never pollutes your window.

Here is the **course roadmap,** lesson by lesson *([see all in GitHub](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-course-outline)*):

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)
4. **Context Engineering for Coding Agents ← You are here**
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

*But here is what I’m wondering:*

> ***When your coding agent’s window fills up mid-task, what do you actually do today:*** `/clear` ***and lose the thread,*** `/compact` ***and hope the summary gets the job done, or just keep going until it degrades?***

*Click the button below and tell me. I read every response.*

[Leave a comment](https://www.decodingai.com/p/context-engineering-for-coding-agents/comments)

---

*Enjoyed the article? The most sincere compliment is to restack this for your readers.*

[Share](https://www.decodingai.com/p/context-engineering-for-coding-agents?utm_source=substack&utm_medium=email&utm_content=share&action=share)

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

## Images & videos

If not otherwise stated, all images are created by the author.
