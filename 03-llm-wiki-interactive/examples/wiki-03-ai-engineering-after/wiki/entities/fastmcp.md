---
type: entity
title: FastMCP
description: A Python SDK for building MCP servers and clients, built by Prefect, used across these sources as a thin delivery layer that adds no business logic of its own.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/owning-your-context-layer]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/orchestrator-placement]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
created: 2026-08-29T16:14:02Z
timestamp: 2026-08-29T16:14:02Z
source_count: 5
---

# FastMCP

> A Python SDK for building MCP servers and clients — built by Prefect and used, across every source that touches it, as a thin delivery layer rather than a place logic lives.

## Definition

FastMCP is the Python SDK these sources reach for to build both MCP servers and MCP clients. It is built by Prefect and described as having become "the practical default" for building MCP servers in Python [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]. Its role is consistently framed as delivery, not logic: tools built on it are meant to stay thin wrappers around business logic that lives elsewhere — "the MCP layer is a delivery mechanism, not a logic layer" [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]] — and it is used symmetrically, implementing both the server and the client-side connection to it in the same stack [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

One source complicates the "pure delivery layer" framing: FastMCP also ships a `SkillsDirectoryProvider` that packages a skills folder as MCP *resources* (`skill://name/SKILL.md`, `_manifest`, supporting files). By FastMCP's own description this is "a packaging decision, not an architectural one" — but because Claude Code only agentically invokes MCP Tools and its own `.claude/skills/`, never MCP resources, a skill shipped this way ends up discoverable by any MCP client yet not autonomously callable by Claude Code [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]].

## Key claims

- FastMCP tools are recommended to stay thin delegates — extract lifespan context, call an existing business-logic function, return — so the same code path runs whether it's triggered by a live MCP call or a batch job. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
- FastMCP's `SkillsDirectoryProvider` exposes a skills folder as MCP resources rather than as a new protocol primitive; since Claude Code doesn't agentically consume MCP resources, skills packaged this way fall into a "dead zone" — neither a developer-owned tool/prompt nor a user-owned `.claude/skills` entry. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- FastMCP was used to build and deploy a personal memory MCP server, with Prefect Horizon Cloud handling deployment, auth and redeploy-on-push once GitHub, the MCP entry point and the UV environment were specified. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/owning-your-context-layer]]
- Built by Prefect, FastMCP has become the practical default Python SDK for building MCP servers; David Soria Parra (Anthropic, MCP co-creator) is quoted preferring it over Anthropic's own official SDK — "It's just way better than our Python SDK that we shipped." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- FastMCP implements both the MCP server and the client-side connection to it in an agent stack that also uses Prefect to orchestrate the data, memory and retrieval pipelines. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **Prefect**: the two are consistently paired — Prefect orchestrates pipelines (data, memory, retrieval) and FastMCP serves the result over MCP, including through Prefect's own Horizon Cloud for deployment. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]
- **MCP**: FastMCP is not the protocol itself but the dominant Python implementation of it, used for both server and client sides. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]
- **Claude Code**: consumes FastMCP-built servers as any MCP harness would — it auto-invokes the Tools FastMCP exposes, but not the resources FastMCP uses to package skills. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]

> Synthesis: Four of the five sources are the same practitioner's own build write-ups — a personal knowledge-graph/memory server and a book project with Maxime Labonne — that consistently pair FastMCP with Prefect; that pairing is one voice repeated, not independent corroboration. The one distinct voice is Anthropic's own MCP co-creator, David Soria Parra, endorsing FastMCP over Anthropic's official SDK.
