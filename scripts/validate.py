#!/usr/bin/env python3
"""Validate tools.json against taxonomy.json and RULES.md."""

from __future__ import annotations

import json
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "tools.json"
TAXONOMY_PATH = ROOT / "taxonomy.json"

REQUIRED_FIELDS = (
    "id",
    "name",
    "url",
    "logo",
    "about",
    "description",
    "category",
    "tags",
    "platform",
    "pricing",
    "open_source",
)

TRACKING_QUERY = re.compile(
    r"(^|&)(utm_[^=]+|fbclid|gclid|ref|mc_cid|mc_eid)=",
    re.IGNORECASE,
)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"ERROR: cannot parse {path.name}: {exc}")


def main() -> int:
    errors: list[str] = []
    taxonomy = load_json(TAXONOMY_PATH)
    tools = load_json(TOOLS_PATH)

    if not isinstance(taxonomy, dict):
        errors.append("taxonomy.json must be an object")
        _report(errors)
        return 1
    if not isinstance(tools, list):
        errors.append("tools.json must be an array")
        _report(errors)
        return 1

    categories = set(taxonomy.get("categories") or [])
    platforms = set(taxonomy.get("platforms") or [])
    pricing_vals = set(taxonomy.get("pricing") or [])
    tags_allowed = set(taxonomy.get("tags") or [])

    ids: dict[str, str] = {}
    names: dict[str, str] = {}
    urls: dict[str, str] = {}
    names_in_order: list[str] = []

    for i, entry in enumerate(tools):
        loc = f"tools.json[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{loc}: entry must be an object")
            continue

        name = entry.get("name", loc)
        loc = f"{name!r}"

        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{loc}: missing field {field}")

        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            errors.append(f"{loc}: id must be a non-empty string")
        else:
            try:
                parsed = uuid.UUID(entry_id)
            except ValueError:
                errors.append(f"{loc}: id is not a valid UUID")
            else:
                if parsed.version != 4:
                    errors.append(f"{loc}: id must be UUID v4")
                if entry_id in ids:
                    errors.append(f"{loc}: duplicate id (also {ids[entry_id]})")
                else:
                    ids[entry_id] = loc

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{loc}: name must be a non-empty string")
        else:
            names_in_order.append(name)
            key = name.casefold()
            if key in names:
                errors.append(f"{loc}: duplicate name (also {names[key]})")
            else:
                names[key] = loc

        url = entry.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append(f"{loc}: url must start with https://")
        else:
            if TRACKING_QUERY.search(url.split("?", 1)[-1] if "?" in url else ""):
                errors.append(f"{loc}: url has tracking params")
            if "/a/" in url and "gumroad.com" in url:
                errors.append(f"{loc}: url looks like an affiliate link")
            url_key = url.rstrip("/").casefold()
            if url_key in urls:
                errors.append(f"{loc}: duplicate url (also {urls[url_key]})")
            else:
                urls[url_key] = loc

        logo = entry.get("logo")
        if not isinstance(logo, str):
            errors.append(f"{loc}: logo must be a string (empty allowed)")
        elif logo and not logo.startswith("https://"):
            errors.append(f"{loc}: logo must be empty or an https:// URL")

        for text_field in ("about", "description"):
            value = entry.get(text_field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{loc}: {text_field} must be a non-empty string")

        category = entry.get("category")
        if category not in categories:
            errors.append(f"{loc}: category {category!r} not in taxonomy.json")

        tags = entry.get("tags")
        if not isinstance(tags, list) or not tags:
            errors.append(f"{loc}: tags must be a non-empty array")
        else:
            seen_tags: set[str] = set()
            for tag in tags:
                if tag not in tags_allowed:
                    errors.append(f"{loc}: tag {tag!r} not in taxonomy.json")
                if tag in seen_tags:
                    errors.append(f"{loc}: duplicate tag {tag!r}")
                seen_tags.add(tag)

        platform = entry.get("platform")
        if not isinstance(platform, list) or not platform:
            errors.append(f"{loc}: platform must be a non-empty array")
        else:
            seen_plat: set[str] = set()
            for item in platform:
                if item not in platforms:
                    errors.append(f"{loc}: platform {item!r} not in taxonomy.json")
                if item in seen_plat:
                    errors.append(f"{loc}: duplicate platform {item!r}")
                seen_plat.add(item)

        pricing = entry.get("pricing")
        if pricing not in pricing_vals:
            errors.append(f"{loc}: pricing {pricing!r} not in taxonomy.json")

        if "open_source" in entry and not isinstance(entry["open_source"], bool):
            errors.append(f"{loc}: open_source must be a boolean")

    if names_in_order != sorted(names_in_order, key=str.casefold):
        errors.append(
            "tools.json is not sorted by name. Run: python scripts/sort_tools.py"
        )

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print(f"{len(errors)} validation error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
