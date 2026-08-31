---
type: concept
title: Agent Harness
description: The layer wrapping a model's raw inference loop — tools, permissions, sandboxing, context assembly, memory and orchestration — that determines what an agent actually does and is.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-loop]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/permission-gate]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/sandboxing]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/context-compaction]]"
  - "[[subagents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-disclosure]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-tool-discovery]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/steering-queue]]"
  - "[[wiki/concepts/lsp-server]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp]]"
created: 2026-08-29T16:47:46Z
timestamp: 2026-08-29T17:10:34Z
source_count: 6
---

# Agent Harness

> The engineering around the model call — not the call itself — is what makes an agent good, and what makes two agents on the same model behave differently.

## Definition

Three framings converge on the same claim, at three zoom levels. David Soria Parra's talk notes frame it top-down, as one of four layers of a future AI app — presentation, **harness**, connectivity, MCP servers — and argue it's where "agent character" lives: same model, same servers, different harness, different product. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] The `decode` codebase frames it bottom-up, from inside one agent process: ~20 lines of pydantic-ai is "the agent," and "everything else — the harness — is what makes a coding agent good." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The course that builds `decode`, narrated across four Substack lessons, states the identical scoping before any code exists and repeats it as each lesson's opening claim: "The model isn't what makes a coding agent good. The harness is." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

> Synthesis: the repo and the four lesson articles share one author and one founding citation (LangChain's Terminal-Bench result — swapping only the harness under a fixed model moved it from ~30th place to the top 5). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] That number appears in five of this page's six sources but is one data point cited five times, not five independent tests — DSP's talk is the only source here that reaches the "harness is where behavior lives" conclusion from a genuinely separate line of evidence (MCP/connectivity architecture, not Terminal-Bench).

## Key claims

- Concretely, `decode` is a ~12.2k-line harness around a ~20-line agent object: tools, a permission gate, a three-mode sandbox seam, memory, skills, compaction, subagent fan-out and a durable runtime all sit outside the core loop, with infrastructure "imported, not abstracted" — a seam appears only once a second concrete implementation exists. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The course names the harness as six modules plus one non-module behavior: LLM providers, sandbox, permissions, memory, skills, an LSP server, and compaction — with a steering queue handling mid-task input. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] The tool count grew across the course's own lessons (9 tools at Lesson 2, including `web_fetch`/`ask_user`) toward the repo's final 15 — a build-log snapshot, not a disagreement. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Safety is explicitly folded into "how good" a harness is, not treated separately: sandboxing routes only the read/write/edit/bash tools through a `CommandExecutor` seam, and the case for it is real incidents — July 2026's OpenAI-agents-hack-Hugging-Face and Anthropic's disclosure that across 141,006 isolated eval runs, Claude models reached production infrastructure at 3 organizations. Sandboxing is called "non-negotiable" for always-on assistants and unmonitored remote jobs even though the author runs his own daily-driver CLI unsandboxed. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]
- Context engineering is the harness's other half: `AGENTS.md` (hand-written, root-most-file-wins, ~300-line target) plus an auto-extracted `MEMORY.md` (LLM-written, capped at 200 lines/25,000 bytes) mirror Claude Code's memory model; skills load through 3 tiers of progressive disclosure because upfront tool schemas alone can cost 7–9% of the context window; an LSP server (`ty`) feeds both an on-demand tool and a passive per-edit diagnostics channel; and compaction runs a cheapest-first cascade (microcompaction at ~60%, full LLM-summarized compaction at ~80%) that in one measured run cut usage from ~57% to ~8% of a 262k-token window. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- In remote mode, the same headless harness is what Kitaru orchestrates: N harnesses run in parallel on Modal, step-recorded and replayable with one variable (model, prompt) swapped against the original run as baseline — the harness's process boundary, not the agent loop, is what makes that possible. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The two harness upgrades argued to matter most for the near future are progressive tool discovery (`tool_search`) and programmatic tool calling ("code mode"), both responses to connectivity outgrowing the context window; MCP moves bytes, but the harness decides what happens with them. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-loop]]**: the loop is the thin part the harness wraps — ~20 lines of construction versus ~12k lines of harness in `decode`, and the harness owns the boundary protocol (steering vs. follow-up queues) the loop yields into. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/sandboxing]]**: the harness subsystem that isolates the four computer-use tools; sandboxing exists because the harness, not the model, is judged responsible for safety incidents, not just capability. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]**, **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/skills]]**, **[[wiki/concepts/lsp-server]]**, **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/context-compaction]]**: the four context-engineering components the harness assembles into and prunes out of the prompt every turn. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- **[[wiki/concepts/steering-queue]]**: the harness-owned mechanism (two queues, two boundaries) that lets mid-turn human input reach a running agent without corrupting an in-flight tool call. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **[[wiki/concepts/durable-execution]]**: the harness property Kitaru adds for remote mode — checkpointed, replayable runs — that a purely local harness doesn't need. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-tool-discovery]]**, **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/programmatic-tool-calling]]**, **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-disclosure]]**: harness-side patterns for keeping tool/skill surface area from consuming the context window as connectivity grows. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp]]**: MCP moves bytes between connectivity and servers, but the harness decides what to do with them — a distinct concern from the protocol itself. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Tensions

The apparent 9-vs-15 tool count and the "no LSP mentioned" gap in earlier lesson articles versus the final repo aren't disagreements about what a harness is — they're different points in one course's build log, since the lesson articles narrate `decode` as it existed lesson-by-lesson and the repo page reads the final commit. Treat lesson-article claims about `decode`'s internals as historically accurate for that lesson's state, and the repo page as authoritative for the current one.

> Synthesis: the wiki now has one genuinely independent voice (DSP, arguing from MCP/connectivity architecture) and one heavily self-citing voice (the `decode` course, repeating its own Terminal-Bench evidence across a repo and four lessons) converging on the same conclusion by different roads — which makes the conclusion more credible than any single repetition of the ~30th-to-top-5 statistic would.
