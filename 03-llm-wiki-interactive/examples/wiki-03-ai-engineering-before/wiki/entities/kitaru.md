---
type: entity
title: Kitaru
description: ZenML's durable-execution runtime that backs decode's headless remote mode, orchestrating checkpointed, replayable agent flows in parallel on Modal.
aliases: []
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-29T17:08:33Z
timestamp: 2026-08-29T17:08:33Z
source_count: 2
---

# Kitaru

> ZenML's durable-execution runtime; in `decode` it orchestrates the headless remote mode, wrapping the same agent construction in checkpointed, replayable flows.

## Definition

Both sources agree on what Kitaru is and does. The article names it explicitly as "ZenML's agent runtime"; the repo page never spells out the ZenML attribution but describes the identical mechanics under `runtime/`'s "Kitaru durable flow." [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] Kitaru is the durable-execution runtime behind decode's "remote mode": instead of one interactive TUI session, `decode run "<task>"` wraps the same headless agent build in a Kitaru `@flow`, checkpointing every model and tool call so a crash resumes from cache rather than restarting. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- In remote mode, Kitaru runs N headless harnesses in parallel on Modal, records each run's progress step by step so a dying sandbox resumes instead of restarting, freezes at human-input questions with no compute burned while waiting, and lets a finished run be replayed with one variable changed (model, prompt) against the original as baseline. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Concretely, `decode run "<task>"` wraps the same `build_agent()` factory the TUI uses in a Kitaru `@flow`, checkpointing every model and tool call; `--hitl` swaps in a second flow whose gated tools pause on durable waits that an operator resolves out of band. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `model` and `repo` are flow inputs, so `decode replay <exec_id> --model <other>` re-executes a recorded run from a chosen anchor with the model swapped — the stated reason the course gives for having a durable runtime at all. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- decode's `src/decode/runtime/` module holds both the Kitaru durable flows and the Modal orchestrator app pin, making Kitaru-on-Modal one of the two interface modes (with the TUI) built over one shared headless harness core. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/entities/modal]]**: Kitaru is the orchestration layer that runs N headless harnesses in parallel on Modal's compute — Kitaru schedules, checkpoints and replays; Modal executes. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- **[[wiki/concepts/durable-execution]]**: Kitaru is decode's concrete instance of durable execution — step-recorded, resumable, replayable flows — distinct from the sandboxing and permission concerns the rest of the harness owns. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/agent-harness]]**: Kitaru wraps, rather than replaces, the same headless harness core the TUI drives — both interface modes build the identical `Agent` object through one factory. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: the two sources are one voice at two zoom levels, not independent corroboration — the article (by the course's own author) gives Kitaru's user-facing behavior (parallelism, freeze-on-input, replay-with-a-changed-variable), and the repo page it describes supplies the mechanism (`@flow`, `--hitl`, flow inputs) that makes those behaviors true.
