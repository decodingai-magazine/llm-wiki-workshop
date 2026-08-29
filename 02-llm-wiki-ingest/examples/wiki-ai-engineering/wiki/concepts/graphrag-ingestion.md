---
type: concept
title: GraphRAG ingestion pipeline
description: The write path from raw sources to queryable memory — collect, clean, chunk, extract, resolve, embed, store — and the three steps in it that cost real money.
aliases: [Memory pipeline, Ingestion pipeline]
sources:
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/four-prefect-task-runners-four-different-problems]]"
  - "[[wiki/sources/how-to-ingest-1-000-000-documents-into-your-agent-memory]]"
  - "[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/running-multiple-graphrag-ingestion-pipelines-in-parallel]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]"
  - "[[wiki/sources/what-to-focus-on]]"
related:
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/knowledge-graph]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 10
---

# GraphRAG ingestion pipeline

> Two pipelines, not one: raw sources become documents, then documents become memory. They fail differently, cost differently, and scale differently.

## Definition

The shape is consistent across every source that describes it. A **data pipeline**
normalizes anything — RSS, articles, arXiv, local files, conversations — into
documents in a warehouse, deduplicated by a unique source URI. A **memory
pipeline** then turns documents into graph objects: clean, chunk (512 tokens with
64 overlap), extract triples per chunk against the ontology, add structural
entries deterministically, resolve entities, embed, and write
[[wiki/sources/agentic-graphrag-via-mcp-servers]].

The split is not cosmetic. The first stage is network and database I/O where
batching beats compute; the second is LLM, database and GPU work with entirely
different bottlenecks
[[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]].

## Key claims

- Three steps carry nearly all the cost: graph extraction, entity resolution and embedding. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Ingestion at scale is an orchestration problem, not a compute problem — sequential architecture is not fixed by more GPUs. [[wiki/sources/ingesting-1-000-000-documents-is-an-orchestration-problem]]
- Chunking is optional and worth avoiding when the data allows it; embedding a document summary sidesteps it entirely. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]], [[wiki/sources/walkthrough-throw-the-ingestion-and-retrieval-logic]]
- Deduplicate by source URI at the front door, and create placeholder documents for references not yet ingested so links survive. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The same code must serve both batch runs and live tool calls — the difference is only who triggered it. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- When a tool call triggers ingestion, it runs inline: the user is waiting, and a queued job would leave the content unqueryable. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Every stage's output should be checkpointed, because a failure at embedding must not re-run extraction. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]

## Relationships

- **[[wiki/concepts/graph-extraction]]** and **[[wiki/concepts/entity-resolution]]**: the two expensive middle stages.
- **[[wiki/concepts/pipeline-parallelism]]**: how the stages are made to go fast.
- **[[wiki/concepts/durable-execution]]**: how they are made to survive.

> Synthesis: The pipeline is described a dozen times in this wiki with almost no variation, which is itself the finding — the shape is settled, and every remaining argument is about orchestration and storage rather than about the steps.
