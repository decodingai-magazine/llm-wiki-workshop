# MCP Servers for Continual Learning via GraphRAG

How to model your search/write tools for agentic GraphRAG using FastMCP. Especially interesting on how to implement natural language to MongoDB queries tools and tools to dynamically write to the unified memory using different input types such as files, URIs or even the current conversation. 

### Post

[link](https://www.linkedin.com/feed/update/urn:li:share:7446885628320911360/)

---

I’m building a GraphRAG MCP server for my personal assistant.

Here's what surprised me:

Building the knowledge graph was straightforward...

Designing how the agent interacts with that memory was the hard part.

The architecture is simple at a high level:

- Ingest data into a unified memory
- Extract entities + relationships into a graph
- Index for hybrid and graph retrieval
- Expose everything through an MCP server
- Connect it to a harness like Claude Code or OpenCode

But MCP tool design is where things get tricky...

The goal is to let...

- The agent query memory using natural language (while the MCP server translates it into [**MongoDB](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)** queries)
- The agent write to memory as naturally as possible

But if you expose raw database operations, agents struggle.

So I designed the server around how agents actually search and write:

𝟭/ 𝗦𝗲𝗮𝗿𝗰𝗵 𝘁𝗼𝗼𝗹𝘀

- nl_query_memory → LLM maps natural language queries to MongoDB hybrid search + graph queries
- query_memory → structured queries as a fallback when NL fails
- deep_search_memory → progressive disclosure over large results (50+ docs), storing intermediate state (e.g. YAML index) for step-by-step exploration

𝟮/ 𝗪𝗿𝗶𝘁𝗲 𝘁𝗼𝗼𝗹𝘀

- ingest_url
- ingest_file
- ingest_conversation → auto-triggered via a hook every ~10 conversation turns

The goal is to give the agent a set of high-leverage primitives that it can dynamically compose, like LEGOs within SKILLs.

This is why I like building the MCP layer with [**Prefect**](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)’s [**FastMCP**](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#).

It keeps the server thin, so the same Python modules power both:

- Batch ingestion pipelines orchestrated with [**Prefect**](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)
- Real-time memory access via [**FastMCP**](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#), with built-in durability from [**Prefect**](https://platform.authoredup.com/calendar?month=-2&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

(which is critical for production orchestration)

Then you hook it to the harness:

- Claude Code / OpenCode → skills + hooks on top of MCP

If you’re building agentic GraphRAG systems, this is the pattern I’d recommend:

Graph for memory.

FastMCP for access.

Harness for behavior.

P.S. What’s the biggest bottleneck in your MCP servers right now?

![[assets/mcp-servers-for-continual-learning-via-g-image.png]]

---

## Agentic GraphRAG Tool Design — Deepdive

How this repo models **search/write tools for agentic GraphRAG using FastMCP**, with particular focus on the natural-language-to-MongoDB query tool and the multi-input ingestion tools (URLs, files, conversations).

All code references are to files under `src/twin/`.

---

### Executive Summary

#### The Problem

LLMs forget. Every new conversation starts from scratch. Classic RAG — chunk a document, embed it, do cosine-similarity search — retrieves "things that look similar to your query," but it can't retrieve "things that are *connected* to your query." A digital twin needs both: the chunk where Alice said X, **and** the tasks Alice is working on, the people Alice collaborates with, the episodes Alice lived through that inform her current thinking.

Vector search alone flattens that graph structure into a list. You lose relationships, provenance, and the ability to walk from "the person I was talking to" to "what they owe me."

#### The Solution

An **MCP server that exposes a GraphRAG memory layer** to any MCP-compatible agent (Claude, Cursor, Codex, custom harnesses). The memory is a knowledge graph of typed entities — people, tasks, episodes, preferences, documents, chunks — connected by typed edges (`TODO`, `EXPERIENCED`, `HAS`, `MENTIONS`, `RELATED_TO`). Agents read and write through **six tools**: three to ingest knowledge from different sources, three to retrieve it at different granularities.

The payoff: the agent can reach into a persistent, structured memory during any conversation — *query it*, *walk the graph*, *add new knowledge* — without the user copy-pasting context and without the agent re-discovering everything from scratch.

#### High-Level Architecture

```
  Agent (Claude / Cursor / ...)
        │ MCP protocol
        ▼
  FastMCP server  ──►  6 tools  (3 ingest · 3 query)
        │
        ▼
  Unified Memory (MongoDB):
    • documents          — raw source material
    • knowledge_graph    — nodes + edges in one collection,
                           text + vector indexes, upsert-idempotent
        │
        ▼
  Prefect durability layer for write paths
  (retries, per-document isolation, resumable batches)
```

One FastMCP server. One MongoDB collection for the graph. One LLM for extraction. One embedding model for semantic search. Everything initialized once at startup via a lifespan hook and shared across every tool call.

#### The Three Ingest Tools — Three Transport Realities

- **`ingest_url`** — the common case. Paste a Substack article, arXiv paper, blog post — the server dispatches to a source-specific pipeline that knows how to parse it.
- **`ingest_file`** — local-first. Ingest `.md`, `.txt`, `.html` from disk when the knowledge already lives on your machine.
- **`ingest_conversation`** — continual learning. Capture the **current conversation** back into the graph so next week's chat knows what today's decided.

All three funnel into the same downstream extraction pipeline. The difference is just *where the content comes from*.

#### The Three Query Tools — Three Retrieval Regimes

- **`query_memory`** — natural language → MongoDB aggregation pipeline. The **default**. The agent asks in English ("top 5 people with the most open tasks") and an LLM emits a validated aggregation pipeline, with a self-correcting retry loop if the query fails.
- **`search_memory`** — hybrid semantic + text search (RRF fusion) plus k-hop graph expansion. The **deterministic fallback** — no LLM in the critical path, always returns something.
- **`deep_search_memory`** — broad exploration with progressive disclosure. Runs a wide search, writes every result to disk as individual markdown files, returns only a lightweight YAML index. The agent reads files on demand instead of flooding its context with 100+ chunks.

#### The Memory Layer — One Collection, Typed Graph

- **Ontology-first**: node and edge types are Pydantic + StrEnum definitions. They drive the LLM extraction prompt *and* the NL-query prompt — one source of truth.
- **Single-collection design**: nodes have `_id = "type:name"`, edges have `_id = "source|edge_type|target"`. Both live in `knowledge_graph`. One place to search, one place to write, trivially idempotent.
- **Three indexes**: text (`$text` on name/content/aliases), vector (`$vectorSearch` cosine on embeddings), compound graph-traversal indexes.
- **Upsert-idempotent writes**: re-ingesting the same document densifies the graph instead of duplicating it. Aliases and sources accumulate; fuzzy matching collapses variants like "alicia"/"alice" into one canonical node.

#### Why FastMCP — And Why It Pairs So Well with Prefect

MCP is a protocol — tools, resources, prompts, transports — and if you implement a server against the official low-level SDK you end up writing a lot of the same boilerplate the REST-API world left behind a decade ago: hand-crafted JSON schemas, `list_tools()` / `call_tool()` dispatch tables, transport bootstrapping, and a manually-managed singleton for shared state. FastMCP collapses all of that into **three decorators**: `@lifespan`, `@mcp.tool`, and an implicit `Context` parameter that FastMCP injects and omits from the agent-facing schema.

The result: every tool in this project is 10–15 lines. The six-tool MCP surface — three ingest, three query, plus lifespan — fits in a single 300-line module, with no separately-maintained schema, description, or dispatch code. Type hints *are* the schema. Docstrings *are* the description. The function body *is* the implementation. Nothing to keep in sync.

What makes this especially powerful for an *agentic* system:

- **Tool discoverability stays truthful.** The agent reads the tool description directly from the docstring, so when you change behavior you can't forget to update the docs — they come from the same source of truth.
- **Dependency injection is built-in.** The `@lifespan` hook initializes the Mongo client, LLM, and embedding model *once* at server startup and injects them into every tool call via `Context`. No per-request reconnects, no global singletons, no accidental leaks of expensive clients.
- **`instructions=` as a first-class routing layer.** FastMCP exposes the server-level `instructions=` field as a constructor argument, which ships to the agent in the `initialize` response. That's the string that tells the calling LLM *when* to use `query_memory` vs. `search_memory` vs. `deep_search_memory` — the routing rulebook lives next to the code it routes.
- **Six transports, one `mcp.run()`.** stdio for Claude Desktop, HTTP/SSE for remote deployments — one line to switch. The low-level SDK forces you to wire each transport yourself.

**And here's the detail that matters for this specific pairing: FastMCP is built by Prefect.**

The same team that builds Prefect (the orchestrator this project uses for durability) also builds FastMCP. That's not trivia — it's why the two frameworks feel like they belong in the same codebase:

- **Shared design philosophy.** Both favor decorators over configuration, type hints over hand-written schemas, async-first everything, and Pydantic for validation. Switching context between `@flow`/`@task` and `@mcp.tool` costs nothing mentally — it's the *same* decorator-plus-async-function pattern applied to two different concerns.
- **Shared Python idioms.** Both use lifespans/context managers for setup-teardown, both inject a `Context` object for cross-cutting concerns (logging, cancellation), both lean on Pydantic v2. A developer productive in one is productive in the other within a day.
- **Aligned roadmaps.** As MCP spec features land (structured output, progress tokens, elicitation, sampling), FastMCP tracks them — and Prefect's involvement means the feature set is shaped by a team that deeply understands long-running, side-effectful workflow execution (exactly the use case inside MCP tool bodies).
- **One ecosystem, two layers.** FastMCP for the protocol surface, Prefect for the execution substrate underneath. Since both come from the same team, the ergonomic "shape" matches — you don't feel the seam where one framework ends and the other begins.

This is a rare "stars align" moment in the Python ecosystem: the orchestrator you'd want for durability *and* the MCP framework you'd want for ergonomics are built by the same people, for the same style of workflow. You get a coherent developer experience across both layers without hacking an adapter between mismatched abstractions.

#### Durability with Prefect — The Other Half of the Server

FastMCP is a great framework for the **protocol surface** — it turns Python functions into MCP tools with auto-generated schemas, lifespan-injected dependencies, and transport-agnostic serving. What it deliberately does *not* do is make your tool *implementations* resilient. That's not its job, and conflating the two is how MCP servers become flaky.

The work that happens *inside* an ingest tool — fetch a URL, parse HTML, call an LLM 12 times to extract entities from 12 chunks, upsert into Mongo, embed the new nodes — is exactly the kind of multi-step, side-effectful, rate-limited, network-dependent workflow that orchestrators were built for. **That's where Prefect comes in.**

Prefect is used **asymmetrically on purpose**:

- ✅ **Write paths are Prefect-wrapped.** Every ingestion tool (`ingest_url`, `ingest_file`, `ingest_conversation`) dispatches to a `@flow` made of `@task`s with retries, delays, and per-task isolation. A flaky HTTP 503 from a source site or a Gemini 429 no longer crashes the agent's turn — Prefect absorbs it and retries server-side.
- ✅ **Backlog and batch work is Prefect-orchestrated.** Full memory rebuilds (`memory-extraction-etl`, `memory-indexing-etl`, `ingest-all-data-etl`) are deployments that can be triggered from the CLI, a cron schedule, or a webhook. If a batch of 1,000 documents crashes at document 450, you resume from there — you don't re-pay the LLM/embedding cost for the 449 already done.
- ❌ **Read paths (query tools) are *not* Prefect-wrapped.** Queries are cheap, read-only, idempotent, and the agent is already in its own retry loop. Wrapping them in Prefect would add latency for zero durability gain — a deliberate choice, not an oversight.

**Why you need an orchestrator in an MCP server specifically:**

1. **Agent turns are synchronous and expensive.** When the agent calls `ingest_url`, the user is waiting. A transient network failure that's invisible to Prefect (retried and recovered in ~10s) becomes a visible error to the user if you don't have an orchestrator underneath.
2. **Agents don't retry well.** An agent that sees "HTTP 503" might re-call the tool — or might not — or might move on and forget. Durability at the infrastructure layer beats durability at the reasoning layer every time.
3. **LLM extraction is the expensive step.** Extracting a knowledge graph from a single 10-page article makes ~20+ LLM calls. Halfway through, your provider rate-limits you. Without per-task isolation, that document's extraction is lost *and* the `Document` row still exists — a zombie entry the KG doesn't know about. With Prefect, the failed task retries or is visibly marked failed and re-runnable.
4. **Observability in a multi-entry-point system.** The *same* `ingest_substack_article` flow is called from three places: the MCP tool, a cron-scheduled batch refresh, and manual CLI runs. Prefect's UI gives you one pane of glass showing which runs happened, which failed, which retried — regardless of who triggered them.

**Why this pairing is especially good with FastMCP:**

FastMCP keeps the MCP tool definitions minimal — typically 10–15 lines each. That's only possible because the *actual work* lives behind a clean call into a Prefect flow. If you had to embed retry logic, backoff, observability, and error handling inside each `@mcp.tool` function, you'd lose the entire ergonomic advantage of the framework.

```
  FastMCP  ─►  declarative protocol surface
               (tools, schemas, lifespan DI, transport)

  Prefect  ─►  durable execution substrate
               (retries, isolation, resumability, scheduling, UI)

  Division of concerns:
    FastMCP handles WHAT the agent can do.
    Prefect handles HOW RELIABLY it actually gets done.
```

One concrete win: the *same* Prefect flow (`ingest_substack_article`) is reused by the MCP `ingest_url` tool *and* the scheduled `ingest-all-data-etl` batch job. Write the flow once, get both an agent-facing entry point and a cron-schedulable batch job — because FastMCP and Prefect each own a different axis (protocol vs. execution) and don't fight each other.

**Rule of thumb this repo follows:** *Prefect-wrap anything that writes or anything that costs money if it crashes halfway. Everything else stays direct.* That keeps query tools snappy, write tools durable, and the MCP server itself a thin translation layer between the two.

#### How It All Works — End-to-End Flow

The numbered flow below traces one full cycle: ingest a URL, extract knowledge, then query it back later.

**Ingest path:**

1. The agent calls `ingest_url("https://some-substack-post/...")`.
2. FastMCP routes the call to the tool; the lifespan-injected dependencies (Mongo client, LLM, embedding model) are already warm.
3. A **Prefect-backed ETL** dispatches the URL to a source-specific pipeline (Substack, arXiv, etc.) with built-in retries for network failures.
4. The fetched content is persisted as a `Document` (unique `source_uri` → dedup; re-ingest is a no-op).
5. The extraction pipeline **chunks** the Document (tiktoken, 512-token windows with overlap).
6. Each chunk goes to an **LLM** which extracts typed entities (people, tasks, episodes, preferences) and their relationships, per the ontology.
7. **Structural edges** are added deterministically: `DOCUMENT`, `CHUNK`, `PART_OF`, `NEXT`, `MENTIONS`, `REFERENCED`.
8. **Normalization** merges duplicates: in-memory fuzzy matching collapses "alicia"/"alice", then cross-document lookup finds existing nodes in Mongo so the new extraction reuses existing `_id`s.
9. Everything is **upserted** into `knowledge_graph` (aggregation-pipeline `UpdateOne` merges properties, unions aliases and sources, caps array growth).
10. New nodes get **embeddings** (default: `sentence-transformers` `all-MiniLM-L6-v2` at 384-d; pluggable providers include Gemini, Voyage, and Modal-served vLLM) written back incrementally — only nodes with empty vectors, so re-runs don't re-pay API cost.

**Query path (some time later):**

11. The agent picks a tool based on the question shape (structured → `query_memory`, fuzzy → `search_memory`, exploratory → `deep_search_memory`).
12. **`query_memory`**: the agent's English question goes to an LLM, which emits a MongoDB aggregation pipeline. A validator enforces allow-listed stages, rewrites unsafe stages, injects a `$limit`, and swaps `"__EMBED__"` placeholders with real vectors. On failure, the validation error is fed back to the LLM for a self-correcting retry.
13. **`search_memory`**: two parallel searches (vector + `$text`) are fused via Reciprocal Rank Fusion to pick seed nodes, then a bidirectional `$graphLookup` expands the graph `max_hops` deep.
14. **`deep_search_memory`**: same hybrid engine at higher `top_k`/`max_hops`; results are written to `.memory/{session_id}/*.md` and only a YAML index returns to the agent. The agent reads individual files on demand.
15. The agent gets back a JSON payload (or a YAML index) of nodes + edges, already filtered and shaped, and continues reasoning — now grounded in the twin's persistent memory.

#### End-to-End Diagram (Numbered Flow)

```
                                           WRITE PATH                                              READ PATH
                                         ───────────────                                         ───────────────

     user → agent                        (1) agent calls ingest_* tool            (11) agent picks a query tool
         │                                       │                                       │
         │                                       ▼                                       ▼
         │                            ┌──────────────────────┐             ┌──────────────────────────┐
         │                            │ (2) FastMCP routes   │             │  query_memory  (default) │ (12)
         │                            │     tool call        │             │   NL → MongoDB pipeline  │
         │                            │  lifespan injects    │             │   ↳ validator + retry    │
         │                            │  {client, llm,       │             │                          │
         │                            │   embedding_model}   │             │  search_memory (fallback)│ (13)
         │                            └──────────┬───────────┘             │   RRF fuse + graphLookup │
         │                                       │                         │                          │
         │                                       ▼                         │  deep_search_memory      │ (14)
         │                       ┌───────────────┴────────────────┐        │   disk write + YAML idx  │
         │                       │ (3) Prefect ETL (retries,      │        └────────────┬─────────────┘
         │                       │     per-doc isolation)         │                     │
         │                       │ ─ fetch URL / read file / hash │                     │
         │                       │   conversation text            │                     │
         │                       └────────────────┬───────────────┘                     │
         │                                        ▼                                     │
         │                           ┌───────────────────────────┐                      │
         │                           │ (4) Document persisted    │                      │
         │                           │     (source_uri → dedup)  │                      │
         │                           └───────────────┬───────────┘                      │
         │                                           ▼                                  │
         │       ┌──────────────── extraction + indexing pipeline ───────────────┐      │
         │       │  (5) chunk_document (tiktoken, 512/64 overlap)                │      │
         │       │  (6) LLM per-chunk extraction → typed nodes + edges           │      │
         │       │  (7) build structural entries (DOCUMENT, CHUNK, PART_OF,      │      │
         │       │      NEXT, MENTIONS, REFERENCED)                              │      │
         │       │  (8) normalize_nodes (fuzzy + cross-document alias resolve)   │      │
         │       │  (9) upsert to knowledge_graph (merge props, union aliases,   │      │
         │       │      accumulate sources — all idempotent)                     │      │
         │       │ (10) embed_nodes (only empty-vector nodes — incremental)      │      │
         │       └───────────────────────────────┬───────────────────────────────┘      │
         │                                       ▼                                      │
         │       ┌────────────────────────────────────────────────────────────┐         │
         │       │              MongoDB — Unified Memory                      │◄────────┘
         │       │                                                            │
         │       │  documents            (Beanie, unique source_uri)          │
         │       │  knowledge_graph      (single collection)                  │
         │       │    ├─ NODES  _id = "type:name"                             │
         │       │    ├─ EDGES  _id = "source|edge_type|target"               │
         │       │    ├─ text_index                                           │
         │       │    └─ vector_index (cosine, with kind/type filters)        │
         │       └────────────────────────────────────────────────────────────┘
         │                                       │
         │                                       ▼
         └──────────────── (15) agent receives typed JSON / YAML index,
                                continues reasoning with grounded memory
```

The rest of this document zooms into each numbered step with code references, design rationale, and the trade-offs behind each decision.

---

### 0. System at a Glance

Bird's-eye view of the MCP server, the six tools it exposes, and what each tool touches inside the memory system.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Agent (Claude, etc.)                               │
│  picks a tool based on mcp.instructions="Use query_memory for flexible..."  │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ MCP protocol (stdio / http)
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FastMCP("Twin Memory")  — src/twin/mcp/server.py         │
│                                                                             │
│   ┌──── @lifespan app_lifespan ─────────────────────────────────────────┐   │
│   │  init_mongodb() ─► client      get_llm() ─► llm                     │   │
│   │  ensure_indexes()              get_embedding_model() ─► embed_model │   │
│   │  yields lifespan_context = {client, database, llm, embedding_model} │   │
│   └──────────────────────────────────────────────────────────────────┬──┘   │
│                                                                      │      │
│   Tools (registered via @mcp.tool in src/twin/mcp/tools.py):         │      │
│                                                                      ▼      │
│   ┌─────────── READ ────────────┐   ┌─────────── WRITE ──────────────────┐  │
│   │  query_memory  (NL→pipe)    │   │  ingest_url          (URL)         │  │
│   │  search_memory (hybrid RRF) │   │  ingest_file         (path)        │  │
│   │  deep_search_memory (disk)  │   │  ingest_conversation (text)        │  │
│   └─────────────┬───────────────┘   └──────────────┬─────────────────────┘  │
└─────────────────┼──────────────────────────────────┼────────────────────────┘
                  │                                  │
                  ▼                                  ▼
┌────────────────────────────────┐   ┌───────────────────────────────────────┐
│     Unified Memory (MongoDB)   │   │   Data Layer (Prefect flows)          │
│                                │   │                                       │
│  documents            (Beanie) │◄──┤  substack_article / file /            │
│  knowledge_graph  (single col) │   │  conversation   pipelines             │
│    • nodes _id="type:name"     │   │                                       │
│    • edges _id="src|type|tgt"  │   │  all emit → Document rows             │
│    • text_index, vector_index  │   └──────────────┬────────────────────────┘
│                                │                  │
└────────────┬───────────────────┘                  ▼
             │                   ┌────────────────────────────────────────┐
             │                   │ Memory Pipeline (post-ingest)          │
             │                   │   chunk → extract → structural         │
             │                   │   → normalize → upsert → embed         │
             └───────────────────┤  (src/twin/memory/{extraction,         │
                                 │   indexing})                           │
                                 └────────────────────────────────────────┘
```

---

### 1. FastMCP Server Skeleton (`src/twin/mcp/server.py`)

A single `FastMCP` instance with a **lifespan** that initializes heavy dependencies once and injects them into every tool call — avoiding per-call DB connects and model loads.

```python
@lifespan
async def app_lifespan(server: FastMCP) -> AsyncGenerator[dict, None]:
    client = await init_mongodb(...)
    llm = get_llm()
    embedding_model = get_embedding_model()
    await ensure_indexes(client, database)     # idempotent text + vector indexes
    yield {"client": client, "database": database, "llm": llm, "embedding_model": embedding_model}
    await client.close()

mcp = FastMCP("Twin Memory", instructions=..., lifespan=app_lifespan)
import twin.mcp.tools  # side-effect: registers @mcp.tool decorators
```

Key moves:

- **`instructions=` is not filler.** It is the routing manual the calling agent reads to pick between `query_memory` / `search_memory` / `deep_search_memory` / `ingest_*`. It explicitly names the "fallback" semantics (semantic search as a reliable fallback when NL→pipeline fails).
- **Separate registration file** (`tools.py` imported for its side effect) keeps server bootstrap decoupled from the tool surface. You can grow the toolset without touching server init.
- **Lifespan context is a plain dict**, accessed inside tools via `ctx.lifespan_context["client"]`. Tools are thin — no module-level globals, no per-request re-init.

---

### 2. Three Search Tools (`src/twin/mcp/tools.py`)

The project deliberately exposes **three complementary search tools** at different levels of abstraction, so the agent can self-select per query shape:

| Tool | Backend | Use-case |
|---|---|---|
| `query_memory` | NL → MongoDB aggregation (LLM-generated pipeline) | Flexible structured queries, filters, aggregations |
| `search_memory` | Hybrid RRF (vector + `$text`) + k-hop `$graphLookup` expansion | Reliable semantic fallback |
| `deep_search_memory` | Same hybrid but `top_k=50, max_hops=3` + disk write | Broad exploration without flooding context |

#### 2a. Hybrid RRF Search (`memory/query/core.py`)

Two independent pipelines fused by **Reciprocal Rank Fusion**:

```python
# Vector branch (first-stage $vectorSearch only legal as stage 0)
[{"$vectorSearch": {"index": "vector_index", "path": "embedding",
                    "queryVector": vec, "numCandidates": top_k*10,
                    "limit": top_k, "filter": {"kind": "node"}}},
 {"$addFields": {"_search_score": {"$meta": "vectorSearchScore"}}}]

# Text branch (MongoDB $text on name/content/aliases)
[{"$match": {"kind": "node", "$text": {"$search": query}}},
 {"$addFields": {"_search_score": {"$meta": "textScore"}}}, ...]

# RRF: score = Σ 1/(k + rank) across branches; k=60
```

The seed nodes' `_id`s then feed a **bidirectional `$graphLookup`** (outgoing by `source_node_id`, incoming by `target_node_id`, `$setUnion`'d) to expand k hops. Nodes from all edge endpoints are re-hydrated in one `$in` query. Note: `$graphLookup.maxDepth` is 0-indexed, so the code passes `depth = max_hops - 1`; when `max_hops == 0` the traversal is skipped entirely and only seed nodes are hydrated.

#### 2b. Progressive Disclosure via `deep_search_memory`

The cleanest pattern in the repo. Instead of returning 100 node/edge docs inline:

1. Run expanded hybrid + traversal search.
2. Write every node/edge as a standalone markdown file under `.memory/{session_id}/`.
3. Build `index.yaml` with top-level `session_id` / `query` / `created_at` / `directory` / `total_nodes` / `total_edges` counts, plus one entry per result doc: `id`, `kind`, `type`, `name`, `file`, and a one-line `context` summary.
4. **Return only the index YAML** to the agent.

The agent scans the lightweight index, then `Read`s only the files it needs. RAG results become a virtual filesystem rather than a context flood. This is implemented in `src/twin/mcp/deep_search.py`.

---

### 3. NL → MongoDB Aggregation Tool (`memory/query/nl_query.py`)

The most interesting tool. Not a query builder — it **asks an LLM to emit a MongoDB aggregation pipeline as JSON**, then validates and executes it. Four key design decisions:

#### 3a. Ontology-Derived System Prompt

`build_nl_query_system_prompt()` dynamically introspects `NodeType` / `EdgeType` / `NODE_PROPERTIES` / `EDGE_CONSTRAINTS` and emits property JSON schemas via `pydantic.model_json_schema()`. The LLM sees the full typed graph model at every call — **no drift between code and prompt**.

The prompt also documents: document shape (`_id = "type:name"` for nodes, `_id = "source|type|target"` for edges), available indexes (`text_index`, `vector_index`), and required output format (`{"pipeline": [...]}`).

#### 3b. Embedding Placeholder Pattern

The LLM cannot emit a real embedding vector, so it emits a sentinel:

```python
{"$vectorSearch": {"index": "vector_index", "path": "embedding",
                   "queryVector": "__EMBED__", "queryText": "<text>", ...}}
```

After validation, `_replace_embedding_placeholder()` walks the pipeline, pops `queryText`, embeds it, and substitutes the real vector. Keeps the LLM's job fully textual while giving the pipeline a valid vector at execution time.

#### 3c. Allow-List Validator (Safety)

```python
_ALLOWED_STAGES = frozenset({"$vectorSearch", "$match", "$project", ...,
                             "$lookup", "$graphLookup", ...})
```

`validate_pipeline()` enforces:

- Every stage must be in the allow-list — **no `$out`, `$merge`, `$where`, `$function`, `$accumulator`**.
- `$vectorSearch` must be stage 0.
- `$lookup` / `$graphLookup` `from` must equal `"knowledge_graph"`.
- Always appends a `$limit` + `$project: {embedding: 0}` if absent; clamps any existing `$limit` that exceeds the configured max.

This is the containment boundary: the LLM can only *read* the graph.

#### 3d. Self-Correcting Retry Loop

```python
for attempt in range(1 + max_retries):
    try: ... execute ...
    except (PipelineValidationError, OperationFailure) as exc:
        current_prompt = (
            f"Original query: {query}\n\n"
            f"The pipeline failed with this error: {exc}\n\n"
            f"Fix the pipeline to avoid this error."
        )
```

Validation errors and Mongo `OperationFailure` (e.g. missing fields, type mismatch) are fed back verbatim so the LLM can self-correct its own syntax — typically within one retry.

---

### 4. Write Tools: `ingest_url`, `ingest_file`, `ingest_conversation`

Three write tools, one shared post-ingest pipeline. Each follows: **normalize input → persist as `Document` → run `run_ingestion_pipeline`**.

#### 4a. Shared `Document` Abstraction (`entities/documents.py`)

```python
class SourceType(StrEnum):
    SUBSTACK = "substack"; HUGGINGFACE = "..."; LATENT = "latent"
    FILE = "file"; CONVERSATION = "conversation"

class Document(BeanieDocument):
    source_type: SourceType
    source_uri: Indexed(str, unique=True)   # the idempotency key
    title: str | None; content: str | None; date: datetime | None
    references: list[Link["Document"]]
```

Every input type collapses to a `Document` with a distinct `source_uri` scheme — the unique index on `source_uri` is the idempotency anchor.

#### 4b. URL Ingestion — **Domain Dispatch**

`data/core/ingest.py` holds a registry `(domain_substring, handler)` and also derives "custom Substack domains" from config. New sources register here:

```python
_URL_HANDLERS = [("substack.com", _ingest_substack_article)]
# Plus domains derived from app_config.sources.substack(_articles)
```

Extending to a new source (e.g. YouTube) means adding one tuple. The MCP tool itself stays identical.

#### 4c. File Ingestion — **Content Conversion + Upgrade-in-Place**

`data/file.py::load_file_document()`:

- `_SUPPORTED_EXTENSIONS = {".txt", ".md", ".html"}` — unknown extensions raise `ValueError`.
- `.html` routed through `html_to_plain_text()`.
- `source_uri = f"file://{path}"`. Collision on retry means dedup; but if an existing doc is `SourceType.LATENT` (a placeholder previously referenced by another doc), it **upgrades in place** rather than creating a new entry. Nice trick for reconciling forward references.

#### 4d. Conversation Ingestion — **Content-Hash URIs**

```python
source_uri = f"conversation://{sha256(conversation_text)[:16]}"
```

Idempotency without requiring the caller to generate an ID. Re-ingesting the same conversation text is a no-op.

#### 4e. Error Surface Through MCP

All three tools return JSON strings so the calling agent gets structured feedback:

```python
# ingest_url errors
{"error": "unsupported_url", "detail": "No pipeline registered for..."}
{"error": "http_error", "detail": "HTTP 404: ..."}
{"error": "network_error", "detail": "..."}
{"status": "already_ingested", "url": "..."}  # Not an error — idempotent hit
{"status": "ingested", "document_id": "...", "nodes_extracted": 12, ...}
```

The agent can decide to retry, fall back, or report to the user based on the status code.

---

### 5. Shared Post-Ingest Pipeline (`mcp/ingest.py`)

The three write tools converge on `run_ingestion_pipeline(document, ...)`:

```
chunk (tiktoken, cl100k_base, 512/64 overlap)
  → LLM extract per chunk (async semaphore, gathered)
  → build structural entries (DOCUMENT, CHUNK, PART_OF, NEXT, MENTIONS, REFERENCED)
  → normalize_nodes (in-memory fuzzy dedup → cross-document $text candidate lookup)
  → upsert_graph_entries (aggregation-pipeline UpdateOne: $mergeObjects, $setUnion, $slice caps)
  → embed_nodes (only nodes with empty embedding — incremental)
```

Two design moves worth calling out:

- **Aggregation-pipeline upserts.** `UpdateOne(..., [<pipeline>], upsert=True)` uses two stages: stage 1 `$mergeObjects` props + `$setUnion` sources capped at 500; stage 2 unions aliases capped at 50. This is mutate-in-place rather than overwrite — the graph densifies over repeated ingestions without losing provenance, and the `$slice` caps keep arrays bounded.
- **Cross-document normalization.** Before upsert, `normalize_nodes` queries Mongo via `$text` (broad/stemmed candidate pool) then filters locally via `SequenceMatcher` at 0.85 similarity. When a new extraction's `"alicia"` fuzzy-matches an existing `"alice"`, the existing `_id` becomes canonical and the edge endpoints are remapped so no duplicate entity ever lands.

---

### 6. Diagrams

#### 6a. Read Path — How the Three Search Tools Work

```
  agent query string
         │
         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                        query_memory (flexible)                             │
│                                                                            │
│   query ─► nl_to_pipeline(llm, query)                                      │
│              │  prompt built from ontology (NodeType, EdgeType,            │
│              │  NODE_PROPERTIES, EDGE_CONSTRAINTS) at call time            │
│              ▼                                                             │
│            pipeline: list[dict]  ◄───── retry loop (max_retries)           │
│              │                          on PipelineValidationError or     │
│              ▼                          OperationFailure, re-prompt       │
│         validate_pipeline()             with the error text                │
│              │ • allow-list stages                                         │
│              │ • $vectorSearch must be stage 0                             │
│              │ • $lookup/$graphLookup from=knowledge_graph                 │
│              │ • inject $limit + $project:{embedding:0}                    │
│              ▼                                                             │
│      _replace_embedding_placeholder()                                      │
│              │  find "queryVector": "__EMBED__", pop queryText,            │
│              │  call embedding_model.embed([queryText]), substitute       │
│              ▼                                                             │
│          collection.aggregate(pipeline, maxTimeMS=10_000)                  │
└─────────────────────────────┬──────────────────────────────────────────────┘
                              │ docs (JSON, embedding stripped)
                              ▼
                         serialize → return

┌────────────────────────────────────────────────────────────────────────────┐
│                       search_memory (hybrid RRF)                           │
│                                                                            │
│   query ──┬──► vector branch: $vectorSearch(queryVector=embed(query))      │
│           │                                                                │
│           └──► text branch:   $match {$text: {$search: query}}             │
│                      │                                                     │
│                      ▼                                                     │
│            _rrf_fuse(v_results, t_results, k=60)                           │
│               score[id] = Σ 1/(k + rank_i)                                 │
│                      │                                                     │
│                      ▼                                                     │
│            top_k seed nodes  ──►  expand_graph(seed_ids, max_hops)         │
│                                      │                                     │
│                                      ▼                                     │
│         bidirectional $graphLookup (outgoing + incoming)                   │
│         → $setUnion → dedupe edges → hydrate all touched nodes             │
└─────────────────────────────┬──────────────────────────────────────────────┘
                              │ QueryResult(nodes=[...], edges=[...])
                              ▼
                         serialize → return

┌────────────────────────────────────────────────────────────────────────────┐
│                  deep_search_memory (progressive disclosure)               │
│                                                                            │
│   Same hybrid+graphLookup as search_memory, but top_k=50, max_hops=3       │
│                              │                                             │
│                              ▼                                             │
│            write_deep_search_results(query, result, session_id)            │
│                                                                            │
│          .memory/{session_id}/                                             │
│            ├── index.yaml              ◄── returned to the agent           │
│            ├── person-alice.md                                             │
│            ├── person-alice--todo--task-write.md                           │
│            └── ...                     ◄── agent pulls on demand           │
└────────────────────────────────────────────────────────────────────────────┘
```

#### 6a-i. Ontology-Driven Prompt Construction (NL → MongoDB)

The LLM never sees hand-written field lists. Every invocation of `query_memory` rebuilds the system prompt **from the live Pydantic + Enum registries** — so adding a new node/edge type automatically teaches the LLM how to query it.

```
  src/twin/entities/knowledge_graph.py                src/twin/entities/ontology.py
  ┌──────────────────────────────┐         ┌────────────────────────────────────────┐
  │ class NodeType(StrEnum):     │         │ NODE_PROPERTIES: dict[NodeType, BaseModel] = {
  │   DOCUMENT = "document"      │────┐    │   PERSON:     PersonProperties,
  │   CHUNK    = "chunk"         │    │    │   TASK:       TaskProperties,      │
  │   PERSON   = "person"        │    │    │   EPISODE:    EpisodeProperties,   │
  │   TASK     = "task"          │    │    │   ...                              │
  │   EPISODE  = "episode"       │    │    │ }                                  │
  │   PREFERENCE = "preference"  │    │    │                                    │
  │                              │    │    │ EDGE_CONSTRAINTS: dict[EdgeType, _] = {
  │ class EdgeType(StrEnum):     │    │    │   TODO:        person  → task      │
  │   PART_OF, NEXT, MENTIONS,   │────┤    │   EXPERIENCED: person  → episode   │
  │   REFERENCED, RELATED_TO,    │    │    │   HAS:         person  → preference│
  │   TODO, EXPERIENCED, HAS     │    │    │   RELATED_TO:  person  → person    │
  └──────────────────────────────┘    │    │   MENTIONS:    document→ person    │
                                      │    │   ...                              │
                                      │    │ }                                  │
                                      │    └──────────────────┬─────────────────┘
                                      │                       │
                                      ▼                       ▼
                 build_nl_query_system_prompt()  (memory/query/nl_query.py)
                 ┌──────────────────────────────────────────────────────────────┐
                 │ for nt in NodeType:                                          │
                 │     schema = NODE_PROPERTIES[nt].model_json_schema()         │
                 │     emit: "  - {nt.value}: properties schema = {schema}"    │
                 │                                                              │
                 │ for et in EdgeType:                                          │
                 │     c = EDGE_CONSTRAINTS[et]                                 │
                 │     emit: "  - {et.value}: {c.source_type} -> {c.target}"   │
                 └────────────────────────────┬─────────────────────────────────┘
                                              │
                                              ▼
  ┌─────────────────────── System Prompt (rendered) ───────────────────────────┐
  │ You are a MongoDB aggregation pipeline generator for a knowledge graph.    │
  │                                                                            │
  │ ## Collection: `knowledge_graph`                                           │
  │ ### Node document shape                                                    │
  │   _id: "type:name"  kind: "node"  type: ...  properties: {...}             │
  │ ### Edge document shape                                                    │
  │   _id: "source|type|target"  source_node_id, target_node_id, ...           │
  │                                                                            │
  │ ## Node types and property schemas                                         │
  │   - person: properties schema = {                                          │
  │       "aliases": {"type": "array", "items": {"type": "string"}},           │
  │       "email":   {"type": ["string","null"]}                               │
  │     }                                                                      │
  │   - task:   properties schema = {"content": ..., "date": ...}              │
  │   - ...                                                                    │
  │                                                                            │
  │ ## Edge types and constraints (source_type -> target_type)                 │
  │   - todo:        person -> task (Person has a task or project)             │
  │   - experienced: person -> episode                                         │
  │   - has:         person -> preference                                      │
  │   - related_to:  person -> person                                          │
  │   - mentions:    document -> person                                        │
  │   - ...                                                                    │
  │                                                                            │
  │ ## Available indexes                                                       │
  │   text_index   → (name, properties.content, properties.aliases)            │
  │   vector_index → embedding (cosine)                                        │
  │                                                                            │
  │ ## Vector search template (use __EMBED__ placeholder)                      │
  │   {"$vectorSearch": {                                                      │
  │      "index": "vector_index", "path": "embedding",                         │
  │      "queryVector": "__EMBED__", "queryText": "<text>",                    │
  │      "numCandidates": 100, "limit": 10, "filter": {"kind": "node"}}}       │
  │                                                                            │
  │ ## Output format                                                           │
  │   {"pipeline": [<stage1>, <stage2>, ...]}                                  │
  │                                                                            │
  │ ## Safety rules                                                            │
  │   ONLY read operations. NEVER $out/$merge/$where/$function. $lookup from   │
  │   must be "knowledge_graph". Always include $limit. No embedding field.    │
  └────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
  user: "What tasks does alice have, and anything semantically related?"
                                              │
                                              ▼
  LLM emits strictly-typed JSON matching the ontology:

  {"pipeline": [
    {"$vectorSearch": {
       "index": "vector_index", "path": "embedding",
       "queryVector": "__EMBED__",
       "queryText": "alice tasks and related work",
       "numCandidates": 100, "limit": 10,
       "filter": {"kind": "node", "type": "task"}}},       ← type from NodeType
    {"$lookup": {
       "from": "knowledge_graph",                          ← enforced collection
       "localField": "_id",
       "foreignField": "target_node_id",
       "as": "incoming_edges",
       "pipeline": [{"$match": {"type": "todo",            ← edge type from EdgeType
                                "source_node_id": "person:alice"}}]}},
    {"$match": {"incoming_edges": {"$ne": []}}},
    {"$limit": 10}
  ]}

  Why this works reliably:
  • Pydantic schemas exported via .model_json_schema() keep the prompt in sync
    with PersonProperties, TaskProperties, etc. — no hand-maintained docs.
  • Enum.value strings are the same literals the LLM must use in $match.
  • EDGE_CONSTRAINTS documents valid (source_type → target_type) pairs, which
    the LLM uses to pick the correct `source_node_id` / `target_node_id` side.
  • _id conventions ("type:name", "source|type|target") let the LLM join edges
    to nodes without needing a separate schema.
```

#### 6a-ii. Self-Correcting NLQ → MongoDB Loop

The LLM generates syntactically correct JSON roughly always, but **semantically** invalid pipelines happen (wrong `from`, missing field, `$vectorSearch` not first, etc.). Instead of surfacing the error, `execute_nl_query()` feeds it back into the same LLM call.

```
                 user query: "top 5 people with the most tasks"
                                     │
                                     ▼
                      current_prompt = user query
                                     │
  ┌──────────────────────────────────┴──────────────────────────────────┐
  │                                                                     │
  │   ┌─────────── attempt loop (range(1 + max_retries)) ────────────┐  │
  │   │                                                              │  │
  │   │   nl_to_pipeline(llm, current_prompt)                        │  │
  │   │       │  system = build_nl_query_system_prompt()             │  │
  │   │       │  llm.generate_json(current_prompt, system=system)    │  │
  │   │       ▼                                                      │  │
  │   │   pipeline: list[dict]                                       │  │
  │   │       │                                                      │  │
  │   │       ▼                                                      │  │
  │   │   validate_pipeline(pipeline)  ──► PipelineValidationError ──┼──┐
  │   │       │   • allow-list stages                                │  │
  │   │       │   • $vectorSearch only at stage 0                    │  │
  │   │       │   • $lookup/$graphLookup.from == knowledge_graph     │  │
  │   │       │   • inject $limit + $project:{embedding:0}           │  │
  │   │       ▼                                                      │  │
  │   │   _replace_embedding_placeholder(pipeline)                   │  │
  │   │       │  replace "__EMBED__" with embedding_model.embed(…)   │  │
  │   │       ▼                                                      │  │
  │   │   collection.aggregate(pipeline, maxTimeMS=10_000)           │  │
  │   │       │                                                      │  │
  │   │       ├──► success ─► return docs                            │  │
  │   │       │                                                      │  │
  │   │       └──► OperationFailure  (Mongo-side error)  ────────────┼──┤
  │   └──────────────────────────────────────────────────────────────┘  │
  │                                                                     │
  │                                 ▼                                   │
  │                    caught exception `exc`                           │
  │                                 │                                   │
  │                                 ▼                                   │
  │       current_prompt = (                                            │
  │         f"Original query: {query}\n\n"                              │
  │         f"The pipeline failed with this error: {exc}\n\n"           │
  │         f"Fix the pipeline to avoid this error."                    │
  │       )                                                             │
  │                                 │                                   │
  │                                 └── loop back with fresh system ────┘
  │                                     prompt + error-injected user prompt
  └─────────────────────────────────────────────────────────────────────┘
                                     │
                         all retries exhausted → raise last_error
```

**Two concrete failure → recovery examples**

Example 1 — the LLM misremembers the collection name:

```
Attempt 1 — LLM emits:
  {"pipeline": [
    {"$lookup": {"from": "kg", "localField": "_id", ...}},  ← WRONG
    {"$limit": 10}]}

validate_pipeline() raises:
  PipelineValidationError("$lookup 'from' must be 'knowledge_graph', got 'kg'")

Attempt 2 — current_prompt injected back:
  "Original query: top 5 people with the most tasks
   The pipeline failed with this error: $lookup 'from' must be
     'knowledge_graph', got 'kg'
   Fix the pipeline to avoid this error."

LLM re-emits with `"from": "knowledge_graph"` → validates → executes.
```

Example 2 — `$vectorSearch` placed in the middle of the pipeline:

```
Attempt 1 — LLM emits:
  {"pipeline": [
    {"$match": {"type": "person"}},
    {"$vectorSearch": {...}},                               ← stage 1, illegal
    {"$limit": 10}]}

validate_pipeline() raises:
  PipelineValidationError("$vectorSearch must be the first stage of the pipeline")

Attempt 2 — LLM shuffles: $vectorSearch → stage 0, $match → stage 1 (inside
the vectorSearch.filter or as a post-filter) → passes validation → executes.
```

**Why the loop is bounded to 1 retry by default**

`app_config.mcp.max_retries = 1`. Empirically a single error-fed retry fixes
>90% of pipeline failures; beyond that the LLM tends to thrash, and it's cheaper
for the agent to fall back to `search_memory` (deterministic hybrid RRF) than
to keep paying tokens. The returned exception preserves the original failure,
so the agent sees *why* NL→pipeline gave up.

#### 6b. Write Path — Three Inputs → One Document → One Pipeline

```
  URL                  local file path              conversation text
   │                         │                             │
   ▼                         ▼                             ▼
┌─────────────┐        ┌─────────────┐              ┌────────────────┐
│ ingest_url  │        │ ingest_file │              │ ingest_convers │
│ (tool)      │        │ (tool)      │              │ ation (tool)   │
└──────┬──────┘        └──────┬──────┘              └────────┬───────┘
       │                      │                              │
       ▼                      ▼                              ▼
  domain dispatch        read_file()                    sha256 hash
  _URL_HANDLERS          .txt/.md/.html                  of the text
  + substack              html→plain                         │
  custom domains              │                              │
       │                      │                              │
       ▼                      ▼                              ▼
 source_uri =           source_uri =                 source_uri =
  https://...            file:///abs/path            conversation://<16hex>
       │                      │                              │
       └──────────────────────┴──────────────────────────────┘
                              │
                              ▼
           Document (Beanie) — unique index on source_uri
              source_type ∈ {SUBSTACK, FILE, CONVERSATION, ...}
              title, content, date, references[Link[Document]]
                              │
                              │  duplicate? → return {"status": "already_ingested"}
                              │  new?       → insert, then ↓
                              ▼
   ┌────────────────────────────────────────────────────────────────────┐
   │          run_ingestion_pipeline(document, client, db,             │
   │                                 llm, embedding_model)             │
   │                                                                   │
   │   extract_and_store(llm, document_id, content, source_type, ...) │
   │   ┌────────────────────────────────────────────────────────────┐ │
   │   │ 1. chunk_document(content)     tiktoken, 512/64 overlap    │ │
   │   │ 2. for each chunk in parallel (semaphore=llm_concurrency): │ │
   │   │       extract_entities(llm, chunk)                         │ │
   │   │           system prompt = ontology JSON schema             │ │
   │   │           → ExtractionResult(nodes, edges)                 │ │
   │   │ 3. build_structural_entries():                             │ │
   │   │    DOCUMENT + CHUNKs + PART_OF + NEXT + MENTIONS           │ │
   │   │                                                            │ │
   │   │    doc─PART_OF─◄─chunk0─NEXT─►chunk1─NEXT─►chunk2 ...      │ │
   │   │      └─MENTIONS─►person_i   (for every extracted person)   │ │
   │   │      └─REFERENCED─►other_doc (from document.references)    │ │
   │   │                                                            │ │
   │   │ 4. normalize_nodes():                                      │ │
   │   │    • in-memory fuzzy dedup (SequenceMatcher ≥ 0.85)        │ │
   │   │    • cross-doc: $text candidate pool, remap edge endpoints │ │
   │   │ 5. upsert_graph_entries():                                 │ │
   │   │    UpdateOne(…, [pipeline], upsert=True)                   │ │
   │   │      stage 1: $mergeObjects props, $setUnion sources       │ │
   │   │      stage 2: $setUnion aliases, $slice cap 50             │ │
   │   └────────────────────────────────────────────────────────────┘ │
   │                                                                   │
   │   embed_nodes(client, db, embedding_model)                        │
   │     → find {embedding: {$in: [[], None]}}, batch embed, write back│
   └────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
       return {"status": "ingested", "nodes_extracted": N,
               "edges_extracted": M, "source_uri": ...}
```

#### 6c. Single-Collection Data Model (`knowledge_graph`)

Everything reachable by every tool lives here. Nodes and edges share one collection and are distinguished by the `kind` field.

```
┌────────────────────── knowledge_graph (one MongoDB collection) ────────────────────┐
│                                                                                    │
│   NODES                                     EDGES                                  │
│   ┌─────────────────────────────────┐      ┌──────────────────────────────────┐   │
│   │ _id:  "person:alice"            │      │ _id:  "person:alice|todo|        │   │
│   │ kind: "node"                    │      │        task:write report"        │   │
│   │ type: "person"                  │      │ kind: "edge"                     │   │
│   │ name: "alice"                   │      │ type: "todo"                     │   │
│   │ properties: {                   │      │ source_node_id: "person:alice"   │   │
│   │   aliases: ["alicia","a.smith"] │      │ source_type:    "person"         │   │
│   │   email: "alice@…"              │      │ target_node_id: "task:write ..." │   │
│   │ }                               │      │ target_type:    "task"           │   │
│   │ embedding: [0.12, -0.04, ...]   │      │ properties: {...}                │   │
│   │ sources: [ObjectId(doc1), ...]  │      │ sources: [ObjectId(doc1), ...]   │   │
│   │ created_at, updated_at          │      │ created_at, updated_at           │   │
│   └─────────────────────────────────┘      └──────────────────────────────────┘   │
│                                                                                    │
│   Indexes:                                                                         │
│     text_index     → (name, properties.content, properties.aliases)                │
│     vector_index   → embedding (384-d cosine, configurable) + filter(kind) + type  │
│     kind_source_node, kind_target_node, kind_embedding  (compound)                 │
└────────────────────────────────────────────────────────────────────────────────────┘

Ontology edges (enforced by EDGE_CONSTRAINTS in entities/ontology.py):

   document ──PART_OF◄── chunk ──NEXT──► chunk                   (structural)
   document ──MENTIONS──► person                                 (structural)
   document ──REFERENCED──► document                             (structural)

   person ──RELATED_TO──► person                                 (LLM-extracted)
   person ──TODO────────► task
   person ──EXPERIENCED─► episode
   person ──HAS─────────► preference
```

#### 6d. Tool Selection Heuristic (Agent POV)

How the calling agent should pick a tool, mirroring the `instructions=` string on the server:

```
  agent intent
       │
       ▼
  ┌─────────────────────────────────────────────────┐
  │ "I need the graph to answer this."              │
  └──┬──────────────────────────────────────────────┘
     │
     ├── flexible / structured  ────►  query_memory        (NL→pipeline)
     │     "top 5 people with most tasks", filters,
     │     aggregations, multi-hop $lookup
     │
     ├── semantic similarity    ────►  search_memory       (RRF + k-hop)
     │     "things related to X", free-text nearest-
     │     neighbor, reliable fallback when NL pipeline
     │     would be brittle
     │
     └── broad exploration      ────►  deep_search_memory  (disk + index)
           "everything about our Q2 migration", many
           seeds, deep traversal, read files on demand

  ┌─────────────────────────────────────────────────┐
  │ "I need to ADD something to the graph."         │
  └──┬──────────────────────────────────────────────┘
     │
     ├── URL                    ────►  ingest_url
     ├── local file (.txt/.md/.html) ─►  ingest_file
     └── current conversation text ──►  ingest_conversation
```

---

### 7. Durability with Prefect

Prefect provides retries, task-level isolation, deployment-based triggering, and UI observability for every long-running side-effectful step in the system. Crucially, **Prefect is used asymmetrically on purpose**:

| Path | Prefect-wrapped? | Why |
|---|---|---|
| `query_memory` / `search_memory` / `deep_search_memory` | **No** | Queries are cheap, read-only, idempotent, and the agent is already in a retry loop. Adding Prefect would add latency and UI noise for no durability benefit. |
| MCP ingest — data fetch stage (`ingest_substack_article`, `ingest_file`, `ingest_conversation`) | **Yes** — `@flow` with `@task(retries=...)` | Network I/O (`httpx` fetch, HTML parse), file I/O, deduplication inserts — all transient-failure-prone. |
| MCP ingest — extraction/embedding stage (`run_ingestion_pipeline`) | **No** (inline) | Runs live inside the MCP tool call so the agent gets an immediate `nodes_extracted` count back. |
| Backlog memory build-out (`memory_extraction`, `memory_indexing`, `ingest_all_data`) | **Yes** — top-level flows with sub-flows | Hours-long batch jobs across the full `documents` collection; needs isolation per document, resumability, scheduling. |

#### 7a. Where Prefect Sits in the Write Path

```
  MCP ingest_url(url)            (src/twin/mcp/tools.py)
         │
         ▼
  _ingest_url_dispatch(url)      (src/twin/data/core/ingest.py)
         │
         ▼
  ingest_substack_article(url)   ◄──── @flow  ───── Prefect-owned
         │                              │
         │    fetch_and_extract_task ◄──┤  @task(retries=2, retry_delay_seconds=5)
         │          │ httpx GET (follow_redirects=true, 30s timeout),
         │          │ BeautifulSoup parse of OG meta tags
         │          ▼
         │    load_article_document_task ◄── @task(retries=1, retry_delay_seconds=2)
         │          │ Beanie upsert with dedup
         ▼          ▼
  Document (persisted)
         │
         ▼
  run_ingestion_pipeline(document, client, db, llm, embedding_model)
         │                          (src/twin/mcp/ingest.py — NOT Prefect)
         │
         │  extract_and_store(llm, ...)  # chunk → LLM extract → normalize → upsert
         │  embed_nodes(client, db, ...) # incremental: only embedding: {$in: [[], None]}
         ▼
  return {"status": "ingested", "nodes_extracted": N, ...}

  Separate batch path (CLI / schedule — no MCP involvement):

  Prefect deployment: memory-extraction-etl
         │
         ▼
  memory_extraction(document_ids=None)   ◄── @flow
         │
         │  Document.find({content: {$ne: None}}) → list[Document]
         │
         │  for doc in docs:
         │      extract_document_task(llm, doc, client, db)
         │                ◄── @task(retries=1, retry_delay_seconds=10,
         │                          cache_policy=NO_CACHE)
         ▼
  memory-indexing-etl (separate flow) → embed_nodes_task + ensure_indexes_task
```

#### 7b. What Durability Concretely Buys You

Each failure mode below is traced to the Prefect feature that absorbs it.

**Transient network failure during ingest** — `fetch_and_extract_task(retries=2, retry_delay_seconds=5)`
- *Without Prefect:* Substack returns HTTP 503 once → `httpx.HTTPStatusError` bubbles up → `ingest_url` returns `{"error": "http_error"}` → the agent just lost that URL unless it re-invokes the tool. Three flaky URLs in a row = three failed conversations.
- *With Prefect:* The task retries twice server-side with 5s backoff. The agent sees a single success after ~10s instead of a failure.

**LLM provider rate limit during extraction** — `extract_document_task(retries=1, retry_delay_seconds=10)`
- *Without Prefect:* Gemini returns 429 on chunk 7 of 12 → the whole document's extraction is lost → the `Document` row exists but has **zero nodes in the KG** → next query returns stale/empty results, and there's no marker to say "this one needs retry."
- *With Prefect:* The task retries after 10s. If it still fails, Prefect marks that task run as Failed and the flow continues to the next document (per-task isolation). You can re-run only the failed document from the UI/CLI, not the whole batch.

**Idempotency + deduplication at the task boundary** — `cache_policy=NO_CACHE` on DB-mutating tasks
- The extraction/indexing tasks explicitly *disable* Prefect result caching (DB is the source of truth). Combined with `Document.source_uri` unique index and the KG `_id = "type:name"` upsert scheme, re-running a failed flow is safe: `extract_and_store` calls `UpdateOne(..., upsert=True)` and `embed_nodes` skips nodes with non-empty `embedding`.
- *Without Prefect + without this scheme:* You'd either skip re-ingestion entirely (losing data) or get duplicate nodes like `"person:alice"` and `"person:Alice"` polluting the graph.

**Mid-batch crash in `memory_extraction`**
- *Without Prefect:* Python process dies at document 450 of 1000 → you restart from zero, re-embedding the 449 already done. At current Gemini / Voyage / Modal API costs this is 45% wasted spend.
- *With Prefect:* The per-document `extract_document_task` runs are tracked individually. Restart the flow and inspect the UI — completed tasks show as Cached/Completed, only the failed/pending ones re-run. `embed_nodes` is already incremental (`{embedding: {$in: [[], None]}}`), so embedding cost isn't re-paid either.

**Observability — "Why are my queries returning empty?"**
- *Without Prefect:* You tail a 3000-line log looking for "ERROR". The failure might be at extraction (LLM JSON parse), normalization (fuzzy match), or indexing (vector index not ready). Hard to even tell which stage broke.
- *With Prefect UI:* Each `@task` is a row. You see *which* document failed, at *which* stage, with the full stack trace attached. Green = good, red = the exact task to rerun.

**Scheduling + deployment decoupling** — `prefect deployment run ingest-all-data-etl`
- *Without Prefect:* You wire cron, a Bash script that sets env vars, a locking mechanism (to prevent double-runs), log rotation, and a Slack alert on exit code != 0. Then you do it again for `memory-extraction-etl`. And again for `memory-indexing-etl`.
- *With Prefect:* `to_deployment(name=...)` on each flow, served by `make serve-workflows`. Triggered by the Makefile, by a cron block in the deployment, by a webhook, or from the MCP tool path (`ingest_substack_article` is *the same flow* whether called from MCP or from `prefect deployment run`). One runtime, one UI, one set of retry semantics.

#### 7c. Why Query Tools Don't Need Prefect

It's a deliberate asymmetry — worth stating explicitly:

- **Cost of a failed query is zero.** The agent just calls the tool again.
- **Queries are already inside a retry loop** (the NL→pipeline self-correction loop in §6a-ii, and the agent's own reasoning loop above that).
- **Latency matters.** An MCP tool call is a synchronous agent turn; wrapping it in Prefect adds submission/queueing overhead for no durability gain.
- **No partial state to recover.** A `$aggregate` either returns docs or raises — nothing to resume.

Wrapping them would be **cargo-culting the orchestrator**. The rule of thumb in this repo is: *Prefect-wrap anything that writes or anything that costs money if it crashes halfway*. Everything else stays direct.

---

### 8. FastMCP — Why This Framework, and What It Gives Us

The entire MCP surface of this project is **~300 lines** across `src/twin/mcp/server.py`, `tools.py`, `ingest.py`, and `deep_search.py`. The only framework imports are:

```python
from fastmcp import FastMCP, Context
from fastmcp.server.lifespan import lifespan
```

Everything the agent sees — six tools, their schemas, their descriptions, the lifecycle of the DB/LLM/embedding dependencies — rides on three decorators: `@lifespan`, `@mcp.tool`, and implicit `Context` injection.

#### 8a. FastMCP Features Actually Used

| Feature | Where in this repo | What we get for free |
|---|---|---|
| `FastMCP(name, instructions=, lifespan=)` constructor | `mcp/server.py:46` | Server identity, agent-facing routing guidance (`instructions=`) that ships in `initialize` response, one-place lifespan wiring. |
| `@lifespan` async-generator | `mcp/server.py:17` | Startup/shutdown hook — opens `AsyncMongoClient`, builds `llm` and `embedding_model`, calls `ensure_indexes()` once, yields a DI dict, closes the Mongo client on teardown. Zero per-request init. |
| `@mcp.tool` decorator | `mcp/tools.py` (×6) | Auto-registration; no `list_tools()` handler, no `call_tool()` dispatch, no `types.Tool(...)` object to hand-build. |
| **JSON Schema from type hints** | Every tool signature | `query: str`, `visualize: bool = False`, `max_results: int = 10`, `session_id: str \| None = None` → FastMCP emits full `inputSchema` automatically. Defaults become optional params; `None`-unions become nullable. |
| **Tool description from docstring** | Every tool | The multi-line docstring in `query_memory`/`search_memory`/etc. becomes what the calling LLM sees when deciding which tool to pick. The `Args:` block is parsed into per-parameter descriptions. |
| **`Context` parameter injection** | `ctx: Context` on every `@mcp.tool` | `ctx.lifespan_context` is the DI dict yielded by `app_lifespan`. FastMCP **omits `ctx` from the agent-facing schema** — it sees only `query`, `visualize`, etc. |
| **Return-value auto-serialization** | Tools return `str` (JSON payloads) | FastMCP wraps the return in `TextContent` for the MCP protocol — no manual `types.TextContent(type="text", text=...)` wrapping. |
| **`mcp.run()` transport** | `scripts/serve_mcp.py` | One line starts the stdio transport. No `asyncio.run(stdio_server(...))` boilerplate, no `InitializationOptions` struct. |

#### 8b. Concrete Before/After — Standard `mcp` SDK vs. FastMCP

Registering just the two query tools (`query_memory`, `search_memory`) with the low-level SDK vs. with FastMCP:

**Low-level `mcp` SDK** (~80 lines, hand-maintained):

```python
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
import asyncio, json

server = Server("twin-memory")

# Resources manually tracked outside the framework.
_state: dict = {}

async def _startup() -> None:
    _state["client"] = await init_mongodb(...)
    _state["llm"] = get_llm()
    _state["embedding_model"] = get_embedding_model()
    await ensure_indexes(_state["client"], ...)

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="query_memory",
            description="Query the knowledge graph using natural language. ...",
            inputSchema={
                "type": "object",
                "properties": {
                    "query":       {"type": "string",
                                    "description": "Natural language question..."},
                    "visualize":   {"type": "boolean", "default": False,
                                    "description": "If true, also render..."},
                    "max_results": {"type": "integer", "default": 10,
                                    "description": "Maximum number of documents..."},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_memory",
            description="Search the knowledge graph using semantic + text search...",
            inputSchema={
                "type": "object",
                "properties": {
                    "query":       {"type": "string"},
                    "top_k":       {"type": "integer", "default": 10},
                    "max_hops":    {"type": "integer", "default": 1},
                    "max_results": {"type": "integer", "default": 10},
                    "visualize":   {"type": "boolean", "default": False},
                },
                "required": ["query"],
            },
        ),
        # ... four more entries for deep_search_memory, ingest_url,
        #     ingest_file, ingest_conversation ...
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "query_memory":
        results = await execute_nl_query(
            client=_state["client"], database=..., llm=_state["llm"],
            embedding_model=_state["embedding_model"],
            query=arguments["query"],
            max_results=arguments.get("max_results", 10),
        )
        output = _serialize(results)
        if arguments.get("visualize"):
            output += _visualize(results)
        return [types.TextContent(type="text", text=output)]
    elif name == "search_memory":
        # ... duplicate the dispatch for every tool ...
    raise ValueError(f"Unknown tool: {name}")

async def main() -> None:
    await _startup()
    async with stdio_server() as (read, write):
        await server.run(read, write, InitializationOptions(...))

if __name__ == "__main__":
    asyncio.run(main())
```

**FastMCP** (the actual code):

```python
# mcp/server.py
@lifespan
async def app_lifespan(server: FastMCP) -> AsyncGenerator[dict, None]:
    client = await init_mongodb(...)
    llm, embedding_model = get_llm(), get_embedding_model()
    await ensure_indexes(client, database)
    yield {"client": client, "database": database,
           "llm": llm, "embedding_model": embedding_model}
    await client.close()

mcp = FastMCP("Twin Memory", instructions="...", lifespan=app_lifespan)

# mcp/tools.py
@mcp.tool
async def query_memory(query: str, ctx: Context,
                       visualize: bool = False, max_results: int = 10) -> str:
    """Query the knowledge graph using natural language. ...

    Args:
        query: Natural language question about the knowledge graph.
        visualize: If true, also render an interactive HTML graph visualization.
        max_results: Maximum number of documents to return (default 10).
    """
    lc = ctx.lifespan_context
    results = await execute_nl_query(client=lc["client"], ...)
    ...

@mcp.tool
async def search_memory(...): ...

# scripts/serve_mcp.py
if __name__ == "__main__":
    mcp.run()
```

What collapsed:

- **Schema definition** → gone (derived from type hints + `Args:` block).
- **Dispatch `if name == "query_memory"` chain** → gone (decorator-registered).
- **Tool description strings** → gone (pulled from docstring).
- **Shared state singleton** → replaced by `ctx.lifespan_context` DI.
- **Transport bootstrapping** → `mcp.run()`.
- **Return wrapping** → `TextContent` done by the framework.

Ratio: ~80 lines → ~15 lines **per tool pair**, and every future tool is ~10 lines on top, not ~15 lines in two places that must stay in sync.

#### 8c. Why FastMCP Fits *This* Project Specifically

Four properties of agentic GraphRAG map exactly onto FastMCP's strengths:

1. **Tools grow with the ontology.** Every new `NodeType` or data source tends to get a new tool (`ingest_youtube`, `query_people`, ...). With the low-level SDK that means editing three files (`list_tools`, `call_tool`, and the business logic) plus a schema. With FastMCP it's one decorated function.
2. **Heavy shared resources.** MongoDB client, Gemini LLM, embedding model — expensive to build, must be shared across all tool calls. The `@lifespan` DI pattern is exactly the right primitive; you don't build a `_state` dict and hope nothing forgets to read from it.
3. **Instructions-as-routing.** The `instructions=` string on `FastMCP(...)` is the agent's routing manual. In the low-level SDK this is an afterthought; in FastMCP it's a first-class constructor arg — which nudges you to actually write it and keep it current (see the string in `mcp/server.py:48-56`).
4. **Type-hint-driven schemas match the codebase's style.** This project is already `pyproject.toml: requires-python = ">=3.14"` with type hints on every function. FastMCP's "type hints *are* the schema" model is a zero-marginal-cost feature — we'd have written the annotations anyway.

#### 8d. PROs / CONs — FastMCP vs. the Standard `mcp` SDK

**PROs of FastMCP**

- **Less boilerplate** — ~5–10× fewer lines to register a tool (see §8b).
- **No drift between docs and schema** — docstring and type hints are the source of truth, and drift is impossible because the framework reads from them directly.
- **Dependency injection built in** — `Context.lifespan_context` plus the `Context` annotation for logging, progress, elicitation, sampling. The low-level SDK gives you none of this.
- **Server composition** — FastMCP can mount sub-servers (`mcp.mount(other_mcp)`), import OpenAPI specs, proxy other MCP servers, all things we'd want as the toolset grows.
- **More transports out of the box** — stdio, HTTP streamable, SSE switchable via `mcp.run(transport=...)`; low-level SDK forces you to pick and wire each.
- **Maintained aggressively** — FastMCP tracks the evolving MCP spec (elicitation, structured content, progress tokens, cancellation) and backports features faster than the low-level SDK.
- **Decorator-based resources/prompts too** (`@mcp.resource`, `@mcp.prompt`) — same ergonomics if we add resource endpoints for session-ID-scoped deep-search output or static ontology snapshots.

**CONs of FastMCP**

- **Magic you have to learn** — "why is `ctx` not in the schema?" "why did `str | None` become nullable?" is obvious once you read the docs but opaque at first glance. The low-level SDK has no magic — every field is written out.
- **Schema generation is *opinionated*.** For edge cases (recursive types, custom discriminated unions, enums-with-titles for elicitation) you may need to pass `output_schema=`, `meta=`, or a custom generator. The low-level SDK lets you hand-write exactly the schema you want.
- **Third-party dep chasing MCP spec.** FastMCP lags the official spec by days to weeks at most, but if you need the *latest* experimental spec feature on release day you'll get it from the low-level SDK first. (In practice this has not been a problem for this project.)
- **Heavier install footprint.** FastMCP pulls in Pydantic v2, HTTP machinery, OpenAPI parser, etc. The low-level `mcp` SDK is leaner if you only need stdio.
- **Harder to audit exact wire traffic.** When the framework constructs `initialize` / `listTools` / `callTool` responses for you, debugging a spec-conformance bug means reading FastMCP source. With the low-level SDK you wrote it, so you know what went out.
- **Less control over error mapping.** FastMCP's default is to convert exceptions to MCP error responses with a generic shape; if you need specific `McpError` codes (e.g., `INVALID_PARAMS` vs. `INTERNAL_ERROR`) for policy reasons, you have to opt in explicitly.

**When the low-level SDK is actually the right call**

- You're building a reference / compliance test suite and want byte-exact control over the wire format.
- Your "tools" are generated dynamically at runtime from a remote schema service and you need to feed raw `inputSchema` dicts you didn't write.
- You are embedding MCP into a framework that owns its own DI and lifecycle (FastAPI, Django) and the decorator pattern would conflict with existing wiring.
- You need MCP spec features that haven't landed in FastMCP yet *and* can't wait a week.

None of those apply here, which is exactly why this repo picked FastMCP.

---

### 9. Why Six Tools, Not One — Tool Choice Rationale

Every MCP tool has a token cost in the agent's `listTools` response *and* a cognitive cost in the agent's tool-selection reasoning. Shipping six tools is a deliberate choice — each one covers a regime the others can't. Collapsing any pair would either lose a capability or make the common case worse.

#### 9a. Three Query Tools — Each Solves a Different Retrieval Problem

```
                         retrieval regime
  precise / structured ◄──────────────────────────────► broad / exploratory
  (aggregations,                                        (many seeds,
   filters, exact graph                                 deep traversal,
   traversals)                                          100+ results)

       query_memory  ──────► search_memory  ──────► deep_search_memory
       (NL → pipeline)       (hybrid RRF)            (disk + YAML index)
            │                     │                         │
       LLM-flexible           deterministic            progressive
       but can fail           always works            disclosure to
                                                      avoid flooding
                                                      the context
```

**1. `query_memory` — the default (NL → MongoDB aggregation)**

Used when the question is structured enough for MongoDB to answer precisely: *"top 5 people with the most open tasks"*, *"episodes Alice experienced in Q2 that mention Bob"*, *"documents referenced by more than 3 others"*. The NL→pipeline translator (§3, §6a-i) gives the agent the full expressive power of the aggregation framework — filters, `$group`, `$lookup`, `$graphLookup`, `$vectorSearch` with filters — without requiring the agent to know MongoDB.

This is the **default** because most real agent queries *are* structured once you read them carefully. "What's alice working on?" wants a `$match` on `edge.type=todo` starting from `person:alice`, not a semantic nearest-neighbor search.

**Why not just this tool?** Because LLMs emit invalid pipelines sometimes, and the self-correction loop (§6a-ii) caps at `max_retries=1` by design. When the loop gives up, the agent needs a fallback that *will* return results rather than "pipeline failed after retries."

**2. `search_memory` — the hybrid fallback (RRF + k-hop)**

Used when NL→pipeline isn't appropriate or has failed: the question is fuzzy ("anything related to observability"), or the agent already tried `query_memory` and got an error. This tool has **no LLM in the critical path** — it's pure `$vectorSearch` + `$text` + RRF + `$graphLookup`. Deterministic, fast, and it always returns *something* as long as the KG is non-empty.

The `instructions=` string on the server explicitly labels it as the **"reliable fallback for semantic similarity search"** so the agent knows to reach for it in exactly that context.

**Why not always use this?** Because hybrid search can't answer precise questions. "Top 5 people with most tasks" via RRF returns a semantic neighborhood of people-and-tasks, not a ranked count. You'd have to post-process in the agent's context — more tokens, less accurate.

**3. `deep_search_memory` — broad exploration with progressive disclosure**

Used when the agent is investigating, not answering: *"tell me everything we know about our Q2 migration"*, *"summarize what Alice has been doing all year"*. Same hybrid engine as `search_memory`, but cranked up (`top_k=50`, `max_hops=3`) — which would blow out the context window if returned inline.

Instead, the tool writes every node/edge to `.memory/{session_id}/*.md` and **returns only the YAML index** (§6a diagram). The agent — which by assumption has a **filesystem-capable harness** (Claude Code, Cursor, etc., with `Read` available) — pulls individual files on demand. MCP payload stays tiny (one YAML index ≈ 1–5KB) regardless of whether the underlying search found 10 or 500 documents.

**Why this matters:** when you dump 100+ chunks from an MCP response directly into the context window, you pay the token cost *before the agent has even decided what's relevant*. Progressive disclosure inverts that — the agent triages with the index, then pays tokens only for what it actually reads.

**Why not always this one?** Two reasons:
- **Harness assumption.** `deep_search_memory` requires the caller to have `Read` / filesystem tools. Generic MCP clients (no harness) can't follow up on `.md` paths — they need results inline.
- **Latency + disk I/O for small queries.** A "what's Alice working on?" query doesn't need 50 files written to disk. That'd be wasteful overhead for a one-line answer.

#### 9b. Tool Selection Decision Tree

```
  Is the agent inside a filesystem-capable harness (Claude Code / Cursor)?
  │
  ├─ no  ──► query_memory (fallback: search_memory)
  │
  └─ yes ──┬─ Is the question structured? (filters / counts / traversal)
           │   ├─ yes ──► query_memory        ◄── default path
           │   └─ no  ──► search_memory
           │
           └─ Is the question exploratory? (broad / "tell me about X")
                        └─ yes ──► deep_search_memory
```

Empirically in the `instructions=` string the server gives the agent, these routing cues are spelled out explicitly — the agent doesn't have to re-derive this tree at runtime.

#### 9c. Three Ingest Tools — Three Input Realities

```
  local (cold data)    remote (live data)    in-flight (hot context)
       │                     │                      │
       ▼                     ▼                      ▼
   ingest_file           ingest_url         ingest_conversation
   (.txt/.md/.html)      (URL dispatch)     (the current chat)
       │                     │                      │
       │  source_uri         │  source_uri          │  source_uri
       │  = file:///abs/...  │  = https://...       │  = conversation://<hash>
       │                     │                      │
       └────────── all three collapse to Document ──┘
                             │
                             ▼
               run_ingestion_pipeline(...)
```

**1. `ingest_file` — the local path**

Used when I'm working locally and the knowledge exists on disk: notes in Obsidian, downloaded PDFs converted to markdown, meeting transcripts, technical docs I've cloned. No network, no parsing of arbitrary HTML, no API keys needed — just `path.read_text()` through the `.txt`/`.md`/`.html` adapter.

Why a dedicated tool? Because `file://` paths can't be dispatched through `ingest_url` — `httpx` won't fetch them, and the whole URL-handler registry (`substack.com` → Substack handler, etc.) assumes remote hosts. Treating local files as a first-class source also enables the *LATENT upgrade-in-place* trick (§4c): if another ingestion already referenced the file path as a placeholder, `ingest_file` fills it in without producing a duplicate node.

**2. `ingest_url` — the common case**

The **most-used ingestion path**, because most knowledge worth capturing lives on the web: Substack articles, arXiv papers, blog posts, internal wiki pages. The tool dispatches on domain (`data/core/ingest.py` registry) and routes to a source-specific pipeline that knows how to fetch, strip boilerplate, extract metadata, and resolve references.

Why dispatch and not one big URL fetcher? Because "fetching a URL" is a misleadingly abstract operation — Substack articles need author/date extraction, YouTube needs transcript fetching, arXiv needs LaTeX-aware parsing. A registry keeps each source's quirks isolated; adding a new source means writing one handler and registering its domain.

**Why is this the default over `ingest_file`?** Because the typical twin-memory use case is continuous capture from reading, not from local curation. "I just read this article, remember it" >> "I maintain a notes folder and sync it."

**3. `ingest_conversation` — continual learning from the current context**

Used to **feed the conversation I'm currently having back into the twin's memory**. Everything the twin knows about me, my ongoing projects, and recent decisions comes from conversations — not curated documents. Without this tool, the twin would know my published writing but not the live discussion where I actually work things out.

Key design choices:
- **Content-hash source_uri** (`conversation://<sha256[:16]>`) — so re-ingesting the same conversation is a no-op, and the twin never stores duplicates of the same chat.
- **Same extraction pipeline** as files/URLs — conversations become `Document`s with `source_type=CONVERSATION`, and the LLM extracts people, tasks, episodes, preferences from them just like from any other document. No special-cased path.
- **Agent-invoked, not harness-invoked.** The agent decides when a conversation has reached a "checkpoint worth remembering" and calls this tool mid-session. In this repo a Stop hook + the `twin-memory` skill trigger it automatically at end of session, but it's also callable explicitly ("remember what we just discussed").

Why a dedicated tool over "just save the conversation to a file and call `ingest_file`"? Two reasons:
- **Zero-friction capture.** The agent has the conversation text in its context already; writing it to a temp file, calling `ingest_file`, and cleaning up the file is three tool calls when one would do.
- **Semantic distinction.** `SourceType.CONVERSATION` lets queries distinguish conversational knowledge from documentary knowledge — useful when you want to know "what did I actually *say* about X" vs. "what have I *read* about X".

#### 9d. Why These Three Ingest Sources Are Enough (for now)

The ingestion surface is deliberately small — three tools, not "one tool per source type." The adapter pattern (everything becomes a `Document` with a distinct `source_uri` scheme) means:

- Adding **YouTube** doesn't need a new MCP tool — it needs one entry in the `_URL_HANDLERS` registry, and `ingest_url` absorbs it.
- Adding **Google Drive / S3** (remote files) would fit under `ingest_url` with a custom URL scheme or `ingest_file` extended to handle cloud URIs.
- Adding **email / Slack messages** would be a new tool only if the fetching pattern is truly different — otherwise `ingest_conversation` with pre-formatted text covers it.

So the three tools correspond to three **transport realities**, not three content types. Content types are handled by the ontology + extraction pipeline behind them, which is where the semantic interpretation lives and where it belongs.

---

### 10. Architectural Takeaways

1. **Single collection, string `_id`s, upsert semantics.** `"person:alice"` nodes and `"person:alice|todo|task:x"` edges in one collection means every search/traversal is one place and every write is idempotent by construction.
2. **Lifespan-injected dependencies, not globals.** DB client, LLM, embedding model are created once and passed via `ctx.lifespan_context`.
3. **Ontology is the prompt.** Pydantic models of node/edge types drive both LLM extraction prompts *and* the NL-query system prompt — one source of truth.
4. **Validate every LLM-generated pipeline against an allow-list.** Combine with a self-correcting retry loop keyed on the DB/validator exception.
5. **Progressive disclosure for big result sets.** Write to disk, return a YAML index, let the agent pull on demand.
6. **Input adapters, uniform target.** Files, URLs, conversations all normalize to `Document` with distinct `source_uri` namespaces (`file://`, `https://...`, `conversation://<hash>`), after which one extraction + indexing pipeline handles everything.
