# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Count how many distinct source-like pages mention each entity / concept slug.

This is the single source of truth for the wiki's materialization threshold:
an entity or concept page exists **iff at least `--threshold` (default 2)
distinct source-like pages list it** in their `entities:` / `concepts:`
frontmatter. Source-like pages are the pages written directly from an ingested
artifact — `wiki/sources/*.md` here.

The wikilinks are read from frontmatter, not from the body, so the count is a
cheap, deterministic frontmatter walk instead of a full-text scan.

Usage:
  uv run --script count_mentions.py --wiki-dir ../../../../wiki-<slug>
  uv run --script count_mentions.py --wiki-dir ... --threshold 2 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

# Globs (relative to the wiki bundle) whose pages count toward the threshold.
SOURCE_LIKE_GLOBS: list[str] = ["sources/*.md"]

KINDS: list[tuple[str, str]] = [("entities", "entity"), ("concepts", "concept")]


def parse_frontmatter(path: Path) -> dict[str, Any]:
    """YAML frontmatter of a markdown file; empty dict when absent or broken."""
    try:
        text = path.read_text()
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def slug_of(reference: Any) -> str:
    """Last path segment of a wikilink or path: "[[wiki/concepts/mcp]]" -> "mcp"."""
    text = str(reference).strip().strip("[]").split("|")[0].strip()
    if text.endswith(".md"):
        text = text[:-3]
    return text.rsplit("/", 1)[-1]


def source_like_pages(bundle: Path) -> list[Path]:
    pages: list[Path] = []
    for pattern in SOURCE_LIKE_GLOBS:
        pages += [p for p in bundle.glob(pattern) if p.is_file() and p.name != "index.md"]
    return sorted(pages)


def collect(bundle: Path) -> dict[str, dict[str, list[str]]]:
    """{kind: {slug: [pages that mention it]}} — pages are wiki-dir-relative, sorted."""
    mentions: dict[str, dict[str, set[str]]] = {key: {} for key, _ in KINDS}
    for page in source_like_pages(bundle):
        fm = parse_frontmatter(page)
        rel = f"wiki/{page.relative_to(bundle).as_posix()}"
        for key, _ in KINDS:
            for reference in fm.get(key) or []:
                slug = slug_of(reference)
                if slug:
                    mentions[key].setdefault(slug, set()).add(rel)
    return {key: {slug: sorted(pages) for slug, pages in sorted(value.items())} for key, value in mentions.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", required=True, help="Path to wiki-<slug>/ (the dir holding raw/, wiki/ and log.md).")
    parser.add_argument("--threshold", type=int, default=2, help="Mentions needed to materialize a page (default: 2).")
    parser.add_argument("--json", action="store_true", help="JSON only — suppress the human table on stderr.")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir).expanduser().resolve()
    bundle = wiki_dir / "wiki"
    if not bundle.is_dir():
        raise SystemExit(f"not a wiki dir (no wiki/ inside): {wiki_dir}")

    mentions = collect(bundle)
    qualifying = {
        key: [slug for slug, pages in mentions[key].items() if len(pages) >= args.threshold] for key, _ in KINDS
    }

    if not args.json:
        print(f"{'kind':<8} {'slug':<40} {'pages':>5}  qualifies", file=sys.stderr)
        for key, label in KINDS:
            for slug, pages in mentions[key].items():
                mark = "yes" if len(pages) >= args.threshold else ""
                print(f"{label:<8} {slug:<40} {len(pages):>5}  {mark}", file=sys.stderr)

    print(
        json.dumps(
            {
                "wiki_dir": str(wiki_dir),
                "threshold": args.threshold,
                "source_like_pages": len(source_like_pages(bundle)),
                "entities": mentions["entities"],
                "concepts": mentions["concepts"],
                "qualifying": qualifying,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
