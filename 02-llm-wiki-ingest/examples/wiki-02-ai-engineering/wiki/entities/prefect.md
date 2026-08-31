---
type: entity
title: Prefect
description: "The workflow-orchestration company behind FastMCP and Prefect Horizon Cloud, positioned by sources as core agent-runtime infrastructure even as one source rebuts a Prefect LinkedIn post declaring MCP dead."
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/orchestration]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 5
---

# Prefect

> Multiple framings — see Definition

## Definition

Prefect shows up in two related capacities. First, as the maker of the tooling
several sources used directly to build and host MCP-based agent memory
systems: **FastMCP**, described as having become "the practical default"
Python implementation for MCP servers, with MCP co-creator David Soria Parra
quoted calling it "way better than our Python SDK that we shipped"
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]; and
**Prefect Horizon Cloud**, the hosting platform one author used to deploy a
memory MCP server — connect GitHub, point at the MCP entry point and UV
environment — for automatic, authenticated, continuously-updated serverless
deployments within minutes [[wiki/sources/owning-your-context-layer]].

Second, as workflow-orchestration infrastructure in its own right, independent
of MCP. One source runs identical extraction/query business logic whether
triggered by an MCP tool call or "a batch Prefect flow"
[[wiki/sources/agentic-graphrag-via-mcp-servers]], and another positions
Prefect-style tooling as supplying the durable execution, retries, checkpoints
and observability long-running agents need "as part of the runtime itself"
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]. A
third treats Prefect as local/dev-time infrastructure an agent reaches
directly via CLI — alongside MongoDB and Obsidian — rather than through MCP
[[wiki/sources/why-mcp-is-not-dead]].

## Key claims

- FastMCP is built by Prefect and has become "the practical default" Python implementation for MCP servers. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Prefect Horizon Cloud hosts an MCP server after only connecting GitHub and specifying the MCP entry point and UV environment, yielding automatic, authenticated, continuously-updated serverless deployments within minutes. [[wiki/sources/owning-your-context-layer]]
- The same GraphRAG memory business logic runs identically whether invoked as an MCP tool call or as a batch Prefect flow. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Durable, long-running agents need retries, checkpoints, human approvals and observability, which Prefect-style tooling is positioned as providing "as part of the runtime itself." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- In one author's own system, Prefect is dev-time infrastructure reached directly via CLI rather than exposed through MCP, on the reasoning that unmediated agent access there is acceptable. [[wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/entities/fastmcp]]**: Prefect builds FastMCP; the two are packaged together (framework plus hosting) for shipping MCP servers end to end. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/owning-your-context-layer]]
- **[[wiki/concepts/mcp]]**: Prefect's own execution and hosting layer (flows, Horizon Cloud) runs alongside MCP servers rather than being subsumed by them — the same logic can be called via either path. [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/why-mcp-is-not-dead]]

## Tensions

One source frames Prefect as the *origin* of an anti-MCP take: the note is
written as "a direct rebuttal to a Prefect LinkedIn post declaring 'MCP is
dead'" [[wiki/sources/why-mcp-is-not-dead]]. Two other sources instead treat
Prefect's own products as near-essential MCP infrastructure — FastMCP as "the
practical default" server framework and Prefect Horizon Cloud as the fastest
path to deploying one [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]],
[[wiki/sources/owning-your-context-layer]]. The wiki doesn't have Prefect's
original post to resolve this; it may not be a contradiction so much as Prefect
publicly questioning one *use* of MCP while continuing to build the tooling
most sources rely on to implement it.

> Synthesis: Prefect reads less as a single-purpose "MCP company" than as
> general agent-runtime infrastructure (orchestration, hosting) that happens to
> also make the dominant MCP server framework — which is what makes its
> reported "MCP is dead" stance worth noting rather than smoothing over.
