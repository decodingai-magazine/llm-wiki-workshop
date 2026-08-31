---
type: source
title: The future of MCP. Why the future of agents is MCP, skills and CLIs combined
description: "A LinkedIn-post summary of a talk by MCP co-creator David Soria Parra, framing AI applications as four independent, composable layers: presentation, harness/runtime, connectivity, and MCP servers."
origin: local
original_path: data_input_examples/notes/01-easy/The future of MCP. Why the future of agents is MCP, skills and CLIs combined.md
source_url:
authors: []
published_date:
raw_file: raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills.md
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/david-soria-parra]]"
concepts:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
---

# The future of MCP. Why the future of agents is MCP, skills and CLIs combined

> [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills|Raw]] · local

## Summary

A LinkedIn-post-style summary, credited to David Soria Parra's AI Engineering conference talk, condensing "the new way of building software powered by AI" into four independently decomposable layers rather than one stitched-together backend. It restates the growth numbers (110M monthly downloads, faster than React) and Soria Parra's line that "the best agents use all of it — skills, CLI, MCP — together" as the organizing thesis, then maps that onto four layers: a thin presentation renderer, a harness/runtime brain, a connectivity layer (skills, CLIs, MCP clients), and the MCP servers where business logic and private data live.

It closes on an open question about whether browsers stay the primary interface once chat interfaces can render any application on demand — an aside rather than an argued claim.

## Key claims

- The architecture emerging across serious AI applications has four independently decomposable layers: Presentation (thin renderer — TUI, IDE extension, web/desktop app), Harness + Runtime (the LLM↔tool loop, memory, permissions, orchestration), Connectivity (skills, CLIs, MCP clients), and MCP Servers (business logic and private data). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- MCP Apps let a client render a server-shipped UI directly from the harness, so the same MCP App can run unmodified across Claude, ChatGPT, and Cursor. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Within the Connectivity layer, skills are reusable user domain knowledge, CLIs are local host capabilities, and MCP clients cover auth, resources, tasks, and UI — modern agents use all three, and single-mechanism agents underperform. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- A modern MCP server ships tools, resources, prompts, skills, MCP Apps, and tasks/elicitation; FastMCP (by Prefect) has become the practical default Python implementation, quoted by MCP co-creator David Soria Parra as "way better than our Python SDK that we shipped." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- MCP recently crossed 110M monthly downloads, roughly twice the speed of React's adoption curve. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]

## Notable quotes

> "Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together."
> — [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/david-soria-parra]]
- **Concepts**: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]], [[wiki/concepts/agent-connectivity]]

> Synthesis: The condensed, quotable version of the same talk that [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/sources/the-future-of-mcp-vs-skills]] transcribes in full detail — useful as the headline framing, but the transcript is where the reasoning behind it lives.
