---
type: question
title: How do I decide that a fact in the memory has gone stale?
description: The wiki has a mechanism for correcting knowledge and no policy for deciding when to — the gap is recorded rather than papered over.
asked_on: 2026-08-29
created: 2026-08-29T11:20:00Z
timestamp: 2026-08-29T11:20:00Z
answer_doc: null
sources_cited:
  - "[[wiki/concepts/knowledge-freshness]]"
  - "[[wiki/concepts/append-only-log]]"
---

# How do I decide that a fact in the memory has gone stale?

> Asked on 2026-08-29 · 2 wiki pages read · **not answerable from this wiki**

## Answer

The wiki does not cover this. What it has is one half of the problem:

- A **mechanism** — the append-only log makes superseding and reverting cheap, and
  housekeeping (classify, soft-delete, re-materialize) safe
  [[wiki/concepts/append-only-log]].
- A record that the **policy** is missing: [[wiki/concepts/knowledge-freshness]]
  collects the reader questions about decay and wrong extractions and answers none
  of them.

Nothing in the corpus says *when* a fact should be considered stale — no decay
function, no recency weighting, no supersession rule beyond "the latest log entry
wins". Logged as an open question rather than guessed at.

## Why this matters

Every memory system in this wiki accumulates; none of them forgets, and nobody has written down when they should.
