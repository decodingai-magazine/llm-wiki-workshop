---
type: source
title: The Bare-Bones Coding Agent Loop
description: The implementation lesson — one agent loop, nine tools, three input modes (steer, follow-up, abort), and the session log that makes a turn replayable.
origin: article
original_path: https://www.decodingai.com/p/the-coding-agent-loop
source_url: https://www.decodingai.com/p/the-coding-agent-loop
authors: ["Paul Iusztin"]
published_date: "2026-07-28T13:54:35+00:00"
raw_file: raw/article-the-coding-agent-loop.md
created: 2026-08-29T10:45:00Z
timestamp: 2026-08-29T10:45:00Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/modal]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agentic-coding-loop]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/observability]]"
  - "[[wiki/concepts/context-rot]]"
---

# The Bare-Bones Coding Agent Loop

> [[raw/article-the-coding-agent-loop|Raw]] · article · [Original](https://www.decodingai.com/p/the-coding-agent-loop)

## Summary

Lesson two builds the loop the previous article designed, and its most useful
claim is about proportion: **"the tools are 90% of why this is a coding agent and
not any other kind of AI agent."** The minimum set is four — `read`, `write`,
`edit`, `bash` — which one referenced agent ships in under 1,000 tokens of prompt
plus definitions and still places top-10 on a public benchmark. Around them sit
`glob`, `grep`, `todo_write`, `web_fetch` and `ask_user`.

The `edit` tool gets the most attention, and deservedly: it is a find-and-replace
whose difficulty is entirely in what the model *cannot see*. Line-ending
conventions and byte-order marks are normalized away so a match never fails on
invisible characters; a miss retries with whitespace collapsed; and the match must
be **unique** — zero hits returns "not found", two or more returns "ambiguous",
and both come back to the model as a retry rather than an error.

The harness state reaches tools by dependency injection: a single deps object
carrying the working directory, an event sink, the permission gate, two resolver
callbacks and the task list. Tools therefore reach the terminal without importing
the UI, and tests swap the object.

The interaction section is the other half. A TUI can take over the viewport or
append to scrollback; this one appends, keeping scrollback and search. Input
arriving mid-turn cannot be injected immediately without corrupting a tool call,
so it is buffered and released at boundaries in three modes: **steering** (runs
between tool calls), **follow-up** (held until the turn ends), and **cooperative
abort** (stops at the next boundary and clears both queues).

## Key claims

- The tools are what make it a *coding* agent; the loop itself is generic. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- Four tools — read, write, edit, bash — are enough to be competitive on a public benchmark. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- `edit` must normalize invisible formatting the model was never shown, and must refuse ambiguous matches. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- A failed edit returns a retry to the model rather than an error to the user — the loop self-corrects. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- Harness state is injected into every tool call, so tools never import the interface and are trivially testable. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]
- Mid-turn input must be buffered and released at boundaries; injecting it immediately corrupts the current tool call. [[raw/article-the-coding-agent-loop#The TUI and the Queues|cite]]
- Three input modes cover the interaction surface: steer, follow up, abort — with abort clearing both queues to protect the history. [[raw/article-the-coding-agent-loop#The TUI and the Queues|cite]]
- A plan stored as a file on disk is argued to beat an in-memory TODO list the agent has to track. [[raw/article-the-coding-agent-loop#The Core Tools|cite]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/modal]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/agentic-coding-loop]], [[wiki/concepts/provider-abstraction]], [[wiki/concepts/observability]], [[wiki/concepts/context-rot]]

> Synthesis: The most concrete tool-design source in the wiki, and its lesson generalizes past coding agents — the hard part of a tool is not the operation but the failure modes the model cannot see.
