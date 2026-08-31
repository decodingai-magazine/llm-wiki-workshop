---
type: concept
title: Context Compaction
description: The harness mechanism that keeps a coding agent's context window from filling up, escalating from cheap in-memory elision to an LLM-written summary-plus-tail as usage crosses threshold percentages of the window.
aliases: []
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/lsp-server]]"
created: 2026-08-29T17:09:06Z
timestamp: 2026-08-29T17:09:06Z
source_count: 3
---

# Context Compaction

> An automatic two-tier cascade — cheap in-memory elision, then an LLM-written summary plus tail — triggered by usage thresholds, with a manual full wipe as an escalation above both.

## Definition

All three sources describe the same mechanism in decode, at increasing resolution. The system-design lesson names compaction as one of the harness's six modules and gives only its output shape: history becomes `[summary, *tail]` to keep the window small. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] The context-engineering lesson opens the mechanism up into three escalating modes — a manual `/clear` (wipe everything after a memory write-back), full compaction at ~80% window capacity (one LLM call, a summary written into a six-part template plus a ~20,000-token verbatim tail), and microcompaction at ~60% capacity (no LLM call — old tool outputs are replaced in place with a placeholder string). [[wiki/sources/article-context-engineering-for-coding-agents]] The repo architecture page confirms both automatic thresholds against the actual source and adds the implementation detail neither article states: the two-tier cascade is checked once per turn, at the `WOULD_STOP` boundary, against the *last populated* `ModelResponse.usage` rather than the turn's cumulative usage. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- Compaction is triggered by an occupancy ratio checked against the window size: ~60% fires microcompaction, ~80% fires full compaction, both figures agreed by the code and the deep-dive article. [[wiki/sources/article-context-engineering-for-coding-agents]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Microcompaction is cheapest-first and reversible: it blanks old tool-output bodies with a placeholder, in memory only, never persisted — so a crash-and-`--resume` still replays the full, unelided history. [[wiki/sources/article-context-engineering-for-coding-agents]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Full compaction spends one LLM call to replace history with `[summary, *tail]` — a six-part summary template plus a ~20,000-token verbatim tail per the deep-dive — and writes a checkpoint into the session's append-only JSONL log so the rewrite survives a resume. [[wiki/sources/article-context-engineering-for-coding-agents]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The occupancy check reads only the last populated `ModelResponse.usage` (input + cache-read tokens), not the turn's cumulative usage, because pydantic-ai accumulates usage across every tool round and would overcount by roughly N× for an N-round turn. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Any compaction's cut point is always a "compaction boundary" — a user `ModelRequest` or any `ModelResponse`, never a request carrying a tool return — so a compaction can never orphan a tool call from its result. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- A third, manually-triggered mode sits above both automatic thresholds: `/clear` writes back to memory, then wipes the context entirely — the cheapest and most destructive option, reserved for when a session's task is finished rather than merely long. [[wiki/sources/article-context-engineering-for-coding-agents]]
- Measured effect of one manual full-compaction run: usage dropped from ~57% (~149,539 tokens) to ~8% of a 262,144-token window. [[wiki/sources/article-context-engineering-for-coding-agents]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: compaction is named as one of the harness's context-engineering modules, not part of the ~20-line agent loop itself. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **[[wiki/concepts/agent-memory]]**: memory files sit in the same instructions block that compaction is built to protect, but compaction acts on conversation history around them, not on memory content — and `/clear`'s write-back is the one place the two mechanisms touch directly. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/skills]]**, **[[wiki/concepts/progressive-disclosure]]**: compaction and skills solve the same problem — keep the window high-signal — with the same tactic, deferring or discarding what isn't needed right now rather than loading everything upfront. [[wiki/sources/article-context-engineering-for-coding-agents]]
- **[[wiki/concepts/lsp-server]]**: named alongside compaction as one of the deep-dive's four cooperating context-engineering components across a session, though the LSP server adds signal while compaction removes it. [[wiki/sources/article-context-engineering-for-coding-agents]]

> Synthesis: two of the three sources are one author (Paul Iusztin) narrating the same Decode codebase across two lessons, so their agreement is partly one voice restating itself at different depths; the repo architecture page is the load-bearing third witness, written from an independent read of the actual source, and it confirms the exact 60%/80% thresholds and the `[summary, *tail]` shape rather than just repeating the articles' claims.
