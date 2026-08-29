---
type: concept
title: Database scaling
description: Replicas, shards and the fact that RAM — not disk, not data size — is what actually bounds a knowledge-graph memory layer.
aliases: [Sharding, RAM bottleneck]
sources:
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
related:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 4
---

# Database scaling

> Vertical scaling costs exponentially, horizontal linearly — and the resource you are actually buying is RAM.

## Definition

The baseline: three replicas for availability, ideally across regions or clouds;
sharding for capacity, at roughly 2 TB and three nodes per shard, so node counts
grow in threes [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]. The
constraint that matters is memory. Indexes live in RAM, and queried data is cached
beside them, so an actively-queried collection occupies memory twice — "if you
query more data than you need, more data than necessary gets cached"
[[wiki/sources/scaling-mongodb-brain-dump]].

Vector indexes make it worse: being inverted indexes over every word, they can
equal or exceed the size of the data itself.

## Key claims

- RAM is the scarce, expensive resource; disk is cheap, so designs should be optimized against memory. [[wiki/sources/scaling-mongodb-brain-dump]]
- The data process and the search process compete for the same RAM unless search runs on dedicated nodes — which doubles nodes per shard. [[wiki/sources/scaling-mongodb-brain-dump]], [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- A log-plus-view design can turn 10 GB of data into a 40 GB RAM requirement, and careful querying brings it back to ~10 GB. [[wiki/sources/scaling-mongodb-brain-dump]]
- Vertical scaling raises cost exponentially; sharding raises it linearly. [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]
- The search index caps at roughly 2 billion items per shard. [[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]
- Choose a shard key that co-locates an entity's history, so replay and materialization avoid scatter-gather. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- Letting an LLM write dynamic queries against a large log is a named way to destroy database performance. [[wiki/sources/scaling-mongodb-brain-dump]]

## Relationships

- **[[wiki/concepts/append-only-log]]**: the design whose RAM cost this concept prices.
- **[[wiki/concepts/embeddings]]**: vector indexes are the dominant memory consumer.

> Synthesis: The useful reframing here is that "how big is my data" is the wrong question — "how much of it does a query pull into memory" is the one that predicts the bill.
