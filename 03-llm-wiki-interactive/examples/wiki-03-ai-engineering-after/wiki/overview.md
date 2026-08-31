---
type: overview
title: ai-engineering — Overview
description: "A seventeen-source-like wiki (ten local notes, four Substack articles, and a GitHub repo now carrying two question-spawned repo notes) on MCP-based agent architecture — how agents connect to tools (skills, CLI, MCP), how they remember things (a MongoDB-backed graph store, or plain files folded into the prompt), how a coding-agent harness is actually built down to its permission-wait and subagent-spawn mechanics, and, via five self-asked questions, how the wiki has begun learning from being queried."
created: 2026-08-29T16:20:17Z
timestamp: 2026-08-31T14:51:05Z
total_sources: 17
total_pages: 42
---

# ai-engineering — Overview

## Themes

**Agent memory as a data-layer problem, with two structurally different answers.** [[wiki/sources/agentic-graphrag-via-mcp-servers]] and [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]] converge on one MongoDB cluster running `$vectorSearch` and `$graphLookup` as an alternative to polyglot persistence for [[wiki/concepts/agent-memory]]. The Decode course answers the same question with no database at all — a hand-written `AGENTS.md` plus an auto-extracted `MEMORY.md` folded straight into the prompt, per [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]. [[wiki/concepts/graphrag]] and [[wiki/concepts/knowledge-graph]] belong to the first answer only; neither shows up in the harness's own memory.

**Connectivity is plural — skills, CLI and MCP, not one protocol.** [[wiki/entities/david-soria-parra]]'s "Future of MCP" talk ([[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[wiki/sources/the-future-of-mcp-vs-skills]]) argues for a three-layer stack; the Decode repo corroborates it from the implementation side, reaching its filesystem through nine flat [[wiki/concepts/cli]]-shaped tools and its capability packages through [[wiki/concepts/skills]], with no [[wiki/concepts/mcp]] layer in either lesson. A narrower claim on the same stack — [[wiki/concepts/progressive-tool-discovery]] and [[wiki/concepts/programmatic-tool-calling]] argue the harness must defer tool schemas and let the model script its own multi-call compositions — is still untouched by the repo, whose tool set stays a flat, fixed list.

**The harness, now traced by two independent code questions.** [[wiki/concepts/agent-harness]]'s mechanics keep getting walked in code rather than summarized. The first question asked how a tool call reaches the [[wiki/concepts/permission-gate]] and what happens while it waits — answered by [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-routing-to-the-permission-gate]]: an ephemeral `asyncio.Future` in the TUI versus a durable [[wiki/entities/kitaru]] flow-scope checkpoint under `--hitl`. The second asked how a subagent is spawned and what its parent gets back — answered by [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back]]: a nested `Agent.run()` on the same installed agent, given a brand-new bypass-mode `PermissionGate` and deny resolvers rather than a flag flip, with no separate synthesis LLM call on the way back. Together they pushed [[wiki/concepts/agent-loop]], [[wiki/concepts/permission-gate]] and [[wiki/entities/pydantic-ai]] each to 4 sources and materialized [[wiki/concepts/subagents]] — a concept stuck at 1 mention last round — into its own page, backed by [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] and the new note. Three other self-asked questions probed the memory theme above instead, without sending the wiki back to a primary source.

## Index

### Entities (9)
- [[wiki/entities/claude-code]] — Anthropic's coding-agent harness: an MCP client/orchestrator and comparison baseline across six notes and a four-lesson course, and, per an independent open-source reconstruction, a harness whose own internal design has been rebuilt from its leaked source.
- [[wiki/entities/david-soria-parra]] — Anthropic engineer and MCP co-creator whose "Future of MCP" talk frames agent architecture as four decomposing layers.
- [[wiki/entities/fastmcp]] — Prefect's Python SDK for building MCP servers and clients, used across sources as a thin delivery layer with no business logic of its own.
- [[wiki/entities/kitaru]] — ZenML's durable-execution runtime backing decode's headless remote mode; its own flow-scope checkpoint is the documented alternative to the TUI's in-process permission wait.
- [[wiki/entities/modal]] — A serverless cloud platform the Decode codebase uses in two roles: a GPU/inference backend for self-hosted LLMs, and a remote sandbox backend for isolated tool execution.
- [[wiki/entities/mongodb]] — A document database pitched as a single store for operational, vector and graph data, avoiding polyglot persistence for agent memory.
- [[wiki/entities/opik]] — The tracing platform decode wires into its agent loop via OTLP spans, used both to debug the loop and to run live-scored production evals.
- [[wiki/entities/prefect]] — The workflow-orchestration company behind FastMCP, also used to orchestrate agent data/memory pipelines directly.
- [[wiki/entities/pydantic-ai]] — The Python agent framework — a typed Agent with tools and a deferrable output_type — now traced through three separate code seams: the permission wait, the agent loop, and subagent spawn/report handling.

### Concepts (16)
- [[wiki/concepts/agent-harness]] — The layer wrapping a model's raw inference loop — tools, permissions, sandboxing, context, memory, orchestration — that determines what an agent actually does.
- [[wiki/concepts/agent-loop]] — The boundary-yielding turn loop of a coding agent's interactive TUI, now distinguished both from the headless `--hitl` path and from a subagent's nested run, which reuses the parent's installed Agent rather than starting a second loop.
- [[wiki/concepts/agent-memory]] — Persistent operational/semantic/graph/event-sourced state, or plain files folded into the prompt, that lets an agent recall facts across turns.
- [[wiki/concepts/cli]] — Shelling out to local command-line tools directly; strong for sandboxed coding agents, weak for governed distribution at scale.
- [[wiki/concepts/context-compaction]] — The harness mechanism that keeps a context window from filling up, escalating from cheap elision to an LLM-written summary-plus-tail past threshold usage.
- [[wiki/concepts/graphrag]] — Retrieval assembled by traversing a knowledge graph, often fused with vector search, rather than similarity search alone.
- [[wiki/concepts/knowledge-graph]] — A typed-node/typed-edge memory structure an MCP server exposes for structured, multi-hop retrieval.
- [[wiki/concepts/mcp]] — The Model Context Protocol, framed across sources as delivery infrastructure, one peer in a connectivity stack, and the subject of an "is MCP dead" debate.
- [[wiki/concepts/mcp-applications]] — The case for designing MCP servers as task-shaped product surfaces instead of one-to-one REST wrappers.
- [[wiki/concepts/permission-gate]] — The policy layer deciding, per tool call, whether execution proceeds, is denied, or escalates to a human — now traced both to its TUI/headless wait mechanics and to the fresh bypass-mode instance every spawned subagent gets.
- [[wiki/concepts/programmatic-tool-calling]] — "Code mode": the model writes a script to compose tool calls itself instead of round-tripping through inference per step.
- [[wiki/concepts/progressive-disclosure]] — Revealing content or capability only when needed, applied at two grains: within one agent's context, and across harness environments.
- [[wiki/concepts/progressive-tool-discovery]] — Deferring tool-schema loading until the model needs it, instead of stuffing every definition into context up front.
- [[wiki/concepts/sandboxing]] — The execution boundary that isolates a coding agent's computer-use tools inside a jail instead of the host, so a mistake's blast radius shrinks without losing capability.
- [[wiki/concepts/skills]] — A folder-plus-SKILL.md convention, invoked directly by a coding-agent harness, for packaging reusable capability knowledge outside MCP.
- [[wiki/concepts/subagents]] — The wiki's newest concept: a parent agent spawning narrowed, single-use child runs that fold their reports back as one string with no separate synthesis call, materialized this round from a 1-mention wait into a 2-source page.

### Repos (1)
- [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] — An educational Python coding agent (`decode`) built from a ~20-line pydantic-ai loop plus the harness around it, now with two question-spawned repo notes tracing the permission gate's wait mechanics and the subagent spawn/report call chain.

## Health

- Sources: 14 · Repos: 3 · Entities: 9 · Concepts: 16
- Slugs at 1 mention (waiting for a second): abhishek-bhardwaj, agent-architecture, agent-skills, anthropic, claude-md, cloudflare, codex, context-layer, decode-agent, docker, durable-execution, event-sourcing, hybrid-search, lsp-server, maxime-labonne, mongosh, orchestrator-placement, pi, prefect-horizon, steering-queue, terminal-bench, ty, unified-memory, vector-search
