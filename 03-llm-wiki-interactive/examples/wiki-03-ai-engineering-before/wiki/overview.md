---
type: overview
title: ai-engineering — Overview
description: A fifteen-source-like wiki (ten local notes, four Substack articles, one GitHub repo) on MCP-based agent architecture — how agents should connect to tools (skills, CLI, MCP), how they should remember things (MongoDB-backed GraphRAG, event-sourced memory, or plain files folded into the prompt), and, now via a working codebase and four of its own course articles, how the harness underneath a coding agent is actually built.
created: 2026-08-29T16:20:17Z
timestamp: 2026-08-29T17:14:29Z
total_sources: 15
total_pages: 39
---

# ai-engineering — Overview

## Themes

**Agent memory as a data-layer problem — now with two structurally different
answers.** Three notes converge on the same concrete question — where does an
agent's knowledge graph actually live, and what does it cost to query it? —
and land on one MongoDB cluster running `$vectorSearch` and `$graphLookup`
instead of a polyglot stack: [[wiki/sources/agentic-graphrag-via-mcp-servers]]
builds a working FastMCP server on it,
[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]] supplies the
vendor-side case against polyglot persistence, and
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] uses it as
the memory layer behind a knowledge-graph tool. [[wiki/concepts/agent-memory]]
now holds a second, code-grounded answer with two independent witnesses of its
own: the
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
codebase and its companion piece
[[wiki/sources/article-context-engineering-for-coding-agents]] both describe
memory as a hand-written `AGENTS.md` plus an auto-extracted `MEMORY.md` folded
straight into the prompt — no database, no vector index, no graph at all. The
concept page keeps both mechanisms side by side rather than averaging them
into mush.

**Connectivity is plural — skills, CLI and MCP, not one protocol.**
[[wiki/entities/david-soria-parra]]'s "Future of MCP" talk argues for a
three-layer stack where [[wiki/concepts/skills]] carry stable domain
knowledge, [[wiki/concepts/cli]] wins for sandboxed local tasks, and
[[wiki/concepts/mcp]] is reserved for remote access and governance, reaching
this wiki through
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
and [[wiki/sources/the-future-of-mcp-vs-skills]]. The Decode course now
corroborates this from the implementation side twice over:
[[wiki/sources/article-the-coding-agent-loop]] shows `decode` reaching its
filesystem and shell through nine flat, CLI-shaped tools, and
[[wiki/sources/article-context-engineering-for-coding-agents]] shows it
loading capability packages through a three-tier skills mechanism — no MCP
layer in either lesson — which is why [[wiki/concepts/cli]] and
[[wiki/concepts/skills]] have each picked up new sources from code and course
commentary, not argument alone.

**The harness carries the tool-use efficiency work.** A narrower claim from
the same talk material: [[wiki/concepts/progressive-tool-discovery]] (defer a
tool's schema until it's needed) and
[[wiki/concepts/programmatic-tool-calling]] (the model writes a script instead
of round-tripping through inference per call) are what make an MCP-heavy stack
workable at scale, both routing through [[wiki/concepts/mcp-applications]]'s
pitch that servers should be task-shaped surfaces, not REST wrappers.
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
and [[wiki/sources/the-future-of-mcp-vs-skills]] make the MCP-side case;
[[wiki/sources/article-context-engineering-for-coding-agents]] now supplies
progressive-tool-discovery's third source from a different angle entirely —
Decode's own skill catalog costs 7–9% of the context window in tool schemas
before tiered disclosure fixes it. Programmatic tool calling and
mcp-applications remain untouched by the repo, whose own tool set is still a
flat, fixed list rather than a discovery problem.

**The harness itself, now four working parts instead of one abstraction.**
[[wiki/concepts/agent-harness]] graduated from a single article's framing to a
6-source concept the moment the Decode course arrived, and three sub-mechanisms
the previous version of this page flagged as "repo-only, no second source yet"
have each now materialized as their own concept page:
[[wiki/concepts/agent-loop]] (the ReAct-style plan/explore/apply/execute/observe
cycle, corroborated by [[wiki/sources/article-the-coding-agent-loop]] against
the repo), [[wiki/concepts/permission-gate]] (ask/allow/deny per tool call,
modeled explicitly on Claude Code's approval modes, per
[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]),
and [[wiki/concepts/context-compaction]] (microcompaction at 60% capacity, full
LLM-summary compaction at 80%, detailed line-by-line in
[[wiki/sources/article-context-engineering-for-coding-agents]]).
[[wiki/concepts/sandboxing]] — reconciled from the repo's own `agent-sandboxing`
slug — now has its clearest source yet in
[[wiki/sources/article-run-coding-agents-safely]], which builds the
`CommandExecutor`/`SandboxExecutor` seam over Docker and Modal backends the
repo only showed as code. The entities behind all of this —
[[wiki/entities/pydantic-ai]] (the ~20-line loop itself),
[[wiki/entities/modal]] (sandbox and inference backend),
[[wiki/entities/kitaru]] (the durable remote runtime), and
[[wiki/entities/opik]] (tracing and evals) — are now real pages instead of a
slug list waiting on a second mention.
[[wiki/concepts/durable-execution]] and [[wiki/concepts/subagents]] are the two
pieces of that same architecture still waiting.
> Synthesis: this is what the wiki's context-discipline rule (CONVENTIONS.md
> §12) is for — four articles from one course each corroborated a different
> corner of one codebase, and the concept pages absorbed each corroboration
> into an existing structure instead of a fresh page restating the repo.

## Index

### Entities (9)
- [[wiki/entities/claude-code]] — Anthropic's coding-agent harness: an MCP client/orchestrator and comparison baseline across six notes and a four-lesson course, and, per an independent open-source reconstruction, a harness whose own internal design has been rebuilt from its leaked source.
- [[wiki/entities/david-soria-parra]] — Anthropic engineer and MCP co-creator whose "Future of MCP" talk frames agent architecture as four decomposing layers.
- [[wiki/entities/fastmcp]] — Prefect's Python SDK for building MCP servers and clients, used across sources as a thin delivery layer with no business logic of its own.
- [[wiki/entities/kitaru]] — ZenML's durable-execution runtime that backs decode's headless remote mode, orchestrating checkpointed, replayable agent flows in parallel on Modal.
- [[wiki/entities/modal]] — A serverless cloud platform the Decode codebase uses in two roles: a GPU/inference backend for self-hosted LLMs, and a remote sandbox backend for isolated tool execution.
- [[wiki/entities/mongodb]] — A document database pitched as a single store for operational, vector and graph data, avoiding polyglot persistence for agent memory.
- [[wiki/entities/opik]] — The tracing platform decode wires into its agent loop via OTLP spans, used both to debug the loop and to run live-scored production evals.
- [[wiki/entities/prefect]] — The workflow-orchestration company behind FastMCP, also used to orchestrate agent data/memory pipelines directly.
- [[wiki/entities/pydantic-ai]] — The Python agent framework — a typed Agent with tools and a deferrable output_type — that decode's entire agent loop is built directly on top of.

### Concepts (15)
- [[wiki/concepts/agent-harness]] — The layer wrapping a model's raw inference loop — tools, permissions, sandboxing, context, memory, orchestration — that determines what an agent actually does.
- [[wiki/concepts/agent-loop]] — The boundary-yielding turn loop of a coding agent — plan/explore/apply/execute/observe, with no hard-coded step cap, steerable only at two defined checkpoints.
- [[wiki/concepts/agent-memory]] — Persistent operational/semantic/graph/event-sourced state, or plain files folded into the prompt, that lets an agent recall facts across turns.
- [[wiki/concepts/cli]] — Shelling out to local command-line tools directly; strong for sandboxed coding agents, weak for governed distribution at scale.
- [[wiki/concepts/context-compaction]] — The harness mechanism that keeps a context window from filling up, escalating from cheap elision to an LLM-written summary-plus-tail past threshold usage.
- [[wiki/concepts/graphrag]] — Retrieval assembled by traversing a knowledge graph, often fused with vector search, rather than similarity search alone.
- [[wiki/concepts/knowledge-graph]] — A typed-node/typed-edge memory structure an MCP server exposes for structured, multi-hop retrieval.
- [[wiki/concepts/mcp]] — The Model Context Protocol, framed across sources as delivery infrastructure, one peer in a connectivity stack, and the subject of an "is MCP dead" debate.
- [[wiki/concepts/mcp-applications]] — The case for designing MCP servers as task-shaped product surfaces instead of one-to-one REST wrappers.
- [[wiki/concepts/permission-gate]] — The policy layer that decides, per tool call, whether execution proceeds automatically, is denied, or is escalated to a human — modeled in Decode on Claude Code's approval modes.
- [[wiki/concepts/programmatic-tool-calling]] — "Code mode": the model writes a script to compose tool calls itself instead of round-tripping through inference per step.
- [[wiki/concepts/progressive-disclosure]] — Revealing content or capability only when needed, applied at two grains: within one agent's context, and across harness environments.
- [[wiki/concepts/progressive-tool-discovery]] — Deferring tool-schema loading until the model needs it, instead of stuffing every definition into context up front.
- [[wiki/concepts/sandboxing]] — The execution boundary that isolates a coding agent's computer-use tools inside a jail instead of the host, so a mistake's blast radius shrinks without losing capability.
- [[wiki/concepts/skills]] — A folder-plus-SKILL.md convention, invoked directly by a coding-agent harness, for packaging reusable capability knowledge outside MCP.

### Repos (1)
- [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] — An educational Python coding agent (`decode`) built from a ~20-line pydantic-ai loop plus the harness around it: permission gate, sandbox seam, memory, compaction, skills, subagent fan-out, durable headless runtime.

## Health

- Sources: 14 · Repos: 1 · Entities: 9 · Concepts: 15
- Slugs at 1 mention (waiting for a second): abhishek-bhardwaj, agent-architecture, agent-skills, anthropic, claude-md, cloudflare, codex, context-layer, decode-agent, docker, durable-execution, event-sourcing, hybrid-search, lsp-server, maxime-labonne, mongosh, orchestrator-placement, pi, prefect-horizon, steering-queue, subagents, terminal-bench, ty, unified-memory, vector-search
