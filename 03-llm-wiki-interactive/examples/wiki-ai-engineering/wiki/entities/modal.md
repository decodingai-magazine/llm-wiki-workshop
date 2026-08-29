---
type: entity
title: Modal
description: The serverless GPU platform used as the "open weights you serve yourself" tier — scale-to-zero compute behind the same interface as the hosted APIs.
aliases: []
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/choosing-an-inference-architecture-for-your-agents]]"
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/how-you-pay-for-llm-inference]]"
related:
  - "[[wiki/concepts/inference-economics]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/embeddings]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 6
---

# Modal

> Where the pay-per-GPU-hour half of the inference argument actually runs.

## Definition

Modal fills one of three tiers in the build-versus-buy decision: proprietary
models by API, open weights as a service, and **open weights you serve yourself**
[[wiki/sources/how-you-pay-for-llm-inference]]. Its property that matters to the
argument is serverless scale-to-zero — spin up while the agent works, scale down
when it does not, which suits bursty, parallel, unpredictable workloads.

It is also the production tier for embeddings in the hosting-levels note: vLLM
served on Modal, with a vendor API as the fallback
[[wiki/sources/different-levels-of-hosting-your-embedding-models]].

## Key claims

- Serving an open model on rented GPU time turned a ~$97 per-token job into ~$13. [[wiki/sources/how-you-pay-for-llm-inference]]
- Shared endpoints cover the interactive path; serverless endpoints cover remote and async workloads — same platform, different economics. [[wiki/sources/choosing-an-inference-architecture-for-your-agents]]
- Scale-to-zero is what makes the GPU tier viable for workloads that are idle between tasks. [[wiki/sources/choosing-an-inference-architecture-for-your-agents]]
- In production, vLLM on Modal is the chosen combination for self-serving embedding models. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- It is the self-hosting tier in a shipped coding agent, sitting behind the same provider seam as a hosted API. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Serverless hosting is what makes running your own or fine-tuned open models practical inside a harness. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]

## Relationships

- **[[wiki/concepts/inference-economics]]**: Modal is the concrete instance of the pay-per-hour option.
- **[[wiki/concepts/provider-abstraction]]**: it sits behind the same interface as every other provider.

> Synthesis: Named in three sources by the same author and always in the same role — treat it as one worked configuration rather than as a comparison of serverless GPU vendors.
