---
type: entity
title: Modal
description: A cloud compute platform Decode uses both as a gVisor-based remote sandbox backend for isolating agent tool execution and as a self-hosted LLM-serving provider — a dual role confirmed by both the course's articles and its own codebase.
aliases: []
sources:
  - "[[wiki/sources/article-run-coding-agents-safely]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/sandboxing]]"
  - "[[wiki/entities/docker]]"
  - "[[wiki/entities/decode]]"
created: 2026-08-31T18:45:00Z
timestamp: 2026-08-31T20:10:00Z
source_count: 3
---

# Modal

> A cloud platform Decode integrates twice over: as a gVisor-sandboxed remote execution backend, and separately as a self-hosted LLM-serving provider — both roles visible in the harness's own source code, not just its lesson write-ups.

## Definition

Modal shows up in two unrelated capacities inside Decode, the coding-agent harness described across two lesson articles and confirmed directly by the codebase's own architecture page. As a **sandbox backend**, Modal is the remote leg of Decode's execution seam — `ModalBackend`, selected via `SANDBOX_MODE=modal` — implementing the same `create`/`exec` pair (per the articles) or the same `SandboxBackend` Protocol via a remote `SandboxFilesystem` (per the repo) as the local `DockerBackend`/`none` options, so the agent loop never knows where a command actually runs; its isolation is gVisor, a user-space "sentry" kernel — one rung above plain containers and below microVMs on the article's four-rung spectrum. [[wiki/sources/article-run-coding-agents-safely]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]] As an **LLM provider**, Modal is one of three backends behind Decode's `_build_model()`/`build_model()` (alongside OpenRouter and Gemini, selected by `settings.llm_provider`) and is the default choice for "serve it yourself" self-hosting, distinct from Modal-as-sandbox. [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Key claims

- Modal sandboxes boot through a 5-event lifecycle (Created, Scheduled, Started, Ready, In use) in under half a second; Decode avoids cold starts by pre-provisioning a pool of application-agnostic sandboxes and attaching a repo volume to make them application-ready on demand. [[wiki/sources/article-run-coding-agents-safely]]
- Beyond isolation, Modal sandboxes provide two side benefits: on-demand GPU compute (e.g. `gpu="B200:8"`) for agentic fine-tuning or dataset processing, and horizontal scale — an unsandboxed local orchestrator can fan work out to N background agents each contained in its own Modal sandbox, the pattern cited for Ramp's full-context background coding agent. [[wiki/sources/article-run-coding-agents-safely]]
- Modal's own conclusion from its sandboxing case study, per the article, is that cheap isolation shifts the bottleneck from "can the agent write correct code" to "how many agents can you run in parallel." [[wiki/sources/article-run-coding-agents-safely]]
- In Decode's LLM-provider selection, Modal-hosted serving is the default, chosen after napkin math putting a 1,000-document batch job at ~$13 on Modal vs. ~$97 on (Anthropic-hosted) Sonnet. [[wiki/sources/article-the-coding-agent-loop]]
- Every `SandboxExecutor` backend, Modal included, is fresh-exec: each command runs as a new process, so `cd`/`export` never persist across calls — only the filesystem does — and the sandbox is created lazily on first use. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Modal is also Decode's own deploy target: `src/decode/runtime/` houses both the headless Kitaru durable flow and a separate Modal deploy app (`runtime/modal_app.py`), a subsystem the architecture page flags as real but out of scope for reading the harness itself — so Modal is simultaneously a dependency *inside* Decode (sandbox, LLM serving) and infrastructure Decode is deployed *onto*. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/entities/docker]]**: Modal is Decode's remote sandbox, mirrored by Docker as the local one — both sit behind the same execution seam, differing in isolation strength (gVisor vs. shared-kernel containers) and where the box runs. [[wiki/sources/article-run-coding-agents-safely]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/entities/decode]]**: Decode depends on Modal in three ways now on record — as a sandbox backend for tool execution, as the default backend in its provider-agnostic model builder, and as its own deploy target — making it the harness's most load-bearing external service across all three sources. [[wiki/sources/article-run-coding-agents-safely]], [[wiki/sources/article-the-coding-agent-loop]], [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- **[[wiki/concepts/sandboxing]]**: Modal occupies the gVisor rung of the isolation spectrum (fork/exec < containers < gVisor < microVMs) — stronger than a container jail, weaker than a microVM. [[wiki/sources/article-run-coding-agents-safely]]

> Synthesis: All three sources trace to the same project — Paul Iusztin's Decode course — so this is still one system's account of Modal, not corroboration from the wider ecosystem. What changed with this update is the *kind* of witness: the repo page reads the actual `sandbox/executor.py` and `agent/factory.py` code, not a narrative description of it, so the two roles the articles assert (sandbox backend, LLM provider) are now confirmed by implementation rather than by prose alone — plus a third role, Modal-as-deploy-target, that only the code surfaces.
