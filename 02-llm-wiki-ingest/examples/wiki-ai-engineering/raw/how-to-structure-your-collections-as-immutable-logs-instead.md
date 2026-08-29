# How to structure your collections as immutable logs instead of a one time collections.

- Walk them through how LangChain models the collection and why it makes it super hard to find duplicates and update current relationships.
- How I structured my collection based on immutable logs + materialization
- By computing the embeddings only during materialization we skip computing them for every entry found during ingestion
- PROs and CONs between the two. Still MongoDB makes this stupid simple, while still being super scalable!

**Full note:**

## LangChain gave me a knowledge graph in 10 minutes. It also gave me 34 relationship types, duplicate edges, and no way to fix them.

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | Most GraphRAG tutorials skip straight to retrieval code and treat the data model as an afterthought. Without an ontology, your LLM extraction is unconstrained — it invents entity types, hallucinates relationships, and floods your graph with noise. LangChain's MongoDBGraphStore demonstrates this perfectly: 17 node types and 34 relationship types from 5 documents, with duplicate edges you can't detect or fix. |
| **Solution**    | Design a typed ontology first — 6 node types, 8 edge types, each with a Pydantic attribute schema and directional edge constraints. Split extraction into two strategies: LLM-powered for semantic entities (person, task, episode, preference) and deterministic for structural entities (document, chunk). Store everything as immutable observation logs, then materialize a deduplicated query view via MongoDB aggregation. Compute embeddings only after deduplication. |
| **Transformation** | A knowledge graph where the ontology constrains the LLM to produce consistent, business-aligned output. Every entity has a type, every relationship has a direction and constraint, every observation is traceable to its source chunk. Deduplication is structural, embeddings are computed once per entity, and the query layer combines text, vector, and graph traversal — because the schema was designed for it from the start. |
| **Hook**        | LangChain gave me a knowledge graph in 10 minutes. It also gave me 34 relationship types, duplicate edges, and no way to fix them. |
| **Target audience** | AI/ML engineers building RAG or GraphRAG systems, backend engineers working with knowledge graphs, anyone designing LLM extraction pipelines that need structured output. |

### Outline

1. Hook: LangChain's MongoDBGraphStore in 10 minutes — what the collection looks like, why 34 relationship types and embedded arrays make dedup impossible, and why this is a prototype not a system. (Short — this is the setup, not the lesson.)
2. The ontology is the most important step in GraphRAG: why designing types before writing extraction code changes everything.
3. Designing the ontology for a personal digital twin: 6 node types, 8 edge types, the reasoning behind each — what a "Document Ontology" and "Person Ontology" are and how they connect.
4. Attribute schemas: Pydantic models that define what properties each node type carries — DocumentProperties, ChunkProperties, PersonProperties, TaskProperties, EpisodeProperties, PreferenceProperties. These schemas are what gets sent to the LLM as the extraction contract.
5. Edge constraints: every edge type locked to a specific (source_type → target_type) pair, enforced at extraction time.
6. Two extraction strategies: structured (LLM-powered) for person, task, episode, preference vs semi-structured (metadata + topology) for document, chunk. Why not everything should go through the LLM.
7. The extraction pipeline step-by-step: chunk → parallel LLM extraction → build structural entries → merge → fuzzy normalize → persist as immutable logs.
8. The three-collection architecture: documents, knowledge_graph_log, knowledge_graph — what each stores and why.
9. The materialization pipeline: how $group, $mergeObjects, $addToSet, $unionWith, and $out turn append-only logs into a deduplicated query view. Composite IDs, the DuplicateKeyError that forced the right design, and reverse edges for bidirectional traversal.
10. The embedding optimization: compute vectors once per deduplicated node during materialization, not per observation during ingestion. Why the materialized node produces better embeddings.
11. The query pattern enabled by this data model: text + vector → RRF fusion → $graphLookup expansion.
12. PROs and CONs between LangChain's approach and immutable logs + materialization. MongoDB makes both approaches simple, but only one scales.

---

### Full body

#### The hook: LangChain in 10 minutes

I started where most people start — with LangChain. The `MongoDBGraphStore` from `langchain-mongodb` promises a working knowledge graph in minutes:

```python
from langchain_mongodb.graphrag.graph import MongoDBGraphStore

graph_store = MongoDBGraphStore(
    connection_string=settings.mongo.mongo_uri.get_secret_value(),
    database_name=settings.mongo.mongo_initdb_database,
    collection_name="knowledge_graph_demo",
    entity_extraction_model=llm,  # Gemini 2.5 Flash Lite
)

graph_store.add_documents(chunked_docs)  # 10 chunks from 5 articles
```

Ten minutes later, 80 entities in MongoDB. Then I looked at what was actually stored. Every entity is one document with relationships embedded as parallel arrays:

```json
{
  "_id": "AI Evals",
  "type": "Topic",
  "attributes": { "part_count": ["7"] },
  "relationships": {
    "target_ids": ["Brown", "AI application development lifecycle", ...],
    "types":      ["saved", "Part Of", "Used For", ...],
    "attributes": [{}, {}, ...]
  }
}
```

From 5 documents, the LLM invented **17 node types** and **34 relationship types** — including `"part_of"`, `"Part Of"`, and `"part of"` as three separate types. A `mongosh` scan found **30+ entities with duplicate relationships**: the "AI Evals & Observability series" entity had 8 duplicate `has_part` edges, "Opik" had 6, "AI Evals" had 13.

```javascript
// 34 relationship types with casing inconsistencies from 5 documents
let allTypes = new Set();
db.knowledge_graph_demo.find().forEach(doc => {
  (doc.relationships?.types || []).forEach(t => allTypes.add(t));
});
```

The problem isn't LangChain's code quality — it's the data model. Relationships embedded as arrays inside entity documents means: (1) dedup requires scanning every `(target_id, type)` pair in every document, (2) updating a single relationship means modifying the parent entity, (3) there's no provenance — you can't trace an entity back to its source chunk. This is structurally fine for a prototype. It's structurally broken for a production system.

LangChain does support `allowed_nodes` and `allowed_relationships` parameters, so you could constrain types. But the embedded-array data model — the thing that makes dedup, provenance, and graph traversal impossible — isn't configurable. That's architectural.

Now let me show you what I built instead.

#### The ontology: the most important step in GraphRAG

Before writing any extraction or query code, I designed the ontology — the typed vocabulary the system uses to decompose unstructured content into structured graph entities. This is the single most important step in GraphRAG. Not the retrieval code. Not the embedding model. Not the graph database. The ontology.

Without it, LLM extraction is unconstrained text generation that happens to output JSON. The LLM will be creative, inconsistent, and prolific — exactly the opposite of what a knowledge graph needs. With it, the LLM is constrained to produce exactly what your system needs. The query layer knows what to expect. The materialization knows how to group. The graph grows with signal, not noise.

The ontology is a contract between two systems: the LLM extractor (which writes to the graph) and the query layer (which reads from it). Everything downstream — extraction, materialization, indexing, traversal — follows from this contract.

#### Designing the ontology for a personal digital twin

I'm building a personal digital twin — an AI agent that knows what I've written, who I've mentioned, what I care about, and what I'm working on. The ontology needs to capture that domain. Here's how I reasoned about it.

The ontology splits into two sub-ontologies (visible in the architecture diagram):

**The Document Ontology** describes the structural backbone — how content is organized:
- **Document**: A source article, video, or post. The top-level content unit.
- **Chunk**: A piece of a document, produced by the chunking algorithm.
- Edges: `PART_OF` (chunk → document), `NEXT` (chunk → chunk), `MENTIONS` (document → person), `REFERENCED` (document → document).

**The Person Ontology** describes the semantic layer — what the LLM extracts from the text:
- **Person**: Someone mentioned in or related to the content.
- **Task**: An action item, project, or thing to do.
- **Episode**: An event, experience, or thing that happened.
- **Preference**: An opinion, stance, or tool preference.
- Edges: `TODO` (person → task), `EXPERIENCED` (person → episode), `HAS` (person → preference), `RELATED_TO` (person ↔ person).

Implemented as two Python StrEnums:

```python
class NodeType(StrEnum):
    DOCUMENT = "document"
    CHUNK = "chunk"
    PERSON = "person"
    TASK = "task"
    EPISODE = "episode"
    PREFERENCE = "preference"

class EdgeType(StrEnum):
    PART_OF = "part_of"
    NEXT = "next"
    MENTIONS = "mentions"
    REFERENCED = "referenced"
    RELATED_TO = "related_to"
    TODO = "todo"
    EXPERIENCED = "experienced"
    HAS = "has"
```

The key design decision: **keep it small and specific.** 6 node types, 8 edge types.

Not "entity" and "relationship" — those are too vague. Tell an LLM to extract "entities" and it will extract everything: programming languages, companies, abstract concepts, dates, URLs, adjectives. You get a graph that's technically full but structurally meaningless.

Not fifty specialized types — those create sparse graphs where most types have a single instance. The LLM can't reliably distinguish between fifty options, and your materialization logic needs to handle every one.

The sweet spot is a handful of types that are specific enough to be meaningful but general enough to cover your domain. A different domain (e-commerce, healthcare, legal) would have different types — but the same principle: constrain the LLM to produce what your business actually needs, not what it finds interesting.

#### Attribute schemas: Pydantic models as the extraction contract

Each node type has a Pydantic model defining its expected properties. These schemas serve two purposes: (1) they're sent to the LLM as part of the extraction prompt so it knows what properties to fill, and (2) they document the data contract for downstream consumers.

```python
class DocumentProperties(BaseModel):
    """A source document (article, video, etc.) ingested into the system."""
    source_type: str = Field(description="Source platform (e.g., substack, youtube)")
    source_uri: str = Field(description="URI of the source document")
    date: str | None = Field(default=None, description="Publication date (ISO 8601)")

class ChunkProperties(BaseModel):
    """A chunk of text extracted from a document."""
    source_type: str = Field(description="Source platform of the parent document")
    source_uri: str = Field(description="URI of the parent document")
    content: str = Field(description="Text content of the chunk")
    date: str | None = Field(default=None, description="Publication date of the parent")

class PersonProperties(BaseModel):
    """A person mentioned in or related to the content."""
    aliases: list[str] = Field(default_factory=list,
        description="Alternative names, nicknames, or references to this person")
    email: str | None = Field(default=None, description="Email address if known")

class TaskProperties(BaseModel):
    """A task, project, or actionable item associated with a person."""
    content: str = Field(description="Description of the task or project")
    date: str | None = Field(default=None, description="Due date or mentioned date (ISO 8601)")

class EpisodeProperties(BaseModel):
    """A life or work episode experienced by a person."""
    content: str = Field(description="Description of the episode or experience")
    date: str | None = Field(default=None, description="When the episode occurred (ISO 8601)")

class PreferenceProperties(BaseModel):
    """A preference, opinion, or pattern exhibited by a person."""
    content: str = Field(description="Description of the preference")
```

Notice the design choices:
- **Person** has `aliases` (for fuzzy matching) and `email` — not `content`. A person is identified by name, not by description.
- **Task, Episode, Preference** all have `content` — the semantic payload the LLM extracts from text.
- **Document, Chunk** have `source_type` and `source_uri` — metadata that comes from the pipeline, not the LLM.

The schemas are registered in a lookup dict and converted to JSON Schema via `.model_json_schema()` for the LLM prompt:

```python
NODE_PROPERTIES: dict[NodeType, type[BaseModel]] = {
    NodeType.DOCUMENT: DocumentProperties,
    NodeType.CHUNK: ChunkProperties,
    NodeType.PERSON: PersonProperties,
    NodeType.TASK: TaskProperties,
    NodeType.EPISODE: EpisodeProperties,
    NodeType.PREFERENCE: PreferenceProperties,
}
```

#### Edge constraints: directional, enforced

Every edge type is locked to a specific `(source_type → target_type)` pair:

```python
EDGE_CONSTRAINTS: dict[EdgeType, EdgeConstraint] = {
    EdgeType.PART_OF: EdgeConstraint(
        source_type=NodeType.CHUNK, target_type=NodeType.DOCUMENT,
        description="Chunk belongs to a document"),
    EdgeType.NEXT: EdgeConstraint(
        source_type=NodeType.CHUNK, target_type=NodeType.CHUNK,
        description="Sequential ordering between chunks"),
    EdgeType.MENTIONS: EdgeConstraint(
        source_type=NodeType.DOCUMENT, target_type=NodeType.PERSON,
        description="Document mentions a person"),
    EdgeType.REFERENCED: EdgeConstraint(
        source_type=NodeType.DOCUMENT, target_type=NodeType.DOCUMENT,
        description="Document references another document"),
    EdgeType.RELATED_TO: EdgeConstraint(
        source_type=NodeType.PERSON, target_type=NodeType.PERSON,
        description="Two people are related or connected"),
    EdgeType.TODO: EdgeConstraint(
        source_type=NodeType.PERSON, target_type=NodeType.TASK,
        description="Person has a task or project to do"),
    EdgeType.EXPERIENCED: EdgeConstraint(
        source_type=NodeType.PERSON, target_type=NodeType.EPISODE,
        description="Person experienced a life or work episode"),
    EdgeType.HAS: EdgeConstraint(
        source_type=NodeType.PERSON, target_type=NodeType.PREFERENCE,
        description="Person has a preference or opinion"),
}
```

These constraints are enforced during extraction. If the LLM returns an edge with `source_type=PERSON, target_type=TASK, type=experienced`, it gets dropped — `experienced` requires `PERSON → EPISODE`:

```python
constraint = EDGE_CONSTRAINTS[edge_type]
if src_type != constraint.source_type or tgt_type != constraint.target_type:
    logger.warning("Edge %s violates constraint (%s→%s expected, got %s→%s)",
        edge_type, constraint.source_type, constraint.target_type, src_type, tgt_type)
    continue
```

This is what "ontology as a contract" means in practice. The LLM can't invent `"human"` when `"person"` exists. It can't create `"vaguely_associated_with"` when the edge types are enumerated. It can't connect a `TASK` to an `EPISODE` with a `TODO` edge. The schema is the guardrail.

#### Two extraction strategies: structured vs semi-structured

Here's something most GraphRAG tutorials miss: not every node type should be extracted the same way. The 6 node types split cleanly into two categories:

**Structured extraction (LLM-powered):** `PERSON`, `TASK`, `EPISODE`, `PREFERENCE`. These are semantic entities buried inside unstructured text. A person is mentioned in a paragraph. A task is implied by a sentence. A preference is expressed through an opinion. You need an LLM to read the text and extract them.

```python
LLM_EXTRACTABLE_NODE_TYPES: set[NodeType] = {
    NodeType.PERSON, NodeType.TASK, NodeType.EPISODE, NodeType.PREFERENCE,
}
LLM_EXTRACTABLE_EDGE_TYPES: set[EdgeType] = {
    EdgeType.RELATED_TO, EdgeType.TODO, EdgeType.EXPERIENCED, EdgeType.HAS,
}
```

**Semi-structured extraction (metadata + topology):** `DOCUMENT`, `CHUNK`. These come from the pipeline's own structure. A document node is created from RSS metadata — title, URI, date, authors are already fields, not something an LLM needs to infer. A chunk node is created from the chunking algorithm — content and position are deterministic. The edges between them (`PART_OF`, `NEXT`, `MENTIONS`, `REFERENCED`) come from pipeline topology.

```python
STRUCTURAL_EDGE_TYPES: set[EdgeType] = {
    EdgeType.PART_OF, EdgeType.NEXT, EdgeType.MENTIONS, EdgeType.REFERENCED,
}
```

This split matters for three reasons:

1. **Reliability.** Semi-structured entities are deterministic. Run the pipeline twice, same results. LLM extraction is non-deterministic. By limiting LLM extraction to only the types that need it, you minimize the surface area for hallucination.

2. **Cost.** LLM extraction is the most expensive step. Document and chunk nodes are free — they come from metadata you already have. Sending your entire ontology through LLM extraction means paying the LLM to tell you things you already know.

3. **Consistency.** The LLM might extract a document with a slightly different title or date format. Your pipeline already has the canonical values. Metadata-driven extraction means structural nodes are always consistent with the source.

#### The extraction pipeline: step by step

Here's the complete flow from raw document to persisted log entries. This is the `extract_and_store()` function in `src/twin/memory/extraction/core.py`.

**Step 1: Chunk the document.**

Token-bounded splitting using `tiktoken` (cl100k_base encoder). Default: 512 tokens per chunk, 64 token overlap.

```python
_ENCODER = tiktoken.get_encoding("cl100k_base")

def chunk_document(text: str, chunk_size=512, chunk_overlap=64) -> list[str]:
    tokens = _ENCODER.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunks.append(_ENCODER.decode(tokens[start:end]))
        start += chunk_size - chunk_overlap
    return chunks
```

Each chunk gets a UUID for provenance tracking: `chunk_ids = [str(uuid4()) for _ in chunks]`.

**Step 2: LLM extraction per chunk (parallel, semaphore-capped).**

Each chunk is sent to the LLM with the ontology schema. The system prompt includes the full ontology (node types with their property schemas, edge types with their constraints) and enforces JSON output:

```python
_SYSTEM_PROMPT = """\
You are a knowledge-graph extraction engine.

Given a chunk of text, extract entities (nodes) and relationships (edges)
according to the ontology below. Return **only** valid JSON.

## Ontology
{ontology}

## Output schema
{{
  "nodes": [{{ "name": "<canonical lowercase name>", "type": "<node type>", "properties": {{}} }}],
  "edges": [{{ "source_node_id": "<name>", "source_type": "<type>",
               "target_node_id": "<name>", "target_type": "<type>",
               "type": "<edge type>", "properties": {{}} }}]
}}

Rules:
- Node names MUST be lowercase.
- Only use node types and edge types listed in the ontology.
- Respect edge constraints (source_type → target_type).
"""
```

The `ontology` variable is built from `get_ontology_schema()` which converts the Pydantic attribute schemas to JSON Schema and includes the edge constraints. This is the contract — the LLM sees exactly what types and properties are valid.

Extraction runs in parallel across chunks with a concurrency semaphore (default 5):

```python
semaphore = asyncio.Semaphore(app_config.extraction.llm_concurrency)

async def _extract(chunk, chunk_id):
    async with semaphore:
        return await extract_entities(llm, chunk, chunk_id=chunk_id)

results = await asyncio.gather(*[_extract(c, cid) for c, cid in zip(chunks, chunk_ids)])
```

Every extracted item is validated against the ontology. Invalid node types, non-extractable types (like `DOCUMENT` or `CHUNK`), and edge constraint violations are silently dropped with a warning log.

**Step 3: Build structural entries (deterministic, no LLM).**

After LLM extraction, the pipeline creates the backbone entries from metadata:

```python
def build_structural_entries(*, document_id, source_type, source_uri, date,
                              chunk_texts, chunk_ids, extracted, reference_uris):
```

This creates:
- 1 **DOCUMENT** node from RSS metadata (`source_type`, `source_uri`, `date`).
- N **CHUNK** nodes, one per text chunk, named `"{source_uri}#chunk-{idx}"`.
- N **PART_OF** edges: each chunk → its parent document.
- N-1 **NEXT** edges: chunk-0 → chunk-1 → chunk-2 (sequential ordering).
- **MENTIONS** edges: document → every unique `PERSON` node that the LLM extracted.
- **REFERENCED** edges: document → every cross-referenced document URI (from hyperlinks).

Notice how `MENTIONS` bridges the two ontologies: the Document Ontology connects to the Person Ontology through this edge. The LLM extracts person nodes; the pipeline deterministically creates the `MENTIONS` edge from the document to each person.

**Step 4: Merge LLM + structural results.**

```python
combined = llm_result.merge(structural)
```

The `ExtractionResult` dataclass has a `merge()` method that concatenates node and edge lists. At this point you have a single result containing both semantic entities (from the LLM) and structural entities (from metadata).

**Step 5: Fuzzy normalization.**

The LLM might extract "Paul Iusztin" from one chunk and "paul iusztin" from another — or "MLOps" and "mlops". The normalization step uses `SequenceMatcher` to merge near-duplicate nodes within each type:

```python
def normalize_nodes(result: ExtractionResult) -> ExtractionResult:
    canonical_map: dict[tuple[NodeType, str], str] = {}
    kept_nodes: list[ExtractedNode] = []

    for node in result.nodes:
        key = (node.type, node.name)
        if key in canonical_map:
            continue

        matched = False
        for kept in kept_nodes:
            if kept.type != node.type:
                continue
            ratio = SequenceMatcher(None, node.name, kept.name).ratio()
            if ratio >= 0.85:  # similarity threshold
                canonical_map[key] = kept.name
                kept.properties = {**node.properties, **kept.properties}  # merge props
                matched = True
                break

        if not matched:
            canonical_map[key] = node.name
            kept_nodes.append(node)

    # Rewrite edge endpoints using the canonical map.
    remapped_edges = []
    for edge in result.edges:
        src_key = (edge.source_type, edge.source_node_id)
        tgt_key = (edge.target_type, edge.target_node_id)
        remapped_edges.append(edge.model_copy(update={
            "source_node_id": canonical_map.get(src_key, edge.source_node_id),
            "target_node_id": canonical_map.get(tgt_key, edge.target_node_id),
        }))

    return ExtractionResult(nodes=kept_nodes, edges=remapped_edges)
```

Key detail: edges are remapped to use canonical node names. If "Paul Iusztin" was normalized to "paul iusztin", all edges pointing to "Paul Iusztin" are rewritten to point to "paul iusztin".

**Step 6: Persist as immutable log entries.**

Every node and edge becomes a separate document in the `knowledge_graph_log` collection:

```python
async def store_log_entries(result, *, source_document_id):
    now = datetime.now(tz=UTC)
    entries = []

    for node in result.nodes:
        entries.append(NodeLogEntry(
            name=node.name, type=node.type, properties=node.properties,
            source_document_id=source_document_id,
            chunk_id=node.chunk_id, created_at=now,
        ))

    for edge in result.edges:
        entries.append(EdgeLogEntry(
            source_node_id=edge.source_node_id, source_type=edge.source_type,
            target_node_id=edge.target_node_id, target_type=edge.target_type,
            type=edge.type, properties=edge.properties,
            source_document_id=source_document_id,
            chunk_id=edge.chunk_id, created_at=now,
        ))

    await NodeLogEntry.insert_many(node_entries)
    await EdgeLogEntry.insert_many(edge_entries)
```

The log is append-only. If three articles mention "paul iusztin", that's three separate `NodeLogEntry` documents — each linking to its source document and chunk. The log is never modified or deleted.

Here's what actual log entries look like in MongoDB:

```json
// Node observation — "paul iusztin" seen in chunk 99f34c43
{
  "_id": ObjectId("69a036a2ca69900a75f17a45"),
  "kind": "node",
  "name": "paul iusztin",
  "type": "person",
  "properties": {},
  "source_document_id": ObjectId("699f2df2589437c9b66b6bf6"),
  "chunk_id": "99f34c43-530c-422b-b65c-4730a534adad",
  "created_at": "2026-02-26T12:03:46.212Z"
}

// Edge observation — "opik" has preference "multimodal ai agents"
{
  "_id": ObjectId("69a036a2ca69900a75f17a57"),
  "kind": "edge",
  "source_node_id": "opik",
  "source_type": "person",
  "target_node_id": "multimodal ai agents",
  "target_type": "preference",
  "type": "has",
  "source_document_id": ObjectId("699f2df2589437c9b66b6bf6"),
  "chunk_id": "1e023ebf-8cd7-42da-89cb-2128aa5c625a",
  "created_at": "2026-02-26T12:03:46.212Z"
}
```

#### Three collections, three responsibilities

**`documents`** — the raw ingested content. Each document indexed by `source_uri` for idempotent ingestion. This is the input layer. One ETL per source (Substack RSS, YouTube, custom sites, markdown files).

**`knowledge_graph_log`** — immutable, append-only observations. Every extraction run appends new entries. The log is the source of truth. Two reasons for immutability: (1) **provenance** — you can trace any node or edge back to the exact chunk that produced it, (2) **replayability** — you can rebuild the materialized graph from scratch by re-aggregating the logs. Change your materialization logic? Re-run the aggregation. No re-extraction needed.

**`knowledge_graph`** — the materialized query view. Rebuilt from logs via a MongoDB aggregation pipeline. Nodes and edges coexist in the same collection — this is deliberate, because `$graphLookup` requires a single collection to traverse.

#### The materialization pipeline

A single MongoDB aggregation pipeline turns logs into the deduplicated query view.

**Nodes: group by `{name, type}`, compose `"type:name"` ID.**

```python
node_branch = [
    {"$match": {"kind": "node"}},
    {"$group": {
        "_id": {"name": "$name", "type": "$type"},
        "properties": {"$mergeObjects": "$properties"},
        "sources": {"$addToSet": "$source_document_id"},
        "created_at": {"$min": "$created_at"},
        "updated_at": {"$max": "$created_at"},
    }},
    {"$project": {
        "_id": {"$concat": ["$_id.type", ":", "$_id.name"]},
        # → "person:paul iusztin", "preference:opik", "document:mlops-guide"
        "kind": {"$literal": "node"},
        "name": "$_id.name",
        "type": "$_id.type",
        "properties": 1,
        "embedding": {"$literal": []},  # Empty — filled post-materialization
        "sources": 1,
        "created_at": 1,
        "updated_at": 1,
    }},
]
```

The composite ID format (`"type:name"`) was born from a bug. Originally I used just the name as the `_id`. Materialization crashed with `DuplicateKeyError: { _id: "opik" }` — "opik" existed as both a person and a preference. The type prefix solved it: `"person:opik"` vs `"preference:opik"`. It also makes IDs self-documenting.

**Edges: group by `{source, target, type}`, compound dict as ID.**

```python
edge_branch = [
    {"$match": {"kind": "edge"}},
    {"$group": {
        "_id": {
            "source_node_id": "$source_node_id",
            "source_type": "$source_type",
            "target_node_id": "$target_node_id",
            "target_type": "$target_type",
            "type": "$type",
        },
        "properties": {"$mergeObjects": "$properties"},
        "sources": {"$addToSet": "$source_document_id"},
        "created_at": {"$min": "$created_at"},
        "updated_at": {"$max": "$created_at"},
    }},
    {"$project": {
        "_id": {
            "source_node_id": {"$concat": ["$_id.source_type", ":", "$_id.source_node_id"]},
            "target_node_id": {"$concat": ["$_id.target_type", ":", "$_id.target_node_id"]},
            "type": "$_id.type",
        },
        # ... remaining fields with "type:name" prefixed IDs
    }},
]
```

Edge IDs are compound dicts — `{source_node_id, target_node_id, type}` — which makes them naturally deduplicated. Two observations of the same edge from different chunks produce one materialized entry.

**Merge and write atomically:**

```python
pipeline = [
    *node_branch,
    {"$unionWith": {"coll": "knowledge_graph_log", "pipeline": edge_branch}},
    {"$out": "knowledge_graph"},
]
```

`$unionWith` merges both branches. `$out` writes atomically — the entire collection is replaced in one operation.

Here's the actual materialized output in MongoDB:

```json
// Materialized node — deduplicated, composite ID, empty embedding
{
  "_id": "person:paul iusztin",
  "kind": "node",
  "name": "paul iusztin",
  "type": "person",
  "properties": {},
  "embedding": [],
  "sources": [ObjectId("699f2df2589437c9b66b6bf6")],
  "created_at": "2026-02-26T12:03:46.212Z",
  "updated_at": "2026-02-26T12:27:31.881Z"
}

// Materialized edge — compound dict ID, natural dedup
{
  "_id": {
    "source_node_id": "person:paul iusztin",
    "target_node_id": "task:apply everything on your own",
    "type": "todo"
  },
  "kind": "edge",
  "type": "todo",
  "source_node_id": "person:paul iusztin",
  "source_type": "person",
  "target_node_id": "task:apply everything on your own",
  "target_type": "task"
}
```

**Reverse edges for bidirectional traversal.**

After materialization, reverse edge copies are created for specific node type pairs so `$graphLookup` can traverse in both directions:

```python
_BIDIRECTIONAL_PAIRS: set[tuple[str, str]] = {
    (NodeType.PERSON, NodeType.DOCUMENT),   # "who wrote this?" + "what did they write?"
    (NodeType.DOCUMENT, NodeType.PERSON),
    (NodeType.PERSON, NodeType.PERSON),     # mutual relationships
    (NodeType.DOCUMENT, NodeType.DOCUMENT), # cross-references
}
```

Not everything is bidirectional. `PERSON → TASK` (todo), `PERSON → EPISODE` (experienced), `PERSON → PREFERENCE` (has) are intentionally one-directional — tasks belong to people, not the other way around.

Reverse edges are inserted with `direction: "reverse"` so the visualization layer can filter them out to avoid rendering doubled edges.

#### Embeddings: once per entity, not once per observation

Notice the `"embedding": {"$literal": []}` in the materialization pipeline. Nodes are created with empty embedding vectors. Embeddings are computed post-materialization:

```python
async def embed_nodes(client, database, embedding_model):
    # Find all nodes without embeddings
    docs = await collection.find(
        {"kind": "node", "embedding": {"$in": [[], None]}},
    ).to_list()

    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        texts = [_node_to_text(doc) for doc in batch]
        vectors = await embedding_model.embed(texts)
        # bulk_write UpdateOne operations
```

The text representation for embedding combines the node's type, ID, properties, and content:

```python
def _node_to_text(node):
    parts = [f"{node.get('type', '')}: {node.get('_id', '')}"]
    props = node.get("properties", {})
    for key, value in props.items():
        if value and key != "content":
            parts.append(f"{key}: {value}")
    if props.get("content"):
        parts.append(str(props["content"]))
    return "\n".join(parts)
```

Why this matters: "paul iusztin" was observed in 2 log entries (two different chunks). In a naive approach, you'd compute an embedding for each observation — 2 calls. Here, the 2 observations are aggregated into 1 materialized node, and you compute 1 embedding.

At the scale of the current data: **244 log entries materialized into 70 nodes.** That's ~3.5x fewer embedding API calls. At larger scale with entities appearing across dozens or hundreds of documents, the savings compound — an entity mentioned in 50 chunks still costs exactly 1 embedding call.

The materialized node also produces a **better** embedding, because `$mergeObjects` combines properties from all observations. The node has richer, more complete information to embed against than any single observation would.

#### The query pattern this enables

The data model was designed for a specific two-phase query pattern:

**Phase 1 — Search seed nodes** via text and vector search, fused with Reciprocal Rank Fusion:
- `$vectorSearch` on the `embedding` field (cosine similarity)
- `$text` query on a text index across `name`, `properties.content`, `properties.aliases`
- RRF fusion: `score = sum(1 / (k + rank + 1))` across both ranked lists
- Top-k by fused score

**Phase 2 — Expand graph** from seed nodes via `$graphLookup`:
- Two passes: outgoing (seed `_id` → edge `source_node_id` → follow `target_node_id`) and incoming (reverse)
- Merge with `$setUnion`, deduplicate edges
- Hydrate all discovered node documents

This works because the data model was designed for it:
- Nodes have `embedding` fields for vector search
- Nodes have `name` and `properties.content` for text search
- Nodes and edges coexist in one collection for `$graphLookup`
- Composite IDs (`"type:name"`) let edges reference nodes directly
- Reverse edges enable bidirectional traversal without adjacency lists

#### PROs and CONs

| Dimension | LangChain MongoDBGraphStore | Immutable logs + materialization |
|---|---|---|
| **Setup time** | 10 minutes. 3 lines of code. | 2 days. Ontology + extraction + materialization + query layer. |
| **Ontology** | None by default. 17 node types and 34 edge types from 5 docs. | Strict. 6 node types, 8 edge types with attribute schemas and edge constraints. |
| **Deduplication** | Near-impossible. Embedded arrays accumulate silently. 30+ entities had duplicates. | Structural. `$group` by `{name, type}` eliminates duplicates by design. |
| **Provenance** | None. Can't trace entities to source chunks. | Full. Every log entry links to `source_document_id` and `chunk_id`. |
| **Replayability** | None. Re-extraction is the only option. | Full. Delete materialized view, re-aggregate, done. Change materialization logic without re-extracting. |
| **Embedding cost** | Per-observation. N observations = N embeddings. | Per-materialized-node. N observations = 1 embedding after dedup. |
| **Query capability** | Entity name lookup → embedded relationships. No vector/text search, no graph traversal. | Text + vector → RRF fusion → `$graphLookup` expansion. |
| **Scalability** | Degrades. More data = more noise, more duplicates. | Scales. Append-only logs + batch aggregation + indexed queries. |
| **When to use** | Prove the concept in an afternoon. | Build the system that runs in production. |

MongoDB makes both approaches possible — and that's the point. The same database handles document storage, aggregation pipelines for materialization, text search indexes, vector search indexes, and `$graphLookup` traversal. No separate graph database. No separate vector store. No glue code between systems. One database, three collections, and the aggregation framework does the heavy lifting. The difference between the prototype and the production system isn't the infrastructure — it's the data model you design on top of it.

![[assets/diagram-extraction-pipeline.png]]

![[assets/diagram-extraction-strategies.png]]

![[assets/diagram-ontology-overview.png]]

![[assets/diagram-query-pattern.png]]

![[assets/diagram-three-collections.png]]
