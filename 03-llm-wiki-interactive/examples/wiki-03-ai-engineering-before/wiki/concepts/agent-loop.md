---
type: concept
title: Agent Loop
description: The boundary-yielding turn loop of a coding agent — a ReAct-style plan/explore/apply/execute/observe cycle with no hard-coded step cap, steerable only at two defined checkpoints.
aliases: []
sources:
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/context-compaction]]"
  - "[[wiki/concepts/subagents]]"
created: 2026-08-29T17:08:57Z
timestamp: 2026-08-29T17:08:57Z
source_count: 2
---

# Agent Loop

> One turn is not one model call — it's a generator that yields at two checkpoints and otherwise loops until the model itself signals it's done.

## Definition

Both sources describe the same `decode` codebase's turn loop, at two different zoom levels. The article frames it conceptually as a ReAct cycle — plan (`todo_write`) → explore (`read`/`glob`/`grep`) → apply (`write`/`edit`, gated behind approval) → execute (`bash`) → observe (exit code or output feeds the next pass) — implemented as an `AgentTurnHandler` async generator chaining `agent.iter` steps, exposing exactly two yield points, `Boundary.MODEL_REQUEST` and `Boundary.WOULD_STOP`, with **no max-step cap**: the loop trusts the model's own text-instead-of-tool-call signal that it is finished. [[wiki/sources/article-the-coding-agent-loop]] The repo's architecture page names the same subsystem "the subsystem that makes the codebase what it is" and adds the mechanics underneath it: a `harness.Runner` owns a single-flight phase machine, drives the handler by sending it whatever it drained at each boundary, and the handler in turn talks to a `PermissionGate` and heals a broken history. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: both pages trace to the same course and codebase, so this is one implementation described twice rather than two independent confirmations — but the depth differs by design: the article is the dedicated deep-dive on the loop's *rationale* (ReAct framing, the no-step-cap philosophy, the Pi comparison), while the repo page sketches its *mechanics* as one of several subsystems (phase machine, deferred tool requests, history healing). Read together rather than as duplicate corroboration.

## Key claims

- The turn lifecycle is plan → explore → apply → execute → observe, with no hard-coded step cap by design — a step cap is "a guess," and the signal worth watching instead is the context window. [[wiki/sources/article-the-coding-agent-loop]]
- The handler is an async generator exposing exactly two yield points — `Boundary.MODEL_REQUEST` for steering, `Boundary.WOULD_STOP` for follow-up — confirmed at the code level by a `Runner`/`AgentTurnHandler`/`agent.iter` sequence diagram. [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Steering (plain Enter) folds into the prompt at the next `MODEL_REQUEST`; follow-up (Alt+Enter) is drained only at `WOULD_STOP` and buys one more leg — because injecting text mid-tool-call would corrupt the running turn. [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- A gated tool call doesn't block the loop — it returns a `DeferredToolRequests`, which the handler routes to the permission gate and resumes the same leg with `DeferredToolResults` once resolved; this is what makes both approval prompts and mid-turn steering possible. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The abort flag is checked only at the two boundaries, never mid-stream or mid-tool, so an Esc-abort keeps the history produced so far; a racing second submission is caught because the runner's phase flips to "busy" synchronously before its first `await`. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The handler heals history whose last message carries tool calls with no results — from a crashed or aborted leg — since an unhealed gap would make the underlying framework reject every later prompt and brick the session. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: the loop is the thin core the harness wraps — construction is short by design; everything that makes the agent good (tools, gate, sandbox, memory, skills, compaction) sits outside it. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/permission-gate]]**: the loop never blocks on approval itself — it defers via `DeferredToolRequests` and lets the gate decide, then resumes. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/context-compaction]]**: compaction is checked at the same `WOULD_STOP` boundary the loop already exposes, rather than adding a separate checkpoint. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/subagents]]**: subagent fan-out spawns nested `agent.run()` calls on the same loop machinery with a narrowed toolset, rather than a separate execution path. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
