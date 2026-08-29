---
type: source
title: The Future of MCP vs. Skills
description: Talk notes from an MCP maintainer arguing that connectivity is a stack — skills, CLIs and MCP each for their own job — and laying out the 2026 protocol roadmap.
origin: local
original_path: data_input_examples/notes/01-easy/The Future of MCP vs. Skills.md
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-vs-skills.md
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/anthropic]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/mcp-apps]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/governance]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
---

# The Future of MCP vs. Skills

> [[raw/the-future-of-mcp-vs-skills|Raw]] · local

## Summary

Near-verbatim notes from a conference talk by an MCP maintainer, structured as
"where the protocol has been, where it is going." The framing claim is that MCP
hit 110M monthly downloads in 18 months — roughly twice as fast as React — and
that this matters less as a vanity metric than as evidence of a shared dialect
across OpenAI's agents SDK, Google ADK, LangChain and thousands of tools nobody
has heard of.

The core argument is a rejection of the "one connectivity mechanism" framing.
Connectivity is a **stack**, and the talk assigns each layer a job: skills carry
reusable domain knowledge in a plain file; CLIs are unbeatable when the agent is
local, sandboxed, and the tool is already in the training data; MCP earns its
keep when you need rich semantics, a UI for long-running work, platform
independence, or the "boring but important enterprise stuff" — authorization,
governance policies, no sandbox to assume. The 2026 prediction is that good
agents stop choosing and use all of them together.

Two techniques are singled out as under-used. **Progressive discovery**: stop
dumping every tool definition into the context window; defer loading and let the
model pull tools in when it needs them. **Programmatic tool calling**: instead of
the model calling a tool, reading the result and calling the next, give it an
execution environment and let it write a script — MCP's structured output gives
it the type information to compose calls safely.

The roadmap items are concrete: a stateless transport so servers deploy like
ordinary REST services, a better async task primitive for agent-to-agent work,
v2 TypeScript and Python SDKs, cross-app access so one enterprise login carries
over, server discovery at well-known URLs, and shipping skills over MCP.

## Key claims

- Connectivity has no single answer — "there is really a big connectivity stack and there's the right tool for the right job." [[raw/the-future-of-mcp-vs-skills#2026 Agent Development Paradigm Shift|cite]]
- CLIs win when the agent is local and the tool was in pre-training; MCP wins when you need rich semantics, platform independence, or cannot assume a sandbox. [[raw/the-future-of-mcp-vs-skills#CLI Layer|cite]]
- Loading every tool into the context window is the current default and is wrong; progressive discovery defers tool loading until the model asks for it. [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- Letting the model orchestrate tool-by-tool wastes inference and latency; giving it a sandboxed execution environment to compose calls in code is cheaper and composes better. [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- Mechanically converting REST APIs into MCP servers is an anti-pattern — design the server for an agent instead. [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|cite]]
- Shipping skills over MCP lets a server author update procedural knowledge centrally, without a plugin registration mechanism. [[raw/the-future-of-mcp-vs-skills#Enterprise Integration & Advanced Features|cite]]

## Notable quotes

> "2026, I think it's all about connectivity and the best agents use every available network. They will use computer use, they will use clis, they will use mcps, we'll use scripts."
> — [[raw/the-future-of-mcp-vs-skills#Vision & Community Direction|location]]

> "Every time I see someone building another rest api MCP server conversion tool, it's a bit cringe because I think it just results in horrible things."
> — [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/anthropic]], [[wiki/entities/fastmcp]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/connectivity-stack]], [[wiki/concepts/agent-skills]], [[wiki/concepts/cli-tools]], [[wiki/concepts/mcp-primitives]], [[wiki/concepts/mcp-apps]], [[wiki/concepts/mcp-server-design]], [[wiki/concepts/skills-over-mcp]], [[wiki/concepts/governance]], [[wiki/concepts/progressive-disclosure]], [[wiki/concepts/programmatic-tool-calling]]

> Synthesis: This is the wiki's anchor source for the connectivity-stack argument — the other notes mostly apply it, quote it, or push back on its enterprise framing.
