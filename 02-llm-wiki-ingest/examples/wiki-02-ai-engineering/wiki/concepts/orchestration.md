---
type: concept
title: Orchestration
description: The question of where the logic that sequences multiple tool calls into one coherent agent workflow should live — inside an MCP server as a deterministic composite tool, or on the client side — plus the techniques used to keep that sequencing efficient at scale.
aliases: []
sources:
  - "[[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]"
  - "[[wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/skills]]"
  - "[[wiki/concepts/cli]]"
  - "[[wiki/concepts/agent-connectivity]]"
  - "[[wiki/concepts/agent-memory]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:05:00Z
source_count: 6
---

# Orchestration

> Multiple framings — see Definition

## Definition

Across the wiki's six sources, "orchestration" covers three related but distinct problems: **where** the logic that sequences multiple tool calls into one coherent unit of agent work should live, **how** to keep that sequencing efficient once a client is driving many tools at once, and — in a different scope entirely — **what runtime** keeps one agent's own execution alive across machines.

On placement, the sources disagree in confidence rather than in substance. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] frames it as a clean binary for deterministic pipelines: **server-side orchestration** — a single composite MCP tool that calls helper functions internally, in one round trip, with a guaranteed step order — versus **prompt-guided client-side orchestration**, which costs multiple round trips and risks the model skipping or reordering steps; it recommends server-side without hedging. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] poses the same placement question for a *custom, non-deterministic planning* orchestrator sitting on top of a memory-backed MCP server (two tools — knowledge-graph search/write — plus prompts): should the orchestrator be packaged inside the MCP server as one exposed tool, or built on the client side (a FastAPI backend or a custom FastMCP client)? Its author reports having implemented both and being unable to judge which is architecturally better, since the choice "propagates through the entire application."

On mechanics, [[wiki/sources/the-future-of-mcp-vs-skills]] treats orchestration as one leg of a broader "connectivity stack" (skills + CLI + MCP as complementary layers, not competing options) and recommends two techniques to keep tool-heavy orchestration usable at scale: progressive tool discovery (keep tool definitions out of context, load on demand) and programmatic "code mode" tool calling (the model writes code against an execution sandbox to compose multiple tool calls instead of one inference round trip per call).

A third, distinct sense of the word shows up in [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], its companion [[wiki/sources/article-the-coding-agent-loop]], and the codebase those lessons build, [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] (all three trace to one author's single coding-agent course and its one codebase, Decode — three views of one project, not three independent voices). There, "orchestration" splits into two things below the placement question above. At the *runtime* level it is Kitaru splitting control, execution and sandbox into three planes to keep one agent's own execution alive across machines. At the *turn* level it is the mechanism the articles describe as the ReAct loop itself (`AgentTurnHandler`, an uncapped async generator) doing the turn-by-turn tool-call sequencing — which the repo shows concretely as a `Runner` single-flight phase machine driving that handler through one or more **legs**, gating each tool call through a `PermissionGate` before resuming.

## Key claims

- Server-side orchestration (a composite MCP tool executing internally) gives one round trip and a guaranteed step order; prompt-guided client-side orchestration needs multiple round trips and risks the model skipping or reordering steps — recommended for deterministic pipelines specifically. [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]]
- A concrete memory-backed agent exposes just two MCP tools (knowledge-graph search, knowledge-graph write) plus prompts that tell an orchestrator how to combine them for a named procedure, and is then driven by either a custom FastMCP-based client or a prebuilt orchestrator such as Claude Code. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Progressive tool discovery (deferring tool definitions instead of loading all of them into context) and programmatic "code mode" tool calling (composing multiple tool calls via sandboxed code instead of one round trip per call) are recommended techniques for keeping large, orchestrated toolsets efficient. [[wiki/sources/the-future-of-mcp-vs-skills]]
- 2026-era agents are expected to combine skills, CLI, and MCP rather than orchestrate through a single mechanism, because each layer covers a different need — packaged capability knowledge, sandboxed local execution, or rich cross-platform semantics and governance. [[wiki/sources/the-future-of-mcp-vs-skills]]
- Remote agent execution is itself described as "orchestrated" — by Kitaru (ZenML's agent runtime), across a control plane, an execution plane and a sandbox plane — giving a headless coding-agent harness durability (resume after a sandbox dies) and replay (rerun a finished trace with one variable changed). [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- Inside a single agent turn, sequencing is done by an uncapped `AgentTurnHandler` async generator with two yield points (before the next model call, before stopping); there is no max-step cap because the model signals completion by returning text instead of a tool call. [[wiki/sources/article-the-coding-agent-loop]]
- Concretely, that turn-level sequencing is a `Runner` single-flight phase machine (`idle → dispatching → running → idle`) driving `AgentTurnHandler` through one or more legs: a `MODEL_REQUEST` boundary drains queued steering text before each model call, a `WOULD_STOP` boundary drains queued follow-up text before each stop, and a gated tool call pauses a leg as `DeferredToolRequests` until the `PermissionGate` resolves it. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Multi-agent orchestration also happens within one turn: the model-callable `agent` tool fans out up to 6 read-only Explore subagents concurrently, each a fresh `agent.run()` re-entering the same installed Agent with narrowed deps so recursion is structurally impossible; each child's report is truncated to a shared byte budget and a harness-owned `SYNTHESIS_FOOTER` instructs the parent model to compile — not just relay — the N reports. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Tensions

Where should orchestration logic live — server side or client side? [[wiki/sources/how-to-integrate-skills-into-mcp-servers-mcp-prompts-vs]] answers this decisively for one specific case (a deterministic pipeline): put it server-side, as a composite tool. [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]] poses the same client-vs-server placement question for a general custom orchestrator and refuses to settle it, having built both versions without being able to say which is architecturally better. The two are not a flat contradiction — they scope differently (a deterministic step sequence vs. general non-deterministic planning) — but the second source is explicit that this is exactly the kind of choice the first source treats as already closed.

## Relationships

- **MCP**: both framings of orchestration are placement decisions within MCP's own Tools/Resources/Prompts primitives — orchestration logic is expressed as either a composite tool or client-side use of tools and prompts. [[wiki/concepts/mcp]]
- **Skills / CLI / Agent connectivity**: orchestration is presented as one of three complementary connectivity layers an agent draws on, alongside skills (packaged capability knowledge) and CLI (sandboxed local execution) — not a replacement for either. [[wiki/concepts/skills]], [[wiki/concepts/cli]], [[wiki/concepts/agent-connectivity]]
- **Agent memory**: the concrete example that motivates the unresolved placement question is a memory pipeline (knowledge-graph search/write) exposed through an MCP server. [[wiki/concepts/agent-memory]]
- **Agent harness**: both the runtime sense of orchestration (Kitaru's control/execution/sandbox split) and the in-process sense (the `Runner`/`AgentTurnHandler` turn-boundary machine, subagent fan-out) are behaviors of "the harness" — the layer the coding-agent course argues is what actually separates a good agent from a mediocre one, independent of the model. [[wiki/concepts/agent-harness]]

> Synthesis: The wiki holds three uses of one word that must not be flattened together: a confident recommendation for one specific case (server-side for deterministic pipelines), an explicit admission that the general client-vs-server placement question is unsettled, and — from an unrelated course by the same author, now corroborated down to the codebase itself — "orchestration" meaning both the infrastructure that keeps one agent's remote execution alive and the turn-boundary machinery (legs, permission gating, subagent fan-out) that sequences a single agent's own work. Read the first as a special case of the second, and the third as a different scope entirely, not a third position in the same debate.
