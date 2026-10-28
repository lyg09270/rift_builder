# Workspace instructions

## Current scope

- Keep the deck project manager, its required local data/validation/export dependencies, research papers, and the basic game state model.
- The numeric model is `scripts/game_state.py`: class `game_state` stores only one NumPy position-advantage observation vector; `StateEnum` contains only explicitly numbered dimension indices, with `STATE_SIZE` stating the dimension count. Do not mix field values into this enum. Use `docs/game-state.md` for feature definitions and the official rules basis. Card details, event history and execution context belong outside it. It does not execute effects, simulate games or score cards.
- The user requested card-to-transition implementation: `scripts/card.py`, `scripts/card_converter.py`, and `scripts/state_transition.py`. Follow `docs/card-transitions.md`; unmapped text must fail explicitly, missing cost data must not be invented, and matrices are bound to a snapshot/context. Full-library audit and semantic tests were explicitly requested for this implementation; their current reports must not be described as full rules certification.
- During design discussions, do not modify code or files unless the user explicitly requests implementation or recording.
- Do not recreate the removed retrieval, recommendation, simulation or scoring interfaces without a new request.

## Tests

- Do not write, add or restore tests, test fixtures, test frameworks or test automation unless the user explicitly requests them.
- Do not run test suites automatically. The current test files were removed at the user's request.
- Required runtime deck validation before saving/exporting remains part of project operations; it is not a test suite.

## Project operations and data

- Read `docs/deck-projects.md` and use `scripts/deck_projects.py` for project operations.
- `scripts/deck_support.py` is an internal lookup/validation/export module. Default data files are in `data/`.
- Preserve existing deck projects, build sessions and immutable revisions.
- Never hand-edit managed manifests, validation reports, revision history or data snapshots.
- Use the local database for card facts; do not invent missing text or treat unknown values as zero.
- Validation uses a dated rules profile and is required before saving a complete deck/export.
- Distinguish implemented behavior, observed results and strategic claims.

## Git

Do not run Git commands, commit or push unless the user explicitly authorizes further Git work.
