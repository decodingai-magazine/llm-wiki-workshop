---
type: source
title: GraphRAG presentation — Context Engineering with GraphRAG, building your digital twin
description: A 17-slide deck with worked examples — three extraction strategies on one email, bottom-up vs top-down retrieval, and the cat-vet query that stitches four silos.
origin: local
original_path: data_input_examples/notes/03-hard/GraphRAG Presentation.md
source_url: null
authors: []
published_date: null
raw_file: raw/graphrag-presentation.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/context-rot]]"
  - "[[wiki/concepts/data-fragmentation]]"
  - "[[wiki/concepts/graph-communities]]"
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/unified-memory]]"
---

# GraphRAG presentation — Context Engineering with GraphRAG, building your digital twin

> [[raw/graphrag-presentation|Raw]] · local

## Summary

The slide deck behind the lecture: seventeen slides, each with its text and an
image-generation prompt, arranged as an argument from problem to payoff. Slides
2–4 set up context rot and data fragmentation and introduce the digital twin;
5–6 cover extraction strategies and property graphs; 7–10 walk the pipeline
(ingest, store immutably, query the latest, reverse mistakes); 11–13 cover
retrieval and agent access; 14–16 are worked end-to-end examples.

Two things here are sharper than anywhere else in the wiki. The first is **one
email put through all three extraction strategies side by side** — structured
extraction constrained to the ontology, semi-structured extraction from the
email's own links and thread order (no LLM), and unstructured extraction where the
model invents `Topic` nodes and a `WANTS_TO_MEET` edge. Seeing the same input
produce three different graphs is the clearest argument for constraining
extraction that the wiki contains.

The second is the **cat-vet query**, used to claim five things traditional RAG
cannot do: bridging silos (SMS, Drive, email and Notion stitched by
`CONNECTED_TO` edges that no single chunk spans); graph-only discoveries (an
episode — a bad reaction at a specific vet — and a task, reachable only through
edges, invisible to embedding similarity); full traceability from claim to node to
`source_uri`; a minimum viable context instead of context stuffing; and living
memory with time travel, where a preference changes from Java to Python and a bad
extraction can be invalidated.

**Content warning about this file.** Roughly two-thirds of it is not new material.
Each of the seventeen slides carries a ~450-word image-generation prompt that is
identical apart from its last two sentences, and the second half of the file
contains **verbatim copies** of the two ghostwriter guides already in this wiki.
The signal is in the slide text and the worked examples.

## Key claims

- The same email yields three different graphs under structured, semi-structured and unstructured extraction — the strategy, not the model, decides what the graph becomes. [[raw/graphrag-presentation#5. Choose Your Extraction Strategy Based on Your Data|cite]]
- Use structured or semi-structured for GraphRAG proper, semi-structured for lineage, unstructured only to explore. [[raw/graphrag-presentation#5. Choose Your Extraction Strategy Based on Your Data|cite]]
- Tasks, episodes and preferences carry their own `content_embedding`, so semantic search can land on them directly rather than through a document. [[raw/graphrag-presentation#4. Structure Your Domain with Knowledge Graphs & Ontologies|cite]]
- The cat-vet answer stitches four silos through edges no single vector chunk spans. [[raw/graphrag-presentation#16. Why GraphRAG: 5 Things Traditional RAG Can't Do|cite]]
- Two of the facts in that answer were reachable only through graph edges, not by any embedding similarity. [[raw/graphrag-presentation#16. Why GraphRAG: 5 Things Traditional RAG Can't Do|cite]]
- Every claim traces to a node, an edge and a `source_uri` — traceability is a property of the data model, not of the prompt. [[raw/graphrag-presentation#16. Why GraphRAG: 5 Things Traditional RAG Can't Do|cite]]
- "Minimum viable context" is the goal: deliver the relevant subgraph rather than fill the window. [[raw/graphrag-presentation#16. Why GraphRAG: 5 Things Traditional RAG Can't Do|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/knowledge-graph]], [[wiki/concepts/graph-extraction]], [[wiki/concepts/context-rot]], [[wiki/concepts/data-fragmentation]], [[wiki/concepts/graph-communities]], [[wiki/concepts/append-only-log]], [[wiki/concepts/hybrid-search]], [[wiki/concepts/unified-memory]]

> Synthesis: The largest file in the wiki and one of the least independent — it is the deck for [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]] and it re-contains [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]] and [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]] verbatim, so treat all four as **one** voice when counting agreement. Its unique contribution is the two worked examples.
