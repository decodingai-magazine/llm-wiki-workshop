---
type: concept
title: CLI (as a connectivity layer)
description: Command-line tools as an agent connectivity layer — fast to adopt in sandboxed, local-execution contexts, but hard to govern once distributed to many users.
aliases:
  - CLI
  - command-line interface
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/entities/mcp]]"
  - "[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/skills]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 3
---

# CLI (as a connectivity layer)

> The connectivity layer every source treats as the easy, ungoverned default — great alone, until governance or multi-user distribution enters the picture.

## Definition

CLIs are treated across this wiki as one of an agent's three complementary connectivity mechanisms: the layer for local host capabilities, valued for how cheaply a model can compose and discover commands in a shell, and for how well-represented common CLIs (like git) already are in LLM training data. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

That same simplicity is also its ceiling: CLIs assume a sandboxed, well-behaved execution environment, and have no built-in way to be governed once distributed beyond a single user's machine. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Key claims

- CLIs are popular with local coding agents because they're easy to compose in a shell and automatically discoverable by a model, and they benefit from being well-represented in LLM training data (e.g., git, GitHub CLIs). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- CLIs are best suited to agents that can assume a sandboxed, good execution environment — a precondition that doesn't hold for every deployment. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- In a four-layer connectivity model, CLIs cover local host capabilities, alongside skills (domain knowledge) and MCP clients (auth/resources/tasks/UI). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- CLIs work well for personal setups (a CLI to one's own database or orchestrator) but don't scale to business distribution: installing a CLI on every customer's machine, with no governance model, is a non-starter. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/concepts/agent-connectivity]]**: CLI is one of the three connectivity layers this wiki argues should be combined, not chosen between. [[wiki/concepts/agent-connectivity]]
- **[[wiki/entities/mcp]]**: positioned as MCP's opposite on the governance axis — great for personal/sandboxed use, weak for governed, multi-user distribution. [[wiki/entities/mcp]]

> Synthesis: The layer every source treats as the easy default — the ceiling it hits (governance, distribution) is exactly the floor MCP is argued to start from.
