# LLM Wiki Workshop — Implementation Plan

Reference implementation: `/Users/pauliusztin/Documents/01-Projects/scrabble/scrabble/plugins/scrabble/skills/wiki-research` (the "scrabble skill"). This workshop is a **stripped-down, three-layer teaching version** of that skill. Reuse its ideas, page contracts and script logic freely; do NOT reuse its complexity. When this plan and scrabble disagree, this plan wins.

Audience: 1-hour workshop, entry/mid-level AI engineers who know Claude Code or a similar harness. Every file must be readable in one sitting. If a rule doesn't earn its place in 1 hour, cut it.

---

## 0. Decisions log (already settled — do not re-litigate)

| # | Decision |
|---|---|
| Packaging | No plugin. Each layer is a self-contained project dir. Skills live in `.agents/skills/`, with a committed symlink `.claude/skills -> ../.agents/skills`. |
| Layers | `01-llm-wiki-vanilla/`, `02-llm-wiki-ingest/`, `03-llm-wiki-interactive/`. Each is a **full superset** of the previous. Unchanged files are byte-identical across layers. New logic goes in **new files** where possible; each layer ≥02 ships `CHANGES-FROM-PREVIOUS.md`. |
| Skill per layer | One skill each: `/01-llm-wiki-vanilla`, `/02-llm-wiki-ingest`, `/03-llm-wiki-interactive`. Each supports **ingest** and **query** modes via mode detection (scrabble Step 0 style, default to query). |
| Harness-agnostic | Subagent logic lives in `agents/*.md` files under the skill (scrabble hack). SKILL.md instructs *the harness* to spawn a subagent with whatever mechanism it has and inline the agent file body as the prompt. No Claude-Code-only frontmatter pins. Model preference stated in prose (Sonnet-class, with fallback to the provider's equivalent tier). |
| Wiki location | One wiki per project: `wiki-<slug>/` in the project root, slug chosen by the user at init. Everything (`raw/`, `wiki/`, `log.md`) lives under it. |
| Viewer | Obsidian. `[[wikilinks]]` everywhere. Clone dirs are dot-prefixed so Obsidian ignores them with zero config. |
| Index | No `index.yaml`. Frontmatter is canonical; `index.md` files are a derived cache built by a script. Keep OKF alignment (`okf_version: "0.1"`, nested per-subdir `index.md`, reserved filenames, `type` on every page) — it is a teaching point. |
| Pages kept | `sources/`, `entities/`, `concepts/`, `overview.md`, `log.md`, generated `index.md`s. 02 adds `repos/`. 03 adds `questions/`, `notes/`, `open-questions.md`. |
| Pages dropped | synthesis, comparisons, contradictions, renders, supersession/`status`, `<!-- KEEP -->` markers, relevance scores, assets/images, PDFs, Layer-2 highlights, research rounds/researcher/gap analyzer/dedup, discussion checkpoint, GitHub star discovery, module mode, `github_parse_targets`. |
| Threshold | Entity/concept page materializes when mentioned by **≥2 distinct source-like pages**. Promissory (forward) wikilinks allowed with strict slug discipline. |
| Append | Supported from 01. **Identity = the raw artifact path** (`raw/<slug>.md` for local notes, `raw/article-<slug>.md` for articles, `raw/repos/.github-<owner>-<repo>/` for repos); if it already exists the input is skipped with a message (no overwrite consent flow). `original_path` is provenance, not identity — the same note reached via two paths (the nested scenario dirs) is one source. Repos are the exception: re-ingest = explicit refresh. |
| 01 = no subagents | Orchestrator reads raw and writes every page inline. Hard cap **10 new sources per run**, with the reason stated. The cap is tuned to the fixture: `02-medium` (10) fits exactly, `03-hard` (50) trips it — that is the hand-off to 02. |
| 02 = fan-out + sources | Page writing moves into `agents/`. Adds repo adapter (clone + architecture doc), article adapter (curl + markdownify), YouTube **skeleton** adapter (`NotImplementedError`), and `SOURCES.md` explaining how to add X/LinkedIn/Reddit/etc. |
| Repos | Raw = the shallow clone at `raw/repos/.github-<owner>-<repo>/` (hidden, `--depth 1`). Curated docs at `wiki/repos/github-<owner>-<repo>/ARCHITECTURE.md` (`type: repo`) — written by `repo_writer`, which emits the same frontmatter contract + receipt as `source_writer` so repos feed entities/concepts. Dedup ID `github://<owner>/<repo>` (no SHA). Sonnet, ≤300 lines, 4–6 sections, scoped to `src/` + `README` + `docs/`. |
| 03 = interaction | Question log (`wiki/questions/`, slim pointers), knowledge notes (`wiki/notes/`), `wiki/open-questions.md`. Repo questions → `repo_writer` in `question` mode → `wiki/repos/<repo>/<slug>.md` (`type: repo_note`) → **ingest tail** re-runs (recount, pages, overview, index, log). General notes are never re-ingested. Spawn the repo agent only when the answer needs code beyond ARCHITECTURE.md. |
| Save policy (03) | Always write the slim question page. Write/enrich a note only when the answer cites ≥2 wiki pages or the user says "save". |
| Open questions (03) | Triggers: user flags one; wiki can't answer. Append-only. Next ingest reports which ones the new sources appear to address (no auto-resolve). |
| Fixture | `data_input_examples/` at repo root (already populated). `notes/{01-easy,02-medium,03-hard}/` are **nested scenarios** (5 ⊂ 10 ⊂ 50 AI-Engineering notes), each with its own `assets/` holding the files its notes embed (sibling paths, so the links resolve from any vault root; +1.2 MB over a shared folder); `github_repositories.md` and `substack_articles.md` hold the 02+ targets. Layer 01's demo ingests `01-easy/`; layer 02's starts from scratch on `02-medium/` and optionally finishes with `03-hard/` (40 new, 10 skipped by raw path). The scenario table lives in the root README (the only README in the repo). |
| Demo targets | Listed in `data_input_examples/github_repositories.md` (repo: `https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course` — 526 files, `src/` = 82 Python files, ~40 MB of GIFs in `assets/`) and `data_input_examples/substack_articles.md` (`https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design`, `https://www.decodingai.com/p/the-coding-agent-loop`). Demos and READMEs reference the link files, not hard-coded URLs, so swapping targets is a one-file edit. |
| Prereqs | Python ≥3.12 + `uv` (scripts are PEP 723, run with `uv run --script`), `git`, `curl`, Obsidian optional. No `gh`. |
| Git hygiene | Live runs (`wiki-*/` in each layer root) are gitignored. `examples/` holds one committed reference run per layer (without `raw/repos/` or `raw/assets/`): 01 = `01-easy` end state, 02 = `03-hard` + repo + articles, 03 = a copy of 02 — the 03 demo's start point, with nothing asked of it yet. |

---

## 1. Repository layout

```
llm-wiki-workshop/
├── README.md                          # the ONLY README: what an LLM wiki is, prereqs, how to run, inputs, one tight section per layer
├── implementation_plan.md             # this file
├── .gitignore                         # + rules in §8
├── data_input_examples/               # fixture (populated)
│   ├── github_repositories.md                # repo URLs for 02+ (currently 1)
│   ├── substack_articles.md              # article URLs for 02+ (currently 2)
│   └── notes/
│       ├── <tier>/assets/             # images/.srt embedded via ![[assets/…]]; per tier; copied into raw/assets/ on ingest, never a source
│       ├── 01-easy/                   # 5 notes  — MCP vs. skills vs. CLIs cluster
│       ├── 02-medium/                 # 10 notes — easy + context layer / agent memory / GraphRAG / harness architecture
│       └── 03-hard/                   # 50 notes — everything (incl. tiny + noisy notes)
├── 01-llm-wiki-vanilla/
│   ├── demo.md                        # exact prompts to type + expected outcomes (verification checklist)
│   ├── .claude/skills -> ../.agents/skills      # symlink (committed)
│   ├── .agents/skills/01-llm-wiki-vanilla/
│   │   ├── SKILL.md                   # orchestrator: mode detection, locate, ingest (inline), query
│   │   ├── CONVENTIONS.md             # data contract (layout, frontmatter, links, log, OKF, regimes)
│   │   ├── PAGES.md                   # page templates + frontmatter per type; used inline in 01, by agents in 02+
│   │   └── scripts/
│   │       ├── build_index_md.py      # frontmatter walk → wiki/index.md + wiki/<subdir>/index.md (deterministic)
│   │       └── count_mentions.py      # frontmatter walk over source-like pages → {slug: [pages]} for the ≥2 threshold
│   └── examples/wiki-ai-engineering/  # committed reference run
├── 02-llm-wiki-ingest/
│   ├── CHANGES-FROM-PREVIOUS.md       # what moved into agents and why; new origins; new scripts
│   ├── demo.md
│   ├── .claude/skills -> ../.agents/skills
│   ├── .agents/skills/02-llm-wiki-ingest/
│   │   ├── SKILL.md                   # + routing step, spawn paragraph, fan-out; cap removed
│   │   ├── CONVENTIONS.md             # + repos layout, origin prefixes, repo refresh rule
│   │   ├── PAGES.md                   # + repo page contract
│   │   ├── SOURCES.md                 # adapter contract, routing table, per-origin recipes, "how to add a source"
│   │   ├── agents/
│   │   │   ├── source_writer.md       # one raw file → one wiki/sources page + receipt
│   │   │   ├── page_writer.md         # one entity/concept page from its source-like pages
│   │   │   ├── overview_writer.md     # wiki/overview.md from frontmatter
│   │   │   └── repo_writer.md         # mode: architecture (02) | question (03, present but unused in 02)
│   │   └── scripts/
│   │       ├── build_index_md.py      # unchanged from 01 except: recurses wiki/repos/<repo>/
│   │       ├── count_mentions.py      # unchanged except: includes wiki/repos/*/*.md
│   │       ├── clone_repo.py          # shallow clone / refresh → JSON receipt
│   │       ├── fetch_article.py       # curl → metadata + body isolation → markdownify → raw/article-<slug>.md
│   │       └── fetch_youtube.py       # skeleton: argparse + docstring contract + raise NotImplementedError
│   └── examples/wiki-ai-engineering/
└── 03-llm-wiki-interactive/
    ├── CHANGES-FROM-PREVIOUS.md
    ├── demo.md
    ├── .claude/skills -> ../.agents/skills
    ├── .agents/skills/03-llm-wiki-interactive/
    │   ├── SKILL.md                   # query mode gains save-back + repo path + open questions; ingest gains open-questions check
    │   ├── CONVENTIONS.md             # + interaction-owned pages, three write regimes, ingest tail
    │   ├── PAGES.md                   # + question, note, repo_note, open_question contracts
    │   ├── QUERY.md                   # Q.1–Q.8: locate, load index, disclosure ladder, answer, save-back, repo path, open questions, log
    │   ├── SOURCES.md                 # unchanged
    │   ├── agents/                    # unchanged except repo_writer question mode is now wired
    │   └── scripts/                   # build_index_md.py + count_mentions.py: + questions/, notes/ subdirs; others unchanged
    └── examples/wiki-ai-engineering/
```

Rule for superset-ness: when a file changes between layers, keep the change minimal and mention it in `CHANGES-FROM-PREVIOUS.md` with the exact section names touched. Prefer adding a new file + a one-line pointer in SKILL.md over rewriting SKILL.md sections.

---

## 2. Shared data contract (`CONVENTIONS.md`)

Write it once for 01; 02 and 03 append sections (marked `<!-- added in 02 -->` / `<!-- added in 03 -->` so the diff is visible in-file too).

### 2.1 Wiki directory layout (final, 03 shape; earlier layers omit the later parts)

```
wiki-<slug>/
├── log.md                                  # append-only; OKF reserved filename
├── raw/                                    # immutable copies of what was ingested
│   ├── <slug>.md                           # local note, copied verbatim (01+)
│   ├── article-<slug>.md                   # fetched article, frontmatter written by fetch_article.py (02+)
│   └── repos/
│       └── .github-<owner>-<repo>/         # shallow clone, hidden from Obsidian; regenerable; refreshed on re-ingest (02+)
└── wiki/                                   # the OKF bundle — every .md here carries a non-empty `type`
    ├── index.md                            # GENERATED bundle root; carries okf_version: "0.1"
    ├── overview.md                         # type: overview
    ├── sources/
    │   ├── index.md                        # GENERATED
    │   └── <slug>.md                       # type: source (one per raw file)
    ├── entities/  { index.md, <slug>.md }  # type: entity   (≥2 threshold)
    ├── concepts/  { index.md, <slug>.md }  # type: concept  (≥2 threshold)
    ├── repos/                              # (02+)
    │   ├── index.md                        # GENERATED — lists every page under every repo dir
    │   └── github-<owner>-<repo>/
    │       ├── ARCHITECTURE.md             # type: repo
    │       └── <question-slug>.md          # type: repo_note (03+)
    ├── questions/ { index.md, YYYY-MM-DD-<slug>.md }   # type: question (03+)
    ├── notes/     { index.md, <slug>.md }              # type: note (03+)
    └── open-questions.md                   # type: open_question, rolling (03+)
```

### 2.2 Three-layer progressive disclosure (read order for any agent)

1. `wiki/index.md` → the relevant `wiki/<subdir>/index.md` (navigation: one `title — description` bullet per page)
2. the wiki page (source / entity / concept / repo)
3. `raw/` — only when the wiki page is insufficient; never bulk-read raw.

### 2.3 Source-like pages and the threshold

"Source-like page" = any page under `wiki/sources/` (01+) or `wiki/repos/*/` (02+). Each lists the slugs it substantively engages with in frontmatter `entities:` / `concepts:` as quoted wikilinks. An entity/concept page exists iff ≥2 distinct source-like pages list it. `count_mentions.py` is the single source of truth for that count. Promissory links: a source-like page may link `[[wiki/concepts/<slug>]]` before the page exists; Obsidian shows a hollow node; slug discipline (lowercase kebab-case, ASCII, ≤60 chars, the slug the eventual page will use) is mandatory.

### 2.4 Identity and dedup

**Identity = the raw artifact path.** Every adapter maps its input to a deterministic path under `raw/`; if that path already exists, the input has been ingested:
- local note: `raw/<slug>.md`, slug from the filename stem (so `notes/01-easy/foo.md` and `notes/02-medium/foo.md` are the same source — the scenario dirs are nested on purpose)
- article: `raw/article-<slug>.md`, slug from the last URL path segment
- repo: `raw/repos/.github-<owner>-<repo>/`
- repo_note: no raw artifact; identity is its wiki path `wiki/repos/<repo>/<question-slug>.md`

`original_path` on every source-like page records **provenance**, not identity: the path as given (normalized relative to the project root, e.g. `data_input_examples/notes/01-easy/foo.md`), the article URL, `github://<owner>/<repo>` (SHA in its own field), or `github://<owner>/<repo>#<question-slug>`.

Before ingesting, compute each input's raw path and `ls` it — no frontmatter walk needed. Existing → skipped and reported (with the existing `original_path` so the user sees where it came from). Same slug but different content → still skipped, with a warning naming both paths (rename the file to ingest it). Repos are refreshed instead of skipped (see 2.7).

### 2.5 Frontmatter rules

- Every wiki page: `type`, `title`, `description` (ONE sentence — it is the only thing the index shows), `created` (preserved across rewrites), `timestamp` (last meaningful change).
- Wikilinks in YAML are always quoted: `- "[[wiki/sources/foo]]"`. Bare `[[..]]` breaks YAML parsers.
- No `tags` field anywhere. Cross-cutting topics are concept pages reached by links.
- Full per-type contracts live in `PAGES.md` (§3).

### 2.6 Linking and citations

- Wiki ↔ wiki and wiki → raw use `[[wikilinks]]` (paths relative to `wiki-<slug>/`, no extension). External: normal markdown links.
- Every claim on a source page cites the raw file (`[[raw/<slug>#<heading>|cite]]`); every claim on an entity/concept page cites a source-like page. LLM judgment is marked `> Synthesis:`. Citations must resolve; only cross-reference links may be promissory.

### 2.7 Immutability and write regimes

- `raw/` is immutable. Exception: `raw/repos/.github-*` is a regenerable cache — re-ingesting a repo runs `git fetch` + `reset --hard`, rewrites `ARCHITECTURE.md`, bumps `commit_sha`, and re-runs the ingest tail. Deleting the clone dir is always safe.
- `wiki/` is LLM-owned. Humans edit it only deliberately.
- All `index.md` files are generated; never hand-edited. `log.md` is append-only, oldest-first.
- 03 adds the three regimes: **ingest-owned** (`raw/`, `sources/`, `entities/`, `concepts/`, `overview.md`, `repos/*/ARCHITECTURE.md`), **interaction-owned** (`questions/`, `notes/`, `open-questions.md`), and **repo notes** (`repos/*/<slug>.md`, added in query mode and then fed through the ingest tail). Query mode never edits an ingest-owned page directly.

### 2.8 The ingest tail (named once, reused everywhere)

After any new source-like page lands: `count_mentions.py` → write/update every entity/concept page whose slug is ≥2 AND is referenced by a new page → rewrite `overview.md` → `build_index_md.py` → append `log.md`. 01 does this inline; 02+ via agents; 03's repo-question path calls the same tail.

### 2.9 `log.md`

```
## YYYY-MM-DD <op> | <subject>
- 2–8 bullets: what was added/skipped, pages written, decisions
```
`<op>` ∈ `ingest`, `query`. Create with `# Log` header on init. Greppable: `grep -E '^## [0-9]{4}-' log.md`.

### 2.10 OKF alignment (teaching section — keep it to ~15 lines)

`wiki/` is an Open Knowledge Format v0.1 bundle: markdown concept documents with YAML frontmatter, path = identity, every non-reserved file carries `type`, `index.md` and `log.md` are reserved navigation/history files, the bundle root `wiki/index.md` declares `okf_version: "0.1"`. Frontmatter is canonical and the index is a rebuildable cache. We diverge on purpose: Obsidian `[[wikilinks]]` instead of relative markdown links, and an oldest-first append-only log. `build_index_md.py` runs a conformance check (missing `type`/`description` → warning list on stderr, non-zero exit only on missing `type`).

---

## 3. Page contracts (`PAGES.md`)

One section per type: frontmatter block + body skeleton + length budget + the receipt JSON the writer returns (used by agents in 02+; in 01 the orchestrator just keeps the same fields in mind). Keep each template ≤40 lines. Derive from scrabble's `source_writer.md` / `wiki_page_writer.md` / `wiki_summary_writer.md` (overview only) but trimmed as below.

### source (`wiki/sources/<slug>.md`)
Frontmatter: `type: source`, `title`, `description`, `origin: local | article | youtube`, `original_path` (provenance, §2.4), `source_url` (null for local), `authors: []`, `published_date` (null ok), `raw_file: raw/<file>`, `created`, `timestamp`, `entities: []`, `concepts: []`.
Body: `# title` → `> [[raw/<slug>|Raw]] · origin` → `## Summary` (2–3 paragraphs, author's framing) → `## Key claims` (3–6 bullets, each `[[raw/...#heading|cite]]`) → `## Notable quotes` (≤3, verbatim) → `## Connections` (Entities / Concepts wikilink lists) → `> Synthesis:` one line. Budget 300–600 words.
Receipt: `{"page": path, "original_path", "entities_referenced": [slugs], "concepts_referenced": [slugs], "suggested_new": [{"kind": "entity|concept", "slug", "name", "why"}]}`.

### entity / concept (`wiki/entities|concepts/<slug>.md`)
Frontmatter: `type`, `title`, `description`, `aliases: []`, `sources: ["[[...]]"]` (source-like pages), `related: ["[[...]]"]`, `created`, `timestamp`, `source_count`.
Body: `# name` → `> one-line definition` → `## Definition` → `## Key claims` (each cites a source-like page) → `## Relationships` → `> Synthesis:`. Budget 200–500 words. No Tensions/Open-questions sections (dropped).
Receipt: `{"page", "action": "created|updated", "source_count"}`.

### overview (`wiki/overview.md`)
Frontmatter: `type: overview`, `title`, `description`, `created`, `timestamp`, `total_sources`, `total_pages`.
Body: `# <slug> — Overview` → `## Themes` (2–4 clusters from co-citation, each links 1–3 pages + 1–2 sources) → `## Index` (Entities / Concepts / Repos [02+] one-liners) → `## Health` (counts). Budget 300–600 words. Reads frontmatter only + ≤5 full pages.

### repo (`wiki/repos/github-<owner>-<repo>/ARCHITECTURE.md`) — 02+
Frontmatter: `type: repo`, `title: <repo>`, `description`, `original_path: github://<owner>/<repo>`, `source_url: https://github.com/<owner>/<repo>/tree/<sha>`, `repo_url`, `commit_sha`, `branch`, `clone_path: raw/repos/.github-<owner>-<repo>`, `created`, `timestamp`, `entities: []`, `concepts: []`.
Body (≤300 lines): `# <repo> — Architecture` → `> Source @ sha[:7]` → `## 1. Bird's-eye view` (mermaid flowchart) → `## 2. Layout` (top-level dirs, plain bullets) → `## 3. Entry flow` (mermaid) → `## 4. Core loop` (mermaid sequenceDiagram) → `## 5–6. <one or two key subsystems>` → `## Reading order` → `## Connections` (Entities/Concepts) → `> Synthesis:`. Code snippets ≤20 lines, permalinks pinned to `commit_sha`. Same receipt shape as source.

### repo_note (`wiki/repos/github-<owner>-<repo>/<question-slug>.md`) — 03+
Frontmatter: `type: repo_note`, `title`, `description`, `original_path: github://<owner>/<repo>#<question-slug>`, `repo: "[[wiki/repos/github-<owner>-<repo>/ARCHITECTURE]]"`, `commit_sha`, `question` (verbatim), `spawned_by_question: "[[wiki/questions/...]]"`, `created`, `timestamp`, `entities: []`, `concepts: []`.
Body: `# <title>` → `> Answers [[question page]] against <repo> @ sha` → `## Answer` (prose + ≤2 mermaid if structural) → `## Evidence` (file:line bullets with permalinks) → `## Connections` → `> Synthesis:`. ≤200 lines. Same receipt shape as source.

### question (`wiki/questions/YYYY-MM-DD-<slug>.md`) — 03+
Frontmatter: `type: question`, `title` (verbatim question), `description`, `asked_on`, `timestamp`, `answer_doc` (wikilink or null), `sources_cited: []`.
Body ≤25 lines: `# question` → `> Asked on … using N pages` → `## Answer` (if `answer_doc`: "Full answer at [[...]]" + 3–6 bullets; else a ≤5-line inline summary) → `## Why this matters` (1 sentence). No diagrams/code/citations here.

### note (`wiki/notes/<slug>.md`) — 03+
Frontmatter: `type: note`, `title`, `description`, `created`, `timestamp`, `spawned_by_question: ["[[...]]"]`, `sources: []`, `related: []`.
Body: `# title` → answer body with per-claim citations to wiki pages, mermaid welcome → `> Synthesis:`. Idempotent: same-topic note → enrich in place, append to `spawned_by_question`.

### open_question (`wiki/open-questions.md`) — 03+
Frontmatter: `type: open_question`, `title: Open questions`, `description`, `timestamp`. Body: `# Open questions` + dated `## YYYY-MM-DD` sections, each bullet `- <question> — from [[wiki/questions/...]]` (or "flagged by user"). Append-only; refresh `timestamp` on append.

---

## 4. Layer 01 — `/01-llm-wiki-vanilla`

**Goal:** show the whole LLM-wiki mechanic with zero moving parts: raw copy → source page → threshold → entity/concept pages → overview → generated index → log. Then query it with the disclosure ladder.

### 4.1 SKILL.md (target ≤250 lines)

Frontmatter: `name: 01-llm-wiki-vanilla`, `description: Build and query a minimal LLM-maintained wiki from local markdown notes (modes: ingest, query).`

Sections:
1. **What this is** (5 lines) + link to `CONVENTIONS.md`/`PAGES.md`.
2. **Step 0 — Locate the wiki.** Glob `wiki-*/` in the project root that contain both `raw/` and `wiki/`. 0 → if ingest: ask for a slug (suggest one from the notes' topic), create `wiki-<slug>/{raw,wiki/{sources,entities,concepts}}` + `log.md`; if query: say there is no wiki yet. 1 → use it. >1 → ask.
3. **Step 1 — Detect mode.** Ingest iff the user used an explicit verb (ingest/add/build/index) OR dropped file/dir paths. Otherwise query. When ambiguous, query (cheap to redirect; mis-ingest is not).
4. **Ingest path (inline — no subagents).**
   - 1.1 Collect inputs: files and dirs (dirs → recursive `*.md`; everything else, e.g. `assets/`, is ignored). Compute each input's `raw/<slug>.md` path (§2.4); split into `new` / `skipped`. **Cap: if `new` > 10, stop and write nothing** — name the count, explain in one sentence that this layer reads everything in one context and 02 removes the cap with fan-out, and suggest a smaller batch (`data_input_examples/notes/02-medium/` fits exactly).
   - 1.2 Copy each new note to `raw/<slug>.md` (`cp`, slug from filename stem; title from first H1 else filename). Record the given path as `original_path`.
   - 1.3 For each new raw file: read it, write `wiki/sources/<slug>.md` per `PAGES.md § source`. Keep the receipt fields in your notes.
   - 1.4 Ingest tail: run `count_mentions.py`; for every slug with ≥2 pages that appears in any new receipt, read its source pages (never raw) and write/update the entity/concept page per `PAGES.md`; preserve `created` and user-added aliases when updating.
   - 1.5 Rewrite `overview.md` (frontmatter walk + ≤5 full reads).
   - 1.6 `uv run --script scripts/build_index_md.py --wiki-dir wiki-<slug>`.
   - 1.7 Append `log.md` (`ingest`).
   - 1.8 Report: new/skipped counts, pages written, path, "open `wiki/index.md` in Obsidian".
5. **Query path.** Q.1 read `wiki/index.md` → Q.2 open the relevant subdir index → Q.3 read 1–3 pages → Q.4 escalate to `raw/` only if a page doesn't answer → Q.5 answer with `[[wikilinks]]` and a "Pages used" list → Q.6 append `log.md` (`query`). Nothing else is written in 01.
6. **Harness notes** (5 lines): tools are described generically (read file / run shell / ask user); a Claude Code footnote maps them.

### 4.2 Scripts (PEP 723 headers, `uv run --script`)

- `build_index_md.py --wiki-dir <wiki-<slug>>` — port of scrabble's `build_index_md.py` minus everything about `index.yaml`. Walks `wiki/`, writes `wiki/index.md` (frontmatter `okf_version: "0.1"` + autogenerated comment, links `overview`, each subdir index with counts, and in 03 `open-questions`) and `wiki/<subdir>/index.md` (no frontmatter; `- [[wiki/<subdir>/<slug>|<title>]] — <description>` sorted by slug). Subdirs in 01: `sources`, `entities`, `concepts`. Deterministic; byte-stable. Conformance check as in §2.10. Dep: `pyyaml`.
- `count_mentions.py --wiki-dir <wiki-<slug>> [--json]` — walks source-like pages, parses `entities`/`concepts` wikilinks, prints `{"entities": {"<slug>": ["wiki/sources/a", ...]}, "concepts": {...}}` plus a human table on stderr. Dep: `pyyaml`. In 01 covers `wiki/sources/` only.

### 4.3 demo.md (the layer's section in the root README carries goal, key idea, prompts, what to look at)

`demo.md` prompts — one or two checks after each, never a script for the user to run (the skill runs its own scripts; everything else is verified by eye or in Obsidian). All paths relative to `01-llm-wiki-vanilla/`.
1. `/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/` → asks slug → `wiki-ai-engineering/` created; 5 source pages; a page for every slug ≥2 notes engage with and nothing else (reference run: 4 entities, 5 concepts, 3 waiting at 1); overview; index files; log has 1 entry.
2. `/01-llm-wiki-vanilla what do my notes say about when to use an MCP server vs. a CLI?` → answer with wikilinks and a `Pages used:` line; nothing written except `log.md`.
3. Open `wiki-ai-engineering/` in Obsidian → hub-and-spoke around concept pages; hollow nodes = promissory links; the embedded image renders from `raw/assets/`.
Then "start over" (`rm -rf wiki-ai-engineering`) and a one-paragraph pointer that `03-hard/` trips the cap — the hand-off to 02, mentioned, not stepped through.

---

## 5. Layer 02 — `/02-llm-wiki-ingest`

**Goal:** (a) make it scale by moving writers into subagents with fan-out; (b) add non-local sources through a uniform adapter contract; (c) repos as a first-class type.

### 5.1 CHANGES-FROM-PREVIOUS.md
Bullets: why the cap existed and how fan-out removes it (the §"context discipline" explainer, ~15 lines: raw is read exactly once by `source_writer`; the orchestrator sees only receipts; `page_writer` reads source-like pages only; `overview_writer` reads frontmatter only); the harness-agnostic spawn paragraph; new files list; SKILL.md sections touched; CONVENTIONS/PAGES sections added; scripts changed (index + count now include `wiki/repos/`).

### 5.2 SKILL.md changes (minimal)
- New **Step 1.0 — Route inputs** (points to `SOURCES.md` routing table): local path → local; `github.com/<o>/<r>` or `*.git` → repo; `youtube.com|youtu.be` → youtube (skeleton — will fail loudly); other `http(s)` → article.
- Step 1.2 becomes "run the adapter for each input" (recipes in `SOURCES.md`); local stays `cp`.
- Step 1.3 becomes "spawn one `source_writer` per new raw file, in parallel; collect receipts". Repos: "spawn one `repo_writer` (mode `architecture`) per repo; collect receipt".
- Step 1.4 tail: "spawn one `page_writer` per qualifying slug, in parallel"; 1.5 "spawn `overview_writer`".
- Remove the 10-source cap.
- Add the **Spawning subagents** paragraph (harness-agnostic): read `agents/<name>.md`, pass its body as the prompt plus the listed inputs, run on a Sonnet-class model (or the equivalent tier of your provider; fall back to the harness default), parallel if supported else sequential, expect exactly one JSON receipt line back. The orchestrator never reads raw files or source pages itself.

### 5.3 SOURCES.md (the extensibility lesson, ≤150 lines)
- **Adapter contract:** input = one URI; output = exactly one raw artifact under `raw/` + a JSON receipt `{origin, original_path, title, source_url, authors, published_date, raw_path}`; the wiki pipeline is origin-agnostic after that. Two adapter shapes: *file adapters* (local, article, youtube) produce a raw markdown file consumed by `source_writer`; *tree adapters* (repo) produce a raw directory consumed by `repo_writer`.
- **Routing table** (URI pattern → adapter → raw path prefix → writer).
- **Per-origin recipes:** local (`cp`), article (`fetch_article.py`), repo (`clone_repo.py` then `repo_writer`), youtube (skeleton).
- **How to add a source** (walk it with YouTube): 1) write `scripts/fetch_<origin>.py` honoring the contract; 2) add one routing row; 3) pick the writer (file → `source_writer`, tree → new writer). Then a short table of what X / LinkedIn / Reddit / Readwise / Obsidian-vault adapters would need (fetch mechanism, ID scheme, gotchas) — described, not built.

### 5.4 Agents (`agents/*.md`) — all with: purpose, inputs, process, output template pointer to `PAGES.md`, receipt JSON, guardrails. No frontmatter pins; a "Model" prose line each.
- `source_writer.md` — from scrabble's `source_writer.md` minus scoring/assets/text-quality. Reads one raw file; writes one source page; returns receipt. Only agent allowed to read raw files.
- `page_writer.md` — from scrabble's `wiki_page_writer.md` minus tensions/open-questions/KEEP/confidence. Inputs: kind, slug, name, aliases, `source_pages` (paths — the only files it may read), `existing_page_path`, output path.
- `overview_writer.md` — from scrabble's summary writer, overview branch only. Frontmatter-walk via shell; ≤5 full reads; includes a Repos list when `wiki/repos/` exists.
- `repo_writer.md` — from scrabble's `github_spec_writer.md`, architecture mode trimmed to the `PAGES.md § repo` shape (≤300 lines, 4–6 sections, scope `src/` + README + `docs/`, ignore `assets/`, `tests/`, `evals/` unless the question needs them). Inputs: `clone_path`, `repo_url`, `owner`, `repo`, `commit_sha`, `branch`, `output_path`, `mode: architecture | question`, and for question mode `question`, `architecture_path`, `question_page`. Question mode is fully specified here but SKILL.md only wires it in 03 (CHANGES notes this).

### 5.5 Scripts
- `clone_repo.py --repo <url> --wiki-dir <wiki-<slug>>` — from scrabble's `github_clone.py`: any git URL, `--depth 1`, target `raw/repos/.github-<owner>-<repo>/`; if present → `fetch` + `reset --hard origin/<branch>` (action `updated`); prints `{owner, repo, branch, clone_path, commit_sha, action}`. Stdlib only. Drop symlink/working-memory/cache-dir options.
- `fetch_article.py --url <url> --wiki-dir <wiki-<slug>> [--output <path>]` — `curl -sL -A "<browser UA>"` via subprocess; parse with BeautifulSoup: title (`og:title` → `<title>`), subtitle (Substack `h3.subtitle` → `og:description`), author (`meta[name=author]` → JSON-LD `author.name`), published (`article:published_time` → JSON-LD `datePublished` → `<time datetime>`), body isolation (`<article>` → `div.body.markup` → `div.available-content` → `<main>` → `<body>`), strip `script/style/nav/footer/form/button`, `markdownify` the fragment (ATX headings). Write `raw/article-<slug>.md` with frontmatter (`title, subtitle, authors, published_date, source_url, origin: article, fetched`) + `# title` + `*subtitle*` + body. Print the receipt; set `"warning": "body under 500 chars — paywall or bot wall?"` when applicable. Deps: `beautifulsoup4`, `markdownify`.
- `fetch_youtube.py --url --wiki-dir` — docstring states the contract and what a real implementation would do (transcript fetch, `youtube://<video_id>` ID, `raw/youtube-<slug>.md`); body is `raise NotImplementedError("Workshop exercise: implement per SOURCES.md § How to add a source")`.
- `build_index_md.py` / `count_mentions.py` — add `wiki/repos/` (recursive one level: `repos/<repo>/*.md`; the repos index lists `[[wiki/repos/<repo>/<page>|<title>]] — <description>` grouped by repo).

### 5.6 CONVENTIONS/PAGES additions
CONVENTIONS: repos layout + hidden clone rationale, origin prefixes (`article-`, `youtube-`), repo refresh rule, source-like pages now include `wiki/repos/*/*.md`, Obsidian note (dot-dir ignored automatically). PAGES: `repo` contract.

### 5.7 demo.md
All paths relative to `02-llm-wiki-ingest/`. Starts from scratch — no layer 01 wiki. Targets come from `../data_input_examples/{github_repositories,substack_articles}.md`. One check per step.
1. Ingest `../data_input_examples/notes/02-medium/` → fresh wiki, 10 source pages, one `source_writer` per note in parallel, the orchestrator sees only receipts.
2. Ingest the repo URL from `github_repositories.md` → the skill clones it under `raw/repos/.github-decodingai-magazine-building-a-coding-agent-from-scratch-course/`, `wiki/repos/github-.../ARCHITECTURE.md` with mermaid and SHA-pinned permalinks, tail runs, a concept page lists the repo beside a note.
3. Ingest the two URLs from `substack_articles.md` → `raw/article-*.md` hold the body only, with frontmatter; concept pages cite notes, repo and article side by side.
4. Re-ingest the repo URL → refreshed, not skipped; ARCHITECTURE rewritten with `created` preserved.
5. Ingest a YouTube URL → skeleton fails loudly with the exercise message; nothing else written.
6. Query: "how does the coding agent's loop actually work?" → answer from `ARCHITECTURE.md` + an article source page; only `log.md` changed.
7. Optional: ingest `../data_input_examples/notes/03-hard/` → 40 new, 10 skipped by raw path; the big graph layer 03 starts from; thin notes get thin pages. Verified in Obsidian.

---

## 6. Layer 03 — `/03-llm-wiki-interactive`

**Goal:** the wiki learns from being used. Questions are logged, synthesized answers become notes, unanswerable ones become open questions, and repo questions add real knowledge back into the graph.

### 6.1 CHANGES-FROM-PREVIOUS.md
New `QUERY.md`; SKILL.md query section replaced by a pointer; new page types; three write regimes; the ingest tail reused from query; scripts index `questions/` + `notes/` + `open-questions.md`; `repo_writer` question mode now wired.

### 6.2 QUERY.md (≤200 lines)
- **Q.1 Locate / Q.2 Load index / Q.3 Disclosure ladder** — same as 01/02 (restated briefly; duplication is fine).
- **Q.4 Classify the question:** *repo-scoped* (names an ingested repo or asks how code works) vs *general*.
- **Q.5 General path:** answer from wiki pages; then save-back: always write the slim question page; write/enrich `wiki/notes/<slug>.md` iff ≥2 wiki pages cited or the user says save (idempotency rule: same topic → enrich in place). If the answer implies an ingest-owned page is wrong or missing something → do NOT edit it; append to `open-questions.md`.
- **Q.6 Repo path:** read `ARCHITECTURE.md`. If it answers the question → general path (note lands in `wiki/notes/`, linking the repo page). Else spawn `repo_writer` (`mode: question`) with the clone path/SHA and the question → it writes `wiki/repos/<repo>/<question-slug>.md` and returns a receipt → run the **ingest tail** (count → `page_writer` for touched ≥2 slugs → `overview_writer` → index) → write the slim question page with `answer_doc` = the repo note → log.
- **Q.7 Open questions:** user flags one ("log this as open") or the wiki genuinely can't answer (say so plainly, then append). Create `open-questions.md` with frontmatter on first use.
- **Q.8 Log + present:** standard answer format (topic line, body with wikilinks, "Pages used", saved-as line). `log.md` entry with op `query` (plus a "repo note ingested" bullet when Q.6 spawned).

### 6.3 SKILL.md changes
Query path → "read `QUERY.md`". Ingest path: after the tail, read `open-questions.md` (if present) and add one report bullet naming open questions the new sources appear to address (no edits). CONVENTIONS: interaction-owned pages, regimes table, ingest-tail-from-query rule. PAGES: `question`, `note`, `repo_note`, `open_question`.

### 6.4 demo.md
Start from `cp -r examples/wiki-ai-engineering .` — this layer's own `examples/` is layer 02's end state with nothing asked of it. The clone is not in it; the skill re-clones on its own when a question needs the code (QUERY.md Q.6). One check per step.
1. General question answered from ≥2 pages → `wiki/questions/<date>-<slug>.md` + `wiki/notes/<slug>.md`; no ingest-owned page changed.
2. Same question rephrased → note enriched in place (`spawned_by_question` has 2 entries, `created` unchanged), a second slim question page, no second note.
3. Unanswerable question → honest answer + `open-questions.md` created; no note.
4. Repo question needing code (tool call → permission gate routing) → skill reads `ARCHITECTURE.md`, clones, spawns `repo_writer` → `wiki/repos/<repo>/<slug>.md` (`type: repo_note`, permalinks pinned to SHA) → tail runs → a concept page's `sources:` grows.
5. A second repo question (subagent spawning) → a second repo note beside the first; `wiki/repos/index.md` lists both.
6. `log this as open: …` → second entry in `open-questions.md`, flagged by the user; nothing resolves it automatically.
7. Read the trail: `log.md`, `wiki/questions/index.md`, the graph in Obsidian. Then "start over" = `rm -rf` + re-copy from `examples/`.

---

## 7. Cross-cutting implementation rules for the implementer

- **Read scrabble first**, then write from scratch with the trimmed contracts. Do not copy scrabble prose about Readwise/NotebookLM/Bright Data/rounds/scoring/assets/PDF/OKF divergences beyond §2.10.
- **Tool-agnostic prose.** Say "read the file", "run in a shell", "ask the user", "spawn a subagent". One Claude Code footnote per SKILL.md mapping to Read/Bash/AskUserQuestion/Agent.
- **Model preference in prose only:** "Run on a Sonnet-class model (Claude Sonnet or the equivalent mid-tier model of your provider). If unavailable, use the harness default." Never in frontmatter.
- **Scripts:** PEP 723 header, `uv run --script`, deterministic output, JSON receipt on stdout, human notes on stderr, exit non-zero on hard failure. Stdlib where possible (`clone_repo.py`, `fetch_youtube.py`); `pyyaml` for the walkers; `beautifulsoup4` + `markdownify` for articles.
- **Byte-identical carry-forward:** build 01 completely, copy to 02, apply the 02 delta, copy to 03, apply the 03 delta. Verify with `diff -r --brief 01-… 02-…` that only intended files differ; paste that list into each `CHANGES-FROM-PREVIOUS.md`.
- **Slugs:** lowercase kebab-case, ASCII, punctuation stripped, ≤60 chars. Repo dirs keep `github-<owner>-<repo>` unslugged beyond lowercasing.
- **Timestamps:** ISO-8601 UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`).
- **Every SKILL.md ends with an "Agent reference" and "Script reference" table** (02+/01 respectively) like scrabble.
- **Symlinks:** create with `ln -s ../.agents/skills .claude/skills` inside each layer; commit them; README notes `git config core.symlinks true` for Windows.
- **Fixture references:** every demo and README section references inputs as `../data_input_examples/...` from the layer dir and reads URLs from the two link files. Never copy fixture notes into a layer.

## 8. `.gitignore` additions

```
# live workshop runs (reference runs live under examples/)
/0*-llm-wiki-*/wiki-*/
# repo clones are regenerable and huge
**/raw/repos/
# python
__pycache__/
.venv/
# macOS
.DS_Store
```

## 9. Verification checklist (per layer, run by the implementer before handing over)

- `uv run --script scripts/build_index_md.py --wiki-dir <dir>` twice → byte-identical output.
- `count_mentions.py` output matches a manual grep for one slug.
- Conformance check passes on the example run (every page has `type` + `description`).
- All `[[wikilinks]]` in `wiki/` resolve to a file OR are promissory entity/concept links (write a throwaway check in the scratchpad; do not ship a lint skill).
- `diff -r --brief` between consecutive layers lists only the files named in `CHANGES-FROM-PREVIOUS.md`.
- 02: `fetch_article.py` on both decodingai URLs yields title, subtitle, author, date, body > 2k chars. `clone_repo.py` twice → `cloned` then `updated`, same SHA.
- 03: the repo-question path leaves ingest-owned pages untouched except through the tail (check `git status` in `examples/`).
- 01: `01-easy` → `02-medium` append skips exactly the 5 shared notes; `03-hard` trips the cap with nothing written.
- `demo.md` steps executed end-to-end once per layer; `examples/` committed from that run (minus `raw/repos/`).

## 10. Implementation order

1. Root `README.md`, `.gitignore`. (`data_input_examples/` already exists — do not touch its contents.)
2. 01: `CONVENTIONS.md`, `PAGES.md`, scripts (+ unit-test them on a hand-made 3-page fixture in the scratchpad), `SKILL.md`, symlink, `demo.md`, the layer's section in the root README. Run the demo on `01-easy` → `02-medium`; commit `examples/`.
3. Copy 01 → 02. Add `SOURCES.md`, agents, `clone_repo.py`, `fetch_article.py`, `fetch_youtube.py`; extend scripts; patch SKILL/CONVENTIONS/PAGES; `CHANGES-FROM-PREVIOUS.md`; demo; examples.
4. Copy 02 → 03. Add `QUERY.md`; patch SKILL/CONVENTIONS/PAGES; extend scripts; wire `repo_writer` question mode; `CHANGES-FROM-PREVIOUS.md`; demo; examples.
5. Final `diff -r` audit across layers; root README progression table with links to each CHANGES file.

## 11. Open items (owner: Paul)

- Review the scenario picks in `data_input_examples/notes/01-easy/` (MCP vs. skills vs. CLIs cluster) and `02-medium/` (+ context layer, unified memory, agentic GraphRAG, harness architecture, MCP-for-DB-access). Swap notes if you want a different first impression; keep `01-easy ⊂ 02-medium ⊂ 03-hard`.
- Confirm the wiki slug used in demos/examples: `wiki-ai-engineering`.
- Confirm the two decodingai.com posts are free-tier (curl-fetchable) at workshop time.
