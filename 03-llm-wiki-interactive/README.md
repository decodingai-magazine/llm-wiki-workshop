# Layer 03 — the wiki learns from being used

**Goal: make interaction a second way for the graph to grow.**

Layers 01 and 02 only grew when you fed them something. Here, asking a question can
leave the wiki better than it found it:

```
question ──► answer from wiki pages ──┬─► wiki/questions/<date>-<slug>.md   (always)
                                      ├─► wiki/notes/<slug>.md             (if ≥2 pages cited)
                                      ├─► wiki/open-questions.md           (if it can't answer)
                                      └─► wiki/repos/<repo>/<slug>.md      (if it needs the code)
                                                    │
                                                    └─► the ingest tail runs ─► concept pages grow
```

That last branch is the point. A repo note is a **source-like page**, so it counts
toward the ≥2 threshold like any ingested source — an answer can materialize a
concept page. Everything else the query path writes is deliberately *not*
source-like, because a wiki that counts its own notes as evidence can cite itself
into existence.

## What's inside

Everything from layer 02, plus:

```
03-llm-wiki-interactive/
├── .agents/skills/03-llm-wiki-interactive/
│   ├── QUERY.md              # NEW — the whole query path, Q.1–Q.8
│   ├── SKILL.md              # query path → a pointer; ingest gains an open-questions report
│   ├── CONVENTIONS.md        # + §13 write regimes, §14 the interaction layer
│   ├── PAGES.md              # + question, note, repo_note, open_question contracts
│   ├── SOURCES.md            # unchanged from 02
│   ├── agents/               # unchanged from 02 — repo_writer's question mode is finally wired
│   └── scripts/              # build_index_md: +questions/notes; count_mentions: unchanged, on purpose
├── CHANGES-FROM-PREVIOUS.md
├── demo.md
└── examples/
```

## Run it

```bash
cd 03-llm-wiki-interactive
cp -r ../02-llm-wiki-ingest/examples/wiki-ai-engineering .   # start from layer 02's end state
claude
```

Then follow `demo.md`:

```
/03-llm-wiki-interactive when should I use an append-only log instead of updating rows in place?
/03-llm-wiki-interactive how does the coding agent decide whether a tool call needs approval?
/03-llm-wiki-interactive what do my sources say about evaluating a GraphRAG system end to end?
```

## What to look at when it finishes

- **`wiki/questions/index.md`** — every question you have asked, one line each. The
  cheapest thing in the wiki and the most useful for "have I been here before?".
- **A note that was enriched twice** — `spawned_by_question` has two entries and
  `created` is still the first date. Asking again improved the answer instead of
  forking it.
- **A repo note** — `type: repo_note`, permalinks pinned to a commit SHA, and the
  concept pages it pushed over the threshold. Trace it: question → repo note →
  `count_mentions` → an updated concept page. That is interaction compounding.
- **`wiki/open-questions.md`** — what the wiki knows it does not know.
- **`git diff` on the ingest-owned pages** — the only ones that changed are the ones
  the tail touched. Nothing was hand-edited.

## The three ideas worth taking away

1. **Regimes, not permissions.** "Query mode may not edit ingest-owned pages" is
   one sentence, and it is what keeps the same question asked twice from producing
   two different wikis.
2. **The tail is the only crossing point.** An answer reaches the knowledge graph
   through exactly the same machinery an ingest uses — recount, rewrite, reindex,
   log — so there is one code path to trust.
3. **What you refuse to count matters as much as what you count.** Notes are not
   evidence. A wiki that forgets that will happily keep a page alive on the
   strength of its own summaries.

Back to [layer 01](../01-llm-wiki-vanilla/) · [layer 02](../02-llm-wiki-ingest/)
