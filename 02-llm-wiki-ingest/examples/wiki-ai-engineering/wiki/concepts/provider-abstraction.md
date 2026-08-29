---
type: concept
title: Provider abstraction
description: One interface per model role, concrete implementations per environment — so tests, dev and production differ by config rather than by code.
aliases: [BaseLLM, BaseEmbeddingModel]
sources:
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/choosing-an-inference-architecture-for-your-agents]]"
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/how-you-pay-for-llm-inference]]"
  - "[[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]"
related:
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/inference-economics]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:45:00Z
source_count: 7
---

# Provider abstraction

> A two-method interface in front of the model, and a config that picks the implementation. That is the whole pattern, and it is what makes every other cost decision reversible.

## Definition

A small abstract class per model role — generate, embed — with concrete
implementations selected from configuration: mocked for tests, a local library for
development, a served model or a vendor API in production
[[wiki/sources/different-levels-of-hosting-your-embedding-models]]. The same
argument arrives from the harness side: "your harness shouldn't care where
inference comes from. It should only know how to request the next completion"
[[wiki/sources/how-you-pay-for-llm-inference]].

## Key claims

- One interface plus per-environment implementations makes tests, dev and prod interchangeable without touching code. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- Mocked implementations are the point of the abstraction, not a side effect — they let integration tests run with no API calls. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- The interface can be tiny: two methods are enough to replace a framework's model layer. [[wiki/sources/building-graphrag-from-scratch-infrastructure-over]]
- Behind one interface, a single agent can offer proprietary, open-weights-as-a-service and self-served models. [[wiki/sources/choosing-an-inference-architecture-for-your-agents]]
- Unifying dev and prod on the same serving stack is the tempting mistake — it breaks on developer hardware. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- A shipped harness selects between a hosted API, an open-weights gateway and a self-served model through one factory call. [[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
- Multiple providers exist partly to prove the point: the harness is independent of the model. [[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]
- The same injection discipline applies to harness state: tools receive a deps object and never import the interface. [[wiki/sources/article-the-coding-agent-loop]]

## Relationships

- **[[wiki/concepts/inference-economics]]**: the abstraction is what lets you act on a cost decision later.
- **[[wiki/concepts/embeddings]]**: the role where the pattern is worked out in most detail.

> Synthesis: A small, unglamorous pattern that quietly underwrites the wiki's louder arguments — portability across harnesses, switching payment models, testing without a network — none of which survive a vendor SDK called directly from business logic.
