---
type: entity
title: David Soria Parra
description: Anthropic engineer and MCP co-creator whose "Future of MCP" talk frames agent architecture as four decomposing layers, with connectivity built from skills, CLIs and MCP together.
aliases: []
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-architecture]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/agent-skills]]"
created: 2026-08-29T16:13:43Z
timestamp: 2026-08-29T16:13:43Z
source_count: 2
---

# David Soria Parra

> Anthropic engineer and MCP co-creator, known in the wiki so far through one talk's worth of framing on where agent architecture is heading.

## Definition

David Soria Parra ("DSP") works at Anthropic and is credited as an MCP co-creator. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] Both source-like pages currently in the wiki are secondhand accounts of the same event — his AI Engineer 2026 talk "The Future of MCP" — one a direct note-taker's summary of the talk, the other a LinkedIn post that cites him and quotes its central thesis. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]

> Synthesis: Two source-like pages exist, but they trace to one independent voice — DSP, in one talk — not two corroborating witnesses. Everything below should be read as "DSP argued this," not as consensus across separate sources.

## Key claims

- Frames the recent history of agents in three phases — "2024 was demos. 2025 was coding agents. 2026 is connectivity" — arguing that knowledge-worker agents, unlike sandboxed coding agents, must reach many SaaS systems, which makes every architectural layer load-bearing. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Argues connectivity is irreducibly plural: skills carry stable domain knowledge, CLIs win for pre-trained/composable/local tasks (`git`, `gh`, `kubectl`), and MCP clients handle whatever needs remote access, auth or rich semantics — "Connectivity is not one thing. The best agents use all of it – skills, CLI, MCP – together." [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Reframes the agent harness as where "agent character" actually lives (same model, same servers, different harness → different product), naming progressive tool discovery (`tool_search`) and programmatic tool calling ("code mode") as its two priority upgrades. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Holds up Cloudflare's MCP server — one JavaScript-execution tool instead of roughly 80 endpoint tools — as the model for a good MCP server being a task-shaped product surface rather than a one-to-one REST wrapper: "Every time I see someone building another REST to MCP server conversion tool, I'm — it's a bit cringe." [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- Prefers FastMCP (built by Prefect) over Anthropic's own official Python SDK for building MCP servers: "It's just way better than our Python SDK that we shipped." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- Previews near-term (June '26) MCP spec work: a stateless transport, an improved async task primitive, v2 SDKs, cross-app auth via corporate IdPs, and well-known-URL server discovery. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/mcp]]**: positioned as an MCP co-creator and the source of the wiki's four-layer account (presentation / harness / connectivity / MCP servers) of where MCP fits in agent architecture. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- **[[wiki/entities/fastmcp]]** / **[[wiki/entities/prefect]]**: endorses FastMCP over Anthropic's official SDK as the practical default for Python MCP servers. [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- **[[wiki/entities/cloudflare]]**: cites Cloudflare's server design as the model for task-shaped MCP servers. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- **[[wiki/concepts/progressive-tool-discovery]]** / **[[wiki/concepts/programmatic-tool-calling]]**: names both as the harness layer's priority upgrades. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

> Synthesis: The wiki currently knows DSP only through one reported talk; his four-layer framing is a strong candidate for the wiki's baseline vocabulary on agent architecture, but it awaits a source independent of that talk before it counts as corroborated rather than well-summarized.
