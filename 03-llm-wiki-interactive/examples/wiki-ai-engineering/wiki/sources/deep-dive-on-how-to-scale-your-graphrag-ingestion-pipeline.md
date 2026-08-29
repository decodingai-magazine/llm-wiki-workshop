---
type: source
title: Scaling a GraphRAG pipeline from 1 machine to 100 — the worker-queue pattern
description: Prefect's server / work pool / worker split, the staged path from serve() to Kubernetes, and the four independent concurrency controls that keep it from overrunning an API.
origin: local
original_path: data_input_examples/notes/03-hard/Deep dive on how to scale your GraphRAG ingestion pipeline with Prefect with the worker-queue.md
source_url: null
authors: []
published_date: null
raw_file: raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
---

# Scaling a GraphRAG pipeline from 1 machine to 100 — the worker-queue pattern

> [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline|Raw]] · local

## Summary

The infrastructure companion to the parallelism notes: how the same pipeline code
goes from one process to a hundred machines by changing its deployment target.

The mental model is a three-layer separation. The **server** stores deployments,
queues runs, tracks state and enforces limits — and never executes code. **Work
pools** are typed queues living in the server's database, not processes.
**Workers** are polling agents on your infrastructure that claim runs, provision a
container or pod, and report back; they never talk to each other, only to the
server. Multiple workers on one pool is the whole of horizontal scaling.

Two details in that model are easy to get wrong, and the note flags both. Queue
priority is a **waterfall, not round-robin** — every `critical` run executes
before any `standard` run starts. And run distribution is first-come-first-served
queue contention, with no load balancing.

The staged migration is one line at a time: `serve()` for development,
`flow.deploy(work_pool_name="cpu-pool")` for Docker workers across machines, then
a Kubernetes or push pool for autoscaling — "the flow code doesn't change."
Separate pools then express hardware differences: CPU workers at `--limit 30` for
I/O and aggregation, GPU workers at `--limit 1` for local inference, with the GPU
pool scaling to zero when its queue empties.

The section worth stealing is **four independent concurrency controls**: pool
limit (all workers on a pool), queue priority (waterfall ordering), worker
`--limit` (per machine), and **global concurrency limits** enforced server-side
across every worker. The arithmetic explains why the fourth exists: 90 concurrent
runs × 5 LLM calls each is 450 concurrent API calls, and only a global limit can
cap that regardless of how many workers you add.

## Key claims

- The server never executes code; work pools are database queues; workers are the only thing that runs anything. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#Prefect's three-layer architecture|cite]]
- Queue priority drains as a waterfall, not round-robin — which is "not what most people expect". [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#Work pools, queues, and workers in detail|cite]]
- Scaling changes one deployment line: `serve()` → Docker pool → Kubernetes or push pool. Flow code is untouched. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#Step-by-step scaling path|cite]]
- Push pools remove workers entirely — no polling delay, no heartbeats, scale to zero. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#How scaling differs by pool type|cite]]
- Four concurrency layers exist and only the global one protects a shared external API across machines. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#The four layers of concurrency control|cite]]
- Splitting CPU and GPU pools is a cost pattern: cheap workers always on, GPU workers only while their queue has work. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#GPU vs CPU work pool separation|cite]]
- Throughput arithmetic: 90 concurrent runs at ~5s each drains a million-run queue in ~15 hours; 300 concurrent brings it to ~4.6. [[raw/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline#End-to-end: 1 million records through three pipelines|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/durable-execution]], [[wiki/concepts/infrastructure-over-frameworks]]

> Synthesis: The third note in the wiki to walk the same million-document plan, and the only one that explains the *mechanism* underneath it — read this one for the model, the others for the arithmetic.
