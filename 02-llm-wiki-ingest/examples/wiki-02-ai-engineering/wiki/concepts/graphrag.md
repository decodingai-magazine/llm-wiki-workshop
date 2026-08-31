---
type: concept
title: GraphRAG
description: A retrieval pattern that augments vector/semantic search with graph traversal over a knowledge graph of typed nodes and edges, so an agent pulls in multi-hop connected context instead of isolated chunks.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
related:
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/vector-search]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/event-sourcing]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 2
---

# GraphRAG

> Retrieval-augmented generation that expands vector search results with graph traversal over connected nodes, rather than returning isolated chunks.

## Definition

The two sources frame GraphRAG at different altitudes rather than disagreeing outright. [[wiki/sources/agentic-graphrag-via-mcp-servers]] treats GraphRAG as a full agent-memory architecture: document content is passed through a fixed 5-stage extraction pipeline (chunk → LLM entity/edge extraction → deterministic structural entries → fuzzy/cross-document normalization → idempotent upsert) into a typed ontology of 6 node types and 8 edge types, then served through three distinct retrieval strategies matched to query shape rather than one generic "graph search." [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]] frames GraphRAG more narrowly, as the "context expansion" step itself — vector search results widened by graph traversal — and treats hop depth as the key variable that determines whether a single database can carry the workload or whether a dedicated graph engine becomes necessary.

Both sources converge on MongoDB's `$graphLookup` as a viable traversal mechanism for GraphRAG at shallow depth, and both discuss it in the context of a single collection holding both content and graph structure.

## Key claims

- GraphRAG retrieval is commonly split by query shape: a forgiving default that fuses vector + text search (Reciprocal Rank Fusion) with 1-hop graph expansion, an LLM-generated/whitelist-validated aggregation path for precise or aggregate questions, and a wide 50-seed/3-hop "deep search" that writes results out via progressive disclosure to avoid overflowing the context window. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Nodes and edges can be stored together in one collection, discriminated by a `kind` field and addressed by composite string IDs (`"type:name"`), which is what makes single-collection graph traversal and atomic upserts practical. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- `$graphLookup` performs recursive multi-hop traversal and is reported sub-second at the 2–3 hop depths described as typical for GraphRAG context expansion. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Past roughly 5 hops, native graph databases (e.g. Neo4j) are reported to hold flat latency while MongoDB's traversal response time grows past 2 seconds — the basis for a decision rule that unified MongoDB suffices for GraphRAG while reasoning stays within 2–3 hops, with deeper traversal or pathfinding pushed to dedicated graph stores. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]

## Relationships

- **[[wiki/concepts/agent-memory]]**: GraphRAG is the retrieval half of an agent memory system in both sources — the graph structure is what memory is stored as, GraphRAG is how it's queried back out. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- **[[wiki/concepts/vector-search]]**: both sources pair GraphRAG with vector/semantic search rather than treating graph traversal as a replacement for it — vector search finds entry points, graph traversal expands context around them. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- **[[wiki/concepts/progressive-disclosure]]**: the "deep search" strategy applies progressive disclosure specifically to keep a wide graph traversal from overflowing the agent's context window. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- **[[wiki/concepts/mcp]]**: the extraction/query logic behind GraphRAG is exposed to an agent as MCP tools in a logic-free delivery layer, so the same code path serves both interactive and batch use. [[wiki/sources/agentic-graphrag-via-mcp-servers]]

> Synthesis: Both sources describe GraphRAG through MongoDB's specific traversal mechanics (`$graphLookup`, single-collection node/edge storage) rather than the pattern in the abstract, so this page currently reflects a MongoDB-centric view of GraphRAG — the mongodb-for-an-ai-agent-unified-memory source is explicit that its performance figures are vendor-cited rather than independently benchmarked, which tempers how much weight the 2–3 hop threshold should carry on its own.
