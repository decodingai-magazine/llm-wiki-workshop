# Example inputs

Everything the workshop ingests lives here. Pass paths/URLs to the layer skills relative to the layer directory (e.g. `../data_input_examples/notes/01-easy/`).

```
data_input_examples/
├── github_repositories.md   # repo URLs, ingested by the repo adapter (02+)
├── substack_articles.md     # article URLs, ingested by the article adapter (02+)
└── notes/
    ├── 01-easy/         # 5 notes  — one tight topic cluster (MCP vs. skills vs. CLIs)
    │   └── assets/      #  1 image  the notes embed
    ├── 02-medium/       # 10 notes — easy + 5 bridging notes (context layer, agent memory, GraphRAG, harness architecture)
    │   └── assets/      #  2 images
    └── 03-hard/         # 50 notes — everything, including short/noisy personal notes
        └── assets/      # 37 images + transcripts
```

## Scenarios

| Scenario | Notes | Fits layer 01 (cap 10, inline)? | What it shows |
|---|---|---|---|
| `01-easy` | 5 | yes | The core mechanic: source pages → ≥2-mention threshold → concept pages → overview → index. Heavy overlap, so several concept pages materialize from just 5 notes. |
| `02-medium` | 10 (⊇ 01-easy) | yes, exactly at the cap | Append + dedup (the 5 easy notes are skipped), cross-cluster concepts (MCP ↔ memory ↔ harness). |
| `03-hard` | 50 (⊇ 02-medium) | **no** — triggers the cap message | Why layer 02 exists: fan-out to subagents, and how the wiki copes with noise (tiny notes, meeting dumps, marketing drafts). |

The scenarios are nested: `01-easy ⊂ 02-medium ⊂ 03-hard`. A note's identity is its filename, so ingesting `02-medium/` after `01-easy/` skips the 5 shared notes instead of duplicating them.

Each tier carries **its own `assets/`** holding exactly the files its notes reference — a
sibling of the notes, so `![[assets/the-future-of-mcp-….png]]` resolves whether you open a
tier folder, `notes/`, or the repo root as your Obsidian vault. The tiers are nested, so this
costs ~1.2 MB over a single shared folder: `03-hard` needs all 37 files anyway, and the
smaller tiers add one and two.

Ingest copies a note **and the attachments it embeds** into the wiki's `raw/`, so the same
embeds keep working there (`raw/note.md` next to `raw/assets/`). Attachments are not sources:
they get no wiki page and never count toward the ≥2 threshold. Only `*.md` is ingested as a
source — which is why the three `.srt` transcripts in `03-hard/assets/` land in `raw/` and
stay unread. That is the workshop's standing exercise: write the adapter that reads them.
