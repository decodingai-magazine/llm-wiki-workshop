---
type: source
title: One database, three search modes — a full GraphRAG layer on MongoDB in 2 days
description: The implementation-level account of running text, vector and graph search on a local MongoDB, including the four gotchas that cost real time.
origin: local
original_path: data_input_examples/notes/03-hard/How smooth was my experience to use MongoDB and build from scratch a GraphRAG layer.md
source_url: null
authors: []
published_date: null
raw_file: raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
---

# One database, three search modes — a full GraphRAG layer on MongoDB in 2 days

> [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from|Raw]] · local

## Summary

The most implementation-level note in the wiki, and the useful part is the
friction it reports rather than the architecture it repeats.

The setup runs entirely locally: MongoDB Community 8.2 plus **mongot**, the
community search process, brought up by Docker Compose with a one-shot container
that initializes the replica set and creates the `searchCoordinator` user. That
combination gives `$vectorSearch` with no Atlas account — the note's opening
surprise.

Three collections divide the work: `documents` (raw content, unique `source_uri`
for idempotent ingestion), `knowledge_graph_log` (append-only observations, each
carrying its source document and chunk for provenance), and `knowledge_graph`
(the materialized view where nodes and edges coexist so `$graphLookup` can walk
them). Text search indexes name, content and aliases; vector search runs over
768-dimension embeddings with cosine similarity; graph traversal runs two
`$graphLookup` passes, outgoing and incoming, made bidirectional by reverse edges
that are created only for specific node-type pairs — person↔document and
document↔document are bidirectional, person→task and person→preference
deliberately are not.

**Four gotchas**, each of which reads like it cost an afternoon: a replica set is
mandatory even for a single local node; mongot's sync means a `$vectorSearch`
immediately after index creation silently returns nothing; `$out` atomically
replaces the collection **and drops every index**, so materialization must
recreate them; and compound dict `_id`s cannot go in a Python set, so edge
deduplication needs sorted tuples.

The closing account of *why two days was realistic* is honest about the division:
a clear system design first (arrived at after hitting a framework's walls),
MongoDB's aggregation framework doing the heavy lifting, Prefect supplying fault
tolerance, and a coding agent writing the implementation once the architecture was
decided. "I didn't build any of these — I configured them."

## Key claims

- `$vectorSearch` runs locally on MongoDB Community via mongot — no cloud account required. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Local infrastructure: MongoDB + mongot via Docker Compose|cite]]
- A replica set is mandatory for vector search, even single-node and local. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Local infrastructure: MongoDB + mongot via Docker Compose|cite]]
- Querying immediately after creating a vector index returns an empty result set with no error — you must poll for sync. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Local infrastructure: MongoDB + mongot via Docker Compose|cite]]
- `$out` drops all indexes on every materialization, so index recreation is part of the pipeline; `$merge` would preserve them. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Search mode 2: Vector search ($vectorSearch)|cite]]
- Bidirectional traversal is a deliberate per-edge-type decision, not a global setting. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Search mode 3: Graph traversal ($graphLookup)|cite]]
- Text search is the graceful-degradation path when mongot is down or the vector index is not ready. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#Search mode 1: Text search ($text)|cite]]
- The two-day timeline rested on four things: a clear design, the aggregation framework, thin orchestration, and a coding agent implementing a decided architecture. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from#The development experience|cite]]
- A handwritten project instruction file, written *before* any code, is credited with making the agentic build work. [[raw/how-smooth-was-my-experience-to-use-mongodb-and-build-from|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/claude-code]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/embeddings]], [[wiki/concepts/agentic-coding-loop]], [[wiki/concepts/infrastructure-over-frameworks]]

> Synthesis: The gotchas are the reason to keep this page — every other note in the memory cluster describes the same design, and only this one records what it costs to make it actually run.
