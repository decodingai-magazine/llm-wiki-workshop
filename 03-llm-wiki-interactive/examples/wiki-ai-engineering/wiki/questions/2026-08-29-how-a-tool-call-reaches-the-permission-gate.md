---
type: question
title: "In the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?"
description: The architecture page covers the gate's policy but not the routing, so the answer came from the code.
asked_on: 2026-08-29
created: 2026-08-29T11:35:00Z
timestamp: 2026-08-29T11:35:00Z
answer_doc: "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-to-permission-gate-routing]]"
sources_cited:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
---

# In the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?

> Asked on 2026-08-29 · `ARCHITECTURE.md` covered the policy, not the routing · answered from the code

## Answer

Full answer: [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-to-permission-gate-routing|How a tool call reaches the permission gate]]

- The tool raises before doing any work — the pause is the routing
- The run leg ends with the paused calls as its output
- Predicate → gate policy → human, in that order
- The resume is typed: allow, or a denial the model can read
- The same pause becomes a durable wait when headless

## Why this matters

It is the difference between "the gate exists" and knowing that a denial can never leave a half-written file.
