---
type: source
title: Owning Your Context Layer
description: A post arguing that models and harnesses are commoditized, so the only remaining moat is a memory you own and can carry between harnesses through an MCP server.
origin: local
original_path: data_input_examples/notes/02-medium/Owning Your Context Layer.md
source_url: null
authors: []
published_date: null
raw_file: raw/owning-your-context-layer.md
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/fastmcp]]"
  - "[[wiki/entities/prefect]]"
concepts:
  - "[[wiki/concepts/context-layer]]"
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/mcp-server-design]]"
---

# Owning Your Context Layer

> [[raw/owning-your-context-layer|Raw]] · local

## Summary

A post draft with the full spoken notes attached, and the wiki's clearest
statement of *why* any of this architecture matters. The argument proceeds by
elimination: people look for freedom first in open-source models, then in
open-source harnesses, and both are the wrong layer — "neither the model nor the
harness is the thing you care about. They're just tools." What you care about is
your research, notes, conversations, tasks, preferences and domain knowledge.

From there the test is operational: if you switch from Claude Code to Codex to
Gemini CLI, ideally nothing changes, and within five minutes the new system knows
who you are and what you are working on — because the memory moved with you. That
is the definition of independence the post offers, and it inverts the usual
lock-in conversation: being deeply invested in one open-source harness is *more*
expensive to leave than using a proprietary one with a portable memory.

The implementation follows the same two-part shape as the rest of the wiki: a
unified memory built with the simplest tools that work (filesystem, BM25,
semantic search, knowledge graphs, added in that order as the use case demands),
and an MCP server as the interface that wraps the business logic for querying and
updating it, exposing tools, resources, prompts, skills and an MCP App to
visualize the memory. The note also reports how cheap deployment has become —
connect a GitHub repo, name the entry point and the uv environment, and get
serverless deployment with authentication and continuous updates.

The closing framing is deliberately strong: whoever owns the context layer owns
your digital identity.

## Key claims

- Models and harnesses are commoditized; the context layer is the remaining moat. [[raw/owning-your-context-layer#Post|cite]]
- Freedom is not open weights or an open harness — those are infrastructure, not the thing you care about. [[raw/owning-your-context-layer#Full notes|cite]]
- The portability test: switch harness and within five minutes the new system knows who you are, because your memory came with you. [[raw/owning-your-context-layer#Post|cite]]
- Build the memory with the simplest tool that works — filesystem, BM25, semantic search, knowledge graph — and add complexity only when the use case demands it. [[raw/owning-your-context-layer#Post|cite]]
- Skills and CLIs are useful but out of scope for a context layer: an MCP server sits on top of tools and carries the resources, prompts and domain knowledge for driving the memory. [[raw/owning-your-context-layer#Full notes|cite]]
- Ownership buys two things: portability across platforms, and data privacy — the memory does not sit on a model provider's servers. [[raw/owning-your-context-layer#Full notes|cite]]

## Notable quotes

> "Models are becoming commoditized. Harnesses are becoming commoditized. The only moat that remains is your context layer."
> — [[raw/owning-your-context-layer#Post|location]]

> "Whoever owns this context layer owns your digital identity."
> — [[raw/owning-your-context-layer#Full notes|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/fastmcp]], [[wiki/entities/prefect]]
- **Concepts**: [[wiki/concepts/context-layer]], [[wiki/concepts/unified-memory]], [[wiki/concepts/agent-harness]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/mcp-server-design]]

> Synthesis: This note supplies the motive the technical sources leave implicit — every "expose it over MCP" decision elsewhere in the wiki is downstream of wanting the memory to outlive the harness.
