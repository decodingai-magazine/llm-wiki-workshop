---
type: source
title: Agentic GraphRAG via MCP Servers
description: An end-to-end technical report on a digital-twin memory — ETL into MongoDB, LLM graph extraction, hybrid retrieval, and a six-tool FastMCP server that any harness can drive.
origin: local
original_path: data_input_examples/notes/02-medium/Agentic GraphRAG via MCP Servers.md
source_url: null
authors: []
published_date: null
raw_file: raw/agentic-graphrag-via-mcp-servers.md
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/context-layer]]"
---

# Agentic GraphRAG via MCP Servers

> [[raw/agentic-graphrag-via-mcp-servers|Raw]] · local

## Summary

The most complete build description in the wiki: an end-to-end report on a
personal digital twin, from ingestion to the MCP server a harness talks to. Five
ETL pipelines (Substack RSS and articles, arXiv via HuggingFace, local files,
conversations) normalize everything into one `documents` collection, deduplicated
by a unique `source_uri` — the same "identity is the source URI" move this wiki
makes with raw paths. Unresolved references become **LATENT placeholder
documents** that get upgraded when the target is ingested later.

A five-stage memory pipeline turns documents into a knowledge graph: chunk at 512
tokens, LLM-extract nodes and edges per chunk against a fixed ontology, add
*structural* entries deterministically (document and chunk nodes, `part_of`,
`next`, `mentions`, `referenced` edges), normalize with fuzzy matching at 0.85,
then bulk-upsert idempotently. The ontology is small and enforced in code — six
node types, eight edge types — so the LLM cannot invent an edge the schema
forbids.

Retrieval offers three strategies with different shapes: hybrid vector + text
search fused by RRF and expanded one hop through `$graphLookup`; a natural
language query compiled by the LLM into a validated MongoDB aggregation pipeline;
and a deep search that writes one markdown file per node to disk and returns a
YAML index for the harness to read selectively.

The last third is the part other notes only assert: the server is a thin
delegation layer that owns zero business logic, and the harness integration is
three stacked layers — the MCP server (portable everywhere), skills (Claude Code
only, teaching tool selection), and hooks (Claude Code only, auto-ingesting each
conversation). Layer 1 works in every harness; 2 and 3 degrade gracefully.

## Key claims

- The MCP layer is a delivery mechanism, not a logic layer — every tool handler delegates to business logic that batch pipelines call identically. [[raw/agentic-graphrag-via-mcp-servers#6. Building the GraphRAG FastMCP Server|cite]]
- Nodes and edges share one collection discriminated by `kind`, which is what makes `$graphLookup` multi-hop traversal and single-index maintenance possible. [[raw/agentic-graphrag-via-mcp-servers#3. Knowledge Graph Data Model|cite]]
- Six tools are enough: three read (`search_memory`, `query_memory`, `deep_search_memory`) and three write (`ingest_url`, `ingest_file`, `ingest_conversation`). [[raw/agentic-graphrag-via-mcp-servers#7. MCP Tool Design: Search + Write|cite]]
- Deep search implements progressive disclosure: write per-node markdown to disk, return a YAML index, let the harness read only what it needs. [[raw/agentic-graphrag-via-mcp-servers#7. MCP Tool Design: Search + Write|cite]]
- Skills tell the model *what it should do* where tool docstrings only say *what it can do* — a decision tree for picking between the three search tools. [[raw/agentic-graphrag-via-mcp-servers#8. Skills: Teaching the Harness When to Use Each Tool|cite]]
- Ingestion runs inline rather than through Prefect because the user is waiting: one `ingest_url` call goes from URL to queryable graph. [[raw/agentic-graphrag-via-mcp-servers#7. MCP Tool Design: Search + Write|cite]]
- Embeddings are always stripped from tool output — a 384-dim array costs ~1500 tokens and tells the model nothing. [[raw/agentic-graphrag-via-mcp-servers#7. MCP Tool Design: Search + Write|cite]]

## Notable quotes

> "Layer 1 is portable. Layers 2 and 3 are progressive enhancements that make the experience richer in harnesses that support them, while degrading gracefully in those that don't."
> — [[raw/agentic-graphrag-via-mcp-servers#9. Hooking the MCP Server to a Harness (Claude Code, OpenCode, etc.)|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/fastmcp]], [[wiki/entities/mongodb]], [[wiki/entities/claude-code]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/knowledge-graph]], [[wiki/concepts/unified-memory]], [[wiki/concepts/agent-memory]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/mcp-server-design]], [[wiki/concepts/agent-skills]], [[wiki/concepts/agent-harness]], [[wiki/concepts/context-layer]]

> Synthesis: This is the note that turns the wiki's abstractions into a bill of materials — several claims other sources make as principles ("design for the agent", "progressive discovery") appear here as file paths and default parameter values.
