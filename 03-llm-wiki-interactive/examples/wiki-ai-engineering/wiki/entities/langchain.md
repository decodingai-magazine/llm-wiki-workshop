---
type: entity
title: LangChain
description: The framework these notes started with and left — used throughout the wiki as the worked example of a data model you cannot configure your way out of.
aliases: [LangGraph, MongoDBGraphStore]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]"
  - "[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]"
related:
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graph-extraction]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 3
---

# LangChain

> The 10-minute knowledge graph, and the reason the rest of this wiki was written from scratch.

## Definition

LangChain appears in these sources almost entirely as a counterexample, and
fairly: its graph store produced a working knowledge graph in ten minutes. The
objection is to what it stored — entities with relationships embedded as parallel
arrays, no ontology enforcement, no observation log
[[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]. Its
ecosystem sibling LangGraph is treated more evenly, as a reasoning layer that
composes with an orchestrator rather than competing with one
[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]].

## Key claims

- The graph store delivered 80 entities in ten minutes — the speed is not disputed. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Unconstrained extraction produced 17 node types and 34 relationship types from 5 documents, including three casings of one type. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Embedded relationship arrays make deduplication a full scan, updates a parent-document write, and traversal impossible without restructuring. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- `allowed_nodes` constrains types but not the data model — "you can't configure your way out of a data model mismatch". [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- LangGraph is credited for multi-agent graphs, explicit state machines and checkpointing, and faulted for coupling, verbosity and no result caching. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]

## Relationships

- **[[wiki/concepts/infrastructure-over-frameworks]]**: the position this entity is the evidence for.
- **[[wiki/concepts/graph-extraction]]**: the specific failure — extraction without an enforced ontology.

> Synthesis: All three sources are one practitioner's account of one project, so read this as a well-documented mismatch between a framework's assumptions and this build's requirements, not as a general verdict.
