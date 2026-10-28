# Canonical deck schema

The canonical JSON is the editable source of truth. Card references should use stable display codes such as `UNL-183` or `SFD-025`.

```json
{
  "schema_version": 1,
  "name": "Rengar tempo",
  "rules_profile": "standard-constructed",
  "strategy": {
    "style": "快攻/节奏",
    "win_condition": "用低费单位抢占战场，通过移动和战斗增益连续得分。",
    "operating_plan": "前期铺场，中期利用反应牌保护进攻并维持手牌。",
    "core_cards": ["UNL-183", "SFD-025", "UNL-184"]
  },
  "legend": "UNL-183",
  "chosen_champion": "SFD-025",
  "main_deck": [
    {"code": "SFD-025", "quantity": 2}
  ],
  "battlefields": [],
  "runes": [],
  "sideboard": []
}
```

## Invariants

- `main_deck` contains the complete tournament Main Deck, including the chosen champion.
- `chosen_champion` points to one copy already counted in `main_deck`.
- RiftAtlas export places that copy in `Champion:` and subtracts it from the `MainDeck:` section.
- Quantities are positive integers.
- Preserve list order because export order is user-facing.
- Strategy requires non-empty `style`, `win_condition`, `operating_plan`, and `core_cards`.

The validator applies counts, type checks, domain identity, champion identity, copy limits, signature-card limits, legal sets, and the dated ban list from `data/rules.json`.
