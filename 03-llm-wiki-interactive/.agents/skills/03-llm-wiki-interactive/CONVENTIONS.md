# CONVENTIONS — the data contract

Everything in this file is shared by all three workshop layers. Layers 02 and 03
**append** to it (look for `<!-- added in 02 -->` / `<!-- added in 03 -->`); they
never rewrite what is here.

Page templates live in `PAGES.md`. The orchestration steps live in `SKILL.md`.

---

## 1. Directory layout

One wiki per project, in the project root, named `wiki-<slug>/`:

```
wiki-<slug>/
├── log.md                       # append-only history; oldest first
├── raw/                         # immutable copies of what was ingested
│   └── <slug>.md                # one file per ingested note
└── wiki/                        # the knowledge bundle — every .md carries a `type`
    ├── index.md                 # GENERATED bundle root (carries okf_version)
    ├── overview.md              # type: overview
    ├── sources/
    │   ├── index.md             # GENERATED
    │   └── <slug>.md            # type: source — one per raw file
    ├── entities/ { index.md, <slug>.md }   # type: entity
    └── concepts/ { index.md, <slug>.md }   # type: concept
```

Two halves, and the split is the whole point:

- `raw/` is **what was said** — never edited, never summarized in place.
- `wiki/` is **what we know** — written by the LLM, rewritten as sources accumulate.

## 2. Three-layer progressive disclosure

Any agent reading the wiki walks down this ladder and **stops as soon as the
question is answered**:

1. `wiki/index.md` → the relevant `wiki/<subdir>/index.md` — one
   `title — description` bullet per page. This is the cheap map.
2. The wiki page itself (source / entity / concept). ~1 page of curated prose.
3. `raw/` — only when a wiki page is genuinely insufficient. **Never bulk-read raw.**

Layer 2 exists so that layer 3 almost never has to be read. A wiki that forces
every reader back into `raw/` has failed at its job.

## 3. Source-like pages and the ≥2 threshold

A **source-like page** is a page written directly from one ingested artifact.
In layer 01 that is exactly `wiki/sources/*.md`.

Every source-like page declares, in its frontmatter, the slugs it substantively
engages with:

```yaml
entities:
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/mcp]]"
```

> **An entity or concept page exists if and only if ≥2 distinct source-like
> pages list it.**

`scripts/count_mentions.py` is the single source of truth for that count — never
eyeball it. One note mentioning something is a fact about that note; two notes
mentioning it is a fact about your knowledge, and that is what earns a page.

**Promissory links.** A source-like page may link `[[wiki/concepts/<slug>]]`
before the page exists. Obsidian renders it as a hollow node and it resolves the
day the second mention lands. The price is **slug discipline**: lowercase
kebab-case, ASCII, punctuation stripped, ≤60 chars — the slug the eventual page
will use. `agent-loop`, not `Agent Loops` or `agentic_loop`.

## 4. Identity and dedup

**Identity is the raw artifact path.** Every ingested input maps to one
deterministic path under `raw/`; if that path already exists, the input has
already been ingested.

| Input | Raw path | Slug from |
|---|---|---|
| local note | `raw/<slug>.md` | the filename stem |

Dedup is therefore an `ls`, not a frontmatter walk: compute the raw path, check
whether it exists, done.

`original_path` on a source page records **provenance, not identity** — the path
as it was given, normalized relative to the project root
(`../data_input_examples/notes/01-easy/foo.md` becomes
`data_input_examples/notes/01-easy/foo.md`). The same note reached through two
different directories is one source, ingested once, and the wiki remembers the
first path it came from.

- Already-ingested input → **skipped**, reported by name with its existing `original_path`.
- Same slug, different content → **still skipped**, with a warning naming both
  paths. Renaming the incoming file is the fix; silently overwriting `raw/` is not.

## 5. Frontmatter rules

- Every page in `wiki/` carries: `type`, `title`, `description`, `created`,
  `timestamp`.
- `description` is **one sentence**. It is the only thing the index shows, so it
  is the single highest-leverage line on the page.
- `created` is preserved across rewrites; `timestamp` is bumped on every
  meaningful change. Both are ISO-8601 UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`).
- **Wikilinks inside YAML are always quoted**: `- "[[wiki/sources/foo]]"`.
  A bare `[[...]]` is a YAML flow sequence and will parse into nonsense.
- **Quote any value containing `: `** — a colon followed by a space makes YAML read
  the rest as a mapping, and the page silently stops parsing. This bites
  `description` first, because one-sentence gists like
  `description: "The rule: quote it"` are natural to write. `build_index_md.py`
  catches it as an `unparseable YAML frontmatter` error.
- **No `tags:` field, anywhere.** A cross-cutting topic worth grouping by is
  worth a concept page; free-form tag strings rot and point at nothing.

Full per-type contracts: `PAGES.md`.

## 6. Linking and citations

- Wiki → wiki and wiki → raw use `[[wikilinks]]`, written **relative to
  `wiki-<slug>/` with no extension**: `[[wiki/concepts/mcp]]`, `[[raw/foo]]`.
  Obsidian resolves these by path suffix, so they work whether the vault is the
  project root or the wiki dir itself.
- External links use normal markdown: `[title](https://...)`.
- **Every claim on a source page cites the raw file**:
  `[[raw/<slug>#<heading>|cite]]`.
- **Every claim on an entity/concept page cites a source-like page**:
  `[[wiki/sources/<slug>]]`.
- LLM judgment is never laundered as a sourced claim. It goes on its own line,
  prefixed `> Synthesis:`.
- Citation links must resolve. Only entity/concept cross-references may be
  promissory (§3).

## 7. Immutability and write regimes

- `raw/` is **immutable**. Re-ingesting a note does not overwrite it (§4).
- `wiki/` is **LLM-owned**. A human may edit it, but the next ingest may rewrite
  what they wrote — deliberate edits belong in `raw/` or in a note the pipeline
  does not own.
- All `index.md` files are **generated**. Never hand-edit one; run
  `build_index_md.py`.
- `log.md` is **append-only**, oldest entry first.

## 8. The ingest tail

Whenever a new source-like page lands, the same five steps run — this workshop
calls them the **ingest tail**, and every layer reuses them verbatim:

1. `count_mentions.py` — recount mentions across all source-like pages.
2. Write/update every entity/concept page whose slug is now ≥2 **and** appears in
   one of the new pages. (A slug at ≥2 that no new page touched is already
   written and unchanged — skip it.)
3. Rewrite `overview.md`.
4. `build_index_md.py` — regenerate the index cache.
5. Append one entry to `log.md`.

## 9. `log.md`

Created on init with a `# Log` header. Entries are appended, oldest first:

```markdown
## YYYY-MM-DD <op> | <subject>

- 2–8 bullets: what was added, what was skipped, which pages were written, decisions taken
```

`<op>` is `ingest` or `query`. The date-led heading keeps the log greppable:
`grep -E '^## [0-9]{4}-' log.md`.

## 10. OKF alignment (why the layout looks like this)

`wiki/` is an [Open Knowledge Format](https://openknowledgeformat.org) v0.1
bundle. The parts we honour:

- markdown documents with YAML frontmatter; **path is identity**;
- every non-reserved file carries a non-empty `type`;
- `index.md` and `log.md` are **reserved** — navigation and history, not content;
- the bundle root `wiki/index.md` declares `okf_version: "0.1"`;
- frontmatter is canonical, the index is a **rebuildable cache** (delete every
  `index.md`, re-run the script, get the same bytes back).

Two deliberate divergences: we use Obsidian `[[wikilinks]]` instead of relative
markdown links (the graph view is a teaching tool), and our log is oldest-first
and append-only.

`build_index_md.py` checks conformance on every run: a page with no `type` is an
error (non-zero exit), a missing `description` or a malformed log heading is a
warning on stderr.

---

<!-- added in 02 -->

## 11. Repos as sources (added in 02)

A repository is a source like any other; only its raw artifact is a directory
instead of a file.

```
wiki-<slug>/
├── raw/
│   ├── <slug>.md                                # local note (01)
│   ├── article-<slug>.md                        # fetched article (02)
│   ├── youtube-<slug>.md                        # transcript (02 — skeleton adapter)
│   └── repos/
│       └── .github-<owner>-<repo>/              # shallow clone, --depth 1
└── wiki/
    └── repos/
        ├── index.md                             # GENERATED — grouped by repo
        └── github-<owner>-<repo>/
            └── ARCHITECTURE.md                  # type: repo
```

**Origin prefixes** keep `raw/` self-describing at a glance: no prefix = a local
note, `article-` = fetched from the web, `youtube-` = a transcript. The prefix is
part of the identity, so the same slug from two origins never collides.

**The clone is dot-prefixed** (`.github-…`) for one reason worth stating: Obsidian
ignores dot-directories, so a 100 MB checkout stays out of the vault, the graph
view and search with zero configuration. It is also gitignored — clones are
regenerable, and nobody should review a vendored copy of someone else's repo in a
pull request.

**Source-like pages now include `wiki/repos/*/*.md`.** A repo page carries the same
`entities:` / `concepts:` frontmatter as a source page and counts toward the ≥2
threshold identically. This is the point: a concept mentioned in one note and
implemented in one codebase has two independent witnesses, and materializes.

**Repos refresh instead of skipping.** Re-ingesting a repo runs `git fetch` plus
`reset --hard`, rewrites `ARCHITECTURE.md`, bumps `commit_sha`, and re-runs the
ingest tail. Every other origin is immutable once ingested (§7); a repo is a
moving target, and pretending otherwise would leave permalinks pointing at code
that no longer exists.

## 12. Context discipline (added in 02)

Layer 01's ten-source cap came from a single fact: the orchestrator read every
note. This layer removes the cap by making sure nothing ever reads everything.

| Who | May read | Never reads |
|---|---|---|
| orchestrator | receipts, script output, `log.md` | `raw/`, wiki pages |
| `source_writer` | **one** raw file | any other raw file, any wiki page |
| `repo_writer` | one clone | other clones, source pages |
| `page_writer` | the source-like pages for its slug | `raw/`, other aggregate pages |
| `overview_writer` | frontmatter; ≤5 full pages | `raw/` |

Each raw file is read **exactly once, ever** — after that, the wiki is the
interface. That is what makes the wiki compound: the expensive read happens on
ingest, and every future question is answered from pages that already exist.

---

<!-- added in 03 -->

## 13. Write regimes (added in 03)

Once querying the wiki can also write to it, "who owns this page" stops being
obvious. Three regimes, and the boundary between them is the layer's whole safety
story:

| Regime | Pages | Written by | Rewritten when |
|---|---|---|---|
| **ingest-owned** | `raw/`, `sources/`, `entities/`, `concepts/`, `overview.md`, `repos/*/ARCHITECTURE.md` | the ingest path | a source is added or a repo refreshed |
| **interaction-owned** | `questions/`, `notes/`, `open-questions.md` | the query path | a question is asked or answered |
| **repo notes** | `repos/<repo>/<question-slug>.md` | `repo_writer` in `question` mode, from the query path | never — they are appended, then flow through the ingest tail |

The rule that follows: **query mode never edits an ingest-owned page.** Reading a
source cannot change what the wiki says the source means, or the same question
asked twice would leave two different wikis behind.

When an answer reveals that an ingest-owned page is wrong, thin or stale, that is
information — record it in `open-questions.md` and let the next ingest fold it in.

### The one crossing point

A repo note *is* a source-like page: it carries `entities:` / `concepts:` and it
counts toward the ≥2 threshold. So after one is written, the query path runs the
**ingest tail** (§8) — recount, update the qualifying pages, rewrite the overview,
regenerate the index, append the log. That is the only way an answer reaches an
ingest-owned page, and it goes through the same machinery an ingest would.

`questions/` and `notes/` are deliberately **not** source-like. They are written
*from* wiki pages, so counting them would let the wiki cite itself into existence —
one note about a concept would be enough to keep that concept's page alive. That
is why `count_mentions.py` is unchanged in this layer.

## 14. The interaction layer (added in 03)

```
wiki-<slug>/wiki/
├── questions/                          # type: question — slim pointers, ≤25 lines
│   ├── index.md                        # GENERATED
│   └── YYYY-MM-DD-<slug>.md
├── notes/                              # type: note — the actual synthesized answers
│   ├── index.md                        # GENERATED
│   └── <slug>.md
└── open-questions.md                   # type: open_question — append-only, dated
```

Three rules keep this layer from turning into a chat log:

1. **Always write the question page; write a note only when the answer earned it** —
   ≥2 wiki pages cited, or the user asked to save it.
2. **The question page never holds the answer.** It is a pointer with a one-line
   why-this-matters, so `questions/index.md` stays cheap to scan.
3. **One note per topic.** A repeat question enriches the existing note and adds a
   second question page pointing at it — never a second note.
