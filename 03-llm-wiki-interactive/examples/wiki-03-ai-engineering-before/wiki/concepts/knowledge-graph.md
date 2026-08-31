---
type: concept
title: Knowledge Graph
description: A typed-node/typed-edge memory structure, extracted from ingested documents by an LLM+rules pipeline, that an MCP server exposes for structured, multi-hop retrieval over an agent's memory.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/agent-memory]]"
created: 2026-08-29T16:14:54Z
timestamp: 2026-08-29T16:14:54Z
source_count: 2
---

# Knowledge Graph

> Entities and relationships extracted from ingested documents, stored as nodes and edges, and reached only through an MCP server rather than direct database access.

## Definition

The two sources describe the same kind of object from different altitudes. [[wiki/sources/agentic-graphrag-via-mcp-servers]] gives the data-model view: nodes and edges live together in a single MongoDB `knowledge_graph` collection, discriminated by a `kind` field and addressed by composite string IDs (`person:paul iusztin`), specifically so `$graphLookup` can do multi-hop traversal without joining across collections. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] gives the pipeline view: a memory pipeline turns normalized documents into knowledge-graph objects — entities and relationships — alongside summary embeddings and source/author/date metadata, then exposes the result through an MCP server as tools for knowledge-graph search and knowledge-graph write.

## Key claims

- The graph combines nodes and edges in a single collection rather than separate ones, using a `kind` discriminator and composite string IDs so a native multi-hop traversal operator can walk relationships without a join. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The graph is populated by an extraction pipeline — described as "LLM+rules" in one source — that reads normalized documents and produces entities/relationships plus document-summary embeddings and metadata. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The graph is never queried directly: one source exposes it through three MCP retrieval strategies of differing precision/breadth (fused vector+text search with one-hop expansion, an LLM-generated validated aggregation query, and a wide dump-to-disk search); the other exposes it through a smaller "knowledge-graph search" / "knowledge-graph write" tool pair plus higher-level "prompts" such as "update episodic memory." [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The graph is one half of a larger memory system, paired with a separate raw-document store (a `documents` collection / "data warehouse") that it is extracted from and can still point back to. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **[[wiki/concepts/mcp]]**: the graph is never queried directly by a client — an MCP server is the delivery mechanism both sources use to make it reachable from an agent or harness. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- **[[wiki/concepts/graphrag]]**: the multi-strategy retrieval built on top of the graph (vector+text fusion, hop expansion, natural-language-to-query translation) is the GraphRAG layer named explicitly in one source. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- **[[wiki/concepts/agent-memory]]**: the graph is presented as the structured, entity/relationship side of a broader memory system that also holds raw documents and embeddings. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

> Synthesis: the two descriptions read as complementary layers of one architecture — the extraction/embedding pipeline in one source plausibly produces exactly the collection described in the other — but both are personal build notes from what appears to be the same author's own system, so this is one voice describing itself twice, not independent corroboration of a general knowledge-graph pattern.
