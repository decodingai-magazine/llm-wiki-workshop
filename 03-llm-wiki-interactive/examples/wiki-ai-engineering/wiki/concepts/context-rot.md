---
type: concept
title: Context rot
description: As a context window fills, the signal-to-noise ratio collapses and the model degrades — the problem every retrieval decision in this wiki is ultimately optimizing against.
aliases: [Lost in the middle, Context bloat]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/graphrag-presentation]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
related:
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/data-fragmentation]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 5
---

# Context rot

> Noise accumulates in the context window until the ratio of signal to noise collapses — and cost and latency rise while quality falls.

## Definition

Context rot is degradation from *volume*, not from any single bad input: as the
window fills, "the ratio between signal and noise becomes very low, and the LLM
starts to have serious issues"
[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]].
Alongside it sits **lost in the middle** — the bias toward the beginning and end
of the window — which frontier models may fix while the underlying rot problem
persists.

It is also the reason the two are always named together with
[[wiki/concepts/data-fragmentation]]: fragmentation is why you retrieve broadly,
rot is why you must not.

## Key claims

- The damage is to performance, cost and latency at once — more tokens processed for less usable signal. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- The goal is a **minimum viable context**: deliver the relevant subgraph rather than fill the window. [[wiki/sources/graphrag-presentation]]
- Graph traversal helps precisely because it retrieves what is *connected* rather than what is merely similar, which is a smaller and better-targeted set. [[wiki/sources/graphrag-presentation]]
- Lost-in-the-middle is a positional bias distinct from rot, and may be solved sooner. [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]
- "The context window of the LLM is a budget" — every observation the loop feeds back spends from it. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Compaction is a harness responsibility with a menu: summarize, truncate, or clear. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- A working implementation has two tiers — an in-memory microcompaction with no LLM, and a full summary — and the tail cut must never split a tool-call/result pair. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Compaction is in-memory only: the session log keeps full fidelity, so shrinking the window does not lose the record. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/concepts/progressive-disclosure]]**: the main mitigation — return an index, not the contents.
- **[[wiki/concepts/agent-harness]]**: context management and compaction are the harness's job.

> Synthesis: Almost every design choice in this wiki — summaries over chunks, indexes over dumps, stripped embeddings, capped result counts — is a context-rot mitigation wearing a different name.
