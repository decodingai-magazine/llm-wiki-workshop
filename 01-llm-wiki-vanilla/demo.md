# Layer 01 — demo

Run from this directory (`cd 01-llm-wiki-vanilla && claude`). Every path below is
relative to it. Check the box after each step before moving on — the whole point
of the demo is watching the invariants hold.

A committed run of exactly these steps lives in `examples/wiki-ai-engineering/`.

---

## 1. First ingest — 5 notes

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
```

The skill has no wiki to find, so it proposes a slug. Accept `ai-engineering`.

**Verify**

- [ ] `wiki-ai-engineering/` exists with `raw/`, `wiki/`, `log.md`.
- [ ] `ls wiki-ai-engineering/raw | wc -l` → 5.
- [ ] `ls wiki-ai-engineering/wiki/sources | wc -l` → 6 (5 pages + the generated `index.md`).
- [ ] Pages appeared for every slug that ≥2 of the five notes engage with. In the
      reference run that is 5 entities (`mcp`, `claude-code`, `fastmcp`, `prefect`,
      `anthropic`) and 11 concepts (`agent-skills`, `cli-tools`,
      `connectivity-stack`, `mcp-primitives`, and 7 more). Your run will differ a
      little — the slugs are the model's judgment call, the **threshold** is not.
- [ ] `wiki/overview.md` and `wiki/index.md` exist; `log.md` has exactly one `## ` entry.
- [ ] Open a source page: every claim ends in a `[[raw/...|cite]]`, and the only
      unsourced line is the `> Synthesis:` one.

```bash
uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/count_mentions.py --wiki-dir wiki-ai-engineering
```

Every slug in `qualifying` has a page; nothing else does. That is the ≥2 threshold,
enforced.

## 2. Append — 10 notes, 5 of them already ingested

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/02-medium/
```

`02-medium/` **contains** `01-easy/` — the same five files, in a different
directory. Identity is the raw path, not the path you typed.

**Verify**

- [ ] The report names 5 skipped notes, each with the `original_path` it was first
      seen at (`.../notes/01-easy/...`), and 5 ingested.
- [ ] `ls wiki-ai-engineering/raw | wc -l` → 10, not 15.
- [ ] New pages bridge the two clusters — in the reference run: `context-layer`,
      `knowledge-graph`, `agent-memory`, `hybrid-search`, `progressive-disclosure`,
      `programmatic-tool-calling`, `durable-execution`, plus the entities `mongodb`
      and `david-soria-parra`. The wiki just connected notes that never mention
      each other.
- [ ] Some of those were **hollow nodes** after step 1 — `knowledge-graph` and
      `agent-memory` sat at one mention until the new notes arrived. Promissory
      links resolving is the wiki learning something.
- [ ] At least one qualifying page was deliberately *not* rewritten
      (`server-side-orchestration` in the reference run): it was already at ≥2 and
      no new source touched it, so there was nothing to update.
- [ ] A concept page that existed after step 1 now has more entries under
      `sources:` and a higher `source_count`, but the **same `created`** timestamp.
- [ ] `log.md` has two entries, oldest first.

## 3. Re-run the same ingest — idempotency

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/02-medium/
```

**Verify**

- [ ] All 10 skipped. No source page rewritten, no concept page touched.
- [ ] The index is byte-identical to before:

```bash
cp -r wiki-ai-engineering/wiki /tmp/wiki-before
uv run --script .agents/skills/01-llm-wiki-vanilla/scripts/build_index_md.py --wiki-dir wiki-ai-engineering
diff -r /tmp/wiki-before wiki-ai-engineering/wiki && echo "identical"
```

- [ ] `log.md` has three entries — the run happened, it just changed nothing.

## 4. Hit the wall — 50 notes

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/03-hard/
```

**Verify**

- [ ] The skill refuses: 40 new notes against a cap of 10, with the reason stated.
- [ ] **Nothing was written** — no raw copies, no pages, and no `log.md` entry.
      `git status` (or `ls raw | wc -l` → still 10) confirms it.

This is the hand-off. The cap is not arbitrary: this layer reads every note into
one context, and one context is a hard ceiling. Layer 02 spends one subagent per
note and the ceiling disappears.

## 5. Query it

```
/01-llm-wiki-vanilla what do my notes say about when to use an MCP server vs. a CLI?
```

**Verify**

- [ ] The answer walks the ladder: index → concept page → maybe a source page. It
      should not need `raw/` at all.
- [ ] Every claim carries a `[[wikilink]]`, and the answer ends with `Pages used:`.
- [ ] Only `log.md` changed (`git status` inside the wiki dir, or check timestamps).
- [ ] Ask something the notes do not cover ("what do my notes say about vector
      index tuning?") — the honest answer is "the wiki doesn't cover this",
      not an invention.

## 6. Look at it in Obsidian

Open `01-llm-wiki-vanilla/` as a vault (or the `wiki-ai-engineering/` dir itself —
the wikilinks resolve either way).

**Verify**

- [ ] Graph view: hub-and-spoke clusters around concept pages, with source pages
      as the spokes.
- [ ] **Hollow nodes** = promissory links: slugs mentioned by exactly one source.
      They are the wiki's to-do list, and they fill themselves in as you ingest.
- [ ] Follow `wiki/index.md → concepts/index.md → a concept → a source → raw`.
      Four clicks from "what do I know" to "who said it".

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering
```

Nothing else in the layer holds state.
