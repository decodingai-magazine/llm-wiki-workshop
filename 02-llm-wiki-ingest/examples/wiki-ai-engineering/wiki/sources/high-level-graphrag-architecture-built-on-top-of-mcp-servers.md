---
type: source
title: High-Level GraphRAG Architecture Built on Top of MCP Servers
description: A lecture write-up covering the whole arc — context rot and data fragmentation, ontologies, immutable logs, materialization, bottom-up and top-down retrieval, and agentic GraphRAG.
origin: local
original_path: data_input_examples/notes/03-hard/High-Level GraphRAG Architecture Built on Top of MCP Servers.md
source_url: null
authors: []
published_date: null
raw_file: raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/neo4j]]"
  - "[[wiki/entities/voyage-ai]]"
concepts:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/graph-communities]]"
  - "[[wiki/concepts/context-rot]]"
  - "[[wiki/concepts/data-fragmentation]]"
  - "[[wiki/concepts/agentic-search]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-freshness]]"
  - "[[wiki/concepts/rag-evaluation]]"
---

# High-Level GraphRAG Architecture Built on Top of MCP Servers

> [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers|Raw]] · local

## Summary

A lecture transcript, and the most complete single account of the wiki's GraphRAG
architecture — it starts from *why* rather than *how*. Two problems motivate
everything: **context rot** (noise accumulates until the signal-to-noise ratio
collapses, with the lost-in-the-middle bias on top) and **data fragmentation**
(the data lives in emails, notes, articles, messages, databases, and never in one
place with a clean API).

The story starts at the **ontology**, described as "a collection of classes and
how they interact" — document, person, task, episode, preference, with typed
relationships between them. Three extraction methods are distinguished and, in
practice, combined: structured (schema-guided), semi-structured (metadata and
lineage — references and authorship need no LLM), and unstructured (no schema,
useful for discovery). On whether the LLM should be allowed to invent types: use
open-ended extraction while exploring, then **stick to the ontology**, because
otherwise the output "will quickly become such a mess that it will be useless" —
and constraining it is also cheaper and faster.

Five components follow: data pipeline, memory pipeline, unified memory,
knowledge graph, agent. The immutable-log argument is made in its most general
form here — append-only storage gives **versioning, temporality and
reversibility**, which matters precisely because "we work with LLMs here and they
fail really often." Materialization squashes logs by ID, and can be partial: a new
observation about one person re-squashes only that person.

Retrieval comes in two shapes. **Bottom-up** — text plus semantic search for entry
points, fused with RRF, then two or three hops, optionally annotated with
communities. **Top-down** — the same entry points, but retrieving *communities*
and hopping between them through bridge nodes, answering from their summaries when
you want an overview rather than detail. Then the line the wiki keeps returning
to: GraphRAG "in reality is just this multi-hop traversal step during retrieval."

The Q&A is where the honesty is. Keeping the data clean is "probably the most
complicated part of all of this", and the answer is an evals layer, extracted
rules for good and bad data, housekeeping pipelines, and soft deletes that the log
makes reversible. On evaluation: retrieval metrics (precision, recall, ranking)
where the hard part is building the query→expected-item dataset, plus six
system-level metrics from the combinations of question, answer and context.

## Key claims

- Context rot and data fragmentation are the two problems GraphRAG exists to address. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Use open-ended extraction only while exploring; past that, adhere to the ontology or the graph becomes unusable — and constraining it is cheaper and faster. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Immutable logs give versioning, temporality and reversibility — necessary because LLM extraction fails often. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Materialization can be partial: a new log for one entity re-squashes only that entity, not the whole graph. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Embeddings are computed at materialization because "it is super hard to compute an embedding on an object that does not have its full state." [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Two retrieval shapes: bottom-up (entities, then hops) for detail, top-down (communities and bridge nodes) for overview. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Two or three hops is enough for most applications, which is why a general-purpose database is usually the right choice over a specialized graph engine. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Data cleanliness is the hardest part, and the log is what makes housekeeping safe: classify, soft-delete, re-materialize, revert if wrong. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]
- Concurrent reads and writes are the database's problem, not the pipeline's — the worst case is a slightly stale entity. [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|cite]]

## Notable quotes

> "GraphRAG, different from normal RAG, in reality is just this multi-hop traversal step during retrieval."
> — [[raw/high-level-graphrag-architecture-built-on-top-of-mcp-servers#Linking Memory to Context via Knowledge Graphs and Ontologies|location]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/mcp]], [[wiki/entities/neo4j]], [[wiki/entities/voyage-ai]]
- **Concepts**: [[wiki/concepts/knowledge-graph]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/graph-communities]], [[wiki/concepts/context-rot]], [[wiki/concepts/data-fragmentation]], [[wiki/concepts/agentic-search]], [[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-freshness]], [[wiki/concepts/rag-evaluation]]

> Synthesis: The best single entry point to the wiki's memory half — and note that it is a transcript of the same talk recorded in [[wiki/sources/graphrag-presentation]], so the two corroborate each other only in the sense that a recording corroborates its own summary.
