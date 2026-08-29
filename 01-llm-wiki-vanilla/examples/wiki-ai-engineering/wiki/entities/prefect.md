---
type: entity
title: Prefect
description: The workflow orchestrator used for the data, memory and retrieval pipelines, and argued to belong inside the agent runtime rather than beside it.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/entities/fastmcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 5
---

# Prefect

> A Python workflow orchestrator that these notes place inside the agent runtime — the thing that makes a long-running agent durable rather than merely retried.

## Definition

Prefect orchestrates every pipeline in the reference architecture: the data
pipeline that normalizes inputs into documents, the memory pipeline that turns
documents into knowledge-graph objects and embeddings, and the retrieval tooling
on the read side [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].
The four-layer post goes further and argues it is part of the runtime itself,
because agents are long-running systems that need durable execution, retries,
checkpoints, human approvals and observability
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]].

## Key claims

- All three pipelines — data, memory, retrieval — are orchestrated by Prefect, with FastMCP handling only the protocol surface. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Because agents are becoming long-running systems rather than single inference calls, a workflow engine counts as part of the runtime layer. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- In day-to-day development the author reaches for Prefect's CLI rather than an MCP server — the local, sandboxed case where CLIs win. [[wiki/sources/why-mcp-is-not-dead]]
- Batch pipelines run as Prefect flows with retries and task-level checkpointing, while the same logic runs inline for MCP tool calls — because there the user is waiting. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Prefect's Horizon Cloud is how the memory server itself gets deployed: serverless, authenticated, redeployed on every push. [[wiki/sources/owning-your-context-layer]]

## Relationships

- **[[wiki/concepts/durable-execution]]**: the property Prefect is brought in to provide.
- **[[wiki/concepts/cli-tools]]**: Prefect is also a worked example of choosing a CLI over a server for local work.
- **[[wiki/entities/fastmcp]]**: the same vendor; the two split the runtime and the protocol surface between them.

> Synthesis: Prefect is the clearest case in the wiki of the same tool being reached for through two different connectivity mechanisms depending on who is running it.
