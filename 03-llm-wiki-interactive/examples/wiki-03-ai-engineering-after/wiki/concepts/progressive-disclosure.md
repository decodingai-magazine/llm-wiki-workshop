---
type: concept
title: Progressive Disclosure
description: A design pattern for revealing content or capability only when it is needed, rather than loading everything upfront — applied here at two different grains, within one agent's context and across harness environments.
aliases: []
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
related:
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/progressive-tool-discovery]]"
created: 2026-08-29T16:48:21Z
timestamp: 2026-08-29T17:10:09Z
source_count: 4
---

# Progressive Disclosure

> Multiple framings — see Definition

## Definition

Four sources apply this label, at two different grains, and only one of the four reaches for a different term for its own pattern.

Three sources converge on the grain of **one agent's context**, and all three trace to the same course and codebase. `decode`'s ARCHITECTURE.md describes the mechanism directly: skills load in three tiers — a catalog line (name + one line) always in the prompt, the full body only when `skill(name)` is called, and a project skill's bundled `references/`, `examples/`, `scripts/` surfacing as an on-demand trailer. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] Lesson 1 of the same course names skills as one of six harness modules — "workflows loaded only on invocation" — without yet showing the mechanism. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]] Lesson 4 restates the identical three tiers and adds the reason they exist: upfront tool schemas alone can cost 7–9% of the context window before any work begins. [[wiki/sources/article-context-engineering-for-coding-agents]]

The GraphRAG report describes a different shape — a 3-layer pattern for wiring an MCP server into any harness — at the grain of **capability across environments**, and its own vocabulary for it is "progressive enhancement," not "progressive disclosure": Layer 1 (the MCP server — tools, instructions, transport) is protocol-standard and works everywhere, while Layers 2 (skills) and 3 (hooks) are Claude-Code-specific enrichments that other harnesses (OpenCode, Cursor, Windsurf) simply don't get, falling back to tool docstrings alone. [[wiki/sources/agentic-graphrag-via-mcp-servers]]

> Synthesis: both are instances of "reveal more only where it can be used," but at different grains — the `decode` course discloses skill *content* over time within one agent's context budget, while the GraphRAG report discloses integration *richness* across harness environments. Treat the three `decode`-course sources as one well-documented witness rather than three independent confirmations (see Tensions); the GraphRAG report is the only independent voice and system in the set, and it names its own pattern "progressive enhancement," a term closer to web development's graceful degradation than to on-demand context loading.

## Key claims

- `decode`'s skills subsystem implements a three-tier reveal: always-loaded catalog line, on-call skill body, on-demand bundled files (`references/`, `examples/`, `scripts/`). [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The same three-tier skill loading is restated across the course's own marketing/teaching material: named as a harness module in lesson 1, then given a concrete cost justification in lesson 4 — upfront tool schemas alone can cost 7–9% of the context window before any work begins. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[wiki/sources/article-context-engineering-for-coding-agents]]
- The GraphRAG report's own three-layer MCP-to-harness pattern (server / skills / hooks) is explicitly framed as layers of decreasing portability, with only the MCP server layer guaranteed to work in a harness that lacks the other two. [[wiki/sources/agentic-graphrag-via-mcp-servers]]
- Quote: "Layer 1 is portable. Layers 2 and 3 are progressive enhancements that make the experience richer in harnesses that support them, while degrading gracefully in those that don't." [[wiki/sources/agentic-graphrag-via-mcp-servers]]

## Relationships

- **Skills**: the catalog-then-body-then-bundle tiering is the concrete mechanism behind the disclosure claim, corroborated identically by the repo and both Substack lessons. [[wiki/concepts/skills]]
- **MCP**: the GraphRAG report's layered server/skills/hooks structure is an MCP integration pattern; progressive disclosure/enhancement is what determines how much of it activates in a given harness. [[wiki/concepts/mcp]]
- **Agent harness**: all four sources tie the pattern to harness capability — what a harness can surface (skill bodies, hooks) bounds what gets progressively revealed. [[wiki/concepts/agent-harness]]
- **Progressive tool discovery**: a separate, already-existing concept page about deferring tool-schema loading in an agent runtime. `article-context-engineering-for-coding-agents` cites both concepts side by side without merging them, which supports keeping them distinct: this page is about skill/capability content, that one is scoped to tool schemas. [[wiki/concepts/progressive-tool-discovery]], [[wiki/sources/article-context-engineering-for-coding-agents]]

## Tensions

- The sources use the phrase for different mechanisms. The `decode` course means "reveal more *content* over time, within one context" (catalog → body → bundle). The GraphRAG report's own language — "progressive enhancement" — means "reveal more *capability* across environments" (docstrings-only → skills → hooks, depending on what the harness supports), a term with roots in web development's graceful-degradation idea rather than in on-demand context loading. Treat them as related but non-identical until a future source ties them together explicitly.
- False-corroboration risk: three of the four sources (the repo's ARCHITECTURE.md and both Substack articles) describe the same underlying artifact — the `decode` codebase and course — and the two articles are both authored by Paul Iusztin, who also writes the course the repo implements. Their agreement on "three tiers, catalog always loaded" is one well-sourced account of one system, not three independent replications. The GraphRAG report remains the only source in this set describing an unrelated system.
