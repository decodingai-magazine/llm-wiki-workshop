---
type: concept
title: Connectivity stack
description: The claim that agent connectivity is a layered choice — skills, CLIs and MCP, each for the job it fits — rather than a single mechanism to standardize on.
aliases: [Full connectivity, Connectivity layer]
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/entities/mcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 4
---

# Connectivity stack

> "Connectivity is not one thing" — skills carry knowledge, CLIs carry local capability, MCP carries semantics, auth and reach, and a serious agent uses all three.

## Definition

The stack is a rejection of the search for a single connectivity answer. Anyone
promising one solution for every connectivity problem "is probably pretty wrong,
because the right answer always means it depends"
[[wiki/sources/the-future-of-mcp-vs-skills]]. The layers divide by *what kind of
thing* is being connected: skills for reusable domain knowledge, CLIs for local
host capability, MCP clients for auth, resources, tasks and UI
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]].

## Key claims

- The prediction for 2026 is agents that use every mechanism seamlessly together, not agents that pick one. [[wiki/sources/the-future-of-mcp-vs-skills]]
- "Single-mechanism agents underperform." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- The blocker is not the protocol but the plumbing: "our agents kind of still suck and partially… we just haven't talked enough about some of the techniques you can do to really put this connective tissue together." [[wiki/sources/the-future-of-mcp-vs-skills]]
- MCP earns its layer when you need rich semantics, long-running UI, platform independence, no sandbox, or enterprise authorization and governance. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Applied honestly, the stack cuts both ways: the same practitioner runs MCP for hosted business logic and CLIs for local development. [[wiki/sources/why-mcp-is-not-dead]]
- The sharpest formulation: CLIs are how the agent talks to the local computer, skills are how it remembers what it knows, MCP is how it talks to everything else. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Still unanswered: how a harness should arbitrate when a skill, a CLI and an MCP tool all offer the same capability. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/agent-skills]]** / **[[wiki/concepts/cli-tools]]** / **[[wiki/entities/mcp]]**: the three layers, each with its own entry.
- **[[wiki/concepts/agent-harness]]**: the layer above, which has to hold all three at once.

> Synthesis: This is the wiki's organizing idea — most of the other disagreements dissolve into "which layer are we talking about," which is exactly what a good frame is supposed to do.
