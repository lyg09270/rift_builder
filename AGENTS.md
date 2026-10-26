# Riftbound workspace instructions

These instructions apply throughout this workspace.

## Required routing

- Before Riftbound card, strategy, selection, legality or export work, read `.agents/skills/riftbound-deck-mvp/SKILL.md` completely and follow its workflow. Before its CLI calls, read `references/tool-usage.md` inside that skill. These files own the card-data, validation, export and handoff requirements.
- For guided construction, read `docs/deckbuilding-pipeline.md`; player decisions and module progress must be persisted before ending a session.
- For project operations, read `docs/deck-projects.md` and use `scripts/deck_projects.py`.
- For development planning, read `ROADMAP.md`. For module-methodology research, consult `docs/references/tcg-deckbuilding-principles.md`.

## Workspace boundaries

- Use local card data for card facts and legality. Browser/UI work requires an explicit user request or a data refresh directed by the skill.
- Never hand-edit managed manifests, validation reports, revision history or data snapshots.
- An unavailable data source or failed validation is a blocker to finalization; report it without inventing data or silently changing player-required cards.
- Distinguish planned behavior, implemented checks and observed results. Passing storage/export tests is not evidence of card-selection quality or competitive strength.

## Git operations

The user authorized one initial local commit only; do not push to GitHub. After that commit, do not run Git commands unless the user explicitly authorizes further Git work. Continue local development without automatic commits or pushes.
