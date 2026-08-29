---
type: overview
title: ai-engineering — Overview
description: A wiki tracing why MCP, Skills, and CLIs are treated as three complementary agent-connectivity layers rather than competing standards.
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
total_sources: 5
total_pages: 14
---

# ai-engineering — Overview

## Themes

**Skills aren't MCP, but they need somewhere to live.** Every source that discusses skills is careful to note they're not a protocol primitive — the raw MCP spec never mentions the word — yet the same sources treat skills as real and worth naming, usually packaged as a prompt, a resource, or a composite tool. [[wiki/concepts/skills]] traces that tension, and [[wiki/entities/mcp]] is the protocol it keeps getting checked against. Best made by [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]], which goes spec-literal on the question, and [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], which treats skills as a first-class architectural layer regardless.

**The connectivity stack: skills, CLI, and MCP together.** "Connectivity is not one thing" is the wiki's recurring headline claim: the strongest agents are argued to combine reusable skill knowledge, sandboxed CLI execution, and governed MCP distribution rather than picking one. [[wiki/concepts/agent-connectivity]] is this thesis, with [[wiki/concepts/cli]] as its local-execution counterpart to skills and MCP. Best made by [[wiki/sources/the-future-of-mcp-vs-skills]] (the full conference-talk transcript) and [[wiki/sources/why-mcp-is-not-dead]] (the same idea applied to two of the author's own real projects).

**Where should orchestration logic actually live?** A recurring, unresolved architectural question: should the multi-step planning that composes tool calls run server-side, as one guaranteed-order composite tool, or client-side, more flexibly but with more round-trips? [[wiki/concepts/orchestration]] holds both positions without picking a winner. Best made by [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]], which poses the question directly from a real build, and [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]], which lays out the server-side-vs-client-side tradeoffs.

**MCP earns its place for governed, centralized business logic.** Where skills and CLIs are personal-scale defaults, MCP's case is made specifically at business scale: centralizing and securing logic (like a knowledge-graph-backed [[wiki/concepts/agent-memory]] store) that needs to be distributed to many clients under one governance point. [[wiki/entities/prefect]] and [[wiki/entities/fastmcp]] are the tooling this pattern is built on in practice. Best made by [[wiki/sources/why-mcp-is-not-dead]] and [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

## Index

### Entities (4)
- [[wiki/entities/mcp]] — the open Anthropic protocol for connecting agents to tools, data, and business logic.
- [[wiki/entities/claude-code]] — Anthropic's coding agent, used as both a reference MCP client and a native-skills harness.
- [[wiki/entities/fastmcp]] — the de facto default Python SDK for MCP servers, maintained by Prefect.
- [[wiki/entities/prefect]] — the company behind FastMCP and a pipeline orchestrator for agent memory builds.

### Concepts (5)
- [[wiki/concepts/skills]] — reusable capability packaging (`SKILL.md`) that sits outside the MCP protocol.
- [[wiki/concepts/cli]] — command-line tools as the local-execution connectivity layer.
- [[wiki/concepts/agent-connectivity]] — the thesis that skills, CLI, and MCP should be combined, not chosen between.
- [[wiki/concepts/orchestration]] — the open question of server-side vs. client-side agent planning logic.
- [[wiki/concepts/agent-memory]] — knowledge-graph-backed unified memory exposed to agents via MCP tools.

## Health

- Sources: 5 · Entities: 4 · Concepts: 5
- Slugs at 1 mention (waiting for a second): david-soria-parra, notion, obsidian
