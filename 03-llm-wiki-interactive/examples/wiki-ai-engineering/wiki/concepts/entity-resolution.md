---
type: concept
title: Entity resolution
description: Deciding that "Art", "Arthur" and "Arthur Iusztin" are one node — the step that determines whether a knowledge graph accumulates knowledge or duplicates.
aliases: [Normalization, Deduplication, Fuzzy matching]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
  - "[[wiki/sources/normalization-entity-resolution]]"
  - "[[wiki/sources/rdf-vs-labeled-property-graphs]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/tivadar-danka-knowledge-graph-questions]]"
related:
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
  - "[[wiki/concepts/materialized-view]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 8
---

# Entity resolution

> The same person appears in fifty documents under six spellings. Resolution is what makes them one node that accumulates, instead of six that fragment.

## Definition

Resolution runs in two phases in these builds. **In-memory**, within one
extraction: fuzzy matching (`SequenceMatcher` at a 0.85 threshold) collapses
near-duplicate names of the same type, and — the step that is easy to forget —
**every edge endpoint is remapped to the canonical name**, or the merge silently
orphans edges [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]].
**Cross-document**, the incoming entity is matched against the nodes already
stored, checking full names and aliases before anything new is created
[[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]].

## Key claims

- Resolution combines an LLM (semantic matching) with database lookups, which makes it both expensive and the most failure-prone step in ingestion. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- It needs serialization *per entity*: two workers resolving the same name concurrently is a race condition. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- A resolved match is cached, so later documents mentioning the same alias resolve instantly. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Without it, unstructured extraction produces exactly the failure it is meant to prevent: entities duplicate and labels drift until the graph is noise. [[wiki/sources/rdf-vs-labeled-property-graphs]]
- Structural deduplication at materialization is the second line of defence — grouping by `{name, type}` merges what fuzzy matching missed. [[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]
- It is skippable: a working graph exists whose author states plainly, "I did not do any normalization." [[wiki/sources/tivadar-danka-knowledge-graph-questions]]

## Relationships

- **[[wiki/concepts/graph-extraction]]**: resolution cleans up what extraction produces; a tighter ontology leaves it less to do.
- **[[wiki/concepts/materialized-view]]**: where the structural half of deduplication happens.

## Tensions

- Most sources treat resolution as mandatory infrastructure; [[wiki/sources/tivadar-danka-knowledge-graph-questions]] runs an 810-node graph without it. The reconciling detail is scope: that graph is generated from one recursive process with one naming convention, where these builds ingest the same entity from email, notes and articles.

> Synthesis: The threshold (0.85) and the two-phase structure are worth copying, but the real lesson is the edge remap — a merge that renames nodes and forgets their edges leaves a graph that looks deduplicated and traverses wrong.
