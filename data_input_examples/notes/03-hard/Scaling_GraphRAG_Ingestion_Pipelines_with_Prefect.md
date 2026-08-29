# Ghostwriter Guide: Scaling GraphRAG Ingestion Pipelines with Prefect

**Sponsored post for Prefect**

**Format:** Step-by-step technical guide following the same architecture diagram (12 numbered steps) used in the MongoDB post, but scoped to the **ingestion pipeline** (Steps 1–8) where Prefect adds value.

**Tone:** Practical, developer-focused. Not a sales pitch — show the pain of running expensive multi-step pipelines without durability, then show how Prefect's primitives solve each pain point naturally. Let the reader conclude "oh, I need an orchestrator here" organically.

**Running example:** Same Digital Twin — ingesting Personal Notes, Research, Email, and Text Messages to build a knowledge graph about Arthur. Use the Arthur/Felix email example and the cat vet data to make costs and failures concrete.

**Key thesis:** The GraphRAG ingestion pipeline has three brutally expensive steps — triple extraction (LLM), entity resolution (LLM + DB), and embedding (API/GPU). At scale (thousands to millions of documents), failures in any of these steps without checkpointing mean re-running everything from scratch, burning tokens and compute. Prefect solves this with two capabilities:

1. **Durable execution with checkpointing** — `@task` result persistence means a failure at Step 6 (embedding) doesn't re-run Steps 4–5 (extraction + resolution). Each expensive step caches its output; retries resume from the last successful checkpoint.
2. **Worker-queue pattern for horizontal scaling** — Work pools + work queues let you fan out document processing across multiple workers, queue jobs to handle ingestion spikes, and set concurrency limits to avoid GPU/memory bottlenecks.

---

## Architecture Context

Reference the same diagram from the MongoDB post. The full pipeline has 12 steps across four zones. **This post focuses on the ingestion side — Steps 1 through 8** — where Prefect acts as the orchestrator. The retrieval/agent side (Steps 9–12) is out of scope.

The three expensive steps in the Memory Pipeline that justify an orchestrator:
- **Step 4 — Graph Extraction:** LLM call per chunk to extract triples. At $0.01–0.05 per document, 100K documents = $1,000–5,000 in LLM costs.
- **Step 5 — Entity Resolution:** LLM + database lookups per extracted entity. Fuzzy matching, deduplication, merging — compute-heavy and failure-prone.
- **Step 6 — Embedding:** API call or GPU inference per node. At $0.0001 per embedding, 1M nodes = $100 — but a batch failure at 900K means re-embedding everything without checkpoints.

---

## The Cost of Fragility (Hook Section)

### Why You Need This Post

Frame the hook around the real cost of running the Memory Pipeline without an orchestrator. Walk through a concrete failure scenario using the Digital Twin example.

**Scenario:** You're ingesting 10,000 documents (emails, Notion notes, articles, SMS) into Arthur's knowledge graph. The pipeline processes each document through Clean → Chunk → Extract Triples → Entity Resolution → Embed → Package → Store.

Document #7,342 fails at the embedding step because the Voyage AI API returns a 429 (rate limit). Without checkpointing:
- Steps 4–5 already completed successfully for this document (LLM extracted 5 triples, entity resolution merged "Art" into "Arthur Iusztin") — that work cost ~$0.03.
- Without result persistence, the retry re-runs extraction and resolution from scratch. $0.03 wasted per retry.
- At 10,000 documents with a 5% failure rate, that's 500 retries x $0.03 = **$15 wasted per batch**. Run this daily and it's **$450/month** in pure waste — just from re-executing already-successful steps.

Now multiply by a real production workload: 100K documents/day, more complex extraction, more expensive models. The waste scales linearly.

**The fix is not "write better error handling."** The fix is an orchestrator that checkpoints after each expensive step so retries resume from the failure point, not from scratch.

---

## Data Pipeline (Steps 1–2) — Light Orchestration

### Step 1 — Collect Data from Sources

Raw data arrives from URIs (articles, YouTube) and personal sources (Notion, GDrive, Gmail, SMS). Each source has its own API, rate limits, and failure modes — the Gmail API throttles differently than the Notion API.

**Prefect angle:** Each source connector is a `@task` with its own retry policy. Gmail API returns 429s? Exponential backoff. Notion API times out? Fast retry. The `@flow` wrapping the collection step fans out across sources using Prefect's `.map()` for concurrent fetching. Each source task caches its result — if Gmail succeeds but Notion fails, the retry only re-fetches from Notion.

### Step 2 — ETL into Data Warehouse

Two ETL paths (Crawl ETL for URIs, Personal Docs ETL for personal sources) normalize raw data into `Document` objects and store them in MongoDB.

**Prefect angle:** Each ETL path is a separate `@task`. The normalization logic (HTML stripping, format conversion) is deterministic and cheap — cache aggressively with `cache_policy=INPUTS` so re-runs of the same source URI skip processing entirely. The ETL flow produces a list of document IDs that feeds into the Memory Pipeline.

---

## Memory Pipeline (Steps 3–7) — This Is the Core. Checkpointing and Scaling Live Here.

### Step 3 — Clean + Chunk

Each document is preprocessed: strip HTML, extract metadata (email headers, Notion properties), normalize text, and chunk long documents. For Felix's email: extract `from: Felix`, `to: Arthur`, `date: 2025-11-15`, clean the body, chunk if needed.

**Prefect angle:** Cleaning and chunking is CPU-bound and cheap — but it's the entry point to the expensive pipeline. Wrap it as a `@task` with `cache_policy=INPUTS` so that if the pipeline fails downstream (at extraction or embedding), retrying the flow skips re-cleaning documents that were already processed. This is your first checkpoint.

**Scaling angle:** Chunking is embarrassingly parallel — each document is independent. Use `.map()` to distribute across chunks. For large batches, this is where the worker-queue pattern starts: submit 10,000 clean+chunk tasks to a work queue and let multiple workers drain it.

### Step 4 — Graph Extraction (LLM Call — Expensive)

An LLM extracts triples (entity → relationship → entity) from each chunk, guided by the ontology. From Felix's email, the LLM produces: `(Felix:Person)-[:MENTIONS]->(email_doc)`, `(Arthur)-[:CONNECTED_TO]->(Felix)`, `(Arthur)-[:HAS]->(Task {content:"Coffee Friday"})`, etc.

**This is the most expensive step.** Each chunk requires an LLM call ($0.01–0.05 depending on model and chunk size). At 100K documents with 3 chunks average = 300K LLM calls.

**Prefect angle — Checkpointing:** Wrap extraction as a `@task` with `retries=3`, `retry_delay_seconds=[1.0, 2.0, 4.0]` (exponential backoff for rate limits), and `cache_policy=INPUTS`. The cache key is derived from the chunk content + model name + ontology version — so identical chunks always hit cache. If the pipeline fails at Step 5 or 6, retrying the flow loads all completed extractions from cache for free. Zero redundant LLM calls.

**Prefect angle — Scaling:** This step is I/O-bound (waiting on LLM API responses). Fan out extraction tasks across a work pool with concurrency limits that match your LLM provider's rate limits. Example: OpenAI allows 10K RPM on tier 3 → set work queue concurrency to ~150 concurrent tasks (assuming ~4s per call). This prevents 429 errors at the source rather than handling them after the fact.

**Use the Felix email as the concrete example:** Show the input (cleaned chunk), the LLM call, the output (triples), and the cached result. Then show what happens when extraction succeeds for 9,500 documents but fails for 500 due to rate limiting — Prefect retries only the 500, loading the 9,500 from cache.

### Step 5 — Entity Resolution (LLM + DB — Expensive)

The LLM extracted "Arthur" from the email, but the graph already has "Arthur Iusztin" with alias "Art". Entity resolution checks existing nodes, runs fuzzy matching, and merges duplicates. "GraphRAG survey" is matched to an existing Document node from GDrive.

**This step is expensive because it combines LLM calls (for fuzzy semantic matching) with database lookups (querying existing nodes).** It's also the most failure-prone — database timeouts, connection pool exhaustion, lock contention on concurrent writes to the same entity.

**Prefect angle — Checkpointing:** Wrap as a `@task` with its own retry policy. Database timeouts get fast retries (`retry_delay_seconds=[0.5, 1.0]`). LLM-based matching gets exponential backoff. Result persistence means a resolved entity (e.g., "Arthur" → "person_arthur") is cached — if embedding fails downstream, entity resolution is not re-run.

**Prefect angle — Scaling:** Entity resolution has a subtle concurrency constraint: two workers might try to resolve "Arthur" simultaneously, creating a race condition. Use Prefect's concurrency limits on the work queue to serialize resolution for the same entity while parallelizing across different entities. Alternatively, batch entities by first letter or hash to partition work across workers without conflicts.

**Use the "Arthur" / "Art" / "Arthur Iusztin" merge as the example.** Show how the resolution result is cached so that 50 later documents mentioning "Art" all resolve instantly from cache.

### Step 6 — Embedding (API/GPU — Expensive)

Generate vector embeddings: `summary_embedding` on Document nodes, `content_embedding` on Task, Preference, and Episode nodes. Each node requires an API call (Voyage AI, OpenAI) or GPU inference (local model).

**Prefect angle — Checkpointing:** This is where checkpointing pays off most. Embedding is typically the last expensive step before storage. If storage (Step 8) fails — network partition, MongoDB timeout — you don't want to re-embed 100K nodes. Wrap as a `@task` with result persistence. The cache key includes the text content + model version — so re-embeddings only happen when content or model changes.

**Prefect angle — Scaling:** Embedding is the most parallelizable step — zero dependencies between nodes. Fan out across a GPU work pool (if using local models) or an API work pool (if using Voyage/OpenAI). Set concurrency to match your API rate limits or GPU memory. Prefect work pools support different infrastructure types — you can route embedding tasks to a GPU-enabled Docker pool while routing extraction tasks to a CPU-only pool.

**Concrete cost example:** 100K nodes at $0.0001/embedding = $10. A failure at 90K without checkpointing re-runs all 100K = $10 wasted. With Prefect caching, the retry re-embeds only the 10K that failed = $1. At daily runs, that's $270/month saved.

### Step 7 — Package into Knowledge Graph Objects

The output of Steps 4–6 is assembled into Knowledge Graph Objects — each containing triples, vectors, and metadata. This is a pure data transformation step (no external calls).

**Prefect angle:** Cheap and deterministic. Wrap as a `@task` with `cache_policy=INPUTS` for completeness, but this step rarely fails. Its main value as a Prefect task is as a checkpoint boundary — it confirms that extraction, resolution, and embedding all succeeded before attempting the write to storage.

---

## Writing to Unified Memory (Step 8) — Durable Writes

### Step 8 — Store as Immutable Logs

KG Objects are appended to the immutable `kg_events` collection in MongoDB. Each event is a log entry (NodeCreated, RelationshipAdded, etc.) with entity ID, payload, version, and timestamp.

**Prefect angle — Exactly-once writes:** This is where Prefect's idempotency matters. If the write succeeds but the flow fails to record the success (network blip after the MongoDB ACK), a retry could double-write. Prefect's task-level idempotency keys (derived from entity ID + version) prevent duplicate events. Use `@task` with `retries=3` and result persistence — a successful write is cached, so flow-level retries skip it.

**Prefect angle — Batching:** Instead of writing one event at a time, batch KG Objects into groups (e.g., 100 per batch) and write each batch as a single `@task`. This reduces MongoDB round-trips and makes the write step more efficient. If a batch fails, only that batch retries — the other 99 batches are cached.

---

## The Worker-Queue Pattern for Horizontal Scaling — Dedicate a Section to This

### Why the Memory Pipeline Needs Horizontal Scaling

The Memory Pipeline (Steps 3–7) processes each document independently. This makes it embarrassingly parallel — but only if you have the infrastructure to fan out. A single Python process can't saturate a 10K RPM LLM API limit. You need multiple workers.

**The problem without an orchestrator:** You write a multiprocessing script, manage your own job queue (Redis? RabbitMQ?), handle worker failures manually, implement your own dead-letter queue, and build a dashboard to monitor progress. That's months of engineering for infrastructure that has nothing to do with your GraphRAG logic.

**Prefect's worker-queue pattern gives you all of this out of the box:**

1. **Work Pool** — Define your execution infrastructure (Docker containers, K8s pods, ECS tasks, or local processes). The work pool is the "what runs my code" layer.

2. **Work Queues** — Within a pool, create queues with priority and concurrency limits. Example setup for the Memory Pipeline:
   - `extraction-queue` (priority 1, concurrency 50) — LLM extraction tasks, limited to avoid rate limits
   - `resolution-queue` (priority 2, concurrency 20) — entity resolution, lower concurrency to avoid DB contention
   - `embedding-queue` (priority 1, concurrency 100) — embedding tasks, highest parallelism (stateless API calls)

3. **Workers** — Processes that poll work queues and execute tasks. Scale horizontally by adding more workers. Workers can run on different machines, different clouds, or different instance types (CPU for extraction, GPU for embedding).

4. **Concurrency Limits** — Prevent resource exhaustion. If your LLM provider allows 10K RPM, set the extraction queue concurrency so workers collectively don't exceed that limit. No more 429 storms.

**Use a concrete scaling scenario:** Arthur's Digital Twin starts with 1,000 documents (one worker is fine). Six months later, it's 100,000 documents. Show how you go from 1 worker to 10 workers by changing a single configuration — no code changes. The work pool handles infrastructure provisioning, the work queue handles job distribution, and Prefect's UI shows progress across all workers.

**Spike handling:** The agent triggers a bulk ingestion (e.g., Arthur exports 5 years of email). 50,000 documents hit the pipeline at once. Without a queue, your single worker OOMs or your LLM API returns nothing but 429s. With Prefect's work queue, documents are queued and workers drain them at a sustainable rate. The concurrency limit is your pressure valve.

---

## Putting It Together — The Full Orchestrated Pipeline

Show the complete Prefect flow that ties Steps 1–8 together. This is a conceptual code sketch (not full implementation) — just enough to show how the pieces compose.

```python
@task(cache_policy=INPUTS)
def clean_and_chunk(doc: Document) -> list[Chunk]:
    ...

@task(retries=3, retry_delay_seconds=[1.0, 2.0, 4.0], cache_policy=INPUTS)
def extract_triples(chunk: Chunk, ontology: Ontology) -> list[Triple]:
    # LLM call — expensive, must cache
    ...

@task(retries=3, retry_delay_seconds=[0.5, 1.0], cache_policy=INPUTS)
def resolve_entities(triples: list[Triple]) -> list[ResolvedTriple]:
    # LLM + DB lookups — failure-prone, must cache
    ...

@task(retries=3, retry_delay_seconds=[1.0, 2.0, 4.0], cache_policy=INPUTS)
def embed_nodes(nodes: list[Node]) -> list[EmbeddedNode]:
    # API/GPU call — expensive, must cache
    ...

@task(retries=3, cache_policy=INPUTS)
def store_kg_events(kg_objects: list[KGObject]) -> None:
    # MongoDB write — idempotent via entity_id + version
    ...

@flow(name="graphrag-ingestion")
def ingest_documents(doc_ids: list[str]):
    documents = fetch_documents.map(doc_ids)          # Step 1-2
    chunks = clean_and_chunk.map(documents)            # Step 3
    triples = extract_triples.map(chunks, ontology)    # Step 4
    resolved = resolve_entities.map(triples)           # Step 5
    embedded = embed_nodes.map(resolved)               # Step 6-7
    store_kg_events.map(embedded)                      # Step 8
```

**Key point:** Every expensive step is independently cached. If `embed_nodes` fails for document #7,342, the retry loads `extract_triples` and `resolve_entities` results from cache (free) and only re-runs `embed_nodes`. The `.map()` calls distribute work across workers in the pool.

---

## Scheduling and Deployment — Brief Section

### Recurring Ingestion

The Digital Twin needs to ingest new data continuously — new emails arrive, Notion notes get updated, new articles are saved. Prefect handles this with scheduling:

```python
ingest_documents.serve(
    name="daily-ingestion",
    cron="0 2 * * *",  # 2am daily
    parameters={"doc_ids": "new_since_last_run"},
)
```

Or event-driven: a Change Stream on the MongoDB `raw_documents` collection triggers the ingestion flow whenever new documents land. Prefect's event triggers can listen for webhooks or external events to kick off flows on-demand.

### Deploying Workers

Show the deployment model: define a work pool (e.g., Docker on ECS), deploy workers that poll the pool, and submit flows. Workers scale independently — add more during bulk ingestion, scale down during quiet periods.

---

## Trade-offs Section (Brief, Honest)

- **Use Prefect if:** Your ingestion pipeline has 3+ expensive steps (LLM calls, embeddings, DB writes), you process more than a few hundred documents per run, you need scheduling or event-driven triggers, or you need observability into where time and money are spent.
- **Skip Prefect if:** You're ingesting <100 documents total (one-time), your pipeline is a single step (just embedding, no extraction), or you're prototyping and don't care about cost yet.
- **Streaming caveat:** Prefect tasks consume their full execution before returning results. If your pipeline needs real-time token streaming to a UI, handle that outside the Prefect flow.
- **Infrastructure overhead:** Prefect requires a server (self-hosted or Prefect Cloud). For the worker-queue pattern, you need at least one worker process. This is non-trivial infrastructure — but it's infrastructure you'd build anyway (job queue, monitoring dashboard, retry logic) if you're running at scale.

**Honest framing:** Prefect doesn't make your pipeline smarter — it makes it survivable. The GraphRAG logic (extraction, resolution, embedding) is yours. Prefect ensures that when things go wrong (and they will, at scale), you don't pay for the same work twice.

---

## Post Structure Summary

1. **Hook:** The real cost of fragility — a concrete failure scenario showing $450/month wasted on re-running already-successful LLM calls. "Your GraphRAG pipeline has three expensive steps. Without checkpointing, every failure reruns all of them."
2. **Architecture diagram:** Reference the same image, highlight Steps 1–8 as the scope. Call out Steps 4, 5, 6 as the expensive trio.
3. **Data Pipeline (Steps 1–2):** Quick. Light orchestration — concurrent source fetching, ETL caching.
4. **Memory Pipeline (Steps 3–7):** **THIS IS THE CORE.** For each step: what it does, why it's expensive, how `@task` with caching checkpoints it, and how the worker-queue scales it. Use Felix email example for extraction, "Arthur"/"Art" merge for resolution, cost math for embedding.
5. **Step 8 (Storage):** Idempotent writes, batching.
6. **Worker-Queue Pattern:** Dedicated section. Work pools, work queues with priority + concurrency, horizontal scaling from 1 to N workers, spike handling. Concrete scaling scenario (1K → 100K documents).
7. **Full Pipeline Code Sketch:** Conceptual `@flow` + `@task` composition showing all steps.
8. **Scheduling + Deployment:** Brief. Cron, event-driven triggers, worker deployment.
9. **Trade-offs:** Honest, brief. When to use Prefect, when to skip it, streaming caveat.
10. **CTA:** Link to Prefect Cloud, Decoding AI course/newsletter.

---

## Prefect-Specific Details to Weave In

| GraphRAG Pipeline Step | Prefect Primitive | Why It Matters |
|---|---|---|
| Source collection (Step 1) | `@task` with per-source retry policies + `.map()` | Different APIs fail differently — Gmail needs backoff, Notion needs fast retry |
| ETL normalization (Step 2) | `@task` with `cache_policy=INPUTS` | Deterministic transforms cached by input — re-runs skip already-processed sources |
| Clean + Chunk (Step 3) | `@task` with `cache_policy=INPUTS` + `.map()` | First checkpoint before expensive work; embarrassingly parallel |
| Graph Extraction (Step 4) | `@task` with retries + exponential backoff + caching | **Most expensive step.** Cache key = chunk content + model + ontology. Zero redundant LLM calls on retry |
| Entity Resolution (Step 5) | `@task` with fast retries (DB) + backoff (LLM) + caching | Failure-prone (DB contention). Concurrency limits prevent race conditions on same entity |
| Embedding (Step 6) | `@task` with retries + caching; routed to GPU work pool | Last expensive step. Failure here without caching re-runs Steps 4–5. GPU pool separate from CPU pool |
| Package KG Objects (Step 7) | `@task` with `cache_policy=INPUTS` | Lightweight checkpoint — confirms all expensive work succeeded before write |
| Store to MongoDB (Step 8) | `@task` with idempotency keys + retries | Prevents duplicate events on retry. Batch writes reduce round-trips |
| Horizontal scaling | Work pools + work queues with concurrency limits | Fan out across workers; concurrency matches API rate limits and DB capacity |
| Spike handling | Work queues as buffer | Documents queued at ingestion rate, drained at sustainable processing rate |
| Scheduling | `cron`, `interval`, or event-driven triggers | Daily batch ingestion or real-time via MongoDB Change Stream webhooks |
| Observability | Prefect UI — task timing, status, retry history | See exactly which step is the bottleneck, which documents failed, total cost per run |
| Infrastructure routing | Multiple work pools (CPU pool, GPU pool) | Route extraction to CPU workers, embedding to GPU workers — different instance types |

---

## Cost Savings Math to Include

Make this concrete with a table the ghostwriter can drop in:

| Metric | Without Prefect | With Prefect |
|---|---|---|
| Documents/day | 10,000 | 10,000 |
| Failure rate | 5% | 5% |
| Cost per extraction (Step 4) | $0.02 | $0.02 |
| Cost per resolution (Step 5) | $0.01 | $0.01 |
| Cost per embedding (Step 6) | $0.001 | $0.001 |
| Wasted cost per retry (no caching) | $0.031 (re-runs Steps 4–6) | $0 (loads from cache) |
| Retries per day (500 failures) | 500 x $0.031 = **$15.50/day** | 500 x $0.001 = **$0.50/day** (only re-runs failed step) |
| Monthly waste | **$465** | **$15** |
| Annual waste | **$5,580** | **$180** |

At 100K documents/day, multiply by 10x. The savings justify Prefect's infrastructure cost many times over.
