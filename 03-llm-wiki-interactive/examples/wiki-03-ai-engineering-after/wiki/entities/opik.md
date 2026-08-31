---
type: entity
title: Opik
description: The tracing platform decode wires into its agent loop via OTLP spans, used both to debug the loop during development and to run live-scored production evals.
aliases: []
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-loop]]"
created: 2026-08-29T17:08:28Z
timestamp: 2026-08-29T17:08:28Z
source_count: 3
---

# Opik

> The observability layer wired into decode's agent loop from day one — OTLP spans out for debugging, plus live-scored production tracing as one of three evals mechanisms.

## Definition

All three sources treat Opik as decode's tracing/observability tool rather than defining it independently — it is named, not explained, which is consistent with it being infrastructure that is "imported, not abstracted" alongside `modal` and `pydantic-ai`. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The build-log article frames it as a development aid — "Opik/OTLP tracing wired in from day one to make the loop debuggable" — while the system-design article frames it as a production mechanism, the tracing backend behind live-scored sampled sessions. [[wiki/sources/article-the-coding-agent-loop]], [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] The codebase corroborates both framings with a dedicated `observability/` module. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- decode has a dedicated `observability/` module doing Opik/OTLP tracing plus a cost-annotating span exporter, and the architecture diagram shows the agent loop emitting spans out to it (`LOOP -.spans.-> OBS`). [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Opik/OTLP tracing is wired into the loop "from day one," motivated purely by debuggability during development, not just as a later production add-on. [[wiki/sources/article-the-coding-agent-loop]]
- In production, the evals/observability layer answers three separate questions with three separate mechanisms: custom internal benchmarks ("does it work?"), regression suites run against a baseline on every new feature ("does it still work?"), and Opik-traced production sessions with live scoring on sampled traces ("does it keep working?"). [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: Opik is one of the harness's named modules — the observability/evals layer sits alongside LLM providers, sandbox, permissions, memory, skills and compaction as a piece of infrastructure engineered on top of the ~20-line agent core. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/agent-loop]]**: the loop is the thing Opik instruments — every leg of the turn handler emits spans out to it, which is what makes the loop's behavior debuggable and later scoreable in production. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[wiki/sources/article-the-coding-agent-loop]]

> Synthesis: all three witnesses trace to the same course and, for the two articles, the same author — this is one voice describing one codebase from two angles (build log vs. system-design), not independent corroboration; treat "Opik is decode's observability backbone" as well-attested within this project rather than externally validated.
