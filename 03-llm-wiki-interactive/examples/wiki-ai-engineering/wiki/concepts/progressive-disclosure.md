---
type: concept
title: Progressive disclosure
description: Give the model an index first and the detail only on request — the pattern that keeps tool schemas and retrieval results out of the context window until they are needed.
aliases: [Progressive discovery, tool_search]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/hybrid-search]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T11:50:00Z
source_count: 6
---

# Progressive disclosure

> Don't load it until the agent needs it — applied to tool schemas, and to retrieval results, with the same result: a small index up front, full detail on demand.

## Definition

The pattern shows up twice in this wiki, at two different layers, which is the
best evidence that it is a real pattern and not a trick.

**For tools:** instead of putting every tool definition in the context window,
expose one search capability; the model queries it, loads the schema it needs, and
only then calls the tool. The architecture note prices the difference at roughly
50K tokens versus 200 tokens plus a 300-token schema load, and insists this is the
client's job, not the protocol's
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]].

**For retrieval:** deep search writes one markdown file per node and edge to disk
and returns a YAML index of one-line summaries; the harness reads individual files
on demand [[wiki/sources/agentic-graphrag-via-mcp-servers]]. Same shape, different
payload.

## Key claims

- Loading every tool into the context window is the dominant 2025 pattern and the source of every "MCP causes context bloat" complaint. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- The protocol already supports deferred loading; most harnesses have simply not built it. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Claude Code shipped tool search and saw a large reduction in tool-context usage. [[wiki/sources/the-future-of-mcp-vs-skills]]
- A broad graph query can return hundreds of nodes; returning an index plus files keeps the context lean while leaving the full result set reachable. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The index entries carry a one-line `context` field precisely so the model can decide what to open without opening anything. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The same rule covers server discovery, tool discovery and skill discovery: don't load it until it is needed. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- The same pattern serves retrieval: return a lightweight index over files on disk and let the agent open only what it needs. [[wiki/sources/retrieval-strategies]]
- Deep search is the named tool for it — a wide traversal whose result is an index, not a dump. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- Skills load in three tiers, with only a one-line catalog entry per skill resident — optionally capped at ~1% of the window. [[wiki/sources/article-context-engineering-for-coding-agents]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: the layer that owns the pattern for tools.
- **[[wiki/concepts/programmatic-tool-calling]]**: the other half of the harness upgrade — one saves schema tokens, the other saves round-trips.

> Synthesis: Both instances share one insight worth generalizing: the expensive thing is not retrieval but *materialization into context*, so the artefact you return should be an index whenever the full set might not be read.
