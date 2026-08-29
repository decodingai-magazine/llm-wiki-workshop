---
type: source
title: Ingesting Knowledge Graph Objects for GraphRAG with MongoDB as Unified Memory
description: A twelve-step ghostwriter guide from raw sources to an agent's memory — extraction, entity resolution, embeddings, immutable logs, hybrid indexes, and an MCP server on top.
origin: local
original_path: data_input_examples/notes/03-hard/Ingesting_Knowledge_Graph_Objects_for_GraphRAG_with_MongoDB_as_Unified_Memory.md
source_url: null
authors: []
published_date: null
raw_file: raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/mcp]]"
concepts:
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/database-scaling]]"
---

# Ingesting Knowledge Graph Objects for GraphRAG with MongoDB as Unified Memory

> [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb|Raw]] · local

## Summary

A brief written for a ghostwriter — and therefore unusually explicit about what
the architecture *is*, since it has to be explained to someone who did not build
it. Twelve steps across four zones: data pipeline (collect, ETL into a warehouse),
memory pipeline (clean and chunk, extract triples against an ontology, resolve
entities, embed, package into knowledge-graph objects), unified memory (store as
immutable logs, build hybrid indexes, materialize query views), and agent layer
(an MCP server exposing write-memory and search-memory tools).

The running example does most of the work: an email — *"Arthur, attached is the
GraphRAG survey… Coffee Friday?"* — becomes structured triples (Felix mentions the
document, Arthur is connected to Felix, Arthur has a task), while semi-structured
extraction turns the email's links and attachments into document-to-document
edges. Entity resolution then matches "Arthur" to an existing "Arthur Iusztin"
with alias "Art" rather than creating a duplicate.

Two details are sharper here than in the other memory notes. **Embeddings go on
more than documents**: tasks, preferences and episodes get their own
`content_embedding`, so a query can land directly on a task without traversing a
document first. And the **immutable log makes correction possible** — a preference
recorded as "prefers Java" in June and "prefers Python" in September keeps both
entries, so invalidating a bad extraction reverts the view instead of requiring an
edit.

The scaling guidance is specific: the event log is the first collection to outgrow
a node, partition it by entity id so replay stays on one shard, and use dedicated
search nodes because the read path (vector entry → traversal) is bursty while the
write path is continuous.

## Key claims

- Structured plus semi-structured extraction is the sweet spot: the ontology keeps it precise, metadata parsing captures document lineage for free. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 4 — Graph Extractor (Open Source)|cite]]
- Entity resolution runs against the existing nodes in the same database, matching on `full_name` and aliases before creating anything. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 5 — Normalization (Entity Resolution)|cite]]
- Embedding non-document nodes (tasks, preferences, episodes) lets a query land directly on them, without a document hop. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 6 — Embedding Model (Open Source)|cite]]
- Nothing is overwritten: a wrong extraction is invalidated as a log entry and the view reverts by itself. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 8 — Store as Immutable Logs|cite]]
- The event log is the first collection to outgrow a single node — partition it by entity id so replay avoids scatter-gather. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 8 — Store as Immutable Logs|cite]]
- Read and write workloads have opposite shapes — bursty reads, continuous writes — which is the argument for isolating search nodes. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 9 — Hybrid Index (Text Search + Semantic Search + Graph Search)|cite]]
- Graph traversal surfaces facts vector search cannot: in the worked example, an episode and a task reachable only through edges. [[raw/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb#Step 10 — Query View + Knowledge Graph|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/mcp]]
- **Concepts**: [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/unified-memory]], [[wiki/concepts/embeddings]], [[wiki/concepts/database-scaling]]

> Synthesis: A sponsored brief, so read the vendor framing with the usual discount — but the correction story (invalidate a log entry, the view reverts) is the wiki's only concrete answer to the freshness questions readers keep asking.
