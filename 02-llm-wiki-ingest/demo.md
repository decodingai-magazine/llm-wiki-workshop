# Layer 02 — demo

Run from this directory (`cd 02-llm-wiki-ingest && claude`). All paths are
relative to it. A committed run of these steps lives in
`examples/wiki-ai-engineering/`.

**Start point.** These steps assume you continue from layer 01's end state:

```bash
cp -r ../01-llm-wiki-vanilla/examples/wiki-ai-engineering .
```

You can also start empty — then step 1 ingests 50 notes instead of 40 and nothing
is skipped.

---

## 1. The batch that layer 01 refused

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/03-hard/
```

This is the exact input that made layer 01 stop and refuse.

**Verify**

- [ ] No cap message. The skill reports 40 new and 10 skipped (the notes already
      ingested in layer 01, matched by raw path — not by the directory you typed).
- [ ] It spawns one `source_writer` per new note, in parallel batches. Watch the
      harness: this is the fan-out.
- [ ] The orchestrator never printed a note's contents. It only ever saw receipts.
- [ ] `ls wiki-ai-engineering/wiki/sources | wc -l` → 51 (50 pages + `index.md`).
- [ ] Slugs that were hollow after layer 01 now have pages: `append-only-log` went
      from 1 mention to 11, because the GraphRAG and scaling notes are its other
      witnesses. `agentic-invocation` stayed hollow at 1 — 40 more notes and still
      only one source engages with it, which is the threshold doing its job.
- [ ] **Look at the thin ones.** `wiki/sources/marketing.md`,
      `wiki/sources/constraints.md`, `wiki/sources/feedback-from-v1.md` are short
      and link almost nothing. A three-line note gets a three-line page — the
      threshold makes noise cheap instead of dangerous.

## 2. Ingest a repo

The URL comes from `../data_input_examples/github_links.md`:

```
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
```

**Verify**

- [ ] `clone_repo.py` reports `"action": "cloned"` with a full `commit_sha`.
- [ ] The clone is at `wiki-ai-engineering/raw/repos/.github-decodingai-magazine-…/`
      — dot-prefixed, so Obsidian never sees ~100 MB of someone else's code.
      `git status` stays clean: `**/raw/repos/` is gitignored.
- [ ] `wiki/repos/github-…/ARCHITECTURE.md` exists, is ≤300 lines, opens each
      section with a mermaid diagram, and every code permalink pins the SHA (not
      `main`).
- [ ] `wiki/repos/index.md` was generated, grouped by repo, and the wiki root index
      has a `Repos` browse line.
- [ ] The tail ran: at least one concept page now lists the repo page under
      `sources:` alongside a note. **This is the moment worth pausing on** — a
      claim from someone's notes and a codebase that implements it are two
      independent witnesses.
- [ ] `overview.md` gained a Repos entry.

## 3. Ingest two articles

URLs from `../data_input_examples/substack_links.md`:

```
/02-llm-wiki-ingest ingest https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design https://www.decodingai.com/p/the-coding-agent-loop
```

**Verify**

- [ ] `raw/article-*.md` exist, with frontmatter carrying title, subtitle, author
      and published date pulled from the page's metadata.
- [ ] Open one and scroll: it is the article body, not the whole page. Body
      isolation (`<article>` → `div.body.markup` → `main` → `body`) is the step
      that makes the raw layer worth keeping.
- [ ] Two new source pages; concept pages gain sources — expect overlap with both
      the notes and the repo (agent loop, tools, context window, harness, skills).
- [ ] No `warning` in the fetch receipts. If you see "body under 500 chars", you
      hit a paywall or a bot wall — the adapter is telling you not to trust it.

## 4. Re-ingest the repo — refresh, not skip

```
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
```

**Verify**

- [ ] `"action": "updated"`. The clone was fetched and hard-reset, not re-cloned.
- [ ] `ARCHITECTURE.md` was rewritten and `commit_sha` still matches HEAD; `created`
      is preserved.
- [ ] `log.md` records a refresh. Every other origin would have been skipped here —
      repos are the one exception, because the code moves.

## 5. Ingest a YouTube URL — fail loudly

```
/02-llm-wiki-ingest ingest https://www.youtube.com/watch?v=v3Fr2JR47KA
```

**Verify**

- [ ] `fetch_youtube.py` raises `NotImplementedError` with the exercise message.
- [ ] **Nothing else was written** — no raw file, no page, no log entry.
- [ ] Read `SOURCES.md § How to add a source`. The exercise is three steps, and
      the hard one is not fetching the transcript — it is deciding what the raw
      path should be. (Hint: the video id, never the title.)

## 6. Query across origins

```
/02-llm-wiki-ingest how does the coding agent's loop actually work?
```

**Verify**

- [ ] The answer draws on `ARCHITECTURE.md` **and** the article source pages, and
      cites both with wikilinks.
- [ ] It never opened the clone or a raw article. The wiki layer was enough — that
      is the whole return on the ingest cost.
- [ ] Only `log.md` changed.

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering
```

To keep the wiki but drop the 100 MB of clones: `rm -rf wiki-ai-engineering/raw/repos`.
Re-ingesting any repo brings it back.
