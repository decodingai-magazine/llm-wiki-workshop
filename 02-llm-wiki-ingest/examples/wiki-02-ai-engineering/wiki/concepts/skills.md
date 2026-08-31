---
type: concept
title: Skills
description: A folder-with-SKILL.md convention for packaging reusable, context-triggered domain knowledge — sources disagree on whether it is a harness-native pattern outside the MCP protocol or a coequal third of agent "connectivity" alongside CLI and MCP.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/hooks]]"
  - "[[wiki/concepts/context-engineering]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:15:00Z
source_count: 9
---

# Skills

> Multiple framings — see Definition

## Definition

One framing treats Skills as having no independent existence in the MCP protocol at all: the word "Skills" appears nowhere in the MCP spec, and there is no `/skills/list` or `/skills/execute` method — a skill is "a prompt, a resource, or a bundle of both," and calling it a skill is a packaging decision, not an architectural one. What actually exists is a folder-with-`SKILL.md` convention that several coding harnesses (Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex) have each independently implemented natively. In Claude Code, `.claude/skills/` is both auto-detected *and* agentically invoked — unlike MCP Resources and Prompts, which Claude Code only auto-detects and requires a human to explicitly trigger — putting skills functionally closer to an MCP Tool than to any MCP primitive. When FastMCP's `SkillsDirectoryProvider` packages that same SKILL.md convention as MCP resources (`skill://name/SKILL.md`, `_manifest`, ...), that packaging makes a skill discoverable by any MCP client but does not make it agentically callable by Claude Code through that route. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]], [[wiki/sources/agentic-graphrag-via-mcp-servers]]

A second framing, running through the David Soria Parra talk material, puts Skills at a higher altitude: one of three coequal "connectivity" mechanisms, alongside CLI and MCP, through which an agent's harness reaches capability and knowledge — skills specifically carrying stable, reusable domain knowledge for how to use a system in context. Its refrain is "connectivity is not one thing": the best agents combine skills, CLI and MCP together, and single-mechanism agents underperform. A third, narrower framing treats skills as a scale-dependent *substitute* for MCP: for personal, single-user setups, skills that glue steps together (plus a CLI) are often simply sufficient, and MCP's payoff — governance, security, distribution to many users — only shows up at business scale.

A fourth, more code-level framing comes from the Decode coding-agent course: it lists Skills as one of six core harness modules (with LLM providers, sandbox, permissions, memory, and an LSP server) and specifies how they actually load — a 3-tier progressive-disclosure scheme (a one-line name+description catalog entry, the full `SKILL.md` body on invocation, then bundled files on demand), motivated by the same context-budget pressure that MCP tool schemas cause: upfront MCP tool schemas alone were measured to consume 7–9% of the context window before any work begins. This is consistent with the first framing (skills as harness-native, outside the MCP protocol) but supplies the concrete engineering reason for treating skill content as deferred rather than system-prompt-resident. The Decode codebase itself implements exactly this: `src/decode/skills/` is a dedicated catalog-plus-dispatcher module over the same `SKILL.md`-per-folder convention, and `assemble_skills_catalog()` is one of the parts folded into the system prompt fresh every turn — grounding the course's argument in running code rather than prose. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-context-engineering-for-coding-agents]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- MCP has no native "Skills" primitive — only Tools, Resources and Prompts; multiple harnesses (Claude Code, GitHub Copilot, Gemini CLI, Cline, Codex) converged independently on a folder-with-`SKILL.md` convention each handles natively, outside MCP. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Claude Code's `.claude/skills/` is auto-detected *and* agentically invoked, unlike MCP Resources/Prompts (auto-detected only, need explicit user triggering) — closer in behavior to an MCP Tool than to any MCP primitive. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- A Claude Code Skill (carrying a tool-selection decision tree and presentation rules) is a harness-specific enrichment layer stacked on a portable MCP server layer: "Tools alone tell the model what it can do. Skills tell it what it should do in context." [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Skills, CLIs and MCP clients are three complementary connectivity mechanisms, not competitors — skills carry reusable domain knowledge, CLIs suit local/composable execution, MCP covers auth and rich semantics — and the best 2026 agents combine all three. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- For personal, single-user setups, skills plus a CLI are often sufficient on their own and don't need MCP; MCP's advantage shows up at business scale for governed multi-user distribution, though a server can also expose the same skills-and-prompts pattern itself. [[wiki/sources/why-mcp-is-not-dead]]
- Skills load through 3 progressive-disclosure tiers — a name+description catalog line, the full `SKILL.md` body on invocation, then bundled files on demand — a scheme motivated by measurements that upfront MCP tool schemas alone consume 7–9% of the context window before any work begins. [[wiki/sources/article-context-engineering-for-coding-agents]]
- Decode, a from-scratch coding-agent harness, treats Skills as one of six core harness modules, alongside LLM Providers, Sandbox, Permissions, Memory, and an LSP server. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- In the Decode codebase, `src/decode/skills/` is a standalone module (a catalog + dispatcher over the `SKILL.md`-per-folder convention) alongside sibling `memory/`, `permissions/`, `sandbox/`, and `services/lsp/` modules, and `assemble_skills_catalog()` is folded into the single system-prompt block assembled at every turn — base prompt + active persona + `assemble_memory()` + skills catalog — matching the course article's description of session-start assembly. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[wiki/sources/article-context-engineering-for-coding-agents]]

## Tensions

- **A packaging convention, or a coequal layer?** [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] argues skills have no independent architectural status — they're just prompts/resources bundled and marketed as "skills," invoked only through a harness's own native skills folder. The Soria Parra talk material ([[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]) instead names skills as one-third of the agent-connectivity architecture, coequal with CLI and MCP. Both agree skills sit outside MCP's three protocol primitives; they disagree on whether that makes skills an implementation detail or a first-class layer.
- **Substitute for MCP, or always combined?** [[wiki/sources/why-mcp-is-not-dead]] frames skills (with CLI) as a scale-dependent substitute for MCP — sufficient for personal use, replaced by MCP once governance matters. [[wiki/sources/the-future-of-mcp-vs-skills]] and [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] instead argue the best agents combine all three mechanisms regardless of scale, and that single-mechanism agents underperform.

> Synthesis: three of the sources here ([[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]) are independent write-ups of the same David Soria Parra talk, and three more ([[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-context-engineering-for-coding-agents]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]) are Lesson 1, Lesson 4, and the codebase itself of the same author's Decode course — so each cluster corroborates only as one voice, not several, though the repo is primary evidence (running code) rather than a second report about the same code. What that leaves as genuinely independent corroboration for Skills-as-harness-native-convention is three separate voices: [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]], [[wiki/sources/agentic-graphrag-via-mcp-servers]], and the Decode-course trio — the codebase being the wiki's most concrete evidence yet, since it shows the loading mechanism (progressive disclosure, `assemble_skills_catalog()`) in running code rather than just arguing the protocol taxonomy.

## Relationships

- **MCP**: Skills sit outside MCP's three protocol primitives (Tools/Resources/Prompts); framed either as packaging over them or as a coequal mechanism alongside them. [[wiki/concepts/mcp]]
- **CLI**: The other local/composable leg of the "connectivity" triad alongside skills and MCP. [[wiki/concepts/cli]]
- **Agent connectivity**: Skills are one of the three mechanisms in the "connectivity is not one thing" framing, with CLI and MCP. [[wiki/concepts/agent-connectivity]]
- **Hooks**: In the "3-layer pattern," a Skill and a Stop hook are the two Claude Code-specific enrichment layers built on top of a portable MCP server. [[wiki/concepts/hooks]]
- **Orchestration**: For deterministic pipelines, composite MCP tools (server-side orchestration) are recommended over relying on a skill or prompt to guide multi-round-trip, client-side orchestration. [[wiki/concepts/orchestration]]
- **Context engineering**: Skills' 3-tier progressive-disclosure loading is one of the harness components (with memory, an LSP server, and compaction) that keep a coding agent's context window high-signal across a session. [[wiki/concepts/context-engineering]]
- **Agent harness**: In Decode, Skills is one of six modules a coding-agent harness is organized into, alongside LLM providers, a sandbox, permissions, memory, and an LSP server — confirmed in the codebase as a standalone `src/decode/skills/` module. [[wiki/concepts/agent-harness]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

> Synthesis: Skills is the most genuinely contested concept in this wiki so far — not a claim any source disputes on the facts, but a disagreement about altitude: is it a harness-level packaging convention with no protocol status, or one-third of how agent connectivity itself is architected in 2026. The Decode-course sources add a third altitude beneath both: skills as one deferred-loading harness module among several, motivated by context economics rather than protocol philosophy — and the Decode repo grounds that third altitude in actual code, not just an argued design.
