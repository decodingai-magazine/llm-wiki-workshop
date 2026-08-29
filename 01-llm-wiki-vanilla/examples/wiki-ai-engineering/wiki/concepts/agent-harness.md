---
type: concept
title: Agent harness
description: The runtime layer that owns the LLM–tool loop, memory, permissions and orchestration — and the layer users now swap the way they once swapped editors.
aliases: [Harness, Runtime]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/entities/claude-code]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 5
---

# Agent harness

> The brain between a thin renderer and the servers: where the LLM–tool loop, memory, permissions and orchestration live.

## Definition

In the four-layer model the harness plus runtime sits under the presentation
layer and above connectivity, and it owns everything stateful about the agent —
the loop, memory, permissions, orchestration
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]. The
second source adds the property that matters commercially: the harness is
**interchangeable**. "Choose your harness of choice: Claude Code, OpenCode,
OpenClaw" is only possible because the knowledge and the data live outside it
[[wiki/sources/why-mcp-is-not-dead]].

## Key claims

- The harness owns the LLM↔tool loop, memory, permissions and orchestration. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Agents are becoming long-running systems rather than single inference calls, which pulls durable execution, retries, checkpoints, approvals and observability into the runtime. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Harnesses are swappable, and keeping data in your own storage behind a server is what keeps them swappable. [[wiki/sources/why-mcp-is-not-dead]]
- Presentation is a thin renderer over this layer — TUI, IDE extension, web or desktop — not a place for logic. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Beyond the loop, the harness owns context management and compaction, the permission model, memory and audit. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Progressive discovery and code mode are harness responsibilities that the protocol already supports — most harnesses simply have not built them. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Harness-specific features (skills, hooks) are progressive enhancements layered over a portable MCP server, and must degrade gracefully. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The commoditization claim in reverse: if harnesses are interchangeable, the thing worth investing in is the memory they plug into. [[wiki/sources/owning-your-context-layer]]

## Relationships

- **[[wiki/entities/claude-code]]**: the harness the notes actually run.
- **[[wiki/concepts/durable-execution]]**: the property that turns a loop into a runtime.
- **[[wiki/concepts/connectivity-stack]]**: what the harness reaches through.

> Synthesis: "Harness" is doing quiet strategic work in these notes — it names the layer you should be able to replace on a Tuesday, which is why both sources insist the memory lives somewhere else.
