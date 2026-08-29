---
type: source
title: Scaling GraphRAG Ingestion Pipelines with Prefect
description: A ghostwriter brief pricing the three expensive ingestion steps — extraction, resolution, embedding — and showing how checkpointing plus a worker-queue pattern stops you paying twice.
origin: local
original_path: data_input_examples/notes/03-hard/Scaling_GraphRAG_Ingestion_Pipelines_with_Prefect.md
source_url: null
authors: []
published_date: null
raw_file: raw/scaling-graphrag-ingestion-pipelines-with-prefect.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/graphrag-ingestion]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/pipeline-parallelism]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/inference-economics]]"
---

# Scaling GraphRAG Ingestion Pipelines with Prefect

> [[raw/scaling-graphrag-ingestion-pipelines-with-prefect|Raw]] · local

## Summary

The orchestration counterpart to the MongoDB ingestion brief: same twelve-step
architecture, scoped to steps 1–8, and organized around three expensive
operations — **graph extraction** (an LLM call per chunk), **entity resolution**
(LLM plus database lookups, and the most failure-prone step), and **embedding**
(API or GPU per node).

The hook is arithmetic. Ingesting 10,000 documents with a 5% failure rate, where
each retry re-runs ~$0.03 of already-successful extraction and resolution, wastes
$15 per batch — $465 a month, $5,580 a year — purely re-executing work that
already succeeded. With per-step result caching the same failures cost ~$15 a
month. The framing is worth keeping: **"The fix is not 'write better error
handling.'"** It is a checkpoint after each expensive step.

Each step then gets a treatment: cache keys derived from chunk content plus model
plus ontology version so identical chunks always hit cache; fast retries for
database timeouts and exponential backoff for rate-limited LLM calls; concurrency
limits set to the provider's rate limit so 429s are prevented rather than handled;
serialized resolution per entity to avoid two workers racing on the same "Arthur";
idempotency keys on writes so a network blip after an acknowledged write does not
double-append to the log.

The worker-queue section is the scaling half: a work pool defines *where* code
runs, work queues carry priority and concurrency limits per stage
(extraction 50, resolution 20, embedding 100), workers drain them, and a queue
doubles as the pressure valve when someone bulk-imports five years of email.

The trade-offs are stated plainly, including the one that matters most: "Prefect
doesn't make your pipeline smarter — it makes it survivable."

## Key claims

- The three expensive steps are extraction, entity resolution and embedding; everything else is cheap by comparison. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#Architecture Context|cite]]
- Without checkpointing, a 5% failure rate on 10,000 documents wastes ~$465/month re-running successful work. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#The Cost of Fragility (Hook Section)|cite]]
- The cache key must include the model and ontology version, not just the input text — otherwise a model change silently reuses stale extractions. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#Step 4 — Graph Extraction (LLM Call — Expensive)|cite]]
- Set queue concurrency to match the provider's rate limit: prevent 429s at the source instead of retrying them. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#Step 4 — Graph Extraction (LLM Call — Expensive)|cite]]
- Entity resolution needs *serialization per entity* — two workers resolving "Arthur" concurrently is a race condition. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#Step 5 — Entity Resolution (LLM + DB — Expensive)|cite]]
- Writes need idempotency keys: an acknowledged write plus a lost response equals a duplicate event without them. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#Step 8 — Store as Immutable Logs|cite]]
- Different stages belong on different infrastructure — extraction on CPU workers, embedding on a GPU pool — which work pools express directly. [[raw/scaling-graphrag-ingestion-pipelines-with-prefect#The Worker-Queue Pattern for Horizontal Scaling — Dedicate a Section to This|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/graphrag-ingestion]], [[wiki/concepts/durable-execution]], [[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/embeddings]], [[wiki/concepts/append-only-log]], [[wiki/concepts/inference-economics]]

> Synthesis: A sponsored brief that pairs with the MongoDB one — same diagram, opposite half — and the pairing is the useful part: the storage argument and the orchestration argument are about the same twelve steps seen from either end.
