# Example inputs

Everything the workshop ingests lives here. Pass paths/URLs to the layer skills relative to the layer directory (e.g. `../data_input_examples/notes/01-easy/`).

```
data_input_examples/
├── github_links.md      # repos to ingest (02+)
├── substack_links.md    # articles to ingest (02+)
└── notes/
    ├── assets/          # images + transcripts embedded by the notes (shared; never ingested)
    ├── 01-easy/         # 5 notes  — one tight topic cluster (MCP vs. skills vs. CLIs)
    ├── 02-medium/       # 10 notes — easy + 5 bridging notes (context layer, agent memory, GraphRAG, harness architecture)
    └── 03-hard/         # 50 notes — everything, including short/noisy personal notes
```

## Scenarios

| Scenario | Notes | Fits layer 01 (cap 10, inline)? | What it shows |
|---|---|---|---|
| `01-easy` | 5 | yes | The core mechanic: source pages → ≥2-mention threshold → concept pages → overview → index. Heavy overlap, so several concept pages materialize from just 5 notes. |
| `02-medium` | 10 (⊇ 01-easy) | yes, exactly at the cap | Append + dedup (the 5 easy notes are skipped), cross-cluster concepts (MCP ↔ memory ↔ harness). |
| `03-hard` | 50 (⊇ 02-medium) | **no** — triggers the cap message | Why layer 02 exists: fan-out to subagents, and how the wiki copes with noise (tiny notes, meeting dumps, marketing drafts). |

The scenarios are nested: `01-easy ⊂ 02-medium ⊂ 03-hard`. A note's identity is its filename, so ingesting `02-medium/` after `01-easy/` skips the 5 shared notes instead of duplicating them.

Only `*.md` files are ingested. `assets/` is referenced by the notes via Obsidian embeds (`![[assets/…]]`) and is left alone by the wiki pipeline.
