---
type: concept
title: Graph extraction
description: Turning text into typed triples — structured (ontology-guided), semi-structured (metadata and lineage, no LLM) and unstructured (free-form, for discovery only).
aliases: [Triple extraction, Structured extraction]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/rdf-vs-labeled-property-graphs]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/entity-resolution]]"
  - "[[wiki/concepts/graphrag-ingestion]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 6
---

# Graph extraction

> Three strategies, one rule: let the LLM extract only what an LLM is needed for, and enforce the ontology on everything it returns.

## Definition

The taxonomy is consistent across sources. **Structured** extraction is
schema-guided: the ontology's node types, property schemas and edge constraints go
into the prompt, and anything violating them is dropped.
**Semi-structured** extraction needs no model at all — document-to-chunk
relationships, authorship, references and links are already in the pipeline's own
metadata; it is called "free signal"
[[wiki/sources/rdf-vs-labeled-property-graphs]]. **Unstructured** extraction lets
the model invent labels, which is useful for exploring a new corpus and dangerous
in production, because "labels drift, entities duplicate, the graph becomes
noise".

The most convincing evidence is one email put through all three side by side,
producing three different graphs [[wiki/sources/graphrag-presentation]].

## Key claims

- The rule of thumb: unstructured for discovery, structured for production, semi-structured for free signal. [[wiki/sources/rdf-vs-labeled-property-graphs]]
- Edge constraints are enforced at extraction: an edge whose endpoints violate its `(source_type → target_type)` pair is dropped with a warning. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Property schemas double as the extraction contract — they are serialized into the prompt so the model fills known fields instead of inventing them. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Limiting the LLM to semantic types improves reliability (structural nodes are deterministic), cuts cost, and keeps structural data consistent with the source. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Unconstrained extraction produced 17 node types and 34 relationship types from five documents, including three casings of one type. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Start with a frontier model guided by the ontology; move to a smaller fine-tuned model when scaling. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- Combining structured and semi-structured is the sweet spot: the ontology gives precision, metadata gives lineage. [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]

## Relationships

- **[[wiki/concepts/knowledge-graph]]**: extraction is how the graph gets built; the ontology is what it is built against.
- **[[wiki/concepts/entity-resolution]]**: the cleanup pass over what extraction returns.

> Synthesis: Every source agrees the expensive mistake is asking the LLM for things you already know — which makes "what does the pipeline already have?" the first question of any extraction design.
