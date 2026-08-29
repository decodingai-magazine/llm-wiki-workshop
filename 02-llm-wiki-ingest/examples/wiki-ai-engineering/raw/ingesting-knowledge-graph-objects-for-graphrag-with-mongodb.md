# Ghostwriter Guide: Ingesting Knowledge Graph Objects for GraphRAG with MongoDB as Unified Memory

**Sponsored post for MongoDB**

**Format:** Step-by-step technical guide following the architecture diagram (12 numbered steps)

**Tone:** Practical, developer-focused, educational. Not a sales pitch — show MongoDB as the natural fit by walking through the architecture. Let the reader conclude "oh, MongoDB can do all of this" organically.

**Running example:** The Digital Twin — an AI agent that ingests Personal Notes (Notion/GDrive), Research (articles), Email, and Text Messages to build a knowledge graph about Arthur (the user). Use the Arthur/Felix email example throughout to make it concrete.

**Key thesis:** You don't need separate databases for documents, vectors, and graphs. MongoDB Atlas serves as a **unified memory** layer that handles all three — document storage, native vector search (Atlas Vector Search / HNSW), and recursive graph traversals (`$graphLookup`) — plus immutable event logs via Change Streams. This eliminates the "synchronization tax" of polyglot persistence (cross-DB ETL, consistency risks, complex security).

---

## Architecture Overview

Reference the diagram. The post walks through 12 numbered steps split across three zones:

- **Data Pipeline** (Steps 1–2): Collect raw data from sources into a Data Warehouse (MongoDB)
- **Memory Pipeline** (Steps 3–7): Clean, chunk, extract graph triples, resolve entities, embed, and package into Knowledge Graph Objects
- **Unified Memory** (Steps 8–10): Store as immutable logs in MongoDB, build hybrid indexes (text + semantic + graph), construct query-time views and the knowledge graph
- **Agent Layer** (Steps 11–12): MCP Server exposes Write Memory + Search Memory tools to the agent

---

## Data Pipeline

### Step 1 — Collect Data from Sources

Raw data comes from URIs (web articles, YouTube) and personal sources (Notion, GDrive, Email, SMS). Each source has a different format: structured JSON (Google Calendar), semi-structured (email headers + body, Notion markdown + metadata), or unstructured natural language (SMS, PDFs).

**MongoDB angle:** MongoDB's flexible BSON document model means you don't need to force all these formats into a rigid schema upfront — each source type can have its own shape while living in the same collection.

### Step 2 — ETL into Data Warehouse (MongoDB)

Two ETL paths feed into a single MongoDB Data Warehouse: a **Crawl ETL** for URIs (web scraping, API calls to fetch articles/videos) and a **Personal Docs ETL** for personal sources (Gmail API, Notion API, local file readers). Both produce normalized `Document` objects stored in MongoDB.

**MongoDB angle:** MongoDB Atlas acts as both the data warehouse and the downstream memory layer — no separate staging database needed. Documents land in a `raw_documents` collection with source metadata (`source_type`, `source_uri`, `date`, `authors`).

---

## Memory Pipeline

### Step 3 — Clean + Chunk

Each document is preprocessed: strip HTML, extract headers/metadata (e.g., email `from`, `to`, `date`), normalize text, and chunk long documents into manageable pieces. For the email example: *"Arthur, attached is the GraphRAG survey. Related to your Notion notes on vector search. Coffee Friday?"* → extract headers (`from: Felix`, `to: Arthur`, `date: 2025-11-15`), clean the body text, chunk if needed.

**MongoDB angle:** Cleaned documents are updated in-place using atomic `$set` operations on the same MongoDB collection — no need to move data to a separate processing store.

### Step 4 — Graph Extractor (Open Source)

An LLM (or open-source graph extraction model) extracts **triples** (entity → relationship → entity) guided by a predefined **ontology**. The ontology defines allowed node types (Person, Document, Task, Preference, Episode) and edge types (MENTIONS, CONNECTED_TO, HAS, EXPERIENCED, RELATED_TO).

From Felix's email, the structured extraction produces:
```
(Felix:Person)-[:MENTIONS]->(email_doc:Document {source_type:"email"})
(Arthur:Person)-[:MENTIONS]->(email_doc)
(Arthur)-[:CONNECTED_TO]->(Felix)
(Arthur)-[:HAS]->(Task {content:"Coffee with Felix on Friday"})
(email_doc)-[:RELATED_TO]->(task)
```

Semi-structured extraction (no LLM needed) parses email links/attachments to produce:
```
(email_doc)-[:CONNECTED_TO]->(graphrag_paper:Document {source_type:"article"})
(email_doc)-[:CONNECTED_TO]->(notion_doc:Document {source_type:"notion_note"})
```

**Key point:** Structured + semi-structured extraction combined is the sweet spot for GraphRAG — the ontology keeps it precise, while metadata parsing captures document lineage.

### Step 5 — Normalization (Entity Resolution)

The LLM extracted "Arthur" from the email, but the graph already has "Arthur Iusztin" with alias "Art". Entity resolution checks `full_name` and `aliases`, runs fuzzy/phonetic matching, and merges duplicates instead of creating new nodes. Similarly, "GraphRAG survey" is matched to an existing Document node previously ingested from GDrive.

**MongoDB angle:** Entity resolution queries run against the existing `kg_nodes` collection using MongoDB's text indexes and aggregation pipelines — `$match` on aliases arrays, fuzzy string comparison via `$regex` or Atlas Search, all within the same database where the nodes already live.

### Step 6 — Embedding Model (Open Source)

Generate vector embeddings for multiple node types: `summary_embedding` on Document nodes (so documents are searchable by meaning) AND `content_embedding` on Task, Preference, and Episode nodes (so these non-document entities are also directly findable via semantic search). This is crucial — it means a query can land directly on a Task or Preference without needing to traverse through a Document first.

**MongoDB angle:** Embeddings are stored as vector fields directly on each node document in MongoDB. Atlas Vector Search indexes these using HNSW algorithm. Supports up to 8192 dimensions. MongoDB 8.0 adds Scalar Quantization (4x memory reduction) and Binary Quantization (32x reduction) for scale. Dedicated Search Nodes isolate vector indexing from operational workloads.

### Step 7 — Package into Knowledge Graph Objects

The output of steps 4–6 is a set of **Knowledge Graph Objects** — each containing triplets (node-edge-node relationships), vectors (embeddings), and metadata (source_uri, timestamps, properties). These are the atomic units that will be written to the unified memory.

**MongoDB angle:** Each KG Object maps naturally to a BSON document. A node document in the `kg_nodes` collection might look like:
```json
{
  "_id": "person_arthur",
  "type": "Person",
  "full_name": "Arthur Iusztin",
  "aliases": ["Art", "A. Iusztin"],
  "edges": [
    {"type": "MENTIONS", "target": "doc_email_042"},
    {"type": "CONNECTED_TO", "target": "person_felix"},
    {"type": "HAS", "target": "task_coffee_friday"},
    {"type": "HAS", "target": "pref_langgraph"},
    {"type": "EXPERIENCED", "target": "ep_rag_meetup"}
  ]
}
```
A Document node carries `summary_embedding` as a vector field alongside its properties. A Task node carries `content_embedding`. Everything in one collection, one database.

---

## Unified Memory (MongoDB) — This is the core of the post. Double down here.

### Step 8 — Store as Immutable Logs

KG Objects are **never overwritten**. Every extraction result is appended to an immutable `kg_events` collection as a log entry. Each event document includes: event type (e.g., `NodeCreated`, `RelationshipAdded`, `PreferenceUpdated`), entity ID, the full payload, a version ID, and a timestamp.

**Example — Tracking a preference change:**
- Log entry 1 (June 2025, from Notion): `{type: "PreferenceCreated", entityId: "pref_lang", payload: {content: "Prefers Java"}, timestamp: "2025-06-01"}`
- Log entry 2 (Sep 2025, from SMS): `{type: "PreferenceUpdated", entityId: "pref_lang", payload: {content: "Prefers Python"}, timestamp: "2025-09-15"}`

Both entries are stored. Nothing is overwritten. If the LLM misextracted the September preference, you invalidate that log entry and the view auto-reverts to Java.

**MongoDB angle:** This is Event Sourcing + CQRS natively in MongoDB. The `kg_events` collection is append-only. Use **Change Streams** to monitor new events in real-time — when a new event lands, trigger a background process to update a materialized `kg_current` collection (the latest state). **Performance guardrail:** Use a snapshotting strategy — periodically save current entity state so you only replay events after the last snapshot, not the entire log. **Scaling guardrail:** The event log is the first collection that will outgrow a single node — it's append-only and never pruned. When it does, MongoDB's built-in sharding distributes `kg_events` across multiple servers. Partition by `entityId` so all events for a given entity stay co-located on the same shard, which means event replay and view materialization avoid scatter-gather queries. MongoDB includes a query analyzer that samples live traffic to help pick the right shard key — look for one that's non-monotonic (avoids hot shards) and has enough distinct values for even distribution.

### Step 9 — Hybrid Index (Text Search + Semantic Search + Graph Search)

The unified memory supports three search modes, all within MongoDB:

1. **Text Search:** MongoDB Atlas Search (built on Lucene) provides full-text search on `content` and `summary` fields — keyword matches like "vector databases" or "GraphRAG". Create Atlas Search indexes on the `kg_nodes` collection.

2. **Semantic Search:** Atlas Vector Search uses HNSW to find nodes by meaning. The query is embedded and compared against `summary_embedding` on Documents AND `content_embedding` on Tasks, Preferences, Episodes. A single `$vectorSearch` aggregation stage can combine vector similarity with metadata filters (e.g., `source_type`, `date` ranges).

3. **Graph Search:** MongoDB's `$graphLookup` aggregation stage performs recursive traversals across the `kg_nodes` collection using the `edges` array. For the 2–3 hop traversals standard in GraphRAG, MongoDB is highly competitive (sub-second for depth 1–3). Example: start from `person_arthur`, traverse `MENTIONS` edges to Documents, then `CONNECTED_TO` edges to linked Documents — all in one aggregation pipeline.

**MongoDB angle:** All three search modes hit the **same collection** in the **same database**. No cross-database joins, no sync lag, no consistency risks. This is the core value prop: hybrid search without polyglot persistence. **Workload isolation at scale:** As the knowledge graph grows, vector indexing and graph traversals will compete for the same compute resources — and the pressure shows up in parts of the application you don't expect, including writes that don't touch search at all. MongoDB lets you spin up dedicated search nodes that handle vector and text indexing independently from the operational cluster. You scale them separately — different instance sizes, different node counts — without rearchitecting anything. This matters for GraphRAG specifically because the hybrid search pattern (vector entry point → graph traversal) is read-heavy and bursty, while the memory pipeline (Steps 3–8) is write-heavy and continuous.

**Also mention Community Detection:** Runs as a periodic batch process (Louvain/Leiden) on the stored graph. Clusters densely connected nodes, generates LLM summaries per community, and writes summaries back as queryable documents in the same MongoDB collection. Used for global/top-down retrieval.

### Step 10 — Query View + Knowledge Graph

At query time, the system builds **views** from the immutable logs to get the latest state. MongoDB Views use aggregation pipelines to `$sort` events by timestamp, `$group` by entity ID, and `$last` to derive the current state.

The resulting **Knowledge Graph** is the queryable structure — Person nodes connected to Document nodes via MENTIONS, Documents linked to other Documents via CONNECTED_TO, Persons linked to Tasks/Preferences/Episodes via HAS/EXPERIENCED. All stored in MongoDB, all traversable via `$graphLookup`, all searchable via Atlas Vector Search and Atlas Search.

**Example from the presentation:** The cat vet query ("When and where should I go with my cats to the vet?") stitches together 8 facts from 4 silos — SMS (Mom's reminder) + GDrive (vaccination PDF) + Email (appointment confirmation) + Notion (clinic reviews) — all connected via CONNECTED_TO edges in MongoDB. Graph traversal via `$graphLookup` also uncovered facts invisible to vector search: "Mittens had a bad reaction at CheapVet" (Episode) and "Ask Felix for Oak St vet number" (Task) — reachable only through HAS/EXPERIENCED edges.

**MongoDB angle:** The view layer, the knowledge graph, and the hybrid index all live in the same Atlas cluster. `$graphLookup` with `maxDepth: 3` handles the multi-hop traversals. Vector search finds entry points. Text search catches exact keyword matches. One query pipeline, one database.

---

## Agent Layer

### Step 11 — MCP Server (Write Memory + Search Memory Tools)

The agent interacts with the unified memory through an MCP Server that exposes two tools:

- **Write Memory:** Triggers the ingestion pipeline (steps 3–8) to extract new KG Objects from a user conversation and append them as events to `kg_events`. The agent can update its own memory on-the-fly.
- **Search Memory:** Triggers the retrieval pipeline — hybrid search (text + semantic + graph via `$vectorSearch` + `$graphLookup`) across the `kg_nodes` collection, assembles the Minimum Viable Context (MVC), and returns grounded context to the agent.

**MongoDB angle:** Change Streams on `kg_events` can reactively trigger downstream processing (re-embedding, community detection updates) whenever the agent writes new memory. The MCP Server's tools are thin wrappers around MongoDB aggregation pipelines.

### Step 12 — Agent

The Digital Twin agent uses both tools dynamically in a ReAct loop (Think → Act → Observe → Repeat). This pattern is known as **Agentic GraphRAG**. The agent reads from and writes to the same MongoDB-backed knowledge graph, building a living memory that evolves with every interaction.

---

## Trade-offs Section (Brief, Honest)

End the post with a brief, honest trade-offs section. MongoDB is "powerful enough" for most agentic workloads:

- **Use unified MongoDB if:** Graph reasoning is bounded to 2–3 hops, primary workload is operational data + semantic search, and you value operational simplicity + unified security (Queryable Encryption for PII).
- **Consider adding a specialized DB if:** You exceed 100M–1B vectors with ultra-low latency needs, or core logic requires deep traversals (5+ hops) or pathfinding algorithms.

**What happens when the knowledge graph gets huge?** This is the question readers will have, so address it directly. MongoDB's horizontal scaling path is built in — not a bolt-on:
- **Sharding** distributes data across multiple servers by partitioning the primary key space. The database includes tooling to analyze live query patterns and recommend shard keys. With sharding, you go from terabytes to petabyte-scale and from thousands of operations to over a million.
- **Native resharding** lets you redistribute data across new shards with zero downtime — no maintenance windows, no big-bang migrations. If the `kg_events` collection becomes a hot spot, you can isolate it onto dedicated shards while the rest of the cluster continues serving reads uninterrupted.
- **Multi-cloud deployment** stretches a single Atlas cluster across providers (e.g., AWS + Azure + GCP in different regions). If a region or an entire cloud provider goes offline, the knowledge graph stays available. This also addresses data sovereignty requirements for agents handling PII across jurisdictions.
- **Horizontal autoscaling** (upcoming, currently in private preview) will automatically add shards and rebalance data under the hood — the same idea as the vertical autoscaling Atlas already provides, but going wide instead of tall.

The key point: the same MongoDB you start prototyping with is the same MongoDB that scales globally. No re-platforming step.

**MongoDB 8.0 stats to mention:** 36% faster reads, 32% faster mixed workloads vs 7.0, 50x faster resharding for horizontal scaling.

---

## Post Structure Summary

1. **Hook:** The synchronization tax of polyglot persistence — why managing separate DBs for docs, vectors, and graphs is painful
2. **Architecture diagram:** Reference the image, explain the 12 steps
3. **Data Pipeline (Steps 1–2):** Quick, set the stage
4. **Memory Pipeline (Steps 3–7):** The ingestion meat — cleaning, extraction, entity resolution, embedding, KG Objects. Use the Felix email example throughout.
5. **Unified Memory (Steps 8–10):** **THIS IS THE CORE.** Immutable logs, hybrid index (all three search modes in one DB), query views, knowledge graph. Use the cat vet example to show cross-silo stitching. Show MongoDB code snippets (`$graphLookup`, `$vectorSearch`, Change Streams, Views).
6. **Agent Layer (Steps 11–12):** MCP Server, Write/Search Memory, Agentic GraphRAG
7. **Trade-offs:** Honest, brief, builds trust
8. **CTA:** Link to MongoDB Atlas, Decoding AI course/newsletter

---

## MongoDB-Specific Details to Weave In

| Concept from Presentation | MongoDB Implementation |
|---|---|
| Knowledge Graph nodes | Documents in `kg_nodes` collection with `edges` array |
| Graph traversal (multi-hop) | `$graphLookup` aggregation stage (maxDepth: 3) |
| Semantic search (embeddings) | Atlas Vector Search with HNSW, `$vectorSearch` stage |
| Text search (keywords) | Atlas Search (Lucene-based), full-text indexes |
| Immutable logs | Append-only `kg_events` collection |
| Query-time views | MongoDB Views with `$sort` → `$group` → `$last` pipeline |
| Reactivity / triggers | Change Streams on `kg_events` |
| Entity resolution | `$match` + `$regex` on aliases arrays in same collection |
| Hybrid search | Single aggregation pipeline combining `$vectorSearch` + `$graphLookup` + Atlas Search |
| Community detection results | Stored as documents in same collection, queryable alongside nodes |
| Quantization for scale | MongoDB 8.0: Scalar (4x) and Binary (32x) quantization |
| Workload isolation | Dedicated Atlas Search Nodes |
| Atomic updates | `$set`, `$push`, `$inc` operators |
| Dynamic schema | BSON document model — no migrations when ontology evolves |
| Horizontal scaling | Built-in sharding — partition by `entityId`, use query analyzer for shard key selection |
| Zero-downtime capacity changes | Native resharding — redistribute data across new shards without production impact |
| Multi-cloud resilience | Single Atlas cluster stretched across AWS + Azure + GCP regions |
| Automatic horizontal scaling | Horizontal autoscaling (private preview) — Atlas adds shards and rebalances automatically |
