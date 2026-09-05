# tool-stack

Search corpus of tools: websites, installable software, browser extensions, Homebrew casks, Android/iOS apps, AI apps, libraries, and agent skills.

The intended use is keyword search. A query like "grammar checker", "homebrew gui", or "remap android buttons" should return every entry that could answer it. Overlapping products stay in the list; the user picks.

`index.html` is a static search UI over `tools.json`. Missing logos render as a letter stamp.

## Files

- `tools.json` — every entry (id, name, url, logo, about, description, category, tags, platform, pricing, open_source). Sorted by name.
- `taxonomy.json` — allowed categories, tags, pricing tiers, and platforms. Add a tag here before using it in `tools.json`.
- `schema/` — JSON Schema for editor autocomplete (`python3 scripts/write_schema.py` after taxonomy changes).
- `index.html` — keyword search in the browser.
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
python3 -m http.server
# then open http://127.0.0.1:8000
```

After changing tags in `taxonomy.json`, regenerate editor schemas:

```sh
python3 scripts/write_schema.py
```

## Local hooks

```sh
brew install pre-commit
pre-commit install
```

Pushes and pull requests run the same validator in GitHub Actions.
