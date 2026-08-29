# Layer 01 — vanilla LLM wiki

**Goal: see the whole mechanic with zero moving parts.**

Local markdown notes go in. Out comes a wiki that an LLM wrote and that an LLM
(or you, in Obsidian) can navigate:

```
raw/note.md  →  wiki/sources/note.md  →  ≥2 mentions  →  wiki/concepts/mcp.md
                                                      ↘  wiki/overview.md
                                                      ↘  wiki/index.md (generated)
                                                      ↘  log.md (append-only)
```

No subagents. No adapters. No web. One skill, two scripts, and a hard cap of 10
notes per run — because in this layer the orchestrator reads every note into a
single context, and that ceiling is exactly the problem layer 02 exists to solve.

## What's inside

```
01-llm-wiki-vanilla/
├── .agents/skills/01-llm-wiki-vanilla/
│   ├── SKILL.md            # the orchestrator: locate → detect mode → ingest / query
│   ├── CONVENTIONS.md      # the data contract (layout, identity, threshold, links, log, OKF)
│   ├── PAGES.md            # frontmatter + body template + receipt for every page type
│   └── scripts/
│       ├── count_mentions.py    # frontmatter walk → who mentions what (the ≥2 threshold)
│       └── build_index_md.py    # frontmatter walk → the index.md family + OKF conformance
├── .claude/skills -> ../.agents/skills   # so Claude Code finds the skill; other harnesses read .agents/
├── demo.md                 # the 6 prompts to run, and what to check after each
└── examples/               # a committed reference run, so you can read the output before producing it
```

## Prerequisites

- An agent harness with file read/write and shell access (Claude Code, or any
  harness that can load a skill and run commands).
- Python ≥3.12 and [`uv`](https://docs.astral.sh/uv/) — the scripts are PEP 723
  single files, so `uv run --script` installs their one dependency on first use.
- Obsidian (optional, but the graph view is half the point).

## Run it

```bash
cd 01-llm-wiki-vanilla
claude          # or your harness of choice
```

Then follow `demo.md`. The short version:

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/02-medium/
/01-llm-wiki-vanilla what do my notes say about MCP servers?
```

The wiki lands in `wiki-<slug>/` (the demo uses `wiki-ai-engineering`) and is
gitignored — `examples/wiki-ai-engineering/` holds a committed run of the same
demo so you can diff your output against it.

## What to look at when it finishes

**In the terminal** — the ingest report: how many notes were new, how many were
skipped, which concept pages materialized, and which slugs are sitting at exactly
one mention. That last list is the wiki telling you what it is about to learn.

**In the files**:

- `wiki/index.md` and `wiki/concepts/index.md` — pure navigation, generated from
  frontmatter. Delete them, re-run the script, get identical bytes back.
- Any `wiki/sources/*.md` — every claim cites `[[raw/...]]`. The LLM's own
  judgment is quarantined on `> Synthesis:` lines.
- Any `wiki/concepts/*.md` — every claim cites a **source page**, never raw. This
  is the compounding layer: it gets better as sources accumulate, without anyone
  re-reading the notes.
- `raw/assets/` — the images the notes embed, copied in beside them so the embeds
  keep working. Attachments are payload, not sources: no page, no threshold vote.
- `log.md` — the whole history of the wiki, append-only, greppable.

**In Obsidian** (open this directory as a vault): the graph view shows
hub-and-spoke clusters around concept pages, and **hollow nodes** — those are
promissory links, ideas mentioned exactly once, waiting for a second source.

## The three ideas worth taking away

1. **Identity is the raw path.** Dedup is an `ls`, not a database. Ingest the
   same note twice and nothing happens.
2. **The ≥2 threshold.** One note mentioning something is a fact about the note;
   two notes mentioning it is a fact about your knowledge — and only that earns a
   page. It is the cheapest possible defence against a wiki full of stubs.
3. **The index is a cache.** Frontmatter is canonical; navigation is regenerated.
   Nothing in the wiki has to be kept in sync by hand.

Next: [layer 02](../02-llm-wiki-ingest/) removes the cap and teaches the wiki to
read repos and articles.
