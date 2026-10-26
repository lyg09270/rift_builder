# Card selection guide

Use full effective card text from the local database. Build a shortlist before committing quantities.

## Required deck brief

- **Style:** aggro, tempo, midrange, control, combo, or a clear hybrid.
- **Win condition:** the repeatable path that earns the final points, not merely “play strong cards.”
- **Operating plan:** early, middle, and late-game resource and board plan.
- **Core cards:** cards the deck is built to enable or protect.

## Evaluation dimensions

For every candidate, assess:

- legal domains, card type, energy and power costs;
- immediate board impact versus delayed value;
- contribution to the stated win condition;
- synergy with core-card effects and tags;
- whether setup requirements are realistic;
- role overlap and redundancy;
- curve pressure, interaction timing, and card advantage;
- failure mode when drawn without its synergy pieces.

Use `retrieve --legend CODE` for scoped discovery, with keywords and color/other filters for the current module. Results contain IDs only; load needed candidates with `card CODE --json`, inspect complete `effect_effective`, and follow pagination. Keyword matches do not establish a function, synergy or strength; the agent must make the qualitative comparison. The keyword backend has no relevance score or style heuristic.

## Quantity heuristics

- Three copies: core engine, best early play, or card wanted in most opening hands.
- Two copies: strong but situational, expensive, or redundant with similar effects.
- One copy: searchable target, narrow answer, high-cost finisher, or sideboard bullet.

These are defaults, not rules. Explain exceptions through the deck brief.
