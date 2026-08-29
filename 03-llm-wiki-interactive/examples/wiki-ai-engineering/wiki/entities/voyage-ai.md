---
type: entity
title: Voyage AI
description: The embedding provider chosen for its native database integration, with contextualized chunk embeddings and a multimodal model as the specific draws.
aliases: [voyage-3.5, voyage-nano]
sources:
  - "[[wiki/sources/different-levels-of-hosting-your-embedding-models]]"
  - "[[wiki/sources/high-level-graphrag-architecture-built-on-top-of-mcp-servers]]"
  - "[[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]"
related:
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/hybrid-search]]"
  - "[[wiki/entities/mongodb]]"
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
source_count: 3
---

# Voyage AI

> The embedding half of the memory layer, chosen less for benchmark scores than for sitting inside the database that stores the vectors.

## Definition

Voyage is used as the production embedding provider, reachable three ways: through
the database vendor's own embedding API, through Voyage's API directly, or — for
one small open-weights model — from Hugging Face for local development
[[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]. The stated
reason for choosing it is integration first, capabilities second
[[wiki/sources/different-levels-of-hosting-your-embedding-models]].

## Key claims

- Native integration with the database is the primary selection criterion. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- Contextualized chunk embeddings are presented as the practical answer to chunking's cost/latency/quality trade-off. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- A multimodal model that embeds text and images in one message stack preserves the conversation's topology. [[wiki/sources/different-levels-of-hosting-your-embedding-models]]
- Only one model (`voyage-nano`) has open weights; it is positioned for development and testing, not production. [[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]
- A 1024-dimension model is described as a good balance of retrieval quality against vector-index size. [[wiki/sources/retrieval-strategies]]
- Auto-embedding — the database calling the provider itself from a config — is the enterprise-scale path. [[wiki/sources/questions-around-embeddings-with-mongodb-voyage-ai]]

## Relationships

- **[[wiki/entities/mongodb]]**: the integration is the reason for the choice.
- **[[wiki/concepts/embeddings]]**: where the dev/prod hosting decisions live.

> Synthesis: Two of the three sources are vendor conversations, so weigh the capability claims accordingly — the durable, checkable part is the integration argument, not the model quality.
