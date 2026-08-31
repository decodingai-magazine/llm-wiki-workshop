# Log

## 2026-08-29 ingest | 4 articles from data_input_examples/substack_articles.md

- `fetch_article.py` on all 4 URLs: title/subtitle/author/published-date from page metadata, 32k–51k chars of body, no paywall warnings
- Source pages: `article-building-a-coding-agent-from-scratch-system-design`, `article-the-coding-agent-loop`, `article-run-coding-agents-safely`, `article-context-engineering-for-coding-agents` — all four from the same course as the previously-ingested repo
- Reconciled 3 slug collisions before running the tail (writers can't see 1-mention promissory slugs already used by other source-like pages, only materialized pages): `agent-sandboxing`(repo)/`sandboxing`(2 articles) → standardized on `sandboxing`; `permission-layer`(article)/`permission-gate`(repo) → standardized on `permission-gate`; `compaction`(article)/`context-compaction`(repo+article) → standardized on `context-compaction`
- New entity pages (≥2 mentions): `modal` (4), `opik` (3), `kitaru` (2), `pydantic-ai` (2)
- New concept pages (≥2 mentions): `sandboxing` (3), `context-compaction` (3), `agent-loop` (2), `permission-gate` (2)
- Updated pages (new article sources merged in): `claude-code` (7 → 11), `agent-harness` (2 → 6), `agent-memory` (3 → 5, Tensions section preserved), `skills` (5 → 7), `cli` (4 → 5), `progressive-disclosure` (2 → 4), `progressive-tool-discovery` (2 → 3)
- Not touched: `mcp`, `mcp-applications`, `graphrag`, `knowledge-graph`, `programmatic-tool-calling`, `fastmcp`, `mongodb`, `prefect`, `david-soria-parra` — none of the 4 articles reference these; `decode`'s tool set is flat and has no MCP layer
- New entities/concepts at 1 mention (article-only so far): `abhishek-bhardwaj`, `codex`, `docker`, `decode-agent`, `pi`, `terminal-bench`, `ty`; `agent-skills`, `lsp-server`, `steering-queue`
- Rewrote `overview.md` (4th theme now reads "four working parts instead of one abstraction" — agent-loop, permission-gate, context-compaction and sandboxing all graduated from repo-only to multi-source this run); regenerated all `index.md` files — `build_index_md.py` reported 0 errors, 0 warnings
- Final state: 14 note/article sources + 1 repo = 15 source-like pages, 9 entities, 15 concepts, 39 pages total

## 2026-08-29 query | how the coding agent's loop works

- question: "how does the coding agent's loop actually work?"
- pages used: 2 (`wiki/concepts/agent-loop`, `wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE`)
- answer: `decode`'s turn is a multi-leg async-generator loop yielding at two boundaries (MODEL_REQUEST, WOULD_STOP), no step cap, gated tool calls deferred to a PermissionGate rather than blocking, history healed against crashed legs
- gap noticed: none — the concept page and the repo's own architecture page already agree at two zoom levels (rationale vs. mechanics); did not need to escalate to `raw/` or the dedicated article source page

## 2026-08-29 ingest | youtube.com/watch?v=sJpop1juVBQ

- Routed to the `youtube` adapter (`fetch_youtube.py`), which is a deliberate skeleton — it raised `NotImplementedError` pointing at `SOURCES.md § How to add a source`
- Nothing ingested; no files written. This is the workshop's own extension exercise, not a bug

## 2026-08-29 ingest | repo github://decodingai-magazine/building-a-coding-agent-from-scratch-course (re-run)

- `clone_repo.py`: `git fetch` + `reset --hard` ran, action `updated`, but sha is unchanged (`6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea`) — the remote hasn't moved since the last ingest
- No new commit to reflect, so `repo_writer` was not re-run and the tail did not run: `ARCHITECTURE.md`'s existing permalinks are still pinned to the current SHA and stay valid
- Nothing changed; logged for the record

## 2026-08-29 ingest | repo github://decodingai-magazine/building-a-coding-agent-from-scratch-course

- `clone_repo.py`: action `cloned`, sha `6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea`, into `raw/repos/.github-decodingai-magazine-building-a-coding-agent-from-scratch-course/` (hidden from Obsidian, gitignored)
- `repo_writer` (mode `architecture`, opus) wrote `wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE.md` — 278 lines, permalinks pinned to the SHA
- New concept pages (≥2 mentions, both newly qualifying): `agent-harness` (2: repo + system-architecture-of-future-ai-apps note), `progressive-disclosure` (2: repo + agentic-graphrag note — distinct slug from the existing `progressive-tool-discovery`)
- Updated pages (repo added as a source alongside existing article/note sources): `claude-code` (6 → 7), `agent-memory` (2 → 3, gained a `## Tensions` section — MongoDB/MCP frame memory as infrastructure to provision, `decode` treats it as two capped markdown files), `skills` (4 → 5), `cli` (3 → 4)
- The repo did not touch `mcp`, `mcp-applications`, `progressive-tool-discovery` or `programmatic-tool-calling` — `decode` has no MCP layer and a flat, fixed tool list, so those pages are unchanged
- New entities at 1 mention (repo's only witness so far): `pydantic-ai`, `modal`, `opik`, `kitaru`
- New concepts at 1 mention (repo's only witness so far): `agent-loop`, `permission-gate`, `agent-sandboxing`, `subagents`, `context-compaction`, `durable-execution`
- Rewrote `overview.md` — added a fourth theme ("the harness itself, made concrete") and flagged the repo's role explicitly: second source on `agent-harness`, sole witness on six more concepts
- Regenerated all `index.md` files including the new `wiki/repos/index.md` — `build_index_md.py` reported 0 errors, 0 warnings

## 2026-08-29 ingest | 10 notes from data_input_examples/notes/02-medium

- Created `wiki-ai-engineering/` fresh (previous wiki deleted); ingested 10 notes, 0 skipped
- 2 notes carried attachments (`the-context-layer.png`, `the-future-of-mcp-why-the-future-of-agen-image.png`); both copied to `raw/assets/`
- Spawned 10 `source_writer` agents in parallel; orchestrator read no raw file, only receipts
- Corrected one inconsistency before running the tail: `the-future-of-mcp-vs-skills.md` had classified `mcp` under `entities:` while every other new page used `concepts:` — moved it to `concepts:` to avoid splitting the mention count across two namespaces for the same slug
- Source pages: `agentic-graphrag-via-mcp-servers`, `how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs`, `mongodb-for-an-ai-agent-unified-memory`, `owning-your-context-layer`, `stop-using-mcp-servers-to-access-your-mongodb-postgres`, `system-architecture-of-future-ai-apps-ui-tui-ide-extension`, `the-future-of-mcp-vs-skills`, `the-future-of-mcp-why-the-future-of-agents-is-mcp-skills`, `the-right-way-of-building-agents-with-mcp-servers`, `why-mcp-is-not-dead`
- New entity pages (≥2 mentions): `claude-code` (6), `fastmcp` (5), `mongodb` (3), `david-soria-parra` (2), `prefect` (2)
- New concept pages (≥2 mentions): `mcp` (9), `skills` (4), `cli` (3), `agent-memory` (2), `graphrag` (2), `knowledge-graph` (2), `mcp-applications` (2), `programmatic-tool-calling` (2), `progressive-tool-discovery` (2)
- Waiting at 1 mention: `agent-architecture`, `agent-harness`, `agent-skills`, `anthropic`, `claude-md`, `cloudflare`, `context-layer`, `event-sourcing`, `hybrid-search`, `maxime-labonne`, `mongosh`, `orchestrator-placement`, `prefect-horizon`, `progressive-disclosure`, `unified-memory`, `vector-search`
- Wrote `overview.md` (3 themes: agent memory as a data-layer problem, plural connectivity, harness tool-use efficiency), regenerated all `index.md` files — `build_index_md.py` reported 0 errors, 0 warnings

## 2026-08-31 query | append-only log vs. in-place update

- question: "when should I use an append-only log instead of updating rows in place?"
- pages used: 7 (agent-memory, mongodb-for-an-ai-agent-unified-memory, mongodb, graphrag, context-compaction, decode ARCHITECTURE, article-the-coding-agent-loop)
- saved: wiki/questions/2026-08-31-append-only-log-vs-updating-rows-in-place.md + wiki/notes/append-only-log-vs-in-place-update.md
- open question logged: append-only storage beyond agent memory (write amplification, log compaction, retention vs. immutability); `event-sourcing` still at 1 mention

## 2026-08-31 query | event sourcing for a personal knowledge graph

- question: "is event sourcing actually worth it for a personal knowledge graph?"
- pages used: 6 (agentic-graphrag-via-mcp-servers, mongodb-for-an-ai-agent-unified-memory, knowledge-graph, graphrag, mongodb, context-compaction)
- saved: wiki/questions/2026-08-31-event-sourcing-for-a-personal-knowledge-graph.md; enriched wiki/notes/append-only-log-vs-in-place-update.md in place (new section + 2 sources, `created` preserved) rather than opening a second note on the same topic
- finding: the wiki's one end-to-end personal knowledge graph (`agentic-graphrag-via-mcp-servers`) describes no event log and upgrades `LATENT` placeholders in place — the same author recommends `kg_events` in `mongodb-for-an-ai-agent-unified-memory`
- open question logged: what an event-sourced knowledge graph costs to operate over time (snapshot cadence, log growth, derived-view migration)

## 2026-08-31 query | staleness of a stored fact

- question: "how do I decide that a fact in the memory has gone stale?"
- pages used: 7 (agent-memory, article-building-a-coding-agent-from-scratch-system-design, article-context-engineering-for-coding-agents, agentic-graphrag-via-mcp-servers, mongodb-for-an-ai-agent-unified-memory, graphrag, context-compaction)
- saved: wiki/questions/2026-08-31-deciding-a-fact-in-memory-has-gone-stale.md + wiki/notes/staleness-in-agent-memory.md (new topic — distinct from the append-only note, cross-linked via `related`)
- finding: no memory architecture in the wiki detects staleness; they avoid storing invalidatable facts ("just-in-time reads beat a stale heavy index"), evict by age (`MEMORY.md` oldest-first), or let `$last` decide silently. The only continuous detector is the LSP diagnostics enricher — a type checker, not a memory system
- open question logged: staleness mechanisms (TTL, confidence decay, contradiction detection, re-verification) — a consistent negative across 5 designs, all documented at or near their build date

## 2026-08-31 query | tool call routing to the permission gate (repo path)

- question: "in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?"
- routed to the repo path: `ARCHITECTURE.md` covers the gate's policy matrix but not the call path into `gate.check()` or the mechanics of the wait — clone already present at `6ee643f`, matching the page, so not re-cloned
- repo note: `wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/tool-call-routing-to-the-permission-gate.md` (source-like)
- tail: `permission-gate` (2 → 3), `agent-loop` (2 → 3), `kitaru` (2 → 3), `pydantic-ai` (2 → 3), `agent-harness` (6 → 7); overview rewritten; indexes regenerated — 0 errors, 0 warnings
- saved: wiki/questions/2026-08-31-tool-call-routing-to-the-permission-gate.md
- `durable-execution` suggested as a new concept by the repo writer but still at 1 mention — stays promissory

## 2026-08-31 query | how a subagent is spawned and what the parent gets back (repo path)

- question: "in the coding agent repo, how does the agent spawn a subagent, and what does the parent actually get back when it finishes?"
- routed to the repo path: `ARCHITECTURE.md`'s "Subagent fan-out" section covers the caller's fold shape but not `_spawn_child`'s own body — clone already present at `6ee643f`, matching the page, not re-cloned
- repo note: `wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/how-a-subagent-is-spawned-and-what-the-parent-gets-back.md` (source-like)
- tail: `subagents` **created** (1 → 2 sources, was stuck at 1 mention); `agent-loop` (3 → 4), `permission-gate` (3 → 4), `pydantic-ai` (3 → 4); overview rewritten; indexes regenerated — 0 errors, 0 warnings
- saved: wiki/questions/2026-08-31-how-a-subagent-is-spawned-and-what-the-parent-gets-back.md

## 2026-08-31 query | open question flagged: context window assembly

- question: "what actually goes into a coding agent's context window each turn?"
- user explicitly flagged this as open (Q.7 first bullet) — no answer attempted, no question page written
- logged: wiki/open-questions.md — new bullet under the 2026-08-31 section
- candidate sources already in the wiki for a future real answer: `agent-harness`, `context-compaction`, `skills`, `progressive-disclosure`, `progressive-tool-discovery`, the decode repo's own context-engineering wiring
