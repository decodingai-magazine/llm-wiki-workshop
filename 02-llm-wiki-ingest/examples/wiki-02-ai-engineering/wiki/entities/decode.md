---
type: entity
title: Decode
description: A terminal coding agent — a Pydantic AI tool-calling loop wrapped in a permissions/sandboxing/memory/compaction/subagent-fan-out harness — built lesson-by-lesson in Paul Iusztin's open-source course "Building a Coding Agent From Scratch."
aliases: []
sources:
  - "[[wiki/sources/article-run-coding-agents-safely]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/sandboxing]]"
  - "[[wiki/concepts/context-engineering]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/compaction]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/entities/pydantic-ai]]"
  - "[[wiki/entities/kitaru]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/docker]]"
created: 2026-08-31T19:00:00Z
timestamp: 2026-08-31T20:15:00Z
source_count: 3
---

# Decode

> A Pydantic AI tool-calling loop wrapped in a harness — permissions, sandboxing, memory, compaction, subagent fan-out, Kitaru durability — built lesson-by-lesson in the course "Building a Coding Agent From Scratch."

## Definition

Decode is the coding agent built incrementally across Paul Iusztin's open-source
course *Building a Coding Agent From Scratch*: two lesson articles (lesson 3 on
sandboxing, lesson 4 on context engineering) and the course repository itself,
read directly and pinned to a commit. All three sources trace to the same
course and author — the repo page is a more primary source (the shipped code)
than the articles' narrative account, but this is still one project described
three ways, not independent corroboration.
[[wiki/sources/article-run-coding-agents-safely]],
[[wiki/sources/article-context-engineering-for-coding-agents]],
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

At its pinned commit, Decode is a single Pydantic AI `Agent` — a ~20-line
model-calling loop per its README — wrapped in a much larger harness: tool
permissions, sandboxing, memory, compaction, a durable headless runtime, and
subagent fan-out. Two front ends, an interactive TUI and a headless
Kitaru-backed runtime (`decode run`/`decode replay`), drive the same
`build_agent()`.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- Every computer-use tool call (`bash`, `read`, `write`, `edit`) routes through
  a `CommandExecutor`/`SandboxExecutor` seam over a `none`/`docker`/`modal`
  backend (`SANDBOX_MODE`), each backend fresh-exec (a new process per
  command, so `cd`/`export` never persist) — so the agent loop never knows
  where a command actually runs; Decode avoids Modal cold starts by
  pre-provisioning application-agnostic sandboxes with a repo volume attached
  on demand. [[wiki/sources/article-run-coding-agents-safely]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The `Runner` drives each turn as one or more "legs" through an
  `AgentTurnHandler`: a `MODEL_REQUEST` boundary drains queued steering text
  into the prompt, a `WOULD_STOP` boundary drains follow-up text or ends the
  turn, and a gated tool call pauses the leg for the `PermissionGate` before
  resuming.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Memory splits hand-written `AGENTS.md` (under 300 lines) and auto-extracted
  `.decode/MEMORY.md` (one LLM call per session-end, capped at 200
  lines/25,000 bytes, assembled root-most to cwd-most).
  [[wiki/sources/article-context-engineering-for-coding-agents]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Skills load through 3 progressive-disclosure tiers (catalog line →
  `SKILL.md` body on invocation → bundled files on demand); a `ty`-based LSP
  server feeds both an on-demand `lsp` tool and a passive Diagnostics
  Enricher on every Python write/edit.
  [[wiki/sources/article-context-engineering-for-coding-agents]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Compaction cascades in two automatic tiers at every `WOULD_STOP` — no-LLM
  microcompaction (elides stale tool outputs past a lower reserve) and full
  LLM compaction (`[summary, *tail]` past a higher reserve), sized off the
  *last* response's own token usage — plus a manual `/clear` after a memory
  write-back. [[wiki/sources/article-context-engineering-for-coding-agents]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The `agent` tool fans out up to 6 concurrent read-only Explore subagents,
  each re-entering the same installed Agent with narrowed deps;
  under-specified prompts (<8 words) are rejected before spawning, and a bad
  report gets exactly one re-spawn.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The repo's tool registry (files, bash, web, LSP, tasks, `ask_user`, the
  `agent` fan-out tool) lists no MCP client, consistent with lesson 4's claim
  that Decode still deliberately lacks one.
  [[wiki/sources/article-context-engineering-for-coding-agents]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Tensions

- **System-prompt timing.** Lesson 4 says the system prompt is assembled "at
  session start" from four parts; the repo describes instructions as
  assembled "fresh every turn" from the same four parts (base + persona +
  memory + skills catalog). Same components, different cadence — the wiki
  holds both rather than picking one.
  [[wiki/sources/article-context-engineering-for-coding-agents]] vs.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **Auto-mode permissions.** Lesson 4, as of that lesson, says Decode "still
  deliberately lacks... an auto-mode permission layer"; the repo's pinned
  commit has a full `PermissionGate` with `BYPASS`/`PLAN`/`EDIT`/`DEFAULT`
  modes that auto-allow or auto-deny by tool kind. Likely the layer was added
  in a later, not-yet-ingested lesson rather than a real contradiction — but
  the wiki currently holds both claims.
  [[wiki/sources/article-context-engineering-for-coding-agents]] vs.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **Claude Code** / **Codex CLI**: comparison baselines — both already
  sandbox `bash` locally via OS-level jails (Seatbelt/bubblewrap).
  [[wiki/entities/claude-code]]
- **Modal** / **Docker**: Decode's two sandbox backends, alongside a local
  `none` mode. [[wiki/entities/modal]], [[wiki/entities/docker]]
- **Pydantic AI**: the framework Decode's single `Agent` and tool-calling
  loop are built on. [[wiki/entities/pydantic-ai]]
- **Kitaru**: powers Decode's headless durable runtime (`decode run`/`decode
  replay`), lazily imported so interactive REPL sessions don't load it.
  [[wiki/entities/kitaru]]
- **Sandboxing** / **Context engineering** / **Agent harness**: Decode's
  `CommandExecutor` seam and its permissions/memory/skills/compaction/
  subagent stack are this wiki's concrete worked examples of these concepts.
  [[wiki/concepts/sandboxing]], [[wiki/concepts/context-engineering]],
  [[wiki/concepts/agent-harness]]

> Synthesis: Decode is the wiki's only coding agent described at both
> narrative and code level — but all three sources are one course by one
> author, so the repo page corroborates by being a different *kind* of
> artifact (shipped code vs. lesson prose), not a different voice; the two
> tensions above are the visible seam between the lesson-4 snapshot and the
> repo's further-along commit.
