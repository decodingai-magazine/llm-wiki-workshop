---
type: source
title: The Right Way of Building Agents With MCP Servers
description: A walkthrough of a GraphRAG-backed personal-assistant architecture that ends in an open architectural question — should the custom orchestrator live on the MCP server or in the client?
origin: local
original_path: data_input_examples/notes/01-easy/The Right Way of Building Agents With MCP Servers.md
source_url: null
authors: []
published_date: null
raw_file: raw/the-right-way-of-building-agents-with-mcp-servers.md
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/server-side-orchestration]]"
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/agent-memory]]"
---

# The Right Way of Building Agents With MCP Servers

> [[raw/the-right-way-of-building-agents-with-mcp-servers|Raw]] · local

## Summary

A spoken-through design walkthrough, recorded as a question to put to an
audience rather than as a settled answer. The author first lays out the
architecture he considers the go-to version: a **data pipeline** that ingests a
dataset or a URI (article, video, image), normalizes everything to documents and
stores them; a **memory pipeline** that turns documents into knowledge-graph
objects via an extractor, embeds a summary of each document, attaches metadata
(source, author, dates) and writes the result into memory; and a retrieval
surface exposing exactly two core tools — knowledge-graph search and
knowledge-graph write.

Around those tools sit **prompts as predefined procedures**: an "update episodic
memory" prompt that tells the orchestrator how to spot and store what the user
did, a semantic-memory equivalent for preferences and style, and
"write technical article" / "write social media post" procedures that say how to
combine memory search with web search and image generation. The server composes
with off-the-shelf MCP servers (web search, image generation, Google Drive) and
re-exposes the union.

Then the actual question. Two options: **(1)** keep tools and prompts private
inside the server and expose only a custom orchestrator as a single tool, so any
client — including Claude Code — drives the whole packaged solution; or **(2)**
expose the tools and prompts and build the custom orchestrator on the client
side, where the planning logic can live in your own app, a FastAPI service, or
even a React frontend. The author has implemented both and says the choice is not
programmatic but architectural, because it propagates through the entire
application.

## Key claims

- The memory pipeline is the same shape regardless of the orchestrator question: documents → knowledge-graph extraction → embeddings over the document summary → metadata → memory. [[raw/the-right-way-of-building-agents-with-mcp-servers|cite]]
- Two tools are enough for the memory surface: knowledge-graph search and knowledge-graph write; everything else is a procedure over them. [[raw/the-right-way-of-building-agents-with-mcp-servers|cite]]
- Prompts are used here as *predefined procedures* that tell the orchestrator which tools to combine, and in what order, for a named task. [[raw/the-right-way-of-building-agents-with-mcp-servers|cite]]
- Composing prebuilt MCP servers (web search, image generation, Drive) and re-exposing the union is the default integration move — build only what does not exist. [[raw/the-right-way-of-building-agents-with-mcp-servers|cite]]
- Where the custom orchestrator lives — server-side as one packaged tool, or client-side with your own planning logic — is an open decision the author deliberately does not settle. [[raw/the-right-way-of-building-agents-with-mcp-servers|cite]]

## Notable quotes

> "Programmatically, both work — I implemented both. But from the architectural system design point of view, which solution is better? I cannot really choose, and I think it's a very important architectural decision that propagates through the entire application."
> — [[raw/the-right-way-of-building-agents-with-mcp-servers|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/mcp-primitives]], [[wiki/concepts/server-side-orchestration]], [[wiki/concepts/mcp-server-design]], [[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/agent-memory]]

> Synthesis: The one source in the wiki that leaves its central question open — useful precisely because the other notes assert the answer (composite tools, server-side) without having to build the client.
