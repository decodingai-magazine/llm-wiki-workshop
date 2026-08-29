---
type: concept
title: Context layer
description: The memory, notes and preferences that make an agent *yours* — the layer worth owning, because models and harnesses beneath it are commodities.
aliases: [Portable memory, Digital twin]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/owning-your-context-layer]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-memory]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 2
---

# Context layer

> Your research, notes, conversations, tasks and preferences — bundled behind an interface, so switching harness costs you nothing.

## Definition

The context layer is a unified memory plus the server that exposes it, treated as
a single owned asset. Its defining property is portability: switch from Claude
Code to Codex to Gemini CLI and, ideally, nothing changes — within five minutes
the new harness knows who you are, because the memory moved with you
[[wiki/sources/owning-your-context-layer]].

The GraphRAG build is the same idea with the seams visible: the MCP server is
portable across every compatible harness, while skills and hooks are
per-harness enhancements that degrade gracefully
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. Ownership is therefore
architectural, not legal — you own the layer if the thing that knows you is the
thing you can move.

## Key claims

- Models and harnesses are commoditizing; what remains differentiated is the context layer. [[wiki/sources/owning-your-context-layer]]
- Open-source models and harnesses are the wrong place to look for freedom — they are infrastructure, not the thing you care about. [[wiki/sources/owning-your-context-layer]]
- Being deeply invested in one open-source harness can cost *more* to leave than using a proprietary one with portable memory. [[wiki/sources/owning-your-context-layer]]
- Ownership buys portability and privacy — the data does not sit on a model provider's servers. [[wiki/sources/owning-your-context-layer]]
- In practice the portable unit is the MCP server plus its memory; harness-specific skills and hooks sit above it and are expected to be re-created per harness. [[wiki/sources/agentic-graphrag-via-mcp-servers]]

## Relationships

- **[[wiki/concepts/unified-memory]]**: the storage side of the same asset.
- **[[wiki/concepts/agent-harness]]**: the layer this one is deliberately kept independent of.

> Synthesis: This is the wiki's answer to "why bother with any of this architecture" — and it is worth noticing that the argument is about *exit cost*, which is a strategy claim rather than a technical one.
