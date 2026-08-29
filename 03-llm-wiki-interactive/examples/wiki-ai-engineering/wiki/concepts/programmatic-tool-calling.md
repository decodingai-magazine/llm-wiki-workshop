---
type: concept
title: Programmatic tool calling
description: Let the model write a script that composes tool calls in a sandbox instead of orchestrating them one inference step at a time.
aliases: [Code mode]
sources:
  - "[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
related:
  - "[[wiki/concepts/server-side-orchestration]]"
  - "[[wiki/concepts/progressive-disclosure]]"
  - "[[wiki/concepts/cli-tools]]"
created: 2026-08-29T09:20:00Z
timestamp: 2026-08-29T09:20:00Z
source_count: 2
---

# Programmatic tool calling

> Stop paying an inference step per tool call. Give the model a sandbox — a V8 isolate, a Lua interpreter, sandboxed Python — and let it write the composition.

## Definition

The problem is the sequential pattern: call a tool, read the result, call the
next, read that. Each hop costs latency, tokens and an opportunity for the model
to drift. Code mode replaces the loop with a script the model writes once and the
sandbox executes [[wiki/sources/the-future-of-mcp-vs-skills]].

The enabling detail is **structured output**: because MCP declares what a tool
returns, the script has type information and can compose calls, filter results
and drop fields without a round-trip through the model
[[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]. Where
structured output is missing, the fallback is asking a cheap model to extract the
expected type [[wiki/sources/the-future-of-mcp-vs-skills]].

## Key claims

- Model-driven orchestration means the model is the runtime — latency-sensitive, token-hungry, and slower than a script that does the same work. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Structured output gives the composing script type information, which is what makes safe composition possible. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Bash pipes are the fifty-year-old version of the same idea: `gh pr list | jq | xargs` is programmatic tool calling. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- It works on both sides of the wire — the harness can hold the sandbox, or the server can expose one code-execution tool instead of eighty endpoint tools. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- The most interesting composition is vertical: one script calling an MCP tool, piping into a CLI, writing to a resource on another server. [[wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]

## Relationships

- **[[wiki/concepts/server-side-orchestration]]**: the same question one level up — who composes, and where.
- **[[wiki/concepts/cli-tools]]**: the reason a shell-capable agent is already halfway to code mode.

> Synthesis: This is the wiki's most reliable performance lever, and its cost is rarely stated: a script that composes tool calls is code you did not review, running against systems you do care about.
