#!/usr/bin/env python3
"""Sort tools.json by name (case-insensitive)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "tools.json"


def main() -> None:
    tools = json.loads(TOOLS_PATH.read_text())
    tools.sort(key=lambda t: t["name"].casefold())
    TOOLS_PATH.write_text(json.dumps(tools, indent=2, ensure_ascii=True) + "\n")
    print(f"Sorted {len(tools)} entries in tools.json")


if __name__ == "__main__":
    main()
