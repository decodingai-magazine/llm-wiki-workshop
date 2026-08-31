---
type: concept
title: Agent Orchestration Placement
description: The architectural question of where and how an agent's multi-step planning logic runs — server-side as one composite tool, or client-side across several round-trips.
aliases:
  - orchestration
  - orchestrator placement
  - programmatic tool calling
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/entities/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]"
  - "[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 3
---

# Agent Orchestration Placement

> Where should multi-step planning logic live — baked into the server as one tool, or driven from the client one call at a time? This wiki's sources disagree, deliberately.

## Definition

Server-side orchestration packages an entire multi-step workflow as one composite MCP tool: a single request runs every step, guaranteeing execution order and preventing the model from skipping or reordering steps. Client-side orchestration instead exposes each step as its own tool and lets the model (or a custom orchestrator) call them one at a time, trading that guaranteed order for flexibility — at the cost of more round-trips, latency, and token spend. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]

A related technique, programmatic ("code mode") tool calling, tries to get the flexibility of client-side orchestration without its round-trip cost: instead of the model calling one tool, reading the result, and calling the next, it gives the model an execution environment (e.g., a V8 isolate) to write code that composes several tool calls together in one shot. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]

Whether the orchestrator itself belongs inside the MCP server (exposed as a single tool to any client) or on the MCP client side (with the server exposing only raw tools and prompts) is presented as a genuinely open, unresolved question — even by someone who has implemented both. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Key claims

- Server-side orchestration (one composite tool doing all steps in a single request) guarantees execution order and prevents the model from skipping or reordering steps, at the cost of flexibility; client-side (tool-by-tool) orchestration is more flexible but adds round-trips, latency, and skip/reorder risk. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Programmatic/code-mode tool calling — giving the model an execution environment to write composing code instead of chaining tool calls turn by turn — cuts the latency and token cost of model-driven orchestration; MCP's structured-output feature helps the model type-check the composition as it writes it. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- Whether a custom orchestrator belongs inside the MCP server (exposed as a single tool) or on the MCP client side (with the server exposing raw tools/prompts) is an unresolved architectural question, even for someone who has implemented both options. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **[[wiki/entities/mcp]]**: MCP's structured output and composed-server model both bear directly on where orchestration logic can live. [[wiki/entities/mcp]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]**: a pre-built orchestrator option, as an alternative to writing a custom client-side one. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/claude-code]]
- **[[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]**: memory tools and the prompts that guide them are exactly the kind of steps a custom orchestrator has to sequence. [[01-llm-wiki-vanilla/examples/wiki-ai-engineering/wiki/concepts/agent-memory]]

> Synthesis: The one open question in this wiki without a settled answer — every source that touches it argues tradeoffs rather than declaring a winner.
