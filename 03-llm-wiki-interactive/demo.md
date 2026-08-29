# Layer 03 — demo

Run from this directory. A committed run of these steps lives in
`examples/wiki-ai-engineering/`.

**Start point** — continue from layer 02's end state:

```bash
cp -r ../02-llm-wiki-ingest/examples/wiki-ai-engineering .
```

That wiki has 53 source-like pages, 10 entities, 38 concepts and one repo. The
repo clone is not in `examples/` (it is regenerable and huge) — step 4 needs it, so
bring it back first:

```bash
uv run --script .agents/skills/03-llm-wiki-interactive/scripts/clone_repo.py \
  --repo https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course \
  --wiki-dir wiki-ai-engineering
```

---

## 1. A question the wiki can answer

```
/03-llm-wiki-interactive when should I use an append-only log instead of updating rows in place?
```

**Verify**

- [ ] The answer walks the ladder — index → concept pages → maybe a source page —
      and cites ≥2 wiki pages with wikilinks.
- [ ] It surfaces the wiki's own disagreement: nine sources argue for the log, one
      reports abandoning it. A wiki that hides that is worse than no wiki.
- [ ] `wiki/questions/<date>-append-only-log-vs-in-place-updates.md` exists, is
      ≤25 lines, and contains **no** diagrams, code or per-claim citations.
- [ ] `wiki/notes/<slug>.md` exists and holds the actual answer, every claim citing
      a wiki page — never `raw/`.
- [ ] No ingest-owned page changed. `git status` inside the wiki dir shows only
      `questions/`, `notes/`, the regenerated indexes and `log.md`.

## 2. The same question, asked differently

```
/03-llm-wiki-interactive is event sourcing actually worth it for a personal knowledge graph?
```

**Verify**

- [ ] **No second note.** The existing note was enriched in place: `created`
      unchanged, `timestamp` bumped, `spawned_by_question` now has two entries.
- [ ] A second question page was written, pointing at the same note.
- [ ] `wiki/notes/index.md` still lists one note on the topic.

This is the rule that keeps an interaction layer from turning into a chat log:
**referencing over duplication.**

## 3. A question the wiki cannot answer

```
/03-llm-wiki-interactive how do I decide that a fact in the memory has gone stale?
```

**Verify**

- [ ] The answer says plainly that the wiki does not cover this, and says what it
      *does* have (a mechanism — the log — but no policy).
- [ ] `wiki/open-questions.md` was created with frontmatter and a dated entry
      citing the question page.
- [ ] A question page was still written. **No note** — there was no answer to save.

Then flag one yourself:

```
/03-llm-wiki-interactive log this as open: what actually goes into a coding agent's context window each turn?
```

- [ ] Appended under the same date, marked as flagged by the user.

## 4. A question that needs the code

```
/03-llm-wiki-interactive in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?
```

**Verify**

- [ ] The skill reads `wiki/repos/<repo>/ARCHITECTURE.md` **first**, finds it
      covers the policy but not the routing, and only then spawns `repo_writer`
      with `mode: question`.
- [ ] `wiki/repos/<repo>/<question-slug>.md` exists with `type: repo_note`, a
      verbatim `question`, `commit_sha`, and `file:line` evidence whose permalinks
      pin that SHA.
- [ ] **The ingest tail ran.** `count_mentions.py` now counts the repo note as a
      source-like page, and at least one concept page gained it under `sources:`.
      Trace it: question → repo note → recount → updated concept page.
- [ ] `overview.md` and the indexes were regenerated; `log.md` records the tail.
- [ ] The question page's `answer_doc` points at the repo note, not at a note.

This is the layer's whole thesis in one step: **an answer became evidence**, and it
got there through exactly the machinery an ingest uses.

## 5. Ingest something that answers an open question

```
/03-llm-wiki-interactive ingest https://www.decodingai.com/p/context-engineering-for-coding-agents
```

**Verify**

- [ ] Normal ingest: article fetched, source page written, tail run.
- [ ] The report ends with a bullet naming the open question this source appears to
      address — the one you flagged in step 3.
- [ ] **`open-questions.md` was not edited.** Nothing auto-resolves; a human
      decides whether the answer landed.

## 6. Read the trail

```bash
grep -E '^## [0-9]{4}-' wiki-ai-engineering/log.md
cat wiki-ai-engineering/wiki/questions/index.md
```

**Verify**

- [ ] The log reads as a history: ingests and queries interleaved, oldest first.
- [ ] The questions index is one line per question — cheap to scan, and enough to
      answer "have I asked this before?" without opening anything.

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering && cp -r ../02-llm-wiki-ingest/examples/wiki-ai-engineering .
```
