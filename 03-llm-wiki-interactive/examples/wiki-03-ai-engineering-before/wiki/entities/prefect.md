---
type: entity
title: Prefect
description: A workflow-orchestration company that both orchestrates agent data/memory pipelines directly and, through its FastMCP project, builds the de facto default Python SDK for MCP servers.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/entities/fastmcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-architecture]]"
  - "[[wiki/concepts/orchestrator-placement]]"
created: 2026-08-29T16:14:14Z
timestamp: 2026-08-29T16:14:14Z
source_count: 2
---

# Prefect

> A workflow-orchestration company, credited as both a pipeline-orchestration tool and the maker of FastMCP.

## Definition

Prefect shows up in the wiki in two roles that neither source ties together explicitly. One source names it as the company behind FastMCP, cited as evidence the MCP ecosystem is maturing quickly. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] The other names it as the workflow-orchestration tool actually running an agent's data, memory, and retrieval pipelines. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] Both are consistent with Prefect being a workflow-orchestration company that also ships FastMCP, but no source states that link directly — it is inferred from the two mentions together.

## Key claims

- Prefect built FastMCP, which has become the practical default Python SDK for building MCP servers — preferred even by MCP co-creator David Soria Parra over Anthropic's own official SDK. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Prefect is used to orchestrate the data pipeline, memory pipeline, and retrieval pipeline in an MCP-based agent architecture. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Workflow tools like Prefect are framed as belonging inside the agent runtime itself, since agents are becoming long-running systems that need durable execution, retries, checkpoints, human approvals and observability — properties workflow engines already provide. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

## Relationships

- **FastMCP**: Prefect built it; FastMCP is the SDK used for both the MCP server and MCP client side in an agent architecture. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/entities/fastmcp]]
- **MCP**: Prefect's orchestration role is cited as one reason agent runtimes are converging toward workflow-engine properties. [[wiki/concepts/agent-architecture]]

> Synthesis: The two source pages corroborate Prefect's presence in this space from independent angles (ecosystem commentary vs. a hands-on architecture walkthrough) but describe two different roles — pipeline orchestrator and FastMCP's maker — that together, not separately, make the case for Prefect sitting at the runtime layer.
