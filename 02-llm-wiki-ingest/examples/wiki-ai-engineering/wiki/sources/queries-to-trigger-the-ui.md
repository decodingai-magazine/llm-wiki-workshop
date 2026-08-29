---
type: source
title: Queries to Trigger the UI
description: Four example prompts that trigger memory-visualization tools — whole-graph, scoped subgraph, an interactive dashboard, and a generated one.
origin: local
original_path: data_input_examples/notes/03-hard/Queries to Trigger the UI.md
source_url: null
authors: []
published_date: null
raw_file: raw/queries-to-trigger-the-ui.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities: []
concepts:
  - "[[wiki/concepts/mcp-apps]]"
  - "[[wiki/concepts/graph-visualization]]"
---

# Queries to Trigger the UI

> [[raw/queries-to-trigger-the-ui|Raw]] · local

## Summary

A test script, in the literal sense: four natural-language prompts and the tool
each is meant to trigger. Visualize the whole memory graph
(`visualize_memory_graph`, broad); show just the piece around a given entity
(the same tool, scoped); open an interactive dashboard (`memory_dashboard`); and
dynamically generate a dashboard with pie charts of node and relationship types
(`generate_prefab_ui`).

## Key claims

- The memory server exposes UI tools, not just search and write tools. [[raw/queries-to-trigger-the-ui|cite]]
- Visualization comes in two scopes from one tool — the entire graph, or a subgraph around a named entity. [[raw/queries-to-trigger-the-ui|cite]]
- One of the tools generates the interface on demand rather than serving a fixed dashboard. [[raw/queries-to-trigger-the-ui|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/mcp-apps]], [[wiki/concepts/graph-visualization]]

## Notable quotes

> "Dynamically generate a dashboard of my memory, showing a pie chart of all my node types, and another pie chart with all my relationship types."
> — [[raw/queries-to-trigger-the-ui|location]]

> Synthesis: The most concrete evidence in the wiki that server-shipped UI is being used in practice rather than admired in a roadmap — four prompts someone actually types.
