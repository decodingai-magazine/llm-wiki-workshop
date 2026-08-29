---
type: source
title: System architecture of future AI apps — presentation, harness, connectivity, MCP servers
description: A four-layer architecture breakdown of where AI apps are converging, with the harness-side patterns (progressive discovery, code mode) that make the rest work.
origin: local
original_path: data_input_examples/notes/02-medium/System architecture of future AI apps UI-TUI-IDE extension ↔ harness ↔ connectivity.md
source_url: null
authors: []
published_date: null
raw_file: raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension.md
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/anthropic]]"
  - "[[wiki/entities/david-soria-parra]]"
  - "[[wiki/entities/fastmcp]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/mcp-apps]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/governance]]"
  - "[[wiki/concepts/durable-execution]]"
---

# System architecture of future AI apps — presentation, harness, connectivity, MCP servers

> [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension|Raw]] · local

## Summary

A worked-out architecture note derived from the same conference talk as
[[wiki/sources/the-future-of-mcp-vs-skills]], but written as a system architect's
reference rather than as talk notes. Four layers, each decomposed so that
capability, UI and domain knowledge can travel independently of where the agent
runs: **presentation** (web, TUI, IDE extension) reduced to a renderer of
contracts shipped from elsewhere; the **harness** holding the inference loop,
context management, memory, permissions and sandboxing; **connectivity** as three
coexisting mechanisms; and **MCP servers** as small product surfaces.

Its most useful contribution is naming the two harness-side patterns as
harness-side. Progressive discovery replaces "load 100 tool schemas" with one
`tool_search` capability the model queries when it needs something — the note
prices the difference as ~50K tokens versus ~200 tokens plus a 300-token schema
load, and insists the protocol already supports this: "the protocol is not the
problem, the client is." Code mode replaces model-driven tool sequencing with a
script written by the model in a sandbox, using MCP structured output for type
information.

The connectivity section gives the sharpest mental model in the wiki: **CLIs are
how the agent talks to the local computer, skills are how the agent remembers what
it knows, MCP is how the agent talks to everything else.** The server section
repeats the anti-REST-wrapper argument with a concrete alternative — Cloudflare
exposing one code-execution tool instead of eighty endpoint tools — and the
cross-cutting sections cover authorization propagation, discovery and async
work. It closes with a build checklist per layer, and four open questions,
including the one the wiki cannot yet answer: how a harness should arbitrate when
a skill, a CLI and an MCP tool all offer the same capability.

## Key claims

- Progressive discovery is a harness responsibility that the protocol already supports, and most harnesses have not built it. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#3.1 Progressive Discovery|cite]]
- "The protocol moves bytes; the harness decides what to do with them" — same model plus same servers plus a different harness gives a wildly different product. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#3. Layer 2 — The Harness|cite]]
- Bash pipes are code mode that predates the term: `gh pr list | jq | xargs` is real programmatic tool calling. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#4.2 CLIs — Pre-Trained Surfaces, Bash-Composable|cite]]
- Wrapping a pre-trained CLI in an MCP server is often a regression — you lose the model's prior knowledge for a thinner interface. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#4.2 CLIs — Pre-Trained Surfaces, Bash-Composable|cite]]
- Design task-shaped tools (`schedule_meeting_with_summary`), not endpoint-shaped ones (`POST /calendars/{id}/events`). [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#5.1 Stop Wrapping REST APIs One-to-One|cite]]
- Knowledge-worker agents cannot use blocking tool calls the way coding agents could — async tasks need a protocol answer, a runtime answer and a UI answer. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#6.3 Async & Long-Running Work|cite]]
- Presentation surfaces differ in what they can render, which is why the protocol has an explicit extension mechanism: a TUI cannot render an HTML MCP app. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#2. Layer 1 — Presentation (UI / TUI / IDE Extension)|cite]]

## Notable quotes

> "CLIs are how the agent talks to the local computer. Skills are how the agent remembers what it knows. MCP is how the agent talks to everything else, especially other systems' stuff."
> — [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#4.3 MCP Clients — The Connective Tissue|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/claude-code]], [[wiki/entities/anthropic]], [[wiki/entities/david-soria-parra]], [[wiki/entities/fastmcp]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/connectivity-stack]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/programmatic-tool-calling]], [[wiki/concepts/mcp-apps]], [[wiki/concepts/mcp-server-design]], [[wiki/concepts/mcp-primitives]], [[wiki/concepts/cli-tools]], [[wiki/concepts/agent-skills]], [[wiki/concepts/skills-over-mcp]], [[wiki/concepts/governance]], [[wiki/concepts/durable-execution]]

> Synthesis: This and [[wiki/sources/the-future-of-mcp-vs-skills]] share an origin, so treat overlapping claims as one voice — what is genuinely new here is the layer assignment: which of these problems belongs to the harness rather than to the protocol.
