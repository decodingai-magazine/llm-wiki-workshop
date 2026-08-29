---
type: concept
title: Pipeline parallelism
description: Two independent axes — many runs across machines, many tasks inside a run — plus the rule that each stage's bottleneck must scale on its own.
aliases: [Two axes of parallelism, Task runners, Work pools]
sources:
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/four-prefect-task-runners-four-different-problems]]"
  - "[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
related:
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/entities/prefect]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 5
---

# Pipeline parallelism

> Flow-level parallelism spreads runs across machines; task-level parallelism runs tasks inside a run. They are independent, and they multiply.

## Definition

**Flow-level**: work pools and workers distribute many runs — three workers at a
limit of 30 gives 90 concurrent runs, and the pipeline code does not change.
**Task-level**: a task runner or `asyncio.gather()` runs many tasks inside one
run — and this one always changes the code. Ninety runs times ten tasks is 900
operations in flight
[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]].

Inside a run, the choice is mechanical rather than stylistic: async I/O →
`asyncio.gather()` with a semaphore (no task runner at all); sync blocking I/O →
threads; CPU-bound → separate processes; GPU-bound → a GPU-aware scheduler
[[wiki/sources/four-prefect-task-runners-four-different-problems]].

## Key claims

- `await task()` in a loop is sequential; `async` alone buys nothing. [[wiki/sources/four-prefect-task-runners-four-different-problems]], [[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]
- Putting async tasks on a thread pool gives each thread its own event loop — pure overhead. [[wiki/sources/four-prefect-task-runners-four-different-problems]]
- For most API-driven pipelines no task runner is needed at all. [[wiki/sources/four-prefect-task-runners-four-different-problems]]
- Every stage has a different bottleneck — LLM serving, database I/O, CPU — and treating them alike "leaves performance on the table". [[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]
- Queue-and-pull absorbs spikes: add workers, no re-sharding. [[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]
- Distributed workers need references, not objects — a live database connection is not serializable. [[wiki/sources/four-prefect-task-runners-four-different-problems]]
- The two axes multiply into rate-limit breaches unless a global, server-side concurrency limit caps the total. [[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]

## Relationships

- **[[wiki/concepts/durable-execution]]**: parallelism multiplies failures, which is why the two always ship together.
- **[[wiki/entities/prefect]]**: the concrete implementation in every source here.

> Synthesis: Three sources describe these axes and two of them share most of their text — so treat the decision tree as one well-tested opinion rather than as independent corroboration.
