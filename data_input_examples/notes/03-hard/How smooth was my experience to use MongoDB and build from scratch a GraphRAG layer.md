# How smooth was my experience to use MongoDB and build from scratch a GraphRAG layer (local infra, text, semantic, graph search, ingestion, retrieval, writing code with claude code) (~2 days job)

## One database, three search modes: I built a full GraphRAG layer on MongoDB in 2 days

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | Building a GraphRAG system usually means stitching together a document store, a vector database, and a graph database — three separate systems with three APIs, three deployment configs, and glue code holding it all together. Most tutorials skip the infrastructure entirely and assume you have Atlas. If you want to run locally and own the full stack, you're on your own. |
| **Solution**    | Use MongoDB as the single database for everything: document storage (Beanie ODM), text search ($text), vector search ($vectorSearch via mongot Community Edition running locally), and graph traversal ($graphLookup). Three collections, one replica set, zero external services beyond the Gemini API. Docker Compose handles the local infra: MongoDB 8.2 + mongot + automatic replica set init. |
| **Transformation** | A fully local GraphRAG stack where ingestion, extraction, materialization, and hybrid retrieval (text + vector + graph) all run against one database. No Atlas account, no separate vector store, no graph database. The entire system — data pipelines, ontology-constrained extraction, immutable logs, materialized views, RRF-fused search, multi-hop graph expansion — shipped in ~2 days with Claude Code writing the bulk of the implementation. |
| **Hook**        | One database, three search modes: I built a full GraphRAG layer on MongoDB in 2 days. |
| **Target audience** | AI/ML engineers building RAG or GraphRAG systems who want to understand what MongoDB can actually do as a unified backend, developers evaluating local-first alternatives to Atlas, anyone curious how far a single database can go when you design the data model right. |

### Outline

1. The problem: GraphRAG usually means three databases (doc store + vector DB + graph DB). What if one database could do all three?
2. Local infrastructure: Docker Compose with MongoDB 8.2, mongot Community Edition, and automatic replica set initialization — fully local $vectorSearch without Atlas.
3. The three collections: documents (raw content), knowledge_graph_log (immutable observations), knowledge_graph (materialized query view) — and how they leverage MongoDB's strengths.
4. Text search: standard $text index on name, content, and aliases — the simplest search mode and the fallback.
5. Vector search: $vectorSearch via mongot, cosine similarity, 768-dimension embeddings — and the gotchas of running it locally (replica set requirement, mongot sync wait, index polling).
6. Graph traversal: $graphLookup for multi-hop expansion from seed nodes — why nodes and edges coexist in one collection, and how reverse edges enable bidirectional walking.
7. Tying it together: RRF fusion of text + vector results, then graph expansion. The full query pipeline in one database.
8. The development experience: how Claude Code + a clear system design made ~2 days realistic for the full stack (data pipelines, extraction, materialization, indexing, querying, visualization).

---

### Full body

#### The problem: three databases or one?

Most GraphRAG architectures look like this: PostgreSQL or MongoDB for document storage, Pinecone or Qdrant for vector search, Neo4j for graph traversal. Three databases, three connection strings, three deployment configs, and a service layer translating IDs between them.

I didn't want that. I wanted one database that handles document storage, text search, vector search, and graph traversal. MongoDB can do all four — but most people don't realize it because the tutorials either use Atlas (cloud-only features) or stop at basic CRUD.

Here's what I built: a full GraphRAG layer with three collections in one MongoDB instance, running entirely locally via Docker Compose. Text search, vector search, and graph traversal all hit the same database. The entire system — data pipelines, ontology-constrained extraction, immutable logs, materialized views, hybrid retrieval — shipped in about 2 days.

#### Local infrastructure: MongoDB + mongot via Docker Compose

The first surprise: you can run `$vectorSearch` locally without Atlas. MongoDB Community Edition 8.2 supports it through **mongot** — the community search process that syncs data from your replica set and provides vector search capabilities.

The Docker Compose setup has three services:

**MongoDB 8.2** — the database itself:
```yaml
mongodb:
  image: mongodb/mongodb-community-server:8.2.5-ubi9
  ports:
    - "${MONGO_PORT:-27017}:27017"
  volumes:
    - mongodata:/data/db
    - ./docker/mongodb/keyfile:/data/keyfile:ro
    - ./docker/mongodb/mongod.conf:/etc/mongod.conf:ro
  healthcheck:
    test: mongosh --eval "db.adminCommand('ping')"
    interval: 10s
    retries: 5
```

**mongodb-init** — one-shot container that initializes the replica set and creates the mongot user:
```javascript
// Replica set required for $vectorSearch
rs.initiate({ _id: "rs0", members: [{ _id: 0, host: "mongodb:27017" }] });

// mongot needs a user with searchCoordinator role
db.createUser({
  user: "mongot",
  pwd: "mongot",
  roles: [{ role: "searchCoordinator", db: "admin" }]
});
```

**mongot** — the search process that enables `$vectorSearch`:
```yaml
mongot:
  image: mongodb/mongodb-community-search:0.60.1
  ports:
    - "${MONGOT_PORT:-27028}:27028"
  volumes:
    - ./docker/mongot/config.yml:/mongot-community/config.default.yml:ro
    - ./docker/mongot/passwordFile:/etc/mongot/secrets/passwordFile:ro
```

The MongoDB config (`mongod.conf`) tells the database where to find mongot:
```yaml
replication:
  replSetName: rs0

setParameter:
  mongotHost: twin-mongot:27028
  searchIndexManagementHostAndPort: twin-mongot:27028
  useGrpcForSearch: true
```

`make local-start` brings up all three services. `make local-test` validates that text search, vector search, and graph traversal all work. The entire local stack is one command.

**Gotcha #1: Replica set is mandatory.** Even for a single-node local setup, `$vectorSearch` requires a replica set. A standalone MongoDB instance won't work. The init script handles this automatically, but if you're setting up manually, this will bite you.

**Gotcha #2: mongot sync takes time.** After creating a vector search index, mongot needs to sync the data. The code polls for up to 60 seconds:
```python
for _ in range(30):
    cursor = await collection.list_search_indexes(_VECTOR_INDEX_NAME)
    results = await cursor.to_list()
    if results:
        await asyncio.sleep(3)  # Extra time for mongot to sync
        return
    await asyncio.sleep(2)
```

In practice, on a local setup with small data, the sync completes in 5-10 seconds. But if your code tries to run `$vectorSearch` immediately after index creation, you'll get an empty result set with no error.

#### Three collections, three responsibilities

All three collections live in the same `twin` database:

**`documents`** — raw ingested content from data pipelines. Each document has a unique `source_uri` for idempotent ingestion. This is standard MongoDB document storage with Beanie ODM:

```python
class Document(BeanieDocument):
    source_type: SourceType
    source_uri: Indexed(str, unique=True)
    title: str | None
    content: str | None
    authors: list[str]
    date: datetime | None
    references: list[Link["Document"]]

    class Settings:
        name = "documents"
```

**`knowledge_graph_log`** — immutable, append-only observation log. Every entity and relationship extracted from a chunk becomes a separate document. Never modified, never deleted. This collection uses Beanie's polymorphic documents — `NodeLogEntry` and `EdgeLogEntry` share a base class with a `kind` discriminator:

```python
class KnowledgeGraphLogEntry(BeanieDocument):
    kind: Indexed(str)                      # "node" or "edge"
    properties: dict[str, Any]
    source_document_id: Indexed(PydanticObjectId)  # Provenance
    chunk_id: str                                   # Provenance
    created_at: datetime

    class Settings:
        name = "knowledge_graph_log"
        is_root = True  # Enables polymorphic queries
```

**`knowledge_graph`** — the materialized query view. Rebuilt from logs via MongoDB aggregation. Nodes and edges coexist in the same collection (required for `$graphLookup`). This is the collection that gets all three search indexes:

```python
class KnowledgeGraphEntry(BeanieDocument):
    id: Any                     # "type:name" for nodes, {source, target, type} for edges
    kind: Indexed(str)          # "node" or "edge"
    type: NodeType | EdgeType
    name: str | None            # Nodes only
    properties: dict[str, Any]
    embedding: list[float]      # Nodes only — for $vectorSearch

    class Settings:
        name = "knowledge_graph"
```

#### Search mode 1: Text search ($text)

The simplest search mode. A standard MongoDB text index on three fields:

```python
await collection.create_index(
    [
        ("name", "text"),
        ("properties.content", "text"),
        ("properties.aliases", "text"),
    ],
    name="text_index",
)
```

The query is a standard `$text` match with score:

```python
pipeline = [
    {"$match": {"kind": "node", "$text": {"$search": query}}},
    {"$addFields": {"_search_score": {"$meta": "textScore"}}},
    {"$sort": {"_search_score": -1}},
    {"$limit": top_k},
]
```

Text search is the fallback. If mongot is down or the vector index isn't ready, the system gracefully degrades to text-only search. It catches keywords, exact names, and aliases that vector search might miss.

#### Search mode 2: Vector search ($vectorSearch)

This is where mongot earns its keep. After materialization, every node gets an embedding vector (768 dimensions from Gemini's `text-embedding-004` model). The vector search index is created on the `embedding` field:

```python
await collection.create_search_index(
    model={
        "name": "vector_index",
        "type": "vectorSearch",
        "definition": {
            "fields": [{
                "type": "vector",
                "path": "embedding",
                "numDimensions": 768,
                "similarity": "cosine",
            }]
        },
    }
)
```

The query uses MongoDB's `$vectorSearch` aggregation stage:

```python
pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_vector,   # Embedded query text
            "numCandidates": top_k * 10,   # Oversampling for accuracy
            "limit": top_k,
            "filter": {"kind": "node"},    # Only search nodes, not edges
        }
    },
    {"$addFields": {"_search_score": {"$meta": "vectorSearchScore"}}},
]
```

Vector search captures semantic similarity — "MLOps best practices" matches nodes about "production ML deployment" even though the words don't overlap. It's the primary search mode for open-ended queries.

**Gotcha #3: $out destroys indexes.** The materialization pipeline uses `$out` to atomically replace the `knowledge_graph` collection. This drops all indexes, including the vector search index. Every materialization must be followed by `ensure_indexes()`:

```python
# The materialization pipeline
@flow(name="memory-materialization")
async def memory_materialization():
    await materialize_task(client, database)        # $out replaces collection
    await create_reverse_edges_task(client, database)
    await embed_nodes_task(client, database, model)  # Compute embeddings
    await ensure_indexes_task(client, database)       # Recreate ALL indexes
```

There's a TODO in the codebase to switch from `$out` to `$merge`, which would preserve indexes. But `$out` is simpler for now — and with small-to-medium data, the index rebuild takes seconds.

#### Search mode 3: Graph traversal ($graphLookup)

This is the mode that makes GraphRAG different from regular RAG. After finding seed nodes via text + vector search, the system walks edges to discover related entities.

`$graphLookup` requires that the nodes it traverses live in a single collection — that's why nodes and edges coexist in `knowledge_graph`. The traversal runs two passes:

```python
pipeline = [
    {"$match": {"kind": "node", "_id": {"$in": seed_node_ids}}},
    # Outgoing: seed._id → edge.source_node_id → follow edge.target_node_id
    {
        "$graphLookup": {
            "from": "knowledge_graph",
            "startWith": "$_id",
            "connectFromField": "target_node_id",
            "connectToField": "source_node_id",
            "as": "outgoing",
            "maxDepth": 2,  # max_hops - 1 (0-indexed)
            "restrictSearchWithMatch": {"kind": "edge"},
        }
    },
    # Incoming: reverse direction
    {
        "$graphLookup": {
            "from": "knowledge_graph",
            "startWith": "$_id",
            "connectFromField": "source_node_id",
            "connectToField": "target_node_id",
            "as": "incoming",
            "maxDepth": 2,
            "restrictSearchWithMatch": {"kind": "edge"},
        }
    },
    {"$project": {"edges": {"$setUnion": ["$outgoing", "$incoming"]}}},
]
```

The bidirectional traversal is enabled by reverse edges created during materialization. Not every edge type is bidirectional — only specific pairs:

```python
_BIDIRECTIONAL_PAIRS = {
    (NodeType.PERSON, NodeType.DOCUMENT),   # "who wrote this?" + "what did they write?"
    (NodeType.DOCUMENT, NodeType.PERSON),
    (NodeType.PERSON, NodeType.PERSON),     # mutual relationships
    (NodeType.DOCUMENT, NodeType.DOCUMENT), # cross-references
}
```

`PERSON → TASK`, `PERSON → EPISODE`, `PERSON → PREFERENCE` are intentionally one-directional.

**Gotcha #4: Edge deduplication with dict IDs.** Edge `_id`s are compound dicts (`{source_node_id, target_node_id, type}`). To deduplicate edges in Python, you can't just put dicts in a set. The code converts them to sorted tuples:

```python
raw_id = edge["_id"]
edge_key = tuple(sorted(raw_id.items())) if isinstance(raw_id, dict) else raw_id
if edge_key in seen_edge_ids:
    continue
seen_edge_ids.add(edge_key)
```

#### Tying it together: RRF fusion + graph expansion

The full query pipeline combines all three search modes:

**Step 1:** Run text search and vector search in parallel against `knowledge_graph`.

**Step 2:** Fuse results with Reciprocal Rank Fusion. For each document appearing in either list, compute `score = sum(1 / (k + rank + 1))` across both ranked lists:

```python
def _rrf_fuse(vector_results, text_results, *, k=60):
    fused = {}
    for rank, doc in enumerate(vector_results):
        doc_id = doc["_id"]
        if doc_id not in fused:
            fused[doc_id] = {"doc": doc, "score": 0.0}
        fused[doc_id]["score"] += 1.0 / (k + rank + 1)

    for rank, doc in enumerate(text_results):
        doc_id = doc["_id"]
        if doc_id not in fused:
            fused[doc_id] = {"doc": doc, "score": 0.0}
        fused[doc_id]["score"] += 1.0 / (k + rank + 1)

    return fused
```

RRF is deliberately simple — no learned weights, no tuning. It merges ranked lists robustly even when the score distributions are completely different (text scores vs cosine similarity).

**Step 3:** Take the top-k seed nodes by fused score.

**Step 4:** Expand the graph from seeds via `$graphLookup` (up to 3 hops by default).

**Step 5:** Hydrate all discovered nodes and return the subgraph.

All five steps hit the same `knowledge_graph` collection on the same MongoDB instance. One database, one connection, one round-trip per aggregation stage.

#### The development experience

The honest timeline: about 2 days of focused work, writing code with Claude Code.

**Day 1: Infrastructure + data pipelines + ontology + extraction.**
- Docker Compose setup (MongoDB 8.2 + mongot + replica set init) — mostly configuration, some debugging of the mongot sync.
- Data ETL for Substack RSS ingestion (fetch → parse → extract references → deduplicate → persist).
- Ontology design (6 node types, 8 edge types, Pydantic attribute schemas, edge constraints).
- Extraction pipeline (chunking → parallel LLM extraction → structural entries → fuzzy normalization → immutable log persistence).

**Day 2: Materialization + indexing + query layer + visualization.**
- Materialization aggregation pipeline (`$group` → `$mergeObjects` → `$unionWith` → `$out`).
- Embedding computation (post-materialization, batch processing).
- Reverse edge creation for bidirectional traversal.
- Text + vector index setup with mongot sync polling.
- Query layer (vector search, text search, RRF fusion, `$graphLookup` expansion).
- Visualization with NetworkX + pyvis.
- Prefect workflow wiring (@flow, @task wrappers).

What made this possible in 2 days:

1. **Clear system design.** I knew the three-collection architecture, the ontology, and the query pattern before writing code. The design came from studying the problem, trying LangChain first (and hitting its walls), and reading MongoDB's aggregation docs. Once the plan was clear, implementation was execution.

2. **MongoDB doing the heavy lifting.** The aggregation framework handles materialization (deduplication, property merging, ID composition). `$vectorSearch` handles semantic search. `$text` handles keyword search. `$graphLookup` handles graph traversal. I didn't build any of these — I configured them.

3. **Claude Code writing the implementation.** With the architecture clear in my head, I could describe what each function should do and Claude Code produced the implementation — the aggregation pipeline stages, the Beanie ODM models, the extraction prompt, the RRF fusion. The iteration cycle was fast: describe → generate → test → adjust.

4. **Prefect as thin orchestration.** I didn't build a workflow engine. Prefect's `@task(retries=2, retry_delay_seconds=5)` gave me fault tolerance. The monitoring dashboard gave me observability. All my business logic stays in pure functions that I can test without Prefect.

#### What MongoDB gave me

Let me be concrete about what MongoDB handled vs what I wrote:

| MongoDB did this | I wrote this |
|---|---|
| Document storage with unique indexes | Beanie ODM models (3 classes) |
| `$group` + `$mergeObjects` for deduplication | The aggregation pipeline stages |
| `$text` search across multiple fields | The text index definition (3 fields) |
| `$vectorSearch` with cosine similarity | The vector index definition + embedding computation |
| `$graphLookup` for multi-hop traversal | The bidirectional traversal strategy |
| `$out` for atomic collection replacement | The materialization flow (trigger + post-processing) |
| `$addToSet` for provenance tracking | The log entry schema |
| Replica set for durability | The Docker Compose config |
| mongot for local vector search | The mongot config + sync polling |

The aggregation framework is the unsung hero. One `$group` stage handles deduplication that would require a separate dedup service in a multi-database architecture. `$mergeObjects` combines properties from multiple observations without application-level merge logic. `$unionWith` merges nodes and edges into a single collection for `$graphLookup`. And `$out` writes the result atomically.

Is there a limit? Yes — `$out` drops the collection on every materialization, which forces index rebuilds. At millions of documents, switching to `$merge` (upsert in place, preserves indexes) becomes necessary. But for the current scale, and for getting a system working in 2 days, it's the right trade-off.

#### The bottom line

MongoDB handled five jobs that would normally require five systems: document storage, aggregation/materialization, text search, vector search, and graph traversal. The local setup with mongot Community Edition means no cloud dependency — everything runs on Docker Compose.

The ~2 day timeline was real because the infrastructure tools solved the hard problems (durable storage, vector indexing, graph traversal, workflow orchestration). What I built was the business logic layer on top: ontology design, extraction constraints, normalization, materialization pipeline design, query fusion strategy. That's the part that's specific to my domain — and it's the part that should live in my code, not behind a framework abstraction.

One database. Three collections. Three search modes. Zero framework lock-in.

## I built a GraphRAG system on MongoDB from scratch in 2 days — the CLAUDE.md I wrote before any code made it possible

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | Building a GraphRAG system feels like it requires Neo4j, LangChain, or a managed cloud service. The setup overhead is massive, the abstractions are leaky, and you spend more time configuring frameworks than writing retrieval logic. |
| **Solution**    | MongoDB Community Edition running locally via Docker — text search, vector search (via mongot), and graph search ($graphLookup) all on a single database. Prefect for orchestration with a Docker-composed server and worker. A 152-line handwritten CLAUDE.md file that gave Claude Code the full project context before writing a single line of code. |
| **Transformation** | A fully working GraphRAG pipeline — from RSS ingestion to interactive graph visualization — running locally with no cloud dependencies. The CLAUDE.md-first approach meant the coding agent understood the architecture, conventions, and constraints from line one, turning ~2 days of work into a complete system. |
| **Hook**        | I wrote 152 lines of documentation before a single line of code. Two days later I had a full GraphRAG system running on MongoDB. |
| **Target audience** | ML/AI engineers building RAG systems, developers curious about GraphRAG without Neo4j, anyone using coding agents (Claude Code, Cursor, etc.) for complex projects. |

### Outline

1. Open with the assumption that GraphRAG requires Neo4j or a managed service — and why that's wrong.
2. The CLAUDE.md-first approach: what I wrote, why I wrote it by hand, and how it shaped the entire development session.
3. The infrastructure stack: MongoDB Community Edition + mongot + Prefect, all Docker-composed and locally validated before writing app code.
4. The pipeline architecture: 4 Prefect deployments covering ingestion, extraction, materialization, and the query layer.
5. The three search pillars working together: text + vector → RRF fusion → $graphLookup expansion.
6. The bugs I hit and how each one taught me something about MongoDB's internals (DuplicateKeyError, silent query failures, $graphLookup depth limitation).
7. What made this a 2-day job instead of a 2-week job: the slim CLAUDE.md, Claude Code iterating through bugs in real time, and Docker Compose removing all infra friction.

---

### Full body

#### The starting point

I wanted to build a personal knowledge graph — a "digital twin" — that could ingest content from Substack RSS feeds, extract structured knowledge (people, documents, tasks, episodes, preferences, and the relationships between them), and let me query it using natural language with graph-aware retrieval. The full GraphRAG pipeline: ingest → extract → materialize → query → visualize.

My constraints: everything runs locally, no cloud dependencies, no managed services, no framework lock-in. I'd seen too many GraphRAG tutorials that required Neo4j, LangChain, and three different cloud accounts before you wrote your first query.

#### The CLAUDE.md — 152 lines, written by hand, before any code

Before writing a single line of Python, I wrote the CLAUDE.md file. 152 lines. Entirely by hand. Structured as three sections:

**The Why** — one sentence: "Build your digital twin through knowledge graphs, ontologies, memory, LLMs and agents."

**The What** — key components (data pipeline, memory pipeline, unified memory, agentic tools), project structure (folder tree with brief annotations), design choices (async Python, idempotent pipelines, UTC-aware dates, loose clean architecture), tech stack (every tool with its role), and test conventions (AAA pattern, parametrize, mocker fixtures).

**The How** — build/test/run commands via Make, development workflow (plan → implement → test → scan for bugs → suggest CLAUDE.md updates), and one critical line: `Use mongosh to interact with MongoDB directly through the CLI.`

This wasn't a template. Every line was there because the coding agent would need it. No auto-generated docs, no framework boilerplate. All signal, no noise. When Claude Code started working, it already knew:
- We use async Python with Beanie as the ODM
- Pipelines must be idempotent with retries and checkpointing
- Tests mirror the source structure one-to-one
- Make is the command center
- `mongosh` is available for direct database interaction
- Prefect is the orchestrator (with a link to its `llms.txt` sitemap for documentation)

This upfront investment — maybe 30 minutes of writing — saved hours of back-and-forth during development.

#### The infrastructure: Docker Compose with MongoDB + mongot + Prefect

The entire infrastructure stack runs via a single `docker compose up -d`:

**MongoDB** — `mongodb/mongodb-community-server:8.2.5-ubi9` with a replica set configuration. A companion `mongodb-init` container runs once to initialize the replica set and create the `mongot` user with the `searchCoordinator` role.

**mongot** — `mongodb/mongodb-community-search:0.60.1`, the community search container that enables `$vectorSearch` on Community Edition. This was the key discovery: you don't need Atlas for vector search anymore. mongot runs alongside MongoDB and syncs vector search indexes.

**Prefect server** — `prefecthq/prefect:3-latest` with the UI exposed on port 4200. Health-checked via a Python `httpx.get` call to the API.

**Prefect worker** — A custom Docker image built from the project's Dockerfile. It runs `uv run python -m twin.orchestrator`, which registers and serves all 4 workflow deployments. In development mode, you skip this container and run `make serve-workflows` locally so you can iterate without rebuilding.

Before writing any application code, I ran `make local-test` — a validation script (`test_mongodb_setup.py`) that seeds test data, creates text and vector indexes, and verifies all three search pillars work: `$text` queries, `$vectorSearch` pipelines, and `$graphLookup` traversal. Only after all three passed did I start building the actual pipelines.

#### The pipeline architecture: 4 Prefect deployments

The orchestrator (`src/twin/orchestrator.py`) is 40 lines. It registers 4 deployments using Prefect's `serve()`:

1. **`ingest-substack-rss-feed-etl`** — processes a single RSS feed URL
2. **`ingest-substack-rss-feed-batch-etl`** — processes multiple feeds in parallel via `asyncio.gather()`
3. **`memory-extraction-etl`** — extracts knowledge graph nodes and edges from documents using an LLM (Gemini)
4. **`memory-materialization-etl`** — rebuilds the materialized graph, creates reverse edges, embeds nodes, ensures indexes

Each pipeline follows the same pattern: Prefect `@flow` wraps the orchestration logic, `@task` wraps individual steps with retries and `cache_policy=NO_CACHE` (required when passing non-serializable objects like MongoDB clients). The core business logic lives in separate `core.py` files with zero Prefect dependencies — the pipeline files are thin wrappers that add retries, logging, and DB initialization.

Feed URLs are configured in `configs/default.yaml` under `sources.substack` — no more hardcoded CLI arguments. Scripts fall back to the config when no arguments are given.

The Prefect dashboard at `http://127.0.0.1:4200/dashboard` gives full visibility into every run: task states, timing, retries, parameters. During development, I had it open in a browser tab alongside the code.

#### Three collections, three search methods

**`documents`** — raw ingested content. Each document has a `source_type`, `source_uri` (unique), title, content, authors, date, and references. Deduplicated by `(source_type, source_uri)`.

**`knowledge_graph_log`** — immutable, append-only. Each entry is a single observation of a node or edge extracted from a specific chunk. Nodes have `name`, `type` (person/document/chunk/task/episode/preference). Edges have `source_node_id`, `target_node_id`, `type` (part_of/next/mentions/referenced/related_to/todo/experienced/has).

**`knowledge_graph`** — materialized via a MongoDB aggregation pipeline using `$group` → `$project` → `$unionWith` → `$out`. Nodes and edges coexist in the same collection with different `_id` formats: nodes use composite string IDs (`"person:paul_iusztin"`), edges use compound dict IDs (`{source_node_id, target_node_id, type}`).

Querying is two-phase:
1. **Search** — find seed nodes via `$text` (standard text index) and `$vectorSearch` (mongot), fused with Reciprocal Rank Fusion: `score = sum(1 / (k + rank))` across both result lists.
2. **Expand** — walk edges from seed nodes via two `$graphLookup` passes (outgoing + incoming), merged with `$setUnion` for bidirectional traversal.

The result gets rendered as an interactive HTML graph using networkx + pyvis.

#### The bugs and what they taught me

**DuplicateKeyError** — Materialization crashed because the `$project` stage set `_id: "$_id.name"`, dropping the node type. "opik" existed as both a person and a preference. Fix: composite IDs via `{"$concat": ["$_id.type", ":", "$_id.name"]}`.

**Silent query failures** — Every query returned zero results, no errors. Three stacked bugs: (1) `$out` dropped the collection and all indexes on every materialization, (2) text search used `$search` (Atlas Search syntax) instead of `$text` (Community Edition syntax), (3) both search paths had `except Exception: return []`. The fix was already in `test_mongodb_setup.py`.

**$graphLookup depth limitation** — Expected 56 nodes at 3 hops, got 6. `$graphLookup` chains edge→edge in a single collection but can't cross through node documents. Fixed by creating reverse edge copies (with `direction: "reverse"`) for specific node-type pairs: person↔document, person↔person, document↔document. Not all types need bidirectional traversal — tasks, episodes, and preferences are directional by nature.

#### Why it was a 2-day job

Three things made this fast:

1. **The CLAUDE.md** — 152 lines of handwritten context meant zero ramp-up time for the coding agent. No "what framework are we using?" No "where do tests go?" No "how do I run this?" Everything was answered before it was asked.

2. **Docker Compose** — one command for all infrastructure. MongoDB with replica set, mongot for vector search, Prefect server, Prefect worker. No manual database setup, no service management.

3. **Claude Code iterating through bugs in real time** — each bug (DuplicateKeyError, silent failures, $graphLookup limitation) was discovered, diagnosed, and fixed within the same development session. The agent could run `mongosh` to inspect the database, run the pipeline, read the error, propose a fix, and verify — all in a loop.

[VERIFY] The "2 days" timeline is the user's stated estimate — verify exact elapsed time if the user wants to be precise in the post.
