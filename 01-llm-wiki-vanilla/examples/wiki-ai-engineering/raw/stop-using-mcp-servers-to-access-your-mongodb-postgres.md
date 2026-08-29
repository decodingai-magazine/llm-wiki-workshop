# Stop using MCP Servers to access your MongoDB/Postgres database when using coding agents

When developing using coding agents and you need access to your MongoDB/PostgreSQL database, instead of adding useless complexity with an MCP Server that fills in your context just instruct the agent to use the mongosh/psql CLI command through your [CLAUDE.md](http://CLAUDE.md) file or through a skill if you need something more complex. For example, using mongosh, it writes custom scripts to write, query and observe the data from your mongodb in a loop being able to either understand your data, introduce mock data or suggest collection schemas.

**Full note:**

## You don't need an MCP server for database access — one line in CLAUDE.md and mongosh is all you need

### Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | The MCP server hype has developers building custom integrations to give coding agents database access. That means writing a server, defining schemas, managing connections, debugging tool calls, and watching your context window fill up with connection metadata and tool response wrappers. All to let the agent run a query. |
| **Solution**    | One line in a handwritten CLAUDE.md: `Use mongosh to interact with MongoDB directly through the CLI.` The coding agent already has shell access. It writes custom mongosh scripts on the fly to query, write, inspect, and debug — no server, no schema, no wrappers. |
| **Transformation** | Database access goes from a multi-file integration project to a single instruction. The agent writes throwaway scripts, reads the output, and moves on. Context stays clean. Same principle applies to psql, redis-cli, sqlite3 — any CLI database tool. |
| **Hook**        | I replaced an entire MCP server with one line in my CLAUDE.md file. |
| **Target audience** | Developers using AI coding agents (Claude Code, Cursor, Windsurf, etc.), anyone considering building MCP servers for database access, engineers who value simplicity over integration ceremonies. |

### Outline

1. The temptation: you want your coding agent to access your database, so you reach for an MCP server. Why this is over-engineering.
2. The alternative: one line in CLAUDE.md — `Use mongosh to interact with MongoDB directly through the CLI.`
3. What the agent actually does with it: writes throwaway scripts, queries data shapes, validates pipeline output, inserts mock data, inspects indexes.
4. The CLAUDE.md philosophy: 152 lines, handwritten, all signal — why this beats auto-generated docs and framework boilerplate.
5. The broader principle: CLI tools are the universal integration layer. mongosh, psql, redis-cli, sqlite3 — they all work the same way.
6. When you might actually need an MCP server — and why it's not for development workflows.

---

### Full body

#### The MCP server temptation

You're building with a coding agent. You need it to interact with your database — query collections, inspect schemas, check if your pipeline wrote the right data, maybe insert some test documents. The modern instinct is: "I'll build an MCP server."

So you write a server. You define tool schemas. You handle connections and authentication. You write serializers for the responses. You register it with your agent. You debug why the tool call returned an error. You realize the response is filling half your context window with connection metadata and JSON wrappers.

All so the agent can run `db.knowledge_graph.find({kind: "node"}).limit(5)`.

#### One line

Here's what I did instead. In my CLAUDE.md — the project instruction file that Claude Code reads before doing anything — I added one line:

```
Use `mongosh` to interact with MongoDB directly through the CLI.
```

That's it. The agent already has shell access via the Bash tool. `mongosh` is available because MongoDB runs in Docker Compose. The connection string is in the environment. The agent can now:

- Query any collection: `mongosh --eval 'db.knowledge_graph.find({kind: "node"}).limit(5)'`
- Count documents: `mongosh --eval 'db.documents.countDocuments({})'`
- Inspect indexes: `mongosh --eval 'db.knowledge_graph.getIndexes()'`
- Check aggregation output: `mongosh --eval 'db.knowledge_graph_log.aggregate([{$group: {_id: "$kind", count: {$sum: 1}}}])'`
- Insert test data: write a multi-line script, pipe it to mongosh
- Validate pipeline results: query after running a pipeline, compare before and after

No server to maintain. No schema to define. No context overhead. The agent writes a shell command, reads the output, and moves on.

#### What the agent actually does

During development of my GraphRAG system, the agent used `mongosh` constantly — without me ever asking it to:

**Validating the infrastructure setup.** Before writing any application code, the agent wrote `test_mongodb_setup.py` — a script that seeds test data, creates text and vector search indexes, and verifies all three search pillars (text, vector, graph). It ran this in a loop, tweaking the setup until all three passed.

**Debugging silent query failures.** When queries returned zero results with no errors, the agent ran `mongosh` to check: Are there documents in the collection? Do the indexes exist? What does a raw `$text` query return? This is how we discovered that `$out` was dropping all indexes on every materialization — the collection had data but no indexes.

**Inspecting materialization output.** After running the aggregation pipeline, the agent queried the materialized collection to verify node IDs were composite (`"person:paul_iusztin"` not just `"paul_iusztin"`), edges had the right structure, and reverse edges were created for the right node-type pairs.

**Understanding data shapes.** When implementing the query layer, the agent sampled real documents to understand the actual field structure — what properties nodes had, what edge types existed, how many hops a typical traversal would cover.

Every interaction was a throwaway script. No state to manage, no connection to maintain, no tool schema to update when the data model changed.

#### The CLAUDE.md philosophy: signal over noise

The `mongosh` line works because it sits inside a CLAUDE.md that is 152 lines of pure signal. The entire file is handwritten — not auto-generated, not a template dump, not an LLM-produced summary of my codebase.

It's structured as three sections:

**The Why** — one sentence explaining the project's purpose.

**The What** — key components (data pipeline, memory pipeline, unified memory, agentic tools), project structure (folder tree with annotations), design choices (async Python, idempotent pipelines, UTC dates, loose clean architecture), tech stack (every tool mapped to its role), and test conventions (AAA pattern, parametrize, mocker fixtures).

**The How** — build/test/run commands via Make, development workflow (plan → implement → test → scan → update docs), and critical one-liners like `Use mongosh to interact with MongoDB directly through the CLI.`

What's NOT in the file:
- Auto-generated API docs
- Framework boilerplate
- Verbose descriptions of obvious things
- Anything the agent can figure out by reading the code

The result: when the agent starts working, it knows the architecture, the conventions, the tools, and the workflow. It doesn't need to ask "what framework are we using?" or "where do tests go?" or "how do I check the database?" — everything is answered before it's asked.

This is the opposite of how most people use CLAUDE.md (or Cursor rules, or .windsurfrules). They either leave it empty, paste their entire README, or auto-generate it from the codebase. A handwritten, slim file with high signal density is worth more than any of those approaches.

#### The broader principle: CLI tools as the universal integration layer

This isn't specific to MongoDB or mongosh. The same principle applies to any database with a CLI tool:

- **PostgreSQL**: `psql -c "SELECT count(*) FROM users;"`
- **Redis**: `redis-cli GET session:abc123`
- **SQLite**: `sqlite3 app.db "SELECT * FROM migrations ORDER BY id DESC LIMIT 5;"`
- **MySQL**: `mysql -e "SHOW TABLES;"`

The coding agent already has shell access. The CLI tools already exist. The connection details are already in the environment. Adding an MCP server between the agent and the database is adding a translation layer where none is needed.

The key insight: during development, you don't need a structured, typed, schema-validated interface to your database. You need to run queries and read results. That's exactly what CLI tools do.

#### When you might actually need an MCP server

There are valid use cases for MCP servers:
- **Production agentic tools** where the agent operates on behalf of end users and needs guardrails, rate limiting, and access control
- **Cross-service orchestration** where the agent coordinates between multiple systems that don't have CLI tools
- **Non-technical users** who need a natural language interface to a database without shell access

But for development workflows — where you're building, debugging, and iterating with a coding agent — the CLI tool wins. Every time.

[VERIFY] The user's specific examples of mongosh usage during development — confirm they want to include specific examples or keep it more general.
