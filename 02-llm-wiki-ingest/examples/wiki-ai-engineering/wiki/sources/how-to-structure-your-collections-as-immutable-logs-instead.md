---
type: source
title: Structuring collections as immutable logs instead of one-shot collections
description: Why the ontology is the most important step in GraphRAG, and how append-only observation logs plus a materialized view fix the deduplication and provenance that embedded arrays make impossible.
origin: local
original_path: data_input_examples/notes/03-hard/How to structure your collections as immutable logs instead of a one time collections.md
source_url: null
authors: []
published_date: null
raw_file: raw/how-to-structure-your-collections-as-immutable-logs-instead.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/langchain]]"
concepts:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/knowledge-freshness]]"
---

# Structuring collections as immutable logs instead of one-shot collections

> [[raw/how-to-structure-your-collections-as-immutable-logs-instead|Raw]] · local

## Summary

The wiki's most detailed data-modelling note, and the one that states the thesis
outright: **the ontology is the most important step in GraphRAG** — not the
retrieval code, not the embedding model, not the graph database. Without it, "LLM
extraction is unconstrained text generation that happens to output JSON."

The evidence is the same framework experiment reported elsewhere, with the numbers
in full: 5 documents produced 17 node types and 34 relationship types, including
three casings of the same one, and 30+ entities carrying duplicate relationships —
one with 13. The diagnosis is the data model, not the tool: relationships embedded
as arrays inside entity documents mean deduplication requires scanning every
`(target, type)` pair in every document, updating one relationship means writing
the parent entity, and there is no provenance back to a source chunk.

The replacement is a small, enforced ontology (6 node types, 8 edge types), each
node type with a Pydantic property schema that doubles as the LLM's extraction
contract, and each edge type locked to a `(source_type → target_type)` pair that
is checked at extraction and dropped when violated. Types are split by *who
extracts them*: the LLM handles semantic entities (person, task, episode,
preference); the pipeline deterministically builds the structural ones (document,
chunk, and the `part_of` / `next` / `mentions` / `referenced` edges) from metadata
it already has — cheaper, reproducible, and consistent by construction.

Storage is three collections: raw `documents`, an append-only
`knowledge_graph_log` of observations each carrying its source document and chunk,
and a materialized `knowledge_graph` rebuilt by aggregation. Immutability buys two
specific things — **provenance** (trace any node to the chunk that produced it)
and **replayability** (change the materialization logic and re-aggregate; no
re-extraction, no re-paying the LLM). Composite `"type:name"` IDs came out of a
real `DuplicateKeyError`, when "opik" existed as both a person and a preference.

And one optimization that only this design allows: embeddings are computed **after**
deduplication, once per materialized node, instead of once per observation.

## Key claims

- The ontology is the single most important step in GraphRAG, and it is a contract between the extractor and the query layer. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#The ontology: the most important step in GraphRAG|cite]]
- Keep it small and specific — not "entity"/"relationship", and not fifty types nobody can distinguish. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#Designing the ontology for a personal digital twin|cite]]
- Edge constraints are enforced at extraction time; a violating edge is dropped with a warning rather than stored. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#Edge constraints: directional, enforced|cite]]
- Only extract with an LLM what an LLM is needed for — structural nodes come from metadata, which is cheaper, deterministic and always consistent with the source. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#Two extraction strategies: structured vs semi-structured|cite]]
- The log is append-only for two reasons: provenance to the exact chunk, and replayability of the materialization without re-extraction. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#Three collections, three responsibilities|cite]]
- Composite `"type:name"` IDs came from a `DuplicateKeyError` — the same name existed under two types. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#The materialization pipeline|cite]]
- Embedding after materialization computes one vector per deduplicated entity instead of one per observation. [[raw/how-to-structure-your-collections-as-immutable-logs-instead|cite]]
- Fuzzy normalization must remap edge endpoints to canonical names, or the merge silently orphans edges. [[raw/how-to-structure-your-collections-as-immutable-logs-instead#The extraction pipeline: step by step|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/langchain]]
- **Concepts**: [[wiki/concepts/append-only-log]], [[wiki/concepts/materialized-view]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/embeddings]], [[wiki/concepts/knowledge-freshness]]

> Synthesis: Read together with [[wiki/sources/scaling-mongodb-brain-dump]], this is the wiki's sharpest unresolved tension — the log-plus-view design is what makes correction and replay possible, and it is also what doubles the RAM footprint.
