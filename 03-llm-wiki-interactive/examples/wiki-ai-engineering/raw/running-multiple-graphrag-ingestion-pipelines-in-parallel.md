# Running multiple GraphRAG ingestion pipelines in parallel vs. running multiple tasks in parallel within a single ingestion pipeline

**Full note:**

## There are two dimensions of parallelism in Prefect and most engineers only use one

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | You've built a working pipeline with Prefect. You know you can run multiple flow runs in parallel across machines using work pools and workers. But your individual flow runs are still processing items sequentially — one document at a time, one chunk at a time. You're leaving massive performance on the table because you're only parallelizing along one axis. And when you Google "Prefect parallelism," the docs throw ThreadPoolTaskRunner, DaskTaskRunner, RayTaskRunner, and asyncio.gather() at you with no clear guidance on which to use when. |
| **Solution**    | Prefect has two independent parallelism axes: flow-level (work pools + workers — distributing many flow runs across machines) and task-level (task runners — running many tasks concurrently within a single flow run). For async I/O-bound work (API calls, database queries), `asyncio.gather()` with semaphores is the right tool — no task runner needed. For sync CPU-bound work, use `ProcessPoolTaskRunner` or `DaskTaskRunner`. For GPU-aware model inference at scale, `RayTaskRunner` with `remote_options(num_gpus=1)` gives you native GPU scheduling across a cluster. The two axes multiply: 90 concurrent flow runs x 10 concurrent tasks per run = 900 operations in flight. |
| **Transformation** | You can now architect Prefect pipelines that exploit both parallelism dimensions simultaneously, choose the right concurrency primitive for each task type (async I/O vs sync CPU vs GPU), and scale a real GraphRAG system to process 1 million documents in hours instead of weeks. |
| **Hook**        | My GraphRAG pipeline processed documents one at a time. Turns out Prefect has two parallelism axes and I was only using one. |
| **Target audience** | ML/data engineers using Prefect who want to maximize pipeline throughput; engineers building RAG or knowledge graph systems at scale; anyone confused by Prefect's four different task runner options. |

### Outline

1. **Set the scene** — Introduce the digital twin application: a GraphRAG system with three pipelines (data ingestion, memory extraction, materialization) orchestrated by Prefect, and show that the current code processes documents sequentially within each flow run.
2. **Two axes of parallelism** — Explain the fundamental distinction: flow-level parallelism (work pools + workers, across machines) vs task-level parallelism (task runners, within one flow run), and show how they multiply together.
3. **Flow-level parallelism recap** — Briefly cover how submitting 10K flow runs to a work pool with 3 workers gives you 90 concurrent runs — this is the "horizontal" axis most people understand.
4. **Task-level parallelism: the four options** — Deep comparison of asyncio.gather(), ThreadPoolTaskRunner, DaskTaskRunner, and RayTaskRunner — what each does mechanically, when it wins, and when it's the wrong choice.
5. **async/await is not what you think** — The surprising insight that async code with `await task()` in a for loop is sequential, not concurrent. `asyncio.gather()` is what actually gives you concurrency, and it's the right tool for async I/O-bound tasks (not ThreadPoolTaskRunner).
6. **Ray for GPU-heavy workloads at scale** — Deep dive into using RayTaskRunner with `remote_options(num_gpus=1)` for local LLM inference and embedding models, showing how Ray's native GPU scheduling beats Dask for ML workloads.
7. **The 1M document scenario with both axes** — Walk through ingesting 1 million documents through the full pipeline (ingestion → extraction → materialization) using flow-level + task-level parallelism simultaneously, with concrete throughput calculations.
8. **Decision tree and wrap-up** — Simple flowchart for choosing the right concurrency tool based on task characteristics (async I/O vs sync CPU vs GPU).

---

### Full body

#### The application: a digital twin powered by GraphRAG

I'm building a digital twin — a personal knowledge graph that ingests documents from various sources (Substack, YouTube, etc.), extracts entities and relationships via LLM, and materializes them into a queryable graph with vector + text search.

The system has three pipelines orchestrated by Prefect:

```
DATA PIPELINE              EXTRACTION PIPELINE         MATERIALIZATION
RSS Feed URL               Document content            KG log entries
     │                          │                           │
     ▼                          ▼                           ▼
fetch + parse              chunk (512 tokens)          aggregate/dedup
     │                          │                           │
     ▼                          ▼                           ▼
extract document           LLM extract (×5 concurrent) embed nodes
     │                          │                           │
     ▼                          ▼                           ▼
load to MongoDB            normalize + store            reverse edges
                           to KG log                    + indexes

Collection:                Collection:                  Collection:
"documents"                "knowledge_graph_log"        "knowledge_graph"
```

Tech stack: Python 3.14, Prefect 3.6.19, MongoDB 8.2.5 with mongot (vector search), Google Gemini API, Beanie ODM, Docker Compose.

#### The problem: sequential execution hiding in plain sight

Looking at my extraction pipeline, it seems concurrent — it's async Python, uses `await`, all the modern patterns. But here's what it actually does:

```python
# src/twin/memory/extraction/pipeline.py
@flow(name="memory-extraction-etl", log_prints=True)
async def memory_extraction(document_ids: list[str] | None = None):
    # ...
    results: list[ExtractionResult] = []
    for doc in docs:
        result = await extract_document_task(llm, doc)  # BLOCKS until done
        results.append(result)
```

That `await` in a `for` loop means: process document 1, wait until it's completely done, then start document 2. If I have 100 documents, they process one at a time. The `async` keyword doesn't automatically mean concurrent — it just means the function *can* yield control, but only if something else is ready to run on the event loop.

Same problem in my data pipeline:

```python
# src/twin/data/substack/substack_rss_pipeline.py
@flow(name="ingest-substack-rss-feed-etl", log_prints=True)
async def ingest_substack_rss_feed(feed_url: str) -> list[Document]:
    entries = await fetch_feed_task(feed_url)
    documents = [await extract_document_task(entry) for entry in entries]  # ONE AT A TIME

    ingested: list[Document] = []
    for doc, entry in zip(documents, entries):
        result = await load_document_task(doc, entry)  # ONE AT A TIME
```

The irony: I already knew how to fix this. Deeper in the code, my `extract_and_store()` function in `core.py` uses `asyncio.gather()` with a semaphore to process chunks in parallel:

```python
# src/twin/memory/extraction/core.py — THIS is concurrent
semaphore = asyncio.Semaphore(app_config.extraction.llm_concurrency)  # =5

async def _extract(chunk: str, chunk_id: str) -> ExtractionResult:
    async with semaphore:
        return await extract_entities(llm, chunk, chunk_id=chunk_id)

results = await asyncio.gather(
    *[_extract(chunk, cid) for chunk, cid in zip(chunks, chunk_ids)]
)
```

This pattern — `asyncio.gather()` with a semaphore — is the correct way to run async I/O-bound work concurrently. I just wasn't applying it at the higher pipeline levels.

#### The two axes of parallelism in Prefect

Here's the mental model that made everything click:

```
                        FLOW-LEVEL PARALLELISM
                     (Work Pools + Workers)
                     Multiple flow runs across machines

                     Flow Run 1   Flow Run 2   Flow Run 3
                     (doc batch   (doc batch   (doc batch
                      0-99)        100-199)     200-299)
                        │            │            │
                        ▼            ▼            ▼
TASK-LEVEL          ┌────────┐  ┌────────┐  ┌────────┐
PARALLELISM         │task 1  │  │task 1  │  │task 1  │
(Task Runners       │task 2  │  │task 2  │  │task 2  │
 or asyncio)        │task 3  │  │task 3  │  │task 3  │
Multiple tasks      │  ...   │  │  ...   │  │  ...   │
within ONE          │task N  │  │task N  │  │task N  │
flow run            └────────┘  └────────┘  └────────┘
                    Worker A     Worker B     Worker C
```

These two axes are completely independent and they **multiply**:

| | Flow-Level | Task-Level |
|---|---|---|
| **What** | Multiple flow runs in parallel | Multiple tasks within one flow run |
| **Mechanism** | Work pools + workers | Task runners or asyncio.gather() |
| **Where** | Across machines | Within one container/process (or distributed with Dask/Ray) |
| **Controlled by** | Pool concurrency, worker `--limit` | Task runner `max_workers`, semaphores |
| **Your flow code changes?** | No | Yes — `.submit()` or `asyncio.gather()` |

90 flow runs × 10 concurrent tasks per run = 900 operations in flight simultaneously.

#### Flow-level parallelism: the axis most people understand

This is what we covered in the previous article on scaling with Prefect. Quick recap:

1. Deploy your flow to a work pool: `flow.deploy(work_pool_name="cpu-pool")`
2. Start workers on multiple machines: `prefect worker start --pool "cpu-pool" --limit 30`
3. Submit thousands of flow runs: each gets queued, workers drain the queue

```python
# Submit 10K extraction runs, each processing 100 documents
for batch in chunked(all_document_ids, 100):
    await client.create_flow_run_from_deployment(
        deployment.id,
        parameters={"document_ids": batch},
    )
```

With 3 workers at `--limit 30`, you get 90 concurrent flow runs. Each run is independent, self-contained, and can run on any machine. Your flow code doesn't change. You scale by adding machines.

#### Task-level parallelism: the four options

Here's where it gets interesting. Within a single flow run, you have four ways to run tasks concurrently. They solve fundamentally different problems.

##### Option 1: asyncio.gather() — for async I/O-bound tasks

```
┌─────────────────────────────┐
│      Single Thread          │
│      Event Loop             │
│                             │
│  ┌─── coroutine: doc_1 ──┐ │
│  │ await llm.generate()  │ │   While doc_1 waits for the
│  │   (waiting for I/O)   │ │   HTTP response from Gemini,
│  └───────────────────────┘ │   the event loop switches to
│  ┌─── coroutine: doc_2 ──┐ │   doc_2's coroutine. All on
│  │ await llm.generate()  │ │   ONE thread. Zero overhead.
│  │   (running now)       │ │
│  └───────────────────────┘ │
│  ┌─── coroutine: doc_3 ──┐ │
│  │ await db.insert()     │ │
│  │   (waiting for I/O)   │ │
│  └───────────────────────┘ │
└─────────────────────────────┘
```

This is NOT a Prefect feature — it's plain Python. But it's the right tool for my code because all my tasks are `async def` and I/O-bound (Gemini API calls, MongoDB reads/writes, HTTP fetches).

```python
# What my extraction pipeline SHOULD look like
sem = asyncio.Semaphore(10)  # limit concurrent docs

async def _process(doc):
    async with sem:
        return await extract_document_task(llm, doc)

results = await asyncio.gather(*[_process(doc) for doc in docs])
```

**When to use:** All your tasks are `async def` and spend most time waiting for network I/O. This is the cheapest option — zero serialization, zero thread/process overhead, zero setup.

**When NOT to use:** Your tasks are synchronous (blocking), CPU-bound, or need GPU access. `asyncio.gather()` can't help if there's no `await` for the event loop to switch at.

##### Option 2: ThreadPoolTaskRunner — for sync I/O-bound tasks

```
┌─────────────────────────────┐
│     Thread Pool (N threads) │
│                             │
│  Thread 1: task(doc_1)      │   Each task gets its own
│  Thread 2: task(doc_2)      │   thread. OS preemptively
│  Thread 3: task(doc_3)      │   switches between them.
│  Thread 4: task(doc_4)      │   Good for blocking I/O.
│                             │   GIL prevents true CPU
└─────────────────────────────┘   parallelism.
```

```python
from prefect.task_runners import ThreadPoolTaskRunner

@task
def fetch_with_requests(url: str) -> str:
    # Sync, blocking — no await, uses requests library
    return requests.get(url).text

@flow(task_runner=ThreadPoolTaskRunner(max_workers=10))
def ingestion_flow(urls: list[str]):
    futures = [fetch_with_requests.submit(url) for url in urls]
    wait(futures)
```

**When to use:** Your tasks are `def` (not `async def`) and do blocking I/O — e.g., using `requests` instead of `httpx`, or a sync database driver.

**When NOT to use:** Your tasks are async (use `asyncio.gather()` instead) or CPU-bound (GIL will serialize CPU work across threads, giving you zero speedup).

**Key insight for my code:** I don't need this. All my tasks are already async. If I put async tasks on ThreadPoolTaskRunner, each thread would spin up its own event loop — it works but adds unnecessary overhead over plain `asyncio.gather()`.

##### Option 3: DaskTaskRunner — for distributed CPU-bound work

```
┌─────────────────────┐
│  Flow Run Process   │
│  (submitter only)   │           ┌──────────────────────┐
│                     │           │  Dask Cluster         │
│  .submit() ──────────┼──────►  │                      │
│  .submit() ──────────┼──────►  │  Worker 1: task()    │
│  .submit() ──────────┼──────►  │  Worker 2: task()    │
│                     │           │  Worker 3: task()    │
│  wait(futures)      │           │  Worker 4: task()    │
└─────────────────────┘           │                      │
                                  │  Separate processes, │
                                  │  separate machines,  │
                                  │  no GIL limitation   │
                                  └──────────────────────┘
```

```python
from prefect_dask import DaskTaskRunner

@task
def chunk_and_normalize(doc_content: str) -> ExtractionResult:
    # CPU-bound: tokenization, fuzzy matching, parsing
    chunks = chunk_document(doc_content)
    results = [extract_from_chunk(c) for c in chunks]
    return normalize_nodes(merge(results))

# Local cluster — 4 worker processes
@flow(task_runner=DaskTaskRunner(cluster_kwargs={"n_workers": 4, "threads_per_worker": 1}))
def cpu_extraction(docs):
    futures = chunk_and_normalize.map(docs)
    wait(futures)

# Or scale to cloud — auto-scaling Fargate workers
@flow(task_runner=DaskTaskRunner(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    adapt_kwargs={"minimum": 1, "maximum": 20},
))
def cloud_extraction(docs):
    futures = chunk_and_normalize.map(docs)
    wait(futures)
```

**When to use:** Your tasks are sync, CPU-bound, and you need to bypass the GIL (separate processes) or scale beyond one machine. Dask is a mature distributed computing framework with excellent cluster management.

**When NOT to use:** Your tasks are async I/O-bound (use `asyncio.gather()`) or need fine-grained GPU scheduling (use Ray).

**Gotcha:** DaskTaskRunner uses multiprocessing — you must guard your script with `if __name__ == "__main__":` or you'll get fork-related errors. Also, data passed between the flow and Dask workers must be pickle-serializable. For large objects, pass references (document IDs) instead of full content.

##### Option 4: RayTaskRunner — for GPU-aware distributed work

```
┌─────────────────────┐
│  Flow Run Process   │
│  (submitter only)   │           ┌──────────────────────────┐
│                     │           │  Ray Cluster              │
│  with remote_options│           │                          │
│    (num_gpus=1):    │           │  Worker 1 [GPU 0]: task()│
│    .submit() ────────┼──────►  │  Worker 2 [GPU 1]: task()│
│    .submit() ────────┼──────►  │  Worker 3 [CPU]: task()  │
│                     │           │  Worker 4 [CPU]: task()  │
│  wait(futures)      │           │                          │
└─────────────────────┘           │  Native GPU scheduling  │
                                  │  Resource-aware routing  │
                                  └──────────────────────────┘
```

```python
from prefect_ray import RayTaskRunner
from prefect_ray.context import remote_options

@task
def extract_with_local_llm(chunk: str) -> ExtractionResult:
    # Sync, GPU-bound — loads model into VRAM, runs inference
    model = load_llm("LiquidAI/LFM2-Tokenizer")
    return model.generate(chunk)

@task
def embed_with_local_model(texts: list[str]) -> list[list[float]]:
    # Sync, GPU-bound
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
    return model.encode(texts).tolist()

@task
def normalize_results(results: list[ExtractionResult]) -> ExtractionResult:
    # CPU-bound — no GPU needed
    merged = merge_all(results)
    return normalize_nodes(merged)

@flow(task_runner=RayTaskRunner())
def gpu_extraction_flow(chunks: list[str], text_batches: list[list[str]]):
    # Ray allocates 1 GPU + 4 CPUs for each LLM extraction
    with remote_options(num_gpus=1, num_cpus=4):
        extract_futures = extract_with_local_llm.map(chunks)

    # Ray allocates 1 GPU for each embedding batch
    with remote_options(num_gpus=1):
        embed_futures = embed_with_local_model.map(text_batches)

    # CPU-only normalization — no GPU needed
    with remote_options(num_cpus=2):
        norm_future = normalize_results.submit(extract_futures)

    wait([norm_future, *embed_futures])
```

**Why Ray wins for GPU workloads:**

1. **Native GPU scheduling** — `remote_options(num_gpus=1)` is a first-class concept. Ray tracks GPU availability across the cluster and routes tasks to workers that have free GPUs. Dask has resource annotations but they're abstract — you manually declare what your cluster has.

2. **Mixed CPU/GPU in one flow** — In the example above, LLM extraction gets GPUs, normalization gets CPU-only workers. Ray handles the routing. No need for separate work pools or separate flows.

3. **Automatic GPU memory management** — Ray can pack multiple small-GPU tasks onto a single multi-GPU node or spread them across nodes, based on `num_gpus` declarations.

4. **Ray Serve integration** — If you later want to serve the extraction model as a microservice, Ray Serve sits right next to your task runner infrastructure.

**When to use:** Any task that needs GPU — local LLM inference, local embedding models, fine-tuning. Especially when you have mixed CPU/GPU workloads in the same pipeline and need automatic resource allocation.

**When NOT to use:** Pure I/O-bound work (overkill — use asyncio), simple CPU-bound work that fits on one machine (use ProcessPoolTaskRunner), or if you don't have GPU infrastructure.

#### Comparison table

| | asyncio.gather() | ThreadPool | Dask | Ray |
|---|---|---|---|---|
| **Where tasks run** | Same thread, same process | Separate threads, same process | Separate processes, possibly separate machines | Separate processes, possibly separate machines |
| **Parallelism type** | Cooperative (coroutines yield at `await`) | Preemptive threads (OS switches) | True parallelism (separate interpreters) | True parallelism (separate interpreters) |
| **GIL limitation** | N/A (single thread) | Blocks CPU parallelism | No GIL | No GIL |
| **GPU scheduling** | No | No | Manual (resource annotations) | Native (`num_gpus`, `num_cpus`) |
| **Scales beyond 1 machine** | No | No | Yes (Dask cluster) | Yes (Ray cluster) |
| **Data transfer cost** | Zero (shared memory) | Zero (shared memory) | Serialization (pickle) | Serialization (pickle) |
| **Best for** | Async I/O (API calls, DB) | Sync blocking I/O | Distributed CPU work | GPU-aware distributed work |
| **Setup** | Built-in Python | Built-in Prefect | `pip install prefect[dask]` | `pip install prefect[ray]` |

#### Decision tree for my digital twin pipelines

```
Is the task async + I/O-bound?
(Gemini API, MongoDB, HTTP fetch)
│
├── YES → asyncio.gather() + Semaphore
│         No task runner needed.
│         Zero overhead. Already doing this in core.py.
│
└── NO → Is it sync + blocking?
         │
         ├── CPU-bound only?
         │   (chunking, normalization, parsing)
         │   │
         │   ├── Fits on 1 machine → ProcessPoolTaskRunner
         │   │
         │   └── Needs multiple machines → DaskTaskRunner
         │
         └── Needs GPU?
             (local LLM inference, local embeddings, training)
             │
             └── RayTaskRunner with remote_options(num_gpus=N)
```

Pipeline-by-pipeline mapping:

| Pipeline | Today (Gemini API) | Future (Local Models) |
|----------|---|---|
| Data ingestion (HTTP + parse) | `asyncio.gather()` | `asyncio.gather()` (still I/O) |
| Extraction (LLM calls) | `asyncio.gather()` + semaphore | `RayTaskRunner` with `num_gpus=1` |
| Extraction (chunking) | Sequential (fast, pure CPU) | `ProcessPoolTaskRunner` if heavy |
| Extraction (normalization) | Sequential (fuzzy match) | `ProcessPoolTaskRunner` if heavy |
| Materialization (aggregate) | Sequential (MongoDB server-side) | Same (runs in MongoDB) |
| Materialization (embed) | `asyncio.gather()` | `RayTaskRunner` with `num_gpus=1` |
| Materialization (indexes) | Sequential (one-time) | Same |

#### Ray at scale: running local models across a GPU cluster

This is where it gets powerful. Imagine I've replaced Gemini with a local Liquid model for extraction and a local sentence-transformers model for embeddings. A single flow run needs to process 100 documents, each chunked into ~5 chunks = 500 LLM inference calls + 1 embedding batch.

```python
from prefect_ray import RayTaskRunner
from prefect_ray.context import remote_options

@task
def extract_chunk_local(chunk: str) -> ExtractionResult:
    # Each call loads/uses a local LLM on GPU
    # Takes ~2-3 seconds per chunk on an A100
    model = get_cached_llm()  # Ray handles model caching on workers
    raw = model.generate(chunk, system=EXTRACTION_PROMPT)
    return parse_extraction(raw)

@task
def embed_batch_local(texts: list[str]) -> list[list[float]]:
    model = get_cached_embedding_model()
    return model.encode(texts).tolist()

@task
def normalize_and_store(results: list[ExtractionResult], doc_id: str):
    merged = merge_all(results)
    structural = build_structural_entries(doc_id, merged)
    combined = merged.merge(structural)
    normalized = normalize_nodes(combined)
    store_log_entries(normalized, doc_id)
    return normalized

@flow(task_runner=RayTaskRunner(
    address="ray://ray-head:10001",  # Connect to existing Ray cluster
    init_kwargs={"runtime_env": {"pip": ["prefect-ray", "transformers", "sentence-transformers"]}},
))
def extraction_flow_gpu(document_ids: list[str]):
    # Phase 1: Extract chunks with GPU
    all_futures = []
    for doc in load_documents(document_ids):
        chunks = chunk_document(doc.content)
        with remote_options(num_gpus=1, num_cpus=2):
            chunk_futures = extract_chunk_local.map(chunks)
        # Phase 2: Normalize on CPU (depends on extraction completing)
        with remote_options(num_cpus=2):
            norm_future = normalize_and_store.submit(chunk_futures, doc.id)
        all_futures.append(norm_future)

    # Phase 3: Embed all nodes on GPU
    with remote_options(num_gpus=1):
        embed_future = embed_batch_local.submit(get_all_node_texts())

    wait([*all_futures, embed_future])
```

On a Ray cluster with 4× A100 GPUs across 2 nodes:

```
Ray Cluster
├── Node 1 (2× A100)
│   ├── GPU 0: extract_chunk_local (chunk 1) → extract_chunk_local (chunk 5) → ...
│   ├── GPU 1: extract_chunk_local (chunk 2) → extract_chunk_local (chunk 6) → ...
│   └── CPU: normalize_and_store (doc 1) → normalize_and_store (doc 3) → ...
│
├── Node 2 (2× A100)
│   ├── GPU 0: extract_chunk_local (chunk 3) → extract_chunk_local (chunk 7) → ...
│   ├── GPU 1: embed_batch_local (batch 1) → embed_batch_local (batch 2) → ...
│   └── CPU: normalize_and_store (doc 2) → normalize_and_store (doc 4) → ...
```

Ray automatically routes GPU tasks to nodes with free GPUs and CPU tasks to any available worker. No manual scheduling. No separate work pools for GPU vs CPU. It all happens within one flow run.

#### The 1M document scenario: both axes combined

Here's how the full system would look when processing 1 million documents through the complete pipeline, using flow-level AND task-level parallelism:

**Infrastructure:**

```
Prefect Server
├── Work Pool: "cpu-pool" (docker, concurrency: 100)
│   └── 3 CPU workers, --limit 30 each
├── Work Pool: "gpu-pool" (docker, concurrency: 8)
│   └── 2 GPU workers, --limit 4 each (Ray cluster inside)
└── Global concurrency limits:
    ├── "gemini-api": 150 (if still using Gemini)
    └── "mongodb-writes": 200
```

**Phase 1: Data Ingestion (cpu-pool, asyncio.gather within each run)**

```
Submit: 1,000,000 flow runs (1 per document/feed URL)
Workers: 3 × --limit 30 = 90 concurrent runs
Within each run: asyncio.gather for extract + load (parallel within feed)

                    cpu-pool queue
                    ┌───────────────────────────┐
                    │ 999,910 Scheduled │ 90 Run│
                    └───────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Worker A     Worker B     Worker C
          30 runs      30 runs      30 runs
          each with    each with    each with
          asyncio      asyncio      asyncio
          .gather()    .gather()    .gather()

Throughput: ~18 runs/sec → ~1M in ~15 hours
```

**Phase 2: Memory Extraction (gpu-pool, RayTaskRunner within each run)**

```
Submit: 10,000 flow runs (batch of 100 docs each)
Workers: 2 GPU workers, --limit 4 each = 8 concurrent runs
Within each run: RayTaskRunner processes 100 docs × 5 chunks = 500 tasks
  - GPU tasks: LLM extraction (num_gpus=1)
  - CPU tasks: normalization

                    gpu-pool queue
                    ┌──────────────────────────┐
                    │ 9,992 Scheduled │ 8 Run  │
                    └──────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
               GPU Worker A  GPU Worker B
               4 flow runs   4 flow runs
               each with     each with
               Ray cluster   Ray cluster
               (4 GPUs)      (4 GPUs)

8 runs × 500 chunks ÷ 4 GPUs per worker = massive throughput
Each GPU processes ~1 chunk every 2-3 seconds
Throughput: ~1,000 chunks/sec across cluster
1M docs × 5 chunks = 5M chunks → ~1.4 hours [VERIFY]
```

**Phase 3: Materialization (cpu-pool, sequential tasks — correct)**

```
Submit: 1 flow run
Steps: aggregate → reverse edges → embed → index
  - Aggregate: MongoDB server-side ($group + $out), minutes
  - Embed: RayTaskRunner with GPU for local model, or asyncio for API
  - Index: one-time, seconds

Single run, ~30 minutes
```

**Full timeline with both axes:**

```
TIME ──────────────────────────────────────────────────────────────────►

PHASE 1: DATA INGESTION (1M flow runs, asyncio within each)
├───────────────────────────────────────────────────────────┤
│ ██████████████████████████████████████████████████████████ │  cpu-pool
│ 90 concurrent runs × asyncio.gather() per run             │
│ ~15 hours                                                 │
├───────────────────────────────────────────────────────────┤

PHASE 2: EXTRACTION (10K flow runs, Ray within each)
                                                             ├──────────────────┤
                                                             │ ████████████████ │ gpu-pool
                                                             │ 8 concurrent     │ RayTaskRunner
                                                             │ 4 GPUs per worker│
                                                             │ ~1.4 hours       │
                                                             ├──────────────────┤

PHASE 3: MATERIALIZATION (1 run)
                                                                                ├─────┤
                                                                                │ ███ │
                                                                                │~30m │
                                                                                ├─────┤
```

#### Key takeaways

1. **Two axes multiply.** Flow-level parallelism (work pools) distributes runs across machines. Task-level parallelism runs tasks concurrently within each run. Use both.

2. **async/await ≠ concurrent.** `await task()` in a for loop is sequential. `asyncio.gather()` is what gives you concurrency. For async I/O-bound tasks (API calls, DB queries), this is the right tool — no task runner needed.

3. **ThreadPoolTaskRunner is for sync I/O.** If your tasks use `requests.get()` instead of `await httpx.get()`, threads unblock them. But for async code, it adds overhead without benefit.

4. **DaskTaskRunner is for distributed CPU.** Bypasses the GIL with separate processes. Scales to cloud clusters (Fargate, Kubernetes). Best for heavy CPU work that doesn't need GPUs.

5. **RayTaskRunner is for GPU-aware scheduling.** `remote_options(num_gpus=1, num_cpus=4)` gives you native GPU allocation per task. Mixed CPU/GPU workloads in one flow. The right choice when you run local models at scale.

6. **Your flow code stays the same across scaling stages.** Today: `asyncio.gather()` with Gemini API. Tomorrow: `RayTaskRunner` with a local Liquid model. The deployment target changes (`work_pool_name`), the task runner changes (`task_runner=RayTaskRunner()`), but your business logic — chunk, extract, normalize, store — doesn't.

![[assets/diagram-asyncio-event-loop.png]]

![[assets/diagram-both-axes-timeline.png]]

![[assets/diagram-dask-task-runner.png]]

![[assets/diagram-decision-tree.png]]

![[assets/diagram-ray-task-runner.png]]

![[assets/diagram-three-pipelines.png]]

![[assets/diagram-two-axes-parallelism.png]]
