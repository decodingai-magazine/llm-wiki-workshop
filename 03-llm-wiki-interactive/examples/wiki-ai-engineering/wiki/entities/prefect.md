---
type: entity
title: Prefect
description: The workflow orchestrator behind every pipeline in this wiki, argued into the agent runtime itself, and the vendor behind the MCP framework the servers are built with.
aliases: [Prefect Cloud, Horizon]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/four-prefect-task-runners-four-different-problems]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-ingest-1-000-000-documents-into-your-agent-memory]]"
  - "[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/normalization-entity-resolution]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/what-to-focus-on]]"
  - "[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
  - "[[wiki/concepts/read-write-separation]]"
  - "[[wiki/entities/fastmcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 20
---

# Prefect

> Decorators on ordinary Python that add retries, caching, scheduling and observability — and, in these notes, part of the agent runtime rather than infrastructure beside it.

## Definition

Prefect orchestrates every pipeline described in this wiki: data ingestion, memory
extraction, materialization and indexing
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. Its architectural claim is that
long-running agents need durable execution, retries, checkpoints, human approvals
and observability, which makes a workflow engine part of the runtime layer
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]].

Its structural claim is separation: a server that coordinates and never executes,
work pools that are queues in a database, and workers that poll and run — so
scaling changes a deployment target, not pipeline code
[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]].

## Key claims

- Tasks should be thin wrappers around pure functions, so business logic stays testable and runnable without the orchestrator. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- The staged scaling path — `serve()`, Docker work pool, Kubernetes or push pool — changes one line and no flow code. [[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]
- Four independent concurrency controls exist, and only the global one protects a shared API across machines. [[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]
- Queue priority drains as a waterfall rather than round-robin — not what most people expect. [[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]
- It survives agentic coding because the worker *is* a Python process: restarting after a code change takes about two seconds. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- For most API-driven pipelines no task runner is needed at all — `asyncio.gather()` with a semaphore is the right tool. [[wiki/sources/four-prefect-task-runners-four-different-problems]]
- It is used asymmetrically on purpose: write paths are orchestrated, read paths deliberately are not. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- The honest limits: it adds infrastructure, knows nothing about prompts or models, buffers streaming, and is overkill for single-shot calls. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- The same vendor builds the MCP framework these servers use, which is why the two layers share idioms and deploy together. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]], [[wiki/sources/owning-your-context-layer]]
- In day-to-day development, the same author reaches for its CLI rather than an MCP server. [[wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/concepts/durable-execution]]**: the property Prefect is brought in to provide.
- **[[wiki/concepts/pipeline-parallelism]]**: work pools and task runners are its two axes.
- **[[wiki/entities/fastmcp]]**: same vendor; the two split the execution substrate and the protocol surface.

> Synthesis: Twenty sources mention it and several are sponsored, so the discount applies — but the load-bearing claims here are structural (server/pool/worker, four concurrency layers, thin tasks) and those are checkable against the docs rather than against the author.
