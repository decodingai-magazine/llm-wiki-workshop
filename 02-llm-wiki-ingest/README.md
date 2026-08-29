# Layer 02 — ingest at scale

**Goal: remove the ceiling, and let anything with a URI become a source.**

Layer 01 capped a run at 10 notes because the orchestrator read every one of them.
This layer changes who reads:

```
                    ┌── source_writer ── wiki/sources/a.md ──┐
raw artifacts ──────┼── source_writer ── wiki/sources/b.md ──┼── receipts ──► orchestrator
                    └── repo_writer ──── wiki/repos/…/ARCHITECTURE.md ─┘          │
                                                                                  ▼
                                                         count_mentions → page_writer × N
                                                                        → overview_writer
                                                                        → build_index_md
```

Each raw file is read **exactly once, ever**, by one subagent that never sees any
other source. The orchestrator sees a few hundred tokens of JSON per source. Fifty
notes cost about the same orchestrator context as five — which is why the cap
could be deleted rather than raised.

The second half of the layer is the **adapter contract**: one URI in, one raw
artifact plus one receipt out. Local notes, web articles and GitHub repos ship;
YouTube is a deliberate skeleton, and wiring it up is the exercise.

## What's inside

```
02-llm-wiki-ingest/
├── .agents/skills/02-llm-wiki-ingest/
│   ├── SKILL.md                 # orchestrator: route → adapters → fan-out → tail
│   ├── CONVENTIONS.md           # 01's contract + repos as sources + context discipline
│   ├── PAGES.md                 # 01's page contracts + the repo page
│   ├── SOURCES.md               # the adapter contract, routing table, how to add an origin
│   ├── agents/
│   │   ├── source_writer.md     # one raw file → one source page (the only reader of raw/)
│   │   ├── repo_writer.md       # one clone → ARCHITECTURE.md (question mode ships unused)
│   │   ├── page_writer.md       # one slug + its source pages → one entity/concept page
│   │   └── overview_writer.md   # frontmatter walk → overview.md
│   └── scripts/
│       ├── count_mentions.py    # + wiki/repos/*/*.md are source-like too
│       ├── build_index_md.py    # + a grouped wiki/repos/index.md
│       ├── clone_repo.py        # shallow clone / refresh → JSON receipt
│       ├── fetch_article.py     # curl → body isolation → markdown
│       └── fetch_youtube.py     # skeleton: raises NotImplementedError on purpose
├── CHANGES-FROM-PREVIOUS.md     # exact diff from layer 01, section by section
├── demo.md
└── examples/                    # committed reference run
```

## Prerequisites

Everything layer 01 needed, plus `git` and `curl` (both already on macOS and
Linux). No GitHub token — the demo repo is public and cloned with `--depth 1`.

Your harness needs some way to run a subagent. Claude Code has one; if yours does
not, run the `agents/*.md` files as sequential prompts and you get the same wiki,
just slower.

## Run it

```bash
cd 02-llm-wiki-ingest
claude
```

Then follow `demo.md`:

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/03-hard/
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
/02-llm-wiki-ingest ingest https://www.decodingai.com/p/the-coding-agent-loop
```

The repo and article URLs live in `../data_input_examples/github_links.md` and
`../data_input_examples/substack_links.md` — swap them there and every demo step
follows.

## What to look at when it finishes

- **`wiki/repos/github-…/ARCHITECTURE.md`** — a codebase compressed to ≤300 lines
  of diagrams and pinned permalinks. Every future question about that repo is
  answered from this page, not from 300 Python files.
- **A concept page that now cites both a note and the repo.** That is the payoff of
  one line in `count_mentions.py`: a claim someone wrote down and a codebase that
  implements it are two independent witnesses, so the page materializes.
- **`raw/article-*.md`** — what the fetcher actually kept. Compare it to the live
  page: body isolation is the difference between a source and a cookie banner.
- **The thin pages.** `03-hard/` includes real personal notes — a marketing draft,
  a meeting dump, a three-line stub. Their source pages are correspondingly thin
  and contribute almost no links. That is the system working: the threshold makes
  noise cheap.
- **`raw/repos/`** — hidden from Obsidian, gitignored, regenerable. Delete it and
  re-run `clone_repo.py`; nothing in `wiki/` cares.

## The three ideas worth taking away

1. **Fan-out is context engineering, not parallelism.** The speedup is a side
   effect; the point is that no context ever holds everything.
2. **Receipts are the interface.** The orchestrator coordinates writers it cannot
   see, using a JSON shape specified as tightly as the pages themselves.
3. **Origins are a routing detail.** One URI in, one raw artifact out, and the
   entire pipeline downstream never learns where anything came from.

Next: [layer 03](../03-llm-wiki-interactive/) makes the wiki learn from being
queried.
