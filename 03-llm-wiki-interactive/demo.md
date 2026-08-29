# Layer 03 — demo

Run from this directory (`cd 03-llm-wiki-interactive && claude`). Paths are
relative to it. You only type prompts.

**Start point.** `examples/wiki-ai-engineering/` is layer 02's end state — 50
notes, one repo, two articles: 53 source-like pages, 10 entities, 38 concepts —
with nothing asked of it yet. Copy it:

```bash
cp -r examples/wiki-ai-engineering .
```

The repo clone is not part of it (`raw/repos/` is gitignored, ~100 MB). The skill
clones it by itself the first time a question needs the code.

---

## 1. A question the wiki can answer

```
/03-llm-wiki-interactive when should I use an append-only log instead of updating rows in place?
```

**Verify**

- [ ] `wiki/questions/<date>-….md` (a slim pointer) and `wiki/notes/<slug>.md`
      (the answer, every claim citing a wiki page — never `raw/`) both exist, and
      no ingest-owned page changed.

## 2. The same question, asked differently

```
/03-llm-wiki-interactive is event sourcing actually worth it for a personal knowledge graph?
```

**Verify**

- [ ] A second question page and **no second note** — the existing note was
      enriched in place: `spawned_by_question` has two entries, `created` is
      unchanged. Referencing over duplication is what keeps this from becoming a
      chat log.

## 3. A question the wiki cannot answer

```
/03-llm-wiki-interactive how do I decide that a fact in the memory has gone stale?
```

**Verify**

- [ ] The answer says plainly that the wiki does not cover this, and says what it
      *does* have (a mechanism — the log — but no policy); `wiki/open-questions.md`
      gained a dated entry, and no note was written.

## 4. A question that needs the code

```
/03-llm-wiki-interactive in the coding agent repo, how does a tool call actually get routed to the permission gate, and what happens while it waits for the human?
```

The skill reads `ARCHITECTURE.md` first, finds it covers the policy but not the
routing, clones the repo, and spawns `repo_writer` in question mode.

**Verify**

- [ ] `wiki/repos/<repo>/<slug>.md` exists (`type: repo_note`, evidence as
      `file:line` with permalinks pinned to the SHA) **and the ingest tail ran**:
      at least one concept page now lists it under `sources:`. An answer became
      evidence — through exactly the machinery an ingest uses.

## 5. A second question about the same code

```
/03-llm-wiki-interactive in the coding agent repo, how does the agent spawn a subagent, and what does the parent actually get back when it finishes?
```

**Verify**

- [ ] A second repo note beside the first — one page per question, both
      source-like — and `wiki/repos/index.md` lists both under the repo. The
      codebase is now answering questions the architecture page never anticipated.

## 6. Flag an open question

```
/03-llm-wiki-interactive log this as open: what actually goes into a coding agent's context window each turn?
```

**Verify**

- [ ] `open-questions.md` has a second entry, marked as flagged by you. Nothing
      resolves it automatically: the next ingest whose sources appear to address
      it says so in its report, and a human decides.

## 7. Read the trail

Open `wiki-ai-engineering/log.md` and `wiki/questions/index.md`, then the vault
in Obsidian.

**Verify**

- [ ] The log reads as one history, oldest first, and the questions index is one
      line per question — enough to answer "have I asked this before?" without
      opening anything. In the graph, the notes and repo notes hang off the
      concept pages they cite.

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering && cp -r examples/wiki-ai-engineering .
```
