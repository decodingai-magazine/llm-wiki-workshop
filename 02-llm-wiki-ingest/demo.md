# Layer 02 — demo

Run from this directory (`cd 02-llm-wiki-ingest && claude`). Paths are relative
to it. You only type prompts — the skill fetches, clones and counts by itself.

This demo starts from nothing: no wiki from layer 01 is needed. The repo and
article URLs come from `../data_input_examples/github_repositories.md` and
`../data_input_examples/substack_articles.md` — swap them there and every step
below follows.

`examples/wiki-02-ai-engineering/` is where this demo ends up **through step 3**:
the 10 notes, the repo and all four articles. (Its `log.md` shows the articles
arriving before the repo — the order changes nothing — and step 7 is not
included; the pages are what these steps produce.)

---

## 1. Ingest 10 notes

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/02-medium/
```

Accept the proposed slug `ai-engineering`. Then watch the harness: one
`source_writer` per note, in parallel. The orchestrator never prints a note — it
only ever sees receipts.

**Verify**

- [ ] `wiki-ai-engineering/wiki/sources/` has 10 pages, and the report lists the
      entity and concept pages that materialized at ≥2 mentions, plus the slugs
      waiting at 1.

## 2. Ingest a repo

```
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
```

The skill clones it (shallow, ~100 MB, into a dot-prefixed folder Obsidian never
sees) and spawns `repo_writer`.

**Verify**

- [ ] `wiki/repos/github-…/ARCHITECTURE.md` exists — mermaid per section, ≤300
      lines, every permalink pinned to a commit SHA — **and** at least one concept
      page now lists it under `sources:` next to a note. A codebase and a note are
      two independent witnesses; that is what pushed the page over the threshold.

## 3. Ingest four articles

```
/02-llm-wiki-ingest ingest the substack articles from ../data_input_examples/substack_articles.md
```

**Verify**

- [ ] `raw/article-*.md` hold the article body only — title, author and date in
      frontmatter, no navigation, no cookie banner — and concept pages now cite
      notes, the repo and an article side by side.

## 4. Re-ingest the repo — refresh, not skip

```
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
```

**Verify**

- [ ] The report says the repo was **refreshed** (fetched, not re-cloned) and
      `ARCHITECTURE.md` was rewritten with its `created` preserved. Every other
      origin would have been skipped here; repos are the exception because the
      code moves.

## 5. Ingest a YouTube URL (fail loudly)

```
/02-llm-wiki-ingest ingest https://www.youtube.com/watch?v=sJpop1juVBQ
```

**Verify**

- [ ] The skill reports that the adapter is not implemented, and **nothing was
      ingested** — no raw file, no page. Wiring it up is the exercise
      in `SOURCES.md § How to add a source`; the hard part is not the transcript,
      it is choosing the raw path. (Hint: the video id, never the title.)

## 6. Query across origins

#### Question 1

```
/02-llm-wiki-ingest how does the coding agent's loop actually work?
```

#### Question 2

```
/02-llm-wiki-ingest how does agentic graphrag work?
```

#### Question 3

```
/02-llm-wiki-ingest What are some essential context engineering techniques for coding agents?
```

**Verify**

- [ ] The answer cites `ARCHITECTURE.md` **and** an article source page with
      wikilinks, never opened the clone or a raw file, and only `log.md` changed.
      That is the whole return on the ingest cost.

## 7. Optional — the big graph

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/03-hard/
```

`03-hard/` is all 50 notes, the 10 you already ingested included: 40 new, 10
skipped by raw path. It is the batch layer 01 refuses, it takes a while, and the
graph it leaves behind is the one layer 03 starts from.

**Verify**

- [ ] Open `wiki-ai-engineering/` as an Obsidian vault: slugs that were hollow
      after step 1 now have pages, and the three-line notes (`constraints`,
      `marketing`, `feedback-from-v1`) got three-line pages that link almost
      nothing. Noise is cheap; the threshold made it so.

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering
```

To keep the wiki but drop the clone: `rm -rf wiki-ai-engineering/raw/repos`.
Re-ingesting the repo brings it back.
