---
type: concept
title: Server-side orchestration
description: Putting multi-step workflow logic inside the server as a composite tool, so it runs in one round-trip with a guaranteed order the model cannot alter.
aliases: [Composite tools, Client-side orchestration]
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/mcp-server-design]]"
  - "[[wiki/concepts/mcp-primitives]]"
  - "[[wiki/concepts/programmatic-tool-calling]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:00:00Z
source_count: 2
---

# Server-side orchestration

> Who runs the workflow — the model, step by step, or your server, in one call? The answer decides latency, determinism, and where your planning logic lives.

## Definition

Because tool code always executes on the server, a **composite tool** can run a
whole pipeline in a single request: preprocess, configure, train, validate, with
state carried between steps and full control flow available
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]. The
alternative is client-side orchestration, where the model calls atomic tools in
sequence and reasons between them — flexible, but paying a round-trip and an
inference step per stage.

The second source refuses to settle the same question at the level above: should
the *custom orchestrator* be a tool on the server, or a client you build
yourself? Both work programmatically; the author calls it an architectural
decision that propagates through the entire application and leaves it open
[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]].

## Key claims

- Server-side composition gives one round-trip, guaranteed execution order, persistent state across steps and real control flow. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Client-side orchestration costs multiple round-trips and tokens, and the model may skip or reorder steps. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- A hybrid surface — atomic tools for flexibility plus a composite tool for the common path — is the recommended default. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- For deterministic pipelines, do not rely on the model to orchestrate. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- If you are content with a prebuilt orchestrator such as Claude Code, the placement question disappears; it only bites when you want your own planning logic. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]

## Relationships

- **[[wiki/concepts/programmatic-tool-calling]]**: the third option — let the model compose the steps in code instead of in the loop.
- **[[wiki/concepts/mcp-server-design]]**: the surface that results from the choice.

## Tensions

- One source treats server-side composition as settled best practice for deterministic work [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]; the other, writing about the same stack, considers the placement genuinely undecided [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]. The difference is scope: one is placing a *pipeline*, the other a *planner*.

> Synthesis: Determinism is the deciding variable — the more fixed the sequence, the more the logic belongs on the server; planning, being non-deterministic by nature, is exactly the part that resists the same move.
