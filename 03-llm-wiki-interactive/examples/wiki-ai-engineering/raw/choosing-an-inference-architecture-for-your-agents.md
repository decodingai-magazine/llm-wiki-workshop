# Choosing an Inference Architecture for Your Agents

**Source:** [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7496544165175001088/)
**Published:** 2026-08-21
**Engagement:** 19,077 impressions · 352 reactions · 42 comments · 41 reposts · 2.28% engagement rate

![[assets/inference-architectures-agents.jpg]]

---

I processed 1,000 documents through an LLM for ~$14.30 instead of ~$97.

The secret?

How I paid for inference.

In a previous post, I compared two ways of paying for LLM inference:

- Pay per token
- Pay per hour of GPU compute

But how do you know when to use one over another?

While building Decode for my Building a Coding Agent from Scratch series, I've found it mostly depends on whether a human is waiting.

There are 3 architectures I think about:

## 1/ Interactive: Pay per token

Think Claude Code, Codex, Cursor, or any TUI/IDE where you're working with the agent.

You send a prompt and expect something to happen immediately.

A 3-5 minute cold start would destroy the UX.

This is where pay-per-token services make sense:

- Anthropic
- OpenAI
- Gemini
- OpenRouter
- Kimi K3 through Modal Shared Endpoints

You get:

- No cold starts
- Almost no infrastructure
- Easy setup

You pay more at scale, but you're paying for responsiveness.

## 2/ Remote: Pay per hour

Imagine nobody is watching...

Your agent:

- Picks up a Linear ticket
- Spins up a sandbox
- Implements the feature
- Runs the tests
- Opens a PR

Or it's running in CI/CD.

Here, paying for GPU compute by time makes more sense.

You could rent an entire GPU VM and pay while it's running.

Or use serverless GPUs that spin up when needed and scale back to zero.

For these workloads, I prefer serverless.

I can spin up open models like Qwen, Gemma, GLM 5.2, or Kimi K3 through SGLang on Modal Endpoints.

You get:

- Lower costs at high throughput
- More privacy and control
- Open-model flexibility
- No GPU infrastructure to manage
- Scale-to-zero economics

When nobody is waiting, cold starts become an infrastructure detail rather than a UX problem.

## 3/ Async: Offload to pay per hour

You're working interactively with an agent, then ask it to:

- Process 1,000 documents
- Implement a large feature
- Run deep research
- Generate a video
- Execute another compute-heavy background task

You're coming back later so you don't need the result in 500ms.

The interactive harness can use pay-per-token inference, then launch the expensive background job on cheaper pay-per-hour GPU compute.

A 3-5 minute cold start is irrelevant if the job takes 30+ minutes.

Now you can optimize separately for:

Latency in the foreground.

Cost + throughput in the background.

With Modal, you can use Shared Endpoints for the interactive path, then serverless endpoints for remote and async workloads.

The key question is:

Is a human waiting for the result?

If yes, optimize for latency.
If no, optimize for throughput and cost.

The architecture should decide how you pay for inference.

I break down Decode's agent loop + inference layer here: https://lnkd.in/d-3NGttv

P.S. How do you decide between pay-per-token and pay-per-hour GPU inference for your agents?
