# "You don't need a browser anymore"

**Post 16:** MCP App. Serve UIs via MCP apps (e.g., Prefect Prefab)

[https://drive.google.com/file/d/1jqnQ77oThB48O5WYo75xHPHP2_VHocjG/view?usp=drive_link](https://drive.google.com/file/d/1jqnQ77oThB48O5WYo75xHPHP2_VHocjG/view?usp=drive_link)

---

A narrative, code-free handoff for a LinkedIn post about building Tree's in-chat UIs with
**FastMCP + Prefab**. The companion technical doc is [`MCP_APP.md`](https://app.notion.com/p/MCP_APP.md).

**Sponsor framing:** This post is about a capability **FastMCP** makes practical — turning
a backend tool into an interactive UI that renders inside the chat. FastMCP should be the
hero of the "how." The magic isn't just the underlying standard; it's that FastMCP
collapses it into a few lines of Python. Credit **FastMCP** and its **Prefab** UI system by
name; link the docs.

**Core thesis:** For decades, "show the user something interactive" meant building a web
app and sending them a link. That era is ending. With FastMCP, I returned an interactive UI
*as the result of a tool call* — and it rendered **directly inside the AI chat**. No
browser tab, no website, no frontend to deploy. The chat became the app.

## The 6 W's

- **Who:** Me — building Tree, a personal assistant whose memory is a knowledge graph.
- **What:** An interactive graph explorer and a live dashboard that appear *inside* the
chat — hover nodes, sort tables, zoom clusters — built with FastMCP + Prefab.
- **When:** Now. MCP Apps + FastMCP's app layer are brand-new — bleeding edge, which is why
almost nobody is posting about it yet.
- **Where:** Inside AI hosts like Claude — Desktop, web, IDE. One FastMCP server, every host.
- **Why:** My assistant *knows* my data. Why should it hand me a link to go look at it
somewhere else?
- **How:** A FastMCP tool returns a UI instead of text. FastMCP serializes it, sandboxes
it, and the host renders it inline. The AI keeps a short summary so it can keep reasoning;
the human gets something to click.

## The problem (the "before" world)

AI assistants talk well, but show poorly. When the answer is a graph of 142 connected
things or a table of 50 records, words fail three ways: the AI narrates data that was never
meant to be prose; it floods its own context window with raw data; and the human can't
hover, sort, or zoom a paragraph. So the standard fix was: go build a web app — frontend,
server, hosting, auth, deploy — a whole second product, just so the user can *see* their
data. The interactive part always lived **outside** the conversation.

## The solution (the "after" world)

The UI now ships **from the same FastMCP tool that produced the data**, and renders
**inside the chat**. Ask to see the knowledge graph → an interactive, draggable, hover-able
graph appears in the conversation. Ask a follow-up → a dashboard. And there was **no web
app to build**: no separate codebase, no bundler, no hosting bill, no auth layer. The UI
became a *return value*.

## What makes FastMCP Prefab special (the mechanics that matter)

This is the section to make FastMCP shine.

- **You write the UI in pure Python — no HTML, no JavaScript.** Prefab gives you 100+
declarative components (data tables, six chart types, metrics, badges, layout
rows/columns, form inputs). You compose them with Python `with`blocks where indentation
*is* the layout. FastMCP serializes and renders the whole thing client-side. The entire
ceremony to turn a tool into a UI is a **single flag** (`app=True`).
- **FastMCP handles all the hard, scary parts for you — automatically.** Sandboxed iframe,
strict deny-by-default Content Security Policy, serialization, security isolation,
lifecycle. You don't hand-roll any of it. That's the FastMCP value: the dangerous
plumbing is invisible and safe by default.
- **It's a real reactive app, not static HTML.** Prefab ships **client-side reactive
state**: declare state, bind components to it with reactive references, and the UI updates
**instantly** as the user types, toggles, or filters — *with zero server round-trips*.
Search/sort/paginate/conditional-show all happen in the browser. That's the line between
"a screenshot of data" and "a live application," and Prefab gives it to you for free.
- **One result serves both audiences.** FastMCP lets a tool return a short text summary
*for the model* alongside the rich UI *for the human*. The AI reasons on the summary; the
user explores the interface. Same call, two consumers.
- **When the UI must *do* things, FastMCP scales up cleanly.** Its **FastMCPApp** pattern
separates model-visible UI launchers from UI-only backend handlers, so a button can call
a server tool (submit, save, search, mutate). Its standout trick: **composition safety** —
the UI references backend tools by *function*, not by string name, so wiring keeps working
even when you mount the server under a namespace (where string-based names silently
break). A subtle, real-world correctness win you'd otherwise engineer yourself.
- **The endgame is wild: FastMCP can let the model *write the UI at runtime*.** Its
Generative UI provider lets the assistant author Prefab interfaces on the fly,
**streaming the UI into existence as it generates tokens** — components materialize live
as the model "types." FastMCP runs the generated code in a browser sandbox for the live
preview, then re-validates it server-side before swapping in the final result. The model
is constrained to Prefab + the Python standard library (no arbitrary packages), so "the AI
builds your UI" stays *safe by construction*. There's no fixed screen to design — the
interface is synthesized per request.
- **It's built on the open MCP Apps standard — FastMCP is the ergonomic layer on top.**
Under the hood it's the official MCP Apps extension (sandboxed UI resources, a host↔iframe
message channel, capability negotiation so unsupported hosts degrade gracefully). FastMCP
gives you all of that without touching the protocol — and the same app runs across every
MCP host.

## How it works in practice (what I actually built)

Two views of the *same* memory, fed by **one shared data layer** (prepare the data once,
render it many ways):

- A **force-directed graph** for topology — *how things connect*. Hover any node or
relationship for its details; search, drag, zoom.
- A **dashboard** for the summary — *what's in there*: counts by type, a chart, and
sortable/searchable tables.

And it **fails gracefully**: FastMCP checks whether the host supports rich UIs, and falls
back to a self-contained file/link when it doesn't — so it never breaks, and the AI never
has to hand-author a web page.

## Why this is groundbreaking (lean in)

- **You don't need a browser anymore.** For AI-native tools, the host is the runtime and
the chat is the surface. The interface comes to you, in the conversation.
- **A UI stops being a product and becomes a return value** — collapsing the frontend, the
hosting, and the glue into almost nothing.
- **Write once, render everywhere** — one FastMCP server drives the same UI across every AI
host.
- **The model can generate the interface itself**, designed to fit what you just asked. We
stop building dashboards you open, and start getting dashboards that appear when you ask.
- **The analogy:** the way the browser absorbed installable desktop apps, the AI chat is
starting to absorb the frontend for AI-native tools — and FastMCP is the toolkit that
makes that buildable today.

## The honest edge (keeps it credible)

It's early. This works where the host implements MCP Apps and degrades to a file/link where
it doesn't. FastMCP's app layer (and Prefab) are under active development — pin your
versions. Generative UI needs an extra runtime. None of that breaks the thesis; it means
**you're early** — which is the opportunity.

## Builder's notes worth telling (texture)

- I built the dashboard **three ways on purpose** — to compare FastMCP's paradigms side by
side — then **deleted two** once I knew the simple interactive tool fit. Build to compare,
then delete.
- A UX simplification (details on hover instead of click) also *deleted* code — rare when
"nicer for the user" and "less code" agree.
- A debugging beat: my UI clearly rendered the data, but a test couldn't "see" it — because
I was inspecting the rendered widget instead of the data. Lesson: test the data, not the
widget.

## Tone & arc

Open with the provocation ("we're about to stop building web apps for a whole class of
software"), tell the small personal story (building my assistant's memory, realizing I
didn't need a dashboard *website* — FastMCP let me render the graph *in the chat*), land the
before/after, spotlight **what FastMCP + Prefab specifically make trivial** (Python-only UI,
reactive state, safe-by-default sandbox, generative UI), then zoom out to the thesis and the
browser analogy. Builder-voice, concrete, slightly contrarian. Kicker: the model generating
its own UI.

## Quotable one-liners (lift freely)

- "I turned a backend tool into an interactive app with one flag and zero HTML. FastMCP
rendered it inside the chat."
- "For decades, 'show the user something' meant 'build a web app.' FastMCP just made that
optional."
- "With Prefab I wrote the UI in pure Python — and got a reactive app that updates with zero
server round-trips."
- "The wild part: FastMCP can let the model *write the UI as it talks* — streaming the
interface into existence, safely sandboxed."
- "Your AI already knows your data. Why is it still sending you a link to go look at it
somewhere else?"

## Links to credit

- FastMCP Apps — Prefab: [https://gofastmcp.com/apps/prefab](https://gofastmcp.com/apps/prefab)
- FastMCP Apps — FastMCPApp: [https://gofastmcp.com/apps/fastmcp-app](https://gofastmcp.com/apps/fastmcp-app)
- FastMCP Apps — Generative UI: [https://gofastmcp.com/apps/generative](https://gofastmcp.com/apps/generative)
- FastMCP Apps — Low-level / custom HTML: [https://gofastmcp.com/apps/low-level](https://gofastmcp.com/apps/low-level)
