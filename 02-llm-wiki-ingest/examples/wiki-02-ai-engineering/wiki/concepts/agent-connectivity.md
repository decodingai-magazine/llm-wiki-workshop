---
type: concept
title: Agent Connectivity
description: The principle that agents should reach capabilities and external systems through several complementary mechanisms — skills, CLI, and MCP — rather than one universal connectivity layer.
aliases: []
sources:
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/orchestration]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 2
---

# Agent Connectivity

> "Connectivity is not one thing" — the best agents reach capabilities and external systems through several complementary mechanisms (skills, CLI, MCP) rather than a single universal one.

## Definition

Both source pages converge on the same core claim, in near-identical language: connectivity is not a single mechanism to be chosen but a set of complementary layers an agent combines. [[wiki/sources/the-future-of-mcp-vs-skills]] frames this as the direct consequence of a 2026 shift — agents moving from 2025's local, sandboxed "coding agent" era into general knowledge work, where the critical requirement becomes reaching several SaaS applications and a shared drive rather than a local compiler loop. It explicitly rejects any "one true connectivity mechanism" and lays out three layers: skills for packaged capability knowledge, CLI for sandboxed local execution, and MCP for rich semantics, platform independence, and enterprise governance. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] frames the same three mechanisms slightly differently — as one of four independently decomposable layers in a broader agent architecture (Presentation, Harness + Runtime, Connectivity, MCP Servers), with MCP acting as connective tissue across all four; within that Connectivity layer, skills cover reusable domain knowledge, CLIs cover local host capabilities, and MCP clients cover auth, resources, tasks and UI.

## Key claims

- Connectivity is explicitly modeled as multiple complementary layers rather than one universal mechanism: skills, CLI and MCP each cover a distinct job, and 2026-era agents combine all three instead of picking one. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- The 2026 shift from coding agents to general knowledge-work agents makes connectivity the primary bottleneck, because such agents need to reach several SaaS applications and a shared drive rather than a local, sandboxed compiler. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Single-mechanism agents underperform; the best agents "use all of it — skills, CLI, MCP — together." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Connectivity is positioned as one of four independently decomposable layers of agent architecture (alongside Presentation, Harness + Runtime, and MCP Servers), with MCP serving as the connective tissue between them. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

## Relationships

- **MCP**: one of the three connectivity mechanisms — used when rich semantics, platform independence, or enterprise governance (auth, resources, tasks) are needed. [[wiki/concepts/mcp]]
- **Skills**: the connectivity mechanism for packaged/reusable capability knowledge. [[wiki/concepts/skills]]
- **CLI**: the connectivity mechanism for sandboxed local execution and host capabilities. [[wiki/concepts/cli]]
- **Orchestration**: connectivity choices interact with how an agent's harness/runtime loop is structured — [[wiki/sources/the-future-of-mcp-vs-skills]] discusses both under the same 2026-agent framing. [[wiki/concepts/orchestration]]

> Synthesis: Both source pages state the "connectivity is not one thing" thesis almost identically — same three mechanisms, same 110M-download MCP growth figure, same FastMCP/Python-SDK detail — and one source page explicitly attributes its account to MCP co-creator David Soria Parra at an AI Engineering conference talk, while the other is an unattributed but clearly talk-style transcript covering the same ground. This looks like one underlying talk reaching the wiki through two different write-ups (a fuller transcript and a condensed quote distillation) rather than two independent voices reaching the same conclusion; treat the near-verbatim agreement here as corroboration of transcription, not as two independent confirmations of the underlying claim.
