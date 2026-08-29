# Log

## 2026-08-29 ingest | 5 notes from data_input_examples/notes/01-easy

- Created `wiki-ai-engineering/` and ingested 5 notes; 0 skipped (empty wiki)
- Source pages: `how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs`, `the-future-of-mcp-vs-skills`, `the-future-of-mcp-why-the-future-of-agents-is-mcp-skills`, `the-right-way-of-building-agents-with-mcp-servers`, `why-mcp-is-not-dead`
- New entity pages (≥2 mentions): `mcp` (5), `claude-code` (4), `fastmcp` (4), `prefect` (3), `anthropic` (2)
- New concept pages (≥2 mentions): `agent-skills` (4), `cli-tools` (3), `connectivity-stack` (3), `mcp-primitives` (3), `agent-harness`, `governance`, `mcp-apps`, `mcp-server-design`, `server-side-orchestration`, `skills-over-mcp`, `unified-memory` (2 each)
- Waiting at 1 mention: `agent-memory`, `agentic-invocation`, `durable-execution`, `knowledge-graph`, `programmatic-tool-calling`, `progressive-disclosure`, `david-soria-parra`, `mongodb`, `obsidian`
- Wrote `overview.md`, regenerated all `index.md` files

## 2026-08-29 ingest | 10 notes from data_input_examples/notes/02-medium

- Ingested 5 new notes; skipped 5 already present (`how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs`, `the-future-of-mcp-vs-skills`, `the-future-of-mcp-why-the-future-of-agents-is-mcp-skills`, `the-right-way-of-building-agents-with-mcp-servers`, `why-mcp-is-not-dead` — all first seen under `data_input_examples/notes/01-easy/`)
- Source pages: `agentic-graphrag-via-mcp-servers`, `mongodb-for-an-ai-agent-unified-memory`, `owning-your-context-layer`, `stop-using-mcp-servers-to-access-your-mongodb-postgres`, `system-architecture-of-future-ai-apps-ui-tui-ide-extension`
- New pages: entities `mongodb` (4), `david-soria-parra` (2); concepts `knowledge-graph` (4), `agent-memory` (3), `progressive-disclosure` (3), `context-layer` (2), `durable-execution` (2), `hybrid-search` (2), `programmatic-tool-calling` (2)
- Updated 15 pages (new sources + claims); `created` preserved on all of them
- Not touched: `server-side-orchestration` — still at 2 mentions, and no new source page referenced it
- Waiting at 1 mention: `agentic-invocation`, `append-only-log`, `obsidian`
- Rewrote `overview.md`, regenerated all `index.md` files

## 2026-08-29 ingest | 10 notes from data_input_examples/notes/02-medium (re-run)

- All 10 inputs skipped — every raw path already exists; nothing copied, no page rewritten
- `build_index_md.py` re-run: output byte-identical to the previous run
- Logged for the record: the run happened, it just changed nothing

## 2026-08-29 query | MCP server vs. CLI

- question: "what do my notes say about when to use an MCP server vs. a CLI?"
- pages used: 4 (`wiki/concepts/connectivity-stack`, `wiki/concepts/cli-tools`, `wiki/concepts/governance`, `wiki/sources/stop-using-mcp-servers-to-access-your-mongodb-postgres`)
- answer: CLI when you own the machine (local, sandboxed, pre-trained tool, throwaway scripts); server when you own the users (distribution, governance, auth, non-local clients) — the sources agree on the boundary and disagree only on where a given case falls
- gap noticed: nothing in the wiki covers how a harness should arbitrate when a skill, a CLI and an MCP tool all offer the same capability

## 2026-08-29 ingest | 50 notes from data_input_examples/notes/03-hard

- Ingested 40 new notes; skipped 10 already present (matched by raw path, not by the directory given)
- Spawned 40 `source_writer` agents in parallel batches; the orchestrator read no raw file — only receipts
- New entity pages: `langchain` (3), `voyage-ai` (3), `modal` (2)
- New concept pages (19): `graphrag-ingestion` (10), `append-only-log` (11), `embeddings` (12), `entity-resolution` (8), `materialized-view` (8), `graph-extraction` (6), `infrastructure-over-frameworks` (5), `knowledge-freshness` (5), `pipeline-parallelism` (5), `database-scaling` (4), `inference-economics` (4), `agentic-search` (3), `graph-visualization` (3), `provider-abstraction` (3), `agentic-coding-loop` (2), `context-rot` (2), `data-fragmentation` (2), `graph-communities` (2), `read-write-separation` (2)
- Resolved from hollow: `knowledge-graph` 4 → 22 sources, `durable-execution` 2 → 13, `hybrid-search` 2 → 13, `unified-memory` 5 → 14
- Rewrote 6 pages whose corpus had changed shape (`knowledge-graph`, `unified-memory`, `durable-execution`, `hybrid-search`, `mongodb`, `prefect`); merged new claims into 9 more
- Thin notes got thin pages, as designed: `constraints`, `marketing`, `feedback-from-v1` reference nothing at all
- Noted duplication: `graphrag-presentation` re-contains two other ingested notes verbatim; the two task-runner notes overlap heavily. Recorded on the pages so the ≥2 threshold is not read as agreement.
- Still waiting at 1 mention: `agentic-invocation`, `continual-learning`, `rag-evaluation`, `reasoning-memory`, `neo4j`, `obsidian`

## 2026-08-29 ingest | repo github://decodingai-magazine/building-a-coding-agent-from-scratch-course

- `clone_repo.py`: action `cloned`, sha `6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea`, 98 MB under `raw/repos/.github-decodingai-magazine-…/` (hidden from Obsidian, gitignored)
- `repo_writer` (mode `architecture`) wrote `wiki/repos/github-…/ARCHITECTURE.md` — 234 lines, 6 sections, mermaid per section, permalinks pinned to the SHA
- The repo page is source-like: it pushed `agent-harness` 7 → 8 and `context-rot` 2 → 3, and materialized nothing on its own
- `wiki/repos/index.md` generated; the wiki root index gained a Repos row

## 2026-08-29 ingest | 2 articles from data_input_examples/substack_links.md

- `fetch_article.py` on both URLs: title, subtitle, author and published date from page metadata; 39k and 51k chars of body; no paywall warnings
- Source pages written for both; `observability` materialized at 2 mentions
- `agent-harness` reached 10 sources — notes, an article and a codebase now back the same claims
- `build_index_md.py` reported 4 `unparseable YAML frontmatter` errors: descriptions containing `: `. Fixed by quoting; rule added to `CONVENTIONS.md` §5.
- Final state: 53 source-like pages (50 notes · 2 articles · 1 repo), 10 entities, 38 concepts, 101 pages total

## 2026-08-29 query | append-only log vs. in-place updates

- question: "when should I use an append-only log instead of updating rows in place?"
- pages used: 4 (`concepts/append-only-log`, `concepts/materialized-view`, `concepts/database-scaling`, `sources/modeling-knowledge-graph-collections-append-only-log-vs-one`)
- saved: `wiki/questions/2026-08-29-append-only-log-vs-in-place-updates.md` + `wiki/notes/append-only-log-vs-in-place-updates.md` (≥2 pages cited)
- no ingest-owned page touched

## 2026-08-29 query | event sourcing at personal scale

- question: "is event sourcing actually worth it for a personal knowledge graph?"
- pages used: 4 (`concepts/append-only-log`, `concepts/database-scaling`, `sources/scaling-mongodb-brain-dump`, `sources/mcp-servers-for-continual-learning-via-graphrag`)
- saved: `wiki/questions/2026-08-29-is-event-sourcing-worth-it-for-a-personal-knowledge-graph.md`; **enriched** the existing note in place (`spawned_by_question` now has 2 entries, `created` preserved)
- same topic → no second note

## 2026-08-29 query | memory staleness

- question: "how do I decide that a fact in the memory has gone stale?"
- pages used: 2 (`concepts/knowledge-freshness`, `concepts/append-only-log`)
- answered honestly: the wiki has the mechanism, not the policy
- saved: question page only — no note, because there was no answer to save
- open question logged: memory staleness policy
- open question logged (user-flagged): what goes into a coding agent's context window each turn

## 2026-08-29 query | permission-gate routing in the coding agent repo

- question: "in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?"
- read `wiki/repos/github-.../ARCHITECTURE.md` first — it covers the gate's policy, not the routing → spawned `repo_writer` (mode `question`)
- wrote `wiki/repos/github-.../tool-call-to-permission-gate-routing.md` (`type: repo_note`, 7 evidence lines, permalinks pinned to `6ee643f`)
- **ingest tail ran**: the repo note is source-like — `agent-harness` 12 → 13, `durable-execution` 15 → 16, `agentic-coding-loop` 4 → 5; claims merged into all three
- saved: question page with `answer_doc` → the repo note
- no ingest-owned page edited by hand; every change went through the tail

## 2026-08-29 ingest | 1 article from decodingai.com

- Ingested `https://www.decodingai.com/p/context-engineering-for-coding-agents` (article adapter; no paywall warning)
- Source page written; tail updated `context-rot` (5 → 6), `progressive-disclosure` (5 → 6), `agent-skills`, `agent-memory`, `agent-harness`, `agentic-coding-loop`
- **Open questions this source appears to address**: "What actually goes into a coding agent's context window each turn?" — it walks the lifecycle and gives thresholds (80% full compaction, 60% microcompaction, ~1% skills catalog). `open-questions.md` left untouched; a human decides whether it landed.
- Still open: "How do you decide that a fact in the memory has gone stale?"
