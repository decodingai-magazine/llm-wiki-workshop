---
type: concept
title: Orchestrate the writes, never the reads
description: Ingestion is slow, expensive and failure-prone, so it belongs in a durable workflow; queries are cheap and idempotent, so orchestrating them only adds latency.
aliases: [Read path, Write path]
sources:
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/retrieval-strategies]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/graphrag-ingestion]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 2
---

# Orchestrate the writes, never the reads

> The two halves of a memory system have opposite shapes, and the design rule follows: durability on the write path, nothing in the way of the read path.

## Definition

Ingestion is minutes long, side-effectful, rate-limited and failure-prone, so
every write tool dispatches into a durable flow with retries and per-task
isolation — an upstream error stops being the agent's problem
[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]. Queries are
cheap, read-only and idempotent, and the agent already retries, so wrapping them
"would add latency for zero durability gain — a deliberate choice, not an
oversight."

Stated as a rule: "Orchestrate the writes, never the reads — the only thing they
should share is a rate limit" [[wiki/sources/retrieval-strategies]].

## Key claims

- Write tools return in milliseconds by submitting a pipeline run rather than doing the work inline. [[wiki/sources/retrieval-strategies]]
- Partial failure must not block searchability: if extraction partly fails, indexing still runs and the graph stays queryable. [[wiki/sources/retrieval-strategies]]
- Batch rebuilds resume from the failure point instead of re-paying for completed documents. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- The read path stays millisecond-scale precisely because nothing orchestrates it. [[wiki/sources/retrieval-strategies]]
- Reads and writes also have opposite load shapes — bursty versus continuous — which is a second argument for isolating their infrastructure. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]

## Relationships

- **[[wiki/concepts/durable-execution]]**: applied to exactly half the system.
- **[[wiki/concepts/mcp-server-design]]**: "the MCP server is the front desk; the heavy lifting happens in the back office."

## Tensions

- One build runs ingestion **inline** on a tool call, because the user is waiting and a queued job leaves the content unqueryable [[wiki/sources/agentic-graphrag-via-mcp-servers]]; another dispatches to a pipeline and returns immediately [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]. The difference is what the caller expects back — a confirmation of ingestion, or a receipt for it.

> Synthesis: A rare architectural rule with a clean test attached: if a step is idempotent and cheap, orchestration is pure overhead — which generalizes well past memory systems.
