---
type: source
title: The Future of MCP vs. Skills
description: A talk-transcript arguing that skills, CLI and MCP are complementary connectivity layers rather than competing options, and that 2026 agents will combine all three alongside techniques like progressive tool discovery and programmatic tool calling.
origin: local
original_path: "data_input_examples/notes/02-medium/The Future of MCP vs. Skills.md"
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-vs-skills.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/fastmcp]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/orchestration]]"
---

# The Future of MCP vs. Skills

> [[raw/the-future-of-mcp-vs-skills|Raw]] · local

## Summary

A talk-style, informally transcribed note on the state of MCP as of April 2026. It opens with adoption numbers — MCP crossed 110M monthly downloads in 18 months, a faster climb than a comparable React milestone — and credits the growth as much to framework integrations (OpenAI's Agents SDK, Google's ADK, LangChain) as to Anthropic's own additions of remote MCP, centralized authorization, elicitation and MCP applications.

Its central argument is that 2026 is the year agents move past 2025's "coding agent" era into general knowledge work, and that this shift makes connectivity the bottleneck: a knowledge-work agent needs to reach several SaaS apps and a shared drive, not just a local compiler. The note explicitly rejects any single "one true connectivity mechanism" and instead lays out three complementary layers — skills for packaged capability knowledge, CLI for sandboxed local execution, and MCP for rich semantics, platform independence and enterprise governance — arguing that 2026 agents will combine all three rather than pick one.

The back half turns prescriptive: use progressive tool discovery (keep tool definitions out of context and load them on demand) and programmatic "code mode" tool calling (have the model write code against an execution sandbox instead of one tool call per inference round-trip) to keep large toolsets usable; stop converting REST APIs one-to-one into MCP servers and instead design servers the way you would design an interface for a human; and expect a 2026 protocol roadmap covering a stateless transport, an async agent-to-agent task primitive, TypeScript/Python SDK v2s (the Python one informed by FastMCP), cross-app SSO, and automatic server discovery.

## Key claims

- MCP reached 110M monthly downloads in 18 months, a faster climb than a comparable React adoption milestone, driven by adoption inside OpenAI's Agents SDK, Google's ADK and LangChain as much as by Anthropic's own work. [[raw/the-future-of-mcp-vs-skills#MCP Ecosystem Growth & Milestones|cite]]
- 2026 is framed as the shift from 2025's coding-agent era to general knowledge work, where the critical requirement is connectivity to SaaS applications and shared drives rather than a local, sandboxed compiler loop. [[raw/the-future-of-mcp-vs-skills#2026 Agent Development Paradigm Shift|cite]]
- Connectivity is explicitly modeled as three complementary layers rather than one universal solution: skills for reusable capability knowledge, CLI where you can assume a sandbox and good execution environment, and MCP when you need rich semantics, platform independence, or enterprise concerns like authorization and governance. [[raw/the-future-of-mcp-vs-skills#MCP Layer|cite]]
- Two techniques are recommended to keep tool-heavy agents efficient: progressive discovery (defer tool loading via something like a tool-search tool instead of dumping every tool definition into context) and programmatic/"code mode" tool calling (the model writes code against an execution sandbox — a V8 isolate, Monty, or Lua interpreter — to compose multiple tool calls instead of one inference round-trip per call). [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- Server authors are told to stop converting REST APIs one-to-one into MCP servers, to design for how a human would want to interact with the system, and to use MCP-native semantics — structured output, elicitation, tasks, MCP applications, skills shipped over MCP — instead of mirroring a REST API's shape. [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|cite]]
- The stated 2026 protocol roadmap includes a stateless transport protocol built with Google (targeted for June), an async agent-to-agent task primitive, TypeScript and Python SDK v2s (the Python SDK informed by lessons from FastMCP), cross-app access for single sign-on across MCP servers, and automatic server discovery via well-known URLs. [[raw/the-future-of-mcp-vs-skills#Technical Roadmap & Core Infrastructure Improvements|cite]]

## Notable quotes

> "What they need is something that can connect to like five SaaS applications and a shared drive. Because the most important part for them for an agent is connectivity."
> — [[raw/the-future-of-mcp-vs-skills#2026 Agent Development Paradigm Shift|location]]

> "Every time I see someone building another rest apart MTP server conversion tool, it's a bit cringe because I think it just results in horrible things."
> — [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|location]]

> "So 2026, I think it's all about connectivity and the best agents use every available network. They will use computer use, they will use clis, they will use mcps, we'll use scripts because they want to have a wide variety of things they can do."
> — [[raw/the-future-of-mcp-vs-skills#Vision & Community Direction|location]]

## Connections

- **Entities**: [[wiki/entities/fastmcp]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/skills]], [[wiki/concepts/cli]], [[wiki/concepts/agent-connectivity]], [[wiki/concepts/orchestration]]

> Synthesis: A keynote-style transcript that states the "connectivity stack" thesis (skills + CLI + MCP as complementary layers, not one universal mechanism) more explicitly and completely than a passing mention would — later sources touching skills, CLI, or MCP internals should be read against this framing rather than as independent takes.
