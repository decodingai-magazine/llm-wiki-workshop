---
type: concept
title: Graph communities
description: Clusters of densely connected nodes, summarized by an LLM and stored beside them — the layer that makes top-down, overview-shaped retrieval possible.
aliases: [Community detection, Louvain, Leiden]
sources:
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/hybrid-search]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 2
---

# Graph communities

> Cluster the graph, summarize each cluster, store the summaries as queryable documents — and you can answer "what do I know about X" without walking every node.

## Definition

Community detection runs as a periodic batch process (Louvain or Leiden) over the
materialized graph, clustering densely connected nodes; an LLM summarizes each
community and the summaries are written back into the same collection as
queryable documents
[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]].

They enable the **top-down** retrieval shape: find entry points as usual, then
retrieve *communities* rather than entities, hop between them through bridge
nodes, and answer from their summaries — an overview instead of detail
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]].

## Key claims

- Communities are computed in batch, not at query time, and stored alongside the nodes they summarize. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]
- Top-down retrieval answers breadth questions; bottom-up answers depth questions — both start from the same hybrid-search entry points. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Isolated nodes and single-node communities are a normal clustering outcome, not a failure to handle. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Communities can also annotate a bottom-up result, telling the reader which clusters the retrieved entities belong to. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]

## Relationships

- **[[wiki/concepts/knowledge-graph]]**: communities are a derived layer over the same graph.
- **[[wiki/concepts/hybrid-search]]**: both retrieval shapes start from fused seeds.

> Synthesis: The least implemented idea in the wiki's retrieval cluster — described in both architecture sources, absent from every build account, which is worth remembering before treating it as shipped.
