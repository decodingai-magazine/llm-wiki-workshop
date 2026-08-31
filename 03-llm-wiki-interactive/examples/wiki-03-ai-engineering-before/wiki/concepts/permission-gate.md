---
type: concept
title: Permission Gate
description: The policy layer in a coding-agent harness that decides, per tool call, whether execution proceeds automatically, is denied, or is escalated to a human — modeled in Decode on Claude Code's approval modes.
aliases:
  - PermissionGate
sources:
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/sandboxing]]"
  - "[[wiki/concepts/agent-loop]]"
created: 2026-08-29T17:09:11Z
timestamp: 2026-08-29T17:09:11Z
source_count: 2
---

# Permission Gate

> A policy layer that decides, for every tool call a model emits, whether it runs automatically, is refused, or is put in front of a human.

## Definition

The system-design article frames the permission gate at the concept level: an ask/allow/deny policy per tool call, one of six modules composing "the harness" (alongside LLM providers, sandbox, memory, skills, and an LSP server), explicitly modeled on Claude Code's default/edit/auto approval modes. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

The repo's architecture page shows the concrete mechanism behind that framing, in Decode's `permissions/` package (`gate.py` policy, `rules.py` glob matching, `types.py` for modes and tool kinds). Every tool call carries a `ToolKind`: read-only kinds (read, glob, grep, lsp, web_fetch, todo_write, agent) auto-allow unconditionally; file-edit and other kinds run a fixed precedence — deny rules from every source, then allow rules from every source (user `settings.json` union agent frontmatter), then a mode × kind matrix. In that matrix, `bypass` mode allows everything, `plan` mode denies and forces `exit_plan_mode`, `edit` mode allows file edits, and `default` mode asks a human. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Tension: the repo names four permission modes (`bypass`, `plan`, `edit`, `default`); the article's gloss, when comparing to Claude Code, names three (`default`, `edit`, `auto`). `auto` in the article likely corresponds to `bypass` in the code, but neither source page maps the two vocabularies onto each other explicitly, and the article does not mention a `plan`-mode analogue at all.

## Key claims

- The gate is policy only and never prompts directly: an ASK verdict travels up to a human resolver (the TUI, in the interactive case), and an "approve forever" answer persists a rule into `.decode/settings.json`. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Precedence is deny-first: deny rules from every source outrank allow rules from every source, which outrank the mode × kind matrix, which is the fallback before asking a human. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- A gated call does not block the agent loop while awaiting a decision: pydantic-ai's `output_type=[str, DeferredToolRequests]` lets a turn suspend with the pending call packaged as a `DeferredToolRequests` value, which is what makes both the permission prompt and mid-turn steering possible without a blocking wait. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- In the turn sequence, the turn handler calls `PermissionGate.check(kind, subject, mode)` once the model returns a deferred tool request, and the ALLOW/DENY/ASK verdict determines whether the tool executes, is refused, or is routed to a human resolver before the leg resumes. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Permissions are named as one of the harness's six core modules, and the ask/allow/deny scheme is explicitly credited to Claude Code's default/edit/auto modes as its model. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **Agent harness**: the permission gate is one of the modules composing "the harness" — the layer the course's thesis says actually differentiates a coding agent, as distinct from the ~20-line agent loop itself. [[wiki/concepts/agent-harness]]
- **Sandboxing**: an ALLOW verdict from the gate is what lets a tool call reach the sandbox seam (none/docker/modal); the gate decides *whether* a command runs, the sandbox decides *where*. [[wiki/concepts/sandboxing]]
- **Agent loop**: `DeferredToolRequests` is the suspend/resume mechanism the gate depends on to pause a turn for a human decision without blocking, the same mechanism the steering queue relies on for mid-turn input. [[wiki/concepts/agent-loop]]

> Synthesis: the two sources are not fully independent witnesses — the article is the companion write-up for the same course whose codebase the ARCHITECTURE page documents, both tracing to the same author/project, so their agreement that the scheme is "modeled on Claude Code" is one voice describing one system twice rather than two separate confirmations. Only the ARCHITECTURE page shows the actual mechanism — rule precedence, `ToolKind` dispatch, and the `DeferredToolRequests` suspend path — that the article's concept-level gloss leaves unexamined.
