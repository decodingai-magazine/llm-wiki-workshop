---
type: source
title: Agentic GraphRAG via MCP Servers
description: A technical architecture report on building a GraphRAG knowledge-graph memory system as a FastMCP server, plus the Claude Code skills and hooks layered on top of it.
origin: local
original_path: data_input_examples/notes/02-medium/Agentic GraphRAG via MCP Servers.md
source_url: null
authors: []
published_date: null
raw_file: raw/agentic-graphrag-via-mcp-servers.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/hooks]]"
---

# Agentic GraphRAG via MCP Servers

> [[raw/agentic-graphrag-via-mcp-servers|Raw]] · local

## Summary

This is an end-to-end architecture report for a personal knowledge-graph ("digital twin") memory system, written for blog/LinkedIn content rather than as reference docs. It walks the full pipeline from ingestion to retrieval: five ETL pipelines normalize heterogeneous sources (Substack RSS/articles, arXiv, local files, conversations) into one `documents` collection; a five-stage extraction pipeline turns document content into typed nodes and edges against a fixed ontology; a single MongoDB collection holds both nodes and edges for `$graphLookup` traversal; and three distinct query strategies (hybrid search, NL-to-aggregation, and a "deep search" with progressive disclosure) each serve a different question shape.

The second half is about exposing that memory as a **FastMCP** server and wiring it into a harness. The note's central architectural claim is that the MCP server should be a thin, logic-free delivery layer — every tool just extracts context, delegates to existing business logic, and serializes output — so the same code runs identically from an MCP tool call or a batch Prefect flow. It then generalizes its own Claude Code integration (MCP server + Skill + Stop hook) into a reusable "3-layer pattern": a universal MCP layer plus two Claude Code-specific enrichment layers that other harnesses (OpenCode, Cursor, Windsurf) simply don't get.

A worked end-to-end example (ingesting a Substack RSS feed, extracting nodes/edges, indexing, and querying "What does Paul Iusztin think about harness engineering?") ties the abstract pipeline description to concrete commands and data shapes.

## Key claims

- The ETL layer normalizes five source types into one `documents` collection via a shared `BaseETL` contract, using a "LATENT" placeholder document for referenced-but-not-yet-ingested URLs that gets upgraded with real content once that URL is ingested. [[raw/agentic-graphrag-via-mcp-servers#1-data-pipelines-etl-layer|cite]]
- Memory extraction is a fixed 5-stage pipeline (chunk → LLM entity/edge extraction via Gemini → deterministic structural entries → two-phase fuzzy + cross-document node normalization → idempotent bulk upsert) against an ontology of 6 node types and 8 edge types, with edge constraints enforced programmatically rather than left to the LLM. [[raw/agentic-graphrag-via-mcp-servers#2-memory-extraction-pipeline|cite]]
- Nodes and edges are stored together in one MongoDB collection discriminated by a `kind` field and addressed by composite string IDs (`"type:name"`), which the note argues is what makes single-collection `$graphLookup` traversal and atomic upserts practical. [[raw/agentic-graphrag-via-mcp-servers#3-knowledge-graph-data-model|cite]]
- Retrieval is split into three strategies for three query shapes: `search_memory` (vector + text search fused with Reciprocal Rank Fusion, then 1-hop graph expansion) as the forgiving default, `query_memory` (an LLM-generated, whitelist-validated MongoDB aggregation pipeline with self-correcting retry) for precise/aggregate questions, and `deep_search_memory` (a wide 50-seed/3-hop search that writes results to per-node markdown files and returns a lightweight YAML index) for broad exploration without overflowing the context window. [[raw/agentic-graphrag-via-mcp-servers#5-query-logic-3-strategies|cite]]
- The FastMCP server is deliberately logic-free: all 6 tools (3 read, 3 write) only pull lifespan context, delegate to existing business-logic functions, and serialize the result, so the same extraction/indexing/query code runs identically whether triggered by an MCP call or a Prefect batch flow. [[raw/agentic-graphrag-via-mcp-servers#6-building-the-graphrag-fastmcp-server|cite]]
- The note generalizes its own setup into a reusable "3-layer pattern" for any MCP server: Layer 1 (the MCP server) is portable across harnesses; Layer 2 (a Claude Code Skill with a tool-selection decision tree and presentation rules) and Layer 3 (a Stop hook that sentinel-checks and auto-triggers `ingest_conversation`) are Claude Code-specific enrichments that harnesses like OpenCode or Cursor go without. [[raw/agentic-graphrag-via-mcp-servers#9-hooking-the-mcp-server-to-a-harness-claude-code-opencode-etc|cite]]

## Notable quotes

> "This separation is deliberate. The MCP layer is a delivery mechanism, not a logic layer."
> — [[raw/agentic-graphrag-via-mcp-servers#6-building-the-graphrag-fastmcp-server|location]]

> "Tools alone tell the model what it can do. Skills tell it what it should do in context."
> — [[raw/agentic-graphrag-via-mcp-servers#8-skills-teaching-the-harness-when-to-use-each-tool|location]]

## Connections

- **Entities**: [[wiki/entities/fastmcp]], [[wiki/entities/claude-code]], [[wiki/entities/mongodb]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/graphrag]], [[wiki/concepts/agent-memory]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/skills]], [[wiki/concepts/hooks]]

> Synthesis: The first source in this wiki — a founding technical account of the GraphRAG-via-MCP-server pattern and the Claude Code skills/hooks layers built on top of it; nothing yet corroborates or complicates it.
