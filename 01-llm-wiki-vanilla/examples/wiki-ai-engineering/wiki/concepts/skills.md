---
type: concept
title: Skills
description: A convention for packaging reusable, portable capability instructions — typically a `SKILL.md` file — that an agent harness loads and invokes natively, outside the MCP protocol.
aliases: ["Skills", ".claude/skills", "SKILL.md"]
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/cli]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 4
---

# Skills

> Reusable domain knowledge packaged as a simple file — real, widely adopted, and deliberately absent from the MCP spec.

## Definition

A skill is a folder (typically holding a `SKILL.md`) that packages a specific, reusable capability or workflow for an agent to invoke — but it is not an MCP protocol primitive. Sources disagree on whether that matters: the protocol-literal framing treats a skill as just a prompt, a resource, or a composite tool wearing a packaging label, while the practitioner framing treats "skills" as one of three genuinely distinct connectivity layers alongside CLI and MCP. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]], [[wiki/sources/the-future-of-mcp-vs-skills]]

Multiple independent coding agents converged on the same folder-plus-`SKILL.md` shape without going through MCP at all, which suggests skills are less a protocol feature than a cross-ecosystem convention. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

## Key claims

- Skills have no protocol-level existence in MCP: the raw spec never mentions them, so implementing a "skill" means choosing an existing primitive — a prompt, a resource, or a composite tool. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Multiple coding agents (Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex) independently converged on the same folder-plus-`SKILL.md` convention, each handling it natively rather than through MCP. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- In a connectivity architecture spanning skills, CLI, and MCP, skills are the layer for reusable domain knowledge — "capture specific capabilities put into a very simple file" — distinct from CLI's local-execution role and MCP's rich-semantics/governance role. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Skills work well when the underlying logic is simple enough to fit in files; once business logic gets specific enough (e.g., a bespoke GraphRAG memory store on cloud infrastructure), MCP tools become the better fit than skills alone. [[wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/entities/mcp]]**: skills are commonly packaged as MCP resources or shipped through MCP servers, without being an MCP primitive themselves. [[wiki/entities/mcp]]
- **[[wiki/concepts/agent-connectivity]]**: skills are one of the three layers (with CLI and MCP) this wiki argues agents should combine. [[wiki/concepts/agent-connectivity]]
- **[[wiki/concepts/cli]]**: both are lightweight, portable mechanisms, contrasted with MCP's server-hosted governance model. [[wiki/concepts/cli]]

> Synthesis: The one idea every source in this wiki agrees needs a name, precisely because the protocol itself declines to define one.
