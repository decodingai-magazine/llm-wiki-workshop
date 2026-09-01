# Layer 01 — demo

Run from this directory (`cd 01-llm-wiki-vanilla && claude`). Paths are relative
to it. You only type prompts — the skill runs every script itself.

`examples/wiki-ai-engineering/` is a committed run of these steps, so you can read
the output before producing your own.

---

## 1. Ingest 5 notes

```
/01-llm-wiki-vanilla ingest ../data_input_examples/notes/01-easy/
```

No wiki exists yet, so the skill proposes a slug. Accept `ai-engineering`.

**Verify**

- [ ] `wiki-ai-engineering/wiki/` has a page for every slug that ≥2 of the five
      notes engage with — and nothing else. The report names them, plus the slugs
      waiting at exactly 1 mention. (Reference run: 4 entities, 5 concepts, 3
      waiting. Yours will differ a little — the slugs are the model's judgment
      call; the threshold is not.)

## 2. Query it

#### Question 1

```
/01-llm-wiki-vanilla what do my notes say about when to use an MCP server vs. a CLI?
```

#### Question 2

```
/01-llm-wiki-vanilla how should I integrate skills into MCP servers?
```

#### Question 3

```
/01-llm-wiki-vanilla what is the right way of building MCP servers?
```


**Verify**

- [ ] Every claim carries a `[[wikilink]]`, the answer ends with `Pages used:`,
      and the only file that changed is `log.md`.

## 3. Look at it in Obsidian

Open `wiki-ai-engineering/` as a vault.

**Verify**

- [ ] Graph view: hub-and-spoke clusters around concept pages, with **hollow
      nodes** — slugs mentioned by exactly one source. That is the wiki's to-do
      list; they fill themselves in as you ingest more.
- [ ] Open `raw/the-future-of-mcp-….md`: the image renders, because `raw/assets/`
      travelled with the note.

---

## If you want to start over

```bash
rm -rf wiki-ai-engineering
```

Nothing else in the layer holds state.

Curious about the cap? `ingest ../data_input_examples/notes/03-hard/` and the
skill refuses: 40 new notes against a ceiling of 10, nothing written. This layer
reads every note into one context, and one context is a hard ceiling — layer 02
exists to remove it.
