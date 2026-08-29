---
name: 01-llm-wiki-vanilla
description: "Build and query a minimal LLM-maintained wiki from local markdown notes (modes: ingest, query)."
---

# LLM Wiki — layer 01, vanilla

You maintain a small wiki that an LLM writes and an LLM reads. Notes go in; a
navigable, cited, compounding knowledge base comes out. This layer has **no
subagents and no scripts beyond two frontmatter walkers** — you do every read and
every write yourself, so the whole mechanic is visible in one context.

Two files carry the contract, and you follow them exactly:

- `CONVENTIONS.md` — layout, identity, threshold, links, log, OKF alignment.
- `PAGES.md` — the template and receipt for every page type.

Read both before your first write in a session.

---

## Step 0 — Locate the wiki

Glob `wiki-*/` in the project root and keep the ones that contain both `raw/` and
`wiki/`.

| Found | Do |
|---|---|
| exactly 1 | Use it. |
| more than 1 | Ask the user which one. |
| 0, ingest mode | Propose a slug from the topic of the incoming notes (kebab-case, e.g. `ai-engineering`), confirm it with the user, then create the wiki. |
| 0, query mode | Say there is no wiki yet and stop. Do not create one to answer a question. |

Creating a wiki:

```bash
mkdir -p wiki-<slug>/raw wiki-<slug>/wiki/sources wiki-<slug>/wiki/entities wiki-<slug>/wiki/concepts
printf '# Log\n' > wiki-<slug>/log.md
```

## Step 1 — Detect mode

**Ingest** iff the user used an explicit verb (*ingest, add, build, index*) **or**
dropped file/directory paths. Everything else is **query**.

When it is ambiguous, choose **query**. Redirecting a query is cheap; a
mis-triggered ingest writes files the user did not ask for.

---

# Ingest path

You do this inline. No subagents in this layer — that is the lesson it teaches.

### 1.1 Collect inputs and dedup

Expand every path the user gave you:

- a directory → **recursively every `*.md` inside it**. An `assets/` folder is not
  a list of inputs — nothing inside it becomes a source. Its files travel later,
  in 1.2, as attachments of the notes that embed them.
- a file → itself.

For each input compute its raw path — `raw/<slug>.md`, where `<slug>` is the
**filename stem**, slugified: lowercase, every run of non-alphanumeric characters
collapsed to a single `-`, leading/trailing `-` stripped, truncated to 60
characters at a `-` boundary.

Then split the inputs (this is the whole of dedup — see `CONVENTIONS.md` §4):

```bash
ls wiki-<slug>/raw/          # everything already ingested, by identity
```

- raw path exists → **skipped**. Report the note by name plus the
  `original_path` recorded on its existing source page. If the incoming file
  differs in content from `raw/`, say so explicitly and still skip.
- raw path free → **new**.

> **Cap: if `new` is more than 10, stop and write nothing.** Report the count and
> say why in one sentence: this layer reads every note into a single context, so
> a large batch blows past what one context can hold *and* what a reader can
> follow. Point at a smaller batch (`../data_input_examples/notes/02-medium/`
> fits exactly) and at layer 02, which removes the cap by fanning the work out to
> one subagent per note. Do not partially ingest, and do not write a log entry —
> a run that wrote nothing did not happen.

### 1.2 Copy the raw layer

```bash
cp "<input path>" "wiki-<slug>/raw/<slug>.md"
```

Copy verbatim — no reformatting, no frontmatter, no cleanup. Note each file's
`original_path` (the path as given, normalized relative to the project root) and
its title (first H1 in the file, else the filename stem); you need both in 1.3.

**Then copy the note's attachments.** Scan the copied note for embeds and
attachment links — `![[assets/…]]` and `[[assets/…|label]]` — and for each one copy
the file from the note's sibling `assets/` folder into `raw/assets/`, keeping the
filename:

```bash
mkdir -p "wiki-<slug>/raw/assets"
cp "<dir of the input note>/assets/<file>" "wiki-<slug>/raw/assets/<file>"   # skip if it exists
```

Because `raw/assets/` sits beside `raw/<slug>.md`, the embed in the copy resolves
exactly as it did in the source folder — you never rewrite a link, and `raw/`
stays verbatim. Attachments are payload, not sources (`CONVENTIONS.md` §4): they
get no page and never count toward the threshold. Report them as a count, not by
name.

### 1.3 Write one source page per new raw file

For each new raw file: read it, then write `wiki/sources/<slug>.md` following
`PAGES.md § source`. Keep each page's receipt fields — the entity and concept
slugs you referenced — in your working notes; step 1.4 needs them.

Before you start, list the pages that already exist so you reuse their canonical
slugs instead of inventing near-duplicates:

```bash
ls wiki-<slug>/wiki/entities wiki-<slug>/wiki/concepts
```

Be conservative about what you link. Every slug you write is a claim that this
note *engages* with that idea, and two such claims materialize a page.

### 1.4 Ingest tail — entity and concept pages

```bash
uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/count_mentions.py --wiki-dir wiki-<slug>
```

The `qualifying` lists are the slugs at ≥2 distinct source-like pages. Write or
update a page for every qualifying slug **that one of this run's new source pages
touched** — a slug that was already qualifying and that no new page mentions has
not changed, so leave its page alone.

Read only the source pages listed for that slug in the script output. **Never
open `raw/` here.** Follow `PAGES.md § entity / concept`; preserve `created` and
any human-added `aliases` when updating.

### 1.5 Rewrite the overview

Rewrite `wiki/overview.md` per `PAGES.md § overview`, from a frontmatter walk
plus at most 5 full page reads.

### 1.6 Rebuild the index

```bash
uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/build_index_md.py --wiki-dir wiki-<slug>
```

Fix anything it reports as an `ERROR:` (a page with no `type`) before moving on.

### 1.7 Append to the log

```markdown
## <YYYY-MM-DD> ingest | <what came in>

- Ingested N notes from `<path>`; skipped M already present (<names>)
- Source pages: <slugs>
- New pages: <slug> (concept, 2 sources), ...
- Updated pages: <slug> (2 → 3 sources), ...
- Waiting at 1 mention: <slug>, <slug>
```

### 1.8 Report back

New and skipped counts, the pages you wrote, the wiki path, and one line telling
the user to open `wiki-<slug>/wiki/index.md` in Obsidian. If any slug is sitting
at exactly 1 mention, name a couple — that is the wiki's own to-do list.

---

# Query path

Read-only. The only file query mode writes in this layer is `log.md`.

- **Q.1 — Locate** the wiki (Step 0).
- **Q.2 — Load the map.** Read `wiki/index.md`, then the one or two
  `wiki/<subdir>/index.md` files that look relevant. Each bullet is a
  `title — description`; that is enough to choose.
- **Q.3 — Read 1–3 pages.** Prefer entity/concept pages (already synthesized)
  over source pages (single-note views).
- **Q.4 — Escalate only if you must.** If the wiki pages genuinely do not answer
  the question, read the specific `raw/` file a source page points to. Never bulk
  read `raw/`. If the wiki simply does not know, **say so** — a wiki that
  hallucinates coverage is worse than an empty one.
- **Q.5 — Answer** with `[[wikilinks]]` to every page you used, and end with a
  `Pages used:` list. Distinguish what the notes claim from what you inferred.
- **Q.6 — Log it**:

```markdown
## <YYYY-MM-DD> query | <topic>

- question: "<verbatim, ≤200 chars>"
- pages used: <count> (<slugs>)
- gap noticed: <one line, or omit>
```

---

## Harness notes

This skill is written for any agent harness. It needs four capabilities:

| Capability | Used for |
|---|---|
| read a file | raw notes, wiki pages |
| write a file | every page you create |
| run a shell command | `cp`, `ls`, `mkdir`, the two scripts |
| ask the user | the wiki slug, which wiki to use |

In Claude Code those are `Read`, `Write`, `Bash`, and `AskUserQuestion`. Nothing
in this skill pins a model or a tool name; layer 02 keeps the same discipline
when it starts spawning subagents.

## Script reference

Both scripts are PEP 723 single files — `uv` installs their dependencies on the
first run. Paths below are relative to the layer directory.

| Script | Call | Does |
|---|---|---|
| `scripts/count_mentions.py` | `uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/count_mentions.py --wiki-dir wiki-<slug>` | Frontmatter walk over source-like pages → `{slug: [pages]}` + the `qualifying` list at ≥2. JSON on stdout, table on stderr. |
| `scripts/build_index_md.py` | `uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/build_index_md.py --wiki-dir wiki-<slug>` | Regenerates `wiki/index.md` and each `wiki/<subdir>/index.md` from frontmatter, then checks OKF conformance. Deterministic: same input, same bytes. |

Neither script writes content. They count and they render — every word in the
wiki is written by you.
