---
type: source
title: The Bare-Bones Coding Agent Loop
description: A build log for Decode, a from-scratch Pydantic AI coding agent, arguing the harness — not the model — is what makes a coding agent good, and walking through its ReAct loop, 9-tool set, swappable LLM providers, and terminal steering queues.
origin: article
original_path: https://www.decodingai.com/p/the-coding-agent-loop
source_url: https://www.decodingai.com/p/the-coding-agent-loop
authors:
  - Paul Iusztin
published_date: 2026-07-28T13:54:35+00:00
raw_file: raw/article-the-coding-agent-loop.md
created: 2026-08-29T17:03:54Z
timestamp: 2026-08-29T17:03:54Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/pi]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/opik]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-loop]]"
---

# The Bare-Bones Coding Agent Loop

> [[raw/article-the-coding-agent-loop|Raw]] · article · [decodingai.com](https://www.decodingai.com/p/the-coding-agent-loop)

## Summary

Lesson 2 of the open-source course *Building a Coding Agent From Scratch*, this article builds Decode: a bare-bones coding agent in Python on top of Pydantic AI, deliberately scoped to reach feature parity with Mario Zechner's minimalist Pi harness before later lessons add Claude-Code/OpenCode-style features such as memory, skills and sandboxing. Its opening claim — from a LangChain Terminal-Bench experiment where swapping only the harness under a fixed model moved a coding agent from ~30th place to the top 5 — sets the piece's thesis: the harness, not the model, is what makes a coding agent good.

It then walks one turn end-to-end. An `AgentTurnHandler` async generator chains model-call "steps" through `agent.iter`, exposing exactly two yield points — `Boundary.MODEL_REQUEST` for steering and `Boundary.WOULD_STOP` for follow-ups — and deliberately carries no max-step cap, trusting the model's own text-instead-of-tool-call signal that it is done. Nine tools cover the lifecycle plan (`todo_write`) → explore (`read`/`glob`/`grep`) → apply (`write`/`edit`, gated behind an approval prompt) → execute (`bash`), with `web_fetch` and `ask_user` rounding out the set; Pi's 4-tool minimalism (`read`, `write`, `edit`, `bash`) is the recurring philosophical counterpoint.

The rest covers infrastructure made explicit as trade-offs rather than defaults: three swappable LLM providers (Modal, OpenRouter, Gemini) behind one `_build_model()` switch, framed as buy-the-model vs. buy-the-serving vs. serve-it-yourself; Opik/OTLP tracing wired in from day one to make the loop debuggable; and a TUI that buffers keystrokes into separate steering/follow-up queues so mid-turn input never corrupts a running tool call, with session state persisted as an append-only per-session JSONL log instead of a database.

## Key claims

- Changing only the harness on the same model moved a coding agent from ~30th place to the top 5 on LangChain's Terminal-Bench, which the article treats as proof that the harness — not the model — is the real lever. [[raw/article-the-coding-agent-loop#The Bare-Bones Coding Agent Loop|cite]]
- The turn lifecycle is plan → explore → apply → execute → observe, mapped onto tools as `todo_write` (plan), `read`/`glob`/`grep` (explore), `write`/`edit` (apply, stopping for a human verdict), and `bash` (execute), with a failure or exit code feeding the next pass as the observation. [[raw/article-the-coding-agent-loop#The Agent Loop|cite]]
- The loop has no max-steps knob by design, following Pi's principle that it should just loop until the agent says it's done; a step cap is a guess, and the signal actually worth watching is the context window. [[raw/article-the-coding-agent-loop#The Agent Loop|cite]]
- All provider knowledge is isolated in one `_build_model()` function selected by an `LLM_PROVIDER` env var, covering three build-vs-buy tiers — Gemini (buy the model), OpenRouter (buy the serving), Modal (serve open weights yourself) — with Modal as the default because it bills GPU-time instead of tokens and scales to zero. [[raw/article-the-coding-agent-loop#The LLM Providers|cite]]
- Pi ships exactly `read`, `write`, `edit`, and `bash` in under 1,000 tokens of prompt plus definitions and still lands top-10 on Terminal-Bench 2.0, which matters because Pydantic AI adds every registered tool's schema to the system prompt, so each extra tool has a real context-window cost. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- The TUI buffers keystrokes into two queues — steering (plain Enter, drained before each model call) and follow-up (Alt+Enter, drained only once a turn would stop) — plus a cooperative Esc-abort that clears both, because injecting text mid-tool-call would corrupt the running turn. [[raw/article-the-coding-agent-loop#The TUI and the Queues|cite]]

## Notable quotes

> "In LangChain's Terminal-Bench experiment, changing only the harness (with the same model) moved a coding agent from ~30th place into the top 5: the harness, not the model, is what makes a coding agent good."
> — [[raw/article-the-coding-agent-loop#The Bare-Bones Coding Agent Loop|location]]

> "In reality, the tools are 90% of why this is a coding agent and not any other kind of AI agent."
> — [[raw/article-the-coding-agent-loop#The Core Tools|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/pi]], [[wiki/entities/modal]], [[wiki/entities/opik]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/cli]], [[wiki/concepts/agent-loop]]

> Synthesis: A hands-on build log, not a theory piece — its wiki value is a concrete, code-level reference implementation of the ReAct coding-agent loop (steering boundaries, tool-count-as-context-cost, provider abstraction) that other sources on agent harnesses and CLIs can be checked against rather than restated.
