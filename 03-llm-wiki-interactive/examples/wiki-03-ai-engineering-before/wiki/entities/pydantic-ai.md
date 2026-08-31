---
type: entity
title: Pydantic AI
description: The Python agent framework — a typed Agent object with tools and a structured, deferrable output_type — that decode's entire agent loop is built directly on top of, imported rather than abstracted behind an interface.
aliases:
  - pydantic-ai
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]"
  - "[[subagents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
created: 2026-08-29T17:08:34Z
timestamp: 2026-08-29T17:08:34Z
source_count: 2
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
- Subagent fan-out reuses the *same* `Agent` object rather than a second one — a child is a nested `agent.run()` call with narrowed `deps`, so the framework's own `prepare=` tool-filtering collapses the child's toolset with no agent rebuild. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-loop]]**: pydantic-ai's `Agent` plus `agent.iter` *is* the agent loop in decode's own vocabulary — the ~20-line core the rest of the harness wraps. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]**: the harness/agent boundary both sources draw is defined by what pydantic-ai's `Agent` construction does versus everything decode builds around it. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]**: built on pydantic-ai's `DeferredToolRequests`/`DeferredToolResults` pause-and-resume mechanism, not a framework-native permission feature. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[subagents]]**: fan-out is nested `agent.run()` calls on the same `Agent` instance with narrowed dependencies, not a second agent object. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]**: the compaction trigger's usage accounting is written around how pydantic-ai reports `usage` across tool rounds. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: both sources describe the same course/codebase, and the article is essentially a prose restatement of the agent/harness boundary the repo's own architecture read already establishes with actual code; treat the ≥2 count as one project witnessed at two zoom levels, not independent corroboration. The framework-specific substance (deferred-tool semantics, usage accounting, history repair, instruction-joining) lives only in the repo page.
