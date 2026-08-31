---
type: entity
title: Pydantic AI
description: The Python agent framework — a typed Agent object with tools and a structured, deferrable output_type — that decode's entire agent loop is built directly on top of, imported rather than abstracted behind an interface.
aliases:
  - pydantic-ai
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[tool-call-routing-to-the-permission-gate]]"
  - "[[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]"
  - "[[subagents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
created: 2026-08-29T17:08:34Z
timestamp: 2026-08-31T14:48:46Z
source_count: 4
---

# Pydantic AI

> The tool-calling agent library decode's "agent" narrowly *is* — everything else the codebase builds around it is "the harness."

## Definition

Both sources draw the same boundary — the "agent" is a small Pydantic AI construction, everything else is harness — at different resolutions. The article states it as thesis: the agent is "a ~20-line Pydantic AI tool-calling loop (model, tools, an `output_type` that ends a turn as either a final answer or paused tool calls)," and everything built across the course's 8 lessons on top is "the coding harness." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] The repo's architecture read shows the construction behind that claim: `build_agent()` instantiates `Agent[AgentDeps, str | DeferredToolRequests]` with `deps_type=AgentDeps`, `output_type=[str, DeferredToolRequests]`, `output_retries=3`, `tool_retries=5`. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- decode's stated design rule treats pydantic-ai as infrastructure to be **imported, not abstracted** — called directly, alongside `modal` and `opik`, because no second agent framework has arrived to justify hiding it behind an interface. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `output_type=[str, DeferredToolRequests]` is the load-bearing construction choice: a tool call needing approval doesn't block, it returns a *deferred request* the harness later resumes with `DeferredToolResults` — this is what makes the permission prompt and mid-turn steering possible. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The turn handler drives the framework via `agent.iter`, one "leg" per prompt + `message_history`, and must repair a history whose last message carries tool calls with no results (after a crash or aborted turn) — otherwise pydantic-ai rejects every subsequent prompt, bricking the session. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `OpenAIChatModel` emits one `system` message per instruction source, and some OpenAI-compatible servers reject more than one, so decode joins base instructions, persona, memory and skills catalog into a single string before handing it to pydantic-ai. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Compaction reads the *last populated* `ModelResponse.usage`, not cumulative usage — pydantic-ai accumulates usage across every tool round within a turn and would overcount roughly N× for an N-round turn otherwise. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The deferred-tool primitive's exact mechanics: a gated tool body raises `ApprovalRequired`, and pydantic-ai catches it *across a whole tool round*, resolving that leg's output to **one** `DeferredToolRequests` bundling every paused call in the round — not one per call. decode's entire per-call approval loop is built on top of this library-level batching. [[tool-call-routing-to-the-permission-gate]]
- Subagent spawn is a direct, re-entrant call: `Agent.run()` is invoked recursively on the *same installed* `Agent` instance (fetched via `_require_main_agent()`, the object `set_main_agent()` stashed once at `build_agent()` time) with a fresh, narrowed `AgentDeps` — not a second `Agent` construction, so a child shares the parent's model and HTTP client outright. [[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- Each nested child run passes `usage_limits=UsageLimits(request_limit=settings.subagent_max_requests)`, bounding that one call, plus its own `event_stream_handler`; because a nested `agent.run()` bypasses decode's own turn loop entirely, that handler is the *only* channel turning the child's `FunctionToolCallEvent`s into events the parent process can show — without it a child's tool calls would be invisible even in verbose mode. [[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]

## Relationships

- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]**: pydantic-ai's `Agent` plus `agent.iter` *is* the agent loop in decode's own vocabulary — the ~20-line core the rest of the harness wraps. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]**: the harness/agent boundary both sources draw is defined by what pydantic-ai's `Agent` construction does versus everything decode builds around it. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]**: built on pydantic-ai's `DeferredToolRequests`/`DeferredToolResults` pause-and-resume mechanism, not a framework-native permission feature — specifically on its one-bundle-per-round batching, which is why decode's resolver walks `requests.approvals` one call at a time. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[tool-call-routing-to-the-permission-gate]]
- **[[subagents]]**: fan-out is nested, re-entrant `agent.run()` calls on the *same* `Agent` instance with narrowed dependencies rather than a second agent object — each call bounded by its own `UsageLimits(request_limit=...)` and made observable to the parent only through `event_stream_handler`. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[how-a-subagent-is-spawned-and-what-the-parent-gets-back]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]**: the compaction trigger's usage accounting is written around how pydantic-ai reports `usage` across tool rounds. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: all four source-like pages trace to the same author/project — decode and its course — so this is one voice at increasing depth (thesis prose, full architecture read, two targeted code traces), not independent corroboration. The routing note opens the deferred-approval primitive itself (`ApprovalRequired` → one `DeferredToolRequests` per round); the subagent note opens the other primitive the harness leans on — recursive `Agent.run()` on one installed instance, scoped per call by `UsageLimits` and made visible only through `event_stream_handler`.
