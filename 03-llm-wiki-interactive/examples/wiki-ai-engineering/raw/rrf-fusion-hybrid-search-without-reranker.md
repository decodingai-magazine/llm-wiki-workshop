# You don't need a reranker model for hybrid search — RRF fusion in 20 lines of Python

## Brief

| Field           | Value |
|-----------------|-------|
| **Problem**     | You're building hybrid search (text + vector) and every tutorial tells you to add a cross-encoder reranker — Cohere Rerank, a BERT model, or some other ML pipeline. That's another API call, another model to manage, another latency hit, another cost line. All to merge two ranked lists. |
| **Solution**    | Reciprocal Rank Fusion (RRF): `score = sum(1 / (k + rank))` across both result lists. No model, no API call, no dependencies. ~20 lines of Python. It ranks documents that appear in both lists highest, without needing to normalize scores across different search methods. |
| **Transformation** | Hybrid search that combines the strengths of keyword and semantic retrieval — exact name matches from text search, conceptual similarity from vector search — with zero additional infrastructure. The fusion runs in microseconds. |
| **Hook**        | Every hybrid search tutorial tells you to add a reranker. Here's why I didn't — and a 20-line alternative that works. |
| **Target audience** | AI/ML engineers building RAG systems, backend developers implementing search, anyone who wants hybrid retrieval without the complexity of a reranker model. |

## Outline

1. The hybrid search problem: text and vector search return differently-scored ranked lists. How do you merge them?
2. The reranker approach: what it is, why it's recommended everywhere, and what it costs (latency, money, complexity).
3. The RRF alternative: the formula, why it works, and why scores don't need to be comparable.
4. The implementation: ~20 lines of Python, walking through each step.
5. How it fits into the full retrieval pipeline: RRF-fused seed nodes → $graphLookup expansion.
6. When you might actually need a reranker — and when RRF is enough.

---

## Full body

### The problem: merging two ranked lists with incomparable scores

I built a retrieval layer for a knowledge graph that uses two search methods:

**Text search** (`$text` on MongoDB) — keyword matching on node names, content, and aliases. Returns results scored by MongoDB's internal `textScore` — a BM25-like relevance metric. Scores are typically in the range 0.5–10+.

**Vector search** (`$vectorSearch` on MongoDB via mongot) — semantic similarity using cosine distance on embedding vectors. Returns results scored between 0.0 and 1.0.

The scores are not comparable. A textScore of 3.5 and a vectorSearchScore of 0.87 tell you nothing about which result is more relevant. You can't just average them, weight them, or sort by either one.

The standard solution: add a reranker model. Pass both result sets to a cross-encoder (like Cohere Rerank or a BERT-based model) that re-scores every document against the original query. This works — but it adds:

- Another API call (50-200ms latency)
- Another cost per query (Cohere charges per search unit)
- Another model to evaluate and maintain
- Another failure point in your retrieval pipeline

### RRF: rank arithmetic instead of score comparison

Reciprocal Rank Fusion was published in 2009. The idea: ignore scores entirely. Only use ranks.

For each document that appears in any result list, compute:

```
rrf_score = sum(1 / (k + rank)) across all lists the document appears in
```

Where:
- `rank` is the 1-indexed position in each result list
- `k` is a constant (typically 60) that controls how much weight later positions get

A document ranked #1 in both lists gets: `1/(60+1) + 1/(60+1) = 0.0328`
A document ranked #1 in text but missing from vector gets: `1/(60+1) = 0.0164`
A document ranked #5 in vector and #10 in text gets: `1/(60+5) + 1/(60+10) = 0.0154 + 0.0143 = 0.0297`

Documents that appear in both lists rank higher than documents in only one list. Documents ranked highly in both lists rank highest. And the scores from the original search methods are never compared — only positions matter.

### The implementation

Here's the full fusion logic:

```python
def _rrf_fuse(
    vector_results: list[dict[str, Any]],
    text_results: list[dict[str, Any]],
    *,
    k: int = 60,
) -> dict[Any, dict[str, Any]]:
    """Reciprocal Rank Fusion: score = sum(1 / (k + rank)) across both lists.

    Returns {doc_id: {"doc": document, "score": float}}.
    """

    fused: dict[Any, dict[str, Any]] = {}

    for rank, doc in enumerate(vector_results):
        doc_id = doc["_id"]
        if doc_id not in fused:
            fused[doc_id] = {"doc": doc, "score": 0.0}
        fused[doc_id]["score"] += 1.0 / (k + rank + 1)

    for rank, doc in enumerate(text_results):
        doc_id = doc["_id"]
        if doc_id not in fused:
            fused[doc_id] = {"doc": doc, "score": 0.0}
        fused[doc_id]["score"] += 1.0 / (k + rank + 1)

    return fused
```

That's it. Two loops, one dictionary. The caller sorts by score descending and takes the top-k:

```python
ranked = sorted(fused.items(), key=lambda x: x[1]["score"], reverse=True)[:top_k]
return [item["doc"] for _, item in ranked]
```

### How it fits into the full retrieval pipeline

The query layer uses RRF as the first phase of a two-phase retrieval:

**Phase 1 — Search seed nodes:**
1. Run `$text` query on the knowledge graph collection (standard MongoDB text index on `name`, `properties.content`, `properties.aliases`)
2. Run `$vectorSearch` pipeline (mongot vector index on `embedding` field, cosine similarity)
3. Fuse results with RRF (k=60)
4. Take top-k nodes by fused score

**Phase 2 — Expand graph:**
1. Start from the seed node IDs
2. Run two `$graphLookup` passes (outgoing + incoming edges)
3. Hydrate all discovered nodes

RRF gives us the best of both worlds: text search catches exact name matches (someone searching "Paul Iusztin" gets the person node even if the embedding is slightly off), while vector search catches conceptual similarity (someone searching "machine learning operations" finds nodes about MLOps even if those exact words don't appear).

### The k parameter

The constant `k` (default: 60) controls the score distribution:

- **Higher k** (e.g., 100): more uniform scores across ranks. Later results contribute almost as much as early ones. Good when both search methods are noisy and you don't want to over-weight the top result.
- **Lower k** (e.g., 10): steeper dropoff. The #1 result dominates. Good when you trust both rankers to put the best result first.

The value 60 comes from the original Cormack et al. 2009 paper and works well as a default. In my knowledge graph queries, I haven't needed to tune it — but it's configurable via `app_config.query.rrf_k`.

### When you might need a reranker

RRF has limits:

- **It only uses rank, not content.** A reranker reads the actual document text and the query, which can catch relevance signals RRF misses.
- **It assumes both search methods return reasonable rankings.** If one method consistently returns garbage, RRF will promote that garbage when it happens to overlap with the other method's results.
- **It doesn't work well for single-method queries.** If you only have one search method, there's nothing to fuse.

In practice, for a knowledge graph with typed entities and structured properties, RRF is more than enough. The text search handles exact matches, the vector search handles semantic similarity, and the fusion handles the rest. I'd consider a reranker if I were building a general-purpose search engine with millions of heterogeneous documents — not for a scoped knowledge graph with a defined ontology.

### The takeaway

RRF is a 2009 technique that costs nothing, runs in microseconds, and requires zero ML infrastructure. Before reaching for a reranker API, try it. For most hybrid search use cases — especially knowledge graphs and structured RAG systems — it's enough.
