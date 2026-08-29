---
type: concept
title: Observability
description: Recording every model and tool call so a regression is a failing score rather than a user complaint — and so a bad answer can be traced to the call that produced it.
aliases: [Tracing, AI evals]
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
created: 2026-08-29T10:45:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 2
---

# Observability

> Every model call and every tool call, recorded — because an agent that fails silently fails invisibly.

## Definition

In the harness described by these sources, observability is a layer over the whole
loop rather than logging inside it: it records each model call and tool call, and
turns "a bad prompt tweak into a failing regression score before your users feel
it in production"
[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]. It is
presence-based — a silent no-op when no key is configured, so the agent behaves
identically without it
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]].

The same requirement appears from the orchestration side, where every task and
flow execution is tracked with timing, status, logs and retry history "in a
dashboard you didn't have to build".

## Key claims

- Tracing exists to catch regressions before users do, which makes it an evaluation tool as much as a debugging one. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- A trace per run with nested spans is what lets a wrong answer be traced back to the call that produced it. [[wiki/sources/article-the-coding-agent-loop]]
- Instrumentation should be optional and invisible when unconfigured — no key, no behaviour change. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Durable orchestration supplies half of it for free: task timing, status, logs and retry history. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]
- A session log kept at full fidelity is the complement to in-memory compaction — the window shrinks, the record does not. [[wiki/sources/article-the-coding-agent-loop]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: observability is a harness responsibility, not a model feature.
- **[[wiki/concepts/durable-execution]]**: the orchestrator's dashboard is the same need, one layer down.

> Synthesis: The thinnest-covered concept in the wiki relative to how often it is named — every source agrees it matters and none of them describes what they actually measure.
