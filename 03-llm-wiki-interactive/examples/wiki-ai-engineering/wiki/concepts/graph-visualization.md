---
type: concept
title: Graph visualization
description: Rendering the memory so a human can see it — in a notebook, a browser, or increasingly inside the chat itself.
aliases: [Graph rendering, Force-directed graph]
sources:
  - "[[wiki/sources/2d-graph-js-rendering-tools]]"
  - "[[wiki/sources/queries-to-trigger-the-ui]]"
  - "[[wiki/sources/tivadar-danka-knowledge-graph-questions]]"
  - "[[wiki/sources/you-don-t-need-a-browser-anymore]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/mcp-apps]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 4
---

# Graph visualization

> A knowledge graph you cannot see is hard to trust. Visualization is how you find out what the extraction pipeline actually built.

## Definition

Two contexts in this wiki. **Offline**: rendering libraries chosen by scale and
effort — a WebGL renderer with a separate algorithm layer for tens of thousands of
nodes, GPU-side simulation for hundreds of thousands, a low-level toolkit when the
visuals are the product [[wiki/sources/2d-graph-js-rendering-tools]]. **In the
conversation**: an interactive graph explorer returned as the result of a tool
call and rendered inside the chat, with hover, drag, zoom and search
[[wiki/sources/you-don-t-need-a-browser-anymore]].

## Key claims

- Practical scale differs by two orders of magnitude across libraries — tens of thousands versus hundreds of thousands of nodes. [[wiki/sources/2d-graph-js-rendering-tools]]
- GPU-side force simulation *and* rendering is what makes very large graphs interactive at all. [[wiki/sources/2d-graph-js-rendering-tools]]
- Prose fails for structured answers in three ways at once, one of which is flooding the model's own context. [[wiki/sources/you-don-t-need-a-browser-anymore]]
- Visualization tools are exposed to the agent like any other tool — "visualize my entire memory knowledge graph" is a prompt, not a menu item. [[wiki/sources/queries-to-trigger-the-ui]]
- One shared data layer can feed two views — a topology graph and a summary dashboard. [[wiki/sources/you-don-t-need-a-browser-anymore]]

## Relationships

- **[[wiki/concepts/mcp-apps]]**: the mechanism that moves visualization from a separate web app into the conversation.
- **[[wiki/concepts/knowledge-graph]]**: what is being rendered, and the reason it needs rendering at all.

> Synthesis: Visualization shows up here as a debugging tool as much as a feature — the fastest way to find out that your ontology produced 34 relationship types is to look at the graph.
