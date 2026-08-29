---
type: repo_note
title: How a tool call reaches the permission gate, and what happens while it waits
description: The route is a deliberate pause — a gated tool raises before doing anything, the run resolves to a deferred request, and the loop resumes it with an allow or a typed denial.
original_path: github://decodingai-magazine/building-a-coding-agent-from-scratch-course#tool-call-to-permission-gate-routing
repo: "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
commit_sha: 6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea
question: "in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?"
spawned_by_question: "[[wiki/questions/2026-08-29-how-a-tool-call-reaches-the-permission-gate]]"
created: 2026-08-29T11:35:00Z
timestamp: 2026-08-29T11:35:00Z
entities: []
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
---

# How a tool call reaches the permission gate, and what happens while it waits

> Answers [[wiki/questions/2026-08-29-how-a-tool-call-reaches-the-permission-gate]] against `decode` @ `6ee643f`

## Answer

The routing is not a call into the gate. **The tool refuses to run**, and the pause
that creates is what carries the call to the gate.

Every gated tool opens its body with the same guard — `if needs_approval(ctx): raise
ApprovalRequired` — before touching a path, a process or the network. Nothing has
happened yet when the exception is raised, which is what makes the pause safe to
resume later.

That exception does not propagate to the user. The agent's output type includes
`DeferredToolRequests`, so the framework collects the paused calls and ends the run
leg with them as the *output*. The loop notices, resolves each one, and starts a
**resume leg** with the answers attached — the same turn, one more model round.

Resolution walks three levels, in order:

1. **The predicate** decides whether this call defers at all. It returns `False`
   when the call is already approved (the resume leg) or the gate is in bypass, so
   headless runs execute inline; under the headless human-in-the-loop posture it
   applies a read-only floor itself, letting read-only tools run and deferring only
   mutating ones into a durable wait.
2. **The gate** evaluates policy — deny rule, allow rule, mode, otherwise ask. An
   allow returns immediately with no prompt; a deny returns its reason as a string.
3. **The human**, only on `ASK`. The loop emits a `PermissionRequested` event so the
   UI can render the request, then awaits a resolver injected on the deps object.
   That await *is* the wait: the turn is suspended inside the resolution step, no
   tool has started, and the model is not in the loop.

The resume is typed. An allow becomes `True`; a denial becomes `ToolDenied(reason)`,
so on the next leg the **model sees why it was refused** and can adapt instead of
retrying blindly. Plan mode uses exactly this path: its denial reason tells the
model to present its plan and call `exit_plan_mode`.

Three consequences worth keeping:

- **Nothing partial is possible.** The tool raised before doing any work, so a
  denial leaves no half-written file and no started process.
- **The wait has no timeout in the interactive path.** It is an `await` on a
  resolver the UI completes; in the headless durable posture the same pause becomes
  a checkpointed wait that survives a process restart.
- **The gate never prompts.** It is policy only; the prompting belongs to whoever
  owns the interaction surface — which is what lets the same gate serve a terminal
  session and an unattended run.

## Evidence

- `src/decode/tools/approval.py:20` — `needs_approval`: the single predicate; returns `False` when already approved or in bypass, applies the read-only floor under headless HITL ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/approval.py#L20-L48))
- `src/decode/tools/files.py:191` — a gated tool raising `ApprovalRequired` as its first act ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/files.py#L185-L191))
- `src/decode/agent/loop.py:182` — the leg ends with `DeferredToolRequests` as its output; the loop stores the resolved results and re-enters ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/agent/loop.py#L152-L186))
- `src/decode/agent/loop.py:429` — `_resolve_deferred`: allow → `True`, deny → `ToolDenied(reason)`, then `build_results` ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/agent/loop.py#L429-L443))
- `src/decode/agent/loop.py:445` — `_decide`: builds the request with the tool's kind and subject, asks the gate, and only escalates on `ASK` ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/agent/loop.py#L445-L467))
- `src/decode/agent/loop.py:470` — `_ask_human`: emits `PermissionRequested`, awaits the injected resolver ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/agent/loop.py#L470-L489))
- `src/decode/permissions/gate.py:66` — `PermissionGate.check`: policy only, never prompts ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/permissions/gate.py#L66))

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/durable-execution]], [[wiki/concepts/agentic-coding-loop]]

> Synthesis: The design worth stealing is that approval is expressed as a **refusal to start** rather than as a check before acting — which is what makes the same mechanism serve an interactive prompt and a durable, restartable wait without either path knowing about the other.
