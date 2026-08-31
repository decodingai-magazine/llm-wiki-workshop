---
type: source
title: The Right Way of Building Agents With MCP Servers
description: An open architectural question -- whether a custom agent orchestrator belongs inside the MCP server, packaged as one tool, or on the MCP client side calling composed tools and prompts directly.
origin: local
original_path: data_input_examples/notes/02-medium/The Right Way of Building Agents With MCP Servers.md
source_url: null
authors: []
published_date: null
raw_file: raw/the-right-way-of-building-agents-with-mcp-servers.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-memory]]"
---

# The Right Way of Building Agents With MCP Servers

> [[raw/the-right-way-of-building-agents-with-mcp-servers|Raw]] · local

## Summary

A video script (addressed to a collaborator, "Curtis") in which the author walks through his current go-to agent architecture and then poses the one design question he hasn't settled. The baseline: an ingestion pipeline normalizes any input (dataset or URI -- article, video, image) into a document and stores it in a data warehouse; a memory pipeline then turns those documents into knowledge-graph objects (entities and relationships), computes embeddings over their summaries, and attaches metadata, before saving everything to memory. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]

That memory is exposed to an agent through an MCP server offering just two core tools -- knowledge-graph search and knowledge-graph write -- plus prompts (predefined procedures) that tell an orchestrator how to combine those tools, such as "update episodic memory" or "write technical article." The server is then composed with other prebuilt MCP servers (web search, image generation, Google Drive) into one merged toolset, which a client -- either a custom FastMCP-based orchestrator or a prebuilt one like Claude Code -- drives. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]

The actual thesis is the unresolved part: once you need custom planning logic instead of a prebuilt orchestrator, should that orchestrator live *inside* the MCP server -- packaged and exposed as a single tool any client can call -- or on the MCP client side, with the server only exposing raw tools and prompts? The author says he has implemented both and cannot yet judge which is architecturally better, since the choice "propagates through the entire application." [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]

## Key claims

- The baseline pipeline is linear: ingest a dataset or URI, normalize to a document, store it in a data warehouse, then extract knowledge-graph entities/relationships, embed the document summary, and attach metadata before saving to memory. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]
- Memory is reached through exactly two MCP tools -- knowledge-graph search and knowledge-graph write -- plus prompts that tell the orchestrator how to combine tool calls for a given procedure. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]
- Episodic memory (what a user did at a specific moment, e.g. a New Year's trip) and semantic memory (preferences, e.g. writing style) are both written automatically into the knowledge graph as the user chats with the agent. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]
- The author's MCP server is composed with other prebuilt MCP servers (web search, image generation, Google Drive) into a single merged set of tools and prompts consumable by any MCP client. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]
- Two ways exist to drive that composed toolset: a custom orchestrator built with FastMCP's client utilities, or a prebuilt orchestrator such as Claude Code -- both are, from the user's perspective, just MCP clients. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]
- The open design question is where a custom orchestrator should live: packaged inside the MCP server as a single exposed tool, or on the MCP client side (a FastAPI backend, or a React/TypeScript frontend) while the server exposes only raw tools/prompts -- the author has built both and considers the choice unresolved. [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|cite]]

## Notable quotes

> "The real question here is: where should we put this custom orchestrator? Should we put it on the MCP server side, or should we put it on the client side?"
> — [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|location]]

> "Programmatically, both work—I implemented both. But from the architectural system design point of view, which solution is better? I cannot really choose, and I think it's a very important architectural decision that propagates through the entire application."
> — [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|location]]

> "Option one would be to build your tools and prompts and keep them inside the server, not expose them, and actually just expose your custom orchestrator as a tool."
> — [[raw/the-right-way-of-building-agents-with-mcp-servers#the-right-way-of-building-agents-with-mcp-servers|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/orchestration]], [[wiki/concepts/agent-memory]]

> Synthesis: A working note posing an open design question rather than asserting a settled answer -- treat the client-side-vs-server-side orchestrator placement as unresolved by the author himself, not as a recommendation.
