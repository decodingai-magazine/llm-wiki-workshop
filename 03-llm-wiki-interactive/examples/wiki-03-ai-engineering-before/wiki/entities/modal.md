---
type: entity
title: Modal
description: A serverless cloud platform that the Decode teaching codebase uses in two distinct roles — a GPU/inference backend for self-hosted LLMs, and a remote sandbox backend for isolated tool execution.
aliases: []
sources:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]]"
related:
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/entities/kitaru]]"
  - "[[wiki/entities/docker]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/sandboxing]]"
  - "[[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]"
created: 2026-08-29T17:08:21Z
timestamp: 2026-08-29T17:08:21Z
source_count: 4
---

# Modal

> A serverless cloud platform playing two separable roles in the Decode course: LLM-inference host and remote sandbox backend.

## Definition

All four sources describe Modal as a serverless cloud platform, but each engages one or both of two independent roles inside the `decode` codebase. As an **inference host**, Modal is the default of three swappable LLM providers (with Gemini and OpenRouter), chosen because it "bills GPU-time instead of tokens and scales to zero" — the "serve open weights yourself" tier of a build-vs-buy spectrum. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]] As a **sandbox backend**, Modal is one of two `CommandExecutor` implementations (with Docker) behind the harness's sandbox seam, giving the agent's `read`/`write`/`edit`/`bash` tools a remote, serverless jail. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]] The repo page confirms both roles at the code level and adds that Modal is infrastructure the codebase imports directly rather than hiding behind an interface. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] No source conflates the two — `_build_model()` and `select_executor()` are separate seams that happen to point at the same vendor.

## Key claims

- As inference host: Modal, OpenRouter and Gemini are the three swappable LLM providers; Modal-hosted inference goes through `OpenAIChatModel` over a bespoke `AsyncOpenAI` client with dual `Modal-Key`/`Modal-Secret` proxy headers. Because it is `vLLM` behind a Modal endpoint, it is one of the strict OpenAI-compatible servers that reject more than one `system` message — why the harness joins all instructions into a single string. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-the-coding-agent-loop]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- As sandbox backend: "Modal Sandboxes" are the remote half of the sandbox module (Docker is local); Modal runs gVisor under its sandboxes so the host bears zero risk from an escape, and starts a sandbox in under half a second through a 5-stage lifecycle (Created→Scheduled→Started→Ready→In use). [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]
- This cheap, elastic compute is credited with letting Ramp scale a full-context background coding agent — the claim being that cheap isolation shifts the bottleneck from code correctness to how many agents can run in parallel. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-run-coding-agents-safely]]
- At the code level, `ModalBackend` is imported only inside the `modal`-mode branch of `select_executor()`, so a `none`-mode process never loads Modal's SDK; in remote mode, Kitaru orchestrates N headless harnesses in parallel on Modal, and `runtime/` pins a "Modal orchestrator app" for this. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]], [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **Kitaru**: Kitaru is the durable-runtime layer that orchestrates many parallel headless harnesses; Modal is the compute substrate it runs them on. [[03-llm-wiki-interactive/examples/wiki-ai-engineering/wiki/entities/kitaru]]
- **Docker**: Modal's counterpart in the sandbox seam — Docker is the local backend, Modal the remote one, behind the same `CommandExecutor` interface. [[wiki/entities/docker]]
- **Sandboxing**: Modal is the concrete remote backend behind the concept, and the source that most directly motivates "remote sandbox" as distinct from "local sandbox." [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/sandboxing]]
- **Agent harness**: Both of Modal's roles illustrate the course's thesis that the harness, not the model, is what gets engineered — Modal sits behind both the provider seam and the sandbox seam. [[03-llm-wiki-interactive/examples/wiki-ai-engineering-after/wiki/concepts/agent-harness]]

> Synthesis: All four source-like pages trace to one project — the `decode` teaching codebase and the course narrating it, written by the same author — so this reads as one designer's consistent choice, not independent corroboration that Modal suits either role; the repo page is the only one that verifies the claims at the code level rather than by assertion.
