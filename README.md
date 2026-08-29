# The LLM Wiki Workshop

**Build a wiki that an LLM writes, an LLM reads, and that gets better every time
you use it.** Three layers, each a complete working system, each adding exactly one
idea to the previous one.

```
raw/note.md ──► wiki/sources/note.md ──► ≥2 mentions ──► wiki/concepts/mcp.md
                                                     ↘   wiki/overview.md
                                                     ↘   wiki/index.md   (generated)
                                                     ↘   log.md          (append-only)
```

## Slides & video

| | |
|---|---|
| 📺 **Video** — the workshop, end to end | *to be added* |
| 🖼 **Slides** | *to be added* |

## What an "LLM wiki" is

A directory of markdown files with two halves that never mix:

- **`raw/`** — immutable copies of what you ingested. What was said.
- **`wiki/`** — pages an LLM wrote from those copies. What you know.

Every page carries YAML frontmatter, every claim carries a `[[wikilink]]` to what
backs it, and one rule governs what exists at all:

> **A concept gets a page when ≥2 distinct sources engage with it.**

One note mentioning something is a fact about the note. Two notes mentioning it is
a fact about your knowledge. That single threshold is what stops the wiki filling
with stubs — and watching it fire is the most useful five minutes of the workshop.

The navigation (`index.md` files) is a **derived cache**: delete it, re-run one
script, get identical bytes back. Nothing has to be kept in sync by hand.

## The three layers

| Layer | Adds | The idea it teaches | Read the diff |
|---|---|---|---|
| **[01 · vanilla](#layer-01--vanilla)** | the whole mechanic, inline | Identity is the raw path, the ≥2 threshold, the index is a cache. Hard cap: 10 notes per run. | — |
| **[02 · ingest](#layer-02--ingest-at-scale)** | subagents + adapters | Fan-out is context engineering: each raw file is read **once**, by one agent, and the orchestrator only ever sees receipts. Anything with a URI becomes a source. | [CHANGES](02-llm-wiki-ingest/CHANGES-FROM-PREVIOUS.md) |
| **[03 · interactive](#layer-03--interactive)** | questions, notes, repo answers | The wiki learns from being used — and the interesting design work is deciding what **not** to count as evidence. | [CHANGES](03-llm-wiki-interactive/CHANGES-FROM-PREVIOUS.md) |

Each layer is a **superset** of the previous one: unchanged files are byte-identical,
and every changed file is listed section-by-section in its `CHANGES-FROM-PREVIOUS.md`.
A wiki built in one layer is a valid wiki in the next. The demos still stand alone:
layers 01 and 02 start from nothing, and layer 03 starts from a committed copy of
layer 02's end state.

Layer 01's cap is not a safety rail — it is the honest ceiling of doing everything in
one context; feed it the 50-note batch and it refuses. Removing the cause rather than
raising the number is how layer 02 earns its complexity.

## Prerequisites

This is the only place they are listed. Install these once and every skill in every
layer works out of the box — the skills run the scripts, clone the repos and fetch
the articles themselves. You only ever type prompts.

- **An agent harness** that can load a skill, read and write files, and run shell
  commands. Claude Code is the reference: run `claude` inside a layer directory and
  it finds the skill through `.claude/skills`. Anything equivalent works — nothing
  here pins a model or a tool name. Layers 02–03 also want a way to spawn
  subagents; if yours cannot, run the `agents/*.md` files as sequential prompts.
- **Python ≥3.12** and [`uv`](https://docs.astral.sh/uv/). The scripts are PEP 723
  single files; `uv` installs their dependencies the first time a skill runs one —
  no virtualenv, no install step.
- **`git` and `curl`**, for the repo and article adapters in layers 02–03. No
  GitHub token: the demo repo is public and cloned shallow.
- **Obsidian**, optional but recommended — it is how you check your work. Open a
  layer's `wiki-ai-engineering/` as a vault and the graph view shows the wiki's
  shape, including the hollow nodes that mark ideas waiting for a second source.

## How to run it

Each layer is a self-contained project with its own skill. Start in one, open your
harness there, and work through its `demo.md`:

```bash
cd 01-llm-wiki-vanilla
claude                     # or your harness

/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
```

Every layer ships the same three things:

- **`.agents/skills/<layer>/`** — the skill: `SKILL.md` is the orchestrator, the
  contract files beside it (`CONVENTIONS.md`, `PAGES.md`, and from 02 `SOURCES.md`
  and `agents/`, from 03 `QUERY.md`) are what it follows, and `scripts/` is what it
  runs. A committed `.claude/skills` symlink points Claude Code at it.
- **`demo.md`** — the exact prompts to type, each with one thing to check.
- **`examples/wiki-ai-engineering/`** — a **committed reference run**, so you can
  read the output before producing your own. In layer 03 it is the demo's start
  point.

The wiki you build lands in `<layer>/wiki-ai-engineering/` and is gitignored. To
verify anything, open that directory as an Obsidian vault. To start over, delete it.

## The inputs

[`data_input_examples/`](data_input_examples/) holds everything the workshop
ingests. Pass paths and URLs to the skills relative to the layer directory
(`../data_input_examples/...`).

| Input | What | Used by |
|---|---|---|
| `notes/01-easy/` | 5 notes — one tight cluster (MCP vs. skills vs. CLIs) | layer 01 |
| `notes/02-medium/` | 10 notes — easy + 5 bridging notes (context layer, memory, GraphRAG, harness) | layer 02, from scratch |
| `notes/03-hard/` | all 50 notes, including tiny and noisy personal ones | layer 02's optional last step; layer 03 starts from its result |
| `github_repositories.md` | one repo URL | layer 02 |
| `substack_articles.md` | four article URLs; the demo ingests two | layer 02 |

The tiers are nested (5 ⊂ 10 ⊂ 50) and a note's identity is its filename, so
ingesting a larger tier over a smaller one skips what is already there — that is
the dedup demo. Each tier carries **its own `assets/`** with exactly the files its
notes embed, as a sibling folder, so `![[assets/….png]]` resolves in any vault.
Ingest copies a note *and its attachments* into `raw/`, so the embeds keep working
there. Attachments are not sources: no page, no threshold vote. Only `*.md` is
ingested, which is why the three `.srt` transcripts in `03-hard/assets/` land in
`raw/` and stay unread — the standing exercise is the adapter that reads them.

---

## Layer 01 — vanilla

**Goal: see the whole mechanic with zero moving parts.** One skill, two scripts, no
subagents, no web.

**Ingest.** The orchestrator does everything itself: copies each note (and its
attachments) into `raw/`, reads it, writes one source page whose every claim cites
`[[raw/...]]`, then runs the *ingest tail* — `count_mentions.py` names every slug
at ≥2 source pages, a page is written or updated for each, `overview.md` is
rewritten, `build_index_md.py` regenerates the indexes, `log.md` gets one entry.
Concept pages cite **source pages**, never raw, so they compound as sources
accumulate without anyone re-reading the notes. Hard cap of 10 notes per run,
because one context has to hold all of them.

**Query** is read-only: `index.md` → a concept page → maybe a source page, and
`raw/` only if a page genuinely fails. Every claim carries a wikilink; the only
file that changes is `log.md`. If the wiki does not know, it says so.

**Run it** — [`01-llm-wiki-vanilla/demo.md`](01-llm-wiki-vanilla/demo.md): ingest
the 5 easy notes, ask one question, look at the graph.

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
/01-llm-wiki-vanilla what do my notes say about when to use an MCP server vs. a CLI?
```

**Look at:** the ingest report's "waiting at 1 mention" list — the wiki telling
you what it is about to learn; `raw/assets/`, the images copied in beside the
notes so the embeds still render; and in Obsidian the hollow nodes, which are the
same list drawn as a graph.

## Layer 02 — ingest at scale

**Goal: remove the ceiling, and let anything with a URI become a source.**

```
                    ┌── source_writer ── wiki/sources/a.md ──┐
raw artifacts ──────┼── source_writer ── wiki/sources/b.md ──┼── receipts ──► orchestrator
                    └── repo_writer ──── wiki/repos/…/ARCHITECTURE.md ─┘          │
                                                                                  ▼
                                                         count_mentions → page_writer × N
                                                                        → overview_writer
                                                                        → build_index_md
```

**Ingest changes who reads.** Every page is written by a subagent defined as plain
markdown in `agents/`: `source_writer` reads one raw file — the only agent allowed
to — `repo_writer` reads one clone, `page_writer` reads only the source pages for
its slug, `overview_writer` reads frontmatter. The orchestrator routes, spawns and
collects JSON receipts; it never sees a note. Fifty notes cost about the same
orchestrator context as five, which is why the cap is deleted rather than raised.

The other half is the **adapter contract** (`SOURCES.md`): one URI in, one raw
artifact plus one receipt out, and nothing downstream learns where anything came
from. Local notes, web articles (`curl` + body isolation) and GitHub repos (shallow
clone into a hidden dot-folder, then an `ARCHITECTURE.md` of ≤300 lines with
SHA-pinned permalinks) ship; YouTube is a skeleton that fails loudly, and wiring it
up is the exercise. Repos are the one origin that **refreshes** instead of skipping,
because the code moves. A repo page is source-like: a codebase and a note are two
independent witnesses, so together they can materialize a concept.

**Query** is unchanged, except that code questions start at `ARCHITECTURE.md` — it
exists so nobody has to read the clone.

**Run it** — [`02-llm-wiki-ingest/demo.md`](02-llm-wiki-ingest/demo.md), from
scratch: 10 notes → the repo → two articles → refresh the repo → YouTube fails →
a query across origins → optionally all 50 notes. What changed from 01:
[`CHANGES-FROM-PREVIOUS.md`](02-llm-wiki-ingest/CHANGES-FROM-PREVIOUS.md).

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/02-medium/
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
/02-llm-wiki-ingest ingest https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design https://www.decodingai.com/p/the-coding-agent-loop
```

**Look at:** the concept page whose `sources:` lists a note *and* the repo;
`raw/article-*.md` next to the live page — body isolation is the difference between
a source and a cookie banner; and after the optional last step, the three-line
pages the noisy notes produce. Noise is cheap; the threshold made it so.

## Layer 03 — interactive

**Goal: make interaction a second way for the graph to grow.**

```
question ──► answer from wiki pages ──┬─► wiki/questions/<date>-<slug>.md   (always)
                                      ├─► wiki/notes/<slug>.md             (if ≥2 pages cited)
                                      ├─► wiki/open-questions.md           (if it can't answer)
                                      └─► wiki/repos/<repo>/<slug>.md      (if it needs the code)
                                                    │
                                                    └─► the ingest tail runs ─► concept pages grow
```

**Ingest is unchanged.** **Query now writes back**, under three write regimes:
ingest-owned pages (`raw/`, `sources/`, `entities/`, `concepts/`, `overview.md`,
`ARCHITECTURE.md`) are read-only; interaction-owned pages (`questions/`, `notes/`,
`open-questions.md`) are written freely; a **repo note** is written by
`repo_writer` in question mode and then run through the same ingest tail as any
source. So: every question leaves a slim pointer page; an answer that cited ≥2
pages becomes a note, and asking again *enriches* that note instead of forking it;
a question the wiki cannot answer becomes an open question — said plainly, and
nothing resolves it automatically; a question that needs the code produces a repo
note that is source-like, so **an answer can push a concept over the threshold**.

`questions/` and `notes/` are deliberately *not* source-like. A wiki that counts its
own notes as evidence can cite itself into existence.

**Run it** — [`03-llm-wiki-interactive/demo.md`](03-llm-wiki-interactive/demo.md):
copy the layer's `examples/` (layer 02's end state, nothing asked of it yet) and
ask seven questions. The clone is not in the copy; the skill re-clones on its own
when a question needs the code. What changed from 02:
[`CHANGES-FROM-PREVIOUS.md`](03-llm-wiki-interactive/CHANGES-FROM-PREVIOUS.md).

```bash
cp -r examples/wiki-ai-engineering .
```

```
/03-llm-wiki-interactive when should I use an append-only log instead of updating rows in place?
/03-llm-wiki-interactive how do I decide that a fact in the memory has gone stale?
/03-llm-wiki-interactive in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?
```

**Look at:** a note with two entries in `spawned_by_question` and its first
`created`; the repo note and the concept page it pushed into `sources:` — trace it,
question → repo note → recount → updated page; and `git status` on the ingest-owned
pages: the only ones that changed are the ones the tail touched.

---

## What the reference runs actually contain

Not a toy. Layer 02's committed run — the one layer 03 starts from — is 53
source-like pages: 50 notes, 2 articles and a codebase, supporting 10 entity pages
and 38 concept pages, with every claim cited and every link resolving.
It is worth opening before you run anything, because it shows what the threshold
produces on real, messy input: a marketing draft and a three-line meeting note get
pages too, and they correctly connect to almost nothing.

## The five ideas, in order of how much they'll change your systems

1. **Identity is the raw path.** Dedup is an `ls`, not a database. Ingest the same
   note through two directories and nothing happens.
2. **The ≥2 threshold.** What you refuse to write down matters more than what you do.
3. **Read raw once, ever.** After ingestion, the wiki *is* the interface — which is
   what makes the cost of ingesting compound instead of repeat.
4. **Receipts are the interface.** The orchestrator coordinates writers it cannot
   see, using a JSON shape specified as tightly as the pages themselves.
5. **Regimes, not permissions.** Reading a source can never change what the wiki
   says that source means — otherwise the same question asked twice leaves two
   different wikis behind.

## Layout

```
llm-wiki-workshop/
├── data_input_examples/       # the fixture: 50 notes in 3 nested scenarios + link files
├── 01-llm-wiki-vanilla/       # layer 01: skill, scripts, demo, committed example run
├── 02-llm-wiki-ingest/        # layer 02: + agents, adapters, SOURCES.md, CHANGES
├── 03-llm-wiki-interactive/   # layer 03: + QUERY.md, questions, notes, open questions
└── implementation_plan.md     # how this repo was specified before it was built
```

This is the only README. Each layer's `demo.md` is its walkthrough. Live runs
(`<layer>/wiki-*/`) and repo clones are gitignored; the committed runs under
`examples/` are the ones to read.

---

Built by [Decoding AI](https://www.decodingai.com). MIT licensed — take the
contracts, the scripts and the page templates and point them at your own notes.
