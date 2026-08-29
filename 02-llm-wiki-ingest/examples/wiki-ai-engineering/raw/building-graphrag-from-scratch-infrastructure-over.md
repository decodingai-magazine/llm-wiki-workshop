# building-graphrag-from-scratch-infrastructure-over-frameworks

Once the system design and plan of attack become clear, how easy was to implement from scratch my digital twin project (data pipelines, memory pipelines, orms, retrieval, etc.). Every from scratch. No AI frameworks. That’s why infrastructure tools such as MongoDB, Prefect and Opik are more important than ever. They support your business logic and coding agents, being hard to implement, while AI frameworks mostly stay in your way. 

**For example in 2 days, I managed to write  a unified memory layer for my AI agents** powered by MongoDB with graph, semantic and text search. Plus, data pipelines, visualizations, immutable logs, ontologies, durable workflows (Prefect) and observability (Opik). Writing everything from scratch anchored into the business logic and having full customizatiom is 100% more powerful once you know what to ask. On the other side of the spectrum initially I tried to use Lang chains of  to see how they do it and how  store stuff  and reverse  and I just I just had issues with it. Once I am not following  their assumption it started to fail and starting to customise it It’s a really pain in the ass.

![[assets/building-graphrag-from-scratch-infrastru-image.png]]

## I built a full GraphRAG system in 2 days. No LangChain. No AI frameworks. Just MongoDB, Prefect, and Python.

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | AI frameworks like LangChain promise to accelerate development, but the moment you deviate from their assumptions — custom ontologies, immutable logs, composite IDs, hybrid search fusion — they fight back. You spend more time working around the framework than building your system. Meanwhile, the actual hard problems (durable workflows, vector search, aggregation pipelines, graph traversal) live in infrastructure tools, not frameworks. |
| **Solution**    | Build from scratch with infrastructure tools that solve the genuinely hard problems: MongoDB for unified memory (document storage + aggregation + text search + vector search + graph traversal), Prefect for durable workflows with retries and monitoring, and direct LLM SDK calls behind a thin abstraction. The business logic — ontologies, extraction, normalization, materialization, query fusion — is custom Python anchored to your domain. |
| **Transformation** | A production-grade unified memory layer for AI agents with graph, semantic, and text search. Plus data pipelines, immutable logs, ontology-constrained extraction, materialization, visualizations, and durable workflows. All in 2 days. Full control over every design decision because there's no framework opinion to fight. |
| **Hook**        | I built a full GraphRAG system in 2 days. No LangChain. No AI frameworks. Just MongoDB, Prefect, and Python. |
| **Target audience** | AI/ML engineers evaluating build-vs-buy for RAG/GraphRAG systems, developers frustrated with LangChain's abstractions, backend engineers who want to understand what infrastructure tools actually give you vs what frameworks pretend to give you. |

### Outline

1. The LangChain detour: I tried MongoDBGraphStore first, hit walls the moment I needed custom ontologies, immutable logs, and graph traversal. The framework's assumptions didn't match my requirements.
2. The realization: the hard parts of GraphRAG aren't the parts frameworks abstract away. The hard parts are infrastructure — durable storage, aggregation pipelines, vector search, workflow orchestration.
3. What I built in 2 days: a complete inventory of the system — data pipelines, ontologies, extraction, normalization, immutable logs, materialization, embeddings, hybrid search, graph traversal, visualization, durable workflows.
4. The architecture: infrastructure tools do the hard work (MongoDB, Prefect, Gemini SDK), business logic is custom Python with thin abstractions.
5. MongoDB as the unified memory: one database handling document storage, aggregation pipelines, text search, vector search, and $graphLookup — no separate graph DB, no separate vector store.
6. Prefect as a thin orchestrator: @flow and @task as wrappers around business logic functions, not workflow logic embedded in the framework.
7. No LangChain, no problem: custom BaseLLM + direct Gemini SDK, custom chunking with tiktoken, custom extraction with ontology constraints — simpler, more testable, fully controlled.
8. The lesson: infrastructure tools support your business logic; AI frameworks replace it. When you know what to build, from-scratch is faster and more powerful.

---

### Full body

#### The LangChain detour

I started with LangChain. Of course I did — everyone does. The `MongoDBGraphStore` from `langchain-mongodb` gave me a working knowledge graph in 10 minutes. I could extract entities, store them, query them. It felt like progress.

Then I tried to customize it:

- **Custom ontology?** LangChain's extractor lets the LLM invent types freely. From 5 documents I got 17 node types and 34 relationship types including `"part_of"`, `"Part Of"`, and `"part of"` as three separate types. The `allowed_nodes` parameter exists but the underlying data model — entities with embedded relationship arrays — doesn't change.

- **Immutable logs?** LangChain writes entities directly. There's no observation log, no provenance, no way to trace an entity back to its source chunk. If you want event sourcing, you're on your own — and the framework's storage model doesn't support it.

- **Graph traversal?** `$graphLookup` requires edges as separate documents in the same collection as nodes. LangChain stores relationships as embedded arrays inside entity documents. You'd need to restructure the entire collection to enable traversal.

- **Duplicate detection?** Relationships are parallel arrays (`target_ids`, `types`, `attributes`). A `mongosh` scan found 30+ entities with duplicate relationships. Dedup means scanning every `(target_id, type)` pair in every document. No index helps.

Each customization was a fight. Not because LangChain's code is bad — but because its assumptions (embedded relationships, no ontology enforcement, no log/materialization split) are architectural. You can't configure your way out of a data model mismatch.

So I scrapped it and built from scratch.

#### What I built in 2 days

Here's the complete inventory of what I shipped:

**Data pipelines:**
- Substack RSS ingestion ETL (fetch → parse → extract references → deduplicate → persist)
- Idempotent by `source_uri` — re-running the pipeline won't create duplicates
- Reference resolution between documents via hyperlink extraction

**Ontology and schemas:**
- 6 node types (`DOCUMENT`, `CHUNK`, `PERSON`, `TASK`, `EPISODE`, `PREFERENCE`) as Python StrEnums
- 8 edge types with directional constraints enforced at extraction time
- Pydantic attribute schemas for each node type (sent to the LLM as the extraction contract)
- Split into LLM-extractable types (semantic entities) and structural types (metadata-derived)

**Extraction pipeline:**
- Token-bounded chunking with tiktoken (512 tokens, 64 overlap)
- Parallel LLM extraction per chunk (semaphore-capped concurrency)
- Structural entry generation (DOCUMENT, CHUNK, PART_OF, NEXT, MENTIONS, REFERENCED — no LLM needed)
- Fuzzy normalization with SequenceMatcher to merge near-duplicate entities
- Immutable log persistence — every observation is a separate document with full provenance

**Materialization:**
- MongoDB aggregation pipeline: `$group` by `{name, type}` for nodes, `{source, target, type}` for edges
- `$mergeObjects` to combine properties from all observations
- Composite IDs (`"type:name"` for nodes, compound dicts for edges) for natural deduplication
- `$unionWith` + `$out` for atomic writes
- Reverse edges for bidirectional `$graphLookup` traversal (scoped to specific node type pairs)

**Embeddings:**
- Computed post-materialization on deduplicated nodes only (244 log entries → 70 nodes = ~3.5x savings)
- Batch processing with bulk_write operations

**Query layer:**
- Vector search (`$vectorSearch`, cosine similarity)
- Text search (`$text` on name, content, aliases)
- Reciprocal Rank Fusion to merge both ranked lists
- Multi-hop graph expansion via `$graphLookup` (outgoing + incoming passes)

**Visualization:**
- NetworkX graph construction from query results
- Interactive HTML rendering with pyvis (color-coded by node type, hover tooltips)

**Durable workflows:**
- All pipelines orchestrated via Prefect with `@flow` and `@task` decorators
- Retries, monitoring, deployment configs

**Supporting infrastructure:**
- Beanie ODM for async MongoDB operations with Pydantic validation
- App configuration split: secrets in `.env` (via pydantic-settings), tuning in YAML
- Fake/mock models for testing without API calls

#### The architecture: infrastructure does the hard work

The system has a clean split between infrastructure tools and business logic:

**Infrastructure handles the hard problems:**

| Tool | What it does | Why it's hard to build yourself |
|------|-------------|-------------------------------|
| **MongoDB** | Document storage, `$group`/`$mergeObjects` aggregation, `$text` search, `$vectorSearch`, `$graphLookup` traversal — all in one database | You'd need 3 separate systems (doc store + vector DB + graph DB) plus glue code |
| **Prefect** | Durable workflow execution, retries (`retries=2, retry_delay_seconds=5`), monitoring dashboard, deployment management | Building reliable workflow orchestration with fault tolerance from scratch is a deep infrastructure problem |
| **Gemini SDK** | LLM inference, embedding computation | Direct API access, no wrapper overhead |
| **Beanie** | Async ODM with Pydantic validation, indexed fields, document relationships | Writing async MongoDB boilerplate with schema validation for every collection |

**Business logic is custom Python:**

| Component | What it does | Why it should be yours |
|-----------|-------------|----------------------|
| **Ontology** | 6 node types, 8 edge types, attribute schemas, edge constraints | Domain-specific. No framework knows your entity types. |
| **Extraction** | Prompt engineering, JSON parsing, ontology validation, constraint enforcement | Your prompt, your validation rules, your error handling. |
| **Normalization** | Fuzzy matching with SequenceMatcher, canonical name mapping, edge remapping | Your similarity threshold, your merge strategy. |
| **Materialization** | Aggregation pipeline design, composite ID format, reverse edge strategy | Your dedup logic, your ID scheme, your traversal needs. |
| **Query fusion** | RRF algorithm, seed selection, graph expansion strategy | Your ranking formula, your hop depth, your result format. |

#### MongoDB as the unified memory

This is the single most important infrastructure decision. MongoDB handles five jobs that would normally require separate systems:

1. **Document storage** — the `documents` collection stores raw ingested content with Beanie ODM.
2. **Aggregation pipelines** — the materialization pipeline uses `$group`, `$mergeObjects`, `$addToSet`, `$unionWith`, `$out` to transform 244 log entries into 70 deduplicated nodes and 104 edges.
3. **Text search** — a standard text index on `name`, `properties.content`, `properties.aliases` enables `$text` queries.
4. **Vector search** — an Atlas vector search index on `embedding` (768 dimensions, cosine similarity) enables `$vectorSearch`.
5. **Graph traversal** — `$graphLookup` walks edges from seed nodes across multiple hops, enabling relationship-aware retrieval.

One database. Three collections. No glue code between a vector store, a graph database, and a document store. The aggregation framework is the workhorse — it handles materialization, deduplication, and search in native MongoDB operations.

#### Prefect as a thin orchestrator

Prefect handles scheduling, retries, and monitoring. It does NOT contain business logic. Every `@task` is a thin wrapper around a pure function:

```python
# The Prefect task — thin wrapper
@task(name="extract-document-to-kg", retries=1, retry_delay_seconds=10, cache_policy=NO_CACHE)
async def extract_document_task(llm: BaseLLM, doc: Document) -> ExtractionResult:
    return await extract_and_store(llm, ...)  # ← actual logic lives here

# The business logic — pure function, testable without Prefect
async def extract_and_store(llm, *, document_id, content, source_type, source_uri, ...):
    chunks = chunk_document(content)
    results = await asyncio.gather(*[extract_entities(llm, chunk) for chunk in chunks])
    structural = build_structural_entries(...)
    combined = llm_result.merge(structural)
    normalised = normalize_nodes(combined)
    await store_log_entries(normalised, source_document_id=document_id)
```

The extraction logic, normalization, structural entry generation — all of it lives in `src/twin/memory/extraction/core.py`, not inside Prefect tasks. I can test it with pytest and mock fixtures. I can run it without a Prefect server. Prefect adds retries, monitoring, and deployment — infrastructure concerns that belong in an orchestrator, not in my code.

#### No LangChain, no problem

The LLM integration is a 2-method abstract class:

```python
class BaseLLM(abc.ABC):
    @abc.abstractmethod
    async def generate_json(self, prompt: str, *, system: str | None = None) -> dict[str, Any]: ...

class BaseEmbeddingModel(abc.ABC):
    @abc.abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
```

The Gemini implementation uses the `google-genai` SDK directly — not `langchain-google-genai`. No chain abstractions, no prompt templates, no output parsers. Just an async API call that returns JSON:

```python
class GeminiLLM(BaseLLM):
    async def generate_json(self, prompt, *, system=None):
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                temperature=0,
            ),
        )
        return json.loads(response.text)
```

Chunking uses tiktoken directly — not `langchain-text-splitters`. The extraction prompt is a string with `{ontology}` interpolation — not a LangChain `PromptTemplate`. The output is parsed with `json.loads` and validated against the ontology — not a LangChain `OutputParser`.

Every abstraction LangChain provides for these operations adds overhead without adding value when you know what you're building. The direct approach is simpler, more testable, and gives you full control over error handling, retries, and output validation.

For testing, there are `FakeLLM` and `MockEmbeddingModel` implementations that return canned responses — swap them in via the factory function and tests run without API calls.

#### The lesson

The hard parts of a GraphRAG system are:
- Durable workflow execution with retries and monitoring → **Prefect**
- Document storage + aggregation + text search + vector search + graph traversal → **MongoDB**
- LLM inference and embedding computation → **Direct SDK calls**

These are infrastructure problems. They're genuinely hard to build yourself, they're well-solved by mature tools, and they support your business logic without constraining it.

The easy parts — once you know what to build — are:
- Defining an ontology (two StrEnums and a dict of constraints)
- Writing an extraction prompt (a system prompt with JSON schema)
- Normalizing entities (fuzzy matching with SequenceMatcher)
- Designing a materialization pipeline (MongoDB aggregation stages)
- Implementing search fusion (RRF is 10 lines of code)

These are business logic problems. They're specific to your domain, they change as your requirements evolve, and they should live in your codebase — not behind a framework's abstraction layer.

AI frameworks like LangChain wrap business logic and present it as infrastructure. They give you chains, agents, output parsers, and prompt templates — abstractions over the parts that are actually easy to write yourself. Meanwhile, the actual infrastructure (MongoDB's aggregation framework, Prefect's durable execution, the Gemini API) does the heavy lifting that would take months to replicate.

When the system design is clear in your head, writing from scratch anchored to your business logic is faster and more powerful than fighting a framework's assumptions. Infrastructure tools support your code. AI frameworks replace it. Choose accordingly.

![[assets/diagram-2day-build-inventory.png]]

![[assets/diagram-infra-vs-framework.png]]

![[assets/diagram-mongodb-unified-memory.png]]

![[assets/diagram-system-architecture.png]]
