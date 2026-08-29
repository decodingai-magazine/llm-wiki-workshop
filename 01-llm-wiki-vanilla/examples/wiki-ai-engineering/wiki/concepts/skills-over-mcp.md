---
type: concept
title: Skills over MCP
description: Shipping skill files from an MCP server so procedural knowledge can be updated centrally — promising in the roadmap, inert in today's clients.
aliases: [SkillsDirectoryProvider]
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
related:
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/agentic-invocation]]"
  - "[[wiki/entities/fastmcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 3
---

# Skills over MCP

> Let the server ship the manual with the tools — "this is how you're supposed to use this" — updated centrally, with no plugin mechanism to register.

## Definition

The idea is a direct response to large servers: if you expose many tools, ship
the procedural knowledge for using them alongside, and update it whenever the
server changes [[wiki/sources/the-future-of-mcp-vs-skills]]. FastMCP implements
it today by exposing skill directories as MCP **resources**
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]].

The gap between the two sources is the whole story. One presents skills over MCP
as an exciting extension on the roadmap; the other checks what a client does with
it and finds the mechanism inert — resources are listable but never invoked by
the model, so a skill shipped this way sits in a dead zone until clients change.

## Key claims

- Shipping skills over MCP lets a server author update procedural knowledge continuously, without relying on a plugin registration mechanism. [[wiki/sources/the-future-of-mcp-vs-skills]]
- FastMCP's `SkillsDirectoryProvider` exposes each skill as `skill://name/SKILL.md` plus a manifest resource. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Because MCP resources are not agentically consumed, a skill shipped as a resource must be named by the user or read programmatically. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- The workaround today is duplication: expose skills as resources for cross-client discovery, and copy them into `.claude/skills/` for native invocation. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Skills over MCP is named as a client-specific extension in the protocol roadmap rather than a core primitive. [[wiki/sources/the-future-of-mcp-vs-skills]]
- The pitch, restated: the server becomes the source of truth for both what it can do and how to drive it, which removes the plugin-and-registry dance. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Open governance question: what it means for safety when a server can change the agent's behaviour remotely. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/agent-skills]]**: the user-owned layer this pattern tries to serve from the vendor side.
- **[[wiki/concepts/agentic-invocation]]**: the property the pattern currently lacks.

## Tensions

- Roadmap optimism [[wiki/sources/the-future-of-mcp-vs-skills]] versus implementation reality [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]. Both can be true — the mechanism ships, the invocation semantics do not exist yet.

> Synthesis: This is the wiki's sharpest example of protocol-versus-client drift: the server side of the feature exists today and the client side is the part that has to change, which is the harder half.
