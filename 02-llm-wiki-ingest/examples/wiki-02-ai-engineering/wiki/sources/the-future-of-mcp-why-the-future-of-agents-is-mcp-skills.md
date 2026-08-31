---
type: source
title: "The future of MCP. Why the future of agents is MCP, skills and CLIs combined"
description: "A condensed, quote-driven distillation of an AI Engineering conference talk by MCP co-creator David Soria Parra, arguing that serious agent architecture decomposes into four independent layers — presentation, harness/runtime, connectivity (skills, CLI, MCP), and MCP servers."
origin: local
original_path: "data_input_examples/notes/02-medium/The future of MCP. Why the future of agents is MCP, skills and CLIs combined.md"
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/david-soria-parra]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
---

# The future of MCP. Why the future of agents is MCP, skills and CLIs combined

> [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills|Raw]] · local

## Summary

A LinkedIn-style post, framed as a distillation of remarks by MCP co-creator David Soria Parra at an AI Engineering conference, that pushes back on the default move of stitching agents and MCP servers into an existing frontend/backend — calling that a sensible but transitional adaptation of the old paradigm. Its organizing idea is Soria Parra's line that "connectivity is not one thing": the best agents combine skills, CLIs and MCP rather than leaning on one mechanism, and single-mechanism agents underperform. The post expands that into four independently decomposable layers, glued together by MCP: a thin Presentation renderer (TUI, IDE extension, web/desktop app — increasingly rendered on demand via MCP Apps rather than hand-built); a Harness + Runtime "brain" where the LLM-tool loop, memory, permissions and orchestration live, and where agents are becoming durable, checkpointable long-running systems rather than single inference calls; a Connectivity layer that picks the right mechanism per job (skills for reusable domain knowledge, CLIs for local host capabilities, MCP clients for auth/resources/tasks/UI); and an MCP Servers layer where business logic and private data live.

![[raw/assets/the-future-of-mcp-why-the-future-of-agen-image.png]]

It closes on FastMCP's rise to "the practical default" Python implementation — endorsed, by the post's account, even by MCP's own co-creator over Anthropic's official SDK — and on MCP's growth to 110M monthly downloads, framed as roughly twice React's adoption speed, before posing an open question about whether browsers stay the primary interface once chat interfaces can render any UI on demand.

## Key claims

- The architecture emerging across serious AI applications decomposes into four independent layers — Presentation, Harness + Runtime, Connectivity, and MCP Servers — with MCP as the connective tissue between them. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Connectivity is not one thing: skills cover reusable user domain knowledge, CLIs cover local host capabilities, and MCP clients cover auth, resources, tasks and UI — modern agents use all three, and single-mechanism agents underperform. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- With MCP Apps, a client can render a server-shipped UI directly from the harness, so the same MCP App runs across different clients (e.g. Claude, ChatGPT, Cursor) without rewriting the UI. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Agents are becoming long-running systems rather than single inference calls, which the post says requires durable execution, retries, checkpoints, human approvals and observability — infrastructure it positions tools like Prefect as providing as "part of the runtime itself." [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- FastMCP, built by Prefect, has become "the practical default" Python implementation for MCP servers, with Soria Parra himself quoted calling it "way better than our Python SDK that we shipped." [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- MCP recently crossed 110M monthly downloads, a growth rate the post frames as roughly twice as fast as React's adoption curve. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]

## Notable quotes

> "Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together."
> — [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]] (attributed to David Soria Parra)

> "It's just way better than our Python SDK that we shipped."
> — [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]] (David Soria Parra, on FastMCP)

## Connections

- **Entities**: [[wiki/entities/fastmcp]], [[wiki/entities/prefect]], [[wiki/entities/david-soria-parra]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/skills]], [[wiki/concepts/cli]], [[wiki/concepts/agent-connectivity]]

> Synthesis: A headline-and-quote condensation of a conference talk rather than an argued essay — its value is the four-layer framing and the "connectivity is not one thing" line, not new evidence; treat its numeric claims (110M downloads, React comparison) as asserted, not verified here.
