---
type: source
title: Building a Coding Agent From Scratch
description: The system design of a coding-agent harness — one headless core with six modules around the loop, two interfaces over one message bus, and an evals layer on top.
origin: article
original_path: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
source_url: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
authors: ["Paul Iusztin"]
published_date: "2026-07-22T11:04:24+00:00"
raw_file: raw/article-building-a-coding-agent-from-scratch-system-design.md
created: 2026-08-29T10:45:00Z
timestamp: 2026-08-29T10:45:00Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/modal]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/context-rot]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/inference-economics]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/observability]]"
---

# Building a Coding Agent From Scratch

> [[raw/article-building-a-coding-agent-from-scratch-system-design|Raw]] · article · [Original](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)

## Summary

The opening lesson of a course whose thesis is stated as a benchmark result: in
LangChain's Terminal-Bench experiment, changing only the harness — same model
throughout — moved a coding agent from roughly 30th place into the top 5. "The
model isn't what makes a coding agent good. The harness is."

The design is drawn as one headless core with interfaces attached. At the centre
is the agent loop every harness shares: the model picks a tool call, the tool
returns an observation, the loop feeds it back, and everything reads from and
writes to the context window. Around it sit six modules — **LLM providers**, an
**LSP server** for immediate feedback on edits, **memory**, **skills**,
**sandbox** and **permissions** — plus compaction, because "the context window of
the LLM is a budget" and every observation spends from it.

Two interfaces connect to that core: an interactive TUI wired to one live session,
and a remote mode where a durable runtime runs N headless harnesses in parallel.
Both speak through the same event stream. On top of everything is an observability
and evals layer that records every model and tool call, so "a bad prompt tweak
[becomes] a failing regression score before your users feel it".

The end-to-end trace is the clearest part: type a request → the steering queue and
priority gate put it in the context window → the loop sends the window and the
tool schemas to the model → the model answers with an action → permissions decides
→ the tool runs in the sandbox → the observation goes back into the window → repeat
until the model stops calling tools, with events streaming to the terminal.

## Key claims

- Changing only the harness moved a coding agent from ~30th to the top 5 on the same benchmark. [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|cite]]
- The harness is "the only layer you can actually engineer" — the argument for building one rather than configuring one. [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|cite]]
- The headless core has no interface of its own; the TUI and the remote runtime are clients of the same module. [[raw/article-building-a-coding-agent-from-scratch-system-design#The High-Level System Design|cite]]
- Multiple providers exist to prove the harness is independent of the model — self-hosted, gateway, and a hosted free tier. [[raw/article-building-a-coding-agent-from-scratch-system-design#The High-Level System Design|cite]]
- An LSP server is "the cheapest way to get feedback on code changes" — it catches broken syntax before anything runs. [[raw/article-building-a-coding-agent-from-scratch-system-design#The High-Level System Design|cite]]
- The context window is a budget and every observation spends from it, so compaction (summarize, truncate, clear) is a harness responsibility. [[raw/article-building-a-coding-agent-from-scratch-system-design#The High-Level System Design|cite]]
- The tighter the feedback loops, the faster the agent converges on working code. [[raw/article-building-a-coding-agent-from-scratch-system-design#The High-Level System Design|cite]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/modal]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/context-rot]], [[wiki/concepts/provider-abstraction]], [[wiki/concepts/inference-economics]], [[wiki/concepts/durable-execution]], [[wiki/concepts/agent-memory]], [[wiki/concepts/agent-skills]], [[wiki/concepts/observability]]

> Synthesis: The prose companion to [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] — same system, one written to explain and one written to run, which makes them the best pair in the wiki for checking whether a description survives contact with its implementation.
