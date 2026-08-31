---
type: overview
title: ai-engineering — Overview
description: A 14-source wiki on 2026 agent architecture, now anchored by one ingested repo (Decode), tracing two intertwined arguments — that MCP, Skills and CLI are complementary connectivity layers, and that the coding-agent harness, not the model, is the real object of design — alongside open questions on orchestration placement and unified agent memory.
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:20:00Z
total_sources: 14
total_pages: 32
---

# ai-engineering — Overview

## Themes

**Connectivity is not one thing.** A core cluster converges on a single claim,
argued most explicitly by MCP co-creator David Soria Parra: agents reach
capabilities through several complementary mechanisms — skills, CLI, MCP —
rather than one universal layer.
[[wiki/concepts/mcp]], [[wiki/concepts/skills]], [[wiki/concepts/cli]] and
[[wiki/concepts/agent-connectivity]] are its pages.
[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
states it most tersely ("Connectivity is not one thing. The best agents use
all of it"); [[wiki/sources/the-future-of-mcp-vs-skills]] argues it most fully.

**Where should orchestration logic live?** A narrower, unresolved question
sits under [[wiki/concepts/orchestration]]: does custom planning logic belong
packaged inside the MCP server as one exposed tool, or on the client side
driving raw tools and prompts? [[wiki/entities/fastmcp]] and
[[wiki/entities/claude-code]] are the recurring client/server building
blocks. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
poses the question and declines to answer it ("I cannot really choose");
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] takes
the narrower stance that deterministic pipelines belong as composite tools,
not MCP prompts.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
now answers concretely on the client side: Decode's `agent` tool fans out
subagents entirely inside the harness, no MCP server involved.

**Unifying agent memory — or refusing to.** [[wiki/concepts/agent-memory]]
holds two incompatible framings side by side: a queryable knowledge graph
reached through MCP tools ([[wiki/concepts/graphrag]],
[[wiki/entities/mongodb]]), versus flat AGENTS.md/MEMORY.md files loaded
wholesale into the system prompt.
[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]] makes the graph case
most concretely, with explicit scale thresholds; [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
makes the opposite bet ("Just-in-time reads beat a stale heavy index"), now
backed by Decode's own code — `assemble_memory()` really does just
concatenate the two files into the prompt every turn.

**The harness, not the model, makes the agent.** Five sources — four lessons
plus the codebase of Paul Iusztin's course *Building a Coding Agent From
Scratch* — anchor on [[wiki/entities/decode]], a Pydantic-AI harness at
feature parity with Claude Code, Pi and OpenCode, now durable/replayable via
[[wiki/entities/kitaru]]. [[wiki/concepts/agent-harness]] anchors the cluster
and still records the
wiki's sharpest live disagreement: [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
draws harness = agent minus the tool-calling loop ("The model isn't what
makes a coding agent good. The harness is."), while
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
puts the loop inside the harness layer and Skills outside it — the two never
cite each other.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
settles it in code: the model call is ~20 lines; permissions, sandboxing,
compaction and subagent fan-out are the majority of the codebase.

## Index

### Entities (9)
- [[wiki/entities/claude-code]] — Anthropic's agentic coding harness and MCP client — the reference implementation cited across both clusters.
- [[wiki/entities/david-soria-parra]] — MCP co-creator whose talk frames agent architecture as four layers glued together by MCP.
- [[wiki/entities/decode]] — Paul Iusztin's Python coding agent, built lesson-by-lesson in his open-source harness course.
- [[wiki/entities/fastmcp]] — Prefect's Python framework for MCP servers/clients — the wiki's default MCP implementation.
- [[wiki/entities/kitaru]] — ZenML's agent runtime — gives Decode's headless/remote mode durability and replay.
- [[wiki/entities/modal]] — Cloud compute platform Decode uses as both a remote sandbox and a self-hosted LLM-serving provider.
- [[wiki/entities/mongodb]] — Document database used as a knowledge-graph store, a proposed unified memory layer, and a database reached via `mongosh` instead of a bespoke MCP server.
- [[wiki/entities/prefect]] — Workflow-orchestration company behind FastMCP, positioned as core agent-runtime infrastructure.
- [[wiki/entities/pydantic-ai]] — Python agent framework whose ~20-line `Agent` object is Decode's tool-calling loop.

### Concepts (8)
- [[wiki/concepts/agent-connectivity]] — Agents should reach capabilities through several complementary mechanisms — skills, CLI, MCP — not one universal layer.
- [[wiki/concepts/agent-harness]] — The infrastructure around a coding agent's loop — sandbox, permissions, memory, skills, evals — with sources disagreeing on where its boundary sits.
- [[wiki/concepts/agent-memory]] — The persistent context layer, framed either as a queryable knowledge graph or as flat markdown loaded into the system prompt.
- [[wiki/concepts/cli]] — A command-line connectivity mechanism, strong locally, weak at governed distribution to many users.
- [[wiki/concepts/graphrag]] — Retrieval that augments vector search with graph traversal, pulling multi-hop context instead of isolated chunks.
- [[wiki/concepts/mcp]] — Open protocol connecting agents to tools/data/systems, treated as one leg of a connectivity stack, not a universal mechanism.
- [[wiki/concepts/orchestration]] — Where tool-sequencing logic should live — inside an MCP server or on the client — plus the loop-level efficiency techniques.
- [[wiki/concepts/skills]] — A folder-with-SKILL.md convention for packaged domain knowledge — sources disagree whether it's harness-native or a coequal connectivity layer.

### Repos (1)
- [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] — Decode's own codebase — a ~20-line Pydantic AI loop in a harness (permissions, sandboxing, memory, compaction, subagent fan-out, Kitaru) — the harness-not-model argument made concrete.

## Health

- Sources: 14 · Entities: 9 · Concepts: 8 · Repos: 1
- Slugs at 1 mention (waiting for a second): abhishek-bhardwaj, ai-evals, claude-md, cloudflare, code-mode, codex-cli, compaction, context-engineering, context-layer, docker, event-sourcing, hooks, lsp, mario-zechner, maxime-labonne, mcp-applications, mongosh, neo4j, opencode, openrouter, opik, pi-agent, progressive-disclosure, progressive-tool-discovery, sandboxing, ty, unified-memory, vector-search
</content>
