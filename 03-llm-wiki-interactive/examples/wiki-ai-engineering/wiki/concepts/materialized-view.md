---
type: concept
title: Materialized view
description: The queryable graph rebuilt from the log by aggregation — where deduplication, property merging and embedding happen, and where the operational pain lives.
aliases: [Materialization, $merge, $out]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
related:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/database-scaling]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 8
---

# Materialized view

> Squash the log by id: merge properties, union sources, compute one embedding per surviving entity, and hand the query layer something already deduplicated.

## Definition

Materialization is one aggregation: group node observations by name and type,
merge their properties, union their source lists, compose a deterministic
`"type:name"` id, and write the result — plus the same treatment for edges — into
the collection the query layer reads
[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]. It
is also the natural place to compute embeddings, "because it is super hard to
compute an embedding on an object that does not have its full state"
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]].

## Key claims

- Composite `"type:name"` ids came from a real duplicate-key crash: the same name existed as two types. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Embedding after materialization is a large saving — one vector per deduplicated entity instead of one per observation (244 log entries → 70 nodes). [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- `$out` replaces the collection atomically **and drops every index**, so index recreation is part of the pipeline. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]], [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- `$merge` preserves indexes and allows incremental updates, but needs date scoping and a stale-document cleanup strategy. [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- Scope the merge to recent operations — otherwise old log data is pulled into RAM to compete with live queries. [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]
- Materialization can be partial: a new observation about one entity re-squashes only that entity. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Scheduling is a real trade: too rare and the view is stale, too frequent and RAM pressure rises. [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]

## Relationships

- **[[wiki/concepts/append-only-log]]**: the input; this is the derived index over it.
- **[[wiki/concepts/entity-resolution]]**: dedup happens twice — fuzzily at extraction, structurally here.
- **[[wiki/concepts/embeddings]]**: computed here, once per surviving node.

> Synthesis: Everything unpleasant about the log-plus-view design lives in this step — index rebuilds, RAM spikes, staleness windows — which is why the one source that abandoned the design abandoned it here.
