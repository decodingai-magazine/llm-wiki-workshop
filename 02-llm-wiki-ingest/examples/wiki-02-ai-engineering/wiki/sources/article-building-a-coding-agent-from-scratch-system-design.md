---
type: source
title: "Building a Coding Agent From Scratch"
description: "Argues that the harness, not the model, is what makes a coding agent good, and lays out Decode's architecture: a ~20-line Pydantic AI loop wrapped in six harness modules, two interfaces (TUI and remote via Kitaru), and a three-tier evals layer."
origin: article
original_path: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
source_url: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
authors: ["Paul Iusztin"]
published_date: "2026-07-22T11:04:24+00:00"
raw_file: raw/article-building-a-coding-agent-from-scratch-system-design.md
created: "2026-08-31T18:40:57Z"
timestamp: "2026-08-31T18:40:57Z"
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/kitaru]]"
  - "[[wiki/entities/pydantic-ai]]"
concepts:
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/ai-evals]]"
---

# Building a Coding Agent From Scratch

> [[raw/article-building-a-coding-agent-from-scratch-system-design|Raw]] · article

## Summary

Lesson 1 of an 8-lesson open-source course in which the author builds **Decode**,
a coding-agent harness in Python, and uses it to argue that the harness — not the
model — is what separates a mediocre coding agent from a top-tier one. The piece
walks the system end to end, starting from the smallest possible core (a
~20-line Pydantic AI tool-calling loop) and building outward: six harness
modules (LLM providers, sandbox, permissions, memory, skills, LSP server) plus a
compaction behavior, two ways to run it (an interactive TUI and a remote mode
orchestrated by Kitaru), and a three-question evals layer. Throughout, the
author benchmarks Decode's design choices against how Claude Code, OpenCode, Pi
and Aider solve the same problems, since the course grew out of reverse-engineering
those tools' internals.

The framing device is a strict boundary: the "agent" is only the small
tool-calling loop; everything else — sandboxing, permissions, memory, skills,
observability, the steering queue, the remote runtime — is "the harness," and
the harness is the only layer an engineer can actually design.

## Key claims

- In a LangChain test on Terminal-Bench, changing only the harness (same model
  throughout) moved a coding agent from roughly 30th place into the top 5 — the
  article's stated reason for treating the harness as the object of study.
  [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|cite]]
- The entire tool-calling agent is a ~20-line Pydantic AI `Agent`: a model, a
  set of tools, an `AgentDeps` dataclass carrying harness state (cwd, event
  sink, permission gate), and an `output_type` of either a final answer or
  deferred tool calls awaiting approval, iterated via `agent.iter()`.
  [[raw/article-building-a-coding-agent-from-scratch-system-design#The Headless Harness & The Agent Loop|cite]]
- Decode organizes the harness into six modules — LLM Providers (Modal,
  OpenRouter, Gemini), Sandbox (Docker locally, Modal Sandboxes remotely),
  Permissions, Memory (AGENTS.md + MEMORY.md), Skills, and an LSP server (ty) —
  plus a Compaction behavior that squashes the context window into
  `[summary, *tail]` once it crosses a size threshold.
  [[raw/article-building-a-coding-agent-from-scratch-system-design#The Six Modules + Compaction|cite]]
- Mid-task input is handled by a steering queue + priority gate: new input is
  buffered and only injected at a safe boundary (before the next model call,
  never mid-tool-call). The article credits Pi (drains steering messages
  mid-turn, follow-ups only at the turn boundary) and Claude Code (ranks queued
  input so user messages never starve) with the same design problem.
  [[raw/article-building-a-coding-agent-from-scratch-system-design#The steering queue|cite]]
- Remote execution runs on Kitaru (ZenML's agent runtime) as a three-plane
  split — control plane (Kitaru on GCP), execution (Python locally / Modal
  remotely), sandbox (Docker locally / Modal remotely) — which gives the
  headless harness durability (resumes from the last recorded step after a
  sandbox dies) and replay (rerun a finished trace with one variable changed
  against the original as baseline).
  [[raw/article-building-a-coding-agent-from-scratch-system-design#The Remote Mode|cite]]
- The evals layer answers three separate questions with three separate
  mechanisms: internal benchmarks ("does it work?", one hidden-oracle-test case
  per task, the SWE-bench/Terminal-Bench pattern), regression tests ("does it
  still work?", scored against a baseline on every change), and production
  evals via Opik ("does it keep working?", every model/tool call traced, every
  conversation logged as a thread).
  [[raw/article-building-a-coding-agent-from-scratch-system-design#The Observability and AI Evals Layer|cite]]

## Notable quotes

> "The model isn't what makes a coding agent good. The harness is."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|location]]

> "These ~20 lines are the entire tool-calling LLM agent. The thing people call
> "the agent" ends here. Everything we build on top of it across 8 lessons is
> the coding harness."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#The Headless Harness & The Agent Loop|location]]

> "Just-in-time reads beat a stale heavy index."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#The Six Modules + Compaction|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/kitaru]], [[wiki/entities/pydantic-ai]]
- **Concepts**: [[wiki/concepts/cli]], [[wiki/concepts/skills]], [[wiki/concepts/agent-memory]], [[wiki/concepts/orchestration]], [[wiki/concepts/agent-harness]], [[wiki/concepts/ai-evals]]

> Synthesis: Where the wiki's other sources treat MCP, skills and memory as
> interfaces an agent reaches through, this one turns inward — the first source
> to describe the harness itself (loop, sandbox, permissions, evals) as one
> designed system, with Claude Code cited repeatedly as the existence proof of
> its design choices.
