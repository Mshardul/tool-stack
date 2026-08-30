# Tools Directory — Rules & Conventions

Curated list of websites, software, AI tools, and agent skills. Structured data for future FE (search + filter by tags/category).

## Files

- `RULES.md` — this file.
- `taxonomy.json` — controlled vocabulary: categories, tags, pricing values, platform values.
- `tools.json` — the actual entries.

## Entry Schema (`tools.json`)

```json
{
  "id": "uuid",
  "name": "string",
  "url": "string",
  "logo": "string (external URL, for now)",
  "about": "string — 1 line, punchy summary",
  "description": "string — 1 paragraph, fuller explanation",
  "category": "string — must exist in taxonomy.json > categories",
  "tags": ["string", "... — each must exist in taxonomy.json > tags"],
  "platform": ["string", "... — must exist in taxonomy.json > platforms"],
  "pricing": "free | freemium | paid",
  "open_source": true
}
```

## Field Rules

- **id**: UUID v4, generated per entry, never reused.
- **name**: official product name, as branded (e.g. "WolframAlpha" not "Wolfram Alpha").
- **url**: canonical homepage URL, `https://`, no tracking params.
- **logo**: external hotlink for now (no local hosting yet — revisit when FE app built).
- **about**: one line. No period at end unless multi-clause. Punchy, not marketing copy.
- **description**: one paragraph (2–4 sentences). What it does, who it's for, standout trait.
- **category**: single value, not array. Must exist in `taxonomy.json`. `website` = you visit it. `software` = you install/run it. `ai-tool` = the product *is* an AI app (Cursor, Perplexity). `skill` = an installable agent skill, skill pack, or prompt pack that runs *inside* an AI app.
- **tags**: array, as many as apply, pulled ONLY from `taxonomy.json`. See tagging layers below.
- **platform**: array. Websites → `["web"]`. Software → all platforms it actually runs on.
- **pricing**: describes cost tier, not license. `free` = no paid tier exists. `freemium` = free tier + paid upgrade. `paid` = no usable free tier.
- **open_source**: boolean, separate from pricing. Open source tool can still be paid (hosted/managed version).

## Tagging Layers

Tag each entry across as many applicable layers as make sense — not just one:

1. **Function/purpose** — what it does. `photo-editing`, `file-transfer`, `price-tracking`, `malware-scan`, `weather-map`, `computation`
2. **Domain/industry** — broader field. `design`, `security`, `productivity`, `finance`, `shopping`, `dev-tools`, `entertainment`
3. **Company/maker** — `google`, `microsoft`, `adobe`, `wolfram`. Skip if no clear maker (indie/anonymous tools).
4. **Audience/use-case** — `developer`, `designer`, `student`, `researcher`, `general-consumer`
5. **Access/usage trait** — `no-signup`, `browser-only`, `offline-capable`, `extension` (usage pattern, not price — that's the `pricing` field)
6. **Tech trait** — `ai-powered`, `self-hosted`, `cross-platform`
7. **Alternative-to** — what it replaces. `photoshop-alternative`, `airdrop-alternative` — key for discovery
8. **Form factor** — how it ships, when it is not a standalone app. `agent-skill` (one skill), `skill-pack` (a repo of skills), `marketplace` (plugin/skill directory), `mcp` (MCP server), `library` (importable SDK), `prompt-library`

## Taxonomy Update Rule

`taxonomy.json` is the single source of truth for allowed `category`, `tags`, `pricing`, `platform` values.

**Before adding any entry:**
1. Check every tag/category you want to use against `taxonomy.json`.
2. New tag needed? Add it to `taxonomy.json` FIRST, then use it in the entry.
3. Never write a tag/category into `tools.json` that doesn't exist in `taxonomy.json`. No drift, no near-duplicate tags (e.g. `photo-editing` vs `photo-editor` — pick one, stick to it).

## Non-Goals (for now)

- No `added_date` field.
- No local logo hosting.
- No CSV — JSON only (tags/platform need arrays, future fields may nest).
