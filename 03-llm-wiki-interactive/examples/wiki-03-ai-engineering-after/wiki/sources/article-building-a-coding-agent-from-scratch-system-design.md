---
type: source
title: Building a Coding Agent From Scratch
description: System-design overview of Decode, an open-source teaching harness that argues the harness — not the model — is what makes a coding agent good.
origin: article
original_path: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
source_url: https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design
authors:
  - Paul Iusztin
published_date: 2026-07-22T11:04:24+00:00
raw_file: raw/article-building-a-coding-agent-from-scratch-system-design.md
created: 2026-08-29T17:03:46Z
timestamp: 2026-08-29T17:03:46Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/kitaru]]"
  - "[[wiki/entities/pydantic-ai]]"
  - "[[wiki/entities/opik]]"
  - "[[wiki/entities/terminal-bench]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/steering-queue]]"
  - "[[wiki/concepts/context-compaction]]"
  - "[[wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/sandboxing]]"
---

# Building a Coding Agent From Scratch

> [[raw/article-building-a-coding-agent-from-scratch-system-design|Raw]] · article

## Summary

This is lesson 1 of an 8-lesson open-source course in which the author builds **Decode**, a teaching-replica coding agent, from a bare tool-calling loop into a remote swarm. The lesson's whole argument rests on one cited result: LangChain's Terminal-Bench experiment, where changing only the harness — same model throughout — moved a coding agent from roughly 30th place into the top 5. From that the author draws a sharp boundary: the "agent" is a ~20-line Pydantic AI tool-calling loop (model, tools, an `output_type` that ends a turn as either a final answer or paused tool calls); everything else — LLM providers, sandbox, permissions, memory, skills, an LSP server, plus context compaction — is the "harness," and the harness is the only layer actually worth engineering.

The piece then walks the system end to end: a headless harness core (no UI of its own) wired to two interfaces — a TUI for one live local session, and a remote mode where ZenML's Kitaru runtime orchestrates many headless harnesses in parallel on Modal, with durable, replayable, step-recorded execution. It closes with an observability/evals layer (via Opik) that separates three distinct questions — does it work, does it still work, does it keep working — into three mechanisms: custom benchmarks, regression suites, and production tracing.

The framing throughout is explicitly "clean architecture": the loop never knows which model or which interface is driving it, dependencies are injected via a single `AgentDeps` object, and the same headless core is meant to be reachable from a TUI, a message bus, or a remote scheduler without change.

## Key claims

- Changing only the harness (same model) moved a coding agent from ~30th place to the top 5 on Terminal-Bench in LangChain's test — the article's founding evidence that the harness, not the model, determines coding-agent quality. [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|cite]]
- The "agent" itself is scoped narrowly: a ~20-line Pydantic AI `Agent` whose `output_type` ends every turn as either a final string answer or `DeferredToolRequests` (tool calls suspended for human approval); everything built on top across the 8 lessons is called "the coding harness." [[raw/article-building-a-coding-agent-from-scratch-system-design#The Headless Harness & The Agent Loop|cite]]
- The headless harness is composed of six modules plus a non-module behavior: LLM Providers (Modal, OpenRouter, Gemini, swappable via config), Sandbox (Docker locally, Modal Sandboxes remotely), Permissions (ask/allow/deny per tool call, modeled on Claude Code's default/edit/auto modes), Memory (plain `AGENTS.md` + `MEMORY.md` files, deliberately no memory database or codebase index), Skills (workflows loaded only on invocation), an LSP server (ty, by Astral) for syntax/semantic feedback before code even runs, and Compaction (`[summary, *tail]`) to keep the context window small. [[raw/article-building-a-coding-agent-from-scratch-system-design#The Six Modules + Compaction|cite]]
- Mid-task input is handled by a steering queue plus priority gate: new input is buffered the instant it arrives and injected only at a safe boundary — before the next model call, never mid-tool-call — because injecting immediately would corrupt an in-flight tool call and dropping it would make the agent unsteerable. [[raw/article-building-a-coding-agent-from-scratch-system-design#The steering queue|cite]]
- In remote mode, Kitaru (ZenML's agent runtime) runs N headless harnesses in parallel on Modal, records each run's progress step by step so a dying sandbox resumes instead of restarting, freezes at human-input questions with no compute burned while waiting, and lets a finished run be replayed with one variable changed (model, prompt) against the original as baseline. [[raw/article-building-a-coding-agent-from-scratch-system-design#The Remote Mode|cite]]
- The evals/observability layer answers three separate questions with three separate mechanisms: custom internal benchmarks ("does it work?"), regression suites run against a baseline on every new feature ("does it still work?"), and Opik-traced production sessions with live scoring on sampled traces ("does it keep working?"). [[raw/article-building-a-coding-agent-from-scratch-system-design#The Observability and AI Evals Layer|cite]]

## Notable quotes

> "The model isn't what makes a coding agent good. The harness is."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#Lesson 1: Building a Coding Agent From Scratch|location]]

> "These ~20 lines are the entire tool-calling LLM agent. The thing people call "the agent" ends here. Everything we build on top of it across 8 lessons is the coding harness."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#The Headless Harness & The Agent Loop|location]]

> "Just-in-time reads beat a stale heavy index."
> — [[raw/article-building-a-coding-agent-from-scratch-system-design#The Six Modules + Compaction|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/modal]], [[wiki/entities/kitaru]], [[wiki/entities/pydantic-ai]], [[wiki/entities/opik]], [[wiki/entities/terminal-bench]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/agent-memory]], [[wiki/concepts/skills]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/steering-queue]], [[wiki/concepts/context-compaction]], [[wiki/concepts/permission-gate]], [[wiki/concepts/sandboxing]]

> Synthesis: This is a course-opening system-design overview, not an implementation record — it names and motivates every module (steering queue, sandbox, permissions, compaction) without yet showing the code, and the article itself points to five follow-on lessons that presumably ground these claims; treat this page as the map the rest of the series will fill in.
