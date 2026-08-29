# PAGES — page contracts

One section per page `type`: the frontmatter, the body skeleton, the length
budget, and the **receipt** — the small JSON blob that describes what was
written. In layer 01 the orchestrator writes the pages itself and the receipt is
just the set of facts it must keep in mind for the ingest tail. From layer 02 on,
subagents write the pages and return that receipt literally.

Shared rules (quoted wikilinks, one-sentence `description`, ISO-8601 timestamps,
citation discipline) live in `CONVENTIONS.md` — they are not repeated here.

---

## `source` — `wiki/sources/<slug>.md`

The LLM's reading of exactly one ingested artifact. Written once, from `raw/`.

```markdown
---
type: source
title: <the note's H1, else its filename stem>
description: <ONE sentence — the sharpest gist of this source>
origin: local
original_path: <path as given, relative to the project root>
source_url: null
authors: []
published_date: null
raw_file: raw/<slug>.md
created: <ISO-8601 UTC>
timestamp: <ISO-8601 UTC>
entities:
  - "[[wiki/entities/<slug>]]"
concepts:
  - "[[wiki/concepts/<slug>]]"
---

# <title>

> [[raw/<slug>|Raw]] · local

## Summary

<2–3 paragraphs in the author's own framing — what this note argues, explains or
demonstrates. Not a generic restatement of the topic.>

## Key claims

- <concrete, citable assertion>. [[raw/<slug>#<heading>|cite]]
- ... (3–6 bullets)

## Notable quotes

> "<verbatim, ≤3 sentences>"
> — [[raw/<slug>#<heading>|location]]

## Connections

- **Entities**: [[wiki/entities/<slug>]], ...
- **Concepts**: [[wiki/concepts/<slug>]], ...

> Synthesis: <one line — how this note sits against the rest of the wiki>
```

**Budget** 300–600 words. A thin note gets a thin page; padding is worse than brevity.
**Only the source page may read `raw/`.** Everything downstream reads this page instead.

**Receipt**

```json
{
  "page": "wiki/sources/<slug>.md",
  "original_path": "<path as given>",
  "entities_referenced": ["<slug>"],
  "concepts_referenced": ["<slug>"],
  "suggested_new": [{"kind": "concept", "slug": "<slug>", "name": "<Name>", "why": "<one line>"}]
}
```

`*_referenced` are the slugs actually wikilinked (promissory ones included) —
this is what the ≥2 threshold counts. Be conservative: a passing mention is not
an engagement.

---

## `entity` / `concept` — `wiki/entities/<slug>.md`, `wiki/concepts/<slug>.md`

Same contract, two kinds of subject: an **entity** is a person, tool, company or
framework; a **concept** is an idea, pattern or technique. Written by aggregating
the source-like pages that mention it — **never** by re-reading `raw/`.

```markdown
---
type: <entity|concept>
title: <canonical display name>
description: <ONE sentence definition>
aliases: []
sources:
  - "[[wiki/sources/<slug>]]"
  - "[[wiki/sources/<slug>]]"
related:
  - "[[wiki/concepts/<slug>]]"
created: <ISO-8601 UTC — preserved from the existing page>
timestamp: <ISO-8601 UTC>
source_count: <int>
---

# <name>

> <one-line definition, or "Multiple framings — see Definition">

## Definition

<1–2 paragraphs. Where sources disagree, lay the framings side by side and cite
each one — do not average them into mush.>

## Key claims

- <claim>. [[wiki/sources/<slug>]], [[wiki/sources/<slug>]]
- ...

## Relationships

- **<other page>**: <one line on how they relate>. [[wiki/concepts/<slug>]]

> Synthesis: <one line — how this fits the wiki as a whole>
```

**Budget** 200–500 words.
**Updating an existing page**: preserve `created` and any human-added `aliases`;
merge new claims into the existing structure instead of rewriting from zero.

**Receipt**

```json
{"page": "wiki/concepts/<slug>.md", "action": "created|updated", "source_count": 3}
```

---

## `overview` — `wiki/overview.md`

The one page a newcomer reads first. Navigation, not argument.

```markdown
---
type: overview
title: <slug> — Overview
description: <ONE sentence — what this wiki covers>
created: <ISO-8601 UTC — preserved>
timestamp: <ISO-8601 UTC>
total_sources: <int>
total_pages: <int>
---

# <slug> — Overview

## Themes

<2–4 clusters that the wiki has actually organized around — derived from
co-citation (which pages get cited together), not invented. Each theme: one
short paragraph, 1–3 wikilinked entity/concept pages, and the 1–2 source pages
that make the case best.>

## Index

### Entities (N)
- [[wiki/entities/<slug>]] — <one line>

### Concepts (N)
- [[wiki/concepts/<slug>]] — <one line>

## Health

- Sources: N · Entities: N · Concepts: N
- Slugs at 1 mention (waiting for a second): <slug>, <slug>
```

**Budget** 300–600 words. Written from a **frontmatter walk** plus at most 5 full
page reads:

```bash
for f in wiki-<slug>/wiki/sources/*.md; do awk '/^---$/{c++; next} c==1' "$f"; echo "---END---"; done
```

The "slugs at 1 mention" line is the wiki telling you what it is about to learn —
those are the pages that materialize as soon as one more source arrives.

---

<!-- added in 02 -->

## `repo` — `wiki/repos/github-<owner>-<repo>/ARCHITECTURE.md`

The page that exists so nobody re-reads the clone. Written by `repo_writer` in
`architecture` mode; a **source-like page**, so its `entities:` / `concepts:`
count toward the ≥2 threshold.

```markdown
---
type: repo
title: <repo>
description: <ONE sentence — what this codebase is and does>
original_path: github://<owner>/<repo>
source_url: https://github.com/<owner>/<repo>/tree/<commit_sha>
repo_url: https://github.com/<owner>/<repo>
commit_sha: <full sha>
branch: main
clone_path: raw/repos/.github-<owner>-<repo>
created: <ISO-8601 UTC>
timestamp: <ISO-8601 UTC>
entities: []
concepts: []
---

# <repo> — Architecture

> Clone: `raw/repos/.github-<owner>-<repo>/` · [<owner>/<repo>](<repo_url>) @ `<sha[:7]>`

(The clone is a *directory*, so it is shown as a path, not a wikilink — a wikilink to a
directory does not resolve in Obsidian.)

> Scope: <one sentence — what this page covers and what it deliberately skips>

## 1. Bird's-eye view

<1–2 paragraphs, then a mermaid flowchart of the whole system.>

## 2. Layout

<Top-level directories, one line each. Plain bullets — this is a map, not prose.>

## 3. Entry flow

<How the program starts and dispatches. Mermaid flowchart.>

## 4. Core loop

<The subsystem that makes this codebase what it is. Mermaid sequenceDiagram.>

## 5–6. <One or two more subsystems that earn a section>

## Reading order

1. `<file>` — <why start here>
2. ...

## Connections

- **Entities**: [[wiki/entities/<slug>]], ...
- **Concepts**: [[wiki/concepts/<slug>]], ...

> Synthesis: <one line — what this codebase demonstrates that the notes only assert>
```

**Budget** ≤300 lines, 4–6 numbered sections, code snippets ≤20 lines with
commit-pinned permalinks (`.../blob/<sha>/<path>#L10-L28`).
**Scope** `src/` + `README` + `docs/`; skip `assets/`, `tests/`, `evals/` unless a
section is unreadable without them.
**Receipt** identical to `§ source`, with `original_path: github://<owner>/<repo>`.
