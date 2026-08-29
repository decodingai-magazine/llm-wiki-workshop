---
type: concept
title: Knowledge graph
description: Typed entities and relationships extracted from documents so retrieval can follow connections instead of only matching text — the structural half of the memory layer.
aliases: [GraphRAG, KG, Property graph]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/mongodb-notes-on-scaling-from-the-meeting]]"
  - "[[wiki/sources/normalization-entity-resolution]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/questions-and-remarks-from-people-while-posting]]"
  - "[[wiki/sources/rdf-vs-labeled-property-graphs]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/rrf-fusion-hybrid-search-without-reranker]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/tivadar-danka-knowledge-graph-questions]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
related:
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/graph-communities]]"
  - "[[wiki/concepts/unified-memory]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 22
---

# Knowledge graph

> Nodes and edges built from documents, so a query can reach what is *connected* to the answer rather than only what resembles it.

## Definition

A knowledge graph here is **built, not authored**: documents are chunked, an LLM
extracts entities and relationships against a fixed ontology, and structural
entries — document nodes, chunk nodes, `part_of`, `next`, `mentions`,
`referenced` — are added deterministically without a model
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. The ontology comes first and is
described as the single most important design step: without it, extraction is
"unconstrained text generation that happens to output JSON"
[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]].

Two modelling questions recur. **Where metadata lives**: RDF makes every attribute
its own triple, which is uniform, larger, and demands the full data model up
front; property graphs hang attributes on nodes and edges, which is why modern
GraphRAG uses them [[wiki/sources/rdf-vs-labeled-property-graphs]]. **How many
types**: small and specific — six node types and eight edge types in every build
described here, because "entity" and "relationship" are too vague and fifty types
produce a sparse graph nobody can extract reliably.

The definition that survives all of it:
**GraphRAG is normal RAG plus one step — multi-hop traversal at retrieval time**
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]].

## Key claims

- The graph is an *expansion* mechanism, not a primary index: similarity finds the entry point, edges find what is connected to it. [[wiki/sources/retrieval-strategies]]
- Nodes and edges live in one collection so recursive traversal can run over them, with `"type:name"` ids that are deterministic and human-readable. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- Traversal is bidirectional by construction — outgoing and incoming passes — and reverse edges are created only for the node-type pairs that need them. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- Two or three hops is what real questions need; deeper traversal is where specialized graph engines start to matter. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]], [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Graph edges surface facts no embedding could reach — in the worked example, an episode and a task that share no words with the query. [[wiki/sources/graphrag-presentation]]
- A graph is optional: start with the simplest retrieval that works and add it when the extra signal is worth the cost. [[wiki/sources/owning-your-context-layer]]
- Skipping topic and domain entities is a deliberate choice — embedding clusters approximate them without the maintenance. [[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]
- The minimal viable graph is smaller than these builds suggest: one JSON file, adjacency arrays, no normalization, rendered in a browser. [[wiki/sources/tivadar-danka-knowledge-graph-questions]]

## Relationships

- **[[wiki/concepts/graph-extraction]]**: how the graph gets built, and the three strategies for building it.
- **[[wiki/concepts/entity-resolution]]**: what keeps one entity from becoming six.
- **[[wiki/concepts/hybrid-search]]**: phase one of retrieval; the graph is phase two.
- **[[wiki/concepts/append-only-log]]**: how the graph's history is kept correctable.

> Synthesis: Every source here agrees on the mechanics and differs only on how much machinery a given scale deserves — which makes "how many hops do my questions actually need?" the most useful sizing question in the wiki.
