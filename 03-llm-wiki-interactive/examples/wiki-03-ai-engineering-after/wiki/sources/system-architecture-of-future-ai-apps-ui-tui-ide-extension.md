---
type: source
title: "System architecture of future AI apps: UI/TUI/IDE extension ↔ harness ↔ connectivity"
description: A layered breakdown of where future AI apps are converging — presentation, harness, connectivity, and MCP servers — as none of the four stays monolithic.
origin: local
original_path: data_input_examples/notes/02-medium/System architecture of future AI apps UI-TUI-IDE extension ↔ harness ↔ connectivity.md
source_url:
authors: []
published_date:
raw_file: raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension.md
created: 2026-08-29T16:10:14Z
timestamp: 2026-08-29T16:10:14Z
entities:
  - "[[wiki/entities/david-soria-parra]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/cloudflare]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/mcp-applications]]"
  - "[[wiki/concepts/skills]]"
---

# System architecture of future AI apps: UI/TUI/IDE extension ↔ harness ↔ connectivity

> [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension|Raw]] · local

## Summary

Notes on David Soria Parra's (DSP, Anthropic) AI Engineer 2026 talk "The Future of MCP," breaking future AI-app architecture into four layers: presentation (UI/TUI/IDE), harness (the agent loop and everything around it), connectivity (skills, CLIs, MCP clients), and MCP servers. DSP's framing is that 2024 was demos, 2025 was coding agents, and 2026 is connectivity — coding agents got by on a local sandbox and a 2D UI, but general knowledge-worker agents must reach many SaaS systems, which makes every one of the four layers load-bearing. The note's throughline is decomposition: no layer is monolithic anymore, so capabilities, UI and domain knowledge can travel independently of where the agent actually runs.

The bulk of the argument lives in the harness and connectivity layers. The harness is reframed as the place "agent character" actually lives (same model, same servers, different harness → different product), and its two must-build patterns are progressive tool discovery (`tool_search` instead of eager schema-stuffing) and programmatic tool calling ("code mode," letting the model write scripts against MCP's structured output instead of chaining inference round-trips). Connectivity is argued to be irreducibly plural — skills, CLIs and MCP clients each own a different job, and single-mechanism agents underperform.

## Key claims

- Future AI-app architecture converges on four layers — presentation, harness, connectivity, MCP servers — each undergoing its own decomposition. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#1. The Big Picture|cite]]
- "2024 was demos. 2025 was coding agents. 2026 is connectivity": knowledge-worker agents (unlike sandboxed coding agents) must reach many SaaS apps, so no layer is optional. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#1. The Big Picture|cite]]
- The harness, not the protocol, decides what happens with the bytes MCP moves; its two priority upgrades are progressive tool discovery via `tool_search` and programmatic tool calling ("code mode") through a sandboxed execution environment. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#3. Layer 2 — The Harness|cite]]
- Connectivity is not one mechanism: skills carry stable domain knowledge, CLIs win for pre-trained/composable/local tasks (`git`, `gh`, `kubectl`), and MCP clients handle everything needing remote access, auth, or rich semantics. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#4. Layer 3 — Connectivity (Skills, CLIs, MCP Clients)|cite]]
- Good MCP servers should be task-shaped product surfaces (tools + UI + skills + tasks), not one-to-one REST wrappers; Cloudflare's server — one JavaScript-execution tool instead of 80 endpoint tools — is DSP's canonical example. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#5.2 Server-Side Execution Environments|cite]]
- Near-term (June '26) MCP spec work adds a stateless transport, an improved async task primitive, v2 SDKs, cross-app auth via corporate IdPs, and well-known-URL server discovery. [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#5.4 Infrastructure Coming Down the Line|cite]]

## Notable quotes

> "If you're a CLI you just have a hard time rendering HTML."
> — [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#2. Layer 1 — Presentation (UI / TUI / IDE Extension)|location]]

> "Every time I see someone building another REST to MCP server conversion tool, I'm — it's a bit cringe."
> — [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#5.1 Stop Wrapping REST APIs One-to-One|location]]

> "You do one call and you can filter that. The model will automatically remove things from the JSON and just continue."
> — [[raw/system-architecture-of-future-ai-apps-ui-tui-ide-extension#3.2 Programmatic Tool Calling (Code Mode)|location]]

## Connections

- **Entities**: [[wiki/entities/david-soria-parra]], [[wiki/entities/claude-code]], [[wiki/entities/cloudflare]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/agent-harness]], [[wiki/concepts/progressive-tool-discovery]], [[wiki/concepts/programmatic-tool-calling]], [[wiki/concepts/mcp-applications]], [[wiki/concepts/skills]]

> Synthesis: This is a structured secondhand account of one talk (DSP's "The Future of MCP"), not firsthand argument — its four-layer vocabulary (presentation/harness/connectivity/servers) is a strong candidate for the wiki's baseline framing of agent architecture until another source corroborates or complicates it.
