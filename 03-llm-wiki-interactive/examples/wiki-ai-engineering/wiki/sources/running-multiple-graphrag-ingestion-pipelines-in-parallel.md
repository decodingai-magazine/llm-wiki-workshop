---
type: source
title: Two dimensions of parallelism — pipelines in parallel vs. tasks in parallel
description: Flow-level and task-level parallelism are independent axes that multiply, and most pipelines only use one — worked through to a million-document ingestion plan.
origin: local
original_path: data_input_examples/notes/03-hard/Running multiple GraphRAG ingestion pipelines in parallel vs. running multiple tasks in parallel.md
source_url: null
authors: []
published_date: null
raw_file: raw/running-multiple-graphrag-ingestion-pipelines-in-parallel.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/embeddings]]"
---

# Two dimensions of parallelism — pipelines in parallel vs. tasks in parallel

> [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel|Raw]] · local

## Summary

The framing this note adds to the task-runner material is a single mental model:
**two independent axes that multiply.** *Flow-level* parallelism distributes many
flow runs across machines through work pools and workers — three workers at a
limit of 30 gives 90 concurrent runs, and your flow code does not change.
*Task-level* parallelism runs many tasks inside one flow run through a task runner
or `asyncio.gather()` — and that one *does* change your code. Ninety runs times
ten concurrent tasks is 900 operations in flight.

The diagnosis is the same one made elsewhere in the wiki and it is worth the
repetition: `await task()` inside a `for` loop is sequential. "The `async` keyword
doesn't automatically mean concurrent." The same codebase already had the correct
pattern one layer down, in a function using `asyncio.gather()` with a semaphore —
it simply had not been applied at the pipeline level.

The second half is a capacity plan rather than an argument: one million documents
through three phases. Ingestion as a million flow runs on a CPU pool with
`asyncio.gather()` inside each, ~90 concurrent, ~15 hours. Extraction as 10,000
batched runs on a GPU pool with Ray inside each, four GPUs per worker, ~1.4 hours
(flagged `[VERIFY]` in the source). Materialization as a single run of ~30
minutes, mostly server-side aggregation. Global concurrency limits sit across
everything so the two axes cannot multiply into a rate-limit breach.

The closing point is the durable one: the business logic does not change across
scaling stages. Today `asyncio.gather()` against a hosted API; tomorrow a Ray task
runner against local models on GPUs. The deployment target and the task runner
change; chunk, extract, normalize, store do not.

## Key claims

- Flow-level and task-level parallelism are independent and multiply; most pipelines use only the first. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#The two axes of parallelism in Prefect|cite]]
- Flow-level scaling needs no code change; task-level scaling always does. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#The two axes of parallelism in Prefect|cite]]
- `async` means a function *can* yield, not that it runs concurrently — `asyncio.gather()` is what parallelizes it. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#The problem: sequential execution hiding in plain sight|cite]]
- A million-document plan: ~15 hours of ingestion, ~1.4 hours of GPU extraction, ~30 minutes of materialization. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#The 1M document scenario: both axes combined|cite]]
- Global concurrency limits are what stop the two axes from multiplying into a rate-limit breach. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#The 1M document scenario: both axes combined|cite]]
- Business logic survives every scaling stage; only the deployment target and task runner change. [[raw/running-multiple-graphrag-ingestion-pipelines-in-parallel#Key takeaways|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/durable-execution]], [[wiki/concepts/embeddings]]

> Synthesis: This note and [[wiki/sources/four-prefect-task-runners-four-different-problems]] share most of their body — same diagrams, same decision tree, same bug — so treat their overlapping claims as **one** source, not two. What is genuinely unique here is the two-axes model and the million-document capacity plan.
