# tool-stack

Search corpus of tools: websites, installable software, browser extensions, Homebrew casks, Android/iOS apps, AI apps, libraries, and agent skills.

The intended use is keyword search. A query like "grammar checker", "homebrew gui", or "remap android buttons" should return every entry that could answer it. Overlapping products stay in the list; the user picks.

Data is JSON so a frontend can search and filter later (`category`, `tags`, `platform`, `pricing`). There is no app yet. Missing logos should render as a fallback in the UI, not a broken image.

## Files

- `tools.json` — every entry (id, name, url, logo, about, description, category, tags, platform, pricing, open_source). Sorted by name.
- `taxonomy.json` — allowed categories, tags, pricing tiers, and platforms. Add a tag here before using it in `tools.json`.
- `RULES.md` — schema, inclusion rules, tagging layers, and what not to add.
- `scripts/validate.py` — catalog checks used by pre-commit and CI.
- `scripts/sort_tools.py` — rewrite `tools.json` in name order.
- `scripts/search.py` — keyword search over the catalog.
- `LICENSE` — MIT.

## Adding an entry

Read `RULES.md` first. Then sort and validate:

```sh
python3 scripts/sort_tools.py
python3 scripts/validate.py
```

## Search

```sh
python3 scripts/search.py grammar checker
python3 scripts/search.py homebrew --platform mac
```

## Local hooks

```sh
pip install pre-commit
pre-commit install
```

Pushes and pull requests run the same validator in GitHub Actions.
