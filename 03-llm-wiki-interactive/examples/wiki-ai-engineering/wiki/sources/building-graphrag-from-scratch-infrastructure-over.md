---
type: source
title: "Building GraphRAG from scratch: infrastructure over frameworks"
description: A two-day from-scratch GraphRAG build, and the argument behind it — infrastructure tools solve the hard problems, AI frameworks abstract the easy ones and fight your data model.
origin: local
original_path: data_input_examples/notes/03-hard/building-graphrag-from-scratch-infrastructure-over-frameworks.md
source_url: null
authors: []
published_date: null
raw_file: raw/building-graphrag-from-scratch-infrastructure-over.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/langchain]]"
concepts:
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/durable-execution]]"
---

# Building GraphRAG from scratch: infrastructure over frameworks

> [[raw/building-graphrag-from-scratch-infrastructure-over|Raw]] · local

## Summary

The build report behind the wiki's most opinionated claim: a complete GraphRAG
system in two days with no AI framework — MongoDB, Prefect, Python.

It opens with the detour. LangChain's `MongoDBGraphStore` gave a working graph in
ten minutes, and then every customization was a fight. A free-form extractor
produced 17 node types and 34 relationship types from five documents, including
`part_of`, `Part Of` and `part of` as three separate types. There is no
observation log and no provenance. `$graphLookup` needs edges as separate
documents, but relationships are embedded arrays. A `mongosh` scan found 30+
entities with duplicate relationships and no index that could help. The diagnosis
is the sentence worth keeping: **"You can't configure your way out of a data model
mismatch."**

The rest is an inventory — ontology as StrEnums with edge constraints, chunking
with tiktoken, parallel extraction, deterministic structural entries, fuzzy
normalization, an immutable log, a materialization pipeline built from `$group`,
`$mergeObjects`, `$unionWith` and `$out`, composite IDs, reverse edges,
post-materialization embeddings (244 log entries → 70 nodes, ~3.5x fewer
embeddings), RRF fusion, `$graphLookup` expansion, pyvis visualization, and
Prefect deployments.

The dividing line is stated as a table and then as a principle: infrastructure
does what is hard to build (durable execution, aggregation, vector search, graph
traversal); business logic — ontology, extraction, normalization, materialization,
fusion — is custom Python because it is domain-specific and changes with your
requirements. "Infrastructure tools support your code. AI frameworks replace it."

## Key claims

- LangChain's assumptions are architectural, not configurable: embedded relationships, no ontology enforcement, no log/materialization split. [[raw/building-graphrag-from-scratch-infrastructure-over#The LangChain detour|cite]]
- Free-form extraction produced three spellings of the same relationship type from five documents. [[raw/building-graphrag-from-scratch-infrastructure-over#The LangChain detour|cite]]
- MongoDB replaces three systems — document store, vector store, graph database — plus the glue between them. [[raw/building-graphrag-from-scratch-infrastructure-over#MongoDB as the unified memory|cite]]
- Prefect tasks are thin wrappers around pure functions, so the business logic is testable without a Prefect server. [[raw/building-graphrag-from-scratch-infrastructure-over#Prefect as a thin orchestrator|cite]]
- The LLM layer is a two-method abstract class over the vendor SDK — no chains, prompt templates or output parsers. [[raw/building-graphrag-from-scratch-infrastructure-over#No LangChain, no problem|cite]]
- Embedding after materialization instead of before cut the work ~3.5x (244 log entries → 70 nodes). [[raw/building-graphrag-from-scratch-infrastructure-over#What I built in 2 days|cite]]
- The hard parts are infrastructure (durable execution, aggregation, search); the easy parts — ontology, prompt, normalization, fusion — are the ones frameworks abstract. [[raw/building-graphrag-from-scratch-infrastructure-over#The lesson|cite]]

## Notable quotes

> "Infrastructure tools support your code. AI frameworks replace it. Choose accordingly."
> — [[raw/building-graphrag-from-scratch-infrastructure-over#The lesson|location]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/prefect]], [[wiki/entities/langchain]]
- **Concepts**: [[wiki/concepts/infrastructure-over-frameworks]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/unified-memory]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/durable-execution]]

> Synthesis: The strongest evidence in the wiki for its own architecture, and also the most self-selecting — a two-day build by the person who designed the system says as much about clarity of intent as about the tools.
