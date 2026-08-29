# Deep dive on how to scale your GraphRAG ingestion pipeline with Prefect with the worker-queue pattern

[Post](https://www.linkedin.com/feed/update/urn:li:share:7436684045205278720/)

Full note:

## I scaled my GraphRAG pipelines from 1 machine to 100 without changing a single line of flow code

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | You've built a working GraphRAG pipeline — data ingestion, knowledge extraction, materialization — running on a single machine with Prefect's `serve()`. It works for 50 documents. But now you have 1 million records, and your single-process setup would take weeks. You need to distribute work across multiple machines, but you don't want to rewrite your pipeline code or adopt a complex distributed computing framework. |
| **Solution**    | Prefect's three-layer architecture — Server (coordinator), Work Pools (typed queues), Workers (execution agents) — lets you scale from a single `serve()` process to dozens of distributed Docker workers to auto-scaling Kubernetes or serverless Cloud Run, all by changing one deployment line: `serve(flow.to_deployment(...))` becomes `flow.deploy(work_pool_name="...")`. Your flow code stays identical. You control concurrency at four layers (pool, queue, worker, global limits) and separate GPU from CPU workloads with distinct work pools. |
| **Transformation** | You can now take any Prefect-orchestrated pipeline and scale it horizontally across machines with a clear, staged migration path — no code rewrites, no new frameworks, just infrastructure configuration. You also understand exactly how to prevent resource exhaustion (API rate limits, GPU contention) with Prefect's concurrency controls. |
| **Hook**        | I had 1 million documents to turn into a knowledge graph. My single-machine pipeline would've taken weeks. Here's how I scaled it to hours without touching my flow code. |
| **Target audience** | ML/data engineers building pipelines with Prefect who've outgrown single-machine execution; engineers evaluating Prefect for distributed workloads; anyone building RAG or knowledge graph systems at scale. |

### Outline

1. **Set the scene** — Introduce the personal assistant / digital twin application: a GraphRAG system that ingests documents, extracts knowledge graphs via LLM, materializes them into a queryable graph, and explain why it needs to scale.
2. **How the app talks to Prefect today** — Walk through the current setup: `serve()` mode, how scripts submit jobs via `create_flow_run_from_deployment`, and why this hits a wall at scale.
3. **Prefect's three-layer model** — Explain Server → Work Pools → Workers with a clear diagram, emphasizing that the server never executes code and work pools are just database queues.
4. **The role of work pools, queues, and workers** — Deep dive into how work pools act as typed queues, how priority queues enable waterfall scheduling within a pool, how workers poll and claim runs, and how multiple workers on the same pool create horizontal scaling.
5. **Step-by-step scaling path** — Stage 1: `serve()` (where we are). Stage 2: Docker work pool + multiple workers (the practical next step). Stage 3: Kubernetes or Push pools for auto-scaling (production).
6. **End-to-end: 1 million records through three pipelines** — Walk through submitting 1M data pipeline runs, then 10K batched extraction runs, then 1 materialization run, with concrete throughput numbers, queue drain rates, and concurrency controls at each phase.
7. **GPU vs CPU work pool separation** — Show how to split pipelines across pools based on compute profile, with Docker `device_requests` for GPU access and cost optimization patterns.
8. **The four layers of concurrency control** — Pool limits, queue priority, worker `--limit`, and global concurrency limits (protecting external APIs like Gemini).
9. **Wrap-up** — The key insight: your flow code never changes, only the deployment target. The scaling is purely an infrastructure concern.

---

### Full body

#### The application: a personal assistant powered by GraphRAG

I'm building a digital twin — a personal knowledge graph constructed from my content (Substack articles, YouTube transcripts, markdown notes). The system has three pipelines:

**Pipeline 1: Data Ingestion** — Fetches RSS feeds, parses them, extracts documents, deduplicates, and persists to MongoDB.

```python
@flow(name="ingest-substack-rss-feed-etl")
async def ingest_substack_rss_feed(feed_url: str) -> list[Document]:
    raw_entries = await fetch_feed_task(feed_url)
    documents = []
    for entry in raw_entries:
        doc = await extract_document_task(entry)
        loaded = await load_document_task(doc, entry)
        if loaded:
            documents.append(loaded)
    return documents
```

**Pipeline 2: Memory Extraction** — Takes documents, chunks them (512 tokens, 64 overlap), sends each chunk to Gemini for entity/relationship extraction (with a semaphore of 5 for concurrent LLM calls), normalizes via fuzzy matching (threshold=0.85), and stores to an immutable `knowledge_graph_log` collection.

```python
@flow(name="memory-extraction-etl")
async def memory_extraction(document_ids: list[str] | None = None):
    # Fetches documents, chunks them, extracts entities via LLM
    # Stores NodeLogEntry and EdgeLogEntry to knowledge_graph_log
```

**Pipeline 3: Materialization** — Aggregates the immutable log into a deduplicated `knowledge_graph` collection, computes embeddings (Gemini text-embedding-004, 768 dims, batches of 64), creates reverse edges for bidirectional `$graphLookup` traversal, and ensures text + vector search indexes (via MongoDB mongot).

```python
@flow(name="memory-materialization-etl")
async def memory_materialization():
    await materialize_task()           # MongoDB $group + $unionWith + $out
    await create_reverse_edges_task()  # Bidirectional graph traversal
    await embed_nodes_task()           # Gemini embeddings, batch_size=64
    await ensure_indexes_task()        # Text index + vector search index
```

The tech stack: Python 3.14, Prefect 3.6.19, MongoDB 8.2.5 with mongot (vector search), Google Gemini API, Beanie ODM, Docker Compose.

#### How the app talks to Prefect today

Currently, everything runs via `serve()` — a single long-lived process that listens for runs and executes them as local subprocesses:

```python
# src/twin/orchestrator.py
from prefect import serve

serve(
    ingest_substack_rss_feed.to_deployment(
        name="ingest-substack-rss-feed-etl",
        tags=["data-pipeline", "substack"],
    ),
    memory_extraction.to_deployment(
        name="memory-extraction-etl",
        tags=["memory-pipeline", "extraction"],
    ),
    memory_materialization.to_deployment(
        name="memory-materialization-etl",
        tags=["memory-pipeline", "materialization"],
    ),
)
```

Scripts submit jobs via the Prefect client:

```python
# scripts/run_data_pipeline.py
async with get_client() as client:
    deployment = await client.read_deployment_by_name(DEPLOYMENT_NAME)
    flow_run = await client.create_flow_run_from_deployment(
        deployment_id=deployment.id,
        parameters={"feed_urls": feed_urls},
    )
```

The Docker Compose setup runs a Prefect server container (`prefecthq/prefect:3-latest` on port 4200) and a worker container that executes `uv run python -m twin.orchestrator`. The worker connects via `PREFECT_API_URL=http://prefect-server:4200/api`.

This works for development. For 50 documents, it's fine. But `serve()` means one process, one machine, roughly one flow run at a time. For 1 million records, this would take weeks.

#### Prefect's three-layer architecture

Prefect separates "what to run" from "where to run it" through three layers:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: ORCHESTRATION — Prefect Server / Cloud                │
│                                                                 │
│  Stores deployments, queues flow runs, tracks state, enforces   │
│  concurrency limits, serves UI + REST API.                      │
│  NEVER executes your code.                                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  LAYER 2: WORK POOLS — Typed queues in the server's database    │
│                                                                 │
│  Bridge between orchestration and infrastructure. Each pool     │
│  has a type (docker, kubernetes, cloud-run:push). Holds         │
│  scheduled runs. Enforces pool-level concurrency.               │
│  NOT separate processes — just database constructs.             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  LAYER 3: WORKERS — Polling agents on YOUR infrastructure       │
│                                                                 │
│  Poll their assigned work pool every ~15 seconds. Claim runs.   │
│  Provision infrastructure (container, pod, process). Execute.   │
│  Multiple workers can poll the same pool = horizontal scaling.  │
└─────────────────────────────────────────────────────────────────┘
```

The server is the central coordinator — the single source of truth. It holds the queue, tracks every run's state (`Scheduled` → `Pending` → `Running` → `Completed`/`Failed`/`Crashed`), and prevents two workers from claiming the same run. But it never runs your code.

Work pools are not separate processes. They're logical queues stored in the server's database. When you call `create_flow_run_from_deployment`, the server creates a flow run in `Scheduled` state and places it in the target work pool's queue.

Workers are lightweight processes running on your machines. They poll the server, claim scheduled runs, spin up the execution environment (a Docker container, a K8s pod, a subprocess), and report state transitions back. Workers never talk to each other — only to the server.

#### Work pools, queues, and workers in detail

**Work pool types determine what infrastructure runs the flow:**

| Type | Infrastructure | Worker Required |
|------|---------------|-----------------|
| `process` | Local subprocess | Yes |
| `docker` | Docker container per run | Yes |
| `kubernetes` | K8s Job/Pod per run | Yes |
| `cloud-run:push` | GCP Cloud Run | No (push) |
| `ecs:push` | AWS ECS Fargate | No (push) |
| `prefect:managed` | Prefect Cloud infra | No (managed) |

**Priority queues within a pool:**

Each work pool has a default queue, but you can add more with different priorities:

```
Work Pool: "cpu-pool" (pool-level concurrency limit: 50)
│
├── Queue "critical"    (priority: 1, concurrency: 5)
├── Queue "standard"    (priority: 5, concurrency: 30)
└── Queue "backfill"    (priority: 10, concurrency: 15)
```

Workers drain queues in priority order — this is a **waterfall pattern, not round-robin**. All `critical` runs must execute before any `standard` run starts. This is important and not what most people expect from a "priority" system.

**Workers and horizontal scaling:**

Multiple workers can poll the same work pool. Runs are distributed first-come-first-served — whichever worker polls and claims a run first, executes it. There's no load balancing algorithm; it's pure queue contention.

```
                    Prefect Server
                         │
                    Work Pool: "cpu-pool"
                    (1000 flow runs queued)
                   /        |         \
            Worker A     Worker B     Worker C
          (Machine 1)  (Machine 2)  (Machine 3)
          --limit 20   --limit 20   --limit 10
```

Each worker's `--limit` flag controls how many concurrent flow runs it will execute. A worker with `--limit 20` will run up to 20 Docker containers simultaneously on that machine.

Workers send heartbeats every 30 seconds. If a worker misses 3 consecutive heartbeats (~90 seconds), it's marked offline.

#### Step-by-step scaling path

##### Stage 1: `serve()` — Where we are now

```
┌──────────────────────────────────────────────┐
│              Single Machine                  │
│                                              │
│  ┌──────────────┐    ┌───────────────────┐   │
│  │Prefect Server│◄───│ orchestrator.py   │   │
│  │  (Docker)    │    │ serve() process   │   │
│  └──────────────┘    │ ~1 run at a time  │   │
│                      └───────────────────┘   │
│                                              │
│  Throughput: ~1 flow run at a time           │
│  Scaling: None                               │
└──────────────────────────────────────────────┘
```

Limitations: single process, single machine, if it crashes all deployments go offline.

##### Stage 2: Docker work pool + multiple workers

Replace `serve()` with `flow.deploy()`:

```python
# The change: serve() → deploy()
ingest_substack_rss_feed.deploy(
    name="ingest-substack-rss-feed-etl",
    work_pool_name="cpu-pool",
    image="my-registry/twin:latest",
    tags=["data-pipeline", "substack"],
)
```

Create the pool and start workers on multiple machines:

```bash
prefect work-pool create "cpu-pool" --type docker

# Machine 1
prefect worker start --pool "cpu-pool" --type docker --limit 10 --name "worker-$(hostname)"
# Machine 2
prefect worker start --pool "cpu-pool" --type docker --limit 10 --name "worker-$(hostname)"
# Machine 3
prefect worker start --pool "cpu-pool" --type docker --limit 10 --name "worker-$(hostname)"
```

```
┌───────────────────────────────────────────────────────────────┐
│                      Prefect Server                           │
│                                                               │
│   Work Pool: "cpu-pool" (type: docker, concurrency: 30)       │
│   ┌─────────────────────────────────────────────────────┐     │
│   │  Queue: 847 Scheduled │ 30 Running │ 123 Completed  │     │
│   └─────────────────────────────────────────────────────┘     │
└──────────┬──────────────────┬──────────────────┬──────────────┘
           │ poll              │ poll              │ poll
     ┌─────▼──────┐     ┌─────▼──────┐     ┌─────▼──────┐
     │  Worker A   │     │  Worker B   │     │  Worker C   │
     │  Machine 1  │     │  Machine 2  │     │  Machine 3  │
     │  --limit 10 │     │  --limit 10 │     │  --limit 10 │
     └─────────────┘     └─────────────┘     └─────────────┘
```

Throughput: 30 concurrent flow runs across 3 machines. Want more? Add machines.

##### Stage 3: Auto-scaling with Kubernetes or Push pools

**The flow code doesn't change.** Only the deployment target:

```python
# Kubernetes — one worker, K8s creates pods, cluster autoscaler adds nodes
memory_extraction.deploy(
    name="memory-extraction-etl",
    work_pool_name="k8s-pool",           # ← only this changes
    image="my-registry/twin:latest",
)
```

```python
# Cloud Run Push — no worker at all, Prefect submits directly
memory_extraction.deploy(
    name="memory-extraction-etl",
    work_pool_name="cloudrun-pool",      # ← only this changes
    image="gcr.io/my-project/twin:latest",
)
```

The migration path:

```
serve()  ──►  Docker pool + workers  ──┬──►  Kubernetes pool (cluster autoscaler)
                                       │
                                       └──►  Push pool (Cloud Run / ECS — no workers)
```

#### End-to-end architecture diagram

The full path from app to execution across all infrastructure options:

```
                        ┌─────────────────────────────┐
                        │     Your App / Scripts       │
                        │                              │
                        │  client.create_flow_run_     │
                        │    from_deployment(          │
                        │      parameters={...}        │
                        │    )                         │
                        └──────────────┬───────────────┘
                                       │ REST API
                                       ▼
              ┌────────────────────────────────────────────────────┐
              │               PREFECT SERVER / CLOUD               │
              │                                                    │
              │  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
              │  │  Work Pool   │ │  Work Pool   │ │ Work Pool  │ │
              │  │  "cpu-pool"  │ │  "gpu-pool"  │ │  "cloud"   │ │
              │  │  type:docker │ │  type:docker  │ │  type:push │ │
              │  │  limit: 50   │ │  limit: 4     │ │  limit:200 │ │
              │  └──────┬───────┘ └──────┬───────┘ └─────┬──────┘ │
              └─────────┼───────────────┼───────────────┼─────────┘
                        │               │               │
                    HYBRID           HYBRID           PUSH
                        │               │               │
          ┌─────────────┤               │               │
          ▼             ▼               ▼               ▼
   Docker Workers    Docker Worker   K8s Worker     Cloud Provider
   (CPU machines)    (GPU machine)   (creates Jobs)  (auto-scales)
   --limit 30        --limit 1       cluster scales   no worker needed
   ┌──┐┌──┐┌──┐     ┌──────────┐    ┌──┐┌──┐┌──┐   ┌──┐┌──┐┌──┐
   │C ││C ││C │...  │ GPU run  │    │P ││P ││P │.. │CR││CR││CR│..
   └──┘└──┘└──┘     └──────────┘    └──┘└──┘└──┘   └──┘└──┘└──┘
```

#### How scaling differs by pool type

| Pool Type | Who Scales | How | Ops Burden |
|-----------|-----------|-----|------------|
| Docker/Process | You | Manually start/stop workers on machines | High |
| Kubernetes | K8s cluster autoscaler | Automatically adds/removes nodes for pending pods | Medium |
| Push (Cloud Run, ECS) | Cloud provider | Serverless, scales to zero when idle | Low |
| Managed | Prefect Cloud | Fully managed | None |

For Docker pools, to auto-scale you'd wrap it yourself — e.g., a VM autoscaling group where each VM starts a worker on boot. Prefect doesn't manage that.

For Kubernetes, the worker creates a K8s Job per flow run. The cluster autoscaler sees pending pods and provisions nodes. When runs finish, pods terminate, nodes become idle, autoscaler removes them.

For Push pools, there's no worker at all. Prefect submits runs directly to the cloud provider's API. No polling delay, no heartbeats, no VMs. Scales to zero when idle.

#### End-to-end: 1 million records through three pipelines

Setup:

```bash
# Create pools
prefect work-pool create "cpu-pool" --type docker --concurrency-limit 100
prefect work-pool create "gpu-pool" --type docker --concurrency-limit 4

# Protect the Gemini API from rate limiting
prefect gcl create "gemini-api" --limit 150

# Start CPU workers (3 machines, 30 concurrent each)
prefect worker start --pool "cpu-pool" --type docker --limit 30   # × 3 machines

# Start GPU workers (2 GPU machines, 1 concurrent each)
prefect worker start --pool "gpu-pool" --type docker --limit 1    # × 2 machines
```

##### Phase 1: Data Ingestion — 1M flow runs

```python
async def submit_ingestion():
    async with get_client() as client:
        deployment = await client.read_deployment_by_name(
            "ingest-substack-rss-feed/ingest-substack-rss-feed-etl"
        )
        for feed_url in all_1_million_feed_urls:
            await client.create_flow_run_from_deployment(
                deployment.id,
                parameters={"feed_url": feed_url},
            )
```

What happens:

```
t=0s     1,000,000 flow runs enter "Scheduled" in cpu-pool
         ┌──────────────────────────────────────────────────────┐
         │ cpu-pool: 1,000,000 Scheduled                        │
         └──────────────────────────────────────────────────────┘

t=15s    Workers poll, claim first batch (90 runs across 3 workers)
         ┌──────────────────────────────────────────────────────┐
         │ cpu-pool: 999,910 Scheduled │ 90 Running             │
         └──────────────────────────────────────────────────────┘

         Each container runs: fetch RSS → extract document → load to MongoDB

t=...    Steady state: 90 concurrent, ~5s per run (I/O-bound)
         Throughput: ~18 runs/second → ~1,080/min → ~64,800/hour
         1M records ≈ ~15.4 hours

         Want faster?
         6 workers × 30 = 180 concurrent → ~7.7 hours
         10 workers × 30 = 300 concurrent → ~4.6 hours

t=end    ┌──────────────────────────────────────────────────────┐
         │ cpu-pool: 0 Scheduled │ 0 Running │ 1,000,000 Done  │
         └──────────────────────────────────────────────────────┘
         MongoDB "documents" collection: 1,000,000 records
```

##### Phase 2: Memory Extraction — 10K batched runs

Batch 100 documents per flow run instead of 1M individual runs:

```python
for batch in chunked(all_document_ids, 100):
    await client.create_flow_run_from_deployment(
        extraction_deployment.id,
        parameters={"document_ids": batch},
    )
# = 10,000 flow runs, each processing 100 documents
```

Each extraction run: chunks 100 docs (avg 5 chunks each = ~500 chunks), calls Gemini API with semaphore=5, normalizes via fuzzy matching, stores to `knowledge_graph_log`.

```
         ┌──────────────────────────────────────────────────────┐
         │ cpu-pool: 10,000 extraction runs queued              │
         │                                                      │
         │ 90 running concurrently × 5 LLM calls each           │
         │ = 450 concurrent Gemini API calls                    │
         │                                                      │
         │ BUT: global concurrency limit "gemini-api" = 150     │
         │ → only 150 LLM calls system-wide at any time         │
         │ → some runs block, waiting for API slots              │
         └──────────────────────────────────────────────────────┘

         At 90 concurrent, ~45s avg per run:
         Throughput ≈ 2 runs/second ≈ 200 docs/second
         1M documents ≈ ~1.4 hours
```

##### Phase 3: Materialization — 1 single run

```python
await client.create_flow_run_from_deployment(materialization_deployment.id)
```

One heavy flow run:
1. MongoDB aggregation: `$group` → `$unionWith` → `$out "knowledge_graph"` (minutes for 1M docs)
2. Embed all nodes: ~50K unique nodes → batch of 64 → ~800 Gemini API calls
3. Create reverse edges for bidirectional `$graphLookup`
4. Ensure text + vector search indexes (mongot sync, up to 60s)

##### Full timeline

```
TIME ──────────────────────────────────────────────────────────────────►

PHASE 1: DATA INGESTION (1M runs)
├───────────────────────────────────────────────────────────┤
│ ██████████████████████████████████████████████████████████ │ cpu-pool
│ 90 concurrent, draining 1M queue, ~15 hours               │ 3 workers
├───────────────────────────────────────────────────────────┤

PHASE 2: MEMORY EXTRACTION (10K runs)
                                                             ├──────────────────┤
                                                             │ ████████████████ │ cpu-pool
                                                             │ 90 concurrent    │ 3 workers
                                                             │ 5 LLM calls each │
                                                             │ ~1.4 hours       │
                                                             ├──────────────────┤

PHASE 3: MATERIALIZATION (1 run)
                                                                                ├─────┤
                                                                                │ ███ │
                                                                                │~30m │
                                                                                ├─────┤

MongoDB: documents → knowledge_graph_log → knowledge_graph
```

#### GPU vs CPU work pool separation

Currently the app uses Gemini API (cloud-based) — no GPUs needed. But if you switch to local models (local LLaMA for extraction, local sentence-transformers for embeddings), you'd split pools:

```
┌──────────────────────────────────────────────────────────────────┐
│                        Prefect Server                            │
│                                                                  │
│  ┌──────────────────────────┐   ┌──────────────────────────┐     │
│  │ Work Pool: "cpu-pool"    │   │ Work Pool: "gpu-pool"    │     │
│  │ type: docker             │   │ type: docker             │     │
│  │ concurrency: 100         │   │ concurrency: 4           │     │
│  │                          │   │                          │     │
│  │ Deployments:             │   │ Deployments:             │     │
│  │ • data ingestion         │   │ • memory extraction      │     │
│  │   (HTTP fetch, I/O)      │   │   (local LLM inference)  │     │
│  │ • materialization        │   │ • embedding              │     │
│  │   (MongoDB aggregation)  │   │   (local embedding model)│     │
│  │ • reverse edges          │   │ • fine-tuning (future)   │     │
│  │ • index creation         │   │                          │     │
│  └────────────┬─────────────┘   └────────────┬─────────────┘     │
└───────────────┼──────────────────────────────┼───────────────────┘
                │                              │
    ┌───────────▼────────────┐     ┌───────────▼────────────┐
    │ CPU Workers            │     │ GPU Workers            │
    │ (cheap machines)       │     │ (GPU machines)         │
    │                        │     │                        │
    │ Worker 1: --limit 30   │     │ Worker 1: --limit 1    │
    │   (8 vCPU, 16GB RAM)   │     │   (1× A100 80GB)      │
    │ Worker 2: --limit 30   │     │ Worker 2: --limit 1    │
    │   (8 vCPU, 16GB RAM)   │     │   (1× A100 80GB)      │
    │ Worker 3: --limit 30   │     │ Worker 3: --limit 2    │
    │   (8 vCPU, 16GB RAM)   │     │   (2× T4 16GB)        │
    │                        │     │                        │
    │ 90 concurrent runs     │     │ 4 concurrent runs      │
    │ I/O + aggregation      │     │ inference + training   │
    └────────────────────────┘     └────────────────────────┘
```

**Pipeline-to-pool mapping:**

| Pipeline | Pool | Why | `--limit` |
|----------|------|-----|-----------|
| `ingest_substack_rss_feed` | cpu-pool | HTTP fetch + parse, I/O bound | 30 |
| `memory_extraction` (Gemini API) | cpu-pool | Network calls to cloud API | 30 |
| `memory_extraction` (local LLM) | gpu-pool | Local inference needs VRAM | 1 |
| `materialization` — aggregate | cpu-pool | MongoDB aggregation | 30 |
| `materialization` — embed (API) | cpu-pool | Network calls | 30 |
| `materialization` — embed (local) | gpu-pool | Local embedding model | 1-2 |
| Fine-tuning (future) | gpu-pool | Training needs VRAM | 1 |

Docker `device_requests` for GPU access:

```python
memory_extraction.deploy(
    name="memory-extraction-etl",
    work_pool_name="gpu-pool",
    image="my-registry/twin-gpu:latest",
    job_variables={
        "device_requests": [
            {"Driver": "nvidia", "Capabilities": [["gpu"]], "Count": 1}
        ]
    },
)
```

**Cost optimization pattern:** CPU workers run always (cheap). GPU workers spin up only when extraction/embedding runs appear in the queue, then shut down when the queue is empty. With push pools (Cloud Run GPU, Vertex AI), this happens automatically — scales to zero when idle.

#### The four layers of concurrency control

This is the part most people miss. Prefect has four independent concurrency controls, and understanding when each matters prevents both under-utilization and resource exhaustion:

**Layer 1: Work pool concurrency limit** — Total concurrent runs across ALL workers polling that pool. If the pool limit is 100 and 150 runs are scheduled, only 100 run at once.

```bash
prefect work-pool create "cpu-pool" --type docker --concurrency-limit 100
```

**Layer 2: Work queue priority** — Queues within a pool drain in priority order (waterfall). Critical jobs get infrastructure before backfill jobs.

**Layer 3: Worker `--limit`** — Per-machine cap. A worker with `--limit 30` won't run more than 30 containers regardless of queue depth.

```bash
prefect worker start --pool "cpu-pool" --type docker --limit 30
```

**Layer 4: Global concurrency limits** — Server-enforced, slot-based limits that work across all workers and machines. The killer feature for protecting shared resources:

```bash
prefect gcl create "gemini-api" --limit 150
```

```python
from prefect.concurrency.sync import concurrency

@flow
def process_dataset(dataset_id: str):
    with concurrency("gemini-api", occupy=1):
        # Only 150 flow runs can be inside this block at once,
        # across ALL workers and ALL machines
        call_gemini_api(dataset_id)
```

The math that makes this critical: 90 concurrent flow runs × 5 LLM calls per run = 450 concurrent Gemini API calls. Without the global concurrency limit, you'd blow past any API rate limit. With `gcl "gemini-api" --limit 150`, the server centrally enforces that only 150 API calls happen system-wide, regardless of how many workers you add.

Rate limiting is also available: `prefect gcl create "api-calls" --limit 10 --slot-decay-per-second 2.0` — at most 10 concurrent, with slots releasing at 2/second for sustained throughput control.

#### The key insight

Your flow code — `ingest_substack_rss_feed`, `memory_extraction`, `memory_materialization` — never changes when you scale. Not a single line. The scaling is purely an infrastructure concern:

- `serve()` → single process, development
- `flow.deploy(work_pool_name="cpu-pool")` → Docker workers, multi-machine
- `flow.deploy(work_pool_name="k8s-pool")` → Kubernetes, auto-scaling
- `flow.deploy(work_pool_name="cloudrun-pool")` → serverless, zero ops

The three-layer separation (server → work pool → worker) means you can start simple and scale incrementally without ever touching your pipeline logic. That's the whole point.

![[assets/diagram-end-to-end-architecture.png]]

![[assets/diagram-execution-timeline.png]]

![[assets/diagram-gpu-vs-cpu-pools.png]]

![[assets/diagram-scaling-stages.png]]

![[assets/diagram-three-layer-architecture.png]]

![[assets/diagram-workers-horizontal-scaling.png]]
