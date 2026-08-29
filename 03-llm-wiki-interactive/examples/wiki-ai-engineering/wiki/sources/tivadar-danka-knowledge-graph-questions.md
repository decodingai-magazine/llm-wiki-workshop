---
type: source
title: Tivadar Danka Knowledge Graph Questions
description: Someone else's minimal knowledge graph — 810 ML algorithms in a JSON file, recursively expanded by an LLM, categorized, unnormalized, rendered with Three.js.
origin: local
original_path: data_input_examples/notes/03-hard/Tivadar Danka Knowledge Graph Questions.md
source_url: null
authors: []
published_date: null
raw_file: raw/tivadar-danka-knowledge-graph-questions.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities: []
concepts:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/graph-visualization]]"
---

# Tivadar Danka Knowledge Graph Questions

> [[raw/tivadar-danka-knowledge-graph-questions|Raw]] · local

## Summary

A reply from another practitioner describing his own knowledge graph, and it is
valuable precisely because it is the minimal version of everything the rest of the
wiki builds carefully. The graph is a JSON file. Each node has an id, a label,
`to` and `from` arrays, a category, a short definition and a long description with
LaTeX in it. It was seeded with roughly 810 machine-learning algorithms and grown
recursively — an LLM wrote each definition, and new nodes came from the concepts
it mentioned. Entities are clustered by category, the whole thing is rendered with
Three.js, and — stated plainly — no normalization was done.

## Key claims

- The entire store is a JSON file with adjacency arrays on each node; no database. [[raw/tivadar-danka-knowledge-graph-questions|cite]]
- The graph was grown recursively: generate a definition, extract the concepts it mentions, make those the next nodes. [[raw/tivadar-danka-knowledge-graph-questions|cite]]
- Clustering is by a hand-assigned `category` field. [[raw/tivadar-danka-knowledge-graph-questions|cite]]
- "I did not do any normalization." [[raw/tivadar-danka-knowledge-graph-questions|cite]]
- Rendering is Three.js over the same JSON. [[raw/tivadar-danka-knowledge-graph-questions|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/knowledge-graph]], [[wiki/concepts/entity-resolution]], [[wiki/concepts/graph-visualization]]

> Synthesis: The useful counterexample in the wiki — a working graph built with none of the machinery the other notes argue for, which makes "I did not do any normalization" the sharpest available question about when entity resolution is actually load-bearing.
