---
type: concept
title: Subagents
description: A pattern where a parent agent spawns narrowed, single-use child agent runs to fan work out concurrently and folds their reports back as plain text with no separate synthesis call.
aliases: []
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
related:
  - "[[wiki/concepts/agent-loop]]"
  - "[[wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T14:47:59Z
timestamp: 2026-08-31T14:47:59Z
source_count: 2
---

# Subagents

> A single `agent` tool call fans a prompt out to N read-only child agent runs and folds their truncated reports back as one string — no dedicated synthesis LLM call.

## Definition

In the `decode` coding-agent codebase, subagents are not a separate agent type or entry point: the `agent` tool spawns N read-only "Explore" children concurrently, each a nested `Agent.run()` on the *same installed* Agent object used by the parent, with narrowed dependencies. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The child shares the parent's model and HTTP client rather than getting its own, and its toolset is collapsed to read/glob/grep/lsp so recursion (a child spawning further children) is structurally impossible. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]

## Key claims

- Fan-out width is capped at 6 prompts and concurrency is capped separately by a semaphore. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Each child gets a brand-new `PermissionGate(mode=BYPASS)` instance (not a flag flip on the parent's gate), plus two async "deny resolvers" that unconditionally deny any permission or user-question request as a safety net behind bypass mode, since an unattended child has no human to answer one. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- A child's "silent event sink" checks the parent's verbose flag at emit time, not spawn time, so toggling verbosity mid-fan-out changes visibility of the next event; a `task_store` is omitted from child deps so nothing a child does touches the parent's task list. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- A result is treated as BAD if it's a deferred tool request, empty text, or shows zero tool calls in the transcript; a BAD result triggers exactly one re-spawn with a nudge appended, and a second BAD result gives up rather than retrying again. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- Exceptions from a child are swallowed inside its own spawn coroutine, so one broken child cannot abort its siblings or the parent's `asyncio.gather`. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- The byte budget for reports is shared across children (`max_bytes // N`), so a wider fan-out doesn't cost the parent more context; each child's report is truncated to a line boundary, and there is no separate synthesis LLM call — reports are concatenated under labelled headings with a footer instructing the parent model to synthesize them itself on its next turn. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]

## Relationships

- **Agent loop**: the child is not a second loop — it's the same installed `Agent`, re-entered via a nested `run()` that bypasses `decode`'s own harness loop entirely. [[wiki/concepts/agent-loop]]
- **Permission gate**: the child's bypass gate is a fresh, separately-scoped `PermissionGate` object, distinct from the parent's gate rather than a mode toggle on it. [[wiki/concepts/permission-gate]]
- **Agent harness**: subagent fan-out is one tool (`agent`) among the harness's flat tool list, sitting behind the same gate/sandbox seams as any other tool. [[wiki/concepts/agent-harness]]

> Synthesis: both sources trace to the same codebase (`decode`) and the same underlying mechanism — ARCHITECTURE.md names the fan-out pattern at a summary level, and the spawn-mechanics note walks the same `agent.py` call chain in code-level detail — so this is one project's design described at two altitudes, not independent corroboration of a general "subagents" pattern.
