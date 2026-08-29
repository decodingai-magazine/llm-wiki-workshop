---
type: concept
title: Unified memory
description: One store holding documents, vectors, graph and history — so the agent has a single place to search and write, and no synchronization tax to pay.
aliases: [Agent memory layer, One database]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/e2e-personal-assistant-architecture-using-mongodb-as-a]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
  - "[[wiki/sources/you-don-t-need-a-browser-anymore]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/data-fragmentation]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 15
---

# Unified memory

> One store, a small tool surface, any harness. The argument is not that one database is fastest — it is that four databases cost more than they return.

## Definition

Agent memory has four workloads — operational state, semantic vectors, graph
traversal, and an event history — usually solved by four systems. Consolidating
them avoids the **"synchronization tax"**: cross-database ETL, inconsistency risk,
and four security models [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]].
The build that follows this argument runs documents, text search, vector search
and traversal against one database, locally, with three collections
[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]].

The surface exposed to the agent stays deliberately small: two tools in the
earliest sketch [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]],
six in the shipped systems — three to read at different granularities, three to
write from different sources
[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]].

## Key claims

- Polyglot persistence buys niche performance and charges an integration tax in ETL, consistency and security. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- One database replaces three plus the glue between them — document store, vector store, graph engine. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Build with the simplest tool that works — filesystem, BM25, semantic search — and add the graph when the use case demands it. [[wiki/sources/owning-your-context-layer]]
- The thresholds where one store stops being right are stated: past ~100M vectors, past 5-hop traversals, or when analytical replay threatens interactive latency. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- The trade accepted in exchange is a graph-native query language — worth it at personal scale, by explicit choice. [[wiki/sources/retrieval-strategies]]
- The memory ingests everything — notes, emails, papers, videos, conversations — rather than federating across silos. [[wiki/sources/why-mcp-is-not-dead]], [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Preferences and episodes are detected from conversation and written back automatically, which is what makes the memory personal rather than archival. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Specific business logic plus hosted infrastructure is what makes a server the right exposure — "doing this through a CLI would have been a nightmare." [[wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/concepts/data-fragmentation]]**: the problem this is the answer to.
- **[[wiki/concepts/context-layer]]**: unified memory is the asset; the context layer is why owning it matters.
- **[[wiki/concepts/hybrid-search]]** and **[[wiki/concepts/knowledge-graph]]**: the two retrieval modes it has to serve at once.

> Synthesis: "Unified" is doing the load-bearing work — the claim is not about a database's feature list but about refusing to let each source keep its own retrieval path, and every cost in this wiki (RAM, materialization, index rebuilds) is the bill for that refusal.
