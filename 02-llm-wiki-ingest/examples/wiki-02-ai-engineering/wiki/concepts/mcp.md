---
type: concept
title: MCP (Model Context Protocol)
description: An open protocol for connecting AI agents to tools, data and other systems through three primitives (Tools, Resources, Prompts), which the wiki's sources treat as one leg of a connectivity stack rather than a universal mechanism.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/code-mode]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/david-soria-parra]]"
  - "[[wiki/entities/claude-code]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 9
---

# MCP (Model Context Protocol)

> Multiple framings — see Definition

## Definition

At the protocol level, MCP defines exactly three primitives: Tools (AI-controlled — an agent decides when to call them), Resources (application-controlled — listable but not agentically invoked), and Prompts (user-controlled — must be explicitly triggered). There is no native "Skills" primitive; the word does not appear in the spec at all. What looks like "MCP shipping skills" — e.g. FastMCP's `SkillsDirectoryProvider`, which packages the cross-agent `SKILL.md` folder convention as `skill://` Resources — is a packaging decision layered on top of Resources, not a fourth protocol concept, and Claude Code does not agentically invoke it the way it invokes its own native `.claude/skills/`. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

Architecturally, sources place MCP at different points on a spectrum. One cluster — three notes tracing to the same David Soria Parra talk (flagged below) — frames MCP as one of three-to-four co-equal "connectivity" layers (alongside skills and CLI) that any serious 2026 agent combines, valued for auth, remote/hosted access, rich semantics and platform independence. A second cluster is more skeptical of MCP as a default: it argues MCP earns its place specifically for **governed, multi-tenant distribution of business logic** — for personal or dev-time access, a CLI is not just adequate but strictly simpler, and reaching for an MCP server there is over-engineering. [[wiki/sources/why-mcp-is-not-dead]], [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]

## Key claims

- No native Skills primitive exists in MCP; "skills over MCP" is Resources-shaped packaging (FastMCP's `SkillsDirectoryProvider`), discoverable by any MCP client but not agentically callable by Claude Code the way `.claude/skills/` is. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- "Connectivity is not one thing": the best 2026 agents combine skills, CLI and MCP together rather than picking one; MCP's specific edge is auth, remote/hosted access, rich semantics, platform independence and enterprise governance. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] — **same-voice caveat**: all three explicitly anchor on David Soria Parra's talk, so this is one witness triangulated three ways, not three independent corroborations.
- MCP earns its place at business scale specifically for governed distribution to many users — requiring customers to install a CLI and drop markdown files on every machine is unworkable and forecloses governance/security discussions entirely. [[wiki/sources/why-mcp-is-not-dead]]
- For coding-agent development workflows specifically, a bespoke MCP server for database access (schemas, connection handling, serializers, context-bloating response wrappers) is unnecessary: one CLAUDE.md line pointing the agent at the database's own CLI (`mongosh`, `psql`, `redis-cli`) is sufficient and was used unprompted to debug real issues. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- Good MCP servers should ship task-shaped composite tools (`schedule_meeting_with_summary`) rather than one-to-one REST wrappers (`POST /calendars/{id}/events`), since endpoint-shaped tools push low-level orchestration back onto the model. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]] (same-talk caveat as above)
- MCP servers should stay thin, logic-free delivery layers — tools extract context, delegate to existing business-logic functions, and serialize output — so the same code path runs identically via an MCP call or a batch pipeline (e.g. Prefect). [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- MCP is repeatedly proposed as the portable interface for a memory/context layer: pairing a unified memory (knowledge graph, embeddings, BM25) with an MCP server that exposes tools/resources/prompts/skills/apps makes that memory pluggable into any harness. [[wiki/sources/owning-your-context-layer]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]], [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Adoption is reported at 110M+ monthly downloads, growing faster than a comparable React milestone, driven substantially by third-party framework integrations (OpenAI's Agents SDK, Google's ADK, LangChain); FastMCP is repeatedly called the practical default Python implementation. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] — same-talk caveat; treat the figures as asserted, not independently verified by this wiki.

## Tensions

- **Default connectivity leg, or last resort?** The DSP-talk cluster treats MCP as one of the mechanisms every serious agent should be actively combining with skills and CLI. The skeptical cluster treats reaching for MCP as something to actively resist unless a specific governance/scale reason exists — for personal or dev-time work, both sources argue CLI wins outright rather than merely "also being an option." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] vs. [[wiki/sources/why-mcp-is-not-dead]], [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- **Does MCP "provide" skills?** Two sources speak loosely of an MCP server exposing or shipping skills as part of its standard offering. One source, reading the protocol spec directly, says this elides a real gap: MCP has no Skills primitive, and Resources-packaged skills are not agentically invoked by Claude Code the way native skills are. [[wiki/sources/owning-your-context-layer]], [[wiki/sources/why-mcp-is-not-dead]] vs. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- **Where does a custom orchestrator live?** One source gives a confident answer for deterministic pipelines — package them as a server-side composite tool, since client-side prompt-guided orchestration risks the model skipping or reordering steps. Another source, discussing an adaptive/planning orchestrator rather than a fixed pipeline, states the client-vs-server placement is genuinely unresolved even after building both. The two aren't strictly opposed — they answer different scopes of the same question — but neither should be read as settling the other's case. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] vs. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **Skills**: positioned as a complementary connectivity mechanism, not a shared implementation — MCP has no native Skills primitive. [[wiki/concepts/skills]]
- **CLI**: named repeatedly as the leaner default for personal, local or dev-time access that an MCP server would over-engineer. [[wiki/concepts/cli]]
- **Orchestration**: whether pipeline/agent logic belongs inside the MCP server (as a composite or single exposed tool) or on the client is a live, only partly resolved design question. [[wiki/concepts/orchestration]]
- **Agent Connectivity**: MCP is one leg of the "connectivity is not one thing" stack alongside skills and CLI. [[wiki/concepts/agent-connectivity]]
- **Context Layer / Agent Memory**: MCP is the proposed portable interface for exposing a unified memory or knowledge graph to any harness. [[wiki/concepts/context-layer]], [[wiki/concepts/agent-memory]]
- **FastMCP** (entity): the Python implementation used or endorsed across nearly every source that builds an MCP server. [[wiki/entities/fastmcp]]

> Synthesis: MCP is this wiki's hub concept, but its coverage is lopsided — three of the nine engaging sources trace to one David Soria Parra talk and should be read as one voice wearing three transcriptions, not three independent corroborations; the sharper, more independently-sourced disagreement is between "combine MCP with everything" (the talk cluster) and "avoid MCP unless governance or scale demands it" (the two skeptical, single-author sources).
