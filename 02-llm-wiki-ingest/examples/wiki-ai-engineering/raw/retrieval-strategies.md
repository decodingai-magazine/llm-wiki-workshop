# LinkedIn Post Guideline

Post 19: Deep dive into the retrieval algorithms used for GraphRAG + how to serve it via FastMCP + how Prefect helps

## LinkedIn Post

[LinkedIn Post](https://www.linkedin.com/feed/update/urn:li:activity:7480236757758742528/)

Building memory for AI agents is less about storage and more about retrieval.

Let me explain...

I'm building a personal assistant from scratch for my next book with Manning.

And one challenge I faced was deciding how the agent retrieves (from unified memory) the appropriate information quickly, reliably, and with as little complexity as possible.

This led me to store the entire knowledge graph in a single database (e.g., MongoDB).

One system handles:

• Full-text search
• Semantic search
• Graph traversal

But you'll lose a graph-native query language.

In exchange for simplicity, this is a trade I'd make every time for a personal assistant.

When doing GraphRAG, the agent has three ways to search its unified memory:

1/ Graph search

This is the default path.

1. Run text search and vector search in parallel.
2. Fuse both rankings using Reciprocal Rank Fusion (RRF).
3. Traverse 2-3 hops through the graph to retrieve connected knowledge.
4. Rerank the candidates.
5. To keep context tight, pick the top 10.

2/ Deep search

Sometimes keeping the top 10 isn't enough.

You want to use everything that was retrieved as context.

But after 2-3 hops, you can easily retrieve 50+ documents that won't fit in the context window.

Instead, save everything to disk and build a lightweight LLM wiki on demand.

This temporary wiki serves as the agent's localized memory, allowing it to explore large amounts of data through progressive disclosure without overwhelming the context window.

3/ Agentic search

Some questions don't fit predefined retrieval algorithms so the LLM writes the database query itself.

The ontology tells it which entities and relationships exist.

You add a validation loop to ensure the query is syntactically correct.
And a permission layer to ensure the query stays within safe boundaries.

Here's the insight:

GraphRAG isn't just vector search plus a graph; It's multi-hop traversal during retrieval.

Similarity finds the entry point and the graph finds everything connected to it.

We serve this unified memory as an MCP server via FastMCP (by Prefect).

The agent never talks directly to the database.

Instead, a harness such as Claude Code calls search-and-write tools, while the MCP layer decides how memory should be queried.

Every fact the agent retrieves must first be processed.

This is where Prefect comes in.

Every ingestion pipeline runs asynchronously as durable workflows across parallel workers with retries, caching, checkpointing, and centralized rate limiting.

Even if one extraction step fails, indexing can continue, so the graph remains searchable.

The read path never waits for orchestration.

This has become one of my most important design principles.

Orchestrate the writes.
Never the reads.

P.S. What retrieval strategy do you rely on most when building the memory for your AI agents?

![[assets/retrieval-strategies-1783325032221.jpeg]]

## What We Are Planning to Share

A deep dive into the retrieval algorithms behind the GraphRAG memory of Paul's personal assistant: the three search options the agent can call — normal graph search (hybrid seeds, reranked, then traversal), deep search (broad traversal that builds a light on-demand wiki the agent uses as localized memory), and agentic search (the LLM writes the database query itself, guided by the ontology) — then the multi-hop traversal step that makes it all GraphRAG, and how the unified memory is powered in production: served to coding agents via FastMCP, with writes scaled by Prefect pipelines. Readers walk away understanding exactly how a query flows through a GraphRAG system and the design rules that keep the read path fast: one database over three, fuse by rank before you rerank, and "orchestrate the writes, never the reads."

## Why We Think It's Valuable

Most GraphRAG content stops at a toy demo or a vague boxes-and-arrows diagram — almost none of it walks through the actual retrieval algorithms. This post does: how seed searches are fused with Reciprocal Rank Fusion and reranked into a final top 10, how deep search builds an on-demand wiki that acts as the agent's localized memory, how the ontology tells the LLM what to search when it writes queries itself (and the validation loop that fixes its mistakes), why the multi-hop traversal step is the single thing separating GraphRAG from normal RAG, and how FastMCP and Prefect carry it all into production without ever slowing down a read. Engineers get the why behind each choice, not just the what.

## Who Is the Target Audience

AI engineers and technically curious builders working on RAG, agents, or memory systems — a broader slice than hardcore GraphRAG specialists. They know what RAG and agents are and may have played with vector databases; they don't need database internals to follow. They are missing a worked, opinionated reference for how ingestion and retrieval fit together in one production system.

## Point of View

Defaults apply: Paul Iusztin writes in the first person, addresses a single reader as "you", and refers to the team as "we" / "our" where a team framing fits; the build itself is personal ("I am building").

## Personal Story

While building a personal assistant from scratch for my next book with Manning, I learned that the unified memory is 90% of the problem — ingestion and retrieval are two halves of one system, and they only work when built in harmony. Source: https://github.com/iusztinpaul/building-agentic-systems

## Metadata

- Word count: 400-450 words

## Content

1. **Hook (2 lines).** Anchor in the lived build, then pivot straight to retrieval, verbatim: _"I'm building a personal assistant from scratch for my next book with Manning."_ / _"90% of the problem is memory — and the hardest part of memory is retrieval. Here's how GraphRAG retrieval actually works (and how FastMCP + Prefect power it):"_ Manning appears by name, plain text.
2. **Foundation beat (the contrarian setup that unlocks everything).** The assistant's memory is a knowledge graph. The whole graph — nodes, edges, AND vectors — lives in ONE collection of a single database that supports everything (text, vector, and graph search), such as MongoDB. No dedicated graph database, no separate vector store. That one decision means full-text search, semantic (vector) search, and graph traversal all run against the same data. Trade-off named honestly: you give up a graph-native query language, and it works because the graph is personal-scale, not Google-scale. Naming rule: this is the ONLY place a specific database is named — everywhere else in the post say "the database".
3. **Transition (1 line).** _"The agent gets three ways to search this memory:"_ — sets up the three Unicode-bold numbered blocks (𝟭/ 𝟮/ 𝟯/). Keep each block tight (3–5 rendered lines).
4. **𝟭/ Graph search — the workhorse.** The default path, walked plainly: embed the query (an embedding model with 1024 dimensions is a good balance: strong retrieval quality without bloating the vector index) → vector search finds what's _similar_ while full-text search finds what _matches by name_, in parallel → fuse the two ranked lists with Reciprocal Rank Fusion (RRF) → rerank the fused candidates and keep the top 10 hits → expand the graph 1 hop around them. Why this order: RRF fuses by rank, not score, so the two searches never need calibration — and the reranker then only has to fine-order a small fused candidate set, not the whole collection. If vector search fails, it silently degrades to text-only: a read never hard-fails.
5. **𝟮/ Deep search — an on-demand wiki as localized memory.** Same algorithm, scaled up: top 50 seeds, up to 3 hops. The clever part is the return shape — instead of dumping hundreds of nodes into the conversation, it builds a light LLM wiki on demand, per query: full results written as readable files, fronted by a lightweight index with one-line summaries. That wiki becomes the agent's localized memory for the task — it queries it dynamically, reads only the entries that matter, and comes back to it as it works. Progressive disclosure: whole graph neighborhoods become explorable without ever flooding the context window.
6. **𝟯/ Agentic search — the LLM writes the query itself.** For questions the fixed paths can't express (filters, aggregations, counts), the LLM (Gemini) translates natural language straight into a database query — dynamically, per question. How it knows _what_ to search: the graph's ontology — every entity and relationship type the memory can contain — is compiled into its prompt, so it writes queries against a schema it actually understands instead of guessing at field names. How it stays safe: every generated query passes a validation gauntlet (an operation allow-list, forced user-scoping the model cannot override, a hard result cap) — and when validation or execution fails, the error is fed back to the LLM, which fixes its own query and retries. Flexibility with a fence around it.
7. **What-makes-it-GraphRAG beat (Unicode-bold lead line, not numbered — e.g. 𝗦𝗼 𝘄𝗵𝗮𝘁 𝗺𝗮𝗸𝗲𝘀 𝘁𝗵𝗶𝘀 𝗚𝗿𝗮𝗽𝗵𝗥𝗔𝗚?).** The core idea of the post, verbatim: _"GraphRAG, different from normal RAG, is really just one extra step: multi-hop traversal during retrieval."_ All three options lean on it: seeds are only entry points, and the algorithm walks the graph in BOTH edge directions from there, pulling in entities _connected_ to the answer that no similarity search would ever surface (a project links to its people, decisions, and deadlines even when none of them resemble the query). That connected slice of memory, not a pile of look-alike chunks, is what the agent reasons over.
8. **FastMCP beat (Unicode-bold lead line).** Zoom out: what we actually built is a unified memory — and we serve it as an MCP server via FastMCP (by Prefect). The three search options ship as three read tools, plus write tools for ingesting new documents, conversations, and URLs, so coding agents like Claude Code talk to the memory directly — no custom API layer; the tool descriptions themselves tell the agent which tool fits which question. The write tools carry the bridge to the next beat: they never block a session — they submit a pipeline run and return in milliseconds, verbatim: _"The MCP server is the front desk. The heavy lifting happens in the back office."_
9. **Prefect beat (Unicode-bold lead line).** The back office is Prefect, and it's how the writes scale: every fact the three searches retrieve was manufactured by a Prefect pipeline — chunking, LLM extraction, entity resolution, embeddings, indexes — sharded across parallel worker runs, with automatic retries, result caching (a failed run resubmitted skips the LLM calls it already paid for), and one global rate limit keeping a burst of ingestions inside the embedding API budget. The guarantee that matters to retrieval: even when extraction partially fails, the indexing step still runs — the graph stays searchable. Then the rule, verbatim: _"Prefect never touches the read path — that's the point."_ Reads stay millisecond-scale; the pipelines make sure what they read exists, is embedded, and is indexed.
10. **Synthesis (1–2 lines).** The design rule that ties it together, verbatim: _"Orchestrate the writes, never the reads — the only thing they should share is a rate limit."_
11. **P.S. engagement question.** Verbatim: _"P.S. Would you have picked a dedicated graph database instead? Curious why."_ No link — the post itself is the resource. Attribution check: FastMCP (by Prefect) named once in the FastMCP beat, Prefect named in the Prefect beat lead — both plain text, no markdown bold on brand names.

## Notes

Background reference for the writer — how the system actually works in the repo (github.com/iusztinpaul/building-agentic-systems). High-level grounding only; the post's narrative lives in `## Content` above. Do not pull extra beats from here into the post; use it to keep every claim accurate.

Naming rule for this post (sponsor focus): FastMCP and Prefect are the technologies to spotlight. MongoDB is named exactly once — in the foundation beat, as the example of a database that supports everything — and nowhere else; elsewhere say "the database". Embedding models stay generic: never name Voyage AI in the post; the vendor-free claim "1024 dimensions is a good balance" is allowed (it matches the shipped config). The vendor specifics below exist for fact-checking only.

**The system.** "Tree" is a personal assistant rooted in a knowledge-graph memory. Monorepo with two apps: a Python memory app (the context layer: ETL + knowledge graph + MCP server) and a TypeScript coding-agent harness that consumes the memory over MCP. The memory is the product; the post covers its read path, its serving layer, and its write path.

**Design decision 1 — one collection, no graph database.** The entire knowledge graph lives in a single MongoDB collection (`knowledge_graph`). Nodes and edges are documents in the same collection, discriminated by a `kind` field; vectors are embedded on the node documents. IDs are deterministic (node: user + type + name; edge: source + type + target), which makes every write an idempotent upsert. Why: text search, vector search, and graph traversal run against one store — one system to operate, no sync between a vector DB and a graph DB, and it's honest about scale (a personal knowledge graph, not a web-scale one). Trade-off: no graph-native query language like Cypher; traversal is MongoDB's `$graphLookup` aggregation stage.

**Design decision 2 — hybrid retrieval with RRF (reranker on the roadmap).** The read path: embed the query (Voyage AI `voyage-3.5`, 1024 dimensions, cosine similarity) → run two searches in parallel — Atlas vector search (candidate pool = 10× the requested results) and classic MongoDB full-text search over names, aliases, and content → fuse the two ranked lists with Reciprocal Rank Fusion (constant k=60, both lists weighted equally). RRF fuses by _rank_, not score, so the two scoring systems never need calibration. IMPORTANT accuracy note for the writer: a reranking step that re-orders the fused candidates into the final top 10 is on the roadmap but NOT yet in the code — per Paul's direction the post presents "fuse with RRF → rerank → keep top 10" as the algorithm; keep that phrasing (it describes the design), don't claim a specific reranker model or benchmark. The fused winners become seeds for graph expansion: two `$graphLookup` passes (one following outgoing edges, one incoming — traversal is bidirectional by construction), 1 hop by default, 3 hops for deep search, results merged and deduplicated. If vector search fails, retrieval silently degrades to text-only — a read never hard-fails.

**Design decision 3 — a second, LLM-written query path.** For questions the fixed algorithm can't express (aggregations, filters, counts), a separate tool lets Gemini translate natural language directly into a MongoDB aggregation pipeline. The model knows what to search because the graph's full ontology — every entity and relationship type the memory can contain — is compiled into its system prompt, so it targets a schema it actually understands. It ships only because of the guardrails: an allow-list of permitted stages (the only join allowed is `$graphLookup`, and only on the graph collection), tenant scoping injected and overwritten by the server so the model can never escape its user, an `__EMBED__` placeholder so the model can request vector search without ever seeing an embedding, a forced result limit, embeddings stripped from every response, and a self-correction retry where validation/execution errors are fed back to the model. Predictable path for most queries; guarded flexible path for the rest.

**Design decision 4 — the memory is an MCP server, not an API.** The Python memory app is exposed via FastMCP (by Prefect) as an MCP server — 13 tools in three families: retrieval (query / search / deep search), ingestion (URLs, files, conversations, web search + scrape), and human curation (review and confirm/reject duplicate-entity merges). Coding agents (Claude Code, Cursor, the custom harness) connect to it like any other tool server: stdio locally, OAuth-protected HTTP on FastMCP Cloud from the same codebase. Serving details that matter: tool docstrings are written as routing instructions for the _agent_ (which tool to prefer when); deep search uses progressive disclosure (returns a lightweight YAML index, writes full results to markdown files the agent reads selectively — in effect a light on-demand wiki per query that acts as the agent's localized memory, protecting the context window); every tool returns structured JSON errors instead of raising; the server boots the DB connection and the LLM/embedding clients once in its lifespan and validates the live vector index dimensions against config at startup.

**Design decision 5 — Prefect orchestrates every write, and never a read.** Ingestion is minutes-long (chunk → LLM graph extraction per chunk → entity resolution → embed → dedup → write → index) and LLM calls fail routinely, so the write path runs as Prefect durable workflows. The topology: an orchestrator flow finds pending documents, shards them, dispatches one worker run per shard in parallel, then fires exactly one trailing indexing run — regardless of shard failures, so a partial extraction is still searchable. Reliability mechanics: task-level retries with delays; result caching on the pure, expensive stages (30-day cache on LLM extraction, 90-day on embeddings) so a resubmitted failed run skips the LLM calls it already paid for — while every DB-write stage is deliberately uncached; a Prefect global concurrency limit named after the embedding API (3 requests/minute, matching Voyage's free tier) shared across all concurrent runs, plus an admission cap of 4 concurrent flow runs. Idempotency lives in MongoDB, not Prefect state: there is no "ingested" status flag — a document counts as ingested iff its ID appears in some graph node's sources list, and every run just recomputes the pending set. Deployment: local dev serves flows in-process; production uses a Prefect managed work pool (Prefect Cloud hosts the workers, clones the repo per run) with nightly cron schedules. Free-tier constraint acknowledged in the design: max 5 deployments.

**The data flow, end to end.** Write path: sources (Substack, YouTube, RSS, HuggingFace datasets, web URLs, conversations) → per-source ETL pipelines normalize into a `documents` collection → the memory pipeline chunks (512 tokens, 64 overlap), extracts entities/relationships with Gemini, resolves entities (alias → exact → fuzzy → semantic matching), embeds, deduplicates, and upserts nodes/edges → indexing embeds any remaining nodes and ensures the search indexes. Read path: agent calls an MCP tool → in-process hybrid search + RRF + graph expansion → results back in the same request. The two paths meet in exactly one place: the shared embedding rate limit (query-time embedding acquires the same Prefect concurrency slot as pipeline embedding).

**Where MCP and Prefect meet.** The ingestion MCP tools are fire-and-forget: they create a Prefect flow run scoped to the new document IDs and return "submitted" with a run ID in milliseconds. The serverless MCP host must not block on a minutes-long pipeline; Prefect makes async, durable, retryable execution possible from a single tool call. Honest limitations (fine to acknowledge, not central to the post): the agent has no tool to check a submitted run's status, and freshly ingested content isn't queryable until the pipeline and trailing indexing settle (no read-your-writes).

**Tech stack (for accuracy — only the Content section decides which names appear in the post).** MongoDB as the unified memory (vector + text + graph in one collection); Voyage AI `voyage-3.5` embeddings (1024-dim); Gemini as the frontier LLM (extraction + NL-to-query); FastMCP (by Prefect) for the MCP server; Prefect for orchestration and durable workflows; Beanie/PyMongo async ODM; Opik for tracing every tool call and pipeline run; Bright Data for web search/scraping tools; Docker for local infra; Pydantic everywhere.

**Pros/cons summary (the trade-offs the post draws on).**

- One collection vs dedicated graph DB: one system, one query surface, natural hybrid search vs no Cypher, app-level traversal semantics, personal-scale assumption.
- RRF + reranker vs reranker-only: rank-based fusion needs no score calibration, and the reranker only fine-orders a small fused candidate set instead of the whole collection. (Reranker is roadmap — not yet in code; see the accuracy note in design decision 2.)
- LLM-written queries vs fixed algorithm: expressive long tail vs needs an allow-list, tenant injection, and self-correction to be safe.
- Fire-and-forget ingestion vs blocking: instant tool response, durable retries, cached restarts vs no ingestion-status feedback and delayed queryability.
