---
type: source
title: The Future of MCP vs. Skills
description: A note-taker's transcript of a 2026 talk arguing that agent connectivity needs skills, CLI and MCP together as complementary layers rather than one universal protocol.
origin: local
original_path: "data_input_examples/notes/02-medium/The Future of MCP vs. Skills.md"
source_url: null
authors: []
published_date: null
raw_file: raw/the-future-of-mcp-vs-skills.md
created: 2026-08-29T16:09:44Z
timestamp: 2026-08-29T16:09:44Z
entities: []
concepts:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
  - "[[wiki/concepts/mcp-applications]]"
---

# The Future of MCP vs. Skills

> [[raw/the-future-of-mcp-vs-skills|Raw]] · local

## Summary

These are note-taker's bullets from a talk (apparently given by an Anthropic
engineer who "wrote the Python SDK" for MCP) surveying where the Model Context
Protocol stands 18 months in and where agent connectivity is headed in 2026. The
note's central move is to reject the idea of one winning connectivity standard:
it argues agents need a stack of at least three complementary layers — skills
(reusable capability files), CLI (great for sandboxed local coding agents that
can already lean on training data), and MCP (needed once you require rich
semantics, UI, platform independence, or enterprise auth/governance) — and
predicts 2026 agents will use all three "quite seamlessly together."

Two technical fixes get sustained attention as prerequisites for that future:
progressive tool discovery (deferring tool-loading with something like a
"tool search" pattern instead of stuffing every tool definition into context)
and programmatic tool calling / "code mode" (giving the model a code execution
environment so it composes tool calls itself, in a script, rather than round-
tripping through inference for every step — with MCP's structured-output
feature supplying the type information that makes this composable). The note
also carries a roadmap: a stateless transport protocol built with Google,
cross-app access for enterprise SSO, well-known-URL server discovery, v2 of the
TypeScript and Python SDKs, and "skills over MCP" so a server can ship updated
capability knowledge without a plugin/registration mechanism.

(The raw note is an unedited transcript and visibly mangles "MCP" as "MTP",
"NCP" and "FTP" in places — preserved verbatim in the quotes below rather than
silently corrected.)

## Key claims

- MCP reached 110M monthly downloads in 18 months and is now a dependency
  pulled in by OpenAI's Agents SDK, Google's ADK, LangChain, and "thousands"
  of other frameworks. [[raw/the-future-of-mcp-vs-skills#MCP Ecosystem Growth & Milestones|cite]]
- 2026 is framed as the pivot from 2025's coding agents (ideal because they're
  local, verifiable, and sandboxed) to general "knowledge worker" agents, whose
  defining requirement is connectivity to several SaaS apps and a shared drive
  rather than a compiler. [[raw/the-future-of-mcp-vs-skills#2026 Agent Development Paradigm Shift|cite]]
- Connectivity is a three-layer stack, not a single protocol: skills carry
  "main knowledge" in a simple, reusable file; CLI suits sandboxed local coding
  agents and benefits from training-data familiarity; MCP is for rich
  semantics, platform independence, and enterprise concerns like authorization
  and governance. [[raw/the-future-of-mcp-vs-skills#Skills Layer|cite]] [[raw/the-future-of-mcp-vs-skills#CLI Layer|cite]] [[raw/the-future-of-mcp-vs-skills#MCP Layer|cite]]
- Progressive tool discovery — deferring tool loading and only loading a tool
  when the model needs it, via a tool-search pattern — is presented as the fix
  for tool definitions bloating the context window. [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- Programmatic tool calling ("code mode") has the model write a script against
  an execution environment (a V8 isolate, Monty, or a Lua interpreter) to
  compose tool calls itself instead of the model orchestrating one tool call
  per inference turn; MCP's structured-output feature supplies the typing that
  makes this composition reliable. [[raw/the-future-of-mcp-vs-skills#Technical Implementation Improvements|cite]]
- The 2026 MCP roadmap includes a stateless transport protocol built with
  Google (shipping "in June"), cross-app access for enterprise single sign-on,
  well-known-URL server discovery, TypeScript/Python SDK v2s, and "skills over
  MCP" so a large server can ship updated capability knowledge without a
  plugin/registration mechanism. [[raw/the-future-of-mcp-vs-skills#Technical Roadmap & Core Infrastructure Improvements|cite]] [[raw/the-future-of-mcp-vs-skills#Enterprise Integration & Advanced Features|cite]]

## Notable quotes

> "And so this is all to say that I think in 2026 we're going to start
> building agents that use all of them. They don't use one thing, they use
> all of it. And they use it quite seamlessly together."
> — [[raw/the-future-of-mcp-vs-skills#MCP Layer|location]]

> "And that means we all need to stop taking rest APIs and put them one to
> one into an MTP server. Every time I see someone building another rest apart
> MTP server conversion tool, it's a bit cringe because I think it just
> results in horrible things."
> — [[raw/the-future-of-mcp-vs-skills#Server Design Philosophy Revolution|location]]

> "You're just going to shift skills over mcp because it's very obvious that
> if you have a large MCP server with tons and tons of tools, you just want to
> ship the main knowledge with and say, oh, this is how you're supposed to use
> this."
> — [[raw/the-future-of-mcp-vs-skills#Enterprise Integration & Advanced Features|location]]

## Connections

- **Concepts**: [[wiki/concepts/mcp]], [[wiki/concepts/skills]], [[wiki/concepts/cli]], [[wiki/concepts/progressive-tool-discovery]], [[wiki/concepts/programmatic-tool-calling]], [[wiki/concepts/mcp-applications]]

> Synthesis: The first source in this wiki — it supplies the core vocabulary
> (MCP, skills, CLI, progressive tool discovery, programmatic tool calling,
> MCP applications) that later sources will need to engage with before any of
> these earn their own page.
