# Why Durable Workflow Tools Are More Important Than AI Frameworks

# **The uncomfortable truth about AI agents in production**

Building an AI agent that works in a demo takes an afternoon. Building one that works reliably at scale — that's a completely different beast.

Every AI framework — Pydantic AI, LangGraph, CrewAI — solves the same problem: how to get an LLM to reason, call tools, and produce structured output. They do it well. You can wire up an agent with `google-genai` or `openai`'s SDK in 20 lines of Python. Add Pydantic AI and you get type safety, dependency injection, and auto-correction on top.

But none of that matters when your agent fails at step 7 of 10 because OpenAI returned a 429, your database hiccupped, or your cloud function timed out. Without durable execution, you restart from scratch — burning tokens, duplicating side effects, and losing time.

**Durable workflow tools like Prefect solve the problem that AI frameworks don't even attempt to address: what happens when things go wrong.**

Prefect solves this with three primitives:

- **`@flow`** — wraps your entire pipeline into an observable unit with its own retry and timeout policies
- **`@task`** — wraps individual steps with independent retries, caching, and timeouts
- **Result persistence** — completed tasks store their outputs; on retry, they load from cache instead of re-executing

That's it. Three decorators and your fragile script becomes a durable, observable, resumable workflow.

---

## **The real cost of fragility**

Consider a multi-step agent pipeline:

```
1. LLM call: analyze transcript        → $0.003
2. Tool call: store_event("meeting")   → free
3. Tool call: store_fact("prefers X")  → free
4. LLM call: summarize findings        → $0.004
5. Tool call: search_episodes("Y")     → free  ← FAILS (timeout)
6. LLM call: synthesize answer         → $0.003
```

Without durable execution, a retry re-runs everything from step 1. Steps 1-4 were already successful — you just wasted $0.007 and duplicated two memory writes.

At scale (hundreds of agent runs per day), this adds up:

- **100 runs/day x 30% failure rate x $0.01 wasted per retry = $9/day = ~$270/month** in pure waste.
- Plus duplicated side effects (double writes, double API calls, double notifications).
- Plus engineering time debugging "why did this memory get stored twice?"

With Prefect's result caching, a retry loads steps 1-4 from cache (free, instant) and only re-executes step 5 onward. Zero waste. Zero duplicates.

Here's exactly what that looks like in a real multi-agent pipeline:

```
full_memory_pipeline("transcript...", "What are the blockers?")

Run 1 (fails at step 4 of 6):
  ✅ LLM call: Analyze transcript          → cached
  ✅ Tool call: store_event("ML pipeline")  → cached
  ✅ Tool call: store_fact("prefers Polars") → cached
  ❌ Tool call: store_fact("GPU cluster")   → TIMEOUT (disk full)
  ⊘  LLM call: QA reasoning                → never reached
  ⊘  Tool call: search_facts               → never reached

Run 2 (automatic retry):
  ⚡ LLM call: Analyze transcript          → loaded from cache (FREE)
  ⚡ Tool call: store_event("ML pipeline")  → loaded from cache (FREE)
  ⚡ Tool call: store_fact("prefers Polars") → loaded from cache (FREE)
  🔄 Tool call: store_fact("GPU cluster")   → retried, succeeds
  ✅ LLM call: QA reasoning                → executes normally
  ✅ Tool call: search_facts               → executes normally
```

The first three steps cost $0 on retry. No redundant LLM calls. No duplicate memory writes. The custom cache policy generates keys based on stable factors (prompt content, model name, tool parameters) while ignoring transient metadata like timestamps — so identical logical operations always hit cache.

---

## **What durable execution actually gives you**

### **1. Result caching and resumption**

Every task's output is persisted. When a flow retries, completed tasks load their cached results instead of re-executing. This is the single most important feature for cost efficiency at scale.

```python
@task(retries=3, retry_delay_seconds=[1.0, 2.0, 4.0], cache_policy=INPUTS)
def call_llm(prompt: str) -> str:
    # If this succeeds once, retries of the parent flow skip it entirely
    ...
```

### **2. Granular retry policies**

Different components fail differently. LLM calls need exponential backoff (rate limits). Tool calls need fast retries (transient I/O). Database writes might need exactly-once semantics. Prefect lets you configure each independently:

```python
durable_agent = PrefectAgent(
    agent,
    model_task_config=TaskConfig(retries=3, retry_delay_seconds=[1.0, 2.0, 4.0]),
    tool_task_config=TaskConfig(retries=5, retry_delay_seconds=[0.5, 1.0, 2.0, 4.0, 8.0]),
)
```

No AI framework gives you this level of control over failure handling.

### **3. Observability for free**

Every task and flow execution is tracked with timing, status, logs, and retry history. You see exactly where your agent spent time, which steps failed, and how many retries it took — all in a dashboard you didn't have to build.

This is critical for debugging agents in production. When a user reports "the agent gave a wrong answer," you can trace back through every LLM call and tool invocation to find what went wrong.

### **4. Scheduling and deployment**

Agents aren't always triggered by a user message. ETL pipelines, daily reports, periodic memory consolidation — these need cron schedules, event triggers, and infrastructure management. Prefect handles all of this:

```python
recall_memory_flow.serve(
    name="daily-memory-review",
    cron="0 9 * * *",
    parameters={"topic": "priorities"},
)
```

### **5. Human-in-the-loop without custom infrastructure**

Agents that need human approval can pause execution, present a form, and resume when the human responds. No WebSocket servers, no polling loops, no custom UI — Prefect generates it.

### **6. Dynamic control flow — no precompiled DAGs**

Traditional orchestrators (Airflow, Dagster) require you to define the execution graph before runtime. Agents can't work that way — they decide their next action at runtime based on LLM output. Prefect follows normal Python control flow: `if/else`, `while` loops, `try/except`. Your agent code is just Python. Prefect instruments it, it doesn't constrain it.

### **Important caveat: streaming**

Streaming inside Prefect flows is buffered, not real-time. Tasks consume their entire execution before returning results. If you need real-time token streaming to a UI, handle that outside the Prefect flow or use an event stream handler that wraps each event as an individual task.

---

## **Why this matters more than choosing the "right" AI framework**

The AI framework debate (Pydantic AI vs LangGraph vs CrewAI vs raw SDK) is about **how you talk to the LLM**. It's the top layer of the stack:

```
┌──────────────────────────────────┐
│  AI Framework (reasoning layer)  │  ← Pydantic AI, LangGraph, raw SDK
│  How the agent thinks            │
├──────────────────────────────────┤
│  Orchestration (durability layer)│  ← Prefect, Temporal
│  How the agent survives          │
├──────────────────────────────────┤
│  Infrastructure (compute layer)  │  ← K8s, Cloud Run, ECS
│  Where the agent runs            │
└──────────────────────────────────┘
```

You can swap the reasoning layer easily. Moving from `google-genai` to Pydantic AI is a refactor. Moving from Pydantic AI to LangGraph is a rewrite, but it's contained. The agent's behavior changes, but the infrastructure doesn't.

The durability layer is the hard part. Building retry logic, result caching, scheduling, observability, and deployment from scratch is months of engineering. Getting it wrong means silent failures, wasted money, and agents that work in demos but break in production.

**The AI framework makes your agent smart. The durability layer makes it reliable. You need both, but reliability is harder to bolt on after the fact.**

---

## **How these tools are complementary**

Prefect is not competing with Pydantic AI or LangGraph. They operate at different layers and compose naturally.

### **Pydantic AI + Prefect**

The officially supported integration. Pydantic AI handles reasoning (LLM calls, tool definitions, structured outputs, auto-correction). Prefect handles operations (retries, caching, scheduling, observability).

```python
from pydantic_ai import Agent
from pydantic_ai.durable_exec.prefect import PrefectAgent, TaskConfig

agent = Agent("google-gla:gemini-2.5-flash", name="my-agent", output_type=MyOutput)
durable_agent = PrefectAgent(agent, model_task_config=TaskConfig(retries=3))

# One line turns a fragile agent into a production-grade durable workflow
result = await durable_agent.run("Do the thing")
```

Every LLM call becomes a Prefect task with retries. Every tool invocation gets its own retry policy. Failed runs resume from the last successful step.

### **LangGraph + Prefect**

LangGraph excels at complex multi-agent graphs with explicit state machines and branching. But it doesn't provide scheduling, infrastructure management, or cost-saving result caching. You can wrap LangGraph node executions in Prefect tasks:

```python
@task(retries=2, cache_policy=INPUTS)
def run_research_node(state: AgentState) -> AgentState:
    return research_graph.invoke(state)

@task(retries=2, cache_policy=INPUTS)
def run_synthesis_node(state: AgentState) -> AgentState:
    return synthesis_graph.invoke(state)

@flow
def multi_agent_pipeline(query: str):
    state = run_research_node(AgentState(query=query))
    return run_synthesis_node(state)
```

LangGraph manages the agent graph. Prefect manages the production lifecycle.

### **Raw SDK + Prefect**

You don't even need an AI framework. Wrap your `google-genai` or `openai` calls directly in Prefect tasks:

```python
@task(retries=3, retry_delay_seconds=[1.0, 2.0, 4.0], cache_policy=INPUTS)
def call_gemini(prompt: str) -> str:
    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    return response.text

@flow
def my_pipeline(question: str):
    context = search_memories(question)  # another @task
    return call_gemini(f"Context: {context}\n\nQuestion: {question}")
```

Simple, typed, durable, observable. No framework needed.

---

## **Full pros and cons**

### **Prefect**

**Pros:**

- Durable execution with smart result caching — failed runs resume, not restart
- Granular retry policies per task (LLM calls get exponential backoff, tools get fast retries)
- First-class scheduling (`cron`, `interval`, event-driven triggers)
- Rich observability UI — every task/flow visualized with timing, status, logs
- Dynamic control flow — follows normal Python `if/else/while`, no DAG compilation needed
- Human-in-the-loop pauses with auto-generated UI forms
- Deployment to any infrastructure (K8s, ECS, Cloud Run) via work pools
- Cost savings at scale — cached results prevent redundant LLM calls

**Cons:**

- Adds infrastructure complexity — you need Prefect server/cloud running
- No LLM-specific primitives — it doesn't know about prompts, agents, or models
- Streaming inside Prefect flows is buffered, not real-time (tasks consume fully before returning)
- Learning curve for concepts like work pools, deployments, result storage
- Overkill for simple scripts or single-shot agent calls

### **LangGraph**

**Pros:**

- Purpose-built for multi-agent coordination — agents as graph nodes with explicit edges
- Sophisticated state management based on Google's Pregel system
- Built-in checkpointing — pause, resume, rewind workflows at any step
- Native support for parallel agent execution within super-steps
- Rich ecosystem of LangChain integrations (retrievers, tools, memory)
- First-class human-in-the-loop via interrupt nodes

**Cons:**

- Graph-based mental model has steep learning curve — even simple agents need nodes/edges
- Tightly coupled to LangChain ecosystem — hard to use without it
- Verbose for simple use cases — a 3-step agent needs significant boilerplate
- Less mature deployment story compared to Prefect (no built-in scheduling/infra management)
- Debugging graph execution is harder than debugging linear Python
- No built-in result caching for cost savings on retries

### **Pydantic AI**

**Pros:**

- Most Pythonic — agents are plain Python objects, tools are plain functions
- Full type safety with Pydantic validation on inputs AND outputs
- Auto self-correction — invalid LLM output triggers automatic retry with error feedback
- Dependency injection system (like FastAPI) for clean tool composition
- Model-agnostic — works with OpenAI, Anthropic, Gemini, Ollama, etc.
- Native durable execution support via Prefect, Temporal, or DBOS backends
- Lightweight — minimal boilerplate for simple agents

**Cons:**

- Newer framework (V1 shipped Sept 2025) — smaller ecosystem than LangChain
- Multi-agent coordination is manual — you compose agents in code, no built-in graph
- No built-in scheduling, deployment, or infrastructure management
- No built-in checkpointing (delegates to durable execution backends)
- Fewer pre-built integrations compared to LangChain/LangGraph

---

## **When to use what**

| Scenario | Best Choice |
| --- | --- |
| Simple agent, needs production reliability | **Pydantic AI + Prefect** |
| Complex multi-agent routing with branching | **LangGraph** (+ Prefect for infra) |
| Scheduled/recurring agent pipelines | **Prefect** (+ any agent framework) |
| Type-safe structured outputs matter | **Pydantic AI** |
| Already in LangChain ecosystem | **LangGraph** |
| Need deployment, monitoring, and ops dashboard | **Prefect** |
| Quick prototype, don't need durability | **Pydantic AI** alone |

---

## **Side-by-side: Prefect-only vs AI framework + Prefect**

You can use Prefect without any AI framework at all — just wrap plain Python functions as tasks and flows. Adding an AI framework (like Pydantic AI) on top adds intelligence but changes the tradeoffs:

| Aspect | Prefect Only | AI Framework + Prefect |
| --- | --- | --- |
| **Intelligence** | Fixed Python logic — you hard-code every query and decision | LLM decides which tools to call, what queries to run, how to synthesize |
| **Flexibility** | Every new "question type" needs new code | Ask anything — the agent adapts its tool usage dynamically |
| **Structured output** | Manual dict construction | Pydantic models validated automatically; LLM auto-corrects invalid output |
| **Cost** | $0 (no LLM calls) | ~$0.01-0.05 per agent run (LLM API costs) |
| **Durability** | Full (retries + caching on every task) | Full (Prefect wraps every LLM call and tool invocation as a task) |
| **Observability** | Task-level in Prefect UI | Task-level in Prefect UI + optional Logfire tracing for LLM internals |
| **Multi-agent** | Compose flows manually | Compose `PrefectAgent` instances in flows — each agent is independently durable |
| **Retry behavior** | Retries the exact Python function | Retries the LLM call, loading cached results for completed steps |
| **Best for** | Data pipelines, ETL, deterministic workflows | AI agents, RAG, dynamic reasoning, conversational systems |

The key insight: Prefect-only is cheaper and simpler for deterministic pipelines. But the moment you need an agent to *decide* what to do at runtime, you need an AI framework on top — and Prefect ensures that the AI framework's decisions are durable.

---

## **The bottom line**

| Layer | What it solves | Can you build it yourself? | Should you? |
| --- | --- | --- | --- |
| AI Framework | Reasoning, tool calling, structured output | Yes, in a day | Maybe — raw SDK works for simple cases |
| Durable Execution | Retries, caching, scheduling, observability | Yes, in months | No — use Prefect, Temporal, or DBOS |
| Infrastructure | Compute, networking, scaling | Yes, in weeks | Depends on your team |

The AI framework is the easiest layer to build or swap. The durability layer is the hardest to get right and the most expensive to skip. Every production agent system will eventually need it — the only question is whether you build it yourself (poorly) or use a tool designed for it.

**Start with Prefect. Then pick whatever AI framework fits your reasoning needs. Not the other way around.**

---

## **Key takeaways**

1. **Prefect is not competing with Pydantic AI or LangGraph** — it's a layer below them that adds production reliability (retries, caching, scheduling, observability).
2. **Use Prefect alone** when your pipeline is deterministic (data ETL, scheduled jobs, fixed-step memory queries).
3. **Use Pydantic AI + Prefect** when you need LLM reasoning with production guarantees. The `PrefectAgent` wrapper is the official integration — one line to make any Pydantic AI agent durable.
4. **Use LangGraph** when you need complex multi-agent graphs with explicit state machines and branching. You can still wrap LangGraph steps in Prefect tasks for durability if needed.
5. **The cost savings are real**: at scale, durable execution with cached results prevents hundreds of dollars/month in wasted LLM API calls from retried failures.
