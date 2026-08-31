# Agentic GraphRAG via MCP Servers

Building a GraphRAG FastMCP server. 

- What tools it needs and how they should be design to search/write to the memory
- How to hook it to a harness such as Claude Code or OpenCode

## Agentic GraphRAG Architecture Report

> Comprehensive E2E technical report for blog/LinkedIn content about building a digital twin with knowledge graphs, FastMCP, and Claude Code.

---

### 1. Data Pipelines (ETL Layer)

**Purpose:** Gather content from multiple sources, normalize it into a unified `documents` MongoDB collection.

#### Architecture

All pipelines inherit from `BaseETL` (`src/twin/data/core/base.py`), which defines the contract:
- `extract_one(raw_entry) -> Document` -- transform raw data
- `run(source_uri) -> list[Document]` -- fetch, extract, persist
- `run_batch(source_uris)` -- process multiple sources

Each pipeline is orchestrated via **Prefect flows** with retry logic and task-level checkpointing.

#### Supported Sources (5 pipelines)

| Source | Pipeline File | Fetch Method | Key Detail |
|--------|--------------|-------------|------------|
| **Substack RSS** | `data/substack/substack_rss.py` | `httpx` + `feedparser` | Parses RSS XML, extracts HTML content, converts to plain text via BeautifulSoup |
| **Substack Articles** | `data/substack/substack_article.py` | Direct HTTP GET | Scrapes `og:title`, `og:description`, `article:published_time` from meta tags; extracts body from `div.body` or `<article>` |
| **ArXiv (HuggingFace)** | `data/huggingface/arxiv_dataset.py` | HuggingFace `datasets` streaming API | Streams `librarian-bots/arxiv-metadata-snapshot`; optional HTML content fetch from `arxiv.org/html/` |
| **Local Files** | `data/file.py` | Filesystem read | Supports `.txt`, `.md`, `.html`; HTML auto-converted to plain text |
| **Conversations** | `data/conversation.py` | Direct text input | UUID-based `source_uri`; always unique (no dedup) |

#### Document Data Model (`src/twin/entities/documents.py`)

```python
class Document(BeanieDocument):
    source_type: SourceType        # SUBSTACK | HUGGINGFACE | FILE | CONVERSATION | LATENT
    source_uri: Indexed(str, unique=True)  # Deduplication key
    title: str | None
    summary: str | None
    content: str | None
    authors: list[str] = []
    date: datetime | None          # Always timezone-aware (UTC)
    references: list[Link["Document"]] = []  # Citation graph
```

#### Key Design Patterns

- **Deduplication via `source_uri`**: Unique index prevents re-ingestion
- **LATENT documents**: When Article A references URL B that hasn't been ingested yet, a placeholder LATENT document is created for B. When B is later ingested, the LATENT is upgraded with real content
- **Reference graph**: `references` field tracks cross-document citations, forming an implicit citation network before graph extraction even runs
- **Idempotent upserts**: Re-running a pipeline on the same source is safe

#### URL Ingestion Router (`data/core/ingest.py`)

Registry-based dispatcher that routes URLs to the correct pipeline automatically. Static patterns (e.g., `substack.com`) plus custom domains from config. This is what the MCP `ingest_url` tool uses under the hood.

---

### 2. Memory Extraction Pipeline

**Purpose:** Transform raw `documents` into a structured knowledge graph of nodes and edges in the `knowledge_graph` collection.

**File:** `src/twin/memory/extraction/core.py`  
**Prefect flow:** `src/twin/memory/extraction/pipeline.py`

#### 5-Stage Pipeline

```
Document.content
    |
    v
[1] chunk_document()          -- Split into 512-token chunks (64-token overlap, tiktoken cl100k_base)
    |
    v
[2] extract_entities()        -- LLM (Gemini) extracts nodes & edges from each chunk (5 concurrent)
    |                            System prompt includes full ontology schema as JSON
    |                            Returns: person, task, episode, preference nodes
    |                            Returns: related_to, todo, experienced, has edges
    v
[3] build_structural_entries() -- Deterministic (no LLM):
    |                              DOCUMENT node for the source
    |                              CHUNK nodes for each text chunk (with full text in properties.content)
    |                              PART_OF edges: chunk -> document
    |                              NEXT edges: chunk[i] -> chunk[i+1] (sequential ordering)
    |                              MENTIONS edges: document -> person
    |                              REFERENCED edges: document -> document (from references list)
    v
[4] normalize_nodes()         -- Two-phase deduplication:
    |                            Phase A (in-memory): Fuzzy match via SequenceMatcher (threshold 0.85)
    |                            Phase B (cross-document): Query MongoDB for existing nodes, merge
    |                            Edge remapping: Update endpoints to canonical names
    v
[5] upsert_graph_entries()    -- Bulk upserts with MongoDB aggregation pipeline updates
                                 Merges properties (new wins), unions sources array, unions aliases
                                 Idempotent: running twice produces the same result
```

#### Ontology Schema (`src/twin/entities/ontology.py`)

**Node types (6):**
| Type | Properties | LLM-Extractable? |
|------|-----------|-------------------|
| `document` | source_type, source_uri, date | No (structural) |
| `chunk` | source_type, source_uri, content, date | No (structural) |
| `person` | aliases, email | Yes |
| `task` | content, date | Yes |
| `episode` | content, date | Yes |
| `preference` | content | Yes |

**Edge types (8):**
| Type | Source -> Target | LLM-Extractable? |
|------|-----------------|-------------------|
| `part_of` | chunk -> document | No (structural) |
| `next` | chunk -> chunk | No (structural) |
| `mentions` | document -> person | No (structural) |
| `referenced` | document -> document | No (structural) |
| `related_to` | person -> person | Yes |
| `todo` | person -> task | Yes |
| `experienced` | person -> episode | Yes |
| `has` | person -> preference | Yes |

**Edge constraints** are enforced programmatically -- the LLM can't create an edge that violates the ontology (e.g., a `todo` edge from `episode` to `document`).

---

### 3. Knowledge Graph Data Model

**Collection:** Single `knowledge_graph` MongoDB collection  
**File:** `src/twin/entities/knowledge_graph.py`

#### Single-Collection Design

Nodes and edges coexist in one collection, discriminated by the `kind` field:

**Node document:**
```json
{
  "_id": "person:paul iusztin",       // Composite string ID: "type:name"
  "kind": "node",
  "type": "person",
  "name": "paul iusztin",
  "properties": {"aliases": ["paul"], "email": null},
  "embedding": [0.12, -0.34, ...],    // 384-dim vector (empty until indexed)
  "sources": [ObjectId("...")],        // Which documents contributed this node
  "created_at": "2025-...",
  "updated_at": "2025-..."
}
```

**Edge document:**
```json
{
  "_id": "person:paul iusztin|todo|task:write blog post",  // "source|type|target"
  "kind": "edge",
  "type": "todo",
  "source_node_id": "person:paul iusztin",
  "source_type": "person",
  "target_node_id": "task:write blog post",
  "target_type": "task",
  "properties": {},
  "sources": [ObjectId("...")],
  "created_at": "2025-...",
  "updated_at": "2025-..."
}
```

#### Why Single Collection?

This enables MongoDB's `$graphLookup` for multi-hop traversal within one collection, simplifies indexing (one text index, one vector index), and enables atomic upserts with composite string IDs that are human-readable and deterministic.

---

### 4. Indexing Pipeline

**Purpose:** Generate embeddings for all nodes and create search indexes.  
**File:** `src/twin/memory/indexing/core.py`  
**Prefect flow:** `src/twin/memory/indexing/pipeline.py`

#### Step 1: Node Embedding (`embed_nodes()`)

- Finds all nodes where `embedding` is empty (`[]` or `None`)
- Builds a text representation per node:
  ```
  {type}: {_id}
  {property_key}: {property_value}
  {content}   // appended last if present
  ```
- Batch processing (default 64 nodes per batch)
- Embedding model: Sentence Transformers `all-MiniLM-L6-v2` (384 dimensions, runs locally)

#### Step 2: Search Index Creation (`ensure_indexes()`)

Creates **two indexes** on the `knowledge_graph` collection:

1. **Text Index** (standard MongoDB):
   - Fields: `name`, `properties.content`, `properties.aliases`
   - Enables `$text` queries for keyword/word-level search

2. **Vector Search Index** (MongoDB Atlas / `mongot`):
   - Field: `embedding`
   - Similarity: `cosine`
   - Dimensions: 384
   - Waits up to 60s for `mongot` to sync

---

### 5. Query Logic (3 Strategies)

**Files:** `src/twin/memory/query/core.py`, `src/twin/memory/query/nl_query.py`

#### Strategy 1: Hybrid Search + Graph Expansion (`search_memory`)

**Two-phase retrieval:**

**Phase 1 -- Seed Node Discovery (`search_nodes()`):**
- **Vector search**: `$vectorSearch` aggregation stage on `vector_index`, cosine similarity
- **Text search**: `$text` operator on the text index (word-level, stemmed)
- **RRF Fusion**: Reciprocal Rank Fusion combines both rankings:
  ```
  score(doc) = sum(1 / (k + rank + 1)) across all result lists
  ```
  Default `k=60`. No absolute weighting -- purely rank-based fusion.

**Phase 2 -- Graph Expansion (`expand_graph()`):**
- Bidirectional `$graphLookup` from seed nodes:
  - Outgoing: node._id -> edge.source_node_id -> follow edge.target_node_id
  - Incoming: node._id -> edge.target_node_id -> follow edge.source_node_id
- Configurable depth (default 1 hop)
- Deduplicates edges, hydrates all discovered nodes
- Returns `QueryResult(nodes, edges)`

#### Strategy 2: Natural Language Query (`query_memory`)

- LLM (Gemini) translates natural language to a MongoDB aggregation pipeline
- System prompt is **dynamically generated** from the ontology registries -- includes all node types, edge types, constraints, index info, and vector search syntax
- Uses an `__EMBED__` placeholder that gets replaced with actual embedding vectors at execution time

**Safety validation (`validate_pipeline()`):**
- Whitelist of 19 allowed aggregation stages
- Blocks all write operations (`$out`, `$merge`, `$delete`, `$drop`, etc.)
- `$lookup`/`$graphLookup` must target `knowledge_graph` collection only
- Auto-injects `$limit` if missing
- Strips `embedding` field from output

**Self-correction:** On pipeline validation or execution error, feeds the error back to the LLM for a retry (default 1 retry).

#### Strategy 3: Deep Search (`deep_search_memory`)

- Broad exploration with larger defaults (`top_k=50`, `max_hops=3`)
- **Progressive disclosure**: Writes individual markdown files per node/edge to `.twin/{session_id}/`
- Returns a lightweight **YAML index** with one-line summaries
- Claude Code reads individual files on-demand based on the index

---

### 6. Building the GraphRAG FastMCP Server

**Framework:** FastMCP  
**File:** `src/twin/mcp/server.py`  
**Entry point:** `scripts/serve_mcp.py`

#### Why MCP?

The Model Context Protocol (MCP) is a standard for connecting AI assistants to external tools and data sources. Instead of baking knowledge graph access into a single monolithic agent, MCP lets you build the memory as a **standalone server** that any MCP-compatible harness (Claude Code, OpenCode, Cursor, Windsurf, etc.) can connect to. The server exposes tools over a JSON-RPC protocol, and the harness discovers and calls them naturally during conversation.

This means the same knowledge graph can serve multiple agents, multiple interfaces, and multiple use cases -- without rewriting any integration code.

#### Server Architecture

The MCP server is a thin orchestration layer. It owns **zero** business logic. Every tool handler delegates to existing business logic modules:

```
src/twin/mcp/
    server.py          # FastMCP instance + lifespan (DB, models, indexes)
    tools.py           # 6 tool handlers (thin delegation)
    ingest.py          # Inline ingestion orchestrator (extraction + indexing)
    deep_search.py     # Progressive disclosure (writes results to disk)
```

This separation is deliberate. The MCP layer is a **delivery mechanism**, not a logic layer. The same extraction, indexing, and query logic runs identically whether triggered by an MCP tool call or a Prefect batch pipeline. This means:
- Business logic is tested independently of the MCP framework
- You can swap FastMCP for another MCP framework without touching query/ingestion code
- Batch pipelines and real-time MCP calls share the same code paths

#### Lifespan: Dependency Initialization

FastMCP's lifespan pattern solves a critical problem: **expensive resources** (database connections, ML models) should be initialized once at startup, not per-request. The lifespan yields a context dictionary that every tool handler receives:

```python
@lifespan
async def app_lifespan(server: FastMCP) -> AsyncGenerator[dict[str, Any], None]:
    # 1. Connect to MongoDB (async driver, timezone-aware)
    client = await init_mongodb(settings.mongo.mongo_uri.get_secret_value(), database)
    
    # 2. Load models (once, reused across all tool calls)
    llm = get_llm()                    # Gemini 2.5 Flash Lite
    embedding_model = get_embedding_model()  # Sentence Transformers (local)
    
    # 3. Ensure search indexes exist (text + vector)
    await ensure_indexes(client, database)
    
    # 4. Yield shared context to all tool handlers
    yield {"client": client, "database": database, "llm": llm, "embedding_model": embedding_model}
    
    # 5. Cleanup on shutdown
    await client.close()
```

Every tool handler accesses these via `ctx.lifespan_context`:
```python
@mcp.tool
async def search_memory(query: str, ctx: Context, ...) -> str:
    lc = ctx.lifespan_context
    result = await structured_query_memory(
        client=lc["client"], database=lc["database"],
        query=query, embedding_model=lc["embedding_model"], ...
    )
```

#### Server Instructions

The `FastMCP` constructor takes an `instructions` string -- a natural language description of the server's purpose that the harness surfaces to the AI model. This is how the model learns **what the server does** before seeing individual tool schemas:

```python
mcp = FastMCP(
    "Twin Memory",
    instructions=(
        "Query and build a personal knowledge graph of documents, people, tasks, "
        "episodes, and preferences. Use 'query_memory' for flexible natural language "
        "queries. Use 'search_memory' as a reliable fallback for semantic similarity search. "
        "Use 'deep_search_memory' for broad exploration — it saves results to disk and "
        "returns a lightweight index; read individual files for details. "
        "Use 'ingest_url' to add web content, 'ingest_file' for local files, "
        "and 'ingest_conversation' to extract knowledge from conversations."
    ),
    lifespan=app_lifespan,
)
```

#### Tool Registration Pattern

Tools are registered via the `@mcp.tool` decorator in a separate `tools.py` file, imported at the bottom of `server.py`:

```python
# server.py — bottom of file
import twin.mcp.tools  # noqa: E402, F401 — registers tools on `mcp`
```

This import side-effect pattern keeps `server.py` focused on infrastructure (lifespan, config) while `tools.py` owns all tool definitions. FastMCP reads each tool's **function signature** (parameter names, types, defaults) and **docstring** (description, arg docs) to auto-generate the MCP tool schema that the harness sees.

#### Entry Point

The entry point is minimal -- just logging setup and `mcp.run()`:

```python
# scripts/serve_mcp.py
from twin.logging import init_logger
init_logger()

from twin.mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
```

`mcp.run()` starts the server on the configured transport (stdio by default). The server blocks until the harness closes the connection.

---

### 7. MCP Tool Design: Search + Write

**File:** `src/twin/mcp/tools.py`

#### Design Principle: Tools as Thin Delegates

Every MCP tool follows the same pattern:
1. **Extract** lifespan context (`ctx.lifespan_context`)
2. **Delegate** to a business logic function
3. **Serialize** the result (strip embeddings, convert BSON types)
4. **Return** a string (MCP tools always return strings)

No tool contains business logic. No tool directly queries MongoDB. This makes tools trivially testable and keeps the MCP layer swappable.

#### Search Tools (3): Reading from Memory

##### Tool 1: `search_memory` -- The Default

```python
@mcp.tool
async def search_memory(
    query: str, ctx: Context,
    top_k: int = 10, max_hops: int = 1, max_results: int = 10, visualize: bool = False,
) -> str:
    """Search the knowledge graph using semantic + text search with graph expansion."""
```

**Why it's the default:** It's the most forgiving tool. It combines vector similarity and text search via RRF fusion, then expands the graph around seed nodes. Even vague queries return useful results because the hybrid search catches both semantic meaning (vector) and exact keywords (text).

**Design decisions:**
- `top_k=10`: Number of seed nodes from the initial search. Higher values cast a wider net but return more noise.
- `max_hops=1`: Graph expansion depth. 1 hop gets directly connected entities. 2+ hops can explode in dense graphs.
- `max_results=10`: Hard cap on returned documents. Critical for preventing context window overflow in the harness.
- `visualize=False`: Optionally renders an interactive HTML graph and opens it in the browser. Useful for spatial understanding but adds latency.

**Return format:** Serialized JSON via `bson.json_util.dumps` (handles `ObjectId`, `datetime`). Embedding vectors are **always stripped** -- they're large float arrays that waste tokens and provide no human-readable value.

##### Tool 2: `query_memory` -- Structured Precision

```python
@mcp.tool
async def query_memory(
    query: str, ctx: Context,
    visualize: bool = False, max_results: int = 10,
) -> str:
    """Query the knowledge graph using natural language."""
```

**Why it exists separately:** `search_memory` can't do aggregations ("how many tasks does Paul have?"), exact filters ("show me all episodes from January"), or complex graph traversals ("find all people 2 hops from Paul who have tasks"). `query_memory` translates natural language to a MongoDB aggregation pipeline via the LLM, giving it the full expressive power of MongoDB's query language.

**Design decisions:**
- No `top_k` or `max_hops` params -- the LLM decides the query shape based on intent
- Safety validation whitelist prevents write operations
- Self-correction: on pipeline error, feeds the error back to the LLM for a retry
- `__EMBED__` placeholder pattern lets the LLM use vector search without knowing embedding dimensions

##### Tool 3: `deep_search_memory` -- Progressive Disclosure

```python
@mcp.tool
async def deep_search_memory(
    query: str, ctx: Context,
    top_k: int = 50, max_hops: int = 3, session_id: str | None = None,
) -> str:
    """Broad search across the knowledge graph with progressive disclosure."""
```

**Why it exists:** Large knowledge graphs can return hundreds of nodes and edges for a broad query. Dumping all of that into the harness context window wastes tokens and confuses the model. Deep search solves this with **progressive disclosure**:

1. Runs an expanded search (50 seeds, 3 hops -- much wider than `search_memory`)
2. Writes **individual markdown files** per node/edge to `.twin/{session_id}/`
3. Returns a **YAML index** with one-line summaries:
   ```yaml
   results:
     - id: "person:paul iusztin"
       kind: node
       type: person
       name: paul iusztin
       file: person-paul_iusztin.md
       context: "person: paul iusztin — aliases: paul"
     - id: "person:paul iusztin|todo|task:build harness"
       kind: edge
       type: todo
       source: "person:paul iusztin"
       target: "task:build harness"
       file: person-paul_iusztin--todo--task-build_harness.md
       context: "person:paul iusztin —[todo]→ task:build harness"
   ```
4. The harness reads individual files on-demand using the `Read` tool

This pattern keeps the context window lean while giving the model access to the full result set.

**Design decisions:**
- `top_k=50` and `max_hops=3`: Much wider than `search_memory` defaults -- this is for exploration, not precision
- Files written as markdown with YAML frontmatter -- human-readable and tool-friendly
- `session_id` allows reusing results across turns without re-running the search
- Slugified filenames from `_id` strings (`person:paul iusztin` -> `person-paul_iusztin.md`)
- Long slugs truncated with SHA-256 suffix for uniqueness

#### Write Tools (3): Writing to Memory

##### Tool 4: `ingest_url` -- Web Content

```python
@mcp.tool
async def ingest_url(url: str, ctx: Context) -> str:
    """Fetch a web page and ingest its content into the knowledge graph."""
```

**Design decisions:**
- Routes URLs through a registry-based dispatcher (`data/core/ingest.py`) that matches URL patterns to pipelines
- Handles deduplication: if the URL was already ingested, returns `{"status": "already_ingested"}`
- Structured error responses for network errors, HTTP errors, and unsupported URLs -- the harness can act on these
- Runs the **full pipeline inline** after data ingestion: extraction + indexing in one call
- Returns node/edge counts so the harness can confirm what was extracted

##### Tool 5: `ingest_file` -- Local Files

```python
@mcp.tool
async def ingest_file(file_path: str, ctx: Context, title: str | None = None) -> str:
    """Read a local file and ingest its content into the knowledge graph."""
```

**Design decisions:**
- Supports `.txt`, `.md`, `.html` (HTML auto-converted to plain text)
- Graceful error handling for filesystem errors (`FileNotFoundError`, `IsADirectoryError`, `PermissionError`)
- Optional `title` override -- defaults to filename

##### Tool 6: `ingest_conversation` -- Conversation Text

```python
@mcp.tool
async def ingest_conversation(conversation_text: str, ctx: Context, title: str | None = None) -> str:
    """Extract knowledge from a conversation and add it to the knowledge graph."""
```

**Design decisions:**
- Validates non-empty input before processing
- Each conversation gets a UUID-based `source_uri` (always unique, no dedup)
- This is the tool that the Stop hook triggers at session end -- it extracts people, tasks, episodes, and preferences from the conversation

#### Inline Ingestion Pipeline (`src/twin/mcp/ingest.py`)

All three write tools call `run_ingestion_pipeline()` after creating the `Document`. This function runs the **full memory pipeline inline** -- not via Prefect:

```python
async def run_ingestion_pipeline(document, *, client, database, llm, embedding_model):
    # 1. Resolve reference URIs from the Document
    reference_uris = [ref.source_uri for ref in document.references if isinstance(ref, Document)]
    
    # 2. Extract: chunk + LLM extract + structural entries + normalize + upsert
    result = await extract_and_store(llm, document_id=document.id, content=document.content, ...)
    
    # 3. Index: embed new nodes
    await embed_nodes(client, database, embedding_model)
    
    # 4. Return summary
    return {"status": "ingested", "nodes_extracted": len(result.nodes), "edges_extracted": len(result.edges), ...}
```

**Why inline instead of Prefect?** MCP tool calls are synchronous from the harness perspective -- the user is waiting for a response. Dispatching to Prefect would mean the content isn't queryable until the async pipeline completes. Inline execution means a single `ingest_url` call goes from raw URL to **queryable knowledge graph** in one step.

#### Serialization Design

Two helpers handle all output formatting:

```python
def _serialize(docs: list[dict]) -> str:
    """Strip embeddings, serialize with bson.json_util for ObjectId/datetime support."""
    cleaned = [{k: v for k, v in doc.items() if k != "embedding"} for doc in docs]
    return json_util.dumps(cleaned, indent=2)

def _visualize(docs: list[dict]) -> str:
    """Build networkx graph from nodes/edges, render as interactive HTML via pyvis."""
```

**Key design choice:** Embeddings are always stripped before returning to the harness. A 384-dim float array per node wastes ~1500 tokens and provides zero value to the model or user.

---

### 8. Skills: Teaching the Harness When to Use Each Tool

**File:** `.claude/skills/twin-memory/SKILL.md`

#### What is a Skill?

A skill is a markdown file that provides **structured guidance** to the AI model inside the harness. When the user invokes `/twin-memory <query>`, the skill content is injected into the model's context alongside the MCP tool schemas. Skills bridge the gap between "the tool exists" and "the model knows when and how to use it well."

Without skills, the model relies only on tool docstrings -- which describe **what** each tool does, but not **when** to pick one over another, or **how** to present results to the user.

#### Skill Structure

The skill has four sections that guide the model's behavior:

##### 1. Reading Strategy (Decision Tree)

```
Is the query structured/precise (counts, filters, aggregations)?
  → YES: Use `query_memory`
  → NO: Is the query broad/exploratory (map connections, comprehensive context)?
    → YES: Use `deep_search_memory` (progressive disclosure)
    → NO: Use `search_memory` (default -- most forgiving)
```

- **`search_memory`** -- "Start here when unsure." The hybrid search is tolerant of vague queries.
- **`query_memory`** -- For questions that need MongoDB's full aggregation power: counts, date filters, specific lookups.
- **`deep_search_memory`** -- For broad exploration. The skill teaches the **progressive disclosure workflow**:
  1. Call `deep_search_memory("topic")` -- get the YAML index
  2. Scan `context` fields to identify relevant entries
  3. Use `Read` tool on individual file paths for full details
  4. Summarize findings for the user

##### 2. Writing Strategy

- **`ingest_url`** -- When user shares a URL
- **`ingest_file`** -- When user wants to add a local file
- **`ingest_conversation`** -- At end of session or when user wants to persist learnings

##### 3. Presentation Guidelines

- Summarize results in human-readable format (never dump raw JSON)
- Group by entity type (people, tasks, episodes, documents)
- Highlight relationships and connections between entities
- For deep search: present index summary first, offer to dive deeper
- For ingestion: report what was created (document title, node count, edge count)

##### 4. Knowledge Graph Reference

Quick reference of all node types (6), edge types (8), and source types (5) so the model can construct meaningful queries and interpret results without guessing.

#### Why Skills Matter

Tools alone tell the model **what it can do**. Skills tell it **what it should do** in context. Consider the difference:

| Without skill | With skill |
|--------------|-----------|
| Model sees 6 tools with docstrings | Model knows `search_memory` is the default, `query_memory` is for precision |
| Model dumps raw JSON to user | Model groups by entity type and highlights relationships |
| Model calls `search_memory` for "how many tasks?" | Model calls `query_memory` which can generate `$count` pipelines |
| Model returns all deep search results at once | Model scans YAML index, reads only relevant files |

---

### 9. Hooking the MCP Server to a Harness (Claude Code, OpenCode, etc.)

#### What is a Harness?

A harness is any MCP-compatible host that connects to MCP servers and exposes their tools to an AI model. Examples: Claude Code, OpenCode, Cursor, Windsurf, Cline, Continue. The MCP server doesn't know or care which harness is connected -- it speaks the MCP protocol and returns results.

#### Connection: `.mcp.json`

The harness discovers MCP servers via a `.mcp.json` file at the project root:

```json
{
  "mcpServers": {
    "twin-memory": {
      "command": "uv",
      "args": ["run", "python", "scripts/serve_mcp.py"],
      "env": { "ENV_FILE_PATH": ".env" }
    }
  }
}
```

**How it works:**
1. The harness reads `.mcp.json` when it starts or opens a project
2. It spawns each server as a **subprocess** using the specified `command` and `args`
3. Communication happens over **stdio** (JSON-RPC messages on stdin/stdout)
4. The harness calls `tools/list` to discover all 6 tools with their schemas
5. The harness calls `tools/call` when the model wants to use a tool

**Why stdio?** It's the simplest transport -- no ports, no networking, no auth. The harness owns the server's lifecycle (start on open, kill on close). For remote deployment, FastMCP also supports SSE transport (`mcp.run(transport="sse")`), which the `Makefile` exposes via `make serve-mcp TRANSPORT=sse`.

#### Claude Code Integration (3 Layers)

Claude Code connects to the MCP server through three complementary layers:

##### Layer 1: MCP Server (`.mcp.json`)

The base connection. Claude Code spawns the server, discovers 6 tools, and can call them during conversation. This works out-of-the-box with zero additional config.

##### Layer 2: Skills (`.claude/skills/twin-memory/SKILL.md`)

Skills are a **Claude Code-specific** feature (not part of the MCP protocol). When the user types `/twin-memory <query>`, the skill content is injected into the model's context. The skill teaches the model:
- Which tool to pick for which query type
- How to present results to the user
- The progressive disclosure workflow for deep search

Other harnesses (OpenCode, Cursor) don't have skills -- they rely on tool docstrings and server instructions alone. This means the same MCP server works everywhere, but Claude Code gets a **richer experience** because the model has more guidance on tool selection and result presentation.

##### Layer 3: Hooks (`.claude/settings.json`)

Hooks are another **Claude Code-specific** feature. They run shell commands in response to lifecycle events. The `Stop` hook auto-ingests conversations:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "SESSION_ID=$(jq -r '.session_id // empty'); SENTINEL=\"/tmp/.claude-twin-ingested-${SESSION_ID}\"; if [ -f \"$SENTINEL\" ]; then echo '{}'; else touch \"$SENTINEL\"; echo '{\"decision\":\"block\",\"reason\":\"Please run: /twin-memory extract current conversation\"}'; fi",
        "timeout": 5
      }]
    }]
  }
}
```

**How it works:**
1. Claude Code fires the Stop hook when the model finishes a response
2. The hook checks for a sentinel file at `/tmp/.claude-twin-ingested-{SESSION_ID}`
3. **First time this session:** No sentinel file exists -> hook returns `"decision": "block"` with the message "Please run: /twin-memory extract current conversation"
4. Claude Code shows this message to the model, which then invokes the `ingest_conversation` tool
5. **Subsequent turns:** Sentinel file exists -> hook passes through silently

This creates a **self-sustaining feedback loop**: every coding session automatically enriches the knowledge graph with new people, tasks, episodes, and preferences discussed in conversation.

#### Connecting to Other Harnesses (OpenCode, Cursor, Windsurf)

The MCP server works with **any** MCP-compatible harness. The only requirement is the `.mcp.json` file (or equivalent config format). Here's what differs:

| Feature | Claude Code | OpenCode | Cursor / Windsurf |
|---------|------------|----------|-------------------|
| **MCP connection** | `.mcp.json` (auto-discovered) | `mcp.json` or CLI config | Built-in MCP settings panel |
| **Tool discovery** | Automatic via `tools/list` | Automatic via `tools/list` | Automatic via `tools/list` |
| **Server instructions** | Surfaced to model context | Surfaced to model context | Surfaced to model context |
| **Skills** | `.claude/skills/` (rich tool guidance) | Not supported -- relies on tool docstrings | Not supported |
| **Hooks** | `.claude/settings.json` (auto-ingestion) | Not supported | Not supported |
| **Tool docstrings** | Full support | Full support | Full support |

**What harnesses without skills/hooks lose:**
- No decision tree for tool selection (model must figure it out from docstrings)
- No progressive disclosure guidance (model may dump all deep search results at once)
- No auto-ingestion of conversations (user must manually trigger ingestion)
- No presentation guidelines (model may dump raw JSON)

**What they keep:**
- All 6 tools work identically
- Server instructions provide high-level guidance
- Tool docstrings describe parameters and behavior
- The knowledge graph is fully queryable and writable

#### The 3-Layer Pattern for Any MCP Server

This architecture suggests a reusable pattern for connecting any MCP server to a harness:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Hooks (harness-specific automation)           │
│  Auto-ingest conversations, trigger pipelines, etc.     │
│  Only works in harnesses that support hooks             │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Skills (harness-specific guidance)            │
│  Decision trees, presentation rules, workflows          │
│  Only works in harnesses that support skills            │
├─────────────────────────────────────────────────────────┤
│  Layer 1: MCP Server (universal, protocol-standard)     │
│  Tools, server instructions, lifespan, transport        │
│  Works in ALL MCP-compatible harnesses                  │
└─────────────────────────────────────────────────────────┘
```

Layer 1 is portable. Layers 2 and 3 are progressive enhancements that make the experience richer in harnesses that support them, while degrading gracefully in those that don't.

---

### 10. E2E Example: Ingesting Decoding AI Articles via RSS

Here's the complete flow when the configured RSS feed `https://www.decodingai.com/feed` is processed:

#### Step 0: Start Fresh (Empty Collections)

```bash
mongosh -u twin -p twin --authenticationDatabase admin twin \
  --eval 'db.documents.drop(); db.knowledge_graph.drop(); print("Collections cleared.")'
```

Both `documents` and `knowledge_graph` collections are now empty. The pipelines will recreate indexes as needed.

#### Step 1: Trigger the Data Pipeline

```bash
make serve-workflows &        # Start Prefect worker
make run-substack-rss-data-pipeline  # Trigger RSS ingestion
```

Or via MCP: Claude Code calls `ingest_url("https://www.decodingai.com/p/some-article")` which routes through the URL ingestion router.

#### Step 2: Fetch & Parse RSS Feed

```
https://www.decodingai.com/feed
    |-- httpx GET (30s timeout)
    |-- feedparser parses XML
    |-- Returns ~20 entry objects with title, summary, content, author, date, links
```

#### Step 3: Extract Documents

For each RSS entry:
```
Raw entry
    |-- title: "The Role of Feature Stores in ML Systems"
    |-- author: "Paul Iusztin"  
    |-- published: "Mon, 15 Jan 2025 10:00:00 GMT" -> datetime(2025, 1, 15, 10, 0, 0, UTC)
    |-- summary: "Feature stores bridge the gap between..."
    |-- content[0].value: "<div><p>In production ML systems...</p>...</div>"
    |                        |-- BeautifulSoup strips HTML tags
    |                        |-- Preserves block structure (newlines around p, div, h1-6)
    |                        `-- Returns clean plain text
    |-- source_uri: "https://www.decodingai.com/p/the-role-of-feature-stores"
    `-> Document(source_type=SUBSTACK, source_uri=..., title=..., content=..., authors=["Paul Iusztin"], date=...)
```

#### Step 4: Load Documents (Dedup + References)

```
Document
    |-- Check: Does source_uri already exist (non-LATENT)? -> Skip if yes
    |-- Extract URLs from HTML content -> ["https://arxiv.org/abs/2309.xxxxx", ...]
    |-- For each referenced URL:
    |     |-- Already in DB? -> Use existing document
    |     `-- New? -> Create LATENT Document(source_type=LATENT, source_uri=url)
    |-- doc.references = [ref1, ref2, ...]
    |-- If LATENT exists for this source_uri -> Upgrade with real content
    `-- Upsert to MongoDB `documents` collection
```

#### Step 5: Memory Extraction

```bash
make run-memory-pipeline-extraction
```

For the article "The Role of Feature Stores in ML Systems":

```
Document.content (5000 tokens)
    |
    |-- [Chunking] -> 10 chunks of ~512 tokens each (64 overlap)
    |
    |-- [LLM Extraction] (5 chunks in parallel via Gemini)
    |   Chunk 1: "Paul Iusztin discusses how feature stores..."
    |     -> nodes: [{name: "paul iusztin", type: "person"},
    |                {name: "feature stores in ml", type: "episode", content: "..."}]
    |     -> edges: [{source: "paul iusztin", target: "feature stores in ml", type: "experienced"}]
    |
    |   Chunk 4: "The author prefers Feast for its simplicity..."
    |     -> nodes: [{name: "feast preference", type: "preference", content: "prefers Feast for simplicity"}]
    |     -> edges: [{source: "paul iusztin", target: "feast preference", type: "has"}]
    |
    |-- [Structural Entries]
    |   -> DOCUMENT node: "document:https://www.decodingai.com/p/the-role-of-feature-stores"
    |   -> 10 CHUNK nodes: "chunk:https://...#chunk-0" through "chunk:...#chunk-9"
    |   -> 10 PART_OF edges: chunk -> document
    |   -> 9 NEXT edges: chunk[0] -> chunk[1] -> ... -> chunk[9]
    |   -> 1 MENTIONS edge: document -> "person:paul iusztin"
    |   -> N REFERENCED edges: document -> referenced documents
    |
    |-- [Normalization]
    |   "paul iusztin" fuzzy matches existing "person:paul iusztin" (score 1.0)
    |   -> Merges into existing node, unions sources array
    |   "feature stores" vs "feature store" (score 0.93 > 0.85) -> Merged
    |
    `-- [Upsert] -> Bulk write to knowledge_graph collection
         Properties merged (new wins), sources array unioned, aliases unioned
```

#### Step 6: Indexing

```bash
make run-memory-pipeline-indexing
```

```
All nodes with empty embeddings
    |-- Build text representation:
    |   "person: person:paul iusztin\naliases: ['paul']\n"
    |   "chunk: chunk:https://...#chunk-3\nsource_type: substack\ncontent: In production ML systems..."
    |
    |-- Sentence Transformers all-MiniLM-L6-v2 (local, 384 dims)
    |-- Batch of 64 nodes at a time
    `-- Update embedding field in MongoDB
    
Ensure indexes:
    |-- Text index on (name, properties.content, properties.aliases)
    `-- Vector search index on embedding (cosine, 384 dims)
```

#### Step 7: Query via Claude Code

User in Claude Code: "What does Paul Iusztin think about harness engineering?"

Claude Code invokes the `twin-memory` skill, which calls `search_memory`:

```
query: "What does Paul Iusztin think about harness engineering?"
    |
    |-- [Vector Search] embed query -> cosine similarity on vector_index
    |   Top hits: "person:paul iusztin" (0.82), "episode:harness engineering practices" (0.79), ...
    |
    |-- [Text Search] $text: "paul iusztin harness engineering"
    |   Top hits: "chunk:...#chunk-1" (score 3.2), "person:paul iusztin" (score 2.8), ...
    |
    |-- [RRF Fusion] Combine rankings
    |   #1: "person:paul iusztin" (appeared in both lists, high combined score)
    |   #2: "episode:harness engineering practices"
    |   #3: "chunk:...#chunk-1"
    |
    |-- [Graph Expansion] 1-hop from seed nodes
    |   From "person:paul iusztin":
    |     -> "has" -> "preference:harness driven development"
    |     -> "experienced" -> "episode:harness engineering practices"
    |     -> "todo" -> "task:build evaluation harness"
    |   From "episode:harness engineering practices":
    |     -> "experienced" (reverse) -> "person:paul iusztin"
    |
    `-- QueryResult(nodes=[...], edges=[...])
        -> Claude summarizes: "Paul Iusztin has experience with harness engineering practices.
           He prefers harness-driven development and has a task to build an evaluation harness..."
```

#### Alternative: Real-Time Ingestion via MCP

During a Claude Code conversation:
```
User: "Ingest this article: https://www.decodingai.com/p/the-role-of-feature-stores"

Claude Code -> ingest_url("https://www.decodingai.com/p/the-role-of-feature-stores")
    |-- URL router matches "decodingai.com" -> Substack article pipeline
    |-- Fetch HTML, extract metadata, parse body
    |-- Load document to MongoDB
    |-- Run extraction inline (chunk + LLM + structural + normalize + upsert)
    |-- Run embedding inline (embed new nodes)
    `-- Returns: {"title": "The Role of Feature Stores", "nodes": 15, "edges": 22}

Claude: "Ingested 'The Role of Feature Stores in ML Systems' - extracted 15 nodes and 22 edges."
```

#### Auto-Ingestion of Conversations (Stop Hook)

At the end of every Claude Code session:
```
Stop hook fires -> checks sentinel file
    |-- First time this session? -> Block: "Please run: /twin-memory extract current conversation"
    |-- User runs: /twin-memory extract current conversation
    |-- Claude calls ingest_conversation(conversation_text)
    |-- Extracts people, tasks, episodes, preferences from the conversation
    |-- Knowledge graph grows with every conversation
    `-- Sentinel file created -> won't prompt again this session
```

---

### Architecture Diagram

```
                    ┌──────────────────────────────────────────────────┐
                    │              Claude Code (CLI / IDE)             │
                    │                                                  │
                    │  Skills: /twin-memory                           │
                    │  Hooks: Stop -> auto-ingest conversations       │
                    └─────────────────┬────────────────────────────────┘
                                      │ stdio (JSON-RPC)
                                      │
                    ┌─────────────────▼────────────────────────────────┐
                    │           FastMCP Server ("Twin Memory")         │
                    │                                                  │
                    │  Search:   query_memory | search_memory          │
                    │            deep_search_memory                    │
                    │  Write:    ingest_url | ingest_file              │
                    │            ingest_conversation                   │
                    └────────┬──────────────────┬──────────────────────┘
                             │                  │
              ┌──────────────▼──────┐    ┌──────▼───────────────────┐
              │   Query Engine      │    │   Ingestion Pipeline     │
              │                     │    │                          │
              │ NL->Pipeline (LLM)  │    │ URL Router -> ETL       │
              │ Hybrid Search (RRF) │    │ Chunk -> LLM Extract    │
              │ Graph Expansion     │    │ Structural Entries       │
              │ Deep Search         │    │ Normalize + Upsert       │
              └────────┬────────────┘    │ Embed + Index            │
                       │                 └──────┬──────────────────┘
                       │                        │
              ┌────────▼────────────────────────▼──────────────────┐
              │              MongoDB (Single Instance)             │
              │                                                    │
              │  documents collection         knowledge_graph      │
              │  ├─ source_uri (unique)       ├─ _id: "type:name"  │
              │  ├─ content, title            ├─ kind: node|edge   │
              │  ├─ authors, date             ├─ embedding[384]    │
              │  └─ references[]              ├─ text_index         │
              │                               └─ vector_index       │
              └────────────────────────────────────────────────────┘

              ┌────────────────────────────────────────────────────┐
              │              External Services                     │
              │                                                    │
              │  Gemini 2.5 Flash Lite -- LLM (extraction, NL)    │
              │  Sentence Transformers -- Embeddings (local)       │
              │  Prefect -- Workflow orchestration (batch ETLs)    │
              └────────────────────────────────────────────────────┘
```

---

### Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| **MCP Framework** | FastMCP (stdio transport) |
| **LLM** | Google Gemini 2.5 Flash Lite |
| **Embeddings** | Sentence Transformers all-MiniLM-L6-v2 (384d, local) |
| **Database** | MongoDB (single instance with mongot for vector search) |
| **ODM** | Beanie (async Pydantic ODM for MongoDB) |
| **Orchestration** | Prefect (10 deployments for batch pipelines) |
| **Agent Platform** | Claude Code (CLI + IDE extensions) |
| **Search** | Hybrid: text index + vector search + RRF fusion + $graphLookup |
| **Config** | Pydantic Settings (.env) + YAML app config |
| **Python** | 3.14, fully async, uv package manager |
