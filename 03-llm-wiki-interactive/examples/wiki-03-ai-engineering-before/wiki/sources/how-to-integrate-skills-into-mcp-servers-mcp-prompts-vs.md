---
type: source
title: "How to integrate Skills into MCP servers: MCP Prompts vs. Skills"
description: Argues that MCP has no native Skills primitive — FastMCP packages skills as prompts, resources or tools, and Claude Code only auto-invokes MCP tools and its own .claude/skills, never MCP resources or prompts.
origin: local
original_path: data_input_examples/notes/02-medium/How to integrate Skills into MCP servers MCP Prompts vs. Skills.md
source_url:
authors: []
published_date:
raw_file: raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs.md
created: 2026-08-29T16:08:31Z
timestamp: 2026-08-29T16:08:31Z
entities:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]"
concepts:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]"
---

# How to integrate Skills into MCP servers: MCP Prompts vs. Skills

> [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs|Raw]] · local

## Summary

The note works through a recurring confusion when building an MCP server: "Skills"
feel like they should be a fourth MCP primitive alongside Tools, Resources and
Prompts, but the protocol has no such thing. It first maps how Claude Code treats
each primitive — only MCP Tools and its own `.claude/skills/` directory are
auto-detected *and* invoked agentically; MCP Resources and MCP Prompts are both
listable but require the user (or an explicit read call) to trigger them. It then
shows that FastMCP's `SkillsDirectoryProvider` is not a new protocol concept but a
packaging convention that exposes a skill folder as MCP resources
(`skill://name/SKILL.md`, `_manifest`, and supporting files) — which lands skills
in a gap where they are discoverable by any MCP client but not autonomously
callable by Claude Code. The second half is a pasted-in architecture guide (framed
around the author's own "AI Twin" MCP server) that works through where tool code
actually executes, contrasts server-side orchestration (one composite `@mcp.tool`
running several steps in a single request) against client-side, prompt-guided
orchestration (multiple round-trips where the AI decides the next call), and lands
on a concrete recommendation: for deterministic pipelines, build composite tools;
reserve MCP prompts for workflows the user explicitly triggers or the AI should be
free to reorder.

## Key claims

- Claude Code only auto-invokes MCP Tools and its native `.claude/skills/`
  directory agentically; MCP Resources and MCP Prompts are both auto-detected/
  listable but never triggered without an explicit reference or user action.
  [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Summary Table|cite]]
- "Skills" do not exist in the raw MCP protocol (revision 2025-11-25) — the word
  appears in no protocol message, schema type, capability declaration or method
  definition. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills Are NOT Part of the MCP Protocol|cite]]
- FastMCP packages skills as MCP resources via `SkillsDirectoryProvider`; by
  FastMCP's own description this is "a packaging decision, not an architectural
  one," so a skill exposed this way is discoverable by any MCP client but not
  agentically callable by Claude Code. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|cite]]
- Because MCP resources aren't consumed agentically, skills shipped through
  `SkillsDirectoryProvider` fall into a "dead zone" — neither developer-owned
  instructions (which belong in tool descriptions or prompts) nor user-owned
  skills (which belong in `.claude/skills/`). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skill Ownership: Developer vs User|cite]]
- Five coding agents (Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex) have
  independently converged on a folder-plus-`SKILL.md` convention, but each handles
  it as a native, agent-specific mechanism rather than through MCP.
  [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills as a Cross-Agent Ecosystem Convention|cite]]
- For deterministic pipelines, the note recommends server-side orchestration —
  one composite MCP tool calling helper functions in a single request, which
  guarantees execution order and can't be skipped or reordered by the model —
  over client-side, prompt-guided orchestration, which costs multiple round-trips
  and lets the AI reorder or drop steps.
  [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Server-Side Orchestration (Recommended for Deterministic Pipelines)|cite]]

## Notable quotes

> "A skill is not a separate concept. It's a prompt, a resource, or a bundle of
> both. Calling them 'skills' is a packaging decision, not an architectural one."
> — [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|location]]

> "There is no `/skills/list` or `/skills/execute` in the MCP protocol."
> — [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills Don't Exist in MCP|location]]

## Connections

- **Entities**: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]
- **Concepts**: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/skills]]

> Synthesis: The note's second half (the "AI Twin" guide) restates the same
> Tools/Resources/Prompts distinction from its first half in more tutorial form —
> same conclusion, more code — so treat them as one argument rather than two
> independent sources of evidence.
