---
type: entity
title: David Soria Parra
description: "MCP co-creator at Anthropic whose 2026 AI Engineering conference talk frames modern AI-agent architecture as four independent layers glued together by MCP."
aliases: []
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/code-mode]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/mcp-applications]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/cloudflare]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
source_count: 2
---

# David Soria Parra

> MCP co-creator at Anthropic — both wiki sources are secondhand renderings of the same 2026 conference talk.

## Definition

David Soria Parra is identified in both source pages as a co-creator of MCP at Anthropic. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]] places his remarks at "AI Engineer 2026," while [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] places the same material at "an AI Engineering conference" — almost certainly one and the same talk, named slightly differently by each note-taker rather than two separate appearances. Neither page is primary reporting: one is a structured note-taking breakdown of the talk, the other a quote-driven, LinkedIn-style distillation of it.

## Key claims

- Frames the industry's trajectory as "2024 was demos, 2025 was coding agents, 2026 is connectivity," arguing general knowledge-worker agents need more surface area than sandboxed coding agents because they must reach many SaaS apps. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Argues serious AI-application architecture decomposes into four independent, stacked layers — presentation, harness/runtime, connectivity, and MCP servers — with MCP as the connective tissue between them. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Holds that "connectivity is not one thing": skills, CLIs and MCP clients are distinct, complementary primitives (skills for stable domain knowledge, CLIs for local/composable surfaces, MCP for auth, remote access and rich semantics), and the best agents combine all three rather than leaning on one mechanism. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Criticizes endpoint-shaped MCP servers built as one-to-one REST wrappers ("it's a bit cringe"), arguing servers should instead expose task-shaped tools such as `schedule_meeting_with_summary`. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Personally endorses FastMCP, built by Prefect, as the practical default Python implementation for MCP servers, quoted saying it is "way better than our Python SDK that we shipped" — preferring it over Anthropic's own official SDK. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

## Relationships

- **MCP**: Co-created the protocol and positions it as the connective tissue across all four architecture layers. [[wiki/concepts/mcp]]
- **Agent connectivity / Skills / CLI**: Source of the "connectivity is not one thing" framing treating skills, CLIs, and MCP clients as complementary, not competing. [[wiki/concepts/agent-connectivity]]
- **FastMCP / Prefect**: Publicly prefers FastMCP over Anthropic's own Python SDK for building MCP servers. [[wiki/entities/fastmcp]]
- **Claude Code**: Cites it as having shipped progressive tool discovery, a harness pattern his talk calls out. [[wiki/entities/claude-code]]
- **Cloudflare**: Cites Cloudflare's single-JS-execution-tool MCP server as the canonical example of server-side code mode. [[wiki/entities/cloudflare]]

> Synthesis: Both source pages trace to the same talk, so this page rests on one voice heard twice, not two independent witnesses — treat the overlapping claims above (the four-layer framing, "connectivity is not one thing") as a single data point corroborated only by agreement between two note-takers, not by separate evidence.
