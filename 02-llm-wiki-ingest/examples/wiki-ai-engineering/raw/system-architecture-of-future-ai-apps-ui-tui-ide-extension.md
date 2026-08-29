# System architecture of future AI apps: UI/TUI/IDE extension ↔ harness ↔ connectivity (MCP clients, CLIs, skills) MCP servers

**Post 15:** System architecture of future AI apps: UI/TUI/IDE extension ↔ harness ↔ connectivity (MCP clients, CLIs, skills) MCP servers  (more details [here](https://read.readwise.io/archive/read/01kpmy78m7aq4tsm1dawdjnmh0))

---

# System Architecture of Future AI Apps

**Source anchor:** [[The Future of MCP — David Soria Parra, Anthropic]] (DSP, AI Engineer 2026)

A breakdown of the layered architecture that future AI apps are converging on: a presentation surface (UI / TUI / IDE extension) on top of an agent harness, which speaks through a connectivity layer (MCP clients, CLIs, skills) to a fleet of MCP servers. The interesting move is that none of these layers is monolithic anymore — each is being decomposed so that capabilities, UI, and domain knowledge can travel independently from where the agent lives.

---

## 1. The Big Picture

```
┌──────────────────────────────────────────────────────────────────┐
│  PRESENTATION                                                    │
│  UI (web/desktop) · TUI (Claude Code) · IDE extension (Cursor)   │
│  - Renders MCP applications (server-shipped UIs)                 │
│  - Renders model output, tool calls, long-running tasks          │
└────────────────────────────┬─────────────────────────────────────┘
                             │ (events, render contracts)
┌────────────────────────────▼─────────────────────────────────────┐
│  HARNESS  (the agent loop + everything around it)                │
│  - Inference loop, context management, memory, compaction        │
│  - Progressive tool discovery (tool_search)                      │
│  - Programmatic tool calling (code mode: V8 isolate / Lua)       │
│  - Permission model, sandboxing, audit                           │
└────────────────────────────┬─────────────────────────────────────┘
                             │ (capability calls)
┌────────────────────────────▼─────────────────────────────────────┐
│  CONNECTIVITY  (the right tool for the right job)                │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   Skills     │  │     CLIs     │  │     MCP Clients        │  │
│  │ domain know- │  │ pre-trained  │  │ rich semantics,        │  │
│  │ ledge files  │  │ surfaces,    │  │ remote, auth, UI,      │  │
│  │ (reusable)   │  │ bash-compos- │  │ tasks, elicitation     │  │
│  │              │  │ able         │  │                        │  │
│  └──────────────┘  └──────────────┘  └────────────┬───────────┘  │
└──────────────────────────────────────────────────┼───────────────┘
                                                   │ (MCP protocol)
┌──────────────────────────────────────────────────▼───────────────┐
│  MCP SERVERS                                                     │
│  - Tools, resources, prompts                                     │
│  - Skills-over-MCP (domain knowledge shipped with the server)    │
│  - MCP applications (server-rendered UIs)                        │
│  - Server-side execution env (Cloudflare-style code mode)        │
│  - Auth (cross-app access), discovery (well-known URLs), tasks   │
└──────────────────────────────────────────────────────────────────┘
```

DSP's framing: **2024 was demos. 2025 was coding agents. 2026 is connectivity.** Coding agents are the easy case — local, verifiable, sandbox available, a 2D UI is enough. General knowledge-worker agents need to reach five SaaS apps and a shared drive, and that means none of these four layers is optional anymore.

---

## 2. Layer 1 — Presentation (UI / TUI / IDE Extension)

The presentation layer is no longer the place where capabilities are defined; it's the place where they are *rendered*. The shift DSP highlights is **MCP applications**: an agent that ships its own interface, served over an MCP server. The server, not the client, owns the UI contract. The client agrees to render it.

**Implications:**

- The same MCP application can be hosted in [Claude.ai](http://claude.ai/), ChatGPT, VS Code, Cursor — *"put it into cloud, put it into ChatGPT, put it into VS Code Cursor, and it will just work."*
- Rich UIs need rich semantics on the wire. This is why MCP-as-protocol matters: both ends must agree on what's being rendered, when a long-running task is in flight, when a UI is incoming.
- **Extension surfaces vary.** Web/desktop clients can render HTML-based MCP applications. A TUI (Claude Code) or a CLI agent cannot — *"if you're a CLI you just have a hard time rendering HTML."* Hence the protocol's explicit extension mechanism: some clients support certain features, others don't, and the server declares what it ships.

**Three classes of presentation today:**

| Surface | Strength | Where MCP apps fit |
| --- | --- | --- |
| Web / desktop UI | Full rendering, HTML, interactive components | First-class |
| TUI (CLI agents) | Local, fast, scriptable, sandbox assumed | Tools only, no apps |
| IDE extension | Embedded in dev workflow, code execution context | Hybrid |

The presentation layer is becoming a thin renderer of contracts shipped from elsewhere — not a place where product features are hard-coded.

---

## 3. Layer 2 — The Harness

The harness is what most people think of as "the agent" but is actually the orchestration runtime around the model. Claude Code, Cursor, ChatGPT desktop, and bespoke in-house agents are all harnesses. This is the layer DSP says we need to invest in most, because **the protocol moves bytes; the harness decides what to do with them.**

Two patterns the harness must implement to make 2026-scale agents work:

### 3.1 Progressive Discovery

The naive approach to MCP — stuff every available tool into the context window — has been the dominant pattern of 2025 and is also the source of every "MCP causes context bloat" complaint. DSP's correction: **the protocol is not the problem, the client is.**

Progressive discovery means the model only gets a `tool_search` (or similar) capability up front. When the model decides it needs a tool, it queries for it, loads its schema, and only then calls it. Claude Code shipped this and saw a *massive* reduction in tool-context usage.

```
Before:           After:
[100 tools]       [1 tool_search]
   ↓                 ↓
context = 50K     context = 200 tokens
                  → search "send slack message"
                  → load schema (300 tokens)
                  → call
```

This is a harness-side responsibility. The protocol already supports it. Most harnesses haven't built it yet.

### 3.2 Programmatic Tool Calling (Code Mode)

The second harness pattern: stop letting the model orchestrate tools through inference. Every "call tool A → look at result → call tool B" round-trip is wasted latency and wasted tokens. Instead, **give the model an execution environment** — V8 isolate, Lua interpreter, sandboxed Python — and have it write a script that composes the tools.

The hook is **MCP's structured output**, which gives the script type information so the model can compose calls correctly. *"You do one call and you can filter that. The model will automatically remove things from the JSON and just continue."*

This is the same pattern that makes Claude Code's `bash` tool so powerful — DSP's point is that it should be the default for MCP too, not an exception.

### 3.3 Other Harness Responsibilities

- **Context management & compaction** — when conversations get long, the harness summarizes prior turns into a smaller representation so work continues without context exhaustion.
- **Permission model** — gating which tools/servers/CLIs the model is allowed to invoke, and when to prompt the user.
- **Memory** — persistent state across sessions, separate from in-context conversation state.
- **Audit & observability** — what was called, with what args, by which model turn.

The harness is where the *agent character* lives. Same model + same MCP servers + different harness = wildly different product behavior.

---

## 4. Layer 3 — Connectivity (Skills, CLIs, MCP Clients)

DSP's core thesis: **connectivity is not one thing.** There is no single right answer — anyone who claims "just use computer use" or "just use MCP" is wrong. There are three primitives, each best at a different job, and 2026 agents will use all three together.

### 4.1 Skills — Domain Knowledge as Files

A skill is a reusable file that captures *how to do something well* — the playbook for a domain task. Skills don't replace tools; they tell the model when and how to use them. They are mostly portable across platforms (with minor differences).

**When to reach for a skill:**

- The task has a procedural shape the model needs reminding of.
- The knowledge is *stable* — it doesn't need to be fetched fresh every call.
- You want it reusable across agents and clients.

The next move DSP teased: **skills over MCP.** Server authors ship domain knowledge alongside their tools, so the moment you connect to the server, the agent learns how to use it well. This kills the awkward dance of plug-in mechanisms and separate registries — the server is the source of truth for both *what it can do* and *how to drive it*.

### 4.2 CLIs — Pre-Trained Surfaces, Bash-Composable

CLIs win in three specific situations:

1. **Pre-training coverage.** `git`, `gh`, `kubectl`, `aws` are in the model's training data. The model already knows them. Wrapping them in MCP servers is often a regression — you lose the model's prior knowledge and force it through a thinner interface.
2. **Composition.** Bash pipes are a code-mode-lite that's been around for 50 years. `gh pr list | jq | xargs` is real programmatic tool calling.
3. **Local + sandboxed.** When the harness has a code-execution environment, the cost of "shell out to a CLI" is near zero.

CLIs are the wrong choice when you need: rich semantics, UI rendering, long-running task tracking, authorization beyond local creds, governance — *"boring enterprise stuff."* That's MCP's territory.

### 4.3 MCP Clients — The Connective Tissue

The MCP client (inside the harness) is what brokers everything else: it speaks the protocol, manages server lifecycles, handles auth, surfaces server-shipped UIs to the presentation layer, and translates between the model's tool-call ABI and what each server expects.

What the MCP client uniquely enables:

- **Remote servers** — not local-only anymore.
- **Centralized auth** — single sign-on across many servers (the "cross-app access" feature shipping for enterprises).
- **Rich primitives** — elicitation (server asks the user for input), tasks (long-running, async, observable), resources (file-like attachments), structured output.
- **Platform independence** — the same server runs against [Claude.ai](http://claude.ai/), ChatGPT, Cursor.
- **MCP applications** — server-shipped UIs.

The mental model: **CLIs are how the agent talks to the local computer. Skills are how the agent remembers what it knows. MCP is how the agent talks to everything else, especially other systems' stuff.** All three coexist in the same agent loop.

---

## 5. Layer 4 — MCP Servers

If the harness is the agent's brain, MCP servers are its limbs. The shape of a *good* MCP server is changing fast — DSP is openly critical of the dominant pattern of 2025.

### 5.1 Stop Wrapping REST APIs One-to-One

*"Every time I see someone building another REST to MCP server conversion tool, I'm — it's a bit cringe."*

The right way to design an MCP server is to design for an agent (and a human) — start by asking *how would I want to drive this if I were the user?* That gives you task-shaped tools (`schedule_meeting_with_summary`), not endpoint-shaped tools (`POST /calendars/{id}/events`). Endpoint-shaped tools force the model into orchestrating low-level calls, which is exactly what programmatic tool calling exists to avoid.

### 5.2 Server-Side Execution Environments

Cloudflare's MCP server is the canonical example: instead of exposing 80 tools, expose one tool that runs JavaScript against the Cloudflare API surface. The model writes a snippet, the server runs it, returns the result. Same code-mode argument as the harness side — fewer tokens, lower latency, cleaner composition.

This pattern works especially well when the server already has an API SDK in some popular runtime.

### 5.3 Use the Rich Semantics the Protocol Offers

What server authors are still underusing:

- **MCP applications** — ship a UI, not just tools.
- **Skills over MCP** — ship the playbook for using your server.
- **Tasks** — for anything long-running, return a task handle, let the agent (or user) poll/await.
- **Elicitation** — when you need input mid-flow, ask the user through the protocol instead of failing.
- **Resources** — file-like attachments (logs, PDFs, structured docs) rather than stuffing everything into tool output.

A 2026 MCP server is not "a JSON-RPC wrapper around an API." It's a small product surface — tools + UI + skills + tasks — that the agent assembles into the user's experience.

### 5.4 Infrastructure Coming Down the Line

DSP previewed several near-term spec changes (June '26):

- **Stateless transport protocol** — proposal from Google. Makes MCP servers deployable like any stateless REST service (Cloud Run, Kubernetes) instead of needing sticky-session streamable HTTP.
- **Improved async task primitive** — formalizing agent-to-agent communication.
- **TypeScript SDK v2 + Python SDK v2** — incorporating FastMCP-level ergonomics.
- **Cross-app access** — auth handshake with identity providers so users log in once with their corporate IdP and don't re-auth per server.
- **Well-known URL discovery** — `example.com/.well-known/mcp` so crawlers, browsers, and agents can auto-discover an MCP server attached to a website.

---

## 6. Cross-Cutting Concerns

Some properties don't live in one layer — they cut across all four.

### 6.1 Authorization

| Layer | Auth concern |
| --- | --- |
| Presentation | User session, who is logged in |
| Harness | Which servers/CLIs this agent run is allowed to invoke |
| Connectivity | Token brokering, refresh, audience scoping |
| Server | OAuth + the new cross-app access pattern with corporate IdPs |

The endgame: a single corporate login propagates down through all layers without the user re-authenticating per server.

### 6.2 Discovery

- **Server discovery** — well-known URLs (coming).
- **Tool discovery within a server** — progressive (via `tool_search`), not eager.
- **Skill discovery** — shipped with the server (skills over MCP).

The pattern is consistent: *don't load it until the agent needs it.*

### 6.3 Async & Long-Running Work

Coding agents could get away with synchronous, blocking tool calls. Knowledge-worker agents cannot — running a financial report, waiting on a human approval, polling an external job. The async task primitive in MCP is the protocol-level answer; the harness is the runtime-level answer; the UI is the rendering answer (showing the user a long-running task in flight).

### 6.4 Composition Across Layers

The most interesting code-mode pattern is *vertical composition*: a script written by the model that invokes one MCP server's tool, pipes the result into a CLI, and writes the output to a file system resource exposed by a second MCP server. All four layers participate in one orchestrated unit of work, and only the script writer (the model, inside the harness's sandbox) sees the seams.

---

## 7. What Changes in 2026

Five concrete shifts a system architect should expect:

1. **Harnesses get smarter, not bigger.** Progressive discovery + code mode are the table-stakes upgrades. Skipping them means burning tokens and latency.
2. **MCP servers become product surfaces, not API wrappers.** Tools + UI + skills + tasks, designed for an agent operator, not an SDK consumer.
3. **The presentation layer goes thin.** The UI is whatever the server ships; the client renders it. Hard-coded product flows become server-shipped MCP applications.
4. **Connectivity is plural by default.** A real agent uses MCP *and* CLIs *and* skills *and* computer use, each where it fits. Single-mechanism agents underperform.
5. **Infrastructure-grade primitives ship.** Stateless transport, cross-app auth, well-known discovery, async tasks — MCP grows up from a developer protocol into something operations teams can run at scale.

---

## 8. A Practical Build Checklist

If you're designing a system in this architecture today:

**Harness side**

- [ ]  Implement `tool_search` (or equivalent) — don't eagerly load tool schemas.
- [ ]  Give the model a code-execution sandbox (V8 isolate, Lua, sandboxed Python).
- [ ]  Surface MCP applications to the renderer; degrade gracefully where not supported.
- [ ]  Build a permission model that scopes per-server, per-tool, per-session.
- [ ]  Plan for async tasks in your UI from day one.

**MCP server side**

- [ ]  Design tools for the agent's job, not the API's shape.
- [ ]  Expose structured output for every tool that returns data.
- [ ]  Ship a skill alongside your server explaining how to drive it well.
- [ ]  Use elicitation for missing-input flows.
- [ ]  Use tasks for anything > a few seconds.
- [ ]  Consider a server-side code-execution tool instead of N specific tools.

**Connectivity side**

- [ ]  Prefer CLIs for pre-trained, sandbox-friendly, composable surfaces.
- [ ]  Prefer skills for stable domain knowledge.
- [ ]  Prefer MCP for everything that needs auth, UI, remote, or rich semantics.
- [ ]  Don't wrap a CLI in an MCP server unless you're adding real semantics.

**Presentation side**

- [ ]  Renderer reads contracts from the server; doesn't hard-code product flows.
- [ ]  Long-running tasks are first-class UI elements, not loading spinners.
- [ ]  Multi-surface: a feature should work in web, TUI, and IDE — what degrades gracefully where?

---

## Open Questions

- How does the harness arbitrate when a skill, a CLI, and an MCP tool *all* offer overlapping capability?
- What's the right governance story for skills-over-MCP when the server can change behavior remotely?
- Does code-mode-on-the-server eat the long tail of tool-shaped MCP servers, or do they coexist?
- When MCP applications become common, who owns the UX consistency layer across servers in one client?

---

## Related

- [[The Future of MCP — David Soria Parra, Anthropic]] — source talk
