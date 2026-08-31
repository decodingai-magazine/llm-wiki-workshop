---
type: concept
title: CLI
description: A command-line connectivity mechanism for agents — best suited to local, sandboxed, pre-trained execution, but structurally weak at governed distribution to many users.
aliases: []
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:10:00Z
source_count: 7
---

# CLI

> One of three complementary agent connectivity mechanisms — strong for local, sandboxed, pre-trained execution; weak for governed distribution to many users.

## Definition

The CLI is treated not as a competitor to MCP or skills but as one of three complementary connectivity primitives an agent reaches through. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]] and [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] define its niche the same way: reach for it where a sandbox/execution environment can be assumed and the target is local, pre-trained, or composable — MCP's job is auth/governance, skills' job is packaged knowledge. [[wiki/sources/why-mcp-is-not-dead]] gives a compatible, sharper framing: CLI is right at *personal, single-user* scale, wrong once access must be distributed and governed across many users, because "CLIs have never had a good story for centralized distribution or control." Three further sources — two articles plus the codebase, all the same *Building a Coding Agent From Scratch* course — ground this in a build: the CLI is Decode's operating surface, styled directly on Claude Code (concrete Click entrypoint under Key claims). [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- CLI is one of three complementary connectivity primitives (with skills and MCP), not a competing alternative — 2026 agents combine all three rather than picking one; CLIs also have a structural presentation limit ("if you're a CLI you just have a hard time rendering HTML"), part of why UI is pushed into a separate MCP Apps layer instead. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- For personal, single-user setups a CLI is often simpler and genuinely sufficient — the "MCP is dead" experience is a fact about a use case CLI already covers, not about MCP being obsolete; CLIs have never had a good story for centralized distribution or governance, so requiring many customers to install one plus a pile of markdown files is unworkable at business scale. One author keeps local files and dev-time infra (Obsidian, MongoDB, Prefect) CLI-driven for that reason, and siloed/hosted services through MCP. [[wiki/sources/why-mcp-is-not-dead]]
- Decode, a from-scratch coding-agent harness benchmarked against Claude Code, OpenCode, Pi and Aider, resumes session state via `decode --resume <session_id>` (styled on Claude Code). The codebase confirms this as one Click entrypoint (`src/decode/cli.py`) with a centralized headless guard chain so its three surfaces — bare `decode`, `decode run` (optional `--hitl` gate), `decode replay` — can't drift apart. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **Agent connectivity**: CLI is one of three mechanisms — with skills and MCP — in the "connectivity is not one thing" model. [[wiki/concepts/agent-connectivity]]
- **MCP**: opposite ends of the same distribution question — CLI wins for personal/local access, MCP wins once access must be governed across many users. [[wiki/concepts/mcp]]
- **Skills**: used alongside (not instead of) MCP; skills package reusable domain knowledge, CLI provides local execution. [[wiki/concepts/skills]]
- **Agent harness**: in Decode, the CLI is the harness's own operating surface — the Click entrypoint that starts, runs and resumes sessions. [[wiki/concepts/agent-harness]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: Three sources ([[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]) write up one David Soria Parra talk — one voice, not three confirmations. [[wiki/sources/why-mcp-is-not-dead]] is a genuinely independent witness, corroborating the same CLI niche from an unrelated argument. The two Decode-course articles and the Decode repo ([[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]) trace to one project, not independent confirmation — but the repo is a different *kind* of evidence: running implementation, not another description of one.
