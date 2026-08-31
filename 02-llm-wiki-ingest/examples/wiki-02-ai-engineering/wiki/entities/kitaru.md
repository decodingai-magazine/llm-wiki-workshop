---
type: entity
title: Kitaru
description: ZenML's agent runtime — the control-plane orchestrator behind Decode's headless/remote execution mode, giving it durability and replay.
aliases: []
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
related:
  - "[[wiki/entities/decode]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/pydantic-ai]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T20:05:00Z
timestamp: 2026-08-31T20:05:00Z
source_count: 2
---

# Kitaru

> ZenML's agent runtime, used as the control plane for Decode's headless/remote execution.

## Definition

Kitaru is ZenML's agent runtime. In Decode's architecture it forms the control plane of a three-plane split for remote execution — control plane (Kitaru on GCP), execution (Python locally / Modal remotely), sandbox (Docker locally / Modal remotely) — which is what gives the headless harness durability (resuming from the last recorded step after a sandbox dies) and replay (rerunning a finished trace with one variable changed, checked against the original run as baseline). [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

Concretely, this surfaces in the codebase as the "Kitaru Durable Flow" that backs `decode run` and `decode replay`, living in `src/decode/runtime/` alongside the Modal deploy app. The repo treats it as opt-in weight rather than a baseline dependency: `kitaru` is imported lazily inside the `run`/`replay` commands, so interactive TUI sessions (`DECODE_ENV=local`) never load it. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- Decode has two ways to run: an interactive TUI, and a remote mode orchestrated by Kitaru. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- `decode run` executes one task headlessly through a Kitaru Durable Flow, either in bypass mode or with `--hitl` for human-in-the-loop gating on tool calls; `decode replay` re-executes a recorded run from a checkpoint with a swapped model. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The three-plane split (control / execution / sandbox) is what gives durability and replay their mechanism: durability comes from resuming at the last recorded step, replay from rerunning a trace with one variable changed against the original as baseline. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Kitaru is imported lazily, only inside the `run`/`replay` code paths, so a local-mode REPL session pays no cost for it. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **Decode**: Kitaru is the durable runtime Decode's headless/remote mode is built on — the mechanism behind `decode run` and `decode replay`. [[wiki/entities/decode]]
- **Modal**: Kitaru is the control plane (on GCP); Modal is the remote execution and sandbox layer it can dispatch to — a division of labor between orchestration and compute. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **Orchestration**: Kitaru is this wiki's one concrete example of durable, replayable agent orchestration, as opposed to the in-process steering/follow-up queue used for the interactive TUI turn. [[wiki/concepts/orchestration]]

> Synthesis: the article names and defines Kitaru ("ZenML's agent runtime") while the repo page only shows it in use (`Kitaru Durable Flow`, lazy import, `run`/`replay`) — but the article is Lesson 1 prose for the same course the repo *is* the code of, both from the same author, so this is one voice describing one system from two angles, not two independent confirmations of what Kitaru is.
