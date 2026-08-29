---
type: concept
title: Agent memory
description: The types of memory an agent keeps — operational state, semantic knowledge, episodes and preferences — and the rules for what gets written back.
aliases: [Episodic memory, Semantic memory]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/agent-reasoning-memory-why-it-matters-and-how-to-use-it]]"
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/designing-an-agents-memory-in-a-nutshell]]"
  - "[[wiki/sources/explaining-the-architecture]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/questions-and-remarks-from-people-while-posting]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/context-layer]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T11:50:00Z
source_count: 10
---

# Agent memory

> Not one store but several kinds of remembering: who the user is, what they prefer, what happened, and what is true in general.

## Definition

The sources converge on a taxonomy without ever agreeing to one. The architecture
walkthrough splits **episodic** memory (what the user did at a particular
moment — "celebrated New Year's Eve in the mountains") from **semantic** memory
(stable preferences and style), and makes both writable by procedures the
orchestrator runs [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].
The GraphRAG ontology encodes almost the same split as node types: `person`,
`task`, `episode`, `preference`
[[wiki/sources/agentic-graphrag-via-mcp-servers]]. The database evaluation adds a
third axis — operational memory (profiles, sessions, message history) — and
treats semantic memory as the vector-search layer
[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]].

## Key claims

- Preferences and episodes are detected from ordinary conversation and written back automatically; the user does not file them. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- The extraction ontology makes memory types explicit and enforceable: four LLM-extractable node types, four structural ones. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Operational memory (users, sessions, messages) has different access patterns from semantic memory and benefits from document-level locking under concurrency. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- A session-end hook that extracts people, tasks, episodes and preferences turns every conversation into memory growth. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Memory needs versioning as much as storage — tracking how the agent's understanding changed over time is a first-class requirement. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
- A third kind exists beyond facts and events: **reasoning memory** — plans, tool sequences and outcomes — giving procedural rather than informational continuity. [[wiki/sources/agent-reasoning-memory-why-it-matters-and-how-to-use-it]]
- The extraction ontology is a memory taxonomy in disguise: person, task, episode and preference are the semantic types an LLM is asked for. [[wiki/sources/how-to-structure-your-collections-as-immutable-logs-instead]]
- Procedural memory — how the user likes a thing done — is named as a distinct third type alongside episodic and semantic. [[wiki/sources/explaining-the-architecture]]
- Whatever is written automatically must also be correctable: memory needs decay and pruning policies, not just storage. [[wiki/sources/agent-reasoning-memory-why-it-matters-and-how-to-use-it]]
- Project memory splits by trust: a project-authored file is trusted and uncapped, a model-maintained one is capped because it grows without bound. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Memory files are assembled root-most to cwd-most with provenance headers, so the most specific context wins. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Wiping a session's window should run a memory write-back first, so what was learned survives the clear. [[wiki/sources/article-context-engineering-for-coding-agents]]

## Relationships

- **[[wiki/concepts/unified-memory]]**: the architectural decision to keep all of these in one place.
- **[[wiki/concepts/knowledge-graph]]**: the representation that makes the types queryable together.

> Synthesis: Every source treats writing to memory as automatic and reading from it as deliberate — which is the opposite of how most note-taking systems work, and probably the reason these agents accumulate anything at all.
