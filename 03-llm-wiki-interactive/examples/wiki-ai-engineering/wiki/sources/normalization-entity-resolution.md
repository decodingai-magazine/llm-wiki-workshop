---
type: source
title: Normalization / Entity Resolution
description: A one-line plan for a deep dive into entity resolution during knowledge-graph extraction, made durable with Prefect, referencing Neo4j's resolution guide.
origin: local
original_path: data_input_examples/notes/03-hard/Normalization - Entity Resolution.md
source_url: null
authors: []
published_date: null
raw_file: raw/normalization-entity-resolution.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/knowledge-graph]]"
---

# Normalization / Entity Resolution

> [[raw/normalization-entity-resolution|Raw]] · local

## Summary

A one-bullet plan for a post: a deep dive into entity resolution and
normalization during knowledge-graph extraction, using Prefect for durability,
anchored to Neo4j's resolution-and-deduplication guide. A screenshot is attached;
the argument is not written down yet.

## Key claims

- Entity resolution is treated as a step of knowledge-graph extraction, not as a separate cleanup pass. [[raw/normalization-entity-resolution|cite]]
- Durability during resolution is a Prefect concern. [[raw/normalization-entity-resolution|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/entity-resolution]], [[wiki/concepts/knowledge-graph]]

> Synthesis: A stub with a good title — the actual mechanics of resolution appear in the pipeline notes, and this page mostly records that the author considers it worth its own deep dive.
