---
type: source
title: "The Right Way of Building Agents With MCP Servers"
description: "An open architectural question about whether a custom agent orchestrator belongs inside the MCP server itself or on the MCP client side."
origin: local
original_path: "data_input_examples/notes/01-easy/The Right Way of Building Agents With MCP Servers.md"
source_url: null
authors: []
published_date: null
raw_file: raw/the-right-way-of-building-agents-with-mcp-servers.md
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-memory]]"
---

# The Right Way of Building Agents With MCP Servers

> [[raw/the-right-way-of-building-agents-with-mcp-servers|Raw]] · local

## Summary

A video-script draft (framed as an open question for the audience) walking through a data/memory/retrieval pipeline architecture: raw input is ingested and normalized into documents, then a memory pipeline turns those documents into knowledge-graph objects (entities, relationships, embeddings, metadata) that get exposed through knowledge-graph search and write tools on an MCP server, alongside prompts that tell the agent how to combine those tools for tasks like updating episodic memory or writing an article.

The note's real question is architectural: once you compose your own MCP server with other prebuilt MCP servers (web search, image generation, Google Drive), where should the custom orchestrator that plans across all of them live — packaged inside the MCP server as a single tool, or on the MCP client side, built with something like Claude Code or a custom FastMCP-based client? The author says they've implemented both and can't yet decide which is architecturally better.

## Key claims

- The memory pipeline turns ingested documents into knowledge-graph objects via an extractor (entities and relationships) plus an embedding model over document summaries, alongside source/author/date metadata. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]
- Knowledge-graph search and write tools are exposed on the MCP server, and specialized prompts (e.g. "update episodic memory," "write technical article") tell the orchestrator how to combine those tools; episodic memory covers user events, semantic memory covers preferences and style. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]
- The custom MCP server is composed with prebuilt MCP servers (web search, image generation, Google Drive) to produce one combined set of tools and prompts that any MCP client can connect to. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]
- Two architectural options are on the table: (1) keep the custom orchestrator inside the MCP server and expose only it as a tool, or (2) expose the raw tools/prompts and build the custom orchestrator on the MCP client side — both are implemented and working, but the author has not settled which is architecturally better. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]
- Where the orchestrator lives determines the client shape: it can be Claude Code using the pre-built logic directly, or a custom Python/FastAPI or TypeScript/React client hosting the MCP client and its own planning logic. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]
- The whole stack is orchestrated with Prefect (data pipeline, memory pipeline, retrieval) and implemented with FastMCP on both the server and the client-side connector. [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|cite]]

## Notable quotes

> "The real question here is: where should we put this custom orchestrator? Should we put it on the MCP server side, or should we put it on the client side?"
> — [[raw/the-right-way-of-building-agents-with-mcp-servers#The Right Way of Building Agents With MCP Servers|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/claude-code]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/orchestration]], [[wiki/concepts/agent-memory]]

> Synthesis: The wiki's most concrete worked example of [[wiki/concepts/orchestration]] placement and of an [[wiki/concepts/agent-memory]] design — the only source that shows the actual pipeline rather than arguing about it in the abstract.
