---
type: source
title: You don't need a reranker for hybrid search — RRF fusion in 20 lines
description: Why Reciprocal Rank Fusion replaces a cross-encoder reranker for hybrid retrieval — rank arithmetic instead of score comparison, with the implementation and its limits.
origin: local
original_path: data_input_examples/notes/03-hard/rrf-fusion-hybrid-search-without-reranker.md
source_url: null
authors: []
published_date: null
raw_file: raw/rrf-fusion-hybrid-search-without-reranker.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/knowledge-graph]]"
---

# You don't need a reranker for hybrid search — RRF fusion in 20 lines

> [[raw/rrf-fusion-hybrid-search-without-reranker|Raw]] · local

## Summary

The problem is stated precisely: text search returns BM25-like scores in the
0.5–10+ range, vector search returns cosine similarities in 0–1, and "a textScore
of 3.5 and a vectorSearchScore of 0.87 tell you nothing about which result is more
relevant." They cannot be averaged, weighted or sorted together. Every tutorial's
answer is a cross-encoder reranker, which costs 50–200ms, money per query, a model
to maintain, and another failure point.

**Reciprocal Rank Fusion** (Cormack et al., 2009) ignores scores entirely and uses
only positions: `score = Σ 1 / (k + rank)` over every list the document appears
in, with `k = 60`. The worked examples make the behaviour obvious — first in both
lists scores 0.0328, first in one list only 0.0164, fifth-and-tenth 0.0297 — so
appearing in both lists beats ranking highly in one. The implementation is two
loops over a dictionary, quoted in full, and the caller sorts and truncates.

It sits as phase one of a two-phase retrieval: fuse text and vector hits into seed
nodes, then expand with two `$graphLookup` passes. The `k` parameter is explained
rather than tuned — higher `k` flattens the distribution when both rankers are
noisy, lower `k` lets the top result dominate when you trust them.

The limits are stated plainly: RRF uses rank, not content, so it misses relevance
signals a reranker would catch; it assumes both methods return sane rankings, and
will promote garbage that happens to overlap; and it does nothing for a
single-method query. The author's line: he would consider a reranker for a
general-purpose engine over millions of heterogeneous documents, not for a scoped
knowledge graph with a defined ontology.

## Key claims

- Scores from text and vector search are incomparable, which is the actual problem a reranker is usually hired to solve. [[raw/rrf-fusion-hybrid-search-without-reranker#The problem: merging two ranked lists with incomparable scores|cite]]
- RRF uses only rank, so no score normalization is needed and no model is involved. [[raw/rrf-fusion-hybrid-search-without-reranker#RRF: rank arithmetic instead of score comparison|cite]]
- Documents appearing in both lists outrank documents that top only one. [[raw/rrf-fusion-hybrid-search-without-reranker#RRF: rank arithmetic instead of score comparison|cite]]
- The whole fusion is ~20 lines: two loops and a dictionary, running in microseconds. [[raw/rrf-fusion-hybrid-search-without-reranker#The implementation|cite]]
- Text search catches exact names, vector search catches concepts; fusion is what lets you have both. [[raw/rrf-fusion-hybrid-search-without-reranker#How it fits into the full retrieval pipeline|cite]]
- RRF's blind spot is content — it will promote a bad result that both rankers happen to surface. [[raw/rrf-fusion-hybrid-search-without-reranker#When you might need a reranker|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/hybrid-search]], [[wiki/concepts/embeddings]], [[wiki/concepts/knowledge-graph]]

> Synthesis: The most reusable engineering result in the wiki — a 2009 paper, twenty lines, no infrastructure — and the honest limits section is what makes it credible rather than merely contrarian.
