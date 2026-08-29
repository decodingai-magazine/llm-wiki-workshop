---
type: source
title: MongoDB Notes on Scaling (from the meeting)
description: Raw meeting notes from a scaling review — questions about an append-only log plus materialized graph, and answers about shards, replicas, RAM and the $merge sync.
origin: local
original_path: data_input_examples/notes/03-hard/MongoDB Notes on Scaling (from the meeting).md
source_url: null
authors: []
published_date: null
raw_file: raw/mongodb-notes-on-scaling-from-the-meeting.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/knowledge-graph]]"
---

# MongoDB Notes on Scaling (from the meeting)

> [[raw/mongodb-notes-on-scaling-from-the-meeting|Raw]] · local

## Summary

Meeting notes in two halves: the questions taken in, and the answers written
down. The setup being reviewed is a from-scratch GraphRAG memory with an
**immutable log collection** of extracted entities and relationships, plus a
**materialized view** that aggregates the log into the queryable knowledge graph,
synced with `$merge`.

The answers are concrete and mostly about memory. Immutability is an application
concern — there is nothing to flag in the database. Atlas gives a three-node
replica set by default, commonly spread across clouds and availability zones.
Sharding gives effectively infinite scale at the cost of cluster complexity, with
~2 TB per shard as a working figure and three nodes per shard, so two shards means
six nodes. The vector index (`mongot`, Lucene-based) caps at roughly 2B items per
shard and is bounded by machine memory; vertical scaling raises cost
exponentially where horizontal raises it linearly.

The sharpest point is contention: `mongod` and `mongot` sit on the same machine
and compete for RAM, and inverted indexes can be as large as the data or larger
because they index every word rather than a few fields. The log is rarely read, so
it mostly stays on disk — fine for disk, a problem for RAM the moment a `$merge`
pulls old data in. Hence the practical guidance: scope `$merge` to recent
operations, or use a dedicated Atlas search node so the two processes stop
competing. Recursive `$graphLookup` is fast because the index is already resident;
the `$match`/`$in` entry-point lookup is fine under a thousand IDs and starts to
slow beyond that.

## Key claims

- "No reason to flag anything in MongoDB as immutable. The immutability should be handled on the application side." [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]
- A shard holds roughly 2 TB and about 2B indexed items; each shard is three nodes, so node count grows in threes. [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]
- Vertical scaling raises cost exponentially, horizontal scaling linearly. [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]
- `mongod` and `mongot` compete for the same RAM; inverted indexes can exceed the size of the data. [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]
- Scope the `$merge` to recent operations (e.g. the last 20 seconds) so old log data is never pulled into RAM. [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]
- `$graphLookup` is fast because recursion keeps the index resident; `$match`/`$in` degrades past thousands of entry-point IDs. [[raw/mongodb-notes-on-scaling-from-the-meeting#Notes|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/database-scaling]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/knowledge-graph]]

> Synthesis: Unpolished meeting notes, and more useful for it — this is the primary record that [[wiki/sources/scaling-mongodb-brain-dump]] later turns into prose, so where the two disagree, prefer this one.
