# Log

## 2026-08-31 ingest | 10 notes from data_input_examples/notes/02-medium (fresh wiki)

- Created `wiki-ai-engineering/` from scratch at the project root (per user request, to avoid disturbing the pre-existing `examples/wiki-ai-engineering/` copy of this same demo); ingested 10 notes, 0 skipped
- 2 notes carried attachments (`the-context-layer.png`, `the-future-of-mcp-why-the-future-of-agen-image.png`); both copied to `raw/assets/`
- Spawned 10 `source_writer` agents in parallel; orchestrator read no raw file, only receipts
- Reconciled an mcp entity-vs-concept split before running the tail: 6 of 9 writers that referenced MCP put it under `entities:`, 3 under `concepts:` — standardized all 6 to `concepts:` (both frontmatter and the Connections section) so the ≥2 count isn't split across two namespaces for the same slug
- Source pages: `agentic-graphrag-via-mcp-servers`, `how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs`, `mongodb-for-an-ai-agent-unified-memory`, `owning-your-context-layer`, `stop-using-mcp-servers-to-access-your-mongodb-postgres`, `system-architecture-of-future-ai-apps-ui-tui-ide-extension`, `the-future-of-mcp-vs-skills`, `the-future-of-mcp-why-the-future-of-agents-is-mcp-skills`, `the-right-way-of-building-agents-with-mcp-servers`, `why-mcp-is-not-dead`
- New entity pages (≥2 mentions): `claude-code` (6), `fastmcp` (6), `prefect` (5), `mongodb` (3), `david-soria-parra` (2)
- New concept pages (≥2 mentions): `mcp` (9), `skills` (6), `cli` (4), `agent-memory` (3), `orchestration` (3), `agent-connectivity` (2), `graphrag` (2)
- Waiting at 1 mention: `cloudflare`, `maxime-labonne`, `mongosh`, `neo4j`, `agent-harness`, `claude-md`, `code-mode`, `context-layer`, `event-sourcing`, `hooks`, `mcp-applications`, `progressive-disclosure`, `progressive-tool-discovery`, `unified-memory`, `vector-search`
- Wrote `overview.md` (3 themes: connectivity as several complementary layers not one, where orchestration logic should live, unifying agent memory across vector/graph/event-sourced storage), regenerated all `index.md` files — `build_index_md.py` reported 0 errors, 0 warnings
- Final state: 10 sources, 5 entities, 7 concepts, 22 pages total

## 2026-08-31 ingest | 4 Substack articles from data_input_examples/substack_articles.md

- Fetched 4 article URLs from `decodingai.com` via `fetch_article.py` (origin `article`); 0 skipped, all new — none of the 4 raw paths existed yet
- Spawned 4 `source_writer` agents in parallel; orchestrator read no raw file, only receipts
- Source pages: `article-building-a-coding-agent-from-scratch-system-design`, `article-the-coding-agent-loop`, `article-run-coding-agents-safely`, `article-context-engineering-for-coding-agents` (all 4 are lessons from Paul Iusztin's "Building a Coding Agent From Scratch" course)
- New entity pages (≥2 mentions, newly qualifying): `decode` (2), `modal` (2), `pydantic-ai` (2)
- New concept pages (≥2 mentions, newly qualifying): `agent-harness` (2)
- Updated entity pages (new sources merged in): `claude-code` (6 → 10)
- Updated concept pages (new sources merged in): `agent-memory` (3 → 6), `cli` (4 → 6), `orchestration` (3 → 5), `skills` (6 → 8)
- Unchanged qualifying pages this run touched no new source for: `fastmcp`, `mongodb`, `prefect`, `david-soria-parra`, `mcp`, `graphrag`, `agent-connectivity`
- Rewrote `overview.md` — added a 4th theme ("the harness, not the model, makes the agent") anchored on the new `agent-harness` concept's tension between two framings of "harness"; regenerated all `index.md` files — `build_index_md.py` reported 0 errors, 0 warnings
- Waiting at 1 mention (14 entities, 15 concepts): `abhishek-bhardwaj`, `cloudflare`, `codex-cli`, `docker`, `kitaru`, `mario-zechner`, `maxime-labonne`, `mongosh`, `neo4j`, `opencode`, `openrouter`, `opik`, `pi-agent`, `ty`, `ai-evals`, `claude-md`, `code-mode`, `compaction`, `context-engineering`, `context-layer`, `event-sourcing`, `hooks`, `lsp`, `mcp-applications`, `progressive-disclosure`, `progressive-tool-discovery`, `sandboxing`, `unified-memory`, `vector-search`
- Final state: 14 sources, 8 entities, 8 concepts, 30 pages total

## 2026-08-31 ingest | GitHub repo decodingai-magazine/building-a-coding-agent-from-scratch-course

- Cloned `github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course` via `clone_repo.py` (origin `repo`, action `cloned`, first ingest); pinned at commit `6ee643f`, branch `main`
- Spawned 1 `repo_writer` agent in architecture mode; orchestrator never read the clone. This is "Decode," the coding agent built lesson-by-lesson in the 4 Substack articles ingested earlier — the writer reused the existing `decode` entity slug rather than inventing a new one
- Repo page: `wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE.md`
- New entity page (≥2 mentions, newly qualifying): `kitaru` (2) — ZenML's durable-execution runtime, substantively implemented in `runtime/flow.py` for `decode run`/`decode replay`
- Updated entity pages (repo merged in as a 3rd source): `decode` (2 → 3, added a `## Tensions` section — the pinned commit's code disagrees with the lesson-4 article on system-prompt assembly timing and the presence of a `PermissionGate`), `modal` (2 → 3), `pydantic-ai` (2 → 3)
- Updated concept pages (repo merged in): `agent-harness` (2 → 3), `agent-memory` (6 → 7), `cli` (6 → 7), `orchestration` (5 → 6), `skills` (8 → 9)
- Unchanged qualifying pages this run touched no new source for: `claude-code`, `fastmcp`, `mongodb`, `prefect`, `david-soria-parra`, `mcp`, `graphrag`, `agent-connectivity`
- Rewrote `overview.md` (now includes a Repos section); regenerated all `index.md` files including the new `wiki/repos/index.md` — `build_index_md.py` reported 0 errors, 0 warnings
- Waiting at 1 mention (13 entities, 15 concepts): `abhishek-bhardwaj`, `cloudflare`, `codex-cli`, `docker`, `mario-zechner`, `maxime-labonne`, `mongosh`, `neo4j`, `opencode`, `openrouter`, `opik`, `pi-agent`, `ty`, `ai-evals`, `claude-md`, `code-mode`, `compaction`, `context-engineering`, `context-layer`, `event-sourcing`, `hooks`, `lsp`, `mcp-applications`, `progressive-disclosure`, `progressive-tool-discovery`, `sandboxing`, `unified-memory`, `vector-search`
- Final state: 14 sources + 1 repo, 9 entities, 8 concepts, 32 pages total

## 2026-08-31 query | Decode's agent loop mechanics

- question: "how does the coding agent's loop actually work?"
- pages used: 3 (`wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE`, `wiki/sources/article-the-coding-agent-loop`, `wiki/concepts/agent-harness`)
- gap noticed: none — the repo's "Core loop" section plus the loop-focused article fully cover the mechanics; `agent-harness` supplied the loop-vs-harness framing tension
