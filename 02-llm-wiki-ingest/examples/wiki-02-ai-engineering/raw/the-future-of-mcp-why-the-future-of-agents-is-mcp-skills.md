# The future of MCP. Why the future of agents is MCP, skills and CLIs combined

The future of MCP. Why the future of agents is MCP, skills and CLIs combined (based on the [AI Engineering conference video](https://www.youtube.com/watch?v=v3Fr2JR47KA) made by David Soria Parra one of the creators of MCP from Anthropic, who said that FasMCP is I quote: “It’s just way f*** better than our Python SDK that we shipped”)

---

Readwise source with all the notes: [https://read.readwise.io/archive/read/01kpmy78m7aq4tsm1dawdjnmh0](https://read.readwise.io/archive/read/01kpmy78m7aq4tsm1dawdjnmh0)

![[data_input_examples/notes/02-medium/assets/the-future-of-mcp-why-the-future-of-agen-image.png]]

### Post

There is a new way of building software powered by AI.

Here is the architecture:

Most teams are building AI applications by taking existing frontend/backend architectures and stitching agents and MCP servers into the backend.

Which makes sense.

Every new paradigm starts by adapting the old one.

But as

[**David Soria Parra**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

(

[**Anthropic**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

, co-creator of MCP) put it:

"Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together."

This idea changed how I think about agent architecture...

Browsers remain the primary interface.

But we're moving toward a world where a single chat interface can render whatever the agent returns.

The browser was built to navigate websites.

AI-native interfaces are being built to generate them on demand.

The architecture I see emerging across serious AI applications looks like this:

𝟭/ 𝗣𝗿𝗲𝘀𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻

The thin renderer.

Today, this means:

- TUI (Claude Code)
- IDE extensions (Cursor, VS Code)
- Web applications
- Desktop applications (ChatGPT, Gemini)

With MCP Apps, clients can render server-shipped UIs directly from the harness.

The same MCP App can run across Claude, ChatGPT, and Cursor without rewriting the UI.

𝟮/ 𝗛𝗮𝗿𝗻𝗲𝘀𝘀 + 𝗥𝘂𝗻𝘁𝗶𝗺𝗲

The brain of the system.

This is where:

- The LLM ↔ tool loop lives
- Memory lives • Permissions live
- Orchestration lives

Agents are becoming long-running systems rather than single inference calls.

Which means they need:

- Durable execution
- Retries
- Checkpoints
- Human approvals
- Observability

This is why I increasingly think of tools like

[**Prefect**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

as part of the runtime itself.

𝟯/ 𝗖𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝘃𝗶𝘁𝘆

The right tool for the right job.

- Skills → reusable user domain knowledge
- CLIs → local host capabilities
- MCP Clients → auth, resources, tasks, and UI

Modern agents use all three.

Single-mechanism agents underperform.

𝟰/ 𝗠𝗖𝗣 𝗦𝗲𝗿𝘃𝗲𝗿𝘀

Where business logic and private data live.

A modern MCP server ships:

- Tools
- Resources
- Prompts
- Skills
- MCP Apps
- Tasks + elicitation

In Python,

[**FastMCP**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

(by

[**Prefect**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

) has effectively become the practical default.

Even

[**David Soria Parra**](https://platform.authoredup.com/calendar?month=0&actors=LNP_ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE#)

said: "It’s just way better than our Python SDK that we shipped."

The MCP ecosystem recently crossed 110M monthly downloads.

React took roughly twice as long to get there.

This is what "full connectivity" looks like.

Four layers.

Each independently decomposable.

MCP acts as the connective tissue between them.

P.S. Do you think browsers become obsolete once chat interfaces can render any application on demand?
