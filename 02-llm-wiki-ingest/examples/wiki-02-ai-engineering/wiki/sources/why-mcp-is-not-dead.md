---
type: source
title: Why MCP is Not Dead
description: "MCP isn't dead — it's the wrong tool for personal setups but the right one for distributing governed business logic to many users, alongside CLIs and skills."
origin: local
original_path: "data_input_examples/notes/02-medium/Why MCP is Not Dead.md"
source_url: null
authors: []
published_date: null
raw_file: raw/why-mcp-is-not-dead.md
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T17:23:45Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/skills]]"
---

# Why MCP is Not Dead

> [[raw/why-mcp-is-not-dead|Raw]] · local

## Summary

The note is a direct rebuttal to a Prefect LinkedIn post declaring "MCP is dead"
— written as the author's notes from a video/event framed around the same
provocation. Its core move: MCP isn't dead, people are just pointing it at the
wrong problem. For personal, single-user setups, a CLI to your database or
vector store, an `llms.txt` sitemap, or skills gluing steps together are simpler
and genuinely sufficient — that's the experience driving the "MCP is dead" take.

At professional/business scale the calculus flips. Telling thousands or millions
of customers to install a CLI and drop a pile of markdown files on their machine
is a non-starter, and it forecloses any real conversation about governance and
security. CLIs have never had a good story for centralized distribution or
control; MCP servers exist precisely to solve that — one place to own the data,
secure it, monitor the business logic running against it, and distribute it (via
skills and prompts) to many clients and harnesses (Claude Code, OpenCode,
OpenClaw) at once.

The author grounds this in two personal systems: a GraphRAG-powered memory
service with enough custom business logic and hosted infra that exposing it as
MCP tools made far more sense than files-and-skills would have; and a "digital
twin" that reaches siloed third-party services (Notion, Readwise) only through
their MCP servers, while local files (Obsidian) and dev-time infra (MongoDB,
Prefect) stay CLI-driven because an agent having full, unmediated access there is
fine.

## Key claims

- "MCP is not dead" — it was misapplied to personal use cases where a CLI,
  `llms.txt` sitemaps, or skills already suffice; that's a fact about the use
  case, not the protocol. [[raw/why-mcp-is-not-dead|cite]]
- At business scale, requiring customers to install a CLI and set up markdown
  files on every machine is unworkable, and governance/security aren't even
  discussable in that model. [[raw/why-mcp-is-not-dead|cite]]
- CLIs have never had a good answer for governed distribution to many users; MCP
  servers centralize business logic in one place that can be secured, monitored,
  and distributed from. [[raw/why-mcp-is-not-dead|cite]]
- An MCP server can expose the same skills-and-prompts pattern server-side, so
  the server itself becomes the single point of control and distribution.
  [[raw/why-mcp-is-not-dead|cite]]
- In the author's own systems, MCP is reserved for complex or siloed/hosted
  services (a GraphRAG memory service; Notion, Readwise), while CLIs handle
  local or dev-time access (Obsidian, MongoDB, Prefect). [[raw/why-mcp-is-not-dead|cite]]
- Conclusion: use MCP "when it makes SENSE," alongside Claude Code skills and
  CLIs — not as a universal replacement for either. [[raw/why-mcp-is-not-dead|cite]]

## Notable quotes

> "MCP is NOT dead." You were just using it wrong.
> — [[raw/why-mcp-is-not-dead|location]]

> "First thing we have to do is install this CLI on everyones machines then we
> have to setup a bunch of markdown files on all of these machines…" people will
> laugh at you
> — [[raw/why-mcp-is-not-dead|location]]

> "MCP is not dead." You just need to use it when it makes SENSE, not for
> everything, along with Claude code skills and CLIs
> — [[raw/why-mcp-is-not-dead|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/cli]], [[wiki/concepts/skills]]

> Synthesis: A direct rebuttal to the "MCP is dead" narrative (itself sourced
> from a Prefect LinkedIn post), reframing the debate as CLI/skills-for-personal-use
> vs. MCP-for-governed-multi-user-distribution rather than one tool replacing the
> other.
