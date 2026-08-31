---
type: concept
title: Permission Gate
description: The policy layer in a coding-agent harness that decides, per tool call, whether execution proceeds automatically, is denied, or is escalated to a human — modeled in Decode on Claude Code's approval modes.
aliases:
  - PermissionGate
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[tool-call-routing-to-the-permission-gate]]"
  - "[[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/sandboxing]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]"
  - "[[subagents]]"
created: 2026-08-29T17:09:11Z
timestamp: 2026-08-31T14:48:26Z
source_count: 4
---

# Permission Gate

> A policy layer that decides, for every tool call a model emits, whether it runs automatically, is refused, or is put in front of a human.

## Definition

The system-design article frames the permission gate at the concept level: an ask/allow/deny policy per tool call, one of six modules composing "the harness" (alongside LLM providers, sandbox, memory, skills, and an LSP server), explicitly modeled on Claude Code's default/edit/auto approval modes. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

The repo's architecture page shows the concrete mechanism behind that framing, in Decode's `permissions/` package (`gate.py` policy, `rules.py` glob matching, `types.py` for modes and tool kinds): every tool call carries a `ToolKind`, read-only kinds auto-allow, other kinds run deny-then-allow rules then a mode × kind matrix. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The routing note refines *how* a call gets there rather than contradicting the matrix: every gated tool body opens with the same `if needs_approval(ctx): raise ApprovalRequired` regardless of `ToolKind` — read-only calls defer too, and their "auto-allow" is a verdict `gate.check()` returns quickly, not a bypass of the deferred path. `_resolve_deferred`/`_decide` in `agent/loop.py` then call `gate.check()` once per pending call; only an `ASK` verdict escalates further. [[tool-call-routing-to-the-permission-gate]]

The subagent-spawning note shows the gate's scoping is per-agent-instance, not global: a subagent child is built with a brand-new `PermissionGate(mode=PermissionMode.BYPASS)` object, not a mode flip on the parent's shared gate, so bypass is a property of that one child's `AgentDeps`, never leaking back to or borrowed from the parent's own gate instance. [[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]

> Tension: the repo names four permission modes (`bypass`, `plan`, `edit`, `default`); the article's gloss, when comparing to Claude Code, names three (`default`, `edit`, `auto`). Neither source page maps the two vocabularies onto each other explicitly.

## Key claims

- The gate is policy only and never prompts directly: an ASK verdict travels up to a human resolver, and an "approve forever" answer persists a rule into `.decode/settings.json`. Precedence is deny-first across every source, then the mode × kind matrix, then ask. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The exact call path: pydantic-ai bundles every paused call in a leg into one `DeferredToolRequests`; `AgentTurnHandler` hands it to `_resolve_deferred`, which loops each pending call and calls `_decide`, which builds a `PermissionRequest` and calls `gate.check(request)` — synchronous, one call per pending tool call, ALLOW/DENY resolving immediately. [[tool-call-routing-to-the-permission-gate]]
- An ASK in the interactive TUI suspends on an ephemeral, in-process `asyncio.Future` owned by a single `DecisionChannel` — nothing is persisted, so a crash loses a pending ask. The actual suspension point is the Runner's turn task parked mid-coroutine (`await agen.asend(...)`), not a yielded `Boundary`, and only one decision can be pending at a time. [[tool-call-routing-to-the-permission-gate]]
- While an ask is open, the TUI's single input surface is entirely captured by the decision: steering/follow-up text cannot be typed, and Esc does not abort the turn — it is parsed as an empty answer by `parse_permission_answer`, which denies anything that isn't `y`/`yes`/`allow`/`a`/`always`. [[tool-call-routing-to-the-permission-gate]]
- Headless `--hitl` does not reuse the TUI's gate-and-`DecisionChannel` plumbing at all: `KitaruAgent.run_sync()` is called directly, bypassing `AgentTurnHandler`/`Runner`. `ask_user`/`exit_plan_mode` use Kitaru's durable, timeout-bearing `wait_for_input()`; file-edit/bash approvals are intercepted by the external Kitaru adapter itself, with decode's own gate wired only as a deny safety net — a denial there ends the run outright rather than feeding back to the model the way a TUI denial does. [[tool-call-routing-to-the-permission-gate]]
- Permissions are named as one of the harness's six core modules, and the ask/allow/deny scheme is explicitly credited to Claude Code's default/edit/auto modes as its model. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- A subagent child's gate is a fresh `PermissionGate(mode=BYPASS)`, so every tool call it emits resolves inline and `ApprovalRequired` is never raised for it — there is no deferred-approval loop for anyone to answer. `resolve_permission` is still wired to `_deny_permission_resolver` (an unconditional deny), but it exists only as a safety net behind bypass mode, since bypass means the resolver is never normally reached. [[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]

## Relationships

- **Agent harness**: the permission gate is one of the modules composing "the harness" — the layer the course's thesis says actually differentiates a coding agent, as distinct from the ~20-line agent loop itself. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]
- **Sandboxing**: an ALLOW verdict from the gate is what lets a tool call reach the sandbox seam (none/docker/modal); the gate decides *whether* a command runs, the sandbox decides *where*. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/sandboxing]]
- **Agent loop**: `DeferredToolRequests` is the suspend/resume mechanism the gate depends on, but the two interfaces suspend differently underneath it — the TUI parks the Runner's turn task on an ephemeral in-process `Future`, while headless `--hitl` skips the loop's boundary machinery entirely for a durable Kitaru wait. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]
- **Subagents**: a spawned child never shares the parent's gate — it gets its own `PermissionGate(mode=BYPASS)` instance, showing the gate is scoped per agent instance rather than being one global policy object the whole process consults. [[subagents]]

> Synthesis: all four source-like pages trace to the same author/project (Paul Iusztin's Decode course) — one voice at increasing depth (concept-level article, whole-repo architecture pass, then two targeted questions) rather than independent corroboration. The layers are complementary, not redundant: the article names the policy, the ARCHITECTURE page shows the matrix, the routing note opens `needs_approval`/`_resolve_deferred`/`DecisionChannel` to show the TUI's ask and headless `--hitl`'s ask are structurally different mechanisms, and the subagent note is the only one to show the gate used a third way — not asked, not denied, but instantiated fresh per child in bypass mode.
