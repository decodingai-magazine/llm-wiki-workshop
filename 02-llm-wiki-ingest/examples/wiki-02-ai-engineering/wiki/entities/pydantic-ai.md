---
type: entity
title: Pydantic AI
description: The Python agent framework whose ~20-line, type-safe `Agent` object is the tool-calling loop underlying Decode, the coding-agent harness built across Paul Iusztin's course.
aliases: []
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/cli]]"
created: "2026-08-31T19:00:00Z"
timestamp: "2026-08-31T20:05:00Z"
source_count: 3
---

# Pydantic AI

> The framework Decode's entire tool-calling agent is built on — reduced to a ~20-line `Agent` object in both the wiki's prose and its code.

## Definition

All three sources treat Pydantic AI as the library underlying Decode's agent
loop rather than defining the framework in the abstract — it appears
consistently as "the thing the ~20-line agent is built with," never as a
standalone subject. The system-design article draws the strongest boundary:
the entire tool-calling agent — everything the piece insists actually counts
as "the agent," as opposed to the surrounding harness — is a ~20-line
Pydantic AI `Agent`. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
The loop-focused companion piece calls Decode itself a "Pydantic-AI
coding-agent harness," using the framework's name as shorthand for the whole
project's foundation. [[wiki/sources/article-the-coding-agent-loop]] The
repo's architecture page confirms the same claim in code: Decode "is a
single Pydantic AI `Agent`," built in `agent/factory.py` and driven by
`agent.iter()` inside `agent/loop.py`'s `AgentTurnHandler`.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- The entire tool-calling agent is a ~20-line Pydantic AI `Agent`: a model, a
  set of tools, an `AgentDeps` dataclass carrying harness state (cwd, event
  sink, permission gate), and an `output_type` of either a final answer or
  deferred tool calls awaiting approval, iterated via `agent.iter()`.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Decode is a "Pydantic-AI coding-agent harness" built to reach feature
  parity with Mario Zechner's minimalist Pi harness.
  [[wiki/sources/article-the-coding-agent-loop]]
- Decode's observability — Opik/OTLP tracing of every model and tool call —
  is wired through Pydantic AI's built-in Logfire integration rather than a
  bespoke tracing layer. [[wiki/sources/article-the-coding-agent-loop]]
- In the codebase, the Agent is built with `output_retries=3` and
  `tool_retries=5`, then `set_main_agent()` marks it as the one installed
  Agent that every subagent re-enters rather than reconstructs.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Decode's two-tier compaction sizes itself off the *last* response's own
  token usage rather than the cumulative per-round total that Pydantic AI
  reports — a workaround the harness needed, not a framework feature.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **Decode**: Pydantic AI supplies the `Agent`/`AgentDeps`/`agent.iter()`
  primitives that all three sources treat as the strict boundary between
  "the agent" and the harness built around it — confirmed in code at
  `agent/factory.py` and `agent/loop.py`, and re-entered unmodified by every
  subagent spawn. [[wiki/entities/decode]], [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **Pi-agent**: Decode, built on Pydantic AI, targets feature parity with
  Mario Zechner's Pi harness rather than reinventing its tool set or loop
  shape. [[wiki/entities/pi-agent]], [[wiki/sources/article-the-coding-agent-loop]]
- **Opik**: Decode's tracing to Opik rides on Pydantic AI's Logfire
  integration rather than a separate instrumentation layer.
  [[wiki/entities/opik]], [[wiki/sources/article-the-coding-agent-loop]]

> Synthesis: all three sources trace to one author and one project (Paul
> Iusztin's Decode course), so this is one voice describing Pydantic AI
> three times, not independent corroboration — but the passes are
> increasingly concrete: the system-design piece names Pydantic AI as *the*
> agent in prose, the loop piece shows it wired up end to end, and the
> repo's architecture page is the code itself, down to the exact `Agent(...)`
> call and the subagent re-entry trick.
