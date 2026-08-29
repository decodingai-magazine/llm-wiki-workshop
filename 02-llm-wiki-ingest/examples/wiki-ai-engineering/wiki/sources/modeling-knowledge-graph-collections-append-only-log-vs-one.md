---
type: source
title: "Modeling knowledge graph collections: append-only log vs. one collection"
description: The full engineering account of the two-collection design — and the note that records its abandonment in favour of a single mutable collection with in-place upserts.
origin: local
original_path: data_input_examples/notes/03-hard/Modeling Knowledge Graph Collections Append Only Log vs. One Collection Design.md
source_url: null
authors: []
published_date: null
raw_file: raw/modeling-knowledge-graph-collections-append-only-log-vs-one.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/knowledge-freshness]]"
---

# Modeling knowledge graph collections: append-only log vs. one collection

> [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one|Raw]] · local

## Summary

A full engineering document for the two-collection, event-sourcing-inspired design
— and the only source in the wiki that reports its **abandonment**. The note is
explicit up front: "This architecture was the initial design and is documented
here for educational purposes. The system was later migrated to a simpler
single-collection mutable approach with in-place upserts."

The design is the one the rest of the memory cluster advocates: an append-only
`knowledge_graph_log` as the source of truth, and a `knowledge_graph` materialized
view rebuilt from it, cleanly splitting a write-optimized path from a
read-optimized one. The advantages are stated fairly — a full audit trail with
temporal history, idempotent re-extraction (running twice just appends; `$group`
deduplicates), property merging that builds richer entity profiles across sources,
`sources` tracking for attribution, and a log that stays on disk during normal
operation.

The disadvantages are what make this note valuable, because they are operational
rather than theoretical. `$out` drops the collection and destroys every index, so
each materialization forces a rebuild plus a wait for search-index sync, and there
is no incremental path without switching to a date-scoped `$merge` and a
stale-document cleanup strategy. Both collections compete for RAM during
materialization. Reverse edges roughly double the qualifying edge count and must
be recreated every time. Mixed `_id` types — strings for nodes, dicts for edges —
force `id: Any` and lose type safety. The multi-branch aggregation is hard to test
and debug. And there is a latency floor: new extractions are invisible to queries
until the next materialization cycle.

Two smaller points land hard. **Immutability is application-level**: MongoDB has no
immutable-collection flag, so the guarantee is only that the code never calls
update or delete — "a design choice, not a database guarantee". And the closing
comparison: a single mutable collection with in-place upserts is simpler on RAM,
simpler to operate, has real-time visibility and no index rebuilds, and the price
is the temporal audit trail.

## Key claims

- The system migrated away from this design to a single mutable collection with in-place upserts. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one|cite]]
- `$out` destroys indexes on every materialization; `$merge` preserves them but needs date scoping and stale-document cleanup. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#8.5 Materialization Scheduling|cite]]
- The two collections compete for RAM during materialization, pulling old log data into the working set. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#8.3 The RAM Problem with Two Collections|cite]]
- Immutability is enforced by the application, not the database — a bug or a shell command can corrupt the log. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#8.6 Immutability is Application-Level|cite]]
- Re-extraction is idempotent by construction: duplicates in the log are collapsed by `$group` at materialization. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#9. Pros and Cons|cite]]
- There is no real-time path: data is unqueryable until the next materialization cycle. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#9. Pros and Cons|cite]]
- Reverse edges roughly double the edge count for qualifying pairs, and must be recreated after every rebuild. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#9. Pros and Cons|cite]]
- The single-collection alternative trades the temporal audit trail for simplicity, real-time visibility and no index rebuilds. [[raw/modeling-knowledge-graph-collections-append-only-log-vs-one#9. Pros and Cons|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/database-scaling]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/knowledge-freshness]]

> Synthesis: The most important source in the memory cluster, because it is the only one written *after* the decision was reversed — every other note argues for immutable logs, and this one reports what happened when they were run.
