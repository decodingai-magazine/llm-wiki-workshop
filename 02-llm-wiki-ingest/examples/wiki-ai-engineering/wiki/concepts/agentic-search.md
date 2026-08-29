---
type: concept
title: Agentic search
description: Letting the model write the database query itself, with the ontology in its prompt and a guard-rail stack around it.
aliases: [NL to query, query_memory]
sources:
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/retrieval-strategies]]"
related:
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/mcp-server-design]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 3
---

# Agentic search

> Fixed retrieval paths cannot express "how many tasks does Paul have?". Agentic search hands the query language to the model — and then fences it in.

## Definition

For questions the hardwired algorithms cannot express — aggregations, filters,
counts — the model translates natural language directly into a database query.
What makes it work is that the **ontology is compiled into the prompt**: every
entity and relationship type the memory can contain, so the model targets a schema
it understands rather than guessing field names
[[wiki/sources/retrieval-strategies]].

What makes it safe is a stack of guard rails: an allow-list of permitted
operations, server-injected user scoping the model cannot override, a forced
result limit, embeddings stripped from responses, a placeholder so the model can
request vector search without seeing a vector, and a self-correction retry that
feeds validation and execution errors back to the model
[[wiki/sources/agentic-graphrag-via-mcp-servers]].

## Key claims

- The ontology in the prompt is what separates a generated query from a guess. [[wiki/sources/retrieval-strategies]]
- Validation is an allow-list, not a blocklist: permitted stages only, no writes, joins restricted to the graph collection. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Errors are fed back for one self-correcting retry rather than surfaced as failures. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- It is the *default* tool in one design and the *fallback* in another — deterministic hybrid search is the counterpart either way. [[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]
- Tenant scoping must be injected by the server and overwritten, so the model cannot escape its user. [[wiki/sources/retrieval-strategies]]
- Agents should be able to write queries dynamically against the graph in whatever query language it speaks. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]

## Relationships

- **[[wiki/concepts/hybrid-search]]**: the deterministic path this one complements — one always returns something, the other can answer anything.
- **[[wiki/concepts/mcp-server-design]]**: the guard rails are a server responsibility, not a prompt.

> Synthesis: The interesting design choice is pairing a flexible path with a deterministic one and telling the agent when to use each — capability and predictability bought separately rather than traded off.
