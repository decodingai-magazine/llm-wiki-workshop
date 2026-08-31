---
type: concept
title: Agent Harness
description: The infrastructure built around a coding agent's tool-calling loop — sandbox, permissions, memory, skills, evals, remote execution — with sources disagreeing on whether the loop itself, and skills, sit inside it.
aliases: []
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/code-mode]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/mcp]]"
created: "2026-08-31T19:20:00Z"
timestamp: "2026-08-31T20:05:00Z"
source_count: 3
---

# Agent Harness

> Multiple framings — see Definition

## Definition

The two independent sources define "harness" differently enough to matter,
and a third page — the Decode repo itself — shows one of those framings in
code rather than merely asserting it. The Decode course frames the harness
as everything *around* the tool-calling loop and explicitly excludes the
loop from it: the "agent" is a ~20-line Pydantic AI loop, and "the harness"
is sandboxing, permissions, memory, skills, observability, the steering
queue and the remote runtime — i.e., harness = agent minus loop.
[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
The repo's own architecture diagram draws the exact same line: the bare
`pydantic-ai Agent.iter()` call sits as a "Core" box *outside* the
"Harness" subgraph, while the Runner, the turn handler, the permission
gate, and memory/skills/compaction sit inside it.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
Because the repo *is* the codebase the article describes, this confirms
Decode's claim in code — it is not an independent second voice on the
question.

David Soria Parra's talk (via its notes) instead treats the harness as one
fixed layer in a four-layer application stack — presentation → harness →
connectivity → MCP servers — and puts the **agent loop itself inside** that
layer, alongside two specific engineering patterns: progressive tool
discovery and code mode. Skills, in this framing, belong to the separate
Connectivity layer downstream of the harness, not to the harness.
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Key claims

- In a LangChain test on Terminal-Bench, changing only the harness (same
  model) moved a coding agent from roughly 30th place into the top 5 — cited
  as the reason to treat the harness, not the model, as the object of design.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Decode's harness is organized into six modules — LLM Providers, Sandbox,
  Permissions, Memory, Skills, and an LSP server — plus a Compaction
  behavior; the repo's actual code splits these further into `harness/`
  (Runner + steering/follow-up queues), `agent/` (loop + factory), `tools/`,
  `context/` (compaction), `runtime/` (Kitaru) and `observability/`,
  confirming the same components at finer grain.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Mid-task input handling (a steering queue + priority gate that only injects
  new input at a safe boundary) is harness-level work; Claude Code and Pi are
  cited as having solved the same problem. In Decode this is implemented as
  two turn-boundary hooks — a `MODEL_REQUEST` boundary drains queued
  steering text into the next prompt, and a `WOULD_STOP` boundary drains
  queued follow-up text before the turn ends or continues.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Compaction is a two-tier cascade in the actual code — a no-LLM
  microcompaction that blanks stale tool-output bodies at a lower
  occupancy threshold, then a full LLM compaction that replaces history
  with `[summary, *tail]` at a higher one — refining the article's
  single-tier description of the same behavior.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The harness also owns subagent fan-out: the one model-callable `agent`
  tool spawns up to 6 read-only Explore subagents that re-enter the same
  installed agent with narrowed permissions — a harness responsibility not
  named in the article's six-module list.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Progressive tool discovery — loading a `tool_search`-style capability up
  front instead of every tool schema — is a harness-side responsibility;
  Claude Code shipped it and saw a large drop in tool-context usage.
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Code mode (programmatic tool calling) — a model-written script in a sandbox
  that composes tool output directly, instead of round-tripping call→inspect→
  call — is the other pattern named as now living in the harness.
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Tensions

- **Does the harness include the agent loop?** Decode's framing draws a hard
  line: the loop is "the agent," the harness is everything else.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
  Soria Parra's four-layer stack puts the loop *inside* the harness layer,
  alongside discovery and code mode.
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- **Does the harness include skills?** Decode counts Skills as one of its six
  harness modules. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
  Soria Parra's diagram places Skills one layer downstream, under
  Connectivity, alongside CLIs and MCP clients — not inside the harness.
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/entities/claude-code]]**: the reference implementation both
  independent sources point to — for its steering-queue priority gate in
  one, and for shipping progressive tool discovery in the other.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]],
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- **[[wiki/entities/decode]]**: the concrete implementation of the Decode
  side of this page — its own architecture diagram nests the turn handler,
  permission gate, and memory/skills/compaction inside "Harness" and keeps
  the bare `Agent.iter()` core outside it, matching the article's
  harness-minus-loop split.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/skills]]**: a harness module in Decode's framing —
  confirmed by the repo's own diagram, which nests Skills inside "Harness" —
  versus a separate connectivity-layer primitive in Soria Parra's framing;
  see Tensions.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/code-mode]]** and **[[wiki/concepts/progressive-tool-discovery]]**:
  the two patterns Soria Parra names as now living inside the harness layer.
  [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- **[[wiki/concepts/agent-memory]]** and **[[wiki/concepts/orchestration]]**:
  named as Decode harness modules (Memory) and as the remote-execution
  concern the harness delegates to Kitaru (orchestration); the repo adds a
  third orchestration-flavored harness responsibility — bounded subagent
  fan-out.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: Adding the Decode repo brings this page's source count to
> three, but not to three independent voices — the repo is the codebase the
> article describes, so it corroborates Decode's side of the loop/skills
> tensions in code rather than adding a new standpoint. The live
> disagreement is still two-sided: Decode (harness = agent minus loop,
> skills included) versus Soria Parra's four-layer stack (loop inside the
> harness layer, skills one layer downstream) — and that is still not
> settled.
