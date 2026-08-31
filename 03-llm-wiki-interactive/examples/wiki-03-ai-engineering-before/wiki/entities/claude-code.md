---
type: entity
title: Claude Code
description: Anthropic's coding-agent harness — an MCP client/orchestrator and a comparison baseline for permission modes, memory and sandboxing in six article sources and a four-lesson course, and, per an independent open-source reconstruction, a harness whose own internal design (permission gate, sandboxing, skills, subagents, compaction) has been rebuilt from its leaked source.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/claude-md]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/agent-sandboxing]]"
  - "[[subagents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-memory]]"
created: 2026-08-29T16:14:10Z
timestamp: 2026-08-29T17:09:17Z
source_count: 11
---

# Claude Code

> An MCP client and coding-agent harness layering its own native extension mechanisms — skills, hooks, CLAUDE.md — on top of (and sometimes instead of) MCP; per one independent codebase and its accompanying course, also a design source and comparison baseline for a from-scratch reconstruction of a coding-agent harness.

## Definition

Across the six original article-style sources, Claude Code appears in two consistent roles: as one of several possible **MCP clients/harnesses** capable of driving a custom MCP server (alongside OpenCode, Cursor, OpenClaw) [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]], and as a **pre-built orchestrator** an agent architecture can adopt wholesale instead of writing a bespoke client [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]. No source in this group treats it as a plain chat client — every engagement centers on a capability specific to Claude Code that sits outside the raw MCP protocol.

A seventh, structurally different source adds a third framing. The `decode` teaching codebase — an open-source coding agent built from scratch across an 8-article course — states an explicit debt to Claude Code's leaked source when designing its own harness, and the repo page's own synthesis calls the result "the closest readable reconstruction of that design the wiki has." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] Unlike the article sources above, which engage Claude Code only from the outside (as an MCP client, or as something steered via CLAUDE.md), this source is evidence *about* Claude Code's own internals — refracted through someone else's reconstruction, not Claude Code's own documentation.

Four newly-added lesson articles from that same `decode` course add a fourth, narrower framing: Claude Code as a **named comparison baseline**. Each lesson cites a specific Claude Code behavior — its permission modes, its auto-memory, its already-sandboxed `bash` calls — as the precedent or feature-parity target for the equivalent piece of `decode`'s own harness, rather than studying Claude Code as a subject in its own right. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]

## Key claims

- Claude Code is the only harness, in one report's setup, wired with all three integration layers — the MCP server, harness-specific skills (tool-selection guidance), and harness-specific hooks (e.g. a `Stop` hook that auto-ingests a conversation once per session) — capabilities OpenCode and Cursor don't get, falling back to tool docstrings alone. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/agentic-graphrag-via-mcp-servers]]
- Claude Code auto-invokes only MCP Tools and its own native `.claude/skills/` directory agentically; MCP Resources and MCP Prompts are listable but never triggered without an explicit reference or user action. It is also one of five coding agents (with GitHub Copilot, Gemini CLI, Cline, Codex) that independently converged on a folder-plus-`SKILL.md` convention, each as a native, agent-specific mechanism outside MCP. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Claude Code's behavior is steered via a handwritten `CLAUDE.md`; one builder replaced an entire MCP server for database access with a single `CLAUDE.md` line instructing the agent to use the database's own CLI (`mongosh`), relying on Claude Code's existing shell access. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- In a design draft weighing where a custom orchestrator should live, Claude Code is named as the pre-built-orchestrator option — an MCP client that could call a packaged orchestrator tool directly — as an alternative to a bespoke Python/FastAPI or TypeScript client. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Claude Code manages purely local files (e.g. Obsidian) directly via its own CLI, in contrast to siloed third-party services (Notion, Readwise) that are only safely reachable through their MCP servers; it is also named as one of several harnesses (with OpenCode, OpenClaw) an MCP server distributes access to at once. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]
- Referenced as one of the harnesses relevant to a four-layer (presentation/harness/connectivity/servers) architecture of future AI apps, drawn from a secondhand account of David Soria Parra's "The Future of MCP" talk — no Claude-Code-specific detail beyond that framing. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- `decode`, a ~12.2k-line teaching codebase, explicitly credits Claude Code's leaked source as a design influence on its own harness: a permission gate with deny-then-allow-then-mode precedence, a pluggable sandbox seam (none/docker/Modal), skills implementing three-tier progressive disclosure (catalog → body → bundled references on demand), subagent fan-out to narrowed, read-only children, and a two-tier context-compaction cascade. This is the repo page's own framing, not a documented statement from Anthropic about Claude Code's internals. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Claude Code already wraps every `bash` call in an OS-level jail (Seatbelt on macOS, bubblewrap on Linux) — cited as evidence that this kind of sandboxing is already standard practice among coding agents, not a novel proposal — even though the same author runs Claude Code raw, unsandboxed, as his own daily driver. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]
- Claude Code recurs across three lesson articles of the same course as a named baseline rather than a subject: its permission modes (default/edit/auto) are the model for `decode`'s own ask/allow/deny gate; its auto-summarizing memory behavior is cited as the precedent for `decode`'s own capped `.decode/MEMORY.md`; and "Claude-Code/OpenCode-style" memory, skills and sandboxing are named as the feature set a minimalist early lesson deliberately does not yet build. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]

## Relationships

- **MCP**: Consistently positioned as one possible MCP client among several — the protocol is portable, but what a client does with it (skills, hooks, auto-invocation rules) is not. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]
- **Skills**: Claude Code's `.claude/skills/` is repeatedly contrasted with MCP's lack of a native skills primitive — skills are Claude-Code-owned (and a cross-agent convention), not something MCP itself defines. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]
- **CLAUDE.md**: Functions as Claude Code's primary steering file, argued by one source to be more effective, signal-dense infrastructure access than a bespoke MCP server. [[wiki/concepts/claude-md]]
- **Agent harness / Permission gate / Agent sandboxing / Subagents / Context compaction**: the original article sources describe Claude Code only from the outside; `decode`'s claimed debt to its leaked source is this wiki's only lead — indirect as it is — on what those internals might look like. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **Agent memory**: `decode`'s own auto-extracted, capped `MEMORY.md` is explicitly described as mirroring Claude Code's auto-memory, another indirect, once-removed data point rather than a documented account. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

> Synthesis: Five of the six original article-style sources trace to what reads as one practitioner's own recurring project (GraphRAG / "Personal Assistant" / "AI Twin"), so despite six citing pages this is closer to one author's consistent experience with Claude Code than six independent perspectives. The David Soria Parra talk writeup is the only outside voice among them, and it barely engages with Claude Code specifically. The four newly-added lesson articles are the *same* `decode` course as the ARCHITECTURE.md repo page already on this wiki — one author, one codebase, four installments — so they reinforce the existing seventh voice rather than add an eighth; none treats Claude Code as its subject, each only borrows one fact about it (a permission-mode name, an auto-memory behavior, an already-sandboxed `bash` call) to motivate a design choice in `decode` itself. Treat the harness-internals picture across all five `decode`-course pages as one consistent but once-removed voice — a debt credited to "leaked source" and comparison points drawn against Claude Code's observed behavior, not a primary account from Anthropic.
