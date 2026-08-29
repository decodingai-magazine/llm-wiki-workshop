---
type: concept
title: MCP Apps
description: Server-shipped user interfaces rendered by the client — an agent shipping its own UI, portable across every harness that speaks the protocol.
aliases: [MCP applications]
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
related:
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/entities/mcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 3
---

# MCP Apps

> An MCP server that ships an interface as well as tools — not a plugin, not an SDK, not a UI generated on the fly, but an app served over the protocol.

## Definition

An MCP App is a user interface served by the server and rendered by the client.
The talk describes it as "an agent shipping its own interface… served over an MCP
server," deployable unchanged into Claude, ChatGPT or VS Code / Cursor
[[wiki/sources/the-future-of-mcp-vs-skills]]. Its precondition is semantic: both
sides must agree on how to describe and render the UI, which is exactly what
having a protocol buys.

## Key claims

- The same MCP App runs across Claude, ChatGPT and Cursor without rewriting the UI per client. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- A server can ship an app *and* tools, so the same surface is usable by a human and by the model. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Rendering requires shared semantics — "you need to have both sides… to understand how you render this" — which is why this needs a protocol rather than a convention. [[wiki/sources/the-future-of-mcp-vs-skills]]
- MCP Apps are a client-specific extension: web-based clients can support them, a CLI "just has a hard time rendering." [[wiki/sources/the-future-of-mcp-vs-skills]]
- In the four-layer model this is what makes the presentation layer thin — the renderer does not have to know the domain. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- The server owns the UI contract and the client merely agrees to render it — which is exactly why the protocol needs an explicit extension mechanism for clients that cannot. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: MCP Apps push UI out of the harness and into the server.
- **[[wiki/concepts/mcp-primitives]]**: an extension on top of the primitives, not one of them.

> Synthesis: This is the one place where MCP is argued for on capability rather than governance grounds — no CLI or skill file can ship a renderable interface.
