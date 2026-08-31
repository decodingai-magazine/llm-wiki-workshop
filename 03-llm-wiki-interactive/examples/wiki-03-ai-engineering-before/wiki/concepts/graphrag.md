---
type: concept
title: GraphRAG
description: Retrieval-augmented generation where context is assembled by traversing a knowledge graph — often fused with vector search — rather than by similarity search alone.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/mongodb]]"
created: 2026-08-29T16:14:39Z
timestamp: 2026-08-29T16:14:39Z
source_count: 2
---

# GraphRAG

> Retrieval-augmented generation where context is assembled by traversing a knowledge graph — often fused with vector search — rather than by similarity search alone.

## Definition

Neither source defines GraphRAG in the abstract; both describe it through a concrete implementation, at different altitudes. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]] names the primitive and its performance envelope: GraphRAG needs multi-hop graph traversal, and MongoDB's `$graphLookup` is judged sub-second for "the 2–3 hop traversals typical of GraphRAG context." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]] builds the system around that primitive: a single-collection MongoDB knowledge graph of typed nodes and edges, read back through three complementary retrieval strategies rather than one. Read together, the two agree on what GraphRAG is doing — grounding generation in graph-structured context, on top of MongoDB rather than a dedicated graph database — without either one stating a formal definition.

## Key claims

- A GraphRAG knowledge graph can live as nodes and edges together in one MongoDB collection, discriminated by a `kind` field and addressed by composite string IDs (e.g. `person:paul iusztin`), so `$graphLookup` traverses multiple hops without a cross-collection join. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
- `$graphLookup` performs at ~25ms–1s for the 2–3 hop traversals typical of GraphRAG context; a dedicated graph database like Neo4j only pulls ahead once traversals reach 5+ hops. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- A practical GraphRAG system benefits from more than one retrieval strategy: a forgiving default (vector+text fusion via Reciprocal Rank Fusion, then a one-hop graph expansion) for most questions, an LLM-to-aggregation-pipeline path for precise/count questions, and a wide, disk-spilling strategy for exploratory ones. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
- A GraphRAG graph's state can be versioned as event sourcing — an append-only events collection replayed through aggregation-pipeline views, with periodic snapshotting to avoid full replay — rather than mutated in place. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]

## Relationships

- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/knowledge-graph]]**: the structure GraphRAG retrieves over; both sources build it as typed nodes/edges in a single MongoDB collection rather than a dedicated graph database. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- **[[wiki/concepts/hybrid-search]]**: the `search_memory` strategy's RRF fusion of vector and text search, followed by one-hop graph expansion, is a hybrid-search layer sitting in front of the graph. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]**: GraphRAG is framed as one of four memory layers — alongside operational, vector, and event-sourced — that make up an AI agent's unified memory. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/mongodb]]**: both sources use MongoDB (`$graphLookup`, single-collection storage) as the engine for GraphRAG instead of a dedicated graph database, and both bound that choice to shallow (2–3 hop) traversal depth. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]

> Synthesis: Both sources describe the same `$graphLookup`/single-collection pattern, and the graph-building source's example data (`person:paul iusztin`) suggests they trace to the same author's own project, viewed from two angles — a build report versus a general memory-architecture argument. Treat this as one strong witness rather than two independent ones until a third, unrelated source corroborates the pattern.
