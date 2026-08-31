---
type: open_question
title: Open questions
description: Questions the wiki cannot answer yet, and gaps worth ingesting for.
created: 2026-08-31T13:58:20Z
timestamp: 2026-08-31T15:18:35Z
---

# Open questions

## 2026-08-31

- Append-only storage beyond agent memory — write amplification, log compaction, and retention/right-to-erasure against an immutable log — from [[wiki/questions/2026-08-31-append-only-log-vs-updating-rows-in-place]]. The wiki's only witnesses are one vendor-architecture note and one coding-agent codebase; `event-sourcing` sits at 1 mention with no concept page.
- What does an event-sourced knowledge graph actually cost to *run* over time — snapshot cadence, log growth, migration of the derived views — from [[wiki/questions/2026-08-31-event-sourcing-for-a-personal-knowledge-graph]]. The wiki has architecture arguments for `kg_events` and one personal graph built without it, but no report from anyone who operated one.
- How does any memory system decide a stored fact has gone **stale** — TTL, confidence decay, contradiction detection, re-verification? — from [[wiki/questions/2026-08-31-deciding-a-fact-in-memory-has-gone-stale]]. Five memory architectures in this wiki and not one has a mechanism; they avoid, evict by age, or let recency win. Every source describes a system at or near its build date, so none has operated long enough to hit the problem.
- What actually goes into a coding agent's context window each turn — the full assembly, not just memory — flagged directly by the user, not yet answered against the wiki. Candidate sources already present: `agent-harness`, `context-compaction`, `skills`, `progressive-disclosure`, `progressive-tool-discovery`, the `decode` repo's context-engineering section.
