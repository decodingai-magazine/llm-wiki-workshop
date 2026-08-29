---
type: source
title: MCP Servers for Continual Learning via GraphRAG
description: A deep dive on tool design for an agentic GraphRAG memory — six tools, why not one, and the deliberate asymmetry of orchestrating writes but never reads.
origin: local
original_path: data_input_examples/notes/03-hard/MCP Servers for Continual Learning via GraphRAG.md
source_url: null
authors: []
published_date: null
raw_file: raw/mcp-servers-for-continual-learning-via-graphrag.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/agentic-search]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/read-write-separation]]"
  - "[[wiki/concepts/continual-learning]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/hybrid-search]]"
---

# MCP Servers for Continual Learning via GraphRAG

> [[raw/mcp-servers-for-continual-learning-via-graphrag|Raw]] · local

## Summary

The note opens with the finding that organizes everything after it: "Building the
knowledge graph was straightforward… Designing how the agent interacts with that
memory was the hard part." Exposing raw database operations makes agents
struggle, so the server is designed around how agents actually search and write.

**Six tools, three of each.** Ingest: `ingest_url` (dispatch by source type),
`ingest_file` (local markdown, text, HTML), and `ingest_conversation` — the
continual-learning one, capturing the current conversation back into the graph so
"next week's chat knows what today's decided", auto-triggered by a hook every ~10
turns. Query: `query_memory` (natural language compiled to a validated aggregation
pipeline, with a self-correcting retry), `search_memory` (hybrid RRF search plus
k-hop expansion — the **deterministic fallback with no LLM in the critical path**,
which "always returns something"), and `deep_search_memory` (wide search, results
written to disk, a lightweight index returned).

The framework section argues ergonomics: type hints are the schema, docstrings are
the description, the function body is the implementation — so every tool is 10–15
lines and nothing has to be kept in sync. Two details are more than convenience:
the lifespan hook initializes the database client, LLM and embedding model once
and injects them into every call, and the server-level `instructions=` field ships
the **routing rulebook** to the agent, so the guidance about which tool to use
lives next to the tools it routes.

The most transferable idea is the **asymmetry**. Write paths are wrapped in
durable flows with retries and per-task isolation, so an upstream 503 or a rate
limit does not crash the agent's turn. Batch rebuilds resume from where they
failed instead of re-paying for the documents already processed. Read paths are
deliberately *not* wrapped: queries are cheap, read-only and idempotent, the agent
is already in its own retry loop, and orchestrating them would add latency for no
durability — "a deliberate choice, not an oversight".

## Key claims

- Building the graph was easy; designing the agent's interface to it was the hard part. [[raw/mcp-servers-for-continual-learning-via-graphrag#Post|cite]]
- Exposing raw database operations to an agent does not work — the tools must match how agents search and write. [[raw/mcp-servers-for-continual-learning-via-graphrag#Post|cite]]
- Six high-leverage primitives the agent composes beat one general-purpose tool. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- The NL-query tool is the default and the hybrid search tool is the deterministic fallback with no LLM in the critical path. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- The ontology drives both the extraction prompt and the NL-query prompt — one source of truth for what the memory can contain. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- This build uses a **single upsert-idempotent collection**: re-ingesting densifies the graph rather than duplicating it. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- Server `instructions=` is a routing layer: it tells the model which tool fits which question, and it lives beside the tools. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- Writes are orchestrated, reads are not — deliberately, because queries are cheap and idempotent and the agent already retries. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]
- Conversation ingestion is what makes the memory continually learning rather than merely persistent. [[raw/mcp-servers-for-continual-learning-via-graphrag#Executive Summary|cite]]

## Notable quotes

> "Graph for memory. FastMCP for access. Harness for behavior."
> — [[raw/mcp-servers-for-continual-learning-via-graphrag#Post|location]]

## Connections

- **Entities**: [[wiki/entities/fastmcp]], [[wiki/entities/prefect]], [[wiki/entities/mongodb]], [[wiki/entities/mcp]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/mcp-server-design]], [[wiki/concepts/agentic-search]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/read-write-separation]], [[wiki/concepts/continual-learning]], [[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/durable-execution]], [[wiki/concepts/agent-skills]], [[wiki/concepts/hybrid-search]]

> Synthesis: This is where the wiki's two halves finally meet — the MCP notes describe a server abstractly, the memory notes describe a graph, and this one is the tool surface between them. It also quietly confirms [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]: the shipped design is a single upsert collection, not a log plus a view.
