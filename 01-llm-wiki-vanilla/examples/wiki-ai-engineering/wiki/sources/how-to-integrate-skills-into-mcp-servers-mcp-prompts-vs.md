---
type: source
title: "How to integrate Skills into MCP servers: MCP Prompts vs. Skills"
description: Working notes establishing that skills are not an MCP primitive, and that FastMCP's skills provider leaves them in a dead zone where clients can list them but never invoke them agentically.
origin: local
original_path: data_input_examples/notes/01-easy/How to integrate Skills into MCP servers MCP Prompts vs. Skills.md
source_url: null
authors: []
published_date: null
raw_file: raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs.md
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/fastmcp]]"
concepts:
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/server-side-orchestration]]"
  - "[[wiki/concepts/agentic-invocation]]"
---

# How to integrate Skills into MCP servers: MCP Prompts vs. Skills

> [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs|Raw]] · local

## Summary

A working note that starts from a practical question — how do you ship skills
with an MCP server? — and answers it by reading the protocol. The finding is
negative and load-bearing: **"skills" do not exist anywhere in the MCP
specification** (revision 2025-11-25). The protocol defines tools, resources,
prompts, sampling, elicitation and (experimentally) tasks; a skill is a packaging
convention layered on top of those, not a primitive of its own.

The note then splits the question by *who invokes what*. Of the four surfaces a
Claude Code user can expose, only two are picked up by the model on its own: MCP
tools, and native `.claude/skills/`. MCP resources and prompts are listable but
inert — they must be named by the user. FastMCP's `SkillsDirectoryProvider`
publishes each skill directory as a resource (`skill://name/SKILL.md`), which
makes skills *discoverable* by any MCP client but not *callable* by the loop.

That produces the note's central complaint: skills-as-resources land in a dead
zone — too developer-owned to be a user skill, too passive to be a tool. The
recommendation follows the ownership split: developer knowledge about how to
drive a server belongs in tool descriptions and prompts; user workflows belong in
`.claude/skills/`; and composite tools, not prompts, are the right home for
deterministic multi-step pipelines, because tool code always runs server-side and
the model cannot skip or reorder the steps.

## Key claims

- "Skills" appear in no MCP protocol message, schema type, capability declaration or method definition — the primitives are tools, resources, prompts, sampling, elicitation and tasks. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills Are NOT Part of the MCP Protocol|cite]]
- Only MCP **tools** and native `.claude/skills/` are auto-detected *and* used agentically; resources and prompts are listable but must be triggered explicitly by the user. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#MCP Primitives vs Claude Code Native Skills|cite]]
- Every major coding agent converged on the same folder-plus-`SKILL.md` convention (Claude Code, Copilot, Gemini CLI, Cline, Codex) while handling it natively rather than through MCP. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Skills as a Cross-Agent Ecosystem Convention|cite]]
- Tool code always executes on the server, so a composite tool costs one round-trip with a guaranteed execution order, where client-side orchestration costs a round-trip plus an inference step per stage. [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Tool Execution Architecture|cite]]
- For deterministic pipelines, composite tools beat prompts: "Don't rely on AI to orchestrate deterministic pipelines." [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#Key Takeaways|cite]]

## Notable quotes

> "A skill is not a separate concept. It's a prompt, a resource, or a bundle of both. Calling them 'skills' is a packaging decision, not an architectural one."
> — FastMCP docs, quoted at [[raw/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs#FastMCP's Skill Abstraction|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/claude-code]], [[wiki/entities/fastmcp]]
- **Concepts**: [[wiki/concepts/mcp-primitives]], [[wiki/concepts/agent-skills]], [[wiki/concepts/skills-over-mcp]], [[wiki/concepts/server-side-orchestration]], [[wiki/concepts/agentic-invocation]]

> Synthesis: This is the only note in the wiki that reads the protocol rather than the discourse, which makes it the reference for what MCP actually specifies — and its "dead zone" finding is the concrete failure mode behind the more optimistic "skills over MCP" pitch elsewhere.
