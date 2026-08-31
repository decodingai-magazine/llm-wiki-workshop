---
type: question
title: is event sourcing actually worth it for a personal knowledge graph?
description: Tests the wiki's storage rule against the one personal knowledge graph it documents — which was built without an event log.
asked_on: 2026-08-31
created: 2026-08-31T14:05:21Z
timestamp: 2026-08-31T14:05:21Z
answer_doc: "[[wiki/notes/append-only-log-vs-in-place-update]]"
sources_cited:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/concepts/context-compaction]]"
---

# is event sourcing actually worth it for a personal knowledge graph?

> Asked on 2026-08-31 · answered from 6 wiki pages · enriched an existing note

## Answer

Full answer: [[wiki/notes/append-only-log-vs-in-place-update|Append-only logs vs. in-place updates]] — see "Does a personal knowledge graph clear the bar?"

- Usually not, on the wiki's evidence.
- The wiki's one personal KG has no event log.
- It upgrades `LATENT` placeholders in place instead.
- Same author recommends `kg_events`, did not build it.
- Cost is fixed, not proportional to scale.
- Flips when an unattended LLM writer mutates the graph.

## Why this matters

It separates the storage rule from the scale it is usually confused with: the trigger is who writes, not how much.
