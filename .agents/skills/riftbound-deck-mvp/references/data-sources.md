# Data sources and refresh policy

The default sync imports the `Wysme/riftbound-cards` Hugging Face dataset, a community mirror derived from the official gallery and errata. It stores card metadata and full original, corrected, and effective effect text locally; images are not downloaded.

For a private MVP, pin the resulting manifest and refresh deliberately. For a public or distributed product, use an approved Riot API key and follow Riot's Riftbound Digital Tools Policy, official-translation requirements, asset restrictions, and attribution requirements.

## Commands

```text
python scripts/riftbound.py sync
python scripts/riftbound.py sync --source path/to/cards.json
python scripts/riftbound.py info
```

Supported JSON shapes are a top-level list, `{ "cards": [...] }`, `{ "data": [...] }`, and the Hugging Face rows response. Array-valued fields may be actual arrays or JSON-encoded strings.

The importer writes a new SQLite file and replaces the old database only after the import succeeds. `data/cards.manifest.json` records source, row count, timestamp, and completeness.
