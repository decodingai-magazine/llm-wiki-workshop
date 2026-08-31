---
type: concept
title: Programmatic Tool Calling
description: A harness-layer pattern where the model writes a script against a sandboxed code-execution environment to compose multiple tool calls itself, instead of round-tripping through inference for every step — also known as code mode.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/progressive-tool-discovery]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]"
created: 2026-08-29T16:15:16Z
timestamp: 2026-08-29T16:15:16Z
source_count: 2
---

# Programmatic Tool Calling

> Also called "code mode": the model writes a script against a sandboxed execution environment to compose tool calls itself, rather than the harness round-tripping through inference for every step.

## Definition

Both sources give the same definition, for a reason worth stating up front (see Synthesis): programmatic tool calling is one of the harness layer's two priority upgrades, alongside progressive tool discovery. Instead of the model orchestrating exactly one tool call per inference turn, it writes a script against a code-execution environment — a sandbox, with a V8 isolate, "Monty," or a Lua interpreter named as candidate runtimes — that composes multiple tool calls itself. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]] MCP's structured-output feature is what makes that model-written composition reliable, by supplying the type information the generated code chains against. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]

## Key claims

- The model writes a script that composes tool calls itself inside a sandboxed execution environment, instead of the harness round-tripping through inference for every call — "code mode." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- Named candidate execution environments include a V8 isolate, "Monty," and a Lua interpreter. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- MCP's structured-output feature supplies the typing that makes the model-written composition reliable. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- It lets the model filter large results within one call rather than paying a round-trip per filter step: "You do one call and you can filter that. The model will automatically remove things from the JSON and just continue." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- It is one of the harness's two priority upgrades — paired with progressive tool discovery — in a four-layer (presentation / harness / connectivity / MCP servers) architecture for future AI apps. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **Progressive tool discovery**: the harness's other named priority upgrade — discovery decides what tools the model can see, programmatic tool calling decides how it uses them once seen. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/progressive-tool-discovery]]
- **MCP**: programmatic tool calling leans on MCP's structured-output feature for the typed, composable results a script needs to chain calls. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]
- **Skills / CLI**: both sources place programmatic tool calling in the harness layer, distinct from skills and CLI, which they treat as connectivity-layer mechanisms. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]

> Synthesis: The two source pages here are not two independent witnesses — both are note-takers' accounts of the same 2026 conference talk (one names Anthropic's David Soria Parra and the talk title "The Future of MCP" directly; the other describes an unedited transcript of a talk by "an Anthropic engineer who 'wrote the Python SDK' for MCP," the same body of work). This page technically clears the ≥2-source threshold but currently rests on one independent voice, not two — corroboration from an unrelated speaker or source is still needed before this definition should be treated as consensus rather than one person's framing.
