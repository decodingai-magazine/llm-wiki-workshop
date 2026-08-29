# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Fetch a YouTube transcript into a wiki's raw/ layer. **Workshop exercise — not implemented.**

This file is a deliberate blank with the contract filled in, because the point of
`SOURCES.md` is that adding an origin is a three-step job and you should be able
to see all three steps from here.

What a real implementation owes the pipeline (SOURCES.md § Adapter contract):

  1. Parse the video id from the URL (`youtube.com/watch?v=<id>`, `youtu.be/<id>`)
     and use it as the identity: the raw path is `raw/youtube-<slug>.md`, where the
     slug comes from the video id — NOT from the title, which changes.
  2. Fetch the transcript (youtube-transcript-api, yt-dlp `--write-auto-sub`, or the
     Data API) plus the metadata: title, channel, publish date, duration.
  3. Write ONE markdown file at the raw path: frontmatter
     (`title, authors, published_date, source_url, origin: youtube, fetched`),
     then `# <title>`, then the transcript — timestamped sections if the transcript
     has them, so a source page can cite `[[raw/youtube-<slug>#12:30|cite]]`.
  4. Print the receipt on stdout:
     {"origin": "youtube", "original_path": <url>, "title", "source_url",
      "authors": [...], "published_date", "raw_path": "raw/youtube-<slug>.md"}

Nothing downstream changes. `source_writer` reads the raw file the same way it
reads a copied note, and the ≥2 threshold never learns where the source came from.

Usage (once implemented):
  uv run --script fetch_youtube.py --url https://www.youtube.com/watch?v=<id> --wiki-dir wiki-<slug>
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="YouTube video URL.")
    parser.add_argument("--wiki-dir", required=True, help="Path to wiki-<slug>/.")
    parser.parse_args()

    raise NotImplementedError(
        "Workshop exercise: implement this adapter per SOURCES.md § How to add a source. "
        "The contract is in this file's docstring; nothing downstream of the raw file changes."
    )


if __name__ == "__main__":
    main()
