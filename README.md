# tool-stack

Curated directory of useful websites, software, AI tools, and agent skills — structured as JSON data for a future frontend (search + filter by category/tags/platform/pricing).

## Files

- `tools.json` — the entries (180 so far). Each has id, name, url, logo, about, description, category, tags, platform, pricing, open_source.
- `taxonomy.json` — controlled vocabulary: allowed categories, tags, pricing tiers, platforms. Single source of truth — no tag/category may appear in `tools.json` that isn't here first.
- `RULES.md` — full schema definition, field-by-field rules, tagging layer system, and conventions for adding new entries.

## Status

Data-only right now — no frontend yet. Structure is designed so search/filter UI can be built later without reshaping the data.

## Adding an entry

See `RULES.md` before adding anything — it covers required fields, tag sourcing rules, and non-goals (no `added_date`, no local logo hosting, no CSV).
