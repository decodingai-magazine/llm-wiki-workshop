# SOURCES — the adapter contract

Layer 01 could ingest exactly one thing: a markdown file already on disk. This
layer can ingest anything, and the reason is a contract three lines long.

Everything downstream of `raw/` — source pages, the ≥2 threshold, entity and
concept pages, the overview, the index — is **origin-agnostic**. It never learns
where a source came from. That is what makes adding an origin cheap.

---

## The adapter contract

> **Input**: one URI.
> **Output**: exactly one artifact under `raw/`, plus one JSON receipt on stdout.

```json
{
  "origin": "local | article | youtube | repo",
  "original_path": "<the URI as given — provenance, §2.4 of CONVENTIONS.md>",
  "title": "<human title>",
  "source_url": "<url, or null for local files>",
  "authors": [],
  "published_date": "<ISO-8601, or null>",
  "raw_path": "raw/<...>"
}
```

Two shapes of adapter, distinguished only by what they leave on disk:

| Shape | Raw artifact | Read by |
|---|---|---|
| **File adapter** — local, article, youtube | one markdown file | `agents/source_writer.md` |
| **Tree adapter** — repo | one directory | `agents/repo_writer.md` |

The rest of the pipeline sees a page under `wiki/sources/` or `wiki/repos/`, and
both kinds carry the same frontmatter contract (`entities:`, `concepts:`), so both
feed the threshold identically.

## Routing table

Match the user's input top to bottom; first match wins.

| Input pattern | Adapter | Raw path | Writer |
|---|---|---|---|
| a path that exists on disk | `cp` | `raw/<slug>.md` | `source_writer` |
| `github.com/<owner>/<repo>`, or any `*.git` | `scripts/clone_repo.py` | `raw/repos/.github-<owner>-<repo>/` | `repo_writer` (mode `architecture`) |
| `youtube.com/watch?v=…`, `youtu.be/…` | `scripts/fetch_youtube.py` | `raw/youtube-<slug>.md` | `source_writer` |
| any other `http(s)://` | `scripts/fetch_article.py` | `raw/article-<slug>.md` | `source_writer` |

Dedup happens **before** the adapter runs: compute the raw path, `ls` it, skip if
it exists (CONVENTIONS.md §4). Repos are the exception — they refresh.

## Per-origin recipes

**local** — no script needed.

```bash
cp "<input path>" "wiki-<slug>/raw/<slug>.md"
```

**article** — `curl` with a browser user agent, isolate the body, markdownify.

```bash
uv run --script <skill>/scripts/fetch_article.py --url "<url>" --wiki-dir wiki-<slug>
```

If the receipt carries `"warning": "body under 500 chars…"`, **stop and tell the
user**: you hit a paywall, a bot wall, or an unmatched body selector. Writing a
source page from 300 characters of cookie banner is worse than not ingesting.

**repo** — shallow clone, then a different writer.

```bash
uv run --script <skill>/scripts/clone_repo.py --repo "<url>" --wiki-dir wiki-<slug>
```

The receipt's `action` is `cloned` or `updated`. Pass `clone_path`, `commit_sha`,
`branch`, `owner` and `repo` straight to `repo_writer`.

**youtube** — a skeleton that raises `NotImplementedError` on purpose. Running it
fails loudly with a pointer to the section below. That is the exercise.

## How to add a source — worked on YouTube

Three steps. Nothing outside this list changes.

1. **Write `scripts/fetch_<origin>.py`** honoring the contract above: one URI in,
   one raw artifact plus one receipt out. Decide the **identity** first — the raw
   path must be derivable from the URI alone and must not change when the title
   does. For YouTube that is the video id, not the title.
2. **Add one row to the routing table** in this file, and one line to Step 1.0 in
   `SKILL.md`.
3. **Pick the writer.** A markdown file → `source_writer`, unchanged. A directory
   or a fundamentally different artifact → a new agent modelled on
   `repo_writer.md`, emitting the same receipt shape.

That is the whole extension surface. The threshold, the page contracts, the index
and the log never learn that a new origin exists.

### What other origins would need

Described, not built — this is the design exercise, and the hard column is always
identity, never fetching.

| Origin | Fetch mechanism | Identity | The part that bites |
|---|---|---|---|
| **YouTube** | `youtube-transcript-api`, `yt-dlp --write-auto-sub`, or the Data API | video id | Auto-captions have no punctuation and no headings, so citations have nothing to anchor to — timestamped sections are the fix. |
| **X / Twitter** | official API (paid) or an export | tweet id; a thread is one source, not N | Deciding the unit: a thread reads as one document, but replies arrive later and change it. |
| **LinkedIn** | no usable API; a data export or manual paste | post URN | Terms of service, and posts that are edited in place under a stable URL. |
| **Reddit** | public JSON (`<url>.json`) | permalink id | The comments *are* the content — flatten the tree, or the source page cites nothing. |
| **Readwise** | Reader API | document id | Highlights are a partial view; the raw file is honestly incomplete and the source page should say so. |
| **Obsidian vault** | filesystem walk | vault-relative path | It already works — it is the `local` adapter — but embeds (`![[…]]`) and `[[wikilinks]]` point at files you did not ingest. |
| **PDF** | `pymupdf` / `pdftotext` | file hash or DOI | Scanned PDFs need OCR, and page numbers are the only citation anchor you get. |

The pattern across all of them: **fetching is a weekend; identity is the design
decision.** Pick a raw path that is stable under re-fetch and unique per source,
and the rest of the pipeline stays honest.
