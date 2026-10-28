# Project scope

## Implemented

- Deck project management: create, revision history, copy, restore, archive, verification, and saved session progress. See [project operations](docs/deck-projects.md).
- Required internal card lookup, validation and RiftAtlas export in `scripts/deck_support.py`; bundled data retained in `data/`.
- Position-advantage observation: one 93-dimensional NumPy vector and a unified `StateEnum`, reviewed against the 2026-10-09 official rules; card identities and execution context remain outside it. See [model](docs/game-state.md).
- First card text-to-effect converter, isolated event projections and snapshot-bound affine matrices; 33 semantic/source examples and an audit of all 1,407 stored printings. Base Power requirements for all 1,143 ordinary playable records are sourced from RiftAtlas; most effect semantics remain unsupported. See [card transitions](docs/card-transitions.md).
- [Local research papers](docs/references/tcg-card-evaluation/README.md).

## Awaiting design and explicit implementation requests

- Additional state axes and information required by card effects.
- Broader card semantics, complete card/payment data, effect interactions, probabilistic transitions and opponent models.
- Scoring criteria and validation against independent evidence.

The earlier scoring, simulation, retrieval and recommendation implementations have been removed. No calibrated card strength or win-rate model is currently implemented.
