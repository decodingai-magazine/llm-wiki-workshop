---
type: source
title: Different Levels of Hosting Your Embedding Models
description: A four-tier guide to running embedding models — mocked in tests, Sentence Transformers in dev, vLLM on serverless GPUs in prod — held together by one interface.
origin: local
original_path: data_input_examples/notes/03-hard/Different Levels of Hosting Your Embedding Models.md
source_url: null
authors: []
published_date: null
raw_file: raw/different-levels-of-hosting-your-embedding-models.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/modal]]"
  - "[[wiki/entities/voyage-ai]]"
  - "[[wiki/entities/mongodb]]"
concepts:
  - "[[wiki/concepts/embeddings]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/inference-economics]]"
---

# Different Levels of Hosting Your Embedding Models

> [[raw/different-levels-of-hosting-your-embedding-models|Raw]] · local

## Summary

A practical tiering of where an embedding model should run, by environment rather
than by benchmark. **Tests**: mocked. **Dev**: Hugging Face Transformers or
Sentence Transformers for simplicity, Ollama or llama.cpp to squeeze more out of a
laptop — and explicitly *not* vLLM, because it has no precompiled binaries for
Apple silicon and porting it across dev machines "quickly becomes a mess".
**Production**, in four steps of increasing scale and maintenance: an API in front
of an open-source model (small/medium data), self-serving with vLLM on Modal,
RunPod, Vertex or AWS (medium), a distributed Ray inference cluster (big data,
hard to maintain), or the vector database's auto-embed feature (big data, easy to
maintain — you write a config and the database does the rest).

The load-bearing recommendation is the abstraction: keep the model behind one
interface (`BaseEmbeddingModel`) with concrete implementations per environment
(`MockedEmbeddingModel`, `SentenceTransformersEmbeddingModel`,
`VoyageAPIEmbeddingModel`, `ModalEmbeddingModel`), selected by a `config.yaml`.
That is what makes the four tiers switchable without touching code.

The author's own setup is given as the example — mocked in tests, Sentence
Transformers in dev (after trying vLLM first and abandoning it on a MacBook),
vLLM on Modal in production, with Voyage AI as the fallback. Voyage is chosen for
its native MongoDB integration and two specific models: contextualized chunk
embeddings, which the note calls the best cost/latency/performance answer to
chunking, and a multimodal model that embeds text and images as one message stack,
"which keeps the natural topology of the conversation".

## Key claims

- Use vLLM in production and something simpler in dev; unifying on vLLM breaks on Apple silicon. [[raw/different-levels-of-hosting-your-embedding-models|cite]]
- Auto-embed inverts the problem — big-data scale that is *easy* to maintain, because the vector database owns the computation. [[raw/different-levels-of-hosting-your-embedding-models|cite]]
- One interface plus per-environment implementations, chosen in config, is what makes tests, dev and prod interchangeable. [[raw/different-levels-of-hosting-your-embedding-models|cite]]
- Contextualized chunk embeddings are presented as the practical answer to chunking's cost/latency/quality trade-off. [[raw/different-levels-of-hosting-your-embedding-models|cite]]
- A multimodal embedding model that takes text and images together preserves the conversation's topology instead of flattening it. [[raw/different-levels-of-hosting-your-embedding-models|cite]]

## Connections

- **Entities**: [[wiki/entities/modal]], [[wiki/entities/voyage-ai]], [[wiki/entities/mongodb]]
- **Concepts**: [[wiki/concepts/embeddings]], [[wiki/concepts/provider-abstraction]], [[wiki/concepts/inference-economics]]

> Synthesis: The same "hide the provider behind an interface" conclusion the inference-cost notes reach, arrived at from the opposite direction — developer experience rather than price — which is the strongest kind of corroboration the wiki has.
