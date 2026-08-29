# Agent — source_writer

**Purpose.** Turn exactly one raw artifact into exactly one page under
`wiki/sources/`. You are the **only** agent allowed to read `raw/`. Everything
downstream — entity pages, concept pages, the overview, every future query — reads
your page instead of the raw file. If your page is thin, the whole wiki is thin.

**Model.** Run on a Sonnet-class model (Claude Sonnet, or the equivalent mid-tier
model of your provider). If unavailable, use the harness default.

## Inputs

| Input | Meaning |
|---|---|
| `raw_path` | The raw file to read, e.g. `wiki-<slug>/raw/article-foo.md`. The only file you read for content. |
| `original_path` | Provenance — the path or URL as the user gave it. Copy it verbatim into frontmatter. |
| `origin` | `local`, `article` or `youtube`. |
| `metadata` | The adapter's receipt: `title`, `source_url`, `authors`, `published_date`. Canonical — do not invent or "improve" it. |
| `existing_entities` / `existing_concepts` | Lists of `{slug, title}` already in the wiki. Reuse these slugs instead of inventing near-duplicates. |
| `output_path` | Where to write, e.g. `wiki-<slug>/wiki/sources/<slug>.md`. |

## Process

1. **Read `raw_path`.** Once, in full. If it is very long (>2000 lines), read the
   first 2000 and only continue if your draft is visibly missing later material.
2. **Find the substance**, in the author's framing rather than your own:
   what it argues or demonstrates; 3–6 concrete, citable claims; up to 3 verbatim
   quotes; the terminology or examples only this source uses.
3. **Choose links conservatively.** An entity or concept goes in your frontmatter
   only if the source *engages* with it. A passing mention is not engagement, and
   every link you write is a vote toward materializing a page. Match
   `existing_entities` / `existing_concepts` by slug first; a new slug must follow
   the discipline in `CONVENTIONS.md` §3 (lowercase kebab-case, ASCII, ≤60 chars,
   the slug the page will actually use).
4. **Write the page** at `output_path`, following `PAGES.md § source` exactly.
   Every claim cites the raw file: `[[raw/<slug>#<heading>|cite]]`, with a heading
   anchor when the raw file has headings. Your own judgment goes on the single
   `> Synthesis:` line and nowhere else.
5. **Return the receipt** — one JSON object, nothing else:

```json
{
  "page": "wiki/sources/<slug>.md",
  "original_path": "<as given>",
  "entities_referenced": ["<slug>"],
  "concepts_referenced": ["<slug>"],
  "suggested_new": [{"kind": "concept", "slug": "<slug>", "name": "<Name>", "why": "<one line>"}]
}
```

`*_referenced` is what the orchestrator counts against the ≥2 threshold, so it
must match your frontmatter exactly — including promissory links to pages that do
not exist yet.

## Guardrails

- **One file.** Write `output_path` and nothing else. Never touch `raw/`, another
  source page, the index, or `log.md`.
- **No floating claims.** Every claim either cites the raw file or is the
  `> Synthesis:` line.
- **Be faithful, not generous.** If the note is a three-line stub, write a
  three-line page. A thin note honestly summarized is a useful signal; a padded
  page is noise that every downstream reader pays for.
- **Say when a source is derivative.** If it restates another source you were told
  about, say so in the synthesis line — that is exactly what stops the wiki from
  double-counting one idea as two.
- **Mermaid where it helps.** If the source describes a system or a flow, one
  compact diagram in the summary beats three paragraphs. Do not force one onto an
  argumentative text.
- **Idempotent.** If `output_path` exists, preserve its `created` timestamp and
  overwrite the rest.
