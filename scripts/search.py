#!/usr/bin/env python3
"""Keyword search over tools.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "tools.json"


def tokenize(text: str) -> list[str]:
    return [t for t in text.casefold().split() if t]


def score(entry: dict, terms: list[str]) -> int:
    name = entry["name"].casefold()
    tags = [t.casefold() for t in entry.get("tags") or []]
    about = (entry.get("about") or "").casefold()
    description = (entry.get("description") or "").casefold()
    blob = f"{about} {description}"

    total = 0
    for term in terms:
        if name == term:
            total += 100
        elif name.startswith(term):
            total += 40
        elif term in name:
            total += 25
        if term in tags:
            total += 20
        if term in about:
            total += 8
        elif term in blob:
            total += 4
    return total


def search(
    tools: list[dict],
    query: str,
    category: str | None = None,
    platform: str | None = None,
    limit: int = 20,
) -> list[tuple[int, dict]]:
    terms = tokenize(query)
    if not terms:
        return []

    hits: list[tuple[int, dict]] = []
    for entry in tools:
        if category and entry.get("category") != category:
            continue
        if platform and platform not in (entry.get("platform") or []):
            continue
        points = score(entry, terms)
        if points > 0:
            hits.append((points, entry))

    hits.sort(key=lambda item: (-item[0], item[1]["name"].casefold()))
    return hits[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the tool-stack catalog")
    parser.add_argument("query", nargs="+", help="search keywords")
    parser.add_argument("--category", choices=["website", "software", "ai-tool", "skill"])
    parser.add_argument("--platform", choices=["web", "windows", "mac", "linux", "ios", "android"])
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    tools = json.loads(TOOLS_PATH.read_text())
    hits = search(tools, " ".join(args.query), args.category, args.platform, args.limit)

    if not hits:
        print("No matches")
        return 1

    for points, entry in hits:
        print(f"{entry['name']}")
        print(f"  {entry['category']} · {entry['about']}")
        print(f"  {entry['url']}")
        print()
    print(f"{len(hits)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
