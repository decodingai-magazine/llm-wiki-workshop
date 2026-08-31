---
type: question
title: in the coding agent repo, how does the agent spawn a subagent, and what does the parent actually get back when it finishes?
description: ARCHITECTURE.md sketches the fan-out shape; went to the code for _spawn_child's own body — narrowing, truncation, and error handling.
asked_on: 2026-08-31
created: 2026-08-31T14:44:23Z
timestamp: 2026-08-31T14:45:35Z
answer_doc: "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
sources_cited:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
  - "[[wiki/concepts/subagents]]"
---

# in the coding agent repo, how does the agent spawn a subagent, and what does the parent actually get back when it finishes?

> Asked on 2026-08-31 · answered against the clone @ `6ee643f` · repo note written, ingest tail run

## Answer

Full answer: [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back|How a subagent is spawned and what the parent gets back]]

- Spawn is a direct nested `Agent.run()`, same installed Agent.
- Child gets a fresh, bypass-mode `PermissionGate` — not a flag flip.
- Deny resolvers are an unreached safety net under bypass.
- One retry on a bad report; exceptions never leave `_spawn_child`.
- Result is truncated to a byte budget, snapped to a line boundary.
- Parent gets one folded string back — no synthesis LLM call.

## Why this matters

`ARCHITECTURE.md`'s fan-out section shows the caller's fold logic but not `_spawn_child`'s own body — the narrowing, truncation and error handling that decide whether one bad child can sink the whole fan-out.
