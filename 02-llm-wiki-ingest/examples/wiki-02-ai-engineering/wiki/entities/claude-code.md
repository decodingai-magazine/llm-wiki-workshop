---
type: entity
title: Claude Code
description: Anthropic's agentic coding harness — an MCP client that treats Skills, hooks, and CLAUDE.md as first-class connectivity/instruction layers, and the harness most often cited as prior art in the wiki's Decode-course sources.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/article-run-coding-agents-safely]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/claude-md]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/sandboxing]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/decode]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T19:20:00Z
source_count: 10
---

# Claude Code

> Anthropic's coding-agent harness: an MCP client with agentically-invoked Skills, hooks, and a CLAUDE.md instruction file layered on top of MCP tools — and the harness most frequently used as prior art or benchmark by the wiki's other sources.

## Definition

Claude Code is Anthropic's agentic coding harness — a CLI/IDE-facing agent loop that consumes MCP servers as a client, while adding harness-specific layers no plain MCP client gets. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] describes it as one of two interchangeable ways to drive a composed MCP toolset (the other being a custom FastMCP-based orchestrator) — "from the user's perspective, just MCP clients." Beyond its MCP-client role, four sources in Paul Iusztin's *Building a Coding Agent From Scratch* course ([[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-the-coding-agent-loop]], [[wiki/sources/article-run-coding-agents-safely]], [[wiki/sources/article-context-engineering-for-coding-agents]]) repeatedly cite Claude Code as the existence-proof/reference implementation their own harness, Decode, is benchmarked against for TUI style, session persistence, sandboxing, and steering.

## Key claims

- Claude Code agentically auto-invokes MCP **Tools**, but only auto-detects (without agentic use) MCP **Resources** and **Prompts** — both need explicit user triggering — while its own `.claude/skills/` folders are auto-detected *and* agentically invoked, and are one of several independently-converged coding-agent implementations of a folder-with-`SKILL.md` convention (alongside Copilot, Gemini CLI, Cline, Codex). [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Claude Code shipped progressive tool discovery (a `tool_search`-style capability loading tool definitions on demand instead of every schema up front) and saw a large reduction in tool-context usage. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Claude Code has native shell access, so one handwritten CLAUDE.md line ("Use `mongosh` to interact with MongoDB directly through the CLI") let it use a database CLI unprompted — to validate infra, debug a silent indexing bug, and inspect data shapes — with no MCP server built for the job. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- On top of a universal MCP-server layer, one author built two Claude-Code-specific enrichments — a Skill (tool-selection guidance) and a Stop hook (auto-triggers a memory-ingestion tool) — that harnesses like OpenCode, Cursor, and Windsurf go without. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Claude Code is named alongside OpenCode and OpenClaw as one of the harnesses that governed, business-scale MCP distribution targets, with the recommendation to use MCP, Claude Code skills, and CLIs together rather than any one exclusively. [[wiki/sources/why-mcp-is-not-dead]]
- Locally, Claude Code (like Codex CLI) already wraps every `bash` call in an OS-level jail (Seatbelt on macOS, bubblewrap on Linux); a Claude Code session firing an unsandboxed cleanup command that deleted half the author's Obsidian notes is the motivating anecdote for sandboxing coding agents at all — yet the same author, "as a Claude Code power user," still runs it unsandboxed locally in git/Obsidian-Sync-versioned folders for everyday work. [[wiki/sources/article-run-coding-agents-safely]]
- Decode's design borrows explicitly from Claude Code in three places: its TUI follows Claude Code's append-to-scrollback pattern (vs. full-screen UIs like Amp/OpenCode); its resumable, append-only JSONL session log is modeled on how Claude Code does session management "replacing a database"; and its steering queue mirrors how Claude Code ranks queued input so user messages never starve mid-task. [[wiki/sources/article-the-coding-agent-loop]], [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **MCP**: Claude Code is an MCP client; it auto-invokes Tools agentically but not Resources/Prompts, and is one of two interchangeable ways (with a custom FastMCP orchestrator) to drive a composed toolset. [[wiki/concepts/mcp]], [[wiki/entities/fastmcp]]
- **Skills**: `.claude/skills/` is Claude Code's own Skills implementation — auto-detected and agentically invoked, functionally closer to Tools than to any native MCP primitive, and one of several independent per-harness implementations of the same folder convention. [[wiki/concepts/skills]]
- **CLI**: Claude Code's built-in shell access makes CLI tools (mongosh, psql, etc.) a lower-overhead alternative to a bespoke MCP server for local/dev workflows. [[wiki/concepts/cli]]
- **Sandboxing**: Claude Code already jails individual `bash` calls (Seatbelt/bubblewrap) but does not sandbox the whole session by default — a gap a Claude Code incident (deleted notes) is cited to motivate. [[wiki/concepts/sandboxing]]
- **Decode / agent harness design**: Decode's TUI, session log, and steering queue are each explicitly benchmarked against Claude Code's behavior. [[wiki/entities/decode]], [[wiki/concepts/agent-harness]]

> Synthesis: Eight of these ten sources trace to one author (Paul Iusztin) — four project notes on his GraphRAG/digital-twin memory system ([[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]], [[wiki/sources/why-mcp-is-not-dead]]) plus four lesson articles from his separate Decode coding-agent course. They corroborate on *usage patterns* (shell access, skills+hooks, benchmark-worthy harness decisions) but are largely one voice describing two different projects, not independent witnesses. Only [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] (protocol-level Tools/Resources/Prompts claims, partly answered by a colleague) and [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] (David Soria Parra's talk, transcribed by the same author) stand as genuinely separate perspectives.
