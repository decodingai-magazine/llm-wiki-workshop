---
type: concept
title: Inference economics
description: Per-token versus GPU-hour, serverless versus reserved, and the one question that decides between them — is a human waiting?
aliases: [Pay per token, Serverless GPU, LLM cost]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/choosing-an-inference-architecture-for-your-agents]]"
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/how-you-pay-for-llm-inference]]"
  - "[[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]"
  - "[[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]]"
related:
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/agent-harness]]"
  - "[[wiki/concepts/durable-execution]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 7
---

# Inference economics

> The payment model is an architectural decision, not a billing detail — and it moves cost by multiples.

## Definition

Two decisions. **Per-token or per-GPU-hour**: hosted APIs bill per token, which
suits interactive work; agent workloads that read repositories or process
thousands of documents can be dramatically cheaper on rented compute — ~$97
versus ~$13 for the same 1,000-document job in the worked example
[[wiki/sources/how-you-pay-for-llm-inference]]. **Serverless or reserved**:
reserved is cheaper per hour but you reserve for peak; serverless follows demand
to zero.

The selection rule is behavioural: **is a human waiting?** If yes, optimize
latency and pay per token. If no, optimize throughput and pay per hour. The hybrid
— interactive foreground, offloaded background — gets both
[[wiki/sources/choosing-an-inference-architecture-for-your-agents]].

## Key claims

- The same workload differs ~7x in cost depending only on how inference is paid for. [[wiki/sources/how-you-pay-for-llm-inference]]
- Idle time is the hidden cost of agent workloads that wait on humans — ten idle GPU-hours is real money. [[wiki/sources/how-you-pay-for-llm-inference]]
- A 3–5 minute cold start is fatal interactively and irrelevant for a 30-minute background job. [[wiki/sources/choosing-an-inference-architecture-for-your-agents]]
- Waste, not unit price, is the number that matters at scale: retries without caching re-pay for completed steps. [[wiki/sources/why-durable-workflow-tools-are-more-important-than-ai]], [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Per-stage cost differences justify routing stages to different infrastructure — CPU pools for I/O, GPU pools for inference. [[wiki/sources/scaling-graphrag-ingestion-pipelines-with-prefect]]
- Dev and prod can use different hosting entirely, as long as one interface hides the difference. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- The three tiers appear as three configured providers in one agent — hosted free tier, gateway, self-hosted serverless GPU. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]

## Relationships

- **[[wiki/concepts/provider-abstraction]]**: what makes switching payment models a config change.
- **[[wiki/concepts/durable-execution]]**: caching turns failure into a rounding error instead of a re-run.

> Synthesis: Every cost argument in this wiki ends up being about *repeated* work rather than unit price — which is why durability shows up in a section about inference billing.
