# Local project data

The Hugging Face `Wysme/riftbound-cards` database, its source manifest and its
pre-RiftAtlas-enrichment backup were removed at the user's request on 2026-10-27.
There is currently no active `cards.sqlite`. Card lookup, transition loading and
deck validation/export require a newly imported compatible SQLite database or an
explicit `--db` path. Downloading a source JSON does not activate a replacement.

Retained data:

- `rules.json`: dated validation profile used by deck project operations.
- `sources/openrift/catalog.json`: downloaded multilingual OpenRift catalog;
  `download.json` records its URL, download time, hash and response metadata.
  This remains raw source data, not an imported SQLite database.
- `sources/rifthunt/`: downloaded bulk catalog, bulk index and set list.
- `sources/riftatlas/`: previously archived catalog and cost-renderer sources.

Existing Power synchronization and card-transition audit reports describe the
removed database. They are historical evidence, not validation of either new
source. `scripts/sync_riftatlas_power.py` only enriches an existing database; it
cannot recreate the removed database or import the new catalogs.

Deck projects, build sessions and revision history were preserved. No historical
database snapshots existed under `decks/.data_versions/` at cleanup time. Any
future snapshots there must remain immutable and must not be manually edited.

The documentation-only [card operator V1](../docs/card-operators.md) and
[per-card reading record](../docs/card-operator-reading.md) describe the fixed
OpenRift snapshot's 1,106 card bodies, including EN/SC/TC text variants and
catalog errata. This does not import a database or certify an executable mapping.
