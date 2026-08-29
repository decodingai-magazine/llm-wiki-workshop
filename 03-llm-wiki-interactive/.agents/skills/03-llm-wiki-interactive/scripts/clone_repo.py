# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shallow-clone a git repo into a wiki's raw/ layer and report its HEAD SHA.

The clone is the **raw artifact** for a repo source, exactly as a copied note is
the raw artifact for a local one. It lands at

    <wiki-dir>/raw/repos/.github-<owner>-<repo>/

Dot-prefixed on purpose: Obsidian ignores dot-directories, so a 40 MB checkout
never shows up in the vault, the graph, or search. It is a **regenerable cache** —
deleting it is always safe, and re-ingesting the repo refreshes it in place rather
than skipping it (CONVENTIONS.md § Immutability).

Usage:
  uv run --script clone_repo.py --repo https://github.com/<owner>/<repo> --wiki-dir wiki-<slug>
  uv run --script clone_repo.py --repo <url> --wiki-dir <dir> --branch develop

Receipt (stdout):
  {"owner", "repo", "branch", "clone_path", "commit_sha", "action": "cloned"|"updated"}
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL_RE = re.compile(
    r"(?:https?://|git@)(?:www\.)?github\.com[/:]"
    r"(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+?)(?:\.git)?"
    r"(?:/(?:tree|blob)/(?P<branch>[^/\s?#]+))?/?$",
    re.IGNORECASE,
)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def parse_repo_url(url: str, branch_override: str | None) -> tuple[str, str, str | None]:
    """(owner, repo, branch) — branch is None when the URL does not pin one."""
    match = REPO_URL_RE.match(url.strip())
    if not match:
        raise SystemExit(f"not a recognizable GitHub repo URL: {url}")
    return match["owner"], match["repo"], branch_override or match["branch"]


def clone(clone_path: Path, clone_url: str, branch: str | None) -> None:
    clone_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth=1"]
    if branch:
        cmd += ["--branch", branch]
    run(cmd + [clone_url, str(clone_path)])


def update(clone_path: Path, branch: str) -> None:
    run(["git", "fetch", "--depth=1", "origin", branch], cwd=clone_path)
    run(["git", "checkout", branch], cwd=clone_path)
    run(["git", "reset", "--hard", f"origin/{branch}"], cwd=clone_path)


def current_branch(clone_path: Path) -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=clone_path).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repo URL (may include /tree/<branch>).")
    parser.add_argument("--wiki-dir", required=True, help="Path to wiki-<slug>/.")
    parser.add_argument("--branch", default=None, help="Branch override (default: the repo's default branch).")
    args = parser.parse_args()

    owner, repo, branch = parse_repo_url(args.repo, args.branch)
    wiki_dir = Path(args.wiki_dir).expanduser().resolve()
    if not (wiki_dir / "wiki").is_dir():
        raise SystemExit(f"not a wiki dir (no wiki/ inside): {wiki_dir}")

    clone_path = wiki_dir / "raw" / "repos" / f".github-{owner}-{repo}".lower()
    clone_url = f"https://github.com/{owner}/{repo}.git"

    if (clone_path / ".git").is_dir():
        action = "updated"
        try:
            update(clone_path, branch or current_branch(clone_path))
        except subprocess.CalledProcessError as err:
            print(f"warn: update failed ({err.stderr.strip()}), re-cloning", file=sys.stderr)
            shutil.rmtree(clone_path)
            clone(clone_path, clone_url, branch)
            action = "cloned"
    else:
        clone(clone_path, clone_url, branch)
        action = "cloned"

    print(
        json.dumps(
            {
                "owner": owner,
                "repo": repo,
                "branch": current_branch(clone_path),
                "clone_path": str(clone_path.relative_to(wiki_dir)),
                "commit_sha": run(["git", "rev-parse", "HEAD"], cwd=clone_path).stdout.strip(),
                "action": action,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
