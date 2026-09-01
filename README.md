# LLM Wikis From First Principles - Workshop

**Build an LLM wiki that an agent writes, an agent reads, and that gets better every time
you use it.** Three exercises, each a complete working system, each adding exactly one
idea to the previous one: vanilla, scale ingestion and make it interactive to learn from every query.

<p>
  <img src="https://img.shields.io/badge/type-open--source_workshop-8a2be2" alt="Open-source workshop">
  <img src="https://img.shields.io/badge/exercises-3-4c8eda" alt="3 exercises">
  <img src="https://img.shields.io/badge/works_with-notes_%2F_repos_%2F_articles-2ea44f" alt="Works with notes, repos and articles">
  <img src="https://img.shields.io/badge/runs_on-any_agent_harness-orange" alt="Runs on any agent harness">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="MIT license">
</p>

<img src="assets/llm_wiki_architecture.png" alt="LLM wiki architecture: notes, repos, articles and videos are ingested into an immutable raw/ layer, transformed into wiki/, and queried by an agent" width="800"/>

> **5 minutes Quickstart:**
>
> ```bash
> git clone https://github.com/decodingai-magazine/llm-wiki-workshop.git
> cd llm-wiki-workshop/01-llm-wiki-vanilla
> claude          # or your harness
> ```
>
> Then type one prompt and watch a wiki appear:
>
> ```
> /01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
> ```
>
> [Prerequisites](#prerequisites) · [full walkthrough](01-llm-wiki-vanilla/demo.md)

## Slides & video

📑 The presentation is available [here](https://canva.link/1k5z1bkoxq1pkhd) ↓

<a href="https://canva.link/1k5z1bkoxq1pkhd" target="_blank">
  <img src="assets/presentation_thumbnail.png" alt="LLM Wikis From First Principles — the workshop presentation" width="600"/>
</a>

🎬 Video — *coming soon*.

<!-- When the recording is live, replace the line above with the clickable thumbnail:

🎬 Full workshop available on [YouTube](https://www.youtube.com/watch?v=VIDEO_ID) ↓

<a href="https://www.youtube.com/watch?v=VIDEO_ID">
  <img src="https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg" alt="Watch the workshop" style="width:100%; max-width:600px;">
</a>
-->

## How to use this repo

Three ways in. Pick the one that fits the time you have — or do all three in
order, since each builds on the last:

1. **Read a finished wiki. ~15 min, nothing to install.** Open a committed
   reference run —
   [`01-llm-wiki-vanilla/examples/wiki-01-ai-engineering/`](01-llm-wiki-vanilla/examples/wiki-01-ai-engineering/)
   is the smallest — ideally as an Obsidian vault. You'll see the two halves
   (`raw/` vs `wiki/`), every claim carrying its citation, and what the ≥2
   threshold chose to write, before running anything yourself.
2. **Run one layer's demo. ~30 min.** Install the
   [prerequisites](#prerequisites), `cd 01-llm-wiki-vanilla`, open your harness,
   and type the prompts in [`demo.md`](01-llm-wiki-vanilla/demo.md). Every
   prompt comes with one thing to verify.
3. **Work through all three layers. ~2–3 h.** Layers 01 and 02 start from
   nothing; layer 03 starts from a committed copy of layer 02's end state. Read
   each layer's `CHANGES-FROM-PREVIOUS.md` first to see exactly which files the
   new idea touched — that diff is the lesson.

## What an "LLM wiki" is

A directory of markdown files with two halves that never mix:

- **`raw/`** — immutable copies of what you ingested. What was said.
- **`wiki/`** — pages an LLM wrote from those copies. What you know.

Every page carries YAML frontmatter, every claim carries a `[[wikilink]]` to what
backs it, and one rule governs what exists at all:

> **A concept gets a page when ≥2 distinct sources engage with it.**

One note mentioning something is a fact about the note. Two notes mentioning it is
a fact about your knowledge. That single threshold is what stops the wiki filling
with stubs .

<img src="assets/one_ingested_item.png" alt="What happens to one ingested item: copied to raw/, distilled into a source page with key insights, entities and concepts — and when a concept reaches ≥2 sources, a synthesized concept page materializes" width="800"/>

The navigation is done via progressive disclosure through the hierarchy of indexes:

<img src="assets/how_the_index_works.png" alt="How the index works: source, concept and entity pages feed per-directory index files, which feed the root index.md, the overview and the log" width="800"/>

Visualized in Obsidian:

<table>
<tr>
<td align="center"><img src="assets/obsidian_graph_02_llm_wiki_ingest_master_index.png" alt="Obsidian graph with the root index.md highlighted, linking out to each section index"/></td>
<td align="center"><img src="assets/obsidian_graph_02_llm_wiki_ingest_concepts_index.png" alt="Obsidian graph with concepts/index.md highlighted, linking out to every concept page"/></td>
</tr>
<tr>
<td align="center"><em>The master <code>index.md</code> — one hop to every section</em></td>
<td align="center"><em><code>concepts/index.md</code> — one hop to every concept page</em></td>
</tr>
</table>

Growing from 14 sources to 135:

<table>
<tr>
<td align="center"><img src="assets/obsidian_graph_02_llm_wiki_ingest.png" alt="Obsidian graph of layer 02's reference run: colored concept and entity hubs surrounded by source pages and hollow nodes waiting for a second mention"/></td>
<td align="center"><img src="assets/obsidian_graph_book.png" alt="Obsidian graph of a mature LLM wiki built from a real corpus: a dense, connected knowledge graph"/></td>
</tr>
<tr>
<td align="center"><em>Layer 02's reference run — 14 sources, 17 nodes</em></td>
<td align="center"><em>The same system after months on a real corpus — 135 sources, 120 nodes</em></td>
</tr>
</table>

<details>
<summary><strong>What a page actually looks like</strong> — a real concept page from the layer 02 reference run (click to expand)</summary>

<br/>

Seven source-like pages — notes, articles **and a codebase** — engage with agent
memory, so [`wiki/concepts/agent-memory.md`](02-llm-wiki-ingest/examples/wiki-02-ai-engineering/wiki/concepts/agent-memory.md)
exists. Frontmatter is the contract; every claim in the body cites the source
page that backs it; disagreements between sources get their own `Tensions`
section; and the LLM's own judgment is fenced off as `> Synthesis:` — here,
noticing that six of the seven sources are one practitioner's voice, not
independent confirmation. Excerpt (full page at the link):

```markdown
---
type: concept
title: Agent Memory
description: The persistent layer that lets an agent reuse context across a
  session or across interactions — framed across sources either as a queryable
  knowledge graph reached through MCP tools, or as flat markdown files loaded
  wholesale into the system prompt at session start.
sources:
  - "[[wiki/sources/agentic-graphrag-via-mcp-servers]]"
  - "[[wiki/sources/article-building-a-coding-agent-from-scratch-system-design]]"
  - "[[wiki/sources/article-context-engineering-for-coding-agents]]"
  - "[[wiki/sources/article-the-coding-agent-loop]]"
  - "[[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]"
  - "[[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]"
  - "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
related:
  - "[[wiki/concepts/graphrag]]"
  - "[[wiki/concepts/mcp]]"
  - "[[wiki/concepts/agent-harness]]"
created: 2026-08-31T17:23:45Z
timestamp: 2026-08-31T20:15:00Z
source_count: 7
---

# Agent Memory

> Multiple framings — see Definition

## Key claims

- A knowledge graph — typed nodes and edges extracted from ingested documents
  — is the recurring representation across the three MCP-based sources […]
  [[wiki/sources/agentic-graphrag-via-mcp-servers]], [[wiki/sources/the-right-way-of-building-agents-with-mcp-servers]]
- Decode's memory is prompt-embedded, not tool-mediated: assembled once at
  session start, with `.decode/MEMORY.md` periodically rewritten in place […]
  [[wiki/sources/article-context-engineering-for-coding-agents]]

## Tensions

Two incompatible architectures share the name "agent memory" here. […] Neither
cluster reconciles the two — likely a scale question (personal knowledge base
vs. single coding session) that no source states directly.
[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]
lands squarely on the file-based side and hardens it […]

> Synthesis: Six of seven sources trace to one practitioner […] so their
> agreement still reads as one voice across time, not independent
> confirmation. [[wiki/sources/mongodb-for-an-ai-agent-unified-memory]]
> remains the sole architecturally independent, vendor-framed source […]
```

</details>

## The three exercises

Each exercise builds on the previous one. You can do them independently as well.

| Layer | Adds | The idea it teaches | Read the diff |
|---|---|---|---|
| **[01 · vanilla](#layer-01--vanilla)** | the whole mechanic, inline | Identity is the raw path, the ≥2 threshold, the index is a cache. Hard cap: 10 notes per run. | — |
| **[02 · ingest](#layer-02--ingest-at-scale)** | subagents + adapters | Fan-out is context engineering: each raw file is read **once**, by one agent, and the orchestrator only ever sees receipts. Anything with a URI becomes a source. | [CHANGES](02-llm-wiki-ingest/CHANGES-FROM-PREVIOUS.md) |
| **[03 · interactive](#layer-03--interactive)** | questions, notes, repo answers | The wiki learns from being used — and the interesting design work is deciding what **not** to count as evidence. | [CHANGES](03-llm-wiki-interactive/CHANGES-FROM-PREVIOUS.md) |

## 📬 Learn more on LLM Wikis and agent memory

> Join 40k+ engineers reading [the Decoding AI Magazine](https://www.decodingai.com/) and watching [the Decoding AI YouTube channel](https://www.youtube.com/@itsdecodingai) to learn to design LLM wikis and advanced agent-memory techniques.

<a href="https://www.decodingai.com/" target="_blank">
  <img src="assets/decodingai.jpg" alt="Decoding AI Magazine" width="100%"/>
</a>

## Prerequisites

| | |
|---|---|
| **Skills** | Comfortable in a terminal. No coding required — you only type prompts. |
| **Level** | Anyone who has used an AI coding assistant; the layers teach the rest. |
| **Time** | ~30 min per layer, ~2–3 h for all three. |
| **Cost** | $0 beyond your harness's LLM usage — no API keys, no accounts. The optional 50-note ingest closing layer 02 is the only token-heavy step. |

## Setup

| Requirement                                     | Check                             | Install                                                                                                              |
| ----------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| An agent harness (Claude Code is the reference) | `claude --version`                | [claude.com/claude-code](https://claude.com/claude-code)                                                             |
| Python ≥3.12                                    | `python3 --version`               | `uv python install 3.12` or [python.org](https://www.python.org/downloads/)                                          |
| [`uv`](https://docs.astral.sh/uv/)              | `uv --version`                    | `curl -LsSf https://astral.sh/uv/install.sh \| sh` ([docs](https://docs.astral.sh/uv/getting-started/installation/)) |
| `git` + `curl`                                  | `git --version`, `curl --version` | pre-installed on macOS/Linux                                                                                         |
| Obsidian (optional)                             | Visualize the examples            | [obsidian.md](https://obsidian.md)                                                                                   |

**Verify the setup** — from the repo root, run one of the workshop's scripts
against a committed reference run:

```bash
uv run --script 01-llm-wiki-vanilla/.agents/skills/01-llm-wiki-vanilla/scripts/count_mentions.py \
  --wiki-dir 01-llm-wiki-vanilla/examples/wiki-01-ai-engineering
```

If it prints a mention table with potential 12 entities/concepts where only 9 qualify.

## How to run it

Each layer is a self-contained project with its own skill. Start in one, open your
harness there, and work through its `demo.md`:

```bash
cd 01-llm-wiki-vanilla
claude                     # or your harness

/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
```
## The inputs

[`data_input_examples/`](data_input_examples/) holds a few notes, a GitHub repo and Substack article URLs as examples:

| Input                    | What                                                  |
| ------------------------ | ----------------------------------------------------- |
| `notes/01-easy/`         | 5 notes — one tight cluster (MCP vs. skills vs. CLIs) |
| `notes/02-medium/`       | 10 notes — context layer, memory, GraphRAG, harness   |
| `notes/03-hard/`         | all 50 notes, including tiny and noisy personal ones  |
| `github_repositories.md` | one repo URL                                          |
| `substack_articles.md`   | four article URLs                                     |

The tiers are nested (5 ⊂ 10 ⊂ 50) and a note's identity is its filename.

---

## Layer 01 — vanilla

**Goal: see the whole mechanic with zero moving parts.** One skill, two scripts, no
subagents, no web.

**Ingest.** The orchestrator does everything itself: copies one local note into raw, and then updates the wiki.

**Query** is read-only: `index.md` → a concept page → maybe a source page, and
`raw/` only if a page genuinely fails.

<img src="assets/progressive_disclosure_query.png" alt="Querying via progressive disclosure: the agent walks index.md, then a section index, then concept/entity pages, then source pages, and reaches raw/ only as a last resort" width="800"/>

**Run it** — [`01-llm-wiki-vanilla/demo.md`](01-llm-wiki-vanilla/demo.md):

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
/01-llm-wiki-vanilla what do my notes say about when to use an MCP server vs. a CLI?
```

## Layer 02 — ingest at scale

**Goal: remove the ceiling, and let anything with a URI become a source.**

**Ingest changes who reads.** Every page is written by a subagent defined as plain
markdown in `agents/`: `source_writer` reads one raw file.

<img src="assets/fan_out_parallelism.png" alt="Fan-out parallelism: each URI is fetched into raw/, read by its own source writer, aggregated by page writers, then the overview writer — the orchestrator only ever sees receipts" width="800"/>

Plus, adding support for GitHub repositories and web articles. Can be easily extended to other sources such as YouTube videos or Reddit threads.

<img src="assets/source_adapter_interface.png" alt="The adapter interface: every origin — local files, articles, repos, videos, threads — maps a URI through its own script to one raw artifact plus one receipt with the same fields" width="800"/>

**Run it** — [`02-llm-wiki-ingest/demo.md`](02-llm-wiki-ingest/demo.md):

```
/02-llm-wiki-ingest ingest ../data_input_examples/notes/02-medium/
/02-llm-wiki-ingest ingest https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course
/02-llm-wiki-ingest ingest https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design https://www.decodingai.com/p/the-coding-agent-loop
```

## Layer 03 — interactive

**Goal: make interaction a second way for the graph to grow.**

<img src="assets/interactive_llm_wiki_workflow.png" alt="The interactive workflow: every question leaves a question page; answers that earn it become notes; unanswerable questions land in open-questions.md; code questions produce a repo note that re-enters through ingest" width="800"/>

Capture user or agent interaction within the wiki (`questions/`, `notes/`,
`open-questions.md`) so the knowledge base grows organically as users interact with it.

We track all questions, create new notes as compositions of multiple concepts or entities, and keep track of open questions. Plus, growing notes based on repositories on top of the default ones.

**Run it** — [`03-llm-wiki-interactive/demo.md`](03-llm-wiki-interactive/demo.md):

```bash
cp -r examples/wiki-03-ai-engineering-before .
```

```
/03-llm-wiki-interactive when should I use an append-only log instead of updating rows in place?
/03-llm-wiki-interactive how do I decide that a fact in the memory has gone stale?
/03-llm-wiki-interactive in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?
```

---

## 📬 Learn more on LLM Wikis and agent memory

> Join 40k+ engineers reading [the Decoding AI Magazine](https://www.decodingai.com/) and watching [the Decoding AI YouTube channel](https://www.youtube.com/@itsdecodingai) to learn to design LLM wikis and advanced agent-memory techniques.

<a href="https://www.decodingai.com/" target="_blank">
  <img src="assets/decodingai.jpg" alt="Decoding AI Magazine" width="100%"/>
</a>

## Resources

| Resource | What it is |
|---|---|
| [Introducing the Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) | Google Cloud's introduction to OKF and why a shared shape for knowledge bundles matters. |
| [Open Knowledge Format (OKF) spec](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) | The spec the `wiki/` bundle aligns with: markdown + frontmatter, path is identity, the index is a rebuildable cache. `CONVENTIONS.md` §10 lists what we honour and where we diverge. |
| [Andrej Karpathy's `llm-wiki` gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | The idea file this pattern traces back to: an LLM that incrementally builds and maintains a persistent wiki, instead of re-deriving answers from raw documents on every query. |
| [Turn 10,994 Notes Into Memory](https://www.decodingai.com/p/llm-wiki-agent-memory) · [video](https://www.youtube.com/watch?v=ZRM_TfEZcIo) | The Decoding AI lesson behind this workshop — an LLM wiki as agent memory, run against a real 10,994-note corpus. |
| [LangChain's OpenWiki](https://github.com/langchain-ai/openwiki) | A CLI that writes and maintains agent documentation for your codebase — the same pattern, pointed at code. |

## Questions and troubleshooting

For any questions or issues open a [GitHub issue](https://github.com/decodingai-magazine/llm-wiki-workshop/issues)

## FAQ

**Do I need Claude Code?**
No. Any harness that can load a skill, read and write files, and run shell
commands works — nothing pins a model or a tool name. Layers 02–03 also want
subagents; without them, run the `agents/*.md` files as sequential prompts.

**Can I point it at my own notes?**
Yes — that is the point. Pass any directory of markdown to an ingest prompt, and
swap the URLs in `data_input_examples/*.md` for your own articles and repos. The
fixture exists only so every reader can reproduce the same wiki.

**Is Obsidian required?**
No — it is the inspection tool, not a dependency. Everything is plain markdown;
Obsidian's graph view just makes the threshold visible (hollow nodes are ideas
waiting for a second source).

## 👨‍🏫 Author

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="15%" align="center" style="border: none;">
      <a href="https://www.pauliusztin.ai/" target="_blank">
        <img src="https://github.com/iusztinpaul.png" width="100" style="border-radius: 50%;" alt="Paul Iusztin"/>
      </a>
      <br/>
      <b>Paul Iusztin</b>
    </td>
    <td width="85%" style="border: none;">
      Senior AI Engineer, Educator & Founder of Decoding AI. Author of the best-selling <a href="https://www.amazon.com/LLM-Engineers-Handbook-engineering-production/dp/1836200072">LLM Engineer's Handbook</a>.
    </td>
  </tr>
</table>

## ⭐ One more thing

If this workshop was useful, consider starring the repository so others can find
it too.

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Decoding AI](https://www.decodingai.com).
