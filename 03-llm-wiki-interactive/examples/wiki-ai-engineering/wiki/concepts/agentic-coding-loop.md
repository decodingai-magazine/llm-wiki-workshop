---
type: concept
title: Agentic coding loop
description: "Edit, run, read, fix — and the tool-selection criterion that follows: can the agent restart the thing it just changed, and see the error where it works?"
aliases: [Edit-run-read-fix, CLAUDE.md]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-to-permission-gate-routing]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]"
  - "[[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]"
related:
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/entities/claude-code]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T11:35:00Z
source_count: 6
---

# Agentic coding loop

> An agent improves code by running it. Any tool that inserts a step the agent cannot perform breaks the loop, no matter how good it is otherwise.

## Definition

The loop is edit → run → read output → fix → repeat, and it works beautifully for
plain Python. Infrastructure breaks it wherever the agent must restart a
scheduler, reload a code location, or rebuild and push an image
[[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]. The remedy is
not agent capability but tool shape: when the worker *is* the Python process,
restarting is `kill` plus re-run, in about two seconds.

The second enabler is feedback. Trigger scripts stream logs to stdout and exit
non-zero on failure, so the agent gets an unambiguous signal in the same terminal —
no UI, no log files.

## Key claims

- The deciding question for any tool in an agent-built system: can the agent restart the execution environment in seconds after a code change? [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- Errors must surface where the agent works; a dashboard is invisible to it. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- Configuration in the same language as the code beats a separate DSL or YAML layer. [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- A handwritten project instruction file, written before any code, is credited with making a two-day build work. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- The instruction file is only writable because the loop is simple: "kill a process, start a process, run a make command, read the output." [[wiki/sources/how-smooth-is-to-use-prefect-for-agentic-coding]]
- The agent's contribution was implementation, not architecture — the design was decided first. [[wiki/sources/how-smooth-was-my-experience-to-use-mongodb-and-build-from]]
- The loop's quality is bounded by feedback speed — a language server flagging a broken edit immediately is "the cheapest way to get feedback on code changes". [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Tool failures should return a retry to the model, not an error to the user: an ambiguous edit is a correctable mistake. [[wiki/sources/article-the-coding-agent-loop]]
- A denial returns to the model as a typed result carrying the reason, so the loop adapts instead of retrying blindly. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-to-permission-gate-routing]]

## Relationships

- **[[wiki/concepts/agent-skills]]**: the instruction file is the same user-owned procedural layer, applied to a repo.
- **[[wiki/concepts/infrastructure-over-frameworks]]**: a second selection criterion for tools, alongside "does it solve a hard problem".

> Synthesis: Both sources are the same build, so this is one experience rather than a pattern — but the four questions it produces are testable against any tool, which is more than most tooling advice offers.
