---
type: concept
title: Agent Memory
description: The persistent state — operational, semantic/vector, relational-graph, event-sourced, or plain markdown files folded into the prompt — that lets an AI agent recall facts and past interactions across turns and sessions.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
related:
  - "[[wiki/concepts/vector-search]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/graphrag]]"
  - "[[wiki/concepts/event-sourcing]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/orchestrator-placement]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
created: 2026-08-29T16:14:37Z
timestamp: 2026-08-29T17:09:42Z
source_count: 5
---

# Agent Memory

> Multiple framings — see Definition

## Definition

Five sources decompose "agent memory" three different ways: infrastructure-heavy, pipeline-output, and plain-file — the last now attested by three sources drawn from a single project rather than one.

The MongoDB source frames memory as **four layers** on one database: operational memory (per-user/session state), semantic memory (vector-searchable recall), a relational knowledge graph (multi-hop reasoning), and an immutable, event-sourced log of the graph's evolution — arguing a single MongoDB Atlas cluster can host all four instead of a "polyglot" stack. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]

The MCP-servers source frames memory as the **output of a pipeline**: ingested documents become knowledge-graph objects (entities/relationships) plus summary embeddings plus metadata, exposed to an orchestrator through MCP tools and prompts. It separately splits **episodic memory** (what a user did at a moment) from **semantic memory** (general preferences) as a content-level distinction, not an infrastructure one. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

The `decode` coding-agent codebase implements memory as neither a database nor a graph pipeline: two markdown files, `AGENTS.md` and `MEMORY.md`, read from disk and concatenated — alongside the base persona, active-agent prompt, and skills catalog — into the single instructions block rebuilt fresh every run. Files layer **root-most to cwd-most** (a directory-hierarchy override, not a database query), and `MEMORY.md` is explicitly size-capped to bound how much context it can consume. No vector index, knowledge graph, or event log exists anywhere in the subsystem. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

Two Substack articles from the same course as the `decode` repo — written by the same author — describe that identical file-based subsystem in more detail and argue *for* it, rather than merely implementing it. The lesson-1 system-design article lists memory as one of six harness modules: "plain `AGENTS.md` + `MEMORY.md` files, deliberately no memory database or codebase index," with a stated principle for the omission — "Just-in-time reads beat a stale heavy index." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] The lesson-4 context-engineering article specifies the mechanism the repo's own architecture page only sketches: `AGENTS.md` is hand-written project context (root-most file wins, ~300-line target, ~600-line guardrail), while `MEMORY.md` is auto-extracted — one LLM-written summary sentence appended per session, capped at 200 lines/25,000 bytes with oldest lines dropped first — a scheme the article says mirrors Claude Code's own auto-memory. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

## Key claims

- A vector/embedding recall layer appears in both article sources — MongoDB's `$vectorSearch` over quantized embeddings, the MCP source's "summary embeddings" computed during ingestion — but not in `decode` or either Substack piece about it, whose memory is unindexed text the model reads directly. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- A knowledge-graph component for multi-hop reasoning appears in both article sources — MongoDB via bounded (2–3 hop) `$graphLookup`, the MCP source via a "knowledge graph extractor" over ingested documents — with no analogue in `decode`. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The MongoDB source additionally isolates an **operational memory** layer (per-user/session BSON state updated with `$set`/`$push`/`$inc`) and treats knowledge-graph state as **event-sourced** (an immutable `kg_events` collection replayed into derived views) — neither is named by the other sources. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- The MCP source additionally exposes memory to an orchestrator only through MCP tools (knowledge-graph search/write) and "prompts," never a direct database query layer. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- `decode` anchors memory files to the **launch directory**, distinct from the sandboxed tool-execution workspace, so `--resume` still finds `MEMORY.md` and session logs after a Docker/Modal sandbox that hosted the actual work has been destroyed. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- `AGENTS.md` and `MEMORY.md` are populated by different mechanisms: `AGENTS.md` is hand-written and length-guarded (~300-line target, ~600-line hard guardrail); `MEMORY.md` is auto-written, one summary sentence per session, capped at 200 lines / 25,000 bytes with oldest content dropped first when it overflows. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- The concrete failure motivating `AGENTS.md` is retyping the same datetime/type-hint corrections every session — a persistence problem the article frames as solvable by a hand-written file, not by a larger context window or a smarter model. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- The lesson-1 article states the absence of a memory database or codebase index in `decode` is a deliberate design position, not an omission still to be filled in — "Just-in-time reads beat a stale heavy index" — the wiki's only explicit argument against the infrastructure the MongoDB and MCP sources build. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **Vector search**: the article sources use embedding-based retrieval as memory's semantic-recall mechanism; `decode` and its own course articles have none, relying on the model reading memory files directly. [[wiki/concepts/vector-search]]
- **GraphRAG**: MongoDB's `$graphLookup` traversal is framed as an alternative to a dedicated graph database for GraphRAG-style retrieval — a capability the file-based memory camp doesn't attempt. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/graphrag]]
- **Event sourcing**: MongoDB's knowledge-graph versioning is event sourcing (`kg_events` + derived views); no other source discusses a comparable mechanism. [[wiki/concepts/event-sourcing]]
- **Knowledge graph**: the entity/relationship graph is the memory component both article sources implement, via different mechanisms; `decode` has none. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/knowledge-graph]]
- **MCP**: the MCP source exposes agent memory to an orchestrator exclusively through MCP tools and prompts, making the memory store a component behind a server rather than a database queried directly. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/mcp]]
- **Orchestrator placement**: the MCP source treats "where memory-driving prompts are interpreted" as an open question sitting on top of the memory layer it describes. [[wiki/concepts/orchestrator-placement]]
- **Context compaction**: `decode`'s architecture page ties memory to the same instructions block that compaction protects; the context-engineering article sharpens this into a mechanism — `/clear` wipes conversation history only *after* writing back to `MEMORY.md`, so memory is the deliberate residue that survives the one compaction event that destroys everything else. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/context-compaction]]
- **Agent harness**: across all three `decode`-project sources, memory is one of the harness's prompt-assembly subsystems alongside skills and agents, not a standalone service — a structural claim the article sources can't make since neither describes a harness. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]

> Synthesis: The two independent article sources (MongoDB, MCP) corroborate each other on a vector layer plus a knowledge-graph layer as the substance of agent memory. The `decode`-project cluster now numbers three sources against those two, but that is a fact about one author's output across one course and one codebase, not field-wide agreement — see Tensions. The substantive spectrum is unchanged and now sharper on one end: "memory is a database problem" (MongoDB) through "memory is a pipeline's output" (MCP) to "memory is deliberately not a database" (decode — no longer just built that way, but now argued for in print).

## Tensions

The MongoDB and MCP sources agree that agent memory requires built infrastructure — a vector index and a knowledge graph, at minimum — to be useful beyond a single turn. `decode`'s memory subsystem contradicts that premise in practice: two plain-text files merged into the system prompt, no retrieval mechanism beyond the model reading them, no persistence mechanism beyond the filesystem. This isn't an implementation detail but a disagreement about what class of problem "agent memory" is — infrastructure to provision (MongoDB, MCP) vs. content to write and cap (decode). The wiki has no basis to call one framing more representative; they may simply target different problems — long-horizon, multi-user recall for the MongoDB/MCP use cases, versus single-operator session continuity for a coding agent. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/mongodb-for-an-ai-agent-unified-memory]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

The two Substack articles sharpen this rather than settle it, and come with a corroboration warning attached. Both are written by the same author as the `decode` repository, describing the same codebase from the same course — so the file-based side of the tension above is **one voice appearing three times**, not three independent witnesses converging on a conclusion. The wiki's ≥2-source threshold is met here by citation count, not by independence, and should be read that way. What the articles add is not new evidence but an explicit argument the repo's code only implied: the lesson-1 article states that omitting a memory database or index is a deliberate design position — "Just-in-time reads beat a stale heavy index" — turning a design choice the repo merely shows into a claimed design principle. Neither MongoDB nor the MCP source argues against file-based memory; they simply build something else. The tension therefore remains open, with the case for one side now more articulate but no more independently attested than before. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
