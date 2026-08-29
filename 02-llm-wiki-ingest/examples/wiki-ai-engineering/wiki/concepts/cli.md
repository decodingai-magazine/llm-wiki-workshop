---
type: concept
title: CLI
description: A connectivity layer that lets agents shell out to local command-line tools directly — well suited to sandboxed coding agents and personal development, but not to distributing governed business logic at scale.
aliases: []
sources:
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]"
  - "[[wiki/sources/why-mcp-is-not-dead]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/agent-architecture]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/agent-sandboxing]]"
  - "[[wiki/concepts/agent-loop]]"
created: 2026-08-29T16:14:41Z
timestamp: 2026-08-29T17:10:27Z
source_count: 5
---

# CLI

> One of three complementary connectivity mechanisms — alongside skills and MCP — by which an agent reaches capabilities; the three article sources treat it as a tool for a specific job, while the two course sources show it from the inside, as the very shape of a terminal coding agent.

## Definition

All three article sources place the CLI inside a stack of connectivity mechanisms rather than treating it as a standalone protocol, but they emphasize different edges of it. The talk transcript frames CLI as one of three layers agents will use "quite seamlessly together" in 2026 — skills, CLI, and MCP — with CLI's advantage being that sandboxed local coding agents can already lean on the model's training-data familiarity with command-line tools. [[wiki/sources/the-future-of-mcp-vs-skills]] The LinkedIn post nests the same idea in a four-layer architecture (Presentation, Harness+Runtime, Connectivity, MCP Servers), where CLI is one of three connectivity mechanisms — alongside skills and MCP clients — covering "local host capabilities." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]] The practitioner rebuttal draws a personal-vs-business-scale line instead: CLIs (plus `llms.txt` and skills) are fine for an individual's own setup, but installing a CLI on "thousands or millions" of customer machines is unworkable and ungovernable — which is why MCP servers persist for that job. [[wiki/sources/why-mcp-is-not-dead]]

Two sources from the same course-and-repo project sharpen this from the inside rather than arguing about it. The `decode` repo demonstrates rather than argues: it is itself a terminal coding agent shipped as a CLI (`decode`, `decode run`, `decode replay`), whose "local host capabilities" are literally a `LocalExecutor` running tool commands on the host, behind the same seam that swaps in Docker or Modal sandboxing. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] The Lesson 2 build-log article for the same course covers an earlier state of that same project — Decode as a bare-bones terminal coding agent deliberately scoped to reach feature parity with Mario Zechner's minimalist Pi harness, before later lessons add the memory, skills and sandboxing the ARCHITECTURE page documents. [[wiki/sources/article-the-coding-agent-loop]] Because both share the same author and the same underlying codebase, they are not two independent witnesses to "CLI suits sandboxed coding agents" — they are one voice narrating the same project twice, once in prose and once as a code architecture, and the wiki should not double-count that as corroboration.

## Key claims

- CLI is one of three complementary connectivity layers for agents (with skills and MCP); it suits sandboxed local coding agents, which can lean on the model's training-data familiarity with command-line tools. [[wiki/sources/the-future-of-mcp-vs-skills]]
- In a four-layer agent architecture, CLI sits in Connectivity alongside skills and MCP clients, covering local host capabilities; quoting David Soria Parra: "Connectivity is not one thing. The best agents use all of it - skills, CLI, MCP - together." [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]]
- CLIs work well for personal tooling and local development access — e.g. one practitioner's own use of CLIs for MongoDB and Prefect, and for Obsidian's local files via Claude Code's own CLI — but do not scale as a distribution mechanism for governed business logic. [[wiki/sources/why-mcp-is-not-dead]]
- All three article sources converge on the same pluralist conclusion: CLI, skills, and MCP are complementary tools for different jobs, not competing standards. [[wiki/sources/the-future-of-mcp-vs-skills]], [[wiki/sources/the-future-of-mcp-why-the-future-of-agents-is-mcp-skills]], [[wiki/sources/why-mcp-is-not-dead]]
- `decode` is a working instance of the "sandboxed local coding agent" case the talk transcript names: invoked as a CLI, with every gated tool call dispatched through an executor seam (`none`/`docker`/`modal`) rather than a remote server — connectivity and sandboxing collapse into one local-process boundary. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- The course's Lesson 2 build log frames Decode from day one as a terminal coding agent built to reach feature parity with Pi's minimalist CLI harness, before memory, skills and sandboxing arrive in later lessons — the same underlying project as the repo source above, so it reinforces rather than independently corroborates the "CLI suits sandboxed coding agents" case. [[wiki/sources/article-the-coding-agent-loop]]

## Relationships

- **MCP**: consistently paired as complementary rather than competing — CLI covers local/sandboxed capability, MCP covers rich semantics, governance and distribution at scale. [[wiki/concepts/mcp]]
- **Skills**: CLI is one of the (typically three-way) connectivity stack alongside skills in every source that discusses architecture. [[wiki/concepts/skills]]
- **Agent architecture**: CLI is one of the connectivity mechanisms inside the "Connectivity" layer of the four-layer architecture. [[wiki/concepts/agent-architecture]]
- **Agent harness**: in `decode`, the CLI *is* the harness's entry point — its Click commands build the same `Agent` the TUI and durable runtime use — a narrower sense than the connectivity-layer framing in the article sources. [[wiki/concepts/agent-harness]]
- **Agent sandboxing**: `decode`'s CLI-invoked tool calls run through the same seam that selects `none`/`docker`/`modal` execution, tying local-command execution to sandbox mode. [[wiki/concepts/agent-sandboxing]]
- **Agent loop**: `decode`'s CLI commands are the entry points that construct and drive the agent loop; the Lesson 2 article documents that same loop end-to-end for an earlier state of the same CLI tool. [[wiki/concepts/agent-loop]]

> Synthesis: the article sources describe CLI from the outside, as one node in a connectivity stack, at two altitudes — general architecture versus personal-vs-business-scale; the two course sources show it from the inside, as a coding agent that *is* a CLI — but since both trace to one author and one project, that is corroboration by demonstration and repetition, not by independent witnesses, and should be weighted as such.
