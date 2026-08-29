---
type: source
title: Scaling MongoDB Brain Dump
description: A worked narrative of database scaling for agent memory — replicas, sharding, and the argument that RAM, not data size, is what actually constrains a knowledge graph.
origin: local
original_path: data_input_examples/notes/03-hard/Scaling MongoDB Brain Dump.md
source_url: null
authors: []
published_date: null
raw_file: raw/scaling-mongodb-brain-dump.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/embeddings]]"
---

# Scaling MongoDB Brain Dump

> [[raw/scaling-mongodb-brain-dump|Raw]] · local

## Summary

The written-up version of a conversation with a MongoDB developer advocate, scoped
to one question: how far does a knowledge-graph agent memory scale, and what
breaks first?

The fundamentals come first — vertical scaling (mostly RAM) versus horizontal
(sharding), three replicas as the default for availability, ideally across clouds
and regions so data sits near users, ~2 TB and three nodes per shard so the node
count explodes quickly. Then the thesis: **RAM is the bottleneck, because RAM is
the expensive resource and disk is not.** Every design decision should be made
against RAM.

The mechanism is explained carefully. Indexes live in RAM; queried data is pulled
from disk into cache beside them, so a collection can occupy memory twice over.
"If you query more data than you need, more data than necessary gets cached" —
which makes query shape, not data size, the real constraint. Vector indexes make
this worse: inverted indexes index every word, so the index can equal or exceed
the data.

Then the arithmetic that gives the note its punch. An append-only log plus a
materialized view is two copies: 10 GB of data becomes 20 GB, plus vector indexes,
and you are looking at 40 GB of RAM — for 10 GB of actual data. Skipping the
vector index on the log gets you to 30 GB; being disciplined about what the
`$merge` touches, and letting the log stay on disk, gets you back to roughly 10 GB.
The warning attached is the memorable one: bugs, or **LLMs writing dynamic
queries against your data**, are exactly how this goes off the rails.

## Key claims

- RAM is the scarce resource and therefore the design constraint; disk is cheap and scales easily. [[raw/scaling-mongodb-brain-dump#RAM as the Biggest Bottleneck|cite]]
- A queried collection occupies RAM twice — the index plus the cached slice of data. [[raw/scaling-mongodb-brain-dump#RAM Lifecycle: Index vs Data|cite]]
- Vector (inverted) indexes can be as large as the data or larger, unlike B-tree indexes. [[raw/scaling-mongodb-brain-dump#Vector Indexes and RAM Overhead|cite]]
- The append-only-plus-materialization design can turn 10 GB of data into a 40 GB RAM requirement — and back down to ~10 GB with careful querying. [[raw/scaling-mongodb-brain-dump#Implications for Knowledge Graph Design|cite]]
- "The biggest issue in reality is not necessarily the size of your data per se, but the size of data that you bring into RAM." [[raw/scaling-mongodb-brain-dump#Implications for Knowledge Graph Design|cite]]
- Letting an LLM write dynamic queries against the log is a named way for database performance to collapse. [[raw/scaling-mongodb-brain-dump#Implications for Knowledge Graph Design|cite]]
- Separating `mongod` and `mongot` onto different nodes fixes RAM contention and doubles the node count per shard. [[raw/scaling-mongodb-brain-dump#MongoDB Processes: mongod vs mongot|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/database-scaling]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/embeddings]]

> Synthesis: The wiki's best example of an architectural decision being priced in hardware rather than in principle — and it quietly undercuts the append-only design the other notes argue for, unless the query discipline holds.
