---
type: entity
title: FastMCP
description: The de facto default Python SDK for building MCP servers and clients, maintained by Prefect.
aliases:
  - FastMCP
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/prefect]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 4
---

# FastMCP

> A third-party Python SDK for MCP that has become the practical default, by the account of MCP's own co-creator.

## Definition

FastMCP is a Python framework for building MCP servers and clients, maintained by Prefect. It has become popular enough that MCP co-creator David Soria Parra called it "way better than our Python SDK that we shipped," and its lessons are informing the official SDK's own v2 rework. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/the-future-of-mcp-vs-skills]]

Beyond raw protocol plumbing, FastMCP adds its own conventions on top — notably a `SkillsDirectoryProvider` that packages "skills" as MCP resources, even though skills are not an MCP primitive. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

## Key claims

- FastMCP packages "skills" as MCP resources via a `SkillsDirectoryProvider`, exposing `skill://name/SKILL.md`, a `_manifest`, and supporting files — a packaging convention layered on the protocol, not a new primitive. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- FastMCP is cited by MCP co-creator David Soria Parra as "way better than our Python SDK that we shipped," and has become the practical default Python implementation for MCP servers. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- The official Python SDK's forthcoming v2 rework is informed partly by lessons learned from FastMCP's design. [[wiki/sources/the-future-of-mcp-vs-skills]]
- FastMCP implements both the MCP server side of a memory pipeline (tools, prompts) and the client-side connector for a custom orchestrator, using only its client utility on the client side. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **[[wiki/entities/mcp]]**: the practical default SDK for implementing MCP servers in Python. [[wiki/entities/mcp]]
- **[[wiki/entities/prefect]]**: built and maintained by Prefect. [[wiki/entities/prefect]]

> Synthesis: Framed less as a competitor to the official SDKs and more as their de facto reference implementation — popular enough that its own conventions (like skills-as-resources) now need explaining relative to the base protocol.
