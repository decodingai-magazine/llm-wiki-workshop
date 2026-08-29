---
type: source
title: "The Future of MCP vs. Skills"
description: "A conference-talk transcript arguing that 2026 agents will need skills, CLIs, and MCP together, not any single connectivity mechanism."
origin: local
original_path: "data_input_examples/notes/01-easy/The Future of MCP vs. Skills.md"
source_url: null
authors: []
published_date: "2026-04-10"
raw_file: raw/the-future-of-mcp-vs-skills.md
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/fastmcp]]"
concepts:
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/orchestration]]"
---

# The Future of MCP vs. Skills

> [[raw/the-future-of-mcp-vs-skills|Raw]] · local

## Summary

Notes transcribed from an AI Engineering conference talk (delivered by an MCP co-creator) tracing MCP's growth from a minimal spec 18 months prior to 110M monthly downloads — faster adoption than React — and arguing that 2026 is the year agents move from local coding tasks to general knowledge work that needs broad SaaS connectivity. The talk's central claim is that connectivity "is not one thing": skills, CLIs, and MCP each solve a different slice of the problem, and serious agents will use all three together rather than picking one as a universal answer.

The second half is more technical: it argues for progressive tool discovery over dumping every tool into context, for programmatic/code-mode tool calling over sequential model-orchestrated tool calls, and for MCP server authors to design for agents first rather than mechanically converting REST APIs. It closes with a roadmap (stateless transport, async tasks, SDK v2, cross-app access, server discovery, skills shipped over MCP).

## Key claims

- MCP crossed 110M monthly downloads in 18 months — roughly twice the adoption speed of React — driven by adoption across OpenAI's agents SDK, Google ADK, LangChain, and enterprise integrations. [[raw/the-future-of-mcp-vs-skills#MCP Ecosystem Growth & Milestones|cite]]
- 2026 knowledge-work agents need connectivity to multiple SaaS applications and shared drives rather than a local sandboxed compiler loop, and "connectivity is not one" — there is no single tool for every connectivity problem. [[raw/the-future-of-mcp-vs-skills#2026 Agent Development Paradigm Shift|cite]]
- A three-layer connectivity architecture is proposed: Skills for reusable domain knowledge, CLI for local-sandbox productivity (and LLM training-data familiarity), and MCP for rich semantics, platform independence, and enterprise governance. [[raw/the-future-of-mcp-vs-skills#MCP Layer|cite]]
- Progressive discovery (deferring tool loading via a tool-search mechanism) and programmatic/code-mode tool calling (having the model write and execute composing code in an isolate rather than chaining tool calls turn by turn) both reduce context bloat and orchestration latency. [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- MCP server authors should design for the agent the way they would design for themselves as a human user, rather than mechanically converting REST APIs one-to-one into MCP servers. [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|cite]]
- A stateless transport protocol (from Google, landing around June) is coming to make MCP servers as easy to scale and deploy as any stateless REST service, alongside async task primitives, SDK v2 for TypeScript/Python, cross-app access, and server discovery. [[raw/the-future-of-mcp-vs-skills#Technical Roadmap & Core Infrastructure Improvements|cite]]

## Notable quotes

> "So this is all to say that I think in 2026 we're going to start building agents that use all of them. They don't use one thing, they use all of it."
> — [[raw/the-future-of-mcp-vs-skills#MCP Layer|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/claude-code]], [[wiki/entities/fastmcp]]
- **Concepts**: [[wiki/concepts/skills]], [[wiki/concepts/cli]], [[wiki/concepts/agent-connectivity]], [[wiki/concepts/orchestration]]

> Synthesis: The most detailed primary account of the "skills + CLI + MCP together" thesis that [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] later condenses into a four-layer architecture diagram from the same talk.
