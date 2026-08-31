---
type: entity
title: FastMCP
description: A Python framework, built by Prefect, for building MCP servers and clients — described across sources as the practical default implementation for MCP servers.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/orchestration]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 6
---

# FastMCP

> A Python framework, built by Prefect, for building MCP servers and clients.

## Definition

FastMCP is the Python framework every source in this wiki reaches for when it builds an MCP server, and sometimes when it builds the client driving one. It is built by Prefect, and one source quotes MCP co-creator David Soria Parra calling it "way better than our Python SDK that we shipped," framing it as "the practical default" Python implementation for MCP servers. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

No source defines FastMCP differently from another; they instead surface different facets of the same tool: a server-building framework (§ Key claims), a source of client-side utilities for custom orchestrators, and an extension point that packages conventions — like the cross-agent `SKILL.md` folder pattern — as MCP resources.

## Key claims

- FastMCP is a Python framework, built by Prefect, for building MCP servers, and it also provides client-side utilities for building custom MCP orchestrators. [[wiki/sources/owning-your-context-layer]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- It is described as "the practical default" Python implementation for MCP servers, with MCP co-creator David Soria Parra quoted saying it is "way better" than Anthropic's own shipped Python SDK; separately, the official Python SDK v2 on the 2026 protocol roadmap is described as informed by lessons from FastMCP. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/the-future-of-mcp-vs-skills]]
  > Synthesis: these two sources may trace back to the same underlying talk on MCP's 2026 trajectory (both cite the same "110M monthly downloads, faster than React" statistic) — treat this as one voice on FastMCP's standing, not two independent ones.
- A FastMCP server can be built as a thin, logic-free delivery layer: tools only pull lifespan context, delegate to existing business-logic functions, and serialize the result — so the same underlying code runs identically whether triggered by an MCP tool call or a separate batch pipeline. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- FastMCP implements the cross-agent skills folder convention (`SKILL.md`) as MCP resources via a `SkillsDirectoryProvider`, exposing each skill as `skill://name/SKILL.md`, `skill://name/_manifest`, and `skill://name/path/to/file` — a packaging decision, since MCP itself has no native "Skills" primitive. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- A FastMCP-built server was deployed to Prefect Horizon Cloud by connecting GitHub and specifying the MCP entry point and UV environment, reported as sufficient for automatic, authenticated, continuously-updated serverless deployment within minutes. [[wiki/sources/owning-your-context-layer]]
- FastMCP's client utilities are one of two named ways to drive a merged toolset composed from several MCP servers, the other being a prebuilt orchestrator such as Claude Code — both are, from the end user's perspective, just MCP clients. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **MCP**: FastMCP is a concrete Python implementation of MCP servers (and clients) — the framework named whenever these sources move from the protocol to actual code. [[wiki/concepts/mcp]]
- **Prefect**: builds FastMCP and hosts FastMCP servers via Prefect Horizon Cloud; Prefect is also framed separately as runtime infrastructure (durable execution, checkpoints) for long-running agents. [[wiki/entities/prefect]]
- **Claude Code**: acts as an MCP client that can drive tools exposed by a FastMCP server, and stands as the "prebuilt orchestrator" alternative to a custom FastMCP-client orchestrator. [[wiki/entities/claude-code]]
- **Skills**: FastMCP's `SkillsDirectoryProvider` packages the `SKILL.md` convention as MCP resources — a different mechanism from Claude Code's own auto-detected, agentically-invoked `.claude/skills/`. [[wiki/concepts/skills]]
- **Orchestration**: FastMCP sits on both sides of the still-unresolved question of where a custom orchestrator should live — as the server framework, and as the toolkit for building the client that calls it. [[wiki/concepts/orchestration]]

> Synthesis: across all six sources currently in this wiki, FastMCP is never the subject of an argument — it is the connective tissue cited in passing at the server layer, the client layer, the skills-packaging layer, and the deployment layer, which is itself a signal of how settled a default it has become in these authors' practice.
