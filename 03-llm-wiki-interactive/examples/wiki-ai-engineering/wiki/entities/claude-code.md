---
type: entity
title: Claude Code
description: Anthropic's coding agent, used across these notes both as the reference harness for skills and as the prebuilt orchestrator you get to skip building.
aliases: []
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/choosing-an-inference-architecture-for-your-agents]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/retrieval-strategies]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/agentic-invocation]]"
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/entities/anthropic]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 16
---

# Claude Code

> A terminal coding agent that doubles, in these notes, as the reference implementation for how a harness treats skills, MCP tools, resources and prompts.

## Definition

Claude Code appears in three distinct roles across the sources: as the **client**
whose invocation rules define what "agentic" means in practice
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]; as a
**prebuilt orchestrator** you can plug into your own MCP server instead of
writing planning logic yourself
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]; and as one of
several interchangeable **harnesses of choice**, alongside OpenCode and OpenClaw
[[wiki/sources/why-mcp-is-not-dead]].

## Key claims

- Claude Code auto-detects and agentically invokes MCP tools and native `.claude/skills/`; MCP resources and prompts are listable but never invoked on the model's own initiative. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Skills placed in `.claude/skills/` are picked up automatically and invoked through the skill tool when judged relevant. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Using Claude Code as the orchestrator removes the client-side planning question entirely — it is only when you want your own planning logic that server-vs-client placement matters. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Progressive tool discovery showed a large context reduction in a Claude Code before/after comparison. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Local file work is handed to Claude Code directly (or an Obsidian CLI) rather than being routed through a server. [[wiki/sources/why-mcp-is-not-dead]]
- Skills and hooks are Claude Code-specific: the same MCP server runs in OpenCode or Cursor, but only Claude Code gets the tool-selection decision tree and lifecycle hooks. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- A `Stop` hook can end every session by extracting people, tasks, episodes and preferences into memory, so the graph grows with each conversation. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- One line in `CLAUDE.md` ("use `mongosh`") replaced an entire database MCP server, because the harness already has shell access. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- Switching from Claude Code to Codex or Gemini CLI should cost five minutes if the memory is portable — the harness is not the thing you own. [[wiki/sources/owning-your-context-layer]]
- Same model plus same servers plus a different harness produces wildly different product behaviour. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Given a CLI and one line of instruction, it independently seeded data, debugged missing indexes and verified pipeline output. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- It built a four-pipeline orchestration setup in ~2 hours with no human intervention, because it could restart the worker itself. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- The agentic build worked because the architecture was decided first — the agent supplied implementation, not design. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- Interactive harnesses justify per-token inference on cold-start grounds alone. [[wiki/sources/choosing-an-inference-architecture-for-your-agents]]
- It is one of the harnesses reverse-engineered to work out what a harness actually contains, alongside OpenCode, Pi and Aider. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Its append-to-scrollback TUI style is the one a from-scratch harness copies, keeping scrollback and search. [[wiki/sources/article-the-coding-agent-loop]]

## Relationships

- **[[wiki/concepts/agent-harness]]**: Claude Code is the concrete instance the notes reason about when they say "harness".
- **[[wiki/concepts/agent-skills]]**: `.claude/skills/` is the native, agentically-invoked home for user-owned procedures.
- **[[wiki/concepts/agentic-invocation]]**: its four-surface matrix is where the auto-detected / agentic distinction comes from.

> Synthesis: Claude Code functions in this wiki as the measuring stick — several architectural claims are really claims about what one specific harness will and will not call on its own.
