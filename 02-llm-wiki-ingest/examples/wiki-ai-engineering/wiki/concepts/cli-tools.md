---
type: concept
title: CLIs as agent connectivity
description: Command-line tools as the cheapest connectivity mechanism for a local, sandboxed agent — strong on discovery and training-data familiarity, weak on distribution.
aliases: [CLI, CLI layer]
sources:
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/governance]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/entities/prefect]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 5
---

# CLIs as agent connectivity

> The connectivity layer you reach for when the agent is local: composable in bash, self-describing through `--help`, and usually already in the model's training data.

## Definition

A CLI gives an agent host capabilities with no protocol in between. The case for
it rests on three properties: composability in a shell, automatic discovery (the
model can ask the tool what it can do), and pre-training — for `git`, `gh` and
their peers the model already knows the interface
[[wiki/sources/the-future-of-mcp-vs-skills]]. The precondition is a local agent
with a sandbox and a reliable execution environment; in the four-layer model CLIs
are simply "local host capabilities"
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]].

## Key claims

- CLIs are "particularly good when you have a local agent where you can assume a sandbox" and a good execution environment. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Tools already present in pre-training make the CLI route disproportionately effective — no schema to teach. [[wiki/sources/the-future-of-mcp-vs-skills]]
- The failure mode is distribution: shipping a CLI plus markdown files to every customer's machine is not a deployment story. [[wiki/sources/why-mcp-is-not-dead]]
- "We had CLIs for so long and we haven't found a good way to govern them when distributing them to users." [[wiki/sources/why-mcp-is-not-dead]]
- The same author who argues for MCP at business scale uses MongoDB, Prefect and Obsidian CLIs during development — the local case, decided on its merits. [[wiki/sources/why-mcp-is-not-dead]]
- Wrapping a pre-trained CLI in an MCP server is often a regression: you lose the model's prior knowledge and force it through a thinner interface. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Bash pipes are composition that predates the term — `gh pr list | jq | xargs` is programmatic tool calling. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Given only a CLI and one line of instruction, an agent independently seeded test data, debugged silent query failures and verified pipeline output — each time as a throwaway script. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]

## Relationships

- **[[wiki/concepts/connectivity-stack]]**: CLIs are the "local and sandboxed" branch of the choice.
- **[[wiki/concepts/governance]]**: the axis on which CLIs lose to servers, and the only one.
- **[[wiki/concepts/mcp-server-design]]**: the mirror-image decision — what you should *not* wrap in a server.

> Synthesis: The sources converge on a clean rule of thumb — CLI when you own the machine, server when you own the users — and none of them treats the choice as ideological.
