---
type: note
title: Append-only log vs. in-place updates
description: When to keep every observation and derive the current state, and when a single mutable collection is the better engineering decision.
created: 2026-08-29T11:00:00Z
timestamp: 2026-08-29T11:10:00Z
spawned_by_question:
  - "[[wiki/questions/2026-08-29-append-only-log-vs-in-place-updates]]"
  - "[[wiki/questions/2026-08-29-is-event-sourcing-worth-it-for-a-personal-knowledge-graph]]"
sources:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/knowledge-freshness]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/entity-resolution]]"
---

# Append-only log vs. in-place updates

The wiki has an unusually clean disagreement here: most of its sources argue for
an append-only log with a derived view, and the one source written *after* that
design was run in production reports abandoning it. Both positions are well
supported, so the answer is a decision rule.

## What the log buys

Three things, and only three
[[wiki/concepts/append-only-log]]:

- **Provenance** — every node and edge traces to the chunk that produced it.
- **Replayability** — change how you materialize and re-aggregate; no
  re-extraction, so no re-paying the model
  [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]].
- **Reversibility** — invalidate a bad extraction and the derived view reverts by
  itself, with no edit and no migration
  [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]].

The third is the one that matters for LLM-written data specifically, and the
sources say so directly: this pattern exists because "we work with LLMs here and
they fail really often"
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]. It
is also what makes housekeeping safe — classify bad entries, soft-delete,
re-materialize, and revert if the classifier was wrong
[[wiki/concepts/knowledge-freshness]].

## What it costs

The bill is paid in memory and in operations
[[wiki/concepts/database-scaling]]:

- Two copies of the data, and during materialization both need to be resident. A
  10 GB graph plus vector indexes can imply a 40 GB machine under this design, and
  only careful scoping brings it back to ~10 GB
  [[wiki/sources/scaling-mongodb-brain-dump]].
- Materialization by full replacement destroys every index, forcing a rebuild and
  a wait for search-index sync; the incremental alternative needs date scoping and
  a stale-document cleanup strategy
  [[wiki/concepts/materialized-view]].
- There is a staleness window by construction: new observations are invisible to
  queries until the next materialization
  [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]].
- Immutability is enforced by the application, not the database. It is "a design
  choice, not a database guarantee", and one stray write breaks it
  [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]].

## What actually happened

The system these notes describe **migrated away** from the two-collection design to
a single mutable collection with in-place upserts — simpler on RAM, real-time
visibility, no index rebuilds — accepting the loss of the temporal audit trail
[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]. The
shipped server confirms it: writes are upsert-idempotent against one collection,
and re-ingesting a document densifies the graph instead of duplicating it
[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]].

## The decision rule

Ask how often you will actually need to revert.

| Choose | When |
|---|---|
| **Append-only + materialized view** | Extractions are model-written and wrong often enough that you will re-run housekeeping; you need provenance for attribution or audit; you expect to change the materialization logic and want to replay rather than re-extract. |
| **Single mutable collection** | Writes are idempotent by construction (deterministic ids); RAM is the binding constraint; you need new data queryable immediately; the audit trail is nice-to-have rather than load-bearing. |

Two things make the second option far more defensible than it first appears:
deterministic composite ids make an upsert naturally idempotent
[[wiki/concepts/materialized-view]], and re-ingestion then *densifies* rather than
duplicates. What you give up is the ability to answer "what did the wiki believe
last month, and why?"

> Synthesis: A source that documented a reversal is worth more than nine that
> documented an intention — and the gap this note cannot close is that nobody
> reports what the reversal *cost* them the first time they needed to undo a bad
> extraction without a log.
