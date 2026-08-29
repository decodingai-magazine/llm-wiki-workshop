---
type: source
title: Why durable workflow tools are more important than AI frameworks
description: AI frameworks decide how an agent thinks; durable execution decides whether it survives — with the cost arithmetic of retrying a failed multi-step pipeline from scratch.
origin: local
original_path: data_input_examples/notes/03-hard/Why Durable Workflow Tools Are More Important Than AI Frameworks.md
source_url: null
authors: []
published_date: null
raw_file: raw/why-durable-workflow-tools-are-more-important-than-ai.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/langchain]]"
concepts:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/inference-economics]]"
---

# Why durable workflow tools are more important than AI frameworks

> [[raw/why-durable-workflow-tools-are-more-important-than-ai|Raw]] · local

## Summary

The argument is a layering: an AI framework decides **how the agent thinks**, the
orchestration layer decides **whether it survives**, infrastructure decides where
it runs. Frameworks are swappable — moving between them is a contained rewrite —
while the durability layer is "months of engineering" to build and the most
expensive to skip.

The cost of skipping it is made concrete. A six-step pipeline fails at step 5; a
naive retry re-runs everything, wasting the money already spent *and* duplicating
two memory writes. At 100 runs a day with a 30% failure rate and a cent wasted per
retry, that is ~$270 a month in pure waste, plus double writes, plus the
engineering time spent debugging why a memory was stored twice. With result
caching, the completed steps load from cache and only the failed step re-executes.

The mechanism is three primitives — `@flow`, `@task`, and result persistence —
and the note lists what they buy: caching and resumption, per-component retry
policies (exponential backoff for rate-limited LLM calls, fast retries for
transient I/O), observability without building a dashboard, scheduling and
deployment, human-in-the-loop pauses, and dynamic control flow. That last one
matters for agents specifically: a precompiled DAG cannot express a plan the model
decides at runtime, so an orchestrator that "instruments Python rather than
constraining it" is the one that fits.

The comparison section is even-handed — Prefect adds infrastructure and knows
nothing about prompts, its streaming is buffered rather than real-time, and it is
overkill for single-shot calls — and it ends with a recommendation of order rather
than of tool: start with durability, then pick whatever reasoning layer fits.

## Key claims

- Every AI framework solves the same problem (reason, call tools, structure output) and none of them addresses what happens when a step fails. [[raw/why-durable-workflow-tools-are-more-important-than-ai|cite]]
- Without result caching a retry re-runs successful steps, burning tokens and duplicating side effects. [[raw/why-durable-workflow-tools-are-more-important-than-ai#The real cost of fragility|cite]]
- Different components need different retry policies — exponential backoff for rate limits, fast retries for I/O. [[raw/why-durable-workflow-tools-are-more-important-than-ai#What durable execution actually gives you|cite]]
- Precompiled DAGs cannot express agent behaviour, because the next action is decided at runtime. [[raw/why-durable-workflow-tools-are-more-important-than-ai#What durable execution actually gives you|cite]]
- Streaming inside a durable flow is buffered, not real-time — real-time token streaming has to live outside it. [[raw/why-durable-workflow-tools-are-more-important-than-ai#What durable execution actually gives you|cite]]
- "The AI framework makes your agent smart. The durability layer makes it reliable… reliability is harder to bolt on after the fact." [[raw/why-durable-workflow-tools-are-more-important-than-ai#Why this matters more than choosing the "right" AI framework|cite]]
- The layers compose rather than compete: durable wrappers around framework agents, framework graphs inside orchestrated tasks, or no framework at all. [[raw/why-durable-workflow-tools-are-more-important-than-ai#How these tools are complementary|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/langchain]]
- **Concepts**: [[wiki/concepts/durable-execution]], [[wiki/concepts/infrastructure-over-frameworks]], [[wiki/concepts/agent-harness]], [[wiki/concepts/inference-economics]]

> Synthesis: The most complete argument in the wiki for a claim the other notes assume — and note that its cost model, like the inference-economics notes, makes waste rather than latency the deciding number.
