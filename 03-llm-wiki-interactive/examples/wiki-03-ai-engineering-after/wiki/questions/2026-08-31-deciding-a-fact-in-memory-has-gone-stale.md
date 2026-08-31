---
type: question
title: how do I decide that a fact in the memory has gone stale?
description: "Found a consistent negative: no memory architecture in the wiki detects staleness, and the reason is structural."
asked_on: 2026-08-31
created: 2026-08-31T14:14:39Z
timestamp: 2026-08-31T14:14:39Z
answer_doc: "[[wiki/notes/staleness-in-agent-memory]]"
sources_cited:
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/context-compaction]]"
---

# how do I decide that a fact in the memory has gone stale?

> Asked on 2026-08-31 · answered from 7 wiki pages · the wiki has no positive mechanism

## Answer

Full answer: [[wiki/notes/staleness-in-agent-memory|Deciding a stored fact has gone stale]]

- No source here detects staleness. None.
- `decode` avoids it: don't index what you re-read.
- `MEMORY.md` evicts by age, ignoring truth.
- `$last` lets recency win without flagging it.
- The only live detector is a type checker.
- Rule: cheap oracle → re-derive; no oracle → cap or log.

## Why this matters

The absence is consistent across five independent memory designs, which makes it a finding about the problem rather than a hole in the wiki.
