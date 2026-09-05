#!/usr/bin/env python3
"""Generate JSON Schema files from taxonomy.json for editor autocomplete."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = ROOT / "taxonomy.json"
SCHEMA_DIR = ROOT / "schema"


def main() -> None:
    taxonomy = json.loads(TAXONOMY_PATH.read_text())
    SCHEMA_DIR.mkdir(exist_ok=True)

    tools_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/Mshardul/tool-stack/schema/tools.schema.json",
        "title": "tool-stack entries",
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": [
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
            ],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID v4, unique, never reused",
                },
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Official product name as branded",
                },
                "url": {
                    "type": "string",
                    "pattern": "^https://",
                    "description": "Canonical homepage, no tracking params",
                },
                "logo": {
                    "type": "string",
                    "description": "https:// URL, or empty for UI fallback",
                },
                "about": {
                    "type": "string",
                    "minLength": 1,
                    "description": "One-line summary",
                },
                "description": {
                    "type": "string",
                    "minLength": 1,
                    "description": "One paragraph, 2-4 sentences",
                },
                "category": {"type": "string", "enum": taxonomy["categories"]},
                "tags": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "enum": taxonomy["tags"]},
                },
                "platform": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "enum": taxonomy["platforms"]},
                },
                "pricing": {"type": "string", "enum": taxonomy["pricing"]},
                "open_source": {"type": "boolean"},
            },
        },
    }

    taxonomy_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/Mshardul/tool-stack/schema/taxonomy.schema.json",
        "title": "tool-stack taxonomy",
        "type": "object",
        "additionalProperties": False,
        "required": ["categories", "platforms", "pricing", "tags"],
        "properties": {
            "categories": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string"},
            },
            "platforms": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string"},
            },
            "pricing": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string"},
            },
            "tags": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string"},
            },
        },
    }

    (SCHEMA_DIR / "tools.schema.json").write_text(
        json.dumps(tools_schema, indent=2) + "\n"
    )
    (SCHEMA_DIR / "taxonomy.schema.json").write_text(
        json.dumps(taxonomy_schema, indent=2) + "\n"
    )
    print("Wrote schema/tools.schema.json and schema/taxonomy.schema.json")


if __name__ == "__main__":
    main()
