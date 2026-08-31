---
type: entity
title: Kitaru
description: ZenML's durable-execution runtime that backs decode's headless remote mode, orchestrating checkpointed, replayable agent flows in parallel on Modal.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[tool-call-routing-to-the-permission-gate]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/modal]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]"
created: 2026-08-29T17:08:33Z
timestamp: 2026-08-31T14:36:07Z
source_count: 3
---

# Kitaru

> ZenML's durable-execution runtime; in `decode` it orchestrates the headless remote mode, wrapping the same agent construction in checkpointed, replayable flows, and its pydantic-ai adapter supplies the durable waits that headless human-in-the-loop approval depends on.

## Definition

All three sources agree on what Kitaru is and does. The article names it explicitly as "ZenML's agent runtime"; the repo pages never spell out the ZenML attribution but describe the identical mechanics under `runtime/`'s "Kitaru durable flow." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] Kitaru is the durable-execution runtime behind decode's "remote mode": instead of one interactive TUI session, `decode run "<task>"` wraps the same headless agent build in a Kitaru `@flow`, checkpointing every model and tool call so a crash resumes from cache rather than restarting. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The routing note adds a second facet: Kitaru is also a pydantic-ai integration — `kitaru.adapters.pydantic_ai`'s `KitaruAgent` wraps the same `Agent` and intercepts pydantic-ai's `ApprovalRequired`/`DeferredToolRequests` primitive itself, rather than decode's own gate resolving it. [[tool-call-routing-to-the-permission-gate]]

## Key claims

- In remote mode, Kitaru runs N headless harnesses in parallel on Modal, records each run's progress step by step so a dying sandbox resumes instead of restarting, freezes at human-input questions with no compute burned while waiting, and lets a finished run be replayed with one variable changed (model, prompt) against the original as baseline. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Concretely, `decode run "<task>"` wraps the same `build_agent()` factory the TUI uses in a Kitaru `@flow`, checkpointing every model and tool call; `--hitl` swaps in a second flow whose gated tools pause on durable waits that an operator resolves out of band. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `model` and `repo` are flow inputs, so `decode replay <exec_id> --model <other>` re-executes a recorded run from a chosen anchor with the model swapped — the stated reason the course gives for having a durable runtime at all. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- decode's `src/decode/runtime/` module holds both the Kitaru durable flows and the Modal orchestrator app pin, making Kitaru-on-Modal one of the two interface modes (with the TUI) built over one shared headless harness core. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `wait_for_input(question=..., name=..., schema=str, timeout=settings.runtime_wait_timeout_s)` is a named, flow-scope durable wait with an explicit timeout — distinct from an in-memory `asyncio.Future` in that it can outlive the process; decode's `flow_resolve_user_question` calls it to resolve `ask_user`/`exit_plan_mode` under `--hitl`. [[tool-call-routing-to-the-permission-gate]]
- For `write`/`edit`/`bash` approvals under `--hitl`, the `KitaruAgent` wrapper intercepts `ApprovalRequired` natively rather than letting decode's own gate/resolver handle it: decode opts those tools out of Kitaru's default per-call checkpoint via `checkpoint_strategy="calls"`, which hoists the approval wait to flow scope instead. Decode's own `PermissionGate` resolver in this path is only a deny "safety-net," per that code's own docstring. [[tool-call-routing-to-the-permission-gate]]
- A paused headless run is resolved from a separate terminal, out of band: `kitaru executions input <exec_id> --wait <name> --value '<answer>'` followed by `kitaru executions resume <exec_id>`; decode's CLI treats the pause itself as a normal exit-0 outcome and just prints this recipe. [[tool-call-routing-to-the-permission-gate]]
- Caveat on that last group of claims: the note's author did not open the `kitaru.adapters.pydantic_ai` package itself — its `_toolset` module and the shape of its own durable approval checkpoint are inferred from decode's docstrings and call sites, not read directly. [[tool-call-routing-to-the-permission-gate]]

## Relationships

- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/modal]]**: Kitaru is the orchestration layer that runs N headless harnesses in parallel on Modal's compute — Kitaru schedules, checkpoints and replays; Modal executes. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **[[wiki/concepts/durable-execution]]**: Kitaru is decode's concrete instance of durable execution — step-recorded, resumable, replayable flows, including flow-scope waits with explicit timeouts — distinct from the sandboxing and permission concerns the rest of the harness owns. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[tool-call-routing-to-the-permission-gate]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]**: Kitaru wraps, rather than replaces, the same headless harness core the TUI drives — both interface modes build the identical `Agent` object through one factory. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]**: under headless `--hitl`, Kitaru's own pydantic-ai adapter bypasses decode's `PermissionGate`/`DecisionChannel` machinery for tool approvals — it is a structurally different waiting room from the TUI's in-process `asyncio.Future`, not a durable version of the same mechanism. [[tool-call-routing-to-the-permission-gate]]

> Synthesis: all three sources trace back to the same author and project — the article and both repo notes are the decode course's own account of its own runtime — so this page is one voice at three depths (product pitch, architecture skim, code-level trace), not independent corroboration. The routing note is also the most epistemically hedged of the three: its claims about the Kitaru adapter's internal behavior are inferred from decode's usage and docstrings, since the adapter package itself was never opened.
