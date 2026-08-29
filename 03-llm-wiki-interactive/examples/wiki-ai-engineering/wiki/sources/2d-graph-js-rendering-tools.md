---
type: source
title: "2D knowledge graph libraries: an executive summary"
description: Five JavaScript graph-rendering libraries compared on scale, execution model and looks, with Sigma.js the pragmatic pick and Cosmograph the only one that survives 100k+ nodes.
origin: local
original_path: data_input_examples/notes/03-hard/2d_graph_js_rendering_tools.md
source_url: null
authors: []
published_date: null
raw_file: raw/2d-graph-js-rendering-tools.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities: []
concepts:
  - "[[wiki/concepts/graph-visualization]]"
---

# 2D knowledge graph libraries: an executive summary

> [[raw/2d-graph-js-rendering-tools|Raw]] · local

## Summary

A comparison table with opinions attached, across three axes: practical scale, how
the library actually runs, and how good the result looks without effort.

**Sigma.js + graphology** separates concerns — graphology holds the data and runs
algorithms (Louvain, centrality, ForceAtlas2), Sigma renders through WebGL — and
is named the best beauty-for-effort at tens of thousands of nodes. **D3.js** is
the lowest level: `d3-force` ticks a simulation and you write every pixel of
rendering and interaction; the highest ceiling and the most labour, with SVG
falling over after a few thousand nodes and Canvas reaching ~10k. **Cosmograph**
runs both the force simulation and the rendering on the GPU, which is why it is
the only option listed for 100k–1M+ nodes, with near-zero main-thread cost and
less per-element control. **Cytoscape.js** is the batteries-included graph-theory
framework, Canvas-rendered, functional-looking by default. **vis-network** is the
easiest and the most limited, comfortable to a few thousand nodes.

The bottom line is a decision list rather than a winner: Sigma.js for a beautiful
interactive graph, Cosmograph past 100k nodes, Cytoscape for analysis-heavy work,
D3 when the visuals are the product, vis-network for a quick small graph.

## Key claims

- Sigma.js + graphology + ForceAtlas2 is the sweet spot of scale, performance and looks. [[raw/2d-graph-js-rendering-tools#Bottom line|cite]]
- Only Cosmograph, with GPU-side simulation *and* rendering, handles hundreds of thousands to millions of nodes. [[raw/2d-graph-js-rendering-tools#On scale|cite]]
- D3 scales as well as you engineer it — SVG breaks after a few thousand nodes, Canvas reaches 10k+. [[raw/2d-graph-js-rendering-tools#On scale|cite]]
- Cytoscape.js trades some render speed for a deep graph-theory algorithm library. [[raw/2d-graph-js-rendering-tools#On how it runs|cite]]
- Beauty tracks effort everywhere except Sigma, which looks good by default. [[raw/2d-graph-js-rendering-tools#On beauty|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/graph-visualization]]

> Synthesis: A tooling survey with a short shelf life, kept useful by its axes — scale, execution model, default aesthetics — which outlive any of the five libraries it ranks.
