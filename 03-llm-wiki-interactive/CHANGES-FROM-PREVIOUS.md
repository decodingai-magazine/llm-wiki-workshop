# What changed from layer 02

Layer 03 is a superset of layer 02. `agents/`, `SOURCES.md` and the three adapters
are **byte-identical**; the ingest path is unchanged except for one added report
step.

```
$ diff -r --brief 02-llm-wiki-ingest/.agents/skills/02-llm-wiki-ingest \
                  03-llm-wiki-interactive/.agents/skills/03-llm-wiki-interactive
Files 02/CONVENTIONS.md and 03/CONVENTIONS.md differ
Files 02/PAGES.md and 03/PAGES.md differ
Only in 03: QUERY.md
Files 02/SKILL.md and 03/SKILL.md differ
Files 02/scripts/build_index_md.py and 03/scripts/build_index_md.py differ
Files 02/scripts/count_mentions.py and 03/scripts/count_mentions.py differ
```

A layer-02 wiki is a valid layer-03 wiki. The 03 demo starts by continuing one.

---

## 1. The idea: the wiki learns from being used

In layers 01 and 02 the wiki only grew when someone ingested something. Here,
asking it a question can leave it better than it found it:

- every question is logged as a slim pointer page, so "what have I already asked?"
  is answerable without re-reading answers;
- an answer that synthesized across ≥2 wiki pages becomes a **note** — and a repeat
  question *enriches that note* rather than adding a second one;
- a question the wiki cannot answer becomes an **open question**, which is the
  wiki telling you what to ingest next;
- a question about an ingested repo produces a **repo note** that is source-like,
  so it flows through the same ingest tail as any source and can push a concept
  page over the ≥2 threshold.

That last one is the point of the layer. Interaction is not a side channel — it is
a second way for the graph to grow, using the same machinery.

## 2. Write regimes — the safety story

| Regime | Pages | Query mode may |
|---|---|---|
| ingest-owned | `raw/`, `sources/`, `entities/`, `concepts/`, `overview.md`, `repos/*/ARCHITECTURE.md` | **read only** |
| interaction-owned | `questions/`, `notes/`, `open-questions.md` | write freely |
| repo notes | `repos/<repo>/<slug>.md` | write, then run the ingest tail |

The invariant: **reading a source can never change what the wiki says that source
means.** Otherwise the same question asked twice leaves two different wikis behind.
When an answer shows an ingest-owned page is wrong, that is recorded in
`open-questions.md`, not edited into the page.

## 3. New file

| File | What it adds |
|---|---|
| `QUERY.md` | The whole query path — Q.1 locate, Q.2 index, Q.3 disclosure ladder, Q.4 classify, Q.5 general path + save-back rules, Q.6 repo path + ingest tail, Q.7 open questions, Q.8 log and present. |

## 4. `SKILL.md` — sections touched

| Section | Change |
|---|---|
| Intro | Three contract files became four; the layer's idea is restated. |
| **Query path** | Replaced by a pointer to `QUERY.md` plus the one-line save-back rule. |
| **Step 1.7b** | New: after the tail, read `open-questions.md` and report which ones the new sources appear to address — **report only, never edit**. |
| Agent reference | `repo_writer` gains its `question`-mode row; the file itself is unchanged from 02. |

Steps 0, 1.0–1.7 and 1.8 are otherwise untouched.

## 5. `CONVENTIONS.md` and `PAGES.md` — appended again

- `CONVENTIONS.md` §13 **Write regimes**: the table above, the one crossing point
  (a repo note through the ingest tail), and why `questions/` and `notes/` are
  deliberately *not* source-like.
- `CONVENTIONS.md` §14 **The interaction layer**: the directory shape and the three
  rules that stop it becoming a chat log.
- `PAGES.md`: contracts for `question`, `note`, `repo_note` and `open_question`.

## 6. Scripts — one real change and one deliberate non-change

- `build_index_md.py`: `questions` and `notes` added to `SUBDIRS`, and
  `open-questions.md` to `SINGLETONS`. Three lines.
- `count_mentions.py`: **unchanged except for a comment explaining why.** This is
  the subtle part of the layer. `questions/` and `notes/` are written *from* wiki
  pages, so counting them as source-like would let the wiki cite itself into
  existence — one note about a concept would be enough to keep that concept alive
  forever. Repo notes are the exception, and they already match the existing
  `repos/*/*.md` glob, so they need no change at all.

If you take one thing from this layer's diff: the interesting design work was
deciding what **not** to count.
