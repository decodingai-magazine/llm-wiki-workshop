---
type: question
title: When should I use an append-only log instead of updating rows in place?
description: The wiki argues both sides — nine sources for the log, one reporting its abandonment — so the answer is a decision rule rather than a verdict.
asked_on: 2026-08-29
created: 2026-08-29T11:00:00Z
timestamp: 2026-08-29T11:00:00Z
answer_doc: "[[wiki/notes/append-only-log-vs-in-place-updates]]"
sources_cited:
  - "[[wiki/concepts/append-only-log]]"
  - "[[wiki/concepts/materialized-view]]"
  - "[[wiki/concepts/database-scaling]]"
  - "[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]]"
---

# When should I use an append-only log instead of updating rows in place?

> Asked on 2026-08-29 · answered from 4 wiki pages

## Answer

Full answer: [[wiki/notes/append-only-log-vs-in-place-updates|Append-only log vs. in-place updates]]

- The log buys provenance, replay and reversibility
- The view buys queryability, and costs a second copy in RAM
- LLM-written data is the case that needs reversibility
- One source reversed this decision after running it
- Decision rule: how often will you actually need to revert?

## Why this matters

It is the wiki's only live architectural disagreement, and picking wrong is expensive in both directions.
