# What changed from layer 01

Layer 02 is a **superset** of layer 01. Every file that did not need to change is
byte-identical, and every file that did is listed here with the exact sections
touched.

```
$ diff -r --brief 01-llm-wiki-vanilla/.agents/skills/01-llm-wiki-vanilla \
                  02-llm-wiki-ingest/.agents/skills/02-llm-wiki-ingest
Files 01/CONVENTIONS.md and 02/CONVENTIONS.md differ
Files 01/PAGES.md and 02/PAGES.md differ
Files 01/SKILL.md and 02/SKILL.md differ
Only in 02: SOURCES.md
Only in 02: agents
Files 01/scripts/build_index_md.py and 02/scripts/build_index_md.py differ
Only in 02/scripts: clone_repo.py
Files 01/scripts/count_mentions.py and 02/scripts/count_mentions.py differ
Only in 02/scripts: fetch_article.py
Only in 02/scripts: fetch_youtube.py
```

Nothing was deleted. No page contract changed. The data on disk from a layer-01
run is a valid layer-02 wiki — the 02 demo starts by continuing one.

---

## 1. Why the cap existed, and why it is gone

Layer 01 refused to ingest more than 10 notes in one run. That was not an
arbitrary safety rail: **the orchestrator read every note itself**, so a run's
cost was the sum of every input, and the 11th note competed for context with the
first ten. Beyond that point the pages get worse before the run gets slower.

Fan-out removes the cause rather than raising the number:

| Who | May read | Never reads |
|---|---|---|
| orchestrator | receipts, script output, `log.md` | `raw/`, wiki pages |
| `source_writer` | **one** raw file | any other raw file, any wiki page |
| `repo_writer` | one clone | other clones, source pages |
| `page_writer` | the source-like pages for its slug | `raw/`, other aggregate pages |
| `overview_writer` | frontmatter; ≤5 full pages | `raw/` |

Each raw file is read **exactly once, ever**. The orchestrator sees a few hundred
tokens of JSON per source instead of the source itself, so 50 sources cost roughly
the same orchestrator context as 5 — the work grows, the context does not. That is
the entire reason this layer exists, and it is the same reason the wiki is worth
building at all: pay the reading cost once, answer questions from pages forever.

The trade you are making: **the orchestrator can no longer see the material it is
organizing.** It coordinates on receipts alone. That is why the receipt shape is
specified as tightly as the page templates — it is the only channel left.

## 2. Harness-agnostic subagents

Subagent logic lives in plain markdown under `agents/`, not in harness-specific
config. To spawn one: read the file, pass its body as the prompt, add the inputs
its table lists, expect one JSON receipt. Model preference is stated in prose
("Sonnet-class, or your provider's equivalent"), never pinned in frontmatter.

Any harness that can run a sub-conversation can run these agents. If yours cannot
run subagents at all, run the agent files as sequential prompts yourself — you get
the same wiki, without the parallelism.

## 3. New files

| File | What it adds |
|---|---|
| `SOURCES.md` | The adapter contract, the routing table, per-origin recipes, and "how to add a source" walked through YouTube. |
| `agents/source_writer.md` | One raw file → one source page. The only agent allowed to read `raw/`. |
| `agents/repo_writer.md` | One clone → one repo page. `architecture` mode used here; `question` mode specified but only wired up in layer 03. |
| `agents/page_writer.md` | One slug + its source-like pages → one entity/concept page. |
| `agents/overview_writer.md` | Frontmatter walk → `wiki/overview.md`. |
| `scripts/clone_repo.py` | Shallow clone / refresh into `raw/repos/.github-<owner>-<repo>/`. |
| `scripts/fetch_article.py` | `curl` → body isolation → markdown at `raw/article-<slug>.md`. |
| `scripts/fetch_youtube.py` | Skeleton that raises `NotImplementedError` — the workshop exercise. |

## 4. `SKILL.md` — sections touched

| Section | Change |
|---|---|
| Intro | Two contract files became three (`SOURCES.md`); the orchestrator's job is restated as route → spawn → tail. |
| **Spawning subagents** | New section, before the ingest path. |
| **Step 1.0 — Route each input** | New. The routing table; the YouTube skeleton fails loudly. |
| Step 1.1 | Dedup now also lists `raw/repos/`; repos refresh rather than skip. **The 10-source cap is removed.** |
| Step 1.2 | "Copy the raw layer" → "Run the adapter for each new input" (`cp`, `fetch_article.py`, `clone_repo.py`). |
| Step 1.3 | "Write one source page" → "Spawn one writer per new raw artifact" (`source_writer` per file, `repo_writer` per repo). |
| Step 1.4 | The tail spawns one `page_writer` per qualifying slug; the count now spans `wiki/repos/*/` too. |
| Step 1.5 | The overview is written by `overview_writer`. |
| Step 1.8 | The report breaks counts down by origin, including refreshed repos. |
| Query path Q.3 | Code questions start at `ARCHITECTURE.md`. |
| Harness notes | Fifth capability: spawn a subagent. |
| **Agent reference** | New table. |
| Script reference | Three adapter rows added. |

Steps 0, 1, 1.6, 1.7 and the rest of the query path are unchanged.

## 5. `CONVENTIONS.md` and `PAGES.md` — appended, never rewritten

- `CONVENTIONS.md` §11 **Repos as sources**: layout, origin prefixes, why the clone
  is dot-prefixed, source-like pages now include `wiki/repos/*/*.md`, refresh rule.
- `CONVENTIONS.md` §12 **Context discipline**: the read table above.
- `PAGES.md` **`repo`**: frontmatter, body skeleton, budget, scope, receipt.

Everything from layer 01 is still there, in the same order, with the same wording.

## 6. Scripts — small, surgical diffs

- `build_index_md.py`: a `NESTED_SUBDIRS` constant, a `nested_page_files()` helper
  and a `render_nested_index()` renderer, so `wiki/repos/<repo>/*.md` gets one
  grouped `wiki/repos/index.md` and a Browse line. ~50 lines; nothing existing
  changed behaviour.
- `count_mentions.py`: **one line** — `SOURCE_LIKE_GLOBS` gains `repos/*/*.md`.
  That single line is what lets a codebase corroborate a concept.
