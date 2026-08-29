---
type: concept
title: Embeddings
description: "Where vectors get computed, hosted and paid for — and the decisions around them: summary versus chunk, dev versus prod, one interface across both."
aliases: [Vector embeddings, Embedding models]
sources:
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]"
  - "[[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
related:
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/entities/voyage-ai]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 12
---

# Embeddings

> The cheap-looking step that turns out to drive index size, RAM, cost and half the retrieval design.

## Definition

Across these builds embeddings are computed **after** deduplication, once per
materialized node, over a text representation of the node — its type, its
properties, its content
[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]. Dimensions
range from 384 (a local sentence-transformer) to 768 to 1024, and the sources
treat the choice as a balance between retrieval quality and index size.

The most consequential decision is *what* to embed: a per-document **summary**
rather than chunks, explicitly to avoid chunking, "which can get complicated to do
it right" [[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]].
Non-document nodes — tasks, preferences, episodes — get their own content
embedding so a query can land on them directly
[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]].

## Key claims

- Embedding after materialization instead of per observation cut the work ~3.5x in one build. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Where the model runs should differ by environment — mocked in tests, Sentence Transformers in dev, a served model or an API in production, behind one interface. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- Embedding is the most parallelizable ingestion step (no dependencies between nodes) and the one most worth checkpointing before storage. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Vector indexes are inverted indexes: they can be as large as the data or larger, which makes them the dominant RAM cost. [[wiki/sources/scaling-mongodb-brain-dump]]
- Quantization is what makes the unified store affordable — 4x memory reduction at Int8, 32x at 1-bit with rescoring. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- Embeddings are always stripped from tool output: a 384-dim array costs ~1500 tokens and tells the model nothing. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Auto-embedding — the database computing vectors from a config — is the big-data option that is *easier*, not harder, to maintain. [[wiki/sources/different-levels-of-hosting-your-embedding-models]], [[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]

## Relationships

- **[[wiki/concepts/hybrid-search]]**: embeddings supply one of the two rankings that get fused.
- **[[wiki/concepts/provider-abstraction]]**: the interface that makes the dev/prod split invisible to the pipeline.
- **[[wiki/concepts/materialized-view]]**: the stage where embedding belongs, because a node needs its full state first.

> Synthesis: The recurring move across these sources is to embed *less*, later — summaries not chunks, deduplicated nodes not observations — which reads as retrieval design but is mostly a cost and RAM decision.
