---
type: note
title: Deciding a stored fact has gone stale
description: No source in this wiki detects staleness; they avoid storing invalidatable facts, evict by age, or let recency silently win — and the one working detector is a type checker, not a memory system.
created: 2026-08-31T14:14:39Z
timestamp: 2026-08-31T14:14:39Z
spawned_by_question:
  - "[[2026-08-31-deciding-a-fact-in-memory-has-gone-stale]]"
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/graphrag]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[append-only-log-vs-in-place-update]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
---

# Deciding a stored fact has gone stale

**No source in this wiki describes a staleness test.** Not one of the five memory
architectures here decides that a stored fact stopped being true. That absence is
consistent enough across independent designs to be the finding, not a gap in the
reading: every system either avoids storing facts that can go stale, discards them
on a schedule that ignores truth, or lets the newest write silently win.

## What the wiki does instead of detecting

**Don't store what you can re-derive.** `decode` ships no codebase index and no
memory database, and the stated principle is exactly this problem: *"Just-in-time
reads beat a stale heavy index."* [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
This is the only position in the wiki that engages staleness head-on, and its answer
is to make the question moot — a fact you re-read on demand cannot be stale.
[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]]

**Evict by age, not by truth.** `MEMORY.md` is auto-extracted, one LLM-written
summary sentence appended per session, capped at 200 lines / 25,000 bytes with
**oldest lines dropped first**. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
Note what that is and isn't: a true-but-old fact is deleted, a false-but-recent one
survives untouched. It bounds how much wrongness can accumulate without identifying
any of it.

**Let recency win, silently.** In the event-sourced graph, current state is derived
from the append-only log with `$sort` / `$group` / `$last` — the newest event for a
key wins. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/graphrag]]
A contradiction between an old fact and a new one is resolved by ordering and never
surfaced as a contradiction. What the log adds is not detection but *recoverability*:
the superseded value is still there for a human to audit.

**Freshness that only moves upward.** The personal knowledge graph stores a
referenced-but-not-yet-ingested URL as a `LATENT` placeholder and upgrades it with
real content when the ingest arrives. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
A fact can go stub → real; nothing takes it real → suspect.

**Make a human re-read it.** `AGENTS.md` is hand-written with a ~300-line target and
a ~600-line guardrail. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
The guardrail *is* the staleness mechanism — a size ceiling that forces periodic
human re-reading of every line.

## The one real detector, and why it isn't memory

The wiki does contain a system that continuously catches wrong claims: the LSP
Diagnostics Enricher, which appends up to 10 type errors to every successful file
edit or write, at no extra turn. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
It works because code has a **cheap oracle** — a type checker — and the artifact
being checked is right there. The evals layer has the same shape at a coarser grain:
*"does it still work?"* is answered by regression suites re-run against a kept
baseline, not by inspecting the agent. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

That gives the decision rule the wiki actually supports, and it is per fact, not per
store:

- **A cheap oracle exists and re-reading is cheap** → don't store the fact. Re-derive
  it. This is `decode`'s whole position, and the reason its memory holds *preferences
  and corrections* (which have no oracle and rarely change) rather than *code facts*
  (which have one and change constantly).
- **No oracle exists** → you cannot detect staleness, and no scheme in this wiki
  pretends otherwise. Bound the damage instead: cap the fact's lifetime
  (`MEMORY.md`), or keep the superseded value so a human can adjudicate later
  (`kg_events`). See [[append-only-log-vs-in-place-update]].

> Synthesis: the wiki can tell you why staleness detection is hard and what people
> build instead, but it has no positive mechanism — no TTL, no confidence decay, no
> contradiction detection, no re-verification pass — because every source here stores
> either oracle-free preferences or an append-only log where the question is deferred
> to a human. A source that ran a memory system long enough to *hit* the problem would
> revise this note substantially; all five here describe systems at or near their
> build date.
