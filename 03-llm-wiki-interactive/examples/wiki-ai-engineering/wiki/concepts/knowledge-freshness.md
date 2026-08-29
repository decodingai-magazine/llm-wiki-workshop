---
type: concept
title: Knowledge freshness
description: Keeping a memory correct as it grows — decay, wrong extractions, stale beliefs — and the housekeeping the immutable log makes possible.
aliases: [Memory decay, Data cleanliness, Housekeeping]
sources:
  - "[[wiki/sources/agent-reasoning-memory-why-it-matters-and-how-to-use-it]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/questions-and-remarks-from-people-while-posting]]"
related:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/rag-evaluation]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 5
---

# Knowledge freshness

> A memory that only accumulates eventually lies. Freshness is the problem of removing, correcting and superseding what is in it.

## Definition

This is the question readers ask most and the sources answer least. Three
variants: memory **decay** (information that was true and is not), **wrong**
information (from a bad source, or a bad extraction of a good one), and staleness
as inputs grow [[wiki/sources/questions-and-remarks-from-people-while-posting]].

The mechanism offered is the append-only log. A preference recorded in June and
contradicted in September keeps both entries, and the derived view reflects the
latest — while invalidating a bad extraction reverts the view without an edit
[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]].

## Key claims

- Data cleanliness is "probably the most complicated part of all of this". [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- The workable loop is: build an evals layer, look at the data, extract rules for good and bad, then run housekeeping pipelines that soft-delete and re-materialize. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Reversibility is the point of immutability: a housekeeping pass that deletes something important can be undone. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Superseding is representable without deletion — both versions of a changed preference stay in the log. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- Reasoning memory has the same problem one level up, and needs decay and pruning or it reinforces stale strategies. [[wiki/sources/agent-reasoning-memory-why-it-matters-and-how-to-use-it]]
- Readers ask about freshness more than about retrieval quality — it is the most common unanswered question in the corpus. [[wiki/sources/questions-and-remarks-from-people-while-posting]]

## Relationships

- **[[wiki/concepts/append-only-log]]**: the substrate that makes correction and reversal possible.
- **[[wiki/concepts/agent-memory]]**: what gets written automatically must also be un-writable.

> Synthesis: The wiki has a strong mechanism (the log) and no policy — nothing here says *when* something should be considered stale, which is exactly the gap the reader questions keep pointing at.
