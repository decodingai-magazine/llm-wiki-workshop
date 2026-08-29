---
type: source
title: I tested all 4 Prefect task runners — the decision tree I wish existed
description: Async I/O, sync blocking I/O, CPU-bound and GPU-bound work need four mechanically different concurrency tools; most API-driven pipelines need none of them.
origin: local
original_path: data_input_examples/notes/03-hard/_four-prefect-task-runners-four-different-problems.md
source_url: null
authors: []
published_date: null
raw_file: raw/four-prefect-task-runners-four-different-problems.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/durable-execution]]"
---

# I tested all 4 Prefect task runners — the decision tree I wish existed

> [[raw/four-prefect-task-runners-four-different-problems|Raw]] · local

## Summary

The note opens with a real bug: an extraction pipeline that "looked concurrent —
it's all async Python" but processed documents one at a time, because
`for doc in docs: await task(doc)` is sequential. 100 documents at 30 seconds each
is 50 minutes. The fix was already present deeper in the same codebase —
`asyncio.gather()` with a semaphore capping concurrency at 5 — and it brings the
same work to about 5 minutes.

The substance is the mechanical comparison. **`asyncio.gather()`**: one thread,
cooperative switching at `await` points, zero overhead, zero serialization — right
for async I/O, useless for CPU work. **ThreadPoolTaskRunner**: OS threads for
*sync* blocking calls like `requests.get()`; putting async tasks on it means every
thread spins up its own event loop, paying overhead for no benefit — the author's
own mistake, stated as such. **DaskTaskRunner**: separate interpreters, so the GIL
stops mattering and CPU-bound work parallelizes, at the cost of pickling data
between processes. **RayTaskRunner**: the same, plus first-class GPU scheduling —
`remote_options(num_gpus=1)` routes tasks to workers with free GPUs and mixes CPU
and GPU tasks in one flow.

The conclusion is deflationary and honest: for most people building API-driven
pipelines, **no task runner is needed at all** — `asyncio.gather()` plus a
semaphore is plain Python. Task runners start earning their place with local
models (Ray), heavy CPU work (Dask), or legacy sync code (threads).

## Key claims

- `for x in xs: await task(x)` is sequential; the concurrency comes from `asyncio.gather()`, not from `async`. [[raw/four-prefect-task-runners-four-different-problems#The problem I ran into|cite]]
- Putting async tasks on a thread pool gives each thread its own event loop — overhead for nothing. [[raw/four-prefect-task-runners-four-different-problems#How each runner works mechanically|cite]]
- Dask and Ray escape the GIL by using separate interpreters, and pay for it in serialization. [[raw/four-prefect-task-runners-four-different-problems#How each runner works mechanically|cite]]
- Pass IDs, not objects, to distributed workers — a live database connection is not picklable. [[raw/four-prefect-task-runners-four-different-problems#Gotchas I'd warn people about|cite]]
- Ray's GPU scheduling is first-class where Dask's resource annotations are manual bookkeeping. [[raw/four-prefect-task-runners-four-different-problems#How each runner works mechanically|cite]]
- Nested parallelism multiplies: 90 flow runs × 10 tasks × 5 calls is 4,500 concurrent API calls without a global concurrency limit. [[raw/four-prefect-task-runners-four-different-problems#Gotchas I'd warn people about|cite]]
- "For most Prefect users building API-driven pipelines… you don't need a task runner at all." [[raw/four-prefect-task-runners-four-different-problems#My take|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/durable-execution]]

> Synthesis: The most transferable note in the orchestration cluster, because the decision tree is about the Python runtime rather than about Prefect — the same four answers apply to any framework wrapping the same primitives.
