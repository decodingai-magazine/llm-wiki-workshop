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
| **[01 · vanilla](01-llm-wiki-vanilla/)** | the whole mechanic, inline | Identity is the raw path, the ≥2 threshold, the index is a cache. Hard cap: 10 notes per run. | — |
| **[02 · ingest](02-llm-wiki-ingest/)** | subagents + adapters | Fan-out is context engineering: each raw file is read **once**, by one agent, and the orchestrator only ever sees receipts. Anything with a URI becomes a source. | [CHANGES](02-llm-wiki-ingest/CHANGES-FROM-PREVIOUS.md) |
| **[03 · interactive](03-llm-wiki-interactive/)** | questions, notes, repo answers | The wiki learns from being used — and the interesting design work is deciding what **not** to count as evidence. | [CHANGES](03-llm-wiki-interactive/CHANGES-FROM-PREVIOUS.md) |

Each layer is a **superset** of the previous one: unchanged files are byte-identical,
and every changed file is listed section-by-section in its `CHANGES-FROM-PREVIOUS.md`.
A wiki built in layer 01 is a valid layer-02 wiki; layer 03's demo continues layer 02's.

Layer 01's cap is not a safety rail — it is the honest ceiling of doing everything in
one context, and hitting it is how layer 02 earns its complexity.

## Prerequisites

- An agent harness that can load a skill, read and write files, and run shell
  commands. Claude Code is the reference; anything equivalent works — nothing here
  pins a model or a tool name. Layers 02–03 also want a way to spawn subagents; if
  yours cannot, run the `agents/*.md` files as sequential prompts instead.
- **Python ≥3.12** and [`uv`](https://docs.astral.sh/uv/). All scripts are PEP 723
  single files run with `uv run --script` — no virtualenv, no install step.
- `git` and `curl` for layer 02's repo and article adapters.
- **Obsidian**, optional but recommended: open a layer directory as a vault and the
  graph view shows the wiki's shape, including the hollow nodes that mark ideas
  waiting for a second source.

## How to run it

Each layer is a self-contained project. Start in one and work through its `demo.md`:

```bash
cd 01-llm-wiki-vanilla
claude                     # or your harness

/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
```

Every layer ships:

- `README.md` — what the layer adds and what to look at when it finishes,
- `demo.md` — the exact prompts to type, each with a verification checklist,
- `examples/wiki-ai-engineering/` — a **committed reference run** of that demo, so
  you can read the output before producing your own (and `diff` against it).

The inputs live in [`data_input_examples/`](data_input_examples/): 50 real
AI-engineering notes in three nested scenarios (5 ⊂ 10 ⊂ 50), plus the repo and
article URLs the later layers ingest. See its
[README](data_input_examples/README.md) for the scenario table.

## What the reference runs actually contain

Not a toy. Layer 03's committed run is 55 source-like pages — 50 notes, 3
articles, a codebase and a question answered against that codebase — supporting 10
entity pages and 38 concept pages, with every claim cited and every link resolving.
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
├── 02-llm-wiki-ingest/        # layer 02: + agents, adapters, SOURCES.md
├── 03-llm-wiki-interactive/   # layer 03: + QUERY.md, questions, notes, open questions
└── implementation_plan.md     # how this repo was specified before it was built
```

Live runs (`<layer>/wiki-*/`) and repo clones are gitignored; the committed runs
under `examples/` are the ones to read.

---

Built by [Decoding AI](https://www.decodingai.com). MIT licensed — take the
contracts, the scripts and the page templates and point them at your own notes.
