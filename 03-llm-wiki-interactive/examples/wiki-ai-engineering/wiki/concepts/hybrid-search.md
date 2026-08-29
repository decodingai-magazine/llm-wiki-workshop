---
type: concept
title: Hybrid search
description: Vector search for meaning, text search for the exact word, fused by rank — the seed-finding step that every retrieval path in this wiki starts from.
aliases: [RRF fusion, Reciprocal Rank Fusion, Text + vector search]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/agentic-search]]"
  - "[[wiki/concepts/unified-memory]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 13
---

# Hybrid search

> Two rankings with incomparable scores, merged by position rather than value — no model, no tuning, no calibration.

## Definition

Text search returns BM25-like scores in the units of one system; vector search
returns cosine similarities in another. They cannot be averaged or sorted
together, which is the problem a reranker is usually hired to solve.
**Reciprocal Rank Fusion** ignores the scores entirely: `score = Σ 1 / (k + rank)`
over every list a document appears in, with `k = 60`. A document in both lists
outranks one that tops only a single list, and nothing needs calibrating
[[wiki/sources/rrf-fusion-hybrid-search-without-reranker]].

Hybrid search is always phase one. The fused winners become **seed nodes**, and
graph expansion runs from them [[wiki/sources/retrieval-strategies]].

## Key claims

- The whole fusion is ~20 lines and runs in microseconds — two loops and a dictionary. [[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]
- Text catches exact names and identifiers, vectors catch meaning; fusion is what lets you have both. [[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]
- RRF's blind spot is content: it can promote a bad result that both rankers happen to surface. [[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]
- Fusing before reranking is deliberate — the reranker then only orders a small fused set instead of the collection. [[wiki/sources/retrieval-strategies]]
- Retrieval degrades rather than fails: if vector search is unavailable it falls back to text-only. [[wiki/sources/retrieval-strategies]], [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- Vector, metadata filters and lexical search can run in a single aggregation stage against one collection. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Dedicated search nodes isolate vector indexing from the operational workload, because read and write loads have opposite shapes. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- Candidate oversampling (a pool ~10x the requested results) is what keeps approximate vector search accurate enough to fuse. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]

## Relationships

- **[[wiki/concepts/knowledge-graph]]**: hybrid search finds entry points; traversal supplies the context.
- **[[wiki/concepts/agentic-search]]**: the deterministic path against the flexible one.

> Synthesis: `k = 60` and no weights is the detail worth keeping — the fusion is deliberately un-tuned, which is exactly what makes it survive a corpus that changes underneath it.
