---
type: concept
title: Agent skills
description: Reusable procedural knowledge packaged as a folder with a SKILL.md file — a cross-agent convention that no protocol defines.
aliases: [Skills, SKILL.md]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/mcp-servers-for-continual-learning-via-graphrag]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/agentic-invocation]]"
  - "[[wiki/entities/claude-code]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 11
---

# Agent skills

> A folder with a `SKILL.md` inside it, holding domain knowledge the agent loads when it needs it — a convention every harness adopted and no protocol specifies.

## Definition

A skill captures "main knowledge" — how to do a specific thing — in a simple file
that an agent can read and follow [[wiki/sources/the-future-of-mcp-vs-skills]].
Its defining property in these notes is *ownership*: skills are the user's
layer, holding personal workflows and project conventions, as opposed to a
server author's tool descriptions
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]].

The convention is portable by accident rather than by design. Claude Code,
Copilot, Gemini CLI, Cline and Codex all landed on the same folder-plus-`SKILL.md`
shape, each handling it natively — which is why skills are described as "mostly
reusable" across agents, with minor differences per file
[[wiki/sources/the-future-of-mcp-vs-skills]].

## Key claims

- Skills exist nowhere in the MCP specification; they are a packaging convention, and every harness implements them itself. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- In Claude Code, `.claude/skills/` is one of only two surfaces the model invokes on its own initiative. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- In the connectivity stack, skills are the layer for reusable user domain knowledge. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Distributing skills as files works for personal setups and collapses at business scale, where you cannot install markdown on a million machines. [[wiki/sources/why-mcp-is-not-dead]]
- Developer-owned instructions do **not** belong in skills — they belong in tool descriptions and prompts that ship with the server. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Tool docstrings say what the model *can* do; a skill says what it *should* do — in practice, a decision tree for choosing between similar tools and rules for presenting results. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Skills are a harness feature, so a server that depends on them degrades to bare docstrings everywhere else. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Reach for a skill when the knowledge is procedural and *stable* — if it must be fetched fresh each call, it is a tool, not a skill. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Sometimes the skill is one line in the project instruction file; complexity is only warranted when the procedure is. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- A skill can be one line in a project instruction file — and that line replaced an entire database integration. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]
- Skills are what make a large tool surface usable: a decision tree telling the model which of three search tools fits which question. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The same file doubles as the runbook for agentic coding — how to serve, trigger and read a pipeline. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- A working implementation matches the convention exactly: `<name>/SKILL.md`, YAML frontmatter of `name` + `description`, instruction body — with project skills overriding built-ins by name. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Malformed built-in skills fail loudly; malformed project skills are skipped with a warning, so a user's typo never breaks a session. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/concepts/skills-over-mcp]]**: the attempt to ship this user-owned layer from a server, and where it runs into the protocol.
- **[[wiki/concepts/connectivity-stack]]**: skills are one of the three mechanisms, chosen for knowledge rather than capability.
- **[[wiki/concepts/governance]]**: the reason files-on-disk stop being an answer once there are users to govern.

> Synthesis: Every source agrees on what a skill *is* and disagrees on where it should live — and that disagreement is really about who the agent belongs to, the user or the vendor.
