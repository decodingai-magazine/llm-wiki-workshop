---
type: source
title: Ingesting 1,000,000 Documents Is an Orchestration Problem
description: Scaling ingestion is architecture, not GPUs — two independent work pools, two levels of parallelism, and per-stage bottlenecks that must scale separately.
origin: local
original_path: data_input_examples/notes/03-hard/Ingesting 1,000,000 Documents Is an Orchestration Problem.md
source_url: null
authors: []
published_date: null
raw_file: raw/ingesting-1-000-000-documents-is-an-orchestration-problem.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/embeddings]]"
---

# Ingesting 1,000,000 Documents Is an Orchestration Problem

> [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem|Raw]] · local

## Summary

A published post that opens by retracting a belief: ingesting a million documents
looked like a compute problem and turned out to be an orchestration problem —
"throwing more GPUs at the pipeline won't help much if your architecture still
processes everything sequentially."

The design splits ingestion into **two independent work pools**. The *data* pool
turns raw sources (web URLs, RSS feeds) into documents: a Prefect workflow
flattens every source into URLs, shards them into jobs, and pushes them onto a
queue that workers pull from as capacity frees up; each worker scrapes 100 URLs
concurrently and batch-loads the results. This stage is network and database I/O,
so **batching matters more than compute**. The *memory* pool then turns documents
into knowledge-graph objects — chunking, batched LLM extraction, entity
normalization, batched embeddings, batch load.

The parallelism is deliberately two-level: **pipeline parallelism** distributes
shards across workers, **task parallelism** batches expensive operations inside
each worker (1,000 documents → 10,000 chunks → batches of 100). The payoff is that
each stage's distinct bottleneck — vLLM for extraction, database I/O for
normalization, CPU for embeddings — can be scaled on its own, and a Dask or Ray
cluster can be swapped in without changing the architecture.

## Key claims

- Ingestion at scale is bounded by orchestration, not by GPU count. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem|cite]]
- Two work pools — raw→documents and documents→memory — scale independently because their bottlenecks differ. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem#1/ Two levels of parallelism|cite]]
- Queue-and-pull lets you absorb spikes by adding workers, with no re-sharding. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem#2/ Data work pool|cite]]
- In the data pool, batching beats compute: the stage is network and database I/O. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem#2/ Data work pool|cite]]
- Treating every stage the same "leaves performance on the table" — extraction, normalization and embedding each bottleneck elsewhere. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem#3/ Memory work pool|cite]]
- Prefect was chosen for sharding, queues, retries, scheduling and durable execution together. [[raw/ingesting-1-000-000-documents-is-an-orchestration-problem#3/ Memory work pool|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/durable-execution]], [[wiki/concepts/embeddings]]

> Synthesis: The clearest statement of the wiki's scaling thesis, and the one that generalizes past GraphRAG: independent bottlenecks demand independently scalable stages, which is an argument for a workflow engine rather than a bigger machine.
