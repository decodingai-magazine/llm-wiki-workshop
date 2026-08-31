---
type: source
title: Why MCP is Not Dead
description: MCP is not obsolete — it is the wrong tool for ungoverned personal setups but the right one for centrally-distributed, governed business logic at scale.
origin: local
original_path: data_input_examples/notes/01-easy/Why MCP is Not Dead.md
source_url:
authors: []
published_date:
raw_file: raw/why-mcp-is-not-dead.md
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]"
  - "[[wiki/entities/obsidian]]"
  - "[[wiki/entities/notion]]"
concepts:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/agent-connectivity]]"
---

# Why MCP is Not Dead

> [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead|Raw]] · local

## Summary

A rebuttal note (drafted as a hook/outline for a post, inspired by a "MCP is dead" LinkedIn post from Prefect) to the claim that MCP is obsolete. The argument is that people declaring MCP dead are judging it from personal setups — where a CLI, an llms.txt sitemap, or skills glue things together just fine — and generalizing that to the professional world, where deploying business logic to thousands of customers with governance and security in mind requires a centralized distribution point that CLIs and per-machine markdown files were never built to provide.

The second half grounds this in the author's own projects: a personal-assistant/unified-memory system where the specific business logic around a GraphRAG memory store justifies MCP tools over plain skills or a CLI, versus a digital twin where siloed third-party services (Notion, Readwise) are only securely reachable via their own MCP servers, while local file management stays on Obsidian and its CLI.

## Key claims

- People who conclude "MCP is dead" are usually judging it against personal setups, where a CLI to their database, links to an llms.txt sitemap, or skills to glue things together already work fine for them alone. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- That personal-scale reasoning breaks down at business scale: telling thousands of customers to install a CLI and a pile of markdown files on every machine is not viable, and it offers no real way to govern or secure that distributed logic. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- MCP servers solve exactly the centralized-distribution problem: your data stays in your own storage, you distribute it to many clients/agents at once, and you can govern and monitor the business logic from one place, including via skills and prompts shipped through the server. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- In the author's personal-assistant project, a GraphRAG-based unified memory with highly specific business logic over cloud-hosted infrastructure justifies exposing that logic as MCP tools — plain skills would have sufficed only for simpler file-based setups, and a CLI would have been unworkable. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- In the author's digital-twin project, siloed services like Notion and Readwise are only securely reachable through their own MCP servers, while local Obsidian files are managed directly by Claude Code or the Obsidian CLI. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- The conclusion is not "always use MCP" but "use MCP when it makes sense," alongside Claude Code skills and CLIs rather than instead of them. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]

## Notable quotes

> "MCP is NOT dead." You were just using it wrong.
> — [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/why-mcp-is-not-dead#Why MCP is Not Dead|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]], [[wiki/entities/obsidian]], [[wiki/entities/notion]]
- **Concepts**: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]], [[wiki/concepts/agent-connectivity]]

> Synthesis: The wiki's clearest statement of *when* to reach for MCP versus [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]] or [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]] — a personal-vs-business framing that complements rather than repeats the layered-architecture framing in [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/sources/the-future-of-mcp-vs-skills]].
