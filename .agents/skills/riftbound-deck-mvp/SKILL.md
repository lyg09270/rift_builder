---
name: riftbound-deck-mvp
description: Build, inspect, validate, and export Riftbound decks from a local full-text card database. Use for card selection, deck construction, legality checks, strategy summaries, or RiftAtlas-ready decklists; not for gameplay simulation or metagame/win-rate analysis.
---

# Riftbound Deck MVP

Use the local CLI as the source of truth for card text, card identity, counts, and legality. Do not rely on remembered card text.

## Tool contract

Resolve `scripts/riftbound.py` relative to this `SKILL.md`; it may be invoked from any working directory because its default database and rules paths are skill-relative. Use a Python 3 launcher (`python` or Windows `py -3`).

Before the first CLI call, read [references/tool-usage.md](references/tool-usage.md). `retrieve` returns card IDs under `card_ids`, not full records. Load selected candidates with `card CODE --json` only when their card information is needed. For the Python retrieval contract and backend extension, read [references/retrieval.md](references/retrieval.md).

Mandatory order:

1. Run `python <skill-dir>/scripts/riftbound.py doctor`. Continue only when it returns exit code 0 and `ready: true`.
2. Resolve the Legend and chosen Champion with `card CODE --json`.
3. Use `retrieve --legend CODE` for scoped discovery, adding literal keywords and color/other filters as needed. Load candidate IDs with `card CODE --json` and inspect `effect_effective` before selecting cards or reasoning about their effects. Page through results when `has_more` is true; an empty page is not proof that a functional effect does not exist.
4. Create the canonical deck JSON, then run `validate DECK.json`.
5. Run `export DECK.json` only when validation returns exit code 0 and `valid: true`.

Do not use `--allow-invalid` unless the user explicitly asks for an intentionally illegal or incomplete draft.

## Workflow

1. If `doctor` reports that `data/cards.sqlite` is absent or incomplete, run `sync`. If network access is unavailable, ask for a local `cards.json` snapshot and pass it with `--source`.
2. Capture a deck brief containing all four required fields: style, win condition, operating plan, and core cards.
3. Resolve the legend and chosen champion by exact card code. Use `card --json` and `retrieve` to inspect full effective rules text before choosing cards.
4. Build the canonical deck JSON described in [references/deck-schema.md](references/deck-schema.md). The canonical `main_deck` contains all 40 cards, including the chosen champion.
5. Run `validate`. Fix errors before presenting the deck. Report warnings instead of silently changing user-requested cards.
6. Run `export` to produce the RiftAtlas text. Explain the four-part strategy briefly alongside the export.

## Card selection

Read [references/card-selection.md](references/card-selection.md) when constructing or revising a deck. Retrieval discovers cards; it does not recommend a style, measure strength, or prove synergy. Compare the complete effect text, costs, stats, curve role, interaction timing, synergy requirements, and redundancy.

Never invent missing effects. If a card has no effective text in the local database, state that limitation and avoid using it as a synergy conclusion.

## Rules and data

`data/rules.json` is a dated rules profile, not timeless truth. Surface its `as_of` date in legality results. Read [references/data-sources.md](references/data-sources.md) only when refreshing, replacing, or distributing the database.

This skill supports deckbuilding and export only. Do not automate gameplay, retain win-rate data, or claim Riot endorsement.
