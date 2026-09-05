# tool-stack

Search corpus of tools: websites, installable software, browser extensions, Homebrew casks, Android/iOS apps, AI apps, libraries, and agent skills.

The intended use is keyword search. A query like "grammar checker", "homebrew gui", or "remap android buttons" should return every entry that could answer it. Overlapping products stay in the list; the user picks.

Data is JSON so a frontend can search and filter later (`category`, `tags`, `platform`, `pricing`). There is no app yet.

## Files

- `tools.json` — every entry (id, name, url, logo, about, description, category, tags, platform, pricing, open_source).
- `taxonomy.json` — allowed categories, tags, pricing tiers, and platforms. Add a tag here before using it in `tools.json`.
- `RULES.md` — schema, inclusion rules, tagging layers, and what not to add.

## Adding an entry

Read `RULES.md` first.
