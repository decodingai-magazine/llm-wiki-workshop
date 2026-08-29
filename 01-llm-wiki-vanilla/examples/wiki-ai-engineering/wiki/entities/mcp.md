---
type: entity
title: Model Context Protocol (MCP)
description: An open protocol from Anthropic that lets AI agents connect to tools, data sources, and business logic through a standardized client-server architecture.
aliases: ["MCP", "Model Context Protocol"]
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/entities/fastmcp]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 5
---

# Model Context Protocol (MCP)

> An open client-server protocol for connecting AI agents to tools, data, and business logic — not, itself, a skills or orchestration mechanism.

## Definition

MCP defines a small set of protocol primitives — Tools (AI-invoked functions), Resources (passive data), Prompts (user-invoked templates), plus Sampling, Elicitation, and experimental Tasks — exchanged between an MCP client (inside a host application) and one or more MCP servers over JSON-RPC. "Skills" are explicitly not one of these primitives: the word appears nowhere in the raw spec, and any skill-like behavior is implemented as a prompt, a resource, or a composite tool. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

The protocol has grown from "a little spec document" 18 months ago to 110M monthly downloads — about twice React's adoption speed — with adoption spanning OpenAI's agents SDK, Google ADK, LangChain, and large enterprise deployments. [[wiki/sources/the-future-of-mcp-vs-skills]]

## Key claims

- Claude Code auto-detects and agentically calls MCP Tools, but MCP Resources and Prompts require explicit user invocation even though they're discoverable. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- MCP's value is centralized, governed distribution of business logic: data stays in the owner's storage, and many clients/agents can reach it at once with security and monitoring in one place — a property ungoverned per-machine CLIs and skill files can't match at business scale. [[wiki/sources/why-mcp-is-not-dead]]
- A modern MCP server ships Tools, Resources, Prompts, skills-as-resources, MCP Apps (server-shipped UI a client can render), and Tasks/Elicitation. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- A custom MCP server can compose prebuilt MCP servers (web search, image generation, Google Drive) into one combined tool/prompt surface reachable by any MCP client. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The protocol roadmap includes a stateless transport for easier scaling, async agent-to-agent task primitives, SDK v2 for TypeScript/Python, cross-app auth, and automatic server discovery. [[wiki/sources/the-future-of-mcp-vs-skills]]

## Relationships

- **[[wiki/concepts/skills]]**: skills are not an MCP primitive but are commonly packaged as MCP resources or shipped through MCP servers. [[wiki/concepts/skills]]
- **[[wiki/concepts/agent-connectivity]]**: MCP is one of three complementary connectivity layers (with skills and CLI), not a universal replacement for the other two. [[wiki/concepts/agent-connectivity]]
- **[[wiki/entities/fastmcp]]**: the de facto default Python SDK for building MCP servers. [[wiki/entities/fastmcp]]

> Synthesis: Across every source in this wiki, MCP is consistently defined by what it is *not* — not a skills mechanism, not a universal connectivity answer, not something to bolt onto every REST API — which turns out to be a sharper definition than a purely positive one would give.
