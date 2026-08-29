---
type: concept
title: MCP primitives
description: The small fixed set the protocol defines — tools, resources, prompts, sampling, elicitation, tasks — and the invocation semantics that follow from it.
aliases: [Tools resources prompts]
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
related:
  - "[[wiki/concepts/agentic-invocation]]"
  - "[[wiki/concepts/skills-over-mcp]]"
  - "[[wiki/concepts/server-side-orchestration]]"
  - "[[wiki/entities/mcp]]"
created: 2026-08-29T09:00:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 4
---

# MCP primitives

> Tools (AI-controlled), resources (application-controlled), prompts (user-controlled), plus sampling, elicitation and experimental tasks. Everything else is convention.

## Definition

The protocol's primitives are distinguished less by what they carry than by **who
decides when they run**: the model decides for tools, the application reads
resources for context, and the user explicitly triggers prompts
[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]. That
control model is the reason a skill shipped as a resource cannot behave like a
tool, and it is what makes "which primitive do I use?" an architecture question
rather than a naming one.

## Key claims

- The full primitive set is tools, resources, prompts, sampling, elicitation and tasks (experimental) — there is no skills primitive and no `/skills/execute` method. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Control differs per primitive: tools are AI-controlled, resources application-controlled, prompts user-controlled. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- Prompts are usable as *predefined procedures* — named recipes telling the orchestrator which tools to combine for a task. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Structured output on tool results gives the model type information, which is what makes composing calls in code safe. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Under-used primitives are where MCP differentiates itself: tasks, elicitation and MCP Apps do things no alternative offers. [[wiki/sources/the-future-of-mcp-vs-skills]]
- The under-used half of the protocol is named again: tasks for long-running work, elicitation for missing input mid-flow, resources for file-like attachments instead of stuffing everything into tool output. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/agentic-invocation]]**: the practical consequence of the control model, as one harness implements it.
- **[[wiki/concepts/skills-over-mcp]]**: what happens when you try to add a primitive the spec does not have.

> Synthesis: Reading the primitives as a *control* taxonomy rather than a *capability* taxonomy resolves most of the confusion in these notes — including the entire prompts-versus-skills question.
