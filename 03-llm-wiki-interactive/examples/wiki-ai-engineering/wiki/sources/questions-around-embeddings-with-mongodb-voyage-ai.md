---
type: source
title: Questions Around Embeddings with MongoDB & Voyage AI
description: A Q&A with the vendor on where embeddings should be computed — Hugging Face locally, the Voyage or Atlas API in production, auto-embedding for enterprise.
origin: local
original_path: data_input_examples/notes/03-hard/Questions Around Embeddings with MongoDB & Voyage AI.md
source_url: null
authors: []
published_date: null
raw_file: raw/questions-around-embeddings-with-mongodb-voyage-ai.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/mongodb]]"
  - "[[wiki/entities/voyage-ai]]"
concepts:
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/provider-abstraction]]"
---

# Questions Around Embeddings with MongoDB & Voyage AI

> [[raw/questions-around-embeddings-with-mongodb-voyage-ai|Raw]] · local

## Summary

A three-round Q&A with the vendor, kept verbatim, about where embeddings should
actually be computed for a book's example code: in your own code via Hugging Face,
through an API, or inside the database.

The answers are specific. `voyage-nano` is the only open-weights model on Hugging
Face and is recommended for local development and testing; production should use
the larger models through the Atlas Embedding and Reranking API or the Voyage API,
and Hugging Face models are best consumed through Sentence Transformers.
**Auto-embedding** — the database adding embeddings to a collection by itself — is
in public preview in the community edition and coming to Atlas, and is described
as something enterprise customers keep asking for.

The second round is the practical one: for a community-oriented book running
MongoDB in Docker, the vendor's recommendation is the API for ease, mentioning
auto-embedding only for enterprise, because while it works across operating
systems it "needs a fair bit of configuration" during preview. Third round, one
line: 200 million free tokens on the Voyage API.

## Key claims

- Only one Voyage model (`voyage-nano`) has open weights on Hugging Face; it is positioned for dev and testing, not production. [[raw/questions-around-embeddings-with-mongodb-voyage-ai|cite]]
- Sentence Transformers is the vendor's recommended way to run the Hugging Face models. [[raw/questions-around-embeddings-with-mongodb-voyage-ai|cite]]
- Auto-embedding delegates embedding computation to the database entirely, configured rather than coded. [[raw/questions-around-embeddings-with-mongodb-voyage-ai|cite]]
- For a portable community setup the recommendation is the API, with auto-embedding mentioned only as an enterprise path. [[raw/questions-around-embeddings-with-mongodb-voyage-ai|cite]]
- The Voyage API includes 200 million free tokens. [[raw/questions-around-embeddings-with-mongodb-voyage-ai|cite]]

## Connections

- **Entities**: [[wiki/entities/mongodb]], [[wiki/entities/voyage-ai]]
- **Concepts**: [[wiki/concepts/embeddings]], [[wiki/concepts/provider-abstraction]]

> Synthesis: Vendor answers, and worth reading as such — but the dev/prod split they recommend is the same one the hosting-levels note reaches independently, which makes it the more credible of the two claims here.
