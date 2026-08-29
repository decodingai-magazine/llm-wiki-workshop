---
type: overview
title: ai-engineering — Overview
description: What ten notes on MCP, skills, CLIs and agent memory add up to — connectivity as a layered choice, and a context layer worth owning underneath it.
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
total_sources: 10
total_pages: 35
---

# ai-engineering — Overview

> Ten notes on how agents connect to the world and what they remember: two conference write-ups, one protocol reading, three architecture walkthroughs, one database evaluation and three post drafts.

## Themes

### Connectivity is a stack, not a choice

The wiki's organizing argument. [[wiki/concepts/connectivity-stack]] holds that
[[wiki/concepts/agent-skills]], [[wiki/concepts/cli-tools]] and
[[wiki/entities/mcp]] each answer a different question — knowledge, local
capability, semantics and reach — and that single-mechanism agents underperform.
Stated in [[wiki/sources/the-future-of-mcp-vs-skills]], turned into a layered
system in [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]],
and stress-tested from the CLI side by
[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]], which
replaces a whole server with one line of instruction.

### What the protocol defines, and what the harness owes it

[[wiki/concepts/mcp-primitives]] is the corrective to the discourse: six things,
sorted by who decides when they run. [[wiki/concepts/agent-skills]] are not among
them, which is why [[wiki/concepts/skills-over-mcp]] ships without invocation
semantics. The complement is [[wiki/concepts/agent-harness]] — the layer that owes
the ecosystem [[wiki/concepts/progressive-disclosure]] and
[[wiki/concepts/programmatic-tool-calling]], both of which the protocol already
supports and most clients have not built.

### Memory is the part worth owning

[[wiki/concepts/context-layer]] is the wiki's answer to *why bother*: models and
harnesses commoditize, so the moat is the memory you can carry between them
[[wiki/sources/owning-your-context-layer]]. Its implementation runs through
[[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-graph]],
[[wiki/concepts/hybrid-search]] and [[wiki/concepts/agent-memory]], built end to
end in [[wiki/sources/agentic-graphrag-via-mcp-servers]] and priced out on
[[wiki/entities/mongodb]] in [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]].

### The case for a server is a case about people

[[wiki/concepts/governance]] is where [[wiki/sources/why-mcp-is-not-dead]] and the
conference notes independently land: servers win on distributing and controlling
business logic, not on capability. [[wiki/concepts/mcp-server-design]] is the
craft that follows — task-shaped tools, thin delegates, a budgeted output — and
[[wiki/concepts/durable-execution]] is what the runtime owes an agent that now
runs for minutes rather than seconds.

## Index

### Entities (7)
- [[wiki/entities/mcp]] — the protocol itself, treated as one layer rather than the whole stack.
- [[wiki/entities/claude-code]] — the reference harness whose invocation rules define "agentic" here.
- [[wiki/entities/fastmcp]] — the Python framework that became the default, and the skills provider under test.
- [[wiki/entities/mongodb]] — the single store behind the memory layer, with its limits stated.
- [[wiki/entities/prefect]] — workflow orchestration, argued into the runtime layer.
- [[wiki/entities/anthropic]] — author of the protocol and of its roadmap.
- [[wiki/entities/david-soria-parra]] — MCP co-creator; the origin of the connectivity framing.

### Concepts (18)
- [[wiki/concepts/connectivity-stack]] — skills, CLIs and MCP, each for the job it fits.
- [[wiki/concepts/agent-skills]] — procedural knowledge as a folder and a `SKILL.md`.
- [[wiki/concepts/cli-tools]] — the local, sandboxed, pre-trained option.
- [[wiki/concepts/mcp-primitives]] — the six things the spec defines, sorted by who invokes them.
- [[wiki/concepts/skills-over-mcp]] — shipping skills from the server, and why it is inert today.
- [[wiki/concepts/mcp-apps]] — server-shipped UI, portable across clients.
- [[wiki/concepts/mcp-server-design]] — design for an agent, not for your REST API.
- [[wiki/concepts/server-side-orchestration]] — composite tools versus a client-side planner.
- [[wiki/concepts/programmatic-tool-calling]] — let the model write the composition, in a sandbox.
- [[wiki/concepts/progressive-disclosure]] — an index first, the detail on request.
- [[wiki/concepts/agent-harness]] — the swappable brain: loop, memory, permissions.
- [[wiki/concepts/durable-execution]] — retries, checkpoints and approvals for long-running agents.
- [[wiki/concepts/governance]] — distribution and control, the axis servers win on.
- [[wiki/concepts/context-layer]] — the memory that makes an agent yours, and portable.
- [[wiki/concepts/unified-memory]] — one store, a small tool surface, any harness.
- [[wiki/concepts/knowledge-graph]] — entities and relationships extracted from documents.
- [[wiki/concepts/hybrid-search]] — vector plus text, fused by rank.
- [[wiki/concepts/agent-memory]] — operational, semantic, episodic, preference.

## Health

- Sources: 10 · Entities: 7 · Concepts: 18
- Waiting at 1 mention (materialize on the next source that touches them):
  `agentic-invocation`, `append-only-log`, and the entity `obsidian`.
- Most-cited pages: `agent-skills` (7), `mcp-server-design` (6), `claude-code` (8).
