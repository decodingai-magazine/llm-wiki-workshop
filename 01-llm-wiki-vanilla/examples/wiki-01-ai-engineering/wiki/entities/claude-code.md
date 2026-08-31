---
type: entity
title: Claude Code
description: Anthropic's terminal-based coding agent and MCP client, which also natively runs skills placed in `.claude/skills/`.
aliases:
  - Claude Code
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/entities/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 5
---

# Claude Code

> Anthropic's coding agent, cited across this wiki both as a reference MCP client and as the reference implementation of native skills.

## Definition

Claude Code is treated in this wiki both as an MCP client/host — one that connects to MCP servers like any other — and as the reference implementation of Claude Code's own native skills system (`.claude/skills/`), which sits outside the MCP protocol entirely. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

It also appears repeatedly as the default, pre-built orchestrator teams reach for instead of writing a custom one, and as an example of the thin "presentation" layer (a TUI) in broader agent-architecture framings. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

## Key claims

- Claude Code treats MCP Tools and native `.claude/skills/` skills as agentically callable, but treats MCP Resources and Prompts as passive/user-invoked only. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- A progressive tool-discovery pattern (deferring tool definitions until the model needs them, instead of loading everything into context) showed a demonstrated massive reduction in context usage in a Claude Code before/after comparison. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- Claude Code can act as a pre-built MCP client/orchestrator, letting a team skip writing custom planning/execution logic when Claude Code's built-in orchestration is sufficient for the use case. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Claude Code is used as a concrete example of the "thin renderer" presentation layer (a TUI) in a four-layer agent architecture (presentation, harness/runtime, connectivity, MCP servers). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Claude Code is a common harness of choice for personal MCP-backed setups, and can manage local files directly (or via the Obsidian CLI) without needing an MCP server for that job. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/entities/mcp]]**: one MCP client/host among several, and the wiki's recurring default orchestrator. [[wiki/entities/mcp]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]**: its native `.claude/skills/` directory is the reference implementation of the skills convention this wiki traces across multiple agent harnesses. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]

> Synthesis: The one entity every source in this wiki treats as a shared reference point — used to illustrate MCP-primitive handling, progressive discovery, orchestrator choice, and personal-scale harness decisions alike.
