# I tested all 4 Prefect task runners. Here's the decision tree I wish existed in the docs.

## Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | Prefect offers four ways to run tasks concurrently — asyncio.gather(), ThreadPoolTaskRunner, DaskTaskRunner, and RayTaskRunner — but the documentation presents them side by side with no clear guidance on when each is the right choice. You end up guessing, or worse, picking ThreadPoolTaskRunner for async I/O-bound code (where it adds overhead without benefit) or using asyncio.gather() for CPU-bound work (where it provides zero parallelism). |
| **Solution**    | The choice maps to a simple decision tree based on two questions: Is your task async or sync? Is it I/O-bound, CPU-bound, or GPU-bound? Async I/O → `asyncio.gather()` (no task runner needed). Sync I/O → `ThreadPoolTaskRunner`. CPU-bound → `ProcessPoolTaskRunner` or `DaskTaskRunner`. GPU-bound → `RayTaskRunner` with `remote_options(num_gpus=1)`. Each solves a mechanically different problem at the Python runtime level. |
| **Transformation** | You can now look at any Prefect task and immediately know which concurrency tool to use, avoiding the performance traps of mismatched runners and the overhead of over-engineering simple I/O-bound pipelines. |
| **Hook**        | Prefect has 4 task runners. I put async tasks on ThreadPoolTaskRunner and wondered why it didn't help. Turns out I was solving the wrong problem. |
| **Target audience** | Python engineers using Prefect who need to parallelize task execution; ML/data engineers building pipelines with mixed I/O, CPU, and GPU workloads; anyone confused by Prefect's concurrency options. |

## Outline

1. **The confusion** — Introduce the four options and why the docs don't give you a clear framework for choosing, using the digital twin GraphRAG pipeline as the motivating example.
2. **How async actually works (and doesn't)** — Show that `await task()` in a for loop is sequential, then explain how `asyncio.gather()` creates concurrency on a single thread via cooperative switching during I/O waits. Use the extraction pipeline's actual code as the before/after.
3. **ThreadPoolTaskRunner: what it's actually for** — Explain that threads solve sync blocking I/O (like `requests.get()`), not async I/O. Demonstrate why putting async tasks on a thread pool adds overhead without benefit.
4. **DaskTaskRunner: escaping the GIL** — Show how Dask distributes tasks across separate processes (bypassing the GIL for CPU work) and can scale to remote clusters. Explain when CPU-bound chunking or normalization would benefit.
5. **RayTaskRunner: GPU-aware scheduling** — Deep dive into `remote_options(num_gpus=1, num_cpus=4)` for local model inference. Show mixed CPU/GPU workloads in one flow where Ray routes GPU tasks to GPU workers and CPU tasks anywhere.
6. **The decision tree** — Present the simple flowchart: async I/O → asyncio, sync I/O → ThreadPool, CPU → Dask/ProcessPool, GPU → Ray. Map every pipeline in the digital twin to the right tool.
7. **Gotchas** — Serialization costs with Dask/Ray, Dask's `__main__` guard, futures must be resolved, don't double-parallelize without global concurrency limits.

---

## Full body

### The application

I'm building a digital twin — a personal knowledge graph powered by GraphRAG. The system has three Prefect pipelines:

1. **Data ingestion**: Fetch RSS feeds, parse entries, extract documents, persist to MongoDB
2. **Memory extraction**: Chunk documents (512 tokens), send chunks to an LLM for entity/relationship extraction, normalize via fuzzy matching, store to an immutable `knowledge_graph_log` collection
3. **Materialization**: Aggregate logs into a deduplicated `knowledge_graph`, compute embeddings (768-dim), create reverse edges for bidirectional graph traversal, build text + vector search indexes

Tech stack: Python 3.14, Prefect 3.6.19, MongoDB 8.2.5, Google Gemini API, Beanie ODM.

All my tasks are `async def`. All my I/O is async (httpx for HTTP, Motor for MongoDB, google-genai for Gemini). This turns out to be the most important detail for choosing the right concurrency tool.

### The problem I ran into

My extraction pipeline looked concurrent — it's all async Python. But it was processing documents one at a time:

```python
# src/twin/memory/extraction/pipeline.py
@flow(name="memory-extraction-etl", log_prints=True)
async def memory_extraction(document_ids: list[str] | None = None):
    await init_mongodb(...)
    llm = get_llm()
    docs = await Document.find(...).to_list()

    results: list[ExtractionResult] = []
    for doc in docs:
        result = await extract_document_task(llm, doc)  # SEQUENTIAL
        results.append(result)
```

That `for doc in docs: result = await task(doc)` pattern is sequential. The `await` suspends the calling coroutine until the task completes. The next document doesn't start until the previous one finishes. With 100 documents at ~30 seconds each, that's 50 minutes of serial execution.

The irony: deeper in the same codebase, I already had the correct pattern:

```python
# src/twin/memory/extraction/core.py — extract_and_store()
semaphore = asyncio.Semaphore(app_config.extraction.llm_concurrency)  # =5

async def _extract(chunk: str, chunk_id: str) -> ExtractionResult:
    async with semaphore:
        return await extract_entities(llm, chunk, chunk_id=chunk_id)

results = await asyncio.gather(
    *[_extract(chunk, cid) for chunk, cid in zip(chunks, chunk_ids)]
)
```

`asyncio.gather()` launches all coroutines onto the event loop. While one waits for the Gemini API response, the event loop switches to another. The semaphore caps concurrent calls at 5 to avoid rate limiting. This is the right tool for async I/O — and it's not a Prefect feature, it's plain Python.

My first instinct was to reach for ThreadPoolTaskRunner because that's what the Prefect docs show first. That's when I learned it was the wrong tool for my code.

### How each runner works mechanically

This is the part that made everything click. Each runner solves a fundamentally different problem at the Python runtime level:

#### asyncio.gather() — one thread, cooperative switching

```
┌─────────────────────────────┐
│      Single Thread          │
│      Event Loop             │
│                             │
│  ┌─── coroutine: doc_1 ──┐ │    While doc_1 waits for the
│  │ await llm.generate()  │ │    Gemini HTTP response, the
│  │   (waiting for I/O)   │ │    event loop switches to
│  └───────────────────────┘ │    doc_2. All on ONE thread.
│  ┌─── coroutine: doc_2 ──┐ │    Zero overhead. No
│  │ await llm.generate()  │ │    serialization. No thread
│  │   (running now)       │ │    safety concerns.
│  └───────────────────────┘ │
│  ┌─── coroutine: doc_3 ──┐ │    This is CONCURRENCY,
│  │ await db.insert()     │ │    not parallelism. Nothing
│  │   (waiting for I/O)   │ │    runs at the exact same
│  └───────────────────────┘ │    time. But for I/O waits,
└─────────────────────────────┘    it doesn't matter.
```

How to apply it to my extraction pipeline:

```python
# Fixed: concurrent document processing
sem = asyncio.Semaphore(10)

async def _process(doc):
    async with sem:
        return await extract_document_task(llm, doc)

results = await asyncio.gather(*[_process(doc) for doc in docs])
```

100 documents, 10 concurrent, each taking ~30 seconds = ~5 minutes instead of ~50 minutes.

**When to use:** All your tasks are `async def` and spend most of their time waiting for network I/O (API calls, database queries, HTTP fetches). This describes my entire codebase today — Gemini API for LLM calls, Motor for MongoDB, httpx for RSS fetching.

**When NOT to use:** Your tasks are sync (`def`, not `async def`), CPU-bound (no `await` to yield at), or need GPU access.

#### ThreadPoolTaskRunner — OS threads for sync blocking I/O

```
┌─────────────────────────────┐
│     Thread Pool (N threads) │
│                             │
│  Thread 1: task(doc_1)      │   Each task gets its own OS
│  Thread 2: task(doc_2)      │   thread. The OS preemptively
│  Thread 3: task(doc_3)      │   switches between them.
│  Thread 4: task(doc_4)      │   Threads share memory — zero
│                             │   serialization cost. But the
└─────────────────────────────┘   GIL prevents true CPU
                                  parallelism.
```

```python
from prefect.task_runners import ThreadPoolTaskRunner

# This is a SYNC task — no async, uses blocking requests library
@task
def fetch_with_requests(url: str) -> str:
    return requests.get(url).text  # blocks the thread for seconds

@flow(task_runner=ThreadPoolTaskRunner(max_workers=10))
def ingestion_flow(urls: list[str]):
    futures = [fetch_with_requests.submit(url) for url in urls]
    wait(futures)
```

**When to use:** Your tasks are `def` (not `async def`) and make blocking I/O calls — `requests.get()`, `psycopg2.execute()`, `open().read()`. The thread pool lets multiple blocking calls happen simultaneously.

**When NOT to use:** Your tasks are async (use `asyncio.gather()` instead — putting async tasks on threads means each thread spins up its own event loop, adding overhead without benefit). Also not useful for CPU-bound work because Python's GIL serializes CPU execution across threads.

**This was my mistake.** My tasks are all `async def`. Putting them on ThreadPoolTaskRunner would mean: each thread runs its own event loop → each event loop runs one coroutine → I'm paying thread overhead for zero concurrency benefit. `asyncio.gather()` does the same thing with zero overhead on a single thread.

#### DaskTaskRunner — separate processes, distributed clusters

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
                                  │  Separate Python     │
                                  │  interpreters.       │
                                  │  No GIL. True        │
                                  │  parallelism.        │
                                  └──────────────────────┘
```

```python
from prefect_dask import DaskTaskRunner

@task
def heavy_cpu_normalization(nodes: list[dict]) -> list[dict]:
    # CPU-bound: fuzzy matching N×N pairs, no I/O
    for i, node_a in enumerate(nodes):
        for node_b in nodes[i+1:]:
            ratio = SequenceMatcher(None, node_a["name"], node_b["name"]).ratio()
            if ratio >= 0.85:
                merge(node_a, node_b)
    return nodes

# Local: 4 worker processes on this machine
@flow(task_runner=DaskTaskRunner(cluster_kwargs={"n_workers": 4, "threads_per_worker": 1}))
def normalize_flow(node_batches):
    futures = heavy_cpu_normalization.map(node_batches)
    wait(futures)

# Cloud: auto-scaling Fargate workers
@flow(task_runner=DaskTaskRunner(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    adapt_kwargs={"minimum": 1, "maximum": 20},
))
def cloud_normalize_flow(node_batches):
    futures = heavy_cpu_normalization.map(node_batches)
    wait(futures)
```

**When to use:** Your tasks are sync and CPU-bound — heavy parsing, number crunching, fuzzy matching, image processing. Dask runs each task in a separate Python interpreter, completely bypassing the GIL. Can scale from local processes to cloud clusters (Fargate, Kubernetes) with one config change.

**When NOT to use:** I/O-bound work (overkill — asyncio or threads are cheaper). GPU workloads (Dask has resource annotations but they're manual/abstract — Ray does this natively).

**Tradeoff:** Data must be serialized (pickled) to move between processes. For my digital twin, passing full document content between workers has a cost. Better to pass document IDs and let each Dask worker fetch from MongoDB directly.

For my codebase today: the `normalize_nodes()` function in `core.py` does fuzzy matching with `SequenceMatcher` — it's CPU-bound and could theoretically benefit from Dask. But with typical document volumes (hundreds of nodes per doc), it runs in milliseconds. Not worth the serialization overhead unless processing tens of thousands of nodes.

#### RayTaskRunner — native GPU scheduling

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
└─────────────────────┘           │  Ray tracks GPU memory,  │
                                  │  routes tasks to workers │
                                  │  with free GPUs.         │
                                  └──────────────────────────┘
```

```python
from prefect_ray import RayTaskRunner
from prefect_ray.context import remote_options

@task
def extract_with_local_llm(chunk: str) -> ExtractionResult:
    # Sync, GPU-bound — loads a Liquid model, runs inference
    model = load_llm("LiquidAI/LFM2-Tokenizer")
    raw = model.generate(chunk, system=EXTRACTION_PROMPT)
    return parse_extraction(raw)

@task
def embed_with_local_model(texts: list[str]) -> list[list[float]]:
    # Sync, GPU-bound — sentence-transformers on CUDA
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
    return model.encode(texts).tolist()

@task
def normalize_cpu(results: list[ExtractionResult]) -> ExtractionResult:
    # CPU-only — no GPU needed
    merged = merge_all(results)
    return normalize_nodes(merged)

@flow(task_runner=RayTaskRunner())
def gpu_extraction_flow(chunks, text_batches):
    # GPU tasks: Ray routes to workers with free GPUs
    with remote_options(num_gpus=1, num_cpus=4):
        extract_futures = extract_with_local_llm.map(chunks)

    with remote_options(num_gpus=1):
        embed_futures = embed_with_local_model.map(text_batches)

    # CPU task: Ray routes anywhere
    with remote_options(num_cpus=2):
        norm_future = normalize_cpu.submit(extract_futures)

    wait([norm_future, *embed_futures])
```

**Why Ray wins over Dask for GPU workloads:**

1. **`remote_options(num_gpus=1)` is first-class.** Ray tracks GPU availability across the cluster and routes tasks to workers with free GPUs. With Dask, you manually declare abstract resources on your cluster and annotate tasks — it works, but it's manual bookkeeping.

2. **Mixed CPU/GPU in one flow.** In the example above, LLM extraction gets GPUs, normalization gets CPU-only workers. One `task_runner`, one flow — Ray handles the routing.

3. **Automatic packing.** Ray can pack multiple small tasks onto a single multi-GPU node (e.g., 2 tasks on a 4-GPU machine) or spread them across nodes. No manual `--limit 1` tuning.

**When to use:** Any task that needs a GPU — local LLM inference, local embedding models, fine-tuning. Especially powerful when you have mixed CPU/GPU workloads in the same flow and need automatic resource-aware routing.

**When NOT to use:** Pure I/O-bound work (asyncio is cheaper). Simple CPU-bound work that fits on one machine (ProcessPoolTaskRunner is simpler). If you don't have GPU infrastructure, there's no reason to add the Ray dependency.

**For my codebase today:** Everything runs on the Gemini API — no local models, no GPUs. But if I switch to a local Liquid model for extraction and local sentence-transformers for embeddings, RayTaskRunner with `remote_options(num_gpus=1)` is exactly what I'd need. The flow code stays the same; I just swap the task runner and rewrite the tasks to use local models instead of API calls.

### The comparison table

| | asyncio.gather() | ThreadPool | Dask | Ray |
|---|---|---|---|---|
| **Where tasks run** | Same thread, same process | Separate threads, same process | Separate processes, possibly separate machines | Separate processes, possibly separate machines |
| **Parallelism type** | Cooperative (yields at `await`) | Preemptive (OS switches) | True (separate interpreters) | True (separate interpreters) |
| **GIL limitation** | N/A (single thread) | Blocks CPU work | No GIL | No GIL |
| **GPU scheduling** | No | No | Manual (annotations) | Native (`num_gpus`, `num_cpus`) |
| **Scales beyond 1 machine** | No | No | Yes (Dask cluster) | Yes (Ray cluster) |
| **Data transfer** | Zero (shared memory) | Zero (shared memory) | Serialization (pickle) | Serialization (pickle) |
| **Best for** | Async I/O | Sync blocking I/O | Distributed CPU | GPU-aware distributed |
| **Setup** | Built-in Python | Built-in Prefect | `pip install prefect[dask]` | `pip install prefect[ray]` |

### The decision tree

```
Is the task async + I/O-bound?
(API calls, DB queries, HTTP fetches)
│
├── YES → asyncio.gather() + asyncio.Semaphore()
│         No task runner needed. Zero overhead.
│
└── NO → Is it sync + blocking?
         │
         ├── I/O-bound? (requests.get, psycopg2, file reads)
         │   └── ThreadPoolTaskRunner(max_workers=N)
         │
         ├── CPU-bound? (parsing, matching, crunching)
         │   │
         │   ├── Fits on 1 machine → ProcessPoolTaskRunner
         │   │
         │   └── Needs multi-machine → DaskTaskRunner
         │
         └── GPU-bound? (model inference, training, embeddings)
             └── RayTaskRunner + remote_options(num_gpus=N)
```

### Mapping my digital twin pipelines

| Task | Type | Runner | Why |
|------|------|--------|-----|
| `fetch_feed_task` (HTTP fetch) | Async I/O | `asyncio.gather()` | httpx async client, waiting for HTTP |
| `extract_document_task` (RSS parse) | Async, fast CPU | Direct call | Pure function, milliseconds |
| `load_document_task` (MongoDB write) | Async I/O | `asyncio.gather()` | Motor async driver, waiting for DB |
| `extract_entities` (Gemini API) | Async I/O | `asyncio.gather()` + semaphore | Already correct in `core.py` |
| `extract_entities` (local Liquid model) | Sync GPU | `RayTaskRunner` | GPU inference, `num_gpus=1` |
| `normalize_nodes` (fuzzy match) | Sync CPU | Direct call (or `ProcessPoolTaskRunner` at scale) | Fast for small sets; Dask if >10K nodes |
| `store_log_entries` (MongoDB bulk write) | Async I/O | Direct call | Single bulk insert, fast |
| `materialize_task` (MongoDB aggregation) | Async I/O | Direct call | Server-side aggregation |
| `embed_nodes_task` (Gemini API) | Async I/O | `asyncio.gather()` per batch | API calls, batch of 64 |
| `embed_nodes_task` (local model) | Sync GPU | `RayTaskRunner` | GPU inference, `num_gpus=1` |

### Gotchas I'd warn people about

1. **Don't put async tasks on ThreadPoolTaskRunner.** Each thread spins up its own event loop to run the coroutine. You're paying thread overhead for zero concurrency benefit over plain `asyncio.gather()`.

2. **Dask requires `if __name__ == "__main__":`.** It uses multiprocessing internally. Without the guard, you get fork-related errors or warnings.

3. **Futures must be resolved.** If you `.submit()` tasks and don't call `.wait()`, `.result()`, or return the futures from your flow, tasks may be left in an unfinished state. The Prefect docs explicitly warn about this.

4. **Serialization costs with Dask/Ray.** Data passed to distributed workers must be pickle-serializable. For large objects (full document content), pass references (document IDs) and let each worker fetch from the database. In my case, passing a `Document` Beanie model to a Dask worker would fail because the MongoDB connection isn't serializable.

5. **Don't double-parallelize without global concurrency limits.** If you have 90 flow runs (flow-level) each with 10 concurrent tasks (task-level) making 5 API calls per task, that's 90 × 10 × 5 = 4,500 concurrent API calls. Use `prefect gcl create "gemini-api" --limit 150` to cap it system-wide.

6. **`.submit()` and `.result()` are always synchronous in Prefect.** Even in async flows. The concurrency comes from the task runner managing the thread/process pool, not from async/await.

7. **Ray's `remote_options` is flow-scoped, not task-scoped.** You set resources via a context manager around `.submit()` calls, not on the `@task` decorator. This means the same task can run with different resource allocations in different parts of your flow.

### My take

For most Prefect users building API-driven pipelines (which is most of us — calling OpenAI, Anthropic, Gemini, or any REST API), **you don't need a task runner at all**. `asyncio.gather()` with a semaphore is the right tool, and it's built into Python. The task runners become essential when you move to local models (Ray for GPU), heavy data processing (Dask for CPU), or need to parallelize legacy sync code (ThreadPool).

The Prefect docs would benefit from leading with this decision tree instead of showing all four options as equal alternatives. They solve different problems at different layers of the Python runtime.
