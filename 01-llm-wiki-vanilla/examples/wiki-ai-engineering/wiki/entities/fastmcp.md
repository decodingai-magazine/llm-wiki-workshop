---
type: entity
title: FastMCP
description: The Python MCP framework that became the practical default for building servers, and whose skills provider is the concrete implementation the notes evaluate.
aliases: [Fast MCP]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/server-side-orchestration]]"
  - "[[wiki/entities/prefect]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 7
---

# FastMCP

> A Python framework for MCP servers and clients, widely treated as the default over the official SDK — including by the person who wrote the official SDK.

## Definition

FastMCP provides the decorator API (`@mcp.tool`, `@mcp.prompt`, `@mcp.resource`)
that the notes use whenever they show server code, plus the client utilities used
to build a custom orchestrator against a composed set of servers
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]. It also ships
the `SkillsDirectoryProvider`, which exposes skill directories as MCP resources —
the mechanism at the centre of the skills-over-MCP question
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]].

## Key claims

- FastMCP's own framing is that a skill is "a prompt, a resource, or a bundle of both" — packaging, not architecture. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- `SkillsDirectoryProvider` publishes each skill as `skill://name/SKILL.md` plus a synthetic `_manifest`, making skills discoverable to any MCP client. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Because resources are not agentically consumed, skills shipped this way are listable but never invoked on the model's initiative — the "dead zone". [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- The maintainer of the official Python SDK says of FastMCP: "It's just way probably better than Python distribution" — and the v2 SDK is being rewritten with its lessons. [[wiki/sources/the-future-of-mcp-vs-skills]]
- In Python, FastMCP "has effectively become the practical default" for shipping tools, resources, prompts, skills and MCP Apps. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Both sides of the orchestrator question are implemented with FastMCP — the server, and the client utility the custom orchestrator uses. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The lifespan pattern initializes expensive resources — database client, LLM, embedding model, indexes — once at startup and hands every tool handler the same context. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Tool schemas are generated from the function signature and docstring, which makes the docstring the model-facing contract. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Deploying a server has collapsed to connecting a repo and naming the entry point plus the uv environment, with auth and continuous deployment included. [[wiki/sources/owning-your-context-layer]]
- The v2 SDKs are being written to incorporate FastMCP-level ergonomics. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/skills-over-mcp]]**: FastMCP is the only concrete implementation the notes examine, and the source of the pattern's known limitation.
- **[[wiki/entities/prefect]]**: FastMCP is maintained by the same company, which is why the two appear together in the runtime layer.

> Synthesis: FastMCP is where the abstract protocol questions become testable — every claim about skills-over-MCP in this wiki is ultimately a claim about what its provider does.
