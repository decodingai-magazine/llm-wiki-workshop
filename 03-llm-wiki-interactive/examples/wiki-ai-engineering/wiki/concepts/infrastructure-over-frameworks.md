---
type: concept
title: Infrastructure over frameworks
description: Infrastructure tools solve problems that are genuinely hard to build; AI frameworks abstract the parts that are easy — and then fight your data model.
aliases: [Build from scratch, No LangChain]
sources:
  - "[[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]"
  - "[[wiki/sources/deep-dive-on-how-to-scale-your-graphrag-ingestion-pipeline]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 5
---

# Infrastructure over frameworks

> Durable execution, aggregation, vector search and graph traversal are months of work. Ontologies, prompts, normalization and rank fusion are an afternoon. Buy the first, write the second.

## Definition

The claim is a division of labour rather than a rejection of libraries.
**Infrastructure** — a database that does documents, aggregation, text, vector and
graph in one place; an orchestrator with retries, caching and observability; a
model SDK — solves problems that would take months to rebuild.
**Business logic** — the ontology, the extraction prompt, normalization,
materialization, rank fusion — is domain-specific, changes with requirements, and
belongs in your codebase [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]].

The framework complaint is architectural, not aesthetic: embedded relationship
arrays, no ontology enforcement, no log/materialization split. "You can't
configure your way out of a data model mismatch."

## Key claims

- The hard parts of a GraphRAG system are infrastructure problems; the parts frameworks abstract are the easy ones. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- A framework's data model is not configurable, so any customization past its assumptions becomes a fight. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- "Infrastructure tools support your code. AI frameworks replace it." [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Frameworks and orchestrators are not competitors — they sit at different layers and compose. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- Pick the durability layer first and the reasoning layer second: the reasoning layer is the easy one to swap. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- The orchestrator earns its place by staying thin — decorators over pure functions that remain testable without it. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- The two-day build is the evidence offered, and its precondition is stated: the system design was already clear. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]

## Relationships

- **[[wiki/concepts/durable-execution]]**: the canonical example of a layer worth buying.
- **[[wiki/concepts/agentic-coding-loop]]**: a second criterion — does the tool fit inside the agent's edit-run-read-fix loop?

> Synthesis: The argument holds best where it is made — a system whose design was already settled — and every source here is the same practitioner, so read it as one strong opinion with several worked examples rather than as a consensus.
