# Ingesting 1,000,000 Documents Is an Orchestration Problem

**Source:** [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:share:7477286521130315776/)
**Published:** 2026-07-04
**Engagement:** 136,494 impressions · 1,629 reactions · 143 comments · 217 reposts · 1.46% engagement rate

![[assets/ingesting-1m-documents-orchestration.jpg]]

---

I used to think ingesting 1,000,000 documents into an AI memory system was mostly a compute problem. But I've been proven wrong...

This is an orchestration problem.

Throwing more GPUs at the pipeline won't help much if your architecture still processes everything sequentially.

The system I've been designing separates ingestion into two independent work pools.

The first turns raw data into documents.
The second turns those documents into memory.

Here's the high-level architecture:

## 1/ Two levels of parallelism

Imagine ingesting 1,000,000 documents.

A Prefect workflow shards them into 1,000-document jobs.

Each worker then processes those jobs in batches of 100.

That gives you two levels of parallelism:

1. Pipeline parallelism → distribute shards across workers.
2. Task parallelism → batch expensive operations inside each worker.

Need more throughput for LLMs or embeddings?

Swap in a Dask or Ray cluster without changing the architecture.

## 2/ Data work pool

The pipeline starts with:

- Web URLs
- RSS feeds

A Prefect workflow flattens every source into URLs, shards them into jobs, and pushes them into a queue.

Workers continuously pull jobs as capacity becomes available, making it easy to absorb traffic spikes by simply adding more workers.

Each worker:

- Flattens URLs
- Scrapes 100 URLs concurrently
- Transforms content
- Batch-loads documents into storage

This stage is mostly network and database I/O.

Batching matters far more than compute.

## 3/ Memory work pool

Once documents reach the warehouse, a second Prefect workflow repeats the pattern.

Each worker runs:

- Chunking
- Batched LLM extraction
- Entity normalization
- Batched embeddings
- Batch-loads Knowledge graph objects into storage

For example, 1,000 documents might become 10,000 chunks, processed in batches of 100.

Every stage has different bottlenecks.

- LLM extraction → vLLM
- Entity normalization → database I/O
- Embeddings → often CPU

Treating them all the same leaves performance on the table.

Here's the gist:

Scaling AI memory isn't about adding GPUs.

It's about designing an architecture where every bottleneck scales independently.

This is why I chose Prefect.

It orchestrates both pipelines with sharding, queues, retries, scheduling, and durable execution, making it practical to scale from thousands to millions of documents.

P.S. What would stop your pipeline from ingesting one million documents today?
