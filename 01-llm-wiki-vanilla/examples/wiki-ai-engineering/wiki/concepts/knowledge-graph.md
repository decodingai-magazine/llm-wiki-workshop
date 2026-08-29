---
type: concept
title: Knowledge graph
description: Entities and relationships extracted from documents so an agent can reason across hops instead of over isolated chunks — the structured half of the memory layer.
aliases: [GraphRAG, KG]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 4
---

# Knowledge graph

> Nodes and edges extracted from documents, so retrieval can follow relationships instead of only matching text.

## Definition

Across these sources a knowledge graph is built, not authored: documents are
chunked, an LLM extracts nodes and edges per chunk against a fixed ontology, and
deterministic structural entries (document nodes, chunk nodes, `part_of`, `next`,
`mentions`) are added without a model
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. The earlier walkthrough
describes the same shape as "a knowledge graph extractor which extracts entities
and relationships" plus embeddings over the document summary
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

The ontology is deliberately small — six node types and eight edge types, with
edge constraints enforced in code so the LLM cannot produce an edge the schema
forbids [[wiki/sources/agentic-graphrag-via-mcp-servers]]. The graph is one option
among several for a memory layer, not a requirement: filesystem, BM25 and semantic
search come first, and the graph is layered on when higher-signal retrieval is
worth the cost [[wiki/sources/owning-your-context-layer]].

## Key claims

- Extraction is LLM work; structure (document/chunk nodes and their edges) is deterministic and needs no model. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Node identity is a composite string like `person:paul iusztin`, which makes upserts deterministic and IDs human-readable. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Deduplication happens in two phases — fuzzy matching in memory at a 0.85 threshold, then a cross-document merge against stored nodes, with edges remapped to canonical names. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- GraphRAG's value is multi-hop reasoning, and in practice that means 2–3 hops; deeper traversals are where dedicated graph engines win. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- A graph is optional: start with the simplest retrieval that works and add the graph when the use case demands higher signal. [[wiki/sources/owning-your-context-layer]]
- The agent's write surface into the graph is a single tool, paired with a single search tool. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **[[wiki/concepts/hybrid-search]]**: how seed nodes are found before the graph is traversed at all.
- **[[wiki/concepts/agent-memory]]**: the ontology (person, task, episode, preference) is a memory taxonomy in disguise.
- **[[wiki/concepts/append-only-log]]**: how the graph's history is preserved as it is revised.

> Synthesis: The sources agree the graph is a retrieval *expansion* mechanism rather than a primary index — every design here finds seeds by similarity first and only then walks edges.
