---
type: source
title: The future of MCP — why the future of agents is MCP, skills and CLIs combined
description: A short LinkedIn post draft laying out a four-layer architecture for AI-native applications — presentation, harness plus runtime, connectivity, MCP servers.
origin: local
original_path: data_input_examples/notes/01-easy/The future of MCP. Why the future of agents is MCP, skills and CLIs combined.md
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills.md
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/anthropic]]"
  - "[[wiki/entities/david-soria-parra]]"
concepts:
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/mcp-apps]]"
  - "[[wiki/concepts/durable-execution]]"
---

# The future of MCP — why the future of agents is MCP, skills and CLIs combined

> [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills|Raw]] · local

## Summary

A post draft, written off the back of the MCP conference talk and built around
one diagram. Its thesis is that most teams are still building AI applications by
bolting agents and MCP servers onto an existing frontend/backend split, which is
the normal way every new paradigm starts — by adapting the old one — and that the
architecture actually emerging is four decomposable layers instead.

**Presentation** is a thin renderer: a TUI, an IDE extension, a web or desktop
app. With MCP Apps the client can render server-shipped UI directly, so the same
app runs in Claude, ChatGPT and Cursor without a rewrite. **Harness plus
runtime** is the brain — the LLM↔tool loop, memory, permissions, orchestration —
and the post's sharpest observation is that agents are becoming long-running
systems rather than single inference calls, which drags in durable execution,
retries, checkpoints, human approvals and observability. That is why the author
counts a workflow engine as part of the runtime, not as infrastructure beside it.
**Connectivity** is the stack: skills for reusable domain knowledge, CLIs for
local host capabilities, MCP clients for auth, resources, tasks and UI.
**MCP servers** are where business logic and private data stay.

The post is derivative by design — it quotes the talk's "connectivity is not one
thing" line and its 110M-downloads figure — but the four-layer decomposition and
the "single-mechanism agents underperform" framing are the author's own. It closes
by asking whether browsers become obsolete once a chat interface can render any
application on demand.

## Key claims

- The emerging architecture has four independently decomposable layers: presentation, harness + runtime, connectivity, MCP servers — with MCP as the connective tissue between them. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Agents are becoming long-running systems, so the runtime needs durable execution, retries, checkpoints, human approvals and observability. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- MCP Apps let one server-shipped UI render across Claude, ChatGPT and Cursor without rewriting it per client. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- Modern agents use skills, CLIs and MCP clients together — "single-mechanism agents underperform." [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]
- A modern MCP server ships more than tools: resources, prompts, skills, MCP Apps, tasks and elicitation. [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|cite]]

## Notable quotes

> "Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together."
> — David Soria Parra, quoted at [[raw/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills#Post|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]], [[wiki/entities/anthropic]], [[wiki/entities/david-soria-parra]]
- **Concepts**: [[wiki/concepts/connectivity-stack]], [[wiki/concepts/agent-harness]], [[wiki/concepts/agent-skills]], [[wiki/concepts/cli-tools]], [[wiki/concepts/mcp-apps]], [[wiki/concepts/durable-execution]]

> Synthesis: A publishing artifact rather than a research note — it is the cleanest statement of the four-layer model in the wiki, and it is the only source that names the person behind the connectivity-stack quote.
