---
type: concept
title: Hybrid search
description: Combining vector similarity with lexical search and fusing the rankings, so retrieval catches both meaning and exact terms before any graph traversal.
aliases: [RRF fusion, Reciprocal Rank Fusion]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 2
---

# Hybrid search

> Vector search for meaning, text search for the exact word, and a rank fusion that needs no tuning to combine them.

## Definition

Hybrid search is the seed-finding step of GraphRAG retrieval. Both rankings are
computed independently — `$vectorSearch` over cosine similarity, and a stemmed
`$text` query — then merged with **Reciprocal Rank Fusion**:
`score = Σ 1 / (k + rank + 1)`, with `k = 60` and no absolute weighting, so the
two systems' incomparable scores never have to be normalized
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. Only then does graph expansion
run over the seeds.

The database evaluation describes the same capability from the storage side:
vector results, metadata filters and lexical search combined in a single
aggregation stage [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]].

## Key claims

- RRF is purely rank-based, so it fuses two rankings without weighting or score normalization. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Hybrid retrieval is what makes vague queries survivable — semantics catch the intent, text catches the exact identifier. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Search and filters can run in one `$vectorSearch` aggregation stage rather than as separate round-trips. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Dedicated search nodes isolate vector indexing from the operational workload so retrieval does not degrade writes. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Hybrid search finds the seeds; graph expansion supplies the context — they are two stages, not two alternatives. [[wiki/sources/agentic-graphrag-via-mcp-servers]]

## Relationships

- **[[wiki/concepts/knowledge-graph]]**: hybrid search is phase one, traversal is phase two.
- **[[wiki/entities/mongodb]]**: both indexes live in the same collection, which is the point.

> Synthesis: The teaching detail here is `k = 60` and no weights — the fusion is deliberately un-tuned, which is what makes it hold up as the corpus changes underneath it.
