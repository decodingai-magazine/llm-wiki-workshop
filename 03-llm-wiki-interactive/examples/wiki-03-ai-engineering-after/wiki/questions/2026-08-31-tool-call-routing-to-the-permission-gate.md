---
type: question
title: in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?
description: Went past the architecture page into the code, and found two structurally different waiting rooms behind one policy layer.
asked_on: 2026-08-31
created: 2026-08-31T14:32:06Z
timestamp: 2026-08-31T14:32:06Z
answer_doc: "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-routing-to-the-permission-gate]]"
sources_cited:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/agent-loop]]"
---

# in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?

> Asked on 2026-08-31 · answered against the clone @ `6ee643f` · repo note written, ingest tail run

## Answer

Full answer: [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-routing-to-the-permission-gate|Tool call routing to the permission gate]]

- Every gated tool body raises `ApprovalRequired`.
- pydantic-ai bundles a whole round into one `DeferredToolRequests`.
- `_decide` calls `gate.check()`, once per pending call.
- TUI wait: one ephemeral `asyncio.Future`, nothing persisted.
- The next typed line is captured — Esc denies, it does not abort.
- `--hitl` bypasses that loop for a durable Kitaru wait.

## Why this matters

`ARCHITECTURE.md` presents one permission gate; the code has one policy layer and two unrelated waiting mechanisms behind it.
