---
type: concept
title: Unified memory
description: One store holding everything an agent knows — personal notes, research, preferences, episodes — exposed through a small search-and-write tool surface.
aliases: [Agent memory layer]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 5
---

# Unified memory

> One memory for everything the agent knows — ingested documents, extracted entities and relationships, embeddings and user preferences — behind two tools.

## Definition

The build is a two-pipeline shape: a data pipeline that normalizes any input
(dataset, article, video, image) into documents, and a memory pipeline that turns
documents into knowledge-graph objects, computes embeddings over each document's
summary, attaches provenance metadata, and writes the result into memory. The read
and write surface is deliberately tiny — knowledge-graph search and
knowledge-graph write
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

The second source states the motivation for exposing it over a server rather than
a CLI: the write and search logic is business-specific, the infrastructure is
hosted, and the same memory has to be reachable from whichever harness the user
picks [[wiki/sources/why-mcp-is-not-dead]].

## Key claims

- The memory ingests everything — notes, emails, arXiv papers, YouTube videos, articles — into one store rather than per-source silos. [[wiki/sources/why-mcp-is-not-dead]]
- Documents become knowledge-graph objects via an extractor; embeddings are computed over the document summary, not the raw text. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Two tools are enough for the interface: search the memory, write to the memory. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Preferences and episodes are detected from conversation and written back automatically, which is what makes the memory personal rather than archival. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Specific business logic plus hosted infrastructure is what makes MCP the right exposure for this memory — "doing this through a CLI would have been a nightmare." [[wiki/sources/why-mcp-is-not-dead]]
- Build it with the simplest tool that works — filesystem, BM25, semantic search — and add the knowledge graph only when the use case demands the extra signal. [[wiki/sources/owning-your-context-layer]]
- Consolidating into one store avoids the synchronization tax of polyglot persistence: cross-database ETL, inconsistency risk and four security models. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- In the built version the surface is six tools — three to read (hybrid, structured, deep) and three to write (URL, file, conversation). [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The thresholds where one store stops being the right answer: past ~100M vectors, past 5-hop traversals, or when analytical replay threatens interactive latency. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]

## Relationships

- **[[wiki/concepts/knowledge-graph]]**: the representation the memory is written into.
- **[[wiki/concepts/agent-memory]]**: the episodic/semantic distinction that governs what gets written.
- **[[wiki/concepts/mcp-server-design]]**: the two-tool surface is this idea applied.

> Synthesis: "Unified" is doing the load-bearing work here — the architectural claim is not about a database but about refusing to let each source keep its own retrieval path.
