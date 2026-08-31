---
type: concept
title: Agent Connectivity (Skills + CLI + MCP)
description: The idea that skills, CLIs, and MCP are complementary connectivity layers agents should combine, not a single universal mechanism to pick once.
aliases:
  - connectivity stack
  - full connectivity
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/skills]]"
  - "[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/cli]]"
  - "[[wiki/entities/mcp]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 3
---

# Agent Connectivity (Skills + CLI + MCP)

> "Connectivity is not one thing" — the best agents use skills, CLI, and MCP together, not one instead of the others.

## Definition

This concept is this wiki's unifying thesis: rather than treating skills, CLIs, and MCP as competing answers to "how should an agent connect to the outside world," multiple sources argue they are complementary layers, each suited to a different situation — reusable domain knowledge, local sandboxed execution, and governed multi-client distribution, respectively. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

The same idea shows up in a more concrete, situational form in a builder's own project choices: which layer to reach for isn't fixed in advance, it depends on whether the logic is simple enough for a file, whether the environment is sandboxed, and whether the data needs to be shared securely across multiple clients. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Key claims

- "Connectivity is not one thing" — no single mechanism solves every connectivity problem, and treating one of skills, CLI, or MCP as universal is a red flag. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- The best 2026 agents are predicted to use skills, CLIs, and MCP "quite seamlessly together," rather than picking one; single-mechanism agents are expected to underperform. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- The choice isn't ideological but situational: a personal-assistant project uses MCP tools for its bespoke memory logic but a CLI for infrastructure access during development, and a digital-twin project uses MCP for siloed third-party services but Claude Code or the Obsidian CLI for local files. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/skills]]**: the reusable-domain-knowledge layer within this connectivity stack. [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/skills]]
- **[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/cli]]**: the local-execution layer within this connectivity stack. [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/cli]]
- **[[wiki/entities/mcp]]**: the governed, multi-client distribution layer within this connectivity stack. [[wiki/entities/mcp]]

> Synthesis: The wiki's organizing thesis — nearly every other page in it makes a case for one layer or another, but this is the one that explains why none of those cases needs to be won outright.
