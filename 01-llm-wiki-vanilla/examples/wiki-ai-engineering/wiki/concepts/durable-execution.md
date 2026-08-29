---
type: concept
title: Durable execution
description: Retries, checkpoints, human approvals and async tasks — what an agent loop needs once it stops being a single inference call.
aliases: [Async tasks, Long-running work]
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/concepts/mcp-primitives]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 2
---

# Durable execution

> Once an agent runs for minutes or days instead of seconds, the loop needs the properties a workflow engine has always had.

## Definition

Both sources make the same move: they notice that agents have stopped being
request-response and conclude that the runtime must change. The four-layer post
lists what that means — durable execution, retries, checkpoints, human approvals,
observability — and puts a workflow engine inside the runtime rather than beside
it [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]].

The architecture note adds the protocol dimension: coding agents could get away
with synchronous, blocking tool calls, but a knowledge-worker agent running a
report or waiting on an approval cannot. The answer has to exist at three levels —
the protocol's async task primitive, the harness runtime, and the UI showing a
task in flight
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]].

## Key claims

- Agents are becoming long-running systems rather than single inference calls, which pulls durability into the runtime. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Blocking tool calls were adequate for coding agents and are not adequate for knowledge-worker agents. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Long-running work needs an answer at all three layers: protocol (async tasks), runtime (harness), and presentation (a task in flight is a first-class UI element, not a spinner). [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Server authors should return a task handle for anything taking more than a few seconds rather than blocking the call. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Improving the async task primitive is on the protocol roadmap, framed as agent-to-agent communication. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/entities/prefect]]**: the concrete engine both sources reach for.
- **[[wiki/concepts/agent-harness]]**: where durability is enforced in practice.

> Synthesis: Neither source resolves the obvious tension — a workflow engine wants determinism, and the thing being orchestrated is a model — which is probably why "human approvals" appears in every one of these lists.
