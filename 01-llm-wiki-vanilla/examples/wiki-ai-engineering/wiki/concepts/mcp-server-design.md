---
type: concept
title: MCP server design
description: Designing a server for an agent to use rather than mirroring a REST API — few well-shaped tools, composition with existing servers, procedures as prompts.
aliases: [Agent-first server design]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/owning-your-context-layer]]"
  - "[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/server-side-orchestration]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 6
---

# MCP server design

> Design the surface an agent would want, not the surface your REST API already has — then compose with servers that already exist.

## Definition

The negative rule comes first and is stated bluntly: stop converting REST APIs
one-to-one into MCP servers, because the result is an agent-hostile tool list
[[wiki/sources/the-future-of-mcp-vs-skills]]. The positive rule is to start from
how *you* would want to interact with the system and design for that. The worked
example does exactly this: a memory server exposing two tools — knowledge-graph
search and knowledge-graph write — with everything else expressed as procedures
over them [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

## Key claims

- Mechanical REST-to-MCP conversion is an anti-pattern; design for an agent instead, starting from how a human would want to use it. [[wiki/sources/the-future-of-mcp-vs-skills]]
- A small tool surface plus named procedures beats a large tool surface: two memory tools, several prompts. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Compose with prebuilt servers (web search, image generation, Drive) and re-expose the union rather than reimplementing them. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Server authors should use the rich semantics only MCP offers — apps, skills, tasks, elicitation — instead of shipping bare tool lists. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Execution environments can live on the server too: expose one and let the model compose calls in code, as Cloudflare's server does. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Design task-shaped tools (`schedule_meeting_with_summary`), not endpoint-shaped ones (`POST /calendars/{id}/events`). [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Tools should be thin delegates that own no business logic, so the same code serves both batch pipelines and live tool calls and the framework stays swappable. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Server `instructions` teach the model what the server is for before it sees a single tool schema. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Budget the output: cap results, strip embeddings and other large fields — a tool's return value is spent from the harness's context window. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- The server also carries the resources, prompts and skills that tell a harness how to read and write the memory behind it. [[wiki/sources/owning-your-context-layer]]
- And the design decision that comes first: whether to build the server at all, when a CLI already covers the case. [[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]]

## Relationships

- **[[wiki/concepts/server-side-orchestration]]**: the decision about how much of the workflow the server owns.
- **[[wiki/concepts/mcp-primitives]]**: the palette a server designer is choosing from.

> Synthesis: Both sources are really arguing the same thing from different ends — a server should expose *intent-shaped* operations, and the number of tools is a decent proxy for whether you did.
