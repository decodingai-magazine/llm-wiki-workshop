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
