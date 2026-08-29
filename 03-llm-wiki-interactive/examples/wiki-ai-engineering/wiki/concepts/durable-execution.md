---
type: concept
title: Durable execution
description: Retries, result caching, checkpoints, scheduling and observability — the layer that decides whether a multi-step agent pipeline survives contact with production.
aliases: [Async tasks, Long-running work, Workflow orchestration]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/four-prefect-task-runners-four-different-problems]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]"
related:
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/read-write-separation]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/entities/prefect]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 15
---

# Durable execution

> The AI framework decides how the agent thinks. The durability layer decides whether it survives — and it is the harder half to add later.

## Definition

Durable execution wraps a pipeline so that failure costs only the failed step.
Three primitives do most of it: a flow as an observable unit, tasks with their own
retry policies, and **result persistence** so a retry loads completed steps from
cache instead of re-running them
[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]].

Two properties make it agent-specific. Agents are long-running rather than
request-response, which pulls retries, checkpoints, human approvals and
observability into the runtime
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]. And
agents decide their next action at runtime, so a precompiled DAG cannot express
them — the orchestrator must instrument ordinary control flow rather than replace
it.

## Key claims

- Without caching, a retry re-runs successful steps: burned tokens, duplicated side effects, and hours spent debugging double writes. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- The waste is quantified twice — ~$270/month for an agent pipeline, ~$465/month for a document ingestion at a 5% failure rate. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]], [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Different components need different retry policies: exponential backoff for rate limits, fast retries for transient I/O. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Cache keys must include the model and ontology version, or a model change silently reuses stale results. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Writes need idempotency keys — an acknowledged write plus a lost response is a duplicate event. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Partial failure must not block searchability: indexing runs even when extraction partly failed. [[wiki/sources/retrieval-strategies]]
- The orchestrator should stay thin — decorators over pure functions that remain testable and runnable without it. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]], [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- Streaming inside a durable flow is buffered, not real-time — token streaming has to live outside it. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- Read paths are deliberately left un-orchestrated: cheap, idempotent, already retried by the agent. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- Applied to an agent loop rather than a pipeline: each turn is checkpointed, so a crash replays finished turns from cache. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Human-in-the-loop survives the same way — gated tools pause on durable waits resolved out of band. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/concepts/read-write-separation]]**: durability applies to half the system on purpose.
- **[[wiki/concepts/pipeline-parallelism]]**: parallelism multiplies failures, which is why the two ship together.
- **[[wiki/entities/prefect]]**: the implementation in every source here.

> Synthesis: The recurring argument is economic rather than technical — durability is sold on the cost of repeated work, not on uptime, which is probably why it keeps winning against "just add better error handling".
