---
type: entity
title: MCP (Model Context Protocol)
description: The open protocol for connecting agents to tools, data and UI, treated across these notes as one layer of a connectivity stack rather than as the whole of it.
aliases: [Model Context Protocol, MTP]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/governance]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/entities/anthropic]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 7
---

# MCP (Model Context Protocol)

> An open client–server protocol that lets an agent reach tools, data and — increasingly — user interfaces, defined by a small set of primitives and nothing else.

## Definition

MCP is a JSON-RPC client–server protocol: an MCP host (Claude Code, an IDE, a
desktop app) runs clients that connect to servers, and the servers expose tools,
resources and prompts. The specification is deliberately small, and the notes
agree on the consequence: anything that is not one of the primitives — skills
above all — is a **packaging convention on top of the protocol**, not part of it.
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

Where the sources differ is scope. The talk notes frame MCP as one layer of a
larger connectivity stack, useful when you need rich semantics, platform
independence or enterprise controls [[wiki/sources/the-future-of-mcp-vs-skills]].
The rebuttal note treats that same positioning as the reason MCP survives the
"MCP is dead" discourse at all: it is the layer where distribution and governance
are tractable [[wiki/sources/why-mcp-is-not-dead]].

## Key claims

- MCP reached 110M monthly downloads in 18 months, roughly twice as fast as React, with adoption across the OpenAI agents SDK, Google ADK and LangChain. [[wiki/sources/the-future-of-mcp-vs-skills]]
- The protocol's primitives are tools, resources, prompts, sampling, elicitation and (experimentally) tasks — there is no skills primitive. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Tool code always executes on the server, which is what makes server-side composition possible at all. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- The near-term roadmap is a stateless transport, better async tasks for agent-to-agent work, v2 SDKs, cross-app access and well-known-URL server discovery. [[wiki/sources/the-future-of-mcp-vs-skills]]
- In the four-layer application model, MCP is the connective tissue between presentation, harness and the servers holding business logic. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Composing prebuilt servers (web search, image generation, Drive) and re-exposing the union is the default integration move. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- "The protocol moves bytes; the harness decides what to do with them" — several problems blamed on MCP, context bloat above all, are client-side. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- A server can own zero business logic and still be the entire integration surface: the MCP layer is a delivery mechanism, not a logic layer. [[wiki/sources/agentic-graphrag-via-mcp-servers]]

## Relationships

- **[[wiki/concepts/mcp-primitives]]**: the six things the protocol actually defines; everything else is convention.
- **[[wiki/concepts/connectivity-stack]]**: MCP is one of three connectivity mechanisms, not the default for all of them.
- **[[wiki/concepts/governance]]**: the property that keeps MCP relevant where CLIs and skill files do not scale.
- **[[wiki/entities/anthropic]]**: authored the protocol and ships most of its early extensions.

> Synthesis: Across five sources MCP is never argued for on capability grounds — every case for it is really a case about distribution, semantics or governance, which is a useful test to apply before reaching for a server.
