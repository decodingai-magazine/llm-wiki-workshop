---
type: overview
title: ai-engineering — Overview
description: What 53 notes and articles, one codebase and the questions asked of them add up to — connectivity as a layered choice, memory worth owning, and the orchestration that keeps both alive.
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T11:50:00Z
total_sources: 55
total_pages: 109
---

# ai-engineering — Overview

> Fifty local notes, three articles and one codebase on how agents connect to the world, what they remember, and what it costs to keep that memory correct — plus what has been asked of them since.

## Themes

### Connectivity is a stack, not a choice

[[wiki/concepts/connectivity-stack]] holds that [[wiki/concepts/agent-skills]],
[[wiki/concepts/cli-tools]] and [[wiki/entities/mcp]] each answer a different
question, and that single-mechanism agents underperform. Stated in
[[wiki/sources/the-future-of-mcp-vs-skills]], laid out as a system in
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], and
tested from the other side by
[[wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres]], which
replaces a whole server with one line of instruction.

### The harness is the part you engineer

[[wiki/concepts/agent-harness]] owns the loop, the context window, permissions and
memory — and the wiki's sharpest number belongs here: changing only the harness
moved a coding agent from ~30th to the top 5 on the same benchmark
[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]. The
claims are checkable against
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]],
where [[wiki/concepts/agent-skills]] are folders with a `SKILL.md`,
[[wiki/concepts/context-rot]] is answered by two tiers of compaction, and
[[wiki/concepts/durable-execution]] means every turn is checkpointed.

### Memory is the asset; the graph is the shape of it

[[wiki/concepts/context-layer]] is the *why* — models and harnesses commoditize,
the memory you can carry does not
[[wiki/sources/owning-your-context-layer]]. The *how* runs through
[[wiki/concepts/unified-memory]], [[wiki/concepts/knowledge-graph]],
[[wiki/concepts/graph-extraction]], [[wiki/concepts/entity-resolution]],
[[wiki/concepts/hybrid-search]] and [[wiki/concepts/agentic-search]], built end to
end in [[wiki/sources/agentic-graphrag-via-mcp-servers]] and priced out on
[[wiki/entities/mongodb]].

### Correctness over time is the unsolved part

[[wiki/concepts/append-only-log]] and [[wiki/concepts/materialized-view]] exist to
make knowledge *correctable* — and [[wiki/concepts/database-scaling]] is the bill.
[[wiki/sources/modeling-knowledge-graph-collections-append-only-log-vs-one]] is the
only source written after that design was reversed, and
[[wiki/concepts/knowledge-freshness]] collects the questions readers keep asking
that the wiki still cannot answer.

### Orchestration is what makes any of it survive

[[wiki/concepts/durable-execution]] is the wiki's most-cited operational claim:
retries, caching and checkpoints turn a failure into a resumption instead of a
re-run. [[wiki/concepts/pipeline-parallelism]] is how the same pipelines get fast,
[[wiki/concepts/read-write-separation]] is the rule about where to apply both, and
[[wiki/concepts/inference-economics]] is why it pays for itself.

## Index

### Entities (10)
- [[wiki/entities/mongodb]] — the single store behind the memory layer (24 sources).
- [[wiki/entities/prefect]] — orchestration, argued into the agent runtime (20).
- [[wiki/entities/claude-code]] — the reference harness (14).
- [[wiki/entities/mcp]] — the protocol, treated as one layer of a stack (11).
- [[wiki/entities/fastmcp]] — the framework the servers are built with (10).
- [[wiki/entities/langchain]] — the framework these notes left, and why (3).
- [[wiki/entities/voyage-ai]] — the embedding provider, chosen for integration (3).
- [[wiki/entities/anthropic]] — author of the protocol and its roadmap (3).
- [[wiki/entities/modal]] — serverless GPUs, the self-hosting tier (5).
- [[wiki/entities/david-soria-parra]] — origin of the connectivity framing (2).

### Concepts (38)

**Connectivity and protocol** — [[wiki/concepts/connectivity-stack]],
[[wiki/concepts/agent-skills]], [[wiki/concepts/cli-tools]],
[[wiki/concepts/mcp-primitives]], [[wiki/concepts/skills-over-mcp]],
[[wiki/concepts/mcp-apps]], [[wiki/concepts/mcp-server-design]],
[[wiki/concepts/server-side-orchestration]], [[wiki/concepts/programmatic-tool-calling]],
[[wiki/concepts/governance]].

**Harness and runtime** — [[wiki/concepts/agent-harness]],
[[wiki/concepts/progressive-disclosure]], [[wiki/concepts/context-rot]],
[[wiki/concepts/durable-execution]], [[wiki/concepts/observability]],
[[wiki/concepts/agentic-coding-loop]], [[wiki/concepts/provider-abstraction]],
[[wiki/concepts/inference-economics]], [[wiki/concepts/infrastructure-over-frameworks]].

**Memory and retrieval** — [[wiki/concepts/context-layer]],
[[wiki/concepts/unified-memory]], [[wiki/concepts/agent-memory]],
[[wiki/concepts/knowledge-graph]], [[wiki/concepts/graph-extraction]],
[[wiki/concepts/entity-resolution]], [[wiki/concepts/embeddings]],
[[wiki/concepts/hybrid-search]], [[wiki/concepts/agentic-search]],
[[wiki/concepts/graph-communities]], [[wiki/concepts/graph-visualization]],
[[wiki/concepts/data-fragmentation]].

**Storage and operations** — [[wiki/concepts/append-only-log]],
[[wiki/concepts/materialized-view]], [[wiki/concepts/database-scaling]],
[[wiki/concepts/knowledge-freshness]], [[wiki/concepts/graphrag-ingestion]],
[[wiki/concepts/pipeline-parallelism]], [[wiki/concepts/read-write-separation]].

### Repos (2 pages, 1 repo)
- [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] — a coding-agent harness where the wiki's claims are executable.
- [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-to-permission-gate-routing]] — a question answered against the code, which then became evidence.

### Interaction (5 questions · 1 note)
- [[wiki/questions/index|Questions]] — every question asked of this wiki, one line each.
- [[wiki/notes/append-only-log-vs-in-place-updates]] — the wiki's one live architectural disagreement, worked through.
- [[wiki/open-questions]] — what it knows it cannot answer yet.

### And what it learned from being asked

Two questions produced [[wiki/notes/append-only-log-vs-in-place-updates]] — the
second enriched it rather than forking it. One produced a **repo note** that became
source-like and pushed [[wiki/concepts/agent-harness]],
[[wiki/concepts/durable-execution]] and [[wiki/concepts/agentic-coding-loop]] up a
source each. Two produced entries in [[wiki/open-questions]], and the next ingest
answered one of them — [[wiki/sources/article-context-engineering-for-coding-agents]]
turned [[wiki/concepts/context-rot]] from a qualitative worry into thresholds.

## Health

- Source-like pages: 55 (50 notes · 3 articles · 1 repo doc · 1 repo note) · Entities: 10 · Concepts: 38
- Interaction layer: 5 questions · 1 note · 2 open questions (1 apparently addressed, not resolved)
- Waiting at 1 mention: `agentic-invocation`, `continual-learning`, `rag-evaluation`,
  `reasoning-memory`, and the entities `neo4j`, `obsidian`.
- Most-cited: `knowledge-graph` (22), `durable-execution` (16), `unified-memory` (15),
  `agent-harness` (14), `hybrid-search` (13), `embeddings` (12).
- Watch for false corroboration: [[wiki/sources/graphrag-presentation]],
  [[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]],
  [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]] and
  [[wiki/sources/ingesting-knowledge-graph-objects-for-graphrag-with-mongodb]] overlap
  heavily; so do the two task-runner notes. Several sources are sponsor-facing.
