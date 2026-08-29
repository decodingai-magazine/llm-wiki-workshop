---
type: source
title: Context Engineering for Coding Agents
description: The four harness components that keep a context window high-signal — memory, skills, an LSP server and compaction — with the thresholds each one fires at.
origin: article
original_path: https://www.decodingai.com/p/context-engineering-for-coding-agents
source_url: https://www.decodingai.com/p/context-engineering-for-coding-agents
authors: ["Paul Iusztin"]
published_date: "2026-08-25T05:01:37+00:00"
raw_file: raw/article-context-engineering-for-coding-agents.md
created: 2026-08-29T11:50:00Z
timestamp: 2026-08-29T11:50:00Z
entities: []
concepts:
  - "[[wiki/concepts/context-rot]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
---

# Context Engineering for Coding Agents

> [[raw/article-context-engineering-for-coding-agents|Raw]] · article · [Original](https://www.decodingai.com/p/context-engineering-for-coding-agents)

## Summary

The article the wiki was missing: a per-turn account of what occupies a coding
agent's context window, and which harness component manages each part. Four
components, each with a threshold rather than a principle.

**Memory** stops you repeating instructions — project conventions live in a file
that is injected every turn, which is exactly why it must stay small.
**Skills** are the fix for what memory files become: conventions that used to bloat
every session moved into skills, leaving "just a few lines, as references". The
mechanism is **progressive disclosure across three tiers** — tier 1 keeps only the
catalog in context, one `name + description` line per skill, with an optional guard
capping the catalog at ~1% of the window; the body and its bundled files load only
when that workflow phase runs. The article cites a measurement that popular tool
servers consume **7–9% of the context window before any work begins**, which is the
same budget argument from the other direction.

**The LSP server** replaces guessing with precision — feedback on an edit without
spending a turn discovering the error.

**Compaction** is where the numbers are. The reported experience is degradation
around **180,000 input tokens** on a model advertised at 1M — "a full window
degrades model performance and reliability long before hitting the hard token
ceiling". Three modes answer it: `/clear` wipes the window after writing learnings
back to the memory file; **full compaction** fires automatically at **80% capacity**
and rebuilds the window as `[system prompt] + [summary] + [recent tail]`, where an
LLM summary follows a six-part template (goal, constraints and preferences,
progress, key decisions, next steps, critical context) and the tail keeps ~20,000
tokens snapped to a **compaction boundary** so tool calls stay paired with their
results; **microcompaction** fires at **60%** and swaps old tool outputs for
placeholders in place.

The implementation detail worth keeping: the summary is written as a synthetic
message that is itself part of the history the *next* compaction summarizes, so
successive compactions merge for free. And the harness owns the list it feeds the
model — "replacing the list IS the compaction".

## Key claims

- A window degrades well before its advertised ceiling: ~180k input tokens on a model rated for 1M. [[raw/article-context-engineering-for-coding-agents#Compaction: Delete before the window rots|cite]]
- Full compaction fires at 80% of the window, microcompaction at 60% — thresholds, not judgement calls. [[raw/article-context-engineering-for-coding-agents#Compaction: Delete before the window rots|cite]]
- The compacted window is system prompt + summary + a ~20k-token tail cut at a boundary that keeps tool calls with their results. [[raw/article-context-engineering-for-coding-agents#Compaction: Delete before the window rots|cite]]
- The summary is itself history, so successive compactions merge without extra machinery. [[raw/article-context-engineering-for-coding-agents#Compaction: Delete before the window rots|cite]]
- Skills load in three tiers; only a one-line catalog entry per skill stays resident, optionally capped at ~1% of the window. [[raw/article-context-engineering-for-coding-agents#Skills: Never load what you can reference|cite]]
- Tool schemas are not free: popular servers were measured at 7–9% of the window before any work begins. [[raw/article-context-engineering-for-coding-agents#Skills: Never load what you can reference|cite]]
- Moving conventions out of the memory file and into skills is the concrete fix for a memory file that pollutes every turn. [[raw/article-context-engineering-for-coding-agents#Skills: Never load what you can reference|cite]]
- `/clear` runs a memory write-back first, so wiping the window does not lose what the session learned. [[raw/article-context-engineering-for-coding-agents#Compaction: Delete before the window rots|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/context-rot]], [[wiki/concepts/agent-harness]], [[wiki/concepts/agent-skills]], [[wiki/concepts/agent-memory]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/agentic-coding-loop]]

> Synthesis: This closes the open question the wiki logged an hour earlier — it is the only source that walks a single turn and accounts for the window — and it converts three of the wiki's qualitative claims (context rot, progressive disclosure, skills-as-references) into thresholds you can implement.
