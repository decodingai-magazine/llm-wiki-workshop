---
type: concept
title: Progressive Tool Discovery
description: Deferring tool-schema loading until the model needs it — via a `tool_search`-style pattern — instead of stuffing every tool definition into context up front.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-harness]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/programmatic-tool-calling]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp-applications]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-disclosure]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/skills]]"
created: 2026-08-29T16:15:36Z
timestamp: 2026-08-29T17:10:07Z
source_count: 3
---

# Progressive Tool Discovery

> Load tool definitions on demand, via a `tool_search`-style pattern, instead of eagerly stuffing every tool's schema into context.

## Definition

Progressive tool discovery is a harness-level fix for a specific failure mode: when a large MCP server (or a set of them) exposes many tools, dumping every tool's schema into the context window up front bloats the prompt and degrades the model's ability to pick the right tool. Instead, the harness defers loading — it exposes a `tool_search`/"tool search" mechanism and only pulls a tool's full definition into context once the model actually needs it. The two DSP-talk sources describe the mechanism identically (deferred loading via a search pattern, fixing context bloat from too many tool definitions). A third, independent source adds a concrete number for the problem this technique solves — upfront tool schemas can cost 7-9% of the context window before any work begins — though that source's own fix for the number it cites is a different mechanism (skill-tier loading, see below), not an explicit `tool_search` call. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

> Synthesis: two of the three source pages here trace to the same talk — "The Future of MCP," given by an Anthropic engineer identified in one source as David Soria Parra ("wrote the Python SDK" in the other) — so those two remain one independent voice reported twice. The third source (a Substack lesson on building a coding agent, unrelated to that talk) is a genuinely separate voice, but it corroborates the *problem* (tool schemas are expensive to load eagerly) more than the specific `tool_search` *mechanism* — its own fix routes through skill progressive disclosure instead. Treat the mechanism claim as still single-voice; treat the cost-of-eager-loading claim as now two-voice.

## Key claims

- Progressive tool discovery is one of the harness's two "must-build" / "priority" upgrades (alongside programmatic tool calling), implemented via `tool_search` rather than eager schema-stuffing; the harness, not the MCP protocol itself, is what decides whether tool bytes get loaded this way. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/system-architecture-of-future-ai-apps-ui-tui-ide-extension]]
- The same pattern is framed as a prerequisite for 2026's shift to general knowledge-worker agents: deferring tool loading and only loading a tool when the model needs it, via a tool-search pattern, is presented as the fix for tool definitions bloating the context window. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/the-future-of-mcp-vs-skills]]
- A from-scratch coding-agent build quantifies the underlying problem: upfront tool schemas alone can cost 7-9% of the context window before any work begins — the same schema-bloat failure mode the `tool_search` pattern targets, though this source's own fix is to load skills (not raw tool schemas) through a three-tier progressive-disclosure scheme rather than a `tool_search` call. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]

## Relationships

- **Agent harness**: progressive tool discovery is described as living in the harness layer, not the protocol layer — same MCP servers, different harness, different tool-loading behavior. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/agent-harness]]
- **Programmatic tool calling**: the two techniques are named together in both DSP-talk sources as the paired technical fixes/upgrades that connectivity-heavy agents need in 2026. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/programmatic-tool-calling]]
- **MCP / MCP applications**: the problem this technique solves — too many tool schemas in context — grows directly with how many tools an MCP server or a fleet of MCP servers exposes. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/mcp-applications]]
- **Progressive disclosure**: a distinct, sibling technique, not a synonym — progressive disclosure (as used in the coding-agent build) tiers the loading of *skills*/capability files (catalog line → full `SKILL.md` → bundled files), while progressive tool discovery tiers the loading of *tool schemas* via a search mechanism. The two are named side by side in the same source as separate concepts solving related but not identical context-bloat problems. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/progressive-disclosure]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-context-engineering-for-coding-agents]]
- **Skills**: in the coding-agent build, skill-tier loading is presented as one concrete way a harness avoids the up-front tool/definition cost that progressive tool discovery also targets — an alternative or complementary lever, not proof of the same mechanism. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/concepts/skills]]

> Synthesis: this concept now has a quantified cost claim from a source outside the original talk, but its defining mechanism (`tool_search`) still rests on a single voice reported twice. The interesting open question the wiki should watch for: does anyone build `tool_search` and skill-tier progressive disclosure into the *same* harness, or do teams pick one lever and not the other?
