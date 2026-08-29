# How Smooth Is to Use Prefect for Agentic Coding

How smooth was to setup the whole Prefect infrastructure through Docker to orchestrate my ingestion pipelines, add durability and monitoring, make them ready for deployment through Docker and ultimately scale them using queues and multiple workers through Prefect’s self managed cloud. Everything done in ~2 hours with Claude Code. 
Then, highlight how natural and easy Prefect fits in coding with AI agents. Give a reminder that to properly develop code with tools such as Claude Code or OpenAI it’s critical to allow them to run the whole logic on their own, evaluate the output and fix any potential issues. When using plain Python this is easy, but once you start adding infrastructure elements such as an orchestrator that has it’s own domain specific language (DSL) things start to get complicated as it’s super hard to deploy (or re-deploy) your orchestrators workers to actually run your code within the agentic loop. Still the beuty of Prefect is that it makes this possible because Prefect is just decorators on normal Python, the architecture is naturally layered between your pure business logic and Prefect’s code (thus generating code it’s super easy - remember: ai coding agent work best with vanilla code from the core library or packages that are old and stable), serving (or reserving workers) has 0 infrastructure complexity, triggering pipelines is pure Python or bash code, and Dockerization is trivial because there's nothing special to containerize,  allowing the following loop for agentic coding tools:

- Do changes to the code
- Reserve the workers
- Run the pipeline
- Read the output from the pipeline
- Done, or fix the code and restart from step 1 until done

Note: the ultimate learning from this is how to properly write code with agentic doing tools, highlighting that providing the agent the ability to run and debug the code it’s ESSENTIAL to create the autonomous loop you are looking for and provide it the full context.

**Full note:**

## Prefect is the only orchestrator that survives agentic coding

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | AI coding agents (Claude Code, Codex, etc.) are great at writing and debugging plain Python. But the moment you add an orchestrator with its own DSL, config files, or infrastructure ceremony, the agentic loop breaks. The agent can't redeploy an Airflow scheduler, rebuild a Docker image mid-loop, or reload a Dagster code location. It gets stuck waiting for infrastructure it can't control, and the self-correcting cycle dies. |
| **Solution**    | Prefect's `serve()` model turns your entire worker into a plain Python process. The agent's debug loop becomes: edit code, kill the process, restart it in 2 seconds, trigger the pipeline, read the streamed logs, fix errors, repeat. Zero infrastructure overhead. No brokers, no schedulers, no image rebuilds. Combined with trigger scripts that stream Prefect logs to stdout and exit with code 1 on failure, the agent has a complete, self-contained feedback loop it can run autonomously. |
| **Transformation** | You can hand an AI coding agent a full pipeline orchestration task — setup, implementation, Dockerization, scaling — and it can run the entire thing end-to-end without human intervention. The ~2 hour build includes not just the pipelines but the Prefect server, Docker Compose setup, and a documented scaling path to production. |
| **Hook**        | I let Claude Code set up my entire pipeline orchestration. 2 hours later, it had built 4 pipelines, Dockerized everything, and I never intervened once. Here's why Prefect was the only orchestrator that could survive the agentic loop. |
| **Target audience** | ML/AI engineers, data engineers, and software engineers who use AI coding agents (Claude Code, Cursor, Codex, Copilot) for infrastructure-adjacent work and have felt the pain of orchestrators breaking their agentic workflow. Also: anyone evaluating orchestrators and wondering which one plays best with AI-assisted development. |

### Outline

1. Open with the hook: the concrete result (4 pipelines, Docker, scaling path, ~2 hours, zero human intervention) to establish credibility and create curiosity.
2. Set the scene: what I was building (a digital twin system with data ingestion + memory extraction + materialization pipelines) and why orchestration was needed (retries, observability, deployment).
3. Explain the core problem with orchestrators + AI agents: the agentic debug loop requires edit-run-read-fix cycles, and most orchestrators inject infrastructure steps that the agent can't control (DAG parsing, scheduler restarts, image rebuilds, broker connections).
4. Introduce the key insight: Prefect's `serve()` makes the worker a plain Python process with zero infrastructure overhead, which means the agent can kill and restart it in 2 seconds — the same way it restarts any Python script.
5. Walk through the concrete agentic loop step-by-step: (1) edit code, (2) kill & re-serve workers, (3) trigger pipeline via make command, (4) read streamed logs in the terminal, (5) fix or done — showing exactly how each step works in the repo.
6. Highlight the second enabler: trigger scripts that stream Prefect logs to stdout and exit with non-zero codes on failure, giving the agent structured feedback without needing a UI.
7. Show how the same setup scales from dev to Docker to production with zero code changes — the `serve()` call is the same command locally and inside the container.
8. Close with the broader lesson: when choosing tools for AI-assisted development, the deciding factor isn't features — it's whether the tool fits inside the agent's edit-run-read-fix loop. Prefect does. Most orchestrators don't.

---

### Full body

#### The exact situation

I'm building a personal assistant system — a personal knowledge graph powered by MongoDB, LLMs, and agents. The system has three pipeline layers:

1. **Data pipelines** — ETL jobs that ingest content from sources like Substack RSS feeds into a `documents` collection in MongoDB.
2. **Memory extraction pipeline** — Takes documents, chunks them, extracts knowledge graph entities and relationships via an LLM (Gemini), embeds them, and stores them as immutable logs.
3. **Memory materialization pipeline** — Aggregates the logs into queryable views, creates reverse edges, embeds nodes, and builds search indexes.

The stack: Python (async), MongoDB + Beanie ODM, Pydantic, Prefect for orchestration, Docker for deployment, `uv` for dependency management, GNU Make as the command center.

I needed to take these pipelines from "bare Python scripts" to "properly orchestrated, observable, retryable, and deployable." I handed this task to Claude Code (powered by claude-opus-4-6) and let it run.

#### What was surprising

The entire Prefect setup — from first `uv add` to 4 deployed pipelines running in Docker with a Prefect server UI — took roughly 2 hours of agentic coding. I didn't write a single line myself. But what surprised me wasn't the speed — it was that the agent never got stuck on infrastructure. Every other time I've tried to have an AI agent set up an orchestrator, it hits a wall where it can't restart the scheduler, can't reload the DAG, can't rebuild the image. With Prefect, that wall simply didn't exist.

#### The architecture Claude Code built

**Layer 1: Pure Python business logic (zero Prefect awareness)**

The core logic lives in regular Python modules. Functions like `fetch_feed()`, `extract_document()`, `load_document()`, `extract_and_store()`, `materialize()`, `embed_nodes()`. No decorators, no framework imports. Plain async Python.

This is the critical architectural decision. The business logic has no knowledge of Prefect. It can be tested directly, imported anywhere, and debugged without any orchestration context.

**Layer 2: Thin Prefect wrappers**

Each pipeline has a dedicated file that wraps core functions with `@task` and `@flow` decorators:

```python
@task(name="fetch-substack-rss-feed", retries=2, retry_delay_seconds=5)
async def fetch_feed_task(source_uri: str) -> list[dict]:
    return await fetch_feed(source_uri)

@flow(name="ingest-substack-rss-feed-batch-etl", log_prints=True)
async def ingest_substack_rss_feed_batch(feed_urls: list[str]) -> list[Document]:
    await init_mongodb(...)
    results = await asyncio.gather(
        *[ingest_substack_rss_feed(feed_url) for feed_url in feed_urls]
    )
    return [doc for docs in results for doc in docs]
```

Each wrapper is ~30-50 lines. It adds retries, logging, cache policies, and DB initialization on top of core logic. That's it.

**Layer 3: The 19-line orchestrator**

The entire deployment registry is one file — `src/twin/orchestrator.py`:

```python
from prefect import serve

from twin.data.substack.substack_rss_pipeline import (
    ingest_substack_rss_feed,
    ingest_substack_rss_feed_batch,
)
from twin.memory.extraction.pipeline import memory_extraction
from twin.memory.materialization.pipeline import memory_materialization

if __name__ == "__main__":
    serve(
        ingest_substack_rss_feed.to_deployment(
            name="ingest-substack-rss-feed-etl",
            tags=["data-pipeline", "substack"],
        ),
        ingest_substack_rss_feed_batch.to_deployment(
            name="ingest-substack-rss-feed-batch-etl",
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

One `serve()` call. It registers 4 deployments and starts an in-process worker that polls for runs. 19 lines. No YAML. No DAG definitions. No deployment configs.

**Layer 4: Trigger scripts that stream logs to stdout**

This is the secret sauce for the agentic loop. Three trigger scripts (one per pipeline) follow an identical pattern:

```python
async with get_client() as client:
    deployment = await client.read_deployment_by_name(DEPLOYMENT_NAME)
    flow_run = await client.create_flow_run_from_deployment(
        deployment_id=deployment.id,
        parameters={...},
    )

    # Poll and stream logs every 2 seconds
    while True:
        logs = await client.read_logs(log_filter=log_filter, offset=log_offset, limit=100)
        for log in logs:
            print(f"{log.timestamp} | {log.level} | {log.message}")
        log_offset += len(logs)

        run = await client.read_flow_run(flow_run.id)
        if run.state and run.state.is_final():
            if run.state.is_completed():
                print("Done. Flow completed successfully.")
            else:
                print(f"Flow finished with state: {run.state.name}", file=sys.stderr)
                sys.exit(1)  # <-- This is the key signal for the agent
            break
```

The script streams every Prefect log (including task-level errors, tracebacks, retry attempts) to the terminal, and exits with code 1 on failure. The agent sees the full execution output in its bash response. No UI needed.

**Layer 5: Makefile as the command center**

```makefile
serve-workflows:
	uv run python -m src.twin.orchestrator

run-data-pipeline:
	uv run python scripts/run_data_pipeline.py

run-memory-pipeline-extraction:
	uv run python scripts/run_memory_pipeline.py $(DOC_IDS)

run-memory-pipeline-materialization:
	uv run python scripts/run_materialization_pipeline.py
```

Four make targets. The agent doesn't need to remember deployment names or script paths.

**Layer 6: Docker Compose for production**

```yaml
prefect-server:
  image: prefecthq/prefect:3-latest
  ports:
    - "${PREFECT_PORT:-4200}:4200"
  command: ["prefect", "server", "start", "--host", "0.0.0.0"]
  healthcheck:
    test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:4200/api/health')"]

prefect-worker:
  build:
    context: .
    dockerfile: docker/Dockerfile
  depends_on:
    prefect-server:
      condition: service_healthy
    mongodb:
      condition: service_healthy
  environment:
    PREFECT_API_URL: http://prefect-server:4200/api
  command: ["uv", "run", "python", "-m", "twin.orchestrator"]
```

The worker container runs the **exact same command** as local dev: `uv run python -m twin.orchestrator`. The Dockerfile is 8 lines (install uv, sync deps, copy source). Zero code changes between dev and Docker.

#### The core insight: why Prefect survives the agentic loop and other orchestrators don't

When an AI coding agent develops a feature, it runs a tight loop:

```
edit code -> run code -> read output -> fix errors -> repeat
```

This works beautifully for plain Python. The agent edits a file, runs `python script.py`, reads the traceback, fixes the bug, re-runs. Every step takes seconds. The agent can iterate 20+ times in 10 minutes.

The moment you introduce an orchestrator, you insert infrastructure steps into this loop. And that's where things break:

| Orchestrator | What "restart after code change" requires | Time | Agent can do it? |
|---|---|---|---|
| **Airflow** | Restart scheduler + webserver, wait for DAG parsing, hope the parser doesn't choke | 30-60s | Barely — multi-step, fragile |
| **Dagster** | Restart `dagster dev` or reload code location via CLI/UI, re-parse definitions | 15-30s | Possible but error-prone |
| **Celery** | Restart worker process, ensure broker (Redis/RabbitMQ) is connected | 10-20s | Possible if broker is stable |
| **Kubernetes Jobs** | Rebuild Docker image, push to registry, update job spec, wait for pod | 2-5 min | No — too many external systems |
| **Prefect `serve()`** | Kill the Python process, re-run it | ~2s | Trivially — it's just `kill %1 && make serve-workflows &` |

With Prefect's `serve()`, there is **no infrastructure between the code change and the execution**. The worker IS your Python process. Killing and restarting it is the same as restarting any Python script. The agent doesn't need to understand schedulers, brokers, registries, or build pipelines. It restarts a process.

#### The agentic debug loop in practice

This is the exact loop Claude Code runs, guided by instructions in the project's `CLAUDE.md`:

**Step 1: Edit the code.** The agent modifies a core module or pipeline wrapper.

**Step 2: Kill and re-serve.** The agent runs:
```bash
kill %1                    # kill the old worker (just a Python process)
make serve-workflows &     # start new worker with latest code (~2 seconds)
```

This is possible because `serve()` loads flow code at import time. The CLAUDE.md explicitly instructs: *"If a serve process is already running, kill it first and re-serve to pick up the latest code changes."*

**Step 3: Trigger the pipeline.** The agent runs `make run-data-pipeline`. The trigger script creates a flow run via the Prefect client API and starts streaming logs.

**Step 4: Read the output.** The agent sees something like:

```
Flow run created: abc123
2026-03-18 10:15:01 | INFO    | Processing 5 documents for KG extraction
2026-03-18 10:15:03 | ERROR   | Task 'extract-document-to-kg' failed: KeyError: 'source_type'
2026-03-18 10:15:03 | INFO    | Task 'extract-document-to-kg' retrying (attempt 2/2)
2026-03-18 10:15:05 | ERROR   | Task 'extract-document-to-kg' failed: KeyError: 'source_type'

Flow finished with state: Failed
```

All Prefect logs — including task failures, retry attempts, and tracebacks — are streamed directly to the agent's terminal. The `sys.exit(1)` on failure gives the agent an unambiguous signal that something broke. No UI to check. No log files to find. The feedback is inline, in the same context window.

**Step 5: Fix or done.** If the flow failed, the agent reads the error from the streamed logs, edits the code, and goes back to step 1. If it succeeded, it moves on.

This loop runs in seconds per iteration. The agent can self-correct through 10-20 iterations without timing out or losing context.

#### Why this was possible to set up via CLAUDE.md instructions

The `CLAUDE.md` file serves as the agent's runbook. The "Running Pipelines" section (lines 161-180) contains the complete instructions for the agentic loop:

```markdown
To test a pipeline after making changes:

1. Serve the workflows in a background process:
   make serve-workflows &
   If already running, kill it first and re-serve.

2. Run the pipeline via the corresponding Make command:
   make run-data-pipeline
   make run-memory-pipeline-extraction
   make run-memory-pipeline-materialization

Always use these Make commands instead of `prefect deployment run`
directly, as the scripts stream all logs (including errors) back
to the current process so you can debug without checking the Prefect UI.
```

These instructions are writable *only because Prefect makes them this simple*. "Kill a process, start a process, run a make command, read the output." Any orchestrator that requires more ceremony than this would need paragraphs of infrastructure-specific instructions that an AI agent would struggle to follow reliably.

#### From dev to Docker: zero refactoring

The Docker Compose setup runs the exact same `serve()` call:

```yaml
command: ["uv", "run", "python", "-m", "twin.orchestrator"]
```

Local dev: `make serve-workflows` (bare Python process, zero overhead, instant restart).
Docker: same command inside a container, Prefect server in another container, MongoDB in a third.

No code changes. No environment-specific pipeline definitions. No "dev mode" vs "prod mode." The code the agent wrote and debugged locally is already the production code.

#### Scaling path without touching pipeline code

The Prefect setup comes with a documented scaling path (a 1,158-line guide in `docs/scaling-with-prefect.md`) that goes from the current `serve()` model to Docker work pools to Kubernetes — and the key point is that **zero flow/task code changes are needed**. You only change infrastructure configuration. The `@flow` and `@task` decorators, the retry policies, the log statements — all stay the same. This means the agent didn't need to "design for scale." The design is inherently scalable because Prefect separates orchestration logic from execution infrastructure.

#### Concrete numbers

- **Total setup time**: ~2 hours of agentic coding [VERIFY exact time]
- **Pipelines built**: 4 deployments (Substack RSS single, Substack RSS batch, memory extraction, memory materialization)
- **Tasks with retries**: 9 total tasks across 3 pipeline files, each with configured retries (1-2 attempts)
- **Orchestrator file**: 19 lines
- **Dockerfile**: 8 lines
- **Trigger scripts**: ~65-80 lines each (identical pattern, copy-paste friendly)
- **Worker restart time**: ~2 seconds (Python process restart)
- **Code changes needed for Docker deployment**: 0

#### The broader lesson

When choosing tools for AI-assisted development, the deciding factor isn't the feature set on the marketing page. It's whether the tool fits inside the agent's edit-run-read-fix loop.

The questions to ask:
- Can the agent restart the execution environment in seconds after a code change?
- Does the tool surface errors in the same terminal where the agent runs?
- Does the tool require external systems (brokers, schedulers, registries) that the agent can't control?
- Is the configuration in the same language as the code (Python), or does it require a separate DSL/YAML/config layer?

Prefect answers all four correctly: yes, yes, no, yes. That's why it was the only orchestrator that survived 2 hours of autonomous agentic coding without a single human intervention.

The irony is that "works well with AI agents" wasn't a design goal for Prefect. It's a side effect of their core philosophy: orchestration should be Python decorators on your existing code, not a separate system you deploy your code into. That philosophy — code-first, infrastructure-last — happens to be exactly what AI coding agents need.
