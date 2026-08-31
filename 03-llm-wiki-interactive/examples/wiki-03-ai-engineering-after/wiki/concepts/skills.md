---
type: concept
title: Agent Skills
description: A folder-plus-SKILL.md convention, invoked directly by a coding-agent harness, for packaging reusable capability knowledge outside the MCP protocol — one leg of a connectivity stack alongside CLI and MCP.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/progressive-disclosure]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]"
  - "[[wiki/entities/decode-agent]]"
created: 2026-08-29T16:16:49Z
timestamp: 2026-08-29T17:10:11Z
source_count: 7
---

# Agent Skills

> A folder-plus-`SKILL.md` convention that packages reusable, harness-invoked capability knowledge — not an MCP protocol primitive, and one leg of a three-way connectivity stack alongside CLI and MCP.

## Definition

Skills are explicitly *not* an MCP concept: the word appears nowhere in the MCP spec (rev 2025-11-25), and five coding agents — Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex — independently converged on the same folder-plus-`SKILL.md` convention, each handling it as a native, agent-specific mechanism rather than routing it through MCP. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] In Claude Code that cashes out as a hard line: only MCP Tools and its own `.claude/skills/` directory are auto-detected *and* autonomously invoked; MCP Resources and Prompts are merely listable. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

Skills are one of (typically three) complementary connectivity mechanisms alongside CLI and MCP, carrying stable domain knowledge that travels independently of the harness. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]] One practitioner's own stack corroborates this from the outside: skills handle purely local file management, while siloed third-party services go through MCP instead. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]] The `decode` coding-agent codebase corroborates it from the inside: its `skills/` module has zero MCP dependency and is one of exactly three prompt-assembly sources — with the active persona and memory files — joined into one instructions block the harness rebuilds every run. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

`decode`'s own course now narrates that implementation in prose. Lesson 1 names Skills as one of six modules making up "the harness" (alongside providers, sandbox, permissions, memory and compaction), loaded only on invocation. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] Lesson 4 goes deeper: skills exist because upfront tool schemas alone can cost 7-9% of the context window before any work begins, and the fix is the same three-tier progressive disclosure the repo implements — a one-line catalog entry always resident, the full `SKILL.md` body loaded only on invocation, bundled `references/`/`examples/`/`scripts/` read on demand. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

> Synthesis: [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] and [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]] both appear to trace to one talk ("The Future of MCP," credited to David Soria Parra in one, "an Anthropic engineer who wrote the Python SDK" in the other) — one voice heard twice, not two witnesses. The `decode` repo and its two course articles are a second single-voice cluster (same author, same codebase, same course) — see Tensions.

## Key claims

- FastMCP's `SkillsDirectoryProvider` packages a skills folder as MCP *resources* — "a packaging decision, not an architectural one" — leaving it in a "dead zone": discoverable by any MCP client but not agentically callable by Claude Code. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Skills carry "stable"/"main knowledge" in a reusable file, one leg of a three-mechanism stack with CLI and MCP; 2026 agents are predicted to use all three "quite seamlessly together." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- A near-term MCP roadmap item, "skills over MCP," would let a large server ship updated capability knowledge as a skill without a plugin/registration mechanism. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- One practitioner routes local files (Obsidian) through Claude Code/skills, reserving MCP for siloed services (Notion, Readwise) — the three are complementary, not proof MCP is unfit at business scale. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]
- `decode` implements skills as three-tier progressive disclosure — a catalog (name plus one line) always in the prompt, full body loaded only on `skill(name)`, bundled `references/`/`examples/`/`scripts/` on demand — with project skills overriding built-ins by name and whitespace-stripped catalog lines blocking injection. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Lesson 1 of the course frames Skills as "workflows loaded only on invocation," one of six harness modules built on top of the ~20-line agent loop. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Lesson 4 quantifies the motivation for progressive disclosure (eager tool/skill schemas can cost 7-9% of the context window before work starts) and walks a real session where the catalog line, the invoked `SKILL.md` body, and its on-demand bundled files each load at a different point in the turn. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

## Tensions

- **Is there a real path for skills inside MCP?** [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] calls today's state a dead end — no protocol primitive, and FastMCP's resource-packaging isn't agentically callable. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]] instead names "skills over MCP" as a near-term roadmap fix. `decode` sidesteps the question, shipping skills with no MCP surface at all. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **False corroboration risk.** The repo's ARCHITECTURE page, [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] and [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]] are three witnesses but one voice: all three come from the same author (Paul Iusztin) and the same "Building a Coding Agent From Scratch" course, with the articles narrating the exact code the repo page already describes. Their agreement on three-tier progressive disclosure is the course explaining itself twice, not independent confirmation — the wiki's only genuinely separate corroboration for skills-as-complementary-to-MCP remains [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]].

## Relationships

- **MCP**: complementary, not competing — skills carry stable capability knowledge a harness invokes directly; MCP handles remote access, auth and governance at scale. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]
- **CLI**: the third leg of the stack — sandboxed/local tasks vs. skills' portable domain knowledge, both framed against MCP's remit. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/cli]]
- **Progressive disclosure**: `decode`'s catalog-then-body loading is a concrete instance of a pattern the articles only assert abstractly elsewhere in the wiki, and the course articles now put a number on the cost it avoids (7-9% of the context window). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/progressive-disclosure]]
- **Agent harness**: lesson 1 places Skills as one of six modules that constitute "the harness," the layer the course argues actually determines coding-agent quality. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]
- **Claude Code**: the harness whose `.claude/skills/` directory is the one non-MCP mechanism both auto-detected and autonomously invoked; `decode`'s memory format is also explicitly modeled on it. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]
- **FastMCP**: the SDK whose `SkillsDirectoryProvider` is the one documented attempt to bridge skills into MCP. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/fastmcp]]
- **decode (agent)**: the concrete implementation both course articles walk through — the repo shows the code, the articles narrate the session-level behavior and its motivating numbers. [[wiki/entities/decode-agent]]

> Synthesis: every source treats skills as real but structurally outside MCP today — unresolved is whether "skills over MCP" or the per-agent `SKILL.md` convention is where skills end up. `decode` remains the wiki's only codebase showing that convention actually working, and its own course is now the wiki's most detailed account of *why* the three-tier design exists — but that detail comes from one author explaining one project, not a second independent implementation.
