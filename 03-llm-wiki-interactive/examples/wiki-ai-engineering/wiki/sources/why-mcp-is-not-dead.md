---
type: source
title: Why MCP is Not Dead
description: Argues that "MCP is dead" confuses personal single-user tooling with the professional need to govern and distribute business logic at scale, where MCP servers remain the right tool.
origin: local
original_path: data_input_examples/notes/02-medium/Why MCP is Not Dead.md
source_url: null
authors: []
published_date: null
raw_file: raw/why-mcp-is-not-dead.md
created: 2026-08-29T16:10:55Z
timestamp: 2026-08-29T16:10:55Z
entities:
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/skills]]"
---

# Why MCP is Not Dead

> [[raw/why-mcp-is-not-dead|Raw]] · local

## Summary

Written as a rebuttal to a viral "MCP is dead" take (the note is explicitly triggered by
a LinkedIn post and a companion in-person event), the note argues that the "dead"
verdict is a category error: people who dropped MCP for CLIs, `llms.txt` sitemaps, and
skills are solving a *personal* setup problem, not a *business* one. The moment you have
to deploy the same logic to thousands or millions of users, installing a CLI and a pile
of markdown files on every machine stops being viable, and nobody can govern or secure
it. MCP servers persist because they give a single, centrally governed place to expose
business logic and data, while the data itself stays in the owner's own storage.

The author backs the framing with their own stack rather than abstract argument: a
"Personal Assistant" GraphRAG project is exposed as MCP tools precisely because its
read/write logic is too specific and its infrastructure too cloud-hosted for a CLI or
plain skill files to cover, while day-to-day access to MongoDB and Prefect during
development goes through their CLIs instead. Siloed business services (Notion,
Readwise) are only reachable safely through their MCP servers, whereas purely local
files (Obsidian) are managed directly by Claude Code or its CLI. The conclusion is
explicitly pluralist: MCP, CLIs, and Claude Code skills are complementary tools for
different jobs, not competitors.

## Key claims

- "MCP is dead" mistakes a personal-tooling preference (CLIs, `llms.txt`, skills) for a
  verdict on MCP's fitness for business-scale deployment. [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- Distributing business logic via CLI-plus-markdown-files to "thousands or millions" of
  customer machines is unworkable, and offers no governance or security story. [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- MCP servers keep data in the owner's own storage while still distributing access to
  multiple clients and harnesses (Claude Code, OpenCode, OpenClaw) at once. [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- In the author's own Personal Assistant project, business logic that is too specific
  and too cloud-hosted for a CLI or skill files is instead exposed as MCP tools, while
  MongoDB and Prefect are still accessed by CLI during development. [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]
- Siloed third-party services (Notion, Readwise) are only safely reachable through their
  MCP servers, whereas purely local files (Obsidian) are managed directly by Claude Code
  or its own CLI. [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|cite]]

## Notable quotes

> "MCP is NOT dead." You were just using it wrong.
> — [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|location]]

> "First thing we have to do is install this CLI on everyones machines then we have to setup a bunch of markdown files on all of these machines…" people will laugh at you
> — [[raw/why-mcp-is-not-dead#Why MCP is Not Dead|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/cli]], [[wiki/concepts/skills]]

> Synthesis: A practitioner's reaction to a viral "MCP is dead" post rather than new
> research — its lasting contribution is the personal-vs-business-scale framing for
> when to reach for MCP versus a CLI or a skill, which later sources on MCP should be
> checked against rather than restated as if novel.
