# Riftbound Deck MVP Roadmap

This file tracks delivery status and remaining work. Workflow details live in the linked documents; a written requirement is not an implemented check.

## TODO 1: Manage each deck as a project

**Status:** Implemented MVP. [Commands and storage contract](docs/deck-projects.md), `scripts/deck_projects.py`.

Supports stable project identity, revision reasons/diffs, saved rules/card data, copying, archiving and restoration. Verification reproduces saved validation/export results; it does not establish that the validator covers every rule or that a deck is strong.

## TODO 2: Player match feedback and deck adjustment

**Depends on:** TODO 1.

**Status:** Planned, after the construction experience is stable.

- Attach player-supplied match context, result and qualitative observations to the exact deck revision; keep observations distinct from inferences.
- Propose a before/after diff with reasons linked to feedback, tradeoffs and affected matchups or game-plan stages. Repeated reports are signals, not proof of statistical strength.
- Activate changes only after player acceptance and validation; preserve previous revisions for comparison and rollback.
- Store only intentionally supplied feedback; do not scrape clients, automate gameplay or infer player identity.

Acceptance: in a later session, recover the feedback and trace each proposed change to its evidence and originating revision.

## TODO 3: Guided deckbuilding workflow

**Priority:** Current focus. [Pipeline specification](docs/deckbuilding-pipeline.md).

**Implemented:** Stage persistence, history snapshots and extensible state storage. Module recording is an Agent convention, not a dedicated checked schema.

**Retrieval foundation:** `BaseRetriever` and a local `KeywordRetriever` share typed requests, color/other filters and paginated ID-only results. Full card information is read on demand by ID. `retrieve` replaces the old search/style-scoring interfaces. [Contract and extension guide](.agents/skills/riftbound-deck-mvp/references/retrieval.md). This is literal discovery, not semantic retrieval or candidate-quality evaluation.

Remaining work:

- Module operations, dependency review, lock/rejection consistency and protection against state loss.
- Better candidate discovery and whole-deck checks for support density, curve and resources.
- Validator boundary coverage, including the known single-battlefield-entry quantity loophole.
- Real conversational trials for style-first, hero-first and conflicting hero/style requests.

Acceptance: players finish and resume these trials without CLI knowledge; selected cards have evidence-based reasons, player constraints survive revisions, and issues are disclosed before export. Existing fixture-based smoke tests establish command behavior only.

## TODO 4: 可视化解释套牌玩法

**Status:** Deferred until construction is stable; scheduled after TODO 2.

- Agent-authored `guide.json` plus a Python-generated offline `guide.html`, bound to deck/rules/data versions.
- Cover the game plan, opening-hand priorities, card packages, play sequences and mistakes; separate exact local effect text from interpretation.
- Use information cards and diagrams; optional local images must degrade gracefully. No bundled official art, API requirement or image scraping.

Acceptance: unchanged inputs regenerate equivalent content, the page works offline with missing images, and guide generation leaves `riftatlas.txt` untouched.
