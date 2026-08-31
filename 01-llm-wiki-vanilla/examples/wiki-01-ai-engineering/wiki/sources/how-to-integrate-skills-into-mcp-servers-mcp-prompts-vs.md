---
type: source
title: "How to integrate Skills into MCP servers: MCP Prompts vs. Skills"
description: Skills are not an MCP protocol primitive — they are a packaging convention (usually a prompt, a resource, or both) that each agent harness handles natively.
origin: local
original_path: data_input_examples/notes/01-easy/How to integrate Skills into MCP servers MCP Prompts vs. Skills.md
source_url:
authors: []
published_date:
raw_file: raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs.md
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]"
concepts:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
  - "[[wiki/concepts/orchestration]]"
---

# How to integrate Skills into MCP servers: MCP Prompts vs. Skills

> [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs|Raw]] · local

## Summary

This note works through where "Skills" actually live in the MCP architecture, prompted by the question of whether an MCP server should expose them as prompts, resources, or something else. It opens with how Claude Code treats each MCP primitive differently — only Tools and native `.claude/skills/` are invoked agentically — then pulls in a longer imported guide arguing that Skills have no protocol-level existence at all: they're a packaging convention that FastMCP and several other coding agents have converged on independently.

The second half is an architectural deep-dive on tool execution — where code runs, server-side vs. client-side orchestration, and concrete FastMCP patterns (atomic tools, composite tools, a `SkillsDirectoryProvider`) for building a "skills"-flavored MCP server without inventing a new primitive.

## Key claims

- Claude Code auto-detects MCP Tools and native `.claude/skills/` and calls both agentically, but MCP Resources and Prompts, though auto-detected, must be explicitly invoked by the user. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#MCP Primitives vs Claude Code Native Skills|cite]]
- "Skills" do not exist anywhere in the raw MCP specification (revision 2025-11-25) — the word appears in no protocol message, schema type, capability declaration, or method definition. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills Are NOT Part of the MCP Protocol|cite]]
- FastMCP packages skills as MCP resources (`skill://name/SKILL.md`, `_manifest`, supporting files) — a packaging convention layered on the protocol, not a new architectural primitive. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|cite]]
- Multiple coding agents (Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex) independently converged on a folder-with-`SKILL.md` convention, but each handles it natively rather than through MCP. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills as a Cross-Agent Ecosystem Convention|cite]]
- Server-side orchestration — one composite tool running every step in a single request — guarantees execution order; client-side, tool-by-tool orchestration risks the model skipping or reordering steps. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Client-Side vs. Server-Side Orchestration|cite]]
- Developer-owned instructions belong in MCP tool descriptions or prompts; user-owned workflows belong in `.claude/skills/` — FastMCP's `SkillsDirectoryProvider` blurs this line because MCP resources aren't consumed agentically by Claude Code. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skill Ownership: Developer vs User|cite]]

## Notable quotes

> "A skill is not a separate concept. It's a prompt, a resource, or a bundle of both. Calling them 'skills' is a packaging decision, not an architectural one."
> — [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]
- **Concepts**: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]], [[wiki/concepts/orchestration]]

> Synthesis: The most protocol-literal treatment in the wiki of the "skills aren't MCP" claim — it grounds the looser, talk-derived framing in [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/sources/the-future-of-mcp-vs-skills]] and [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] in the actual spec text.
