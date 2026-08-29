---
type: question
title: Is event sourcing actually worth it for a personal knowledge graph?
description: The same trade-off asked at a specific scale, where the operational cost lands harder than the correctness benefit.
asked_on: 2026-08-29
created: 2026-08-29T11:10:00Z
timestamp: 2026-08-29T11:10:00Z
answer_doc: "[[wiki/notes/append-only-log-vs-in-place-updates]]"
sources_cited:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/sources/scaling-mongodb-brain-dump]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
---

# Is event sourcing actually worth it for a personal knowledge graph?

> Asked on 2026-08-29 · answered from 4 wiki pages · enriched the existing note

## Answer

Full answer: [[wiki/notes/append-only-log-vs-in-place-updates|Append-only log vs. in-place updates]]

- At personal scale the RAM arithmetic dominates the correctness benefit
- 10 GB of data can imply a 40 GB machine under the log-plus-view design
- The shipped system uses a single upsert collection
- Reversibility is still the one thing the alternative cannot offer

## Why this matters

Same trade-off, different scale — and the scale is what flips the answer.
