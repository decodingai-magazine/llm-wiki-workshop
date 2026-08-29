---
type: source
title: Choosing an Inference Architecture for Your Agents
description: "One question decides how you pay for inference — is a human waiting? — yielding three architectures: interactive, remote, and async offload."
origin: local
original_path: data_input_examples/notes/03-hard/Choosing an Inference Architecture for Your Agents.md
source_url: null
authors: []
published_date: null
raw_file: raw/choosing-an-inference-architecture-for-your-agents.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/inference-economics]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/agent-harness]]"
---

# Choosing an Inference Architecture for Your Agents

> [[raw/choosing-an-inference-architecture-for-your-agents|Raw]] · local

## Summary

The follow-up to the per-token-versus-GPU-hour comparison, answering *when* to use
which with a single test: **is a human waiting for the result?**

**Interactive** — a TUI or IDE where you are working with the agent. A 3–5 minute
cold start would destroy the experience, so pay per token and buy responsiveness:
no cold starts, almost no infrastructure. **Remote** — nobody is watching; the
agent picks up a ticket, spins up a sandbox, implements, tests, opens a PR, or
runs in CI. Here cold starts are an infrastructure detail rather than a UX
problem, so pay per GPU-hour, preferably serverless with scale-to-zero.
**Async offload** — the interesting hybrid: you work interactively, then ask for
something heavy (1,000 documents, deep research, a video). The foreground harness
keeps per-token inference while the background job goes to cheaper per-hour
compute, so latency and throughput are optimized separately.

The opening number — 1,000 documents for ~$14.30 instead of ~$97 — is the same
workload as the previous note, priced after choosing the architecture rather than
just the model.

## Key claims

- "Is a human waiting?" is the deciding question: if yes optimize latency, if no optimize throughput and cost. [[raw/choosing-an-inference-architecture-for-your-agents|cite]]
- Interactive agents justify per-token pricing purely on cold-start avoidance. [[raw/choosing-an-inference-architecture-for-your-agents#1/ Interactive: Pay per token|cite]]
- Remote agent workloads (ticket → sandbox → tests → PR) are the natural home for serverless GPUs. [[raw/choosing-an-inference-architecture-for-your-agents#2/ Remote: Pay per hour|cite]]
- The async pattern splits one session across two payment models — foreground per-token, background per-hour. [[raw/choosing-an-inference-architecture-for-your-agents#3/ Async: Offload to pay per hour|cite]]
- A 3–5 minute cold start is irrelevant when the job takes 30+ minutes. [[raw/choosing-an-inference-architecture-for-your-agents#3/ Async: Offload to pay per hour|cite]]
- The same agent supports proprietary, open-weights-as-a-service and self-served models behind one interface. [[raw/choosing-an-inference-architecture-for-your-agents|cite]]

## Connections

- **Entities**: [[wiki/entities/modal]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/inference-economics]], [[wiki/concepts/provider-abstraction]], [[wiki/concepts/agent-harness]]

> Synthesis: Together with its predecessor this forms the wiki's only complete decision procedure — a question, three architectures, and prices — and it is worth noticing that the deciding variable is a UX fact, not a technical one.
