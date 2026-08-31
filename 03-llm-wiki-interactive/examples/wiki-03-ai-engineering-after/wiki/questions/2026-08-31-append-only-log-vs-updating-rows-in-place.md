---
type: question
title: when should I use an append-only log instead of updating rows in place?
description: Probes whether the wiki's agent-memory sources generalize into a storage-design rule; they do, but only per layer.
asked_on: 2026-08-31
created: 2026-08-31T13:58:20Z
timestamp: 2026-08-31T13:58:20Z
answer_doc: "[[wiki/notes/append-only-log-vs-in-place-update]]"
sources_cited:
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/context-compaction]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
---

# when should I use an append-only log instead of updating rows in place?

> Asked on 2026-08-31 · answered from 7 wiki pages

## Answer

Full answer: [[wiki/notes/append-only-log-vs-in-place-update|Append-only logs vs. in-place updates]]

- The choice is per storage layer, not per system.
- Append when the history itself is read.
- Update in place when only the latest value is.
- `kg_events` appends; operational state uses `$set`/`$push`/`$inc`.
- Destructive rewrites become appended checkpoints.
- Price: replay cost, mitigated by snapshotting.

## Why this matters

It is the wiki's only storage-design rule, and it was reached twice independently of the question.
