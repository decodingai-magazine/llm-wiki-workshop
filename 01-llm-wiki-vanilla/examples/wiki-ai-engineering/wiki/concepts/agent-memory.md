---
type: concept
title: Agent memory
description: The types of memory an agent keeps — operational state, semantic knowledge, episodes and preferences — and the rules for what gets written back.
aliases: [Episodic memory, Semantic memory]
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/unified-memory]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/context-layer]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 3
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

## Relationships

- **[[wiki/concepts/unified-memory]]**: the architectural decision to keep all of these in one place.
- **[[wiki/concepts/knowledge-graph]]**: the representation that makes the types queryable together.

> Synthesis: Every source treats writing to memory as automatic and reading from it as deliberate — which is the opposite of how most note-taking systems work, and probably the reason these agents accumulate anything at all.
