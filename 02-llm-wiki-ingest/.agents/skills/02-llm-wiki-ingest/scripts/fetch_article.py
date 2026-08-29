# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4>=4.12", "markdownify>=0.13"]
# ///
"""Fetch a web article into a wiki's raw/ layer as clean markdown.

Three jobs, in order: get the HTML (`curl`, with a browser user agent, because a
default python UA is blocked by most publishers), find the part of it that is
actually the article, and convert that fragment — not the whole page — to
markdown. Skipping the second step is what produces raw files full of nav menus
and cookie banners.

Identity is the raw path `raw/article-<slug>.md`, with the slug taken from the
last path segment of the URL (CONVENTIONS.md § Identity and dedup).

Usage:
  uv run --script fetch_article.py --url https://example.com/p/some-post --wiki-dir wiki-<slug>

Receipt (stdout):
  {"origin": "article", "original_path": <url>, "title", "subtitle", "source_url",
   "authors": [...], "published_date", "raw_path", "chars", ["warning"]}
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)

# Tried in order; the first hit wins. Publisher-specific selectors go first,
# generic HTML5 landmarks last — see SOURCES.md § How to add a source.
BODY_SELECTORS = ["article", "div.body.markup", "div.available-content", "main", "body"]

STRIP_TAGS = ["script", "style", "noscript", "nav", "footer", "form", "button", "svg", "iframe"]


def slugify(text: str, limit: int = 60) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return slug[:limit].rsplit("-", 1)[0] if len(slug) > limit else slug


def fetch(url: str) -> str:
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "60", "-A", USER_AGENT, url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise SystemExit(f"fetch failed for {url}: {result.stderr.strip() or 'empty response'}")
    return result.stdout


def meta(soup: BeautifulSoup, **attrs: str) -> str | None:
    tag = soup.find("meta", attrs=attrs)
    content = tag.get("content") if tag else None
    return content.strip() if content else None


def json_ld_field(soup: BeautifulSoup, *keys: str) -> str | None:
    """First non-empty value for any of `keys` anywhere in the page's JSON-LD blobs."""
    import json as _json

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            blobs = _json.loads(script.string or "")
        except (ValueError, TypeError):
            continue
        for blob in blobs if isinstance(blobs, list) else [blobs]:
            if not isinstance(blob, dict):
                continue
            for key in keys:
                value = blob.get(key)
                if isinstance(value, dict):
                    value = value.get("name")
                if isinstance(value, list) and value:
                    value = value[0].get("name") if isinstance(value[0], dict) else value[0]
                if isinstance(value, str) and value.strip():
                    return value.strip()
    return None


def extract_body(soup: BeautifulSoup) -> str:
    for tag in soup.find_all(STRIP_TAGS):
        tag.decompose()
    for selector in BODY_SELECTORS:
        node = soup.select_one(selector)
        if node and len(node.get_text(strip=True)) > 200:
            return markdownify(str(node), heading_style="ATX").strip()
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Article URL.")
    parser.add_argument("--wiki-dir", required=True, help="Path to wiki-<slug>/.")
    parser.add_argument("--output", default=None, help="Override the raw path (default: raw/article-<slug>.md).")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir).expanduser().resolve()
    if not (wiki_dir / "wiki").is_dir():
        raise SystemExit(f"not a wiki dir (no wiki/ inside): {wiki_dir}")

    soup = BeautifulSoup(fetch(args.url), "html.parser")

    title = meta(soup, property="og:title") or (soup.title.string.strip() if soup.title else args.url)
    subtitle_tag = soup.select_one("h3.subtitle")
    subtitle = (subtitle_tag.get_text(strip=True) if subtitle_tag else None) or meta(soup, property="og:description")
    author = meta(soup, name="author") or json_ld_field(soup, "author")
    published = (
        meta(soup, property="article:published_time")
        or json_ld_field(soup, "datePublished")
        or (soup.find("time", attrs={"datetime": True}) or {}).get("datetime")
    )
    body = extract_body(soup)

    slug = slugify(args.url.rstrip("/").rsplit("/", 1)[-1]) or slugify(title)
    raw_path = Path(args.output) if args.output else wiki_dir / "raw" / f"article-{slug}.md"
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    front = [
        "---",
        f"title: {json.dumps(title)}",
        f"subtitle: {json.dumps(subtitle) if subtitle else 'null'}",
        f"authors: {json.dumps([author] if author else [])}",
        f"published_date: {json.dumps(published) if published else 'null'}",
        f"source_url: {args.url}",
        "origin: article",
        f"fetched: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "---",
        "",
        f"# {title}",
        "",
    ]
    if subtitle:
        front += [f"*{subtitle}*", ""]
    raw_path.write_text("\n".join(front) + body + "\n")

    receipt = {
        "origin": "article",
        "original_path": args.url,
        "title": title,
        "subtitle": subtitle,
        "source_url": args.url,
        "authors": [author] if author else [],
        "published_date": published,
        "raw_path": str(raw_path.relative_to(wiki_dir)),
        "chars": len(body),
    }
    if len(body) < 500:
        receipt["warning"] = "body under 500 chars — paywall, bot wall, or an unmatched body selector"
        print(f"WARN: {receipt['warning']} ({args.url})", file=sys.stderr)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
