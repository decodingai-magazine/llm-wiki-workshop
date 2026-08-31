---
type: concept
title: Agent Memory
description: Unified, agent-accessible memory built from ingested documents, knowledge-graph extraction, and embeddings, exposed to agents through MCP search/write tools.
aliases:
  - unified memory
  - knowledge graph memory
  - GraphRAG
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]"
related:
  - "[[wiki/concepts/orchestration]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]"
  - "[[wiki/entities/mcp]]"
created: 2026-08-29T15:32:43Z
timestamp: 2026-08-29T15:32:43Z
source_count: 2
---

# Agent Memory

> A concrete pipeline for giving an agent durable memory — and one of the clearest examples in this wiki of why that logic ends up behind an MCP server rather than a skill or a CLI.

## Definition

Agent memory here means a pipeline that ingests raw inputs, normalizes them into documents, extracts a knowledge graph (entities and relationships) plus embeddings over document summaries, and exposes the result to an agent through dedicated search and write tools — with prompts distinguishing episodic memory (what a user did, and when) from semantic memory (preferences and style). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

Its business-logic specificity and cloud-hosted infrastructure are given as a concrete reason to expose this kind of memory through MCP tools rather than through skills or a CLI: the logic is too bespoke for a simple file, and too security-sensitive for an ungoverned local script. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Key claims

- A memory pipeline normalizes ingested inputs into documents, then extracts knowledge-graph entities/relationships and computes embeddings over document summaries, alongside source metadata, before saving into memory. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Memory is exposed to the agent through knowledge-graph search and write tools, guided by prompts (e.g., "update episodic memory") that distinguish episodic memory from semantic memory. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- A GraphRAG-based unified memory with highly specific business logic, hosted on cloud infrastructure, is a concrete case where exposing that logic as MCP tools makes more sense than plain skills or a CLI. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/why-mcp-is-not-dead]]

## Relationships

- **[[wiki/concepts/orchestration]]**: memory tools and the prompts that guide them are exactly the kind of steps a custom orchestrator has to sequence. [[wiki/concepts/orchestration]]
- **[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]**: orchestrates the ingestion and memory-building pipelines behind this store. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/entities/prefect]]
- **[[wiki/entities/mcp]]**: the mechanism this wiki argues memory logic should be exposed through, once it's specific and sensitive enough. [[wiki/entities/mcp]]

> Synthesis: The wiki's only pattern with an actual implementation sketch behind it rather than an argued position — grounding both [[wiki/concepts/orchestration]] and the skills-vs-MCP debate in one real pipeline.
