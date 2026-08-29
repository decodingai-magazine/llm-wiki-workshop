---
type: source
title: The future of MCP. Why the future of agents is MCP, skills and CLIs combined
description: A LinkedIn post arguing that serious agent systems are converging on a four-layer architecture (presentation, harness/runtime, connectivity, MCP servers) where skills, CLIs and MCP are used together rather than as a single mechanism.
origin: local
original_path: data_input_examples/notes/02-medium/The future of MCP. Why the future of agents is MCP, skills and CLIs combined.md
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills.md
created: 2026-08-29T16:10:17Z
timestamp: 2026-08-29T16:10:17Z
entities:
  - "[[wiki/entities/david-soria-parra]]"
  - "[[wiki/entities/anthropic]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-architecture]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/cli]]"
---

# The future of MCP. Why the future of agents is MCP, skills and CLIs combined

> [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills|Raw]] · local

## Summary

The post argues that most teams are still building AI applications by grafting agents and MCP servers onto existing frontend/backend architectures — a reasonable first step, but not where the field is heading. Citing David Soria Parra (Anthropic, MCP co-creator), the author frames the real shift as connectivity itself: "the best agents use all of it — skills, CLI, MCP — together," rather than leaning on one mechanism.

![[raw/assets/the-future-of-mcp-why-the-future-of-agen-image.png]]

From that framing the author lays out a four-layer architecture that recurs across "serious" AI applications: a thin **Presentation** layer (TUIs, IDE extensions, web/desktop apps, increasingly rendered via MCP Apps); a **Harness + Runtime** layer that holds the LLM↔tool loop, memory, permissions and orchestration, and is starting to need durable execution, retries, checkpoints and human approval like a workflow engine; a **Connectivity** layer where skills, CLIs and MCP clients each cover a different kind of capability; and an **MCP Servers** layer where business logic and private data live, shipping tools, resources, prompts, skills, apps and tasks. MCP is positioned as the connective tissue running through all four.

The author also uses FastMCP as evidence that the ecosystem is maturing fast: built by Prefect, it has become the practical default Python SDK, with Soria Parra himself preferring it over Anthropic's own official SDK — and the author cites MCP's download growth as outpacing React's.

## Key claims

- Most current AI applications retrofit agents/MCP servers into pre-existing frontend/backend architectures rather than being designed around them. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- The architecture emerging across serious AI applications has four independently decomposable layers — Presentation, Harness+Runtime, Connectivity, MCP Servers — with MCP as the connective tissue between them. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Connectivity is not one mechanism: skills cover reusable user domain knowledge, CLIs cover local host capabilities, and MCP clients cover auth, resources, tasks and UI; single-mechanism agents underperform. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Agents are becoming long-running systems that need durable execution, retries, checkpoints, human approvals and observability, which is why the author counts workflow tools like Prefect as part of the runtime itself. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- With MCP Apps, clients can render server-shipped UI directly from the harness, and the same MCP App runs across Claude, ChatGPT and Cursor without a UI rewrite. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- FastMCP (built by Prefect) has become the practical default for building MCP servers in Python, and MCP has crossed 110M monthly downloads — roughly twice as fast as React reached that mark. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]

## Notable quotes

> "Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together."
> — [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]] (David Soria Parra)

> "It's just way better than our Python SDK that we shipped."
> — [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]] (David Soria Parra, on FastMCP)

## Connections

- **Entities**: [[wiki/entities/david-soria-parra]], [[wiki/entities/anthropic]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/agent-architecture]], [[wiki/concepts/agent-skills]], [[wiki/concepts/cli]]

> Synthesis: The only source touching agent architecture so far — its four-layer framing and its "connectivity is not one thing" thesis are single-witness claims until another source corroborates them.
