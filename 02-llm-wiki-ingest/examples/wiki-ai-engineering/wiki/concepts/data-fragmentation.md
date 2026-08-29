---
type: concept
title: Data fragmentation
description: Your knowledge lives in email, notes, documents and messages, in different formats behind different APIs — and no single retrieval ever spans them.
aliases: [Data silos]
sources:
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/context-rot]]"
  - "[[wiki/concepts/knowledge-graph]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 2
---

# Data fragmentation

> The data is scattered across emails, notes, articles, messages and databases — "you rarely sit in the beautiful situation where all your data is in one database with a clean API to query it."

## Definition

Fragmentation is the second of the two problems GraphRAG is offered as an answer
to. The data is siloed by platform (Notion, Drive, Gmail, SMS), by structure
(JSON, semi-structured headers, free text), and by access (private, authenticated,
rate-limited)
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]. The
consequence for retrieval is concrete: **no single chunk spans two silos**, so
similarity search can only ever return fragments from one of them
[[wiki/sources/graphrag-presentation]].

## Key claims

- Fragmentation is structural, not incidental — silos differ in format, ownership and API, not just location. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Because no chunk spans silos, traditional RAG "finds 1–2 fragments and hallucinates the rest". [[wiki/sources/graphrag-presentation]]
- Cross-silo edges are what make an answer possible: the worked query stitches SMS, Drive, email and Notion into one subgraph. [[wiki/sources/graphrag-presentation]]
- The unifying move is ingestion into one store, not federation across the silos. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]

## Relationships

- **[[wiki/concepts/unified-memory]]**: the proposed answer — one store rather than many.
- **[[wiki/concepts/knowledge-graph]]**: the representation that makes cross-silo connection expressible.

> Synthesis: Fragmentation is the problem that justifies the entire ingestion pipeline, and it is worth noticing that the solution offered is copying everything into one place — which trades a retrieval problem for a synchronization one.
