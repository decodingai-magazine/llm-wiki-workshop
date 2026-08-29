---
type: concept
title: Append-only log
description: Store every extraction as an immutable observation and derive the queryable graph from it — buying provenance, replay and reversibility at the cost of RAM and a materialization step.
aliases: [Immutable logs, Event sourcing, kg_events]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
related:
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/knowledge-freshness]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/knowledge-graph]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 11
---

# Append-only log

> Never update, never delete — append every observation and derive the current state. What you buy is time travel; what you pay is RAM and an extra pipeline.

## Definition

Every extraction result is written as its own document — a node or edge
observation carrying its source document, its chunk, and a timestamp — into a
collection that is only ever appended to
[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]. The
queryable graph is then *derived* from that log by materialization. The pattern is
event sourcing with CQRS, and the sources name three things it buys:
**provenance** (trace any node to the chunk that produced it), **replayability**
(change the materialization logic and re-aggregate — no re-extraction, no
re-paying the LLM), and **reversibility** — which matters because "we work with
LLMs here and they fail really often"
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]].

## Key claims

- A wrong extraction is fixed by invalidating a log entry, after which the derived view reverts by itself — no edit, no migration. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- The log makes re-extraction idempotent: duplicates are collapsed at materialization by grouping. [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- Immutability is enforced by the application, not the database — there is no immutable-collection flag, only code that never updates or deletes. [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]], [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- The log is the first collection to outgrow a single node; partition it by entity id so replay stays local. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- It is rarely read, so it mostly stays on disk — until a materialization pulls it into RAM, which is exactly where the cost shows up. [[wiki/sources/scaling-mongodb-brain-dump]]
- Housekeeping becomes safe: classify bad entries, soft-delete, re-materialize, and revert if the classifier was wrong. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]

## Relationships

- **[[wiki/concepts/materialized-view]]**: the other half — the log is the source of truth, the view is the index.
- **[[wiki/concepts/knowledge-freshness]]**: the log is what makes correcting stale or wrong knowledge tractable.
- **[[wiki/concepts/database-scaling]]**: two copies of the data is the price, and it is paid in RAM.

## Tensions

- Nine sources argue for this design; the tenth reports abandoning it. [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]] documents the migration to a single mutable collection with in-place upserts — simpler on RAM, real-time, no index rebuilds — and names the price: the temporal audit trail. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]] confirms the shipped system uses the single upsert collection.

> Synthesis: The argument for append-only is about *correctability*, not durability, and the counter-argument is about operations — so the honest question is not "is the log right" but "how often do you actually need to revert?"
