---
type: source
title: Why MCP is Not Dead
description: An outline for a rebuttal post arguing that "MCP is dead" only holds for personal setups, and that distribution, governance and security are what keep servers necessary at business scale.
origin: local
original_path: data_input_examples/notes/01-easy/Why MCP is Not Dead.md
source_url: null
authors: []
published_date: null
raw_file: raw/why-mcp-is-not-dead.md
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
entities:
  - "[[wiki/entities/mcp]]"
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/obsidian]]"
concepts:
  - "[[wiki/concepts/governance]]"
  - "[[wiki/concepts/cli-tools]]"
  - "[[wiki/concepts/agent-skills]]"
  - "[[wiki/concepts/connectivity-stack]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/agent-harness]]"
---

# Why MCP is Not Dead

> [[raw/why-mcp-is-not-dead|Raw]] · local

## Summary

A post outline — hook, argument, examples, conclusion — pushing back on the
"MCP is dead" discourse. The author accepts the premise's evidence and rejects
its scope: people reaching that conclusion are reasoning from **personal**
setups, where a CLI to the database, an `llms.txt` sitemap and a few skill files
genuinely are enough. The claim breaks the moment the same logic has to serve
thousands or millions of customers, because the deployment story becomes "install
this CLI on everyone's machine and set up a bunch of markdown files on all of
them," which the author expects to be laughed out of the room.

From there the argument is about distribution, not capability. A server is the
mechanism we already have for shipping business logic from one central place, and
it is the only one of the three where governance, monitoring and security are
tractable: "we had CLIs for so long and we haven't found a good way to govern
them when distributing them to users." MCP inherits that property — your data
stays in your storage, you distribute access to many clients at once, and you
govern the logic on your server rather than on a million machines.

The examples are the author's own dual setup, and they are deliberately
two-sided: the personal-assistant memory is exposed as MCP tools because the
business logic for writing and searching it is specific and the infrastructure is
in the cloud — "doing this through a CLI would have been a nightmare" — while
during development the same author reaches for the MongoDB and Prefect CLIs, and
lets Claude Code work on local Obsidian files directly. Siloed SaaS (Notion,
Readwise) is reachable only through their MCP servers.

## Key claims

- "MCP is dead" generalizes from personal setups, where CLIs, sitemaps and skills genuinely suffice, to business deployment, where they do not. [[raw/why-mcp-is-not-dead|cite]]
- At business scale the blocker is distribution and governance, not capability: you need one central place to ship and monitor business logic. [[raw/why-mcp-is-not-dead|cite]]
- CLIs have existed for decades without a good governance story for distributing them to end users. [[raw/why-mcp-is-not-dead|cite]]
- An MCP server keeps the data in your storage while distributing access to many clients and harnesses at once. [[raw/why-mcp-is-not-dead|cite]]
- The author's own split is the argument in miniature: MCP for hosted, business-specific memory logic; CLIs for local development against MongoDB, Prefect and Obsidian files. [[raw/why-mcp-is-not-dead|cite]]

## Notable quotes

> "MCP is NOT dead. You were just using it wrong."
> — [[raw/why-mcp-is-not-dead|location]]

## Connections

- **Entities**: [[wiki/entities/mcp]], [[wiki/entities/claude-code]], [[wiki/entities/prefect]], [[wiki/entities/mongodb]], [[wiki/entities/obsidian]]
- **Concepts**: [[wiki/concepts/governance]], [[wiki/concepts/cli-tools]], [[wiki/concepts/agent-skills]], [[wiki/concepts/connectivity-stack]], [[wiki/concepts/unified-memory]], [[wiki/concepts/agent-harness]]

> Synthesis: This note supplies the wiki's strongest "when NOT to use MCP" evidence while arguing the opposite case, which makes it the natural counterweight to the notes that reach for a CLI first.
