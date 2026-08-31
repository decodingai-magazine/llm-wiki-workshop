---
type: concept
title: Agent Memory
description: The persistent layer that lets an agent reuse context across a session or across interactions — framed across sources either as a queryable knowledge graph reached through MCP tools, or as flat markdown files loaded wholesale into the system prompt at session start.
aliases: []
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/vector-search]]"
  - "[[wiki/concepts/event-sourcing]]"
  - "[[wiki/concepts/orchestration]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/compaction]]"
  - "[[wiki/concepts/context-engineering]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:15:00Z
source_count: 7
---

# Agent Memory

> Multiple framings — see Definition

## Definition

Three sources treat agent memory as a knowledge graph reached through an MCP
server, scoped differently: [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
frames it as four orthogonal capabilities (operational, vector, graph, event
log) unifiable in one MongoDB cluster; [[wiki/sources/agentic-graphrag-via-mcp-servers]]
narrows that to a concrete "digital twin" — a five-stage extraction pipeline
into one MongoDB collection, retrieved through three query strategies; and
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] describes a
simpler linear pipeline that splits memory into episodic writes (what
happened) and semantic writes (durable preferences), both automatic during
conversation.

The Decode coding-agent course defines memory differently: not a queried
graph but two flat markdown files loaded wholesale into the system prompt at
session start — `AGENTS.md` (hand-written, under 300 lines) and
`.decode/MEMORY.md` (auto-extracted, one LLM call per session-end, capped at
200 lines / 25,000 bytes). [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]],
[[wiki/sources/article-context-engineering-for-coding-agents]]
The Decode codebase confirms this in code, not just prose: `src/decode/memory/`
discovers and assembles both files (root-most directory → cwd-most) into the
per-turn system-prompt block, feeding the model as instructions rather than
through any callable tool.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
An earlier lesson of the same course, [[wiki/sources/article-the-coding-agent-loop]],
only names memory as a harness module and defers it as later-lesson
territory.

## Key claims

- A knowledge graph — typed nodes and edges extracted from ingested documents
  — is the recurring representation across the three MCP-based sources,
  though extraction pipelines differ (a fixed 5-stage LLM-extraction pipeline
  vs. a simpler ingest-normalize-extract-embed one). [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- That memory is reached through an MCP server, not queried directly: two
  core tools ([[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]])
  or six tools kept deliberately "logic-free" so the same code path serves an
  MCP call or a batch run ([[wiki/sources/agentic-graphrag-via-mcp-servers]]).
- Unified single-database memory has explicit limits: `$graphLookup` stays
  sub-second at 2–3 hops but loses to native graph databases past 5 hops, and
  the same trade-off applies to vector scale past roughly 100M–1B vectors.
  [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- Decode's memory is prompt-embedded, not tool-mediated: assembled once at
  session start, with `.decode/MEMORY.md` periodically rewritten in place by
  "Memory Compression," and a write-back preceding `/clear`.
  [[wiki/sources/article-context-engineering-for-coding-agents]]
- The same course lists Memory alongside Sandbox, Permissions, Skills and an
  LSP server as one of six discrete harness modules — infrastructure the
  harness owns, not a service the agent calls out to.
  [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- The codebase sharpens the "session start" framing above: instructions
  (base prompt + active persona + `assemble_memory()` + skills catalog) are
  in fact rebuilt fresh on *every* turn as one system-prompt block, not
  cached once per session — because strict OpenAI-compatible servers reject
  more than one `system` message per request.
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Tensions

Two incompatible architectures share the name "agent memory" here.
[[wiki/sources/agentic-graphrag-via-mcp-servers]],
[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]] and
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] treat it as
external to the harness — a graph queried on demand via MCP tools.
[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
and [[wiki/sources/article-context-engineering-for-coding-agents]] treat it as
harness-owned flat files loaded once at session start, no runtime query tool
or graph involved; the latter names an MCP client as something it has
"deliberately skipped" so far. Neither cluster reconciles the two — likely a
scale question (personal knowledge base vs. single coding session) that no
source states directly.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
lands squarely on the file-based side and hardens it: the architecture
diagram routes memory into the agent as `Mem -.instructions.-> Core`, a
dotted line straight into the system prompt, structurally separate from the
`Tools` path that mutating calls (including any future MCP tool) would run
through — the tension is visible in the codebase's own module boundaries,
not just asserted in prose.

## Relationships

- **GraphRAG**: retrieval technique run over memory once it is a knowledge
  graph. [[wiki/concepts/graphrag]]
- **MCP**: delivery mechanism for the graph-based model; absent from
  Decode's file-based model entirely. [[wiki/concepts/mcp]]
- **Vector search**: semantic-retrieval layer alongside graph traversal in a
  unified-memory design. [[wiki/concepts/vector-search]]
- **Event sourcing**: [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
  versions knowledge-graph state as an immutable append-only log.
  [[wiki/concepts/event-sourcing]]
- **Agent Harness**: memory as one of six harness-owned modules — the
  file-based counterpart to MCP-exposed memory; the repo shows this module
  as `src/decode/memory/`, sitting alongside `permissions/`, `sandbox/` and
  `skills/` as harness code, not a called-out service.
  [[wiki/concepts/agent-harness]],
  [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **Compaction**: a memory write-back to `.decode/MEMORY.md` precedes
  `/clear` wiping the context window. [[wiki/concepts/compaction]]
- **Orchestration**: [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
  takes memory's MCP-tool surface as given, and asks instead whether the
  orchestrator calling it belongs on the server or the client.
  [[wiki/concepts/orchestration]]

> Synthesis: Six of seven sources trace to one practitioner — explicit for
> the three Decode-course articles and the Decode repo itself (Paul
> Iusztin's own project), previously inferred for
> [[wiki/sources/agentic-graphrag-via-mcp-servers]] and
> [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] — so
> their agreement still reads as one voice across time, not independent
> confirmation. The repo page is a different *kind* of evidence within that
> one voice, though: it is the code the two articles describe, not a fourth
> retelling of it, so it verifies the file-based claim rather than merely
> repeating it. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
> remains the sole architecturally independent, vendor-framed source, the
> only one to name scale/hop-depth limits, and notably absent from the
> file-vs-graph tension since its graph is queried, not prompt-embedded.
