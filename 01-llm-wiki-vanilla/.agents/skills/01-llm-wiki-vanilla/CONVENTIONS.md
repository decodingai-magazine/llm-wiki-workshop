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
