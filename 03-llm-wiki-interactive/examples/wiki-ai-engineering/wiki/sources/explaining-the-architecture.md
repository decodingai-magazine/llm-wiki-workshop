---
type: source
title: Explaining the Architecture
description: A brainstorm-style walkthrough of a second-brain agent — GraphRAG ingestion, an agentic retrieval layer with three memory types, and FastMCP as the serving surface.
origin: local
original_path: data_input_examples/notes/03-hard/Explaining the Architecture.md
source_url: null
authors: []
published_date: null
raw_file: raw/explaining-the-architecture.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/mcp]]"
concepts:
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/embeddings]]"
---

# Explaining the Architecture

> [[raw/explaining-the-architecture|Raw]] · local

## Summary

Deliberately framed as thinking-out-loud — "here are my thoughts so far, what do
you think?" — this is the second-brain agent described in three layers.

**Ingestion.** Documents from the second brain (notes, videos, other media) are
cleaned, run through an open-source knowledge-graph model for entities and
relationships, and summarized by an open-source embedding model; the summary plus
metadata is embedded. The resulting knowledge-graph object supports three
retrievals at once — semantic (vectors), text (metadata), and graph (structured
relationships). Prefect orchestrates it on a schedule or on demand.

**Retrieval.** The agent queries that memory and can also *update* it, and the
note's most useful contribution is naming three memory kinds it maintains:
**episodic** (personal experiences anchored in time), **semantic** (preferences
and style), and **procedural** (how the user likes a post structured). It also
holds external tools — web search, image generation — and an "LLM twin", a
fine-tuned open model that reproduces the author's voice, with the observation
that smaller models often imitate a specific style better than larger reasoning
models. Prefect again handles the agent–tool back-and-forth as the durable
workflow engine.

**Serving.** The whole thing is an MCP server built with FastMCP, so MCP clients
like Claude or Cursor can drive it conversationally — refining ideas agentically
rather than waiting on a single rigid output.

## Key claims

- One knowledge-graph object supports semantic, text and graph retrieval simultaneously. [[raw/explaining-the-architecture#1. The GraphRAG Ingestion Pipeline|cite]]
- The agent maintains three memory kinds: episodic, semantic and procedural. [[raw/explaining-the-architecture#2. The Agentic Retrieval Layer|cite]]
- Smaller fine-tuned models often mimic a specific writing style better than larger reasoning models. [[raw/explaining-the-architecture#2. The Agentic Retrieval Layer|cite]]
- Prefect is used twice — for ingestion *and* for the agent's tool orchestration — as the durable workflow engine. [[raw/explaining-the-architecture#2. The Agentic Retrieval Layer|cite]]
- Serving through FastMCP is what makes the assistant conversational and client-agnostic. [[raw/explaining-the-architecture#3. Serving via FastMCP|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/fastmcp]], [[wiki/entities/mcp]]
- **Concepts**: [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/agent-memory]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/durable-execution]], [[wiki/concepts/embeddings]]

> Synthesis: The bridge note between the wiki's two halves — it is the same architecture the MCP notes describe, told from the memory side, and it adds procedural memory, which no other source names.
