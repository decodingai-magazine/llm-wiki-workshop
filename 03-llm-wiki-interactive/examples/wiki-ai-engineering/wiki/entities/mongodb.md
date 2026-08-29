---
type: entity
title: MongoDB
description: The database this wiki's memory layer runs on — documents, vectors, graph traversal and an event log in one cluster, with its limits stated as clearly as its strengths.
aliases: [MongoDB Atlas, mongosh, mongot]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/e2e-personal-assistant-architecture-using-mongodb-as-a]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]"
  - "[[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
  - "[[wiki/sources/what-to-focus-on]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/cli-tools]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 24
---

# MongoDB

> The single store behind the memory layer — chosen for consolidation rather than for winning any one benchmark.

## Definition

MongoDB appears in this wiki as the answer to "where does the unified memory
live", and the case is explicitly about avoiding polyglot persistence: document
storage, aggregation, text search, native vector search and recursive traversal in
one place [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]. The builds put
nodes and edges in a single collection discriminated by a `kind` field, with
composite `"type:name"` ids, because traversal requires one collection to walk
[[wiki/sources/agentic-graphrag-via-mcp-servers]].

It also appears from the opposite direction — as the thing a coding agent should
reach through its CLI rather than through a server
[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]].

## Key claims

- Five jobs in one system: document storage, aggregation and materialization, text search, vector search, graph traversal. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Vector search runs locally on Community Edition through the search process — no cloud account, but a replica set is mandatory even single-node. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- The aggregation framework is what does the real work: grouping, property merging, union and atomic replacement handle deduplication with no application code. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- `$out` replaces a collection atomically and drops every index, forcing a rebuild plus a wait for search-index sync. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]], [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- Traversal cost is predictable and shallow-friendly: sub-10ms at one hop, ~25–100ms at two, up to a second at three. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Quantization is what makes vectors affordable — 4x reduction at Int8, 32x at 1-bit with rescoring. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- The data process and the search process compete for RAM on one machine; dedicated search nodes are the fix and they double the node count. [[wiki/sources/scaling-mongodb-brain-dump]]
- Change streams over an append-only event collection give reactivity and a replayable history. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Development access goes through `mongosh`, and an agent given only that CLI independently debugged indexes, seeded data and verified pipeline output. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]

## Relationships

- **[[wiki/concepts/unified-memory]]**: MongoDB is the concrete "one store" this wiki keeps arguing for.
- **[[wiki/concepts/database-scaling]]**: where the argument meets its RAM bill.
- **[[wiki/concepts/append-only-log]]**: the pattern its aggregation framework makes cheap.

> Synthesis: Nearly half the wiki's sources touch MongoDB, but several are vendor-facing briefs — the claims that survive that discount are the operational ones, and they are the ones with numbers attached.
