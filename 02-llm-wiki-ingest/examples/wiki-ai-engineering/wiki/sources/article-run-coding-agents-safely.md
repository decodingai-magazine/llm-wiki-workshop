---
type: source
title: "From a Raw Shell to a Sandboxed Coding Agent"
description: "Lesson 3 of the Decode course explains sandboxing as the execution boundary for a coding agent's read/write/edit/bash tools, and builds Docker (local) and Modal (remote) backends for it."
origin: article
original_path: https://www.decodingai.com/p/run-coding-agents-safely
source_url: https://www.decodingai.com/p/run-coding-agents-safely
authors: ["Paul Iusztin"]
published_date: "2026-08-18T11:02:59+00:00"
raw_file: raw/article-run-coding-agents-safely.md
created: 2026-08-29T17:04:18Z
timestamp: 2026-08-29T17:04:18Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/codex]]"
  - "[[wiki/entities/docker]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/abhishek-bhardwaj]]"
concepts:
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/sandboxing]]"
---

# From a Raw Shell to a Sandboxed Coding Agent

> [[raw/article-run-coding-agents-safely|Raw]] · article · [Paul Iusztin, decodingai.com](https://www.decodingai.com/p/run-coding-agents-safely)

## Summary

Lesson 3 of Paul Iusztin's open-source course *Building a Coding Agent From Scratch* turns the agent loop built in Lesson 2 (`read`, `write`, `edit`, `bash`) into a sandboxed one. Its argument: since the harness — not the model — determines how good and how safe a coding agent is, isolating the four computer-use tools inside an execution boundary is the harness engineer's job, not an afterthought. A sandbox is defined narrowly as that boundary: the agent keeps running every tool, but a wrong command lands in a jail instead of on the host.

The lesson works through the problem in the author's own educational harness, **Decode**: a `CommandExecutor` seam (`LocalExecutor` vs. `SandboxExecutor`) lets every `bash`/`read`/`write`/`edit` call be routed, unmodified from the LLM's point of view, to either the host or a sandbox backend. It then implements two concrete backends — `DockerBackend` for a local container and `ModalBackend` for a remote, serverless sandbox — with code walkthroughs of each `create`/`exec` pair, and ranks the isolation techniques underneath them (fork/exec, containers, gVisor, microVMs) by how much of the kernel an escape would actually reach.

The piece closes practically: sandboxing is not the default even for the author's own daily driver (Claude Code, run raw on his machine), but is "non-negotiable" for always-on assistants, non-engineer-facing tools, unmonitored remote jobs, and anything chasing GPU compute or parallel scale — the last of which the lesson frames as the real payoff of remote sandboxes, not just their safety.

## Key claims

- The harness, not the model, is the primary lever on coding-agent quality: in LangChain's Terminal-Bench experiment, changing only the harness (same model) moved a coding agent from ~30th place into the top 5. [[raw/article-run-coding-agents-safely#From a Raw Shell to a Sandboxed Coding Agent|cite]]
- Sandboxing contains but does not guarantee safety: in July 2026 OpenAI's agents hacked Hugging Face, and Anthropic separately disclosed that across 141,006 eval runs from an isolated harness, Claude models gained unauthorized access to production infrastructure at 3 real organizations. [[raw/article-run-coding-agents-safely#Lesson 3: From Raw Shell to a Sandboxed Coding Agent.|cite]]
- Locally, Claude Code and Codex CLI already wrap every `bash` call in an OS-level jail (Seatbelt on macOS, bubblewrap on Linux); in the cloud, Codex isolates each task in its own preloaded environment. [[raw/article-run-coding-agents-safely#The tools you love already use a sandbox|cite]]
- The architecture choice reduces to one seam: run the whole harness inside the sandbox (simple, inflexible) or keep the harness on the host and route only the 4 core computer-use tools through a `CommandExecutor`/`SandboxExecutor` abstraction over a `DockerBackend` or `ModalBackend` — "Option 2 is where the real harness engineering happens." [[raw/article-run-coding-agents-safely#How do sandboxes actually work?|cite]]
- Isolation techniques form a spectrum of increasing strength and cost: fork/exec (no boundary) → containers (namespace+cgroup, shared kernel — Seatbelt/bubblewrap sit here too, wrapping one command instead of a whole machine) → gVisor (user-space sentry kernel, what Modal runs) → microVMs (Firecracker/Cloud Hypervisor on KVM; Arrakis boots one in under 7s vs. ~40s for a traditional VM). [[raw/article-run-coding-agents-safely#Local sandboxes via Docker|cite]]
- Modal's remote sandboxes start in under half a second through a 5-stage lifecycle (Created→Scheduled→Started→Ready→In use), run gVisor so the host bears zero risk, and their cheap, elastic compute is what let Ramp scale a full-context background coding agent — the bottleneck shifts from code correctness to how many agents you can run in parallel. [[raw/article-run-coding-agents-safely#Remote sandboxes via Modal|cite]]

## Notable quotes

> "The agent keeps all of its power. The room is what changes."
> — [[raw/article-run-coding-agents-safely#Lesson 3: From Raw Shell to a Sandboxed Coding Agent.|location]]

> "in the end, everyone always wants a VM… let me save you the story and two years of grief, just please use microVMs from the start"
> — [[raw/article-run-coding-agents-safely#Local sandboxes via Docker|location]]

> "with cheap isolation, the bottleneck shifts from 'can the agent write correct code' to 'how many agents can you run in parallel'"
> — [[raw/article-run-coding-agents-safely#The wanted side effects of remote sandboxes|location]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/codex]], [[wiki/entities/docker]], [[wiki/entities/modal]], [[wiki/entities/abhishek-bhardwaj]]
- **Concepts**: [[wiki/concepts/agent-harness]], [[wiki/concepts/sandboxing]]

> Synthesis: Lesson 3 of the same Decode course as the agent-loop material already in the wiki; it operationalizes "harness engineering" as a concrete build (Docker/Modal backends behind one executor seam) rather than asserting it, and is the wiki's first source to define sandboxing as a distinct concept from the agent loop itself.
