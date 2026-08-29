---
type: source
title: RDF vs. Labeled Property Graphs
description: Why property graphs beat RDF triples in practice, and the three extraction modes — structured, semi-structured, unstructured — that decide whether a graph is production-ready.
origin: local
original_path: data_input_examples/notes/03-hard/RDF vs. Labeled Property Graphs.md
source_url: null
authors: []
published_date: null
raw_file: raw/rdf-vs-labeled-property-graphs.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities: []
concepts:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/entity-resolution]]"
---

# RDF vs. Labeled Property Graphs

> [[raw/rdf-vs-labeled-property-graphs|Raw]] · local

## Summary

Two arguments in one note. The first is a modelling comparison: every graph is
(entity, relationship, entity) triplets, and the only real question is where the
metadata goes. **RDF** makes every attribute its own triplet — uniform and easy to
query, but the graph explodes in size, and the deeper cost is that you must know
the whole data model in advance. **Labeled property graphs** hang attributes
directly on nodes and edges: more compact, easier to query, and you can start
today. The note's own comment is the sharpest version: RDF's real con is upfront
effort, which is why modern GraphRAG stacks use property graphs.

The second argument is that modelling is only half the job, and extraction is the
half that decides whether the graph survives. Three modes, with a rule of thumb
attached to each: **structured** (LLM follows your ontology — clean, consistent,
production), **semi-structured** (no LLM at all: document→chunk relationships,
authors, references, links — cheap, reliable, "often overlooked"), and
**unstructured** (the LLM invents its own labels — useful for discovery, dangerous
in production because labels drift, entities duplicate, and the graph becomes
noise).

## Key claims

- The choice between RDF and property graphs is about where metadata lives, not about expressive power. [[raw/rdf-vs-labeled-property-graphs|cite]]
- RDF's biggest cost is not size but the requirement to know the full data model up front. [[raw/rdf-vs-labeled-property-graphs|cite]]
- Semi-structured extraction is free signal: document, chunk, author and reference relationships need no LLM. [[raw/rdf-vs-labeled-property-graphs|cite]]
- Unstructured extraction is for discovery only — in production, labels drift and entities duplicate until the graph is noise. [[raw/rdf-vs-labeled-property-graphs|cite]]
- "Get this wrong… and no amount of retrieval tuning will save you." [[raw/rdf-vs-labeled-property-graphs|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/knowledge-graph]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/entity-resolution]]

> Synthesis: The three-mode taxonomy is the most portable idea in the wiki's graph cluster — it explains why the GraphRAG build adds "structural entries" deterministically instead of asking the model for them.
