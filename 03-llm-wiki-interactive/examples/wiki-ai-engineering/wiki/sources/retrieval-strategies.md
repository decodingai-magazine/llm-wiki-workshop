---
type: source
title: "Retrieval strategies for GraphRAG: graph search, deep search, agentic search"
description: The three ways an agent searches its unified memory, the multi-hop traversal that makes it GraphRAG, and the design rule underneath — orchestrate the writes, never the reads.
origin: local
original_path: data_input_examples/notes/03-hard/Retrieval Strategies.md
source_url: null
authors: []
published_date: null
raw_file: raw/retrieval-strategies.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/agentic-search]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/read-write-separation]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/durable-execution]]"
---

# Retrieval strategies for GraphRAG: graph search, deep search, agentic search

> [[raw/retrieval-strategies|Raw]] · local

## Summary

A post guideline whose planning notes are more precise than most published
articles. The premise: "building memory for AI agents is less about storage and
more about retrieval", and the foundation decision is that the whole graph —
nodes, edges *and* vectors — lives in one collection of one database, trading
away a graph-native query language for one system to operate.

Three search paths. **Graph search** is the default: embed the query, run vector
and full-text search in parallel, fuse by Reciprocal Rank Fusion, rerank the fused
candidates to a top 10, then expand 1–3 hops. The ordering is justified — RRF
fuses by rank so the two scorers never need calibration, and the reranker then
only orders a small fused set. If vector search fails, retrieval degrades to
text-only: "a read never hard-fails." **Deep search** is the same algorithm scaled
up (50 seeds, 3 hops) with a different return shape: instead of dumping hundreds
of nodes into the conversation it writes full results to files behind a
lightweight index — "a light LLM wiki on demand" that becomes the agent's
localized memory. **Agentic search** hands the query itself to the LLM for
questions the fixed paths cannot express, with the ontology compiled into the
prompt so it targets a schema it understands, and a guard rail stack — operation
allow-list, forced user scoping, hard result cap, embeddings stripped, errors fed
back for self-correction.

Then the definition worth quoting: GraphRAG "is really just one extra step:
multi-hop traversal during retrieval". Similarity finds the entry point; the graph
finds everything connected to it, in both edge directions, including entities that
resemble the query not at all.

The last two beats are operational. The memory is served as an MCP server — the
agent never touches the database, and write tools return in milliseconds by
submitting a pipeline run. And the rule the whole design rests on: **orchestrate
the writes, never the reads.**

## Key claims

- One collection holding nodes, edges and vectors trades a graph-native query language for a single system to operate — a trade the note would make "every time" at personal scale. [[raw/retrieval-strategies#LinkedIn Post|cite]]
- RRF before reranking is deliberate: fusing by rank avoids calibrating two scorers, and the reranker then only orders a small candidate set. [[raw/retrieval-strategies#Content|cite]]
- Retrieval degrades gracefully — if vector search fails it falls back to text-only rather than erroring. [[raw/retrieval-strategies#Content|cite]]
- Deep search returns an index over files instead of a wall of nodes, giving the agent progressive disclosure over a large neighbourhood. [[raw/retrieval-strategies#Content|cite]]
- Agentic search is safe only because of its guard rails: allow-listed operations, server-injected user scoping, a forced limit, and a self-correction retry. [[raw/retrieval-strategies#Content|cite]]
- "GraphRAG, different from normal RAG, is really just one extra step: multi-hop traversal during retrieval." [[raw/retrieval-strategies#Content|cite]]
- "Orchestrate the writes, never the reads — the only thing they should share is a rate limit." [[raw/retrieval-strategies#Content|cite]]
- The write tools never block a session: they submit a pipeline run and return immediately — "the MCP server is the front desk. The heavy lifting happens in the back office." [[raw/retrieval-strategies#Content|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/hybrid-search]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/agentic-search]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/read-write-separation]], [[wiki/concepts/unified-memory]], [[wiki/concepts/durable-execution]]

> Synthesis: This is the retrieval half of the wiki's architecture stated as design rules rather than as code, and it is candid about the gap between the two — the reranking step it describes is on the roadmap, not in the codebase.
