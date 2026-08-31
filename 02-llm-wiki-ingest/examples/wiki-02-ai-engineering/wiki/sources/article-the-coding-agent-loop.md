---
type: source
title: The Bare-Bones Coding Agent Loop
description: A build log for Decode, a Pydantic-AI coding agent at feature parity with the Pi harness, walking through its uncapped ReAct loop, minimal 9-tool set, provider-agnostic LLM backend, and terminal steering model.
origin: article
original_path: https://www.decodingai.com/p/the-coding-agent-loop
source_url: https://www.decodingai.com/p/the-coding-agent-loop
authors: ["Paul Iusztin"]
published_date: "2026-07-28T13:54:35+00:00"
raw_file: raw/article-the-coding-agent-loop.md
created: 2026-08-31T18:40:46Z
timestamp: 2026-08-31T18:40:46Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/pi-agent]]"
  - "[[wiki/entities/mario-zechner]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/openrouter]]"
  - "[[wiki/entities/opik]]"
  - "[[wiki/entities/pydantic-ai]]"
  - "[[wiki/entities/opencode]]"
concepts:
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-memory]]"
---

# The Bare-Bones Coding Agent Loop

> [[raw/article-the-coding-agent-loop|Raw]] · article

## Summary

Lesson 2 of Paul Iusztin's course *Building a Coding Agent From Scratch*
builds Decode, a Pydantic-AI coding-agent harness aimed at feature parity
with Mario Zechner's minimalist [[wiki/entities/pi-agent]] harness. The frame
carried from Lesson 1: an agent is the ReAct loop — reason, pick a tool,
observe — and the harness around that loop, not the model, is what makes a
coding agent good. [[raw/article-the-coding-agent-loop#One Turn, End to End|cite]]

It walks the loop end to end: an `AgentTurnHandler` async generator chaining
model steps with no max-steps cap, provider construction swapping between
Modal, OpenRouter and Gemini behind one function, a nine-tool set built
around Pi's original four (`read`, `write`, `edit`, `bash`), Opik/OTLP
tracing through Pydantic AI's Logfire integration, and a terminal UI that
buffers keystrokes into two queues (steering vs. follow-up) so input is only
injected at defined loop boundaries. [[raw/article-the-coding-agent-loop#The Agent Loop|cite]]

It closes by naming what this "bare-bones" lesson deliberately skips —
headless mode, memory, compaction, skills, sandboxing — as later lessons'
territory. [[raw/article-the-coding-agent-loop#Next Steps|cite]]

## Key claims

- `AgentTurnHandler.__call__` is a `while True` async generator with two
  yield points, `Boundary.MODEL_REQUEST` and `Boundary.WOULD_STOP`, and no
  max-step cap — the model signals completion by returning text instead of a
  tool call. [[raw/article-the-coding-agent-loop#The Agent Loop|cite]]
- Decode's tool set is `read`, `write`, `edit`, `bash` (Pi's original four)
  plus `glob`, `grep`, `todo_write`, `web_fetch`, `ask_user` — kept small
  because every tool's schema is appended to the system prompt. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- One `_build_model()` function selects Gemini (buy the model), OpenRouter
  (buy the serving) or Modal (serve it yourself); Modal is the default,
  chosen after napkin math putting a 1,000-document batch job at ~$13 on
  Modal vs. ~$97 on Sonnet. [[raw/article-the-coding-agent-loop#The LLM Providers|cite]]
- The TUI follows append-to-scrollback (Claude Code, Codex, Pi) rather than
  full-screen (Amp, OpenCode), buffering input into `steering` and
  `follow_up` asyncio queues that drain only at the two loop boundaries.
  [[raw/article-the-coding-agent-loop#The TUI and the Queues|cite]]
- Session state is an append-only JSONL log under `.decode/sessions/`,
  resumable via `decode --resume <session_id>` — the article says this is
  how Claude Code does session management, replacing a database.
  [[raw/article-the-coding-agent-loop#The Session Log|cite]]

## Notable quotes

> "The loop has no max-steps knob, based on Pi's principles: 'the loop just
> loops until the agent says it's done.' A cap is a guess about how many
> steps a task needs, and the model already signals completion by returning
> text instead of a tool call."
> — [[raw/article-the-coding-agent-loop#The Agent Loop|location]]

> "Pi doesn't have a todo_write tool because it considers that the best way
> to store your plan is directly in a Markdown file, not in an in-memory TODO
> list — a PLAN.md on disk beats an in-memory list."
> — [[raw/article-the-coding-agent-loop#The Core Tools|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/pi-agent]],
  [[wiki/entities/mario-zechner]], [[wiki/entities/modal]],
  [[wiki/entities/openrouter]], [[wiki/entities/opik]],
  [[wiki/entities/pydantic-ai]], [[wiki/entities/opencode]]
- **Concepts**: [[wiki/concepts/orchestration]], [[wiki/concepts/cli]],
  [[wiki/concepts/agent-memory]]

> Synthesis: A code-level account of one harness's loop, tools and TUI — the
> concrete implementation the wiki's more abstract MCP/skills sources argue
> around; this is Lesson 1's architecture executed.
