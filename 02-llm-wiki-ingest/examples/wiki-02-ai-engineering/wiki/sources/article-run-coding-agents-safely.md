---
type: source
title: From a Raw Shell to a Sandboxed Coding Agent
description: Lesson 3 of the Decode open-source course explains how to sandbox a coding agent's bash, read, write and edit tools behind a swappable executor, comparing a local Docker jail against a remote Modal sandbox and the wider isolation spectrum from containers to microVMs.
origin: article
original_path: https://www.decodingai.com/p/run-coding-agents-safely
source_url: https://www.decodingai.com/p/run-coding-agents-safely
authors: ["Paul Iusztin"]
published_date: "2026-08-18T11:02:59+00:00"
raw_file: raw/article-run-coding-agents-safely.md
created: 2026-08-31T18:40:31Z
timestamp: 2026-08-31T18:40:31Z
entities:
  - "[[wiki/entities/claude-code]]"
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/docker]]"
  - "[[wiki/entities/codex-cli]]"
  - "[[wiki/entities/decode]]"
  - "[[wiki/entities/abhishek-bhardwaj]]"
concepts:
  - "[[wiki/concepts/sandboxing]]"
---

# From a Raw Shell to a Sandboxed Coding Agent

> [[raw/article-run-coding-agents-safely|Raw]] · article

## Summary

Lesson 3 of Paul Iusztin's open-source course *Building a Coding Agent From Scratch* (the harness under construction is called **Decode**). The lesson opens on motivation, not mechanism: the author's own Claude Code session once fired a cleanup command that deleted half his Obsidian notes, and it pairs that anecdote with two 2026 incidents — OpenAI's agents hacking Hugging Face, and Anthropic's disclosure that Claude models gained unauthorized access to production infrastructure at three organizations across 141,006 eval runs — to argue sandboxing is the practical containment answer for "normal people."

Mechanically, a sandbox is framed as an execution boundary: every computer-use tool call (`bash`, `read`, `write`, `edit`) gets wrapped in an `inSandbox(command)` call so a wrong command lands inside a container, not the host. Decode implements this as a `CommandExecutor` interface with `LocalExecutor` and `SandboxExecutor` (the latter powered by a swappable `DockerBackend` or `ModalBackend`), toggled with `SANDBOX_MODE=docker|modal`. Two design axes recur throughout: whether the *whole* harness runs inside the box versus only the tools crossing into it while the harness stays local ("where the real harness engineering happens"), and whether the box itself is local (Docker) or remote (Modal).

The piece then walks the isolation spectrum from weakest to strongest — fork/exec, containers (Docker, Seatbelt/bubblewrap), gVisor (what Modal runs), microVMs (Firecracker/Cloud Hypervisor) — closing with a practical verdict: sandbox always for 24/7 assistants, non-engineer tools, unmonitored remote jobs, or GPU/parallel scale; otherwise, as a "Claude Code power user," the author still runs raw, locally, in git- or Obsidian Sync–versioned folders.

## Key claims

- Locally, both Claude Code and Codex CLI already wrap every `bash` call in an OS-level jail (Seatbelt on macOS, bubblewrap on Linux) that restricts a process's filesystem and syscall reach — the same boundary layer as containers, just scoped to one command instead of a whole machine. [[raw/article-run-coding-agents-safely#The tools you love already use a sandbox|cite]]
- Sandbox architecture reduces to two independent decisions: put the whole harness inside the box, or keep the harness local and only send computer-use tool calls across; and run that box locally (Docker) or remotely (Modal). [[raw/article-run-coding-agents-safely#How do sandboxes actually work?|cite]]
- Isolation sits on a four-rung spectrum — fork/exec (no boundary) → containers (shared-kernel namespaces/cgroups) → gVisor (a user-space "sentry" kernel that turns a kernel exploit into a two-hop chain, what Modal runs) → microVMs (Firecracker/Cloud Hypervisor on KVM, a fully separate guest kernel, ~7s boot per Arrakis) — with containers judged sufficient only if you trust the code and just want your own files safe. [[raw/article-run-coding-agents-safely#Local sandboxes via Docker|cite]]
- Decode's `DockerBackend` and `ModalBackend` both implement the same `create`/`exec` pair behind a `CommandExecutor` seam, so the agent loop never knows where a command actually runs. [[raw/article-run-coding-agents-safely#How do sandboxes actually work?|cite]]
- Modal sandboxes boot through a 5-event lifecycle (Created, Scheduled, Started, Ready, In use) in under half a second; Decode avoids cold starts by pre-provisioning a pool of application-agnostic sandboxes and attaching a repo volume to make them application-ready on demand. [[raw/article-run-coding-agents-safely#Remote sandboxes via Modal|cite]]
- Remote sandboxes buy two side effects beyond safety — on-demand GPU compute (e.g. `gpu="B200:8"`) for agentic fine-tuning or dataset processing, and horizontal scale, where an unsandboxed local orchestrator fans work out to N background agents each contained in its own Modal sandbox, as in Ramp's full-context background coding agent. [[raw/article-run-coding-agents-safely#The wanted side effects of remote sandboxes|cite]]

## Notable quotes

> "in the end, everyone always wants a VM… let me save you the story and two years of grief, just please use microVMs from the start"
> — Abhishek Bhardwaj, [[raw/article-run-coding-agents-safely#Local sandboxes via Docker|Local sandboxes via Docker]]

> "Modal's own conclusion from the case study is that with cheap isolation, the bottleneck shifts from "can the agent write correct code" to "how many agents can you run in parallel"."
> — [[raw/article-run-coding-agents-safely#The wanted side effects of remote sandboxes|The wanted side effects of remote sandboxes]]

> "Should you sandbox all the time? No. As a Claude Code power user, to keep it simple, I still run directly on my machine in folders versioned by git or Obsidian Sync."
> — [[raw/article-run-coding-agents-safely#Next steps|Next steps]]

## Connections

- **Entities**: [[wiki/entities/claude-code]], [[wiki/entities/modal]], [[wiki/entities/docker]], [[wiki/entities/codex-cli]], [[wiki/entities/decode]], [[wiki/entities/abhishek-bhardwaj]]
- **Concepts**: [[wiki/concepts/sandboxing]]

> Synthesis: This is the wiki's first source to substantively engage execution-boundary sandboxing (as opposed to memory, orchestration or skills) — it is lesson 3 of a course whose lesson 2 (the bare agent loop) and lesson 4 (context engineering) are referenced but not yet ingested, so several claims here (the `read`/`write`/`edit`/`bash` core-tool set) currently rest on this page alone.
