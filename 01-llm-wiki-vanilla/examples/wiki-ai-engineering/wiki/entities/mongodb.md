---
type: entity
title: MongoDB
description: The document database used as the single store for agent memory — documents, vectors, bounded graph traversal and an event log in one cluster.
aliases: [MongoDB Atlas, mongosh]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/cli-tools]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 4
---

# MongoDB

> The database the memory layer actually runs on, chosen for consolidation rather than peak performance in any one dimension.

## Definition

MongoDB appears in this wiki as the answer to "where does the unified memory
live". The case for it is explicitly about avoiding polyglot persistence: one
cluster holding operational documents, vectors with native search, graph
traversal via `$graphLookup`, and an append-only event stream, instead of four
systems and the ETL between them
[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]. The GraphRAG build is
that argument in production: nodes and edges share a single `knowledge_graph`
collection discriminated by a `kind` field, with composite string IDs like
`person:paul iusztin` [[wiki/sources/agentic-graphrag-via-mcp-servers]].

It also appears from the other side — as the thing a coding agent should reach
through `mongosh` rather than through a server
[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]].

## Key claims

- One collection for nodes and edges is what makes `$graphLookup` traversal and single-index maintenance possible. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Vector search runs over HNSW with quantization: 4x memory reduction at Int8, 32x at 1-bit with rescoring against full-fidelity vectors. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Traversal performance degrades predictably with depth — under 10ms at one hop, ~25–100ms at two, up to a second at three, seconds beyond. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Change streams over an append-only `kg_events` collection give reactivity and a replayable history of what the agent believed. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- `$out` silently drops every index on materialization — found by an agent inspecting the collection through `mongosh`. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- Uniqueness on `source_uri` is the deduplication mechanism for ingested documents, with placeholder LATENT documents for not-yet-ingested references. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Local development against MongoDB goes through the CLI, not through a server. [[wiki/sources/why-mcp-is-not-dead]], [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]

## Relationships

- **[[wiki/concepts/unified-memory]]**: MongoDB is the concrete "one store" this wiki keeps arguing for.
- **[[wiki/concepts/hybrid-search]]**: vector plus text in one aggregation stage is the property being bought.
- **[[wiki/concepts/append-only-log]]**: the event-sourcing pattern the graph history uses.

> Synthesis: MongoDB is chosen here for operational simplicity, and both sources are unusually explicit about the thresholds — beyond 3 hops or 100M vectors, the argument they make stops holding.
