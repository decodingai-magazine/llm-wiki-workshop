---
type: source
title: "How to integrate Skills into MCP servers: MCP Prompts vs. Skills"
description: "Argues MCP has no native \"Skills\" primitive, only Tools/Resources/Prompts, and that Claude Code only auto-invokes Tools, so deterministic pipelines should be built as composite tools rather than MCP prompts."
origin: local
original_path: "data_input_examples/notes/02-medium/How to integrate Skills into MCP servers MCP Prompts vs. Skills.md"
source_url: null
authors: []
published_date: null
raw_file: raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/orchestration]]"
---

# How to integrate Skills into MCP servers: MCP Prompts vs. Skills

> [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs|Raw]] · local

## Summary

The note's central argument is that the MCP protocol has exactly three primitives — Tools (AI-controlled), Resources (application-controlled) and Prompts (user-controlled) — and no native "Skills" concept at all. Claude Code specifically only invokes MCP **Tools** agentically; MCP Resources and Prompts are listable but must be explicitly triggered by the user, while Claude Code's own `.claude/skills/` folders are both auto-detected and agentically invoked, putting them closer to Tools in practice than to any MCP primitive.

Against that backdrop, it walks through FastMCP's `SkillsDirectoryProvider`, which packages the cross-agent `SKILL.md` folder convention (also used natively by Copilot, Gemini CLI, Cline and Codex) as MCP **resources** — a packaging decision, not a protocol one, that leaves those skills discoverable by any MCP client but not agentically callable by Claude Code.

The second half applies this to a concrete case — designing an "AI Twin" MCP server — and argues for composite MCP **tools** over MCP prompts wherever a pipeline is deterministic: server-side orchestration (one `@mcp.tool` calling helper functions internally) gives one round trip and a guaranteed step order, while prompt-guided client-side orchestration costs multiple round trips and risks the model skipping or reordering steps.

## Key claims

- Claude Code auto-invokes MCP Tools agentically, but only auto-detects (without agentic use) MCP Resources and Prompts — both must be explicitly triggered by the user — while `.claude/skills/` is auto-detected *and* agentically invoked. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Summary Table|cite]]
- The word "Skills" does not appear anywhere in the MCP protocol spec (revision 2025-11-25); there is no `/skills/list` or `/skills/execute` method. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills Don't Exist in MCP|cite]]
- FastMCP implements skills as MCP resources via `SkillsDirectoryProvider`, exposing each skill directory as `skill://name/SKILL.md`, `skill://name/_manifest`, and `skill://name/path/to/file`. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|cite]]
- Multiple coding agents — Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex — have independently converged on a folder-with-`SKILL.md` convention, each handling it natively rather than through MCP. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills as a Cross-Agent Ecosystem Convention|cite]]
- For deterministic pipelines, server-side orchestration via a composite tool is recommended over prompt-guided client-side orchestration, since the latter needs multiple round trips and the AI "might skip/reorder steps". [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Server-Side Orchestration (Recommended for Deterministic Pipelines)|cite]]
- The note's concrete recommendation for its own "AI Twin" server: express the training/inference pipelines as composite tools and treat MCP prompts as optional, because the pipelines are deterministic and need guaranteed execution order. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#5. Answer to Paul's Question|cite]]

## Notable quotes

> "A skill is not a separate concept. It's a prompt, a resource, or a bundle of both. Calling them 'skills' is a packaging decision, not an architectural one."
> — [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|location]]

> "Tool code ALWAYS executes on the MCP server."
> — [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Where Code Runs|location]]

## Connections

- **Entities**: [[wiki/entities/fastmcp]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/skills]], [[wiki/concepts/orchestration]]

> Synthesis: Two stitched documents — a short reference comparing MCP primitives to Claude Code skills, and a longer architecture note answering a colleague's question about one specific MCP server design — but both converge on the same claim, that "skills" is a packaging convention over Tools/Resources/Prompts rather than a fourth primitive.
