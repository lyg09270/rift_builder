# Agent tool usage

Use this reference before calling `scripts/riftbound.py`. Commands below assume `CLI` means the absolute path to that script. The script resolves its default database and rules files relative to the skill directory, so the caller's working directory does not matter.

On Windows, invoke with `py -3 CLI ...`; elsewhere use `python3 CLI ...` or another available Python 3 launcher.

## Exit codes

- `0`: command succeeded, including empty retrieval pages; for `doctor` and `validate`, the reported state is ready/valid.
- `2`: invalid arguments, missing data, unresolved or ambiguous card, invalid deck, or refused export.

Always inspect both the exit code and the JSON fields. Do not treat textual output alone as proof of legality.

## 1. Check local data

```text
python CLI doctor
```

Expected JSON includes `ready`, `printings`, `records_with_effect_text`, `manifest_complete`, `rules_profile`, and `rules_as_of`. Continue only when `ready` is `true`.

If it is not ready:

```text
python CLI sync
python CLI doctor
```

When network access is unavailable, import a supplied snapshot:

```text
python CLI sync --source /absolute/path/cards.json
```

Do not edit `cards.sqlite` manually.

## 2. Resolve known cards

```text
python CLI card UNL-183 --json
python CLI card SFD-025 --json
```

Use exact card codes whenever available. Important response fields are:

- `display_code` and `display_name`: stable deck/export identity;
- `card_type`, `labels`, `domains`, and `tags`: legality and identity;
- `energy`, `power`, and `might`: curve and efficiency;
- `effect_effective`: current effect after errata;
- `effect_original` and `effect_corrected`: audit trail;
- `has_errata`: whether corrected text applies.

Use `effect_effective`, not `effect_original`, for card-selection reasoning.

## 3. Retrieve candidates (unified JSON)

```text
python CLI retrieve draw --legend UNL-183 --type Spell --max-energy 4 --limit 20
python CLI retrieve "play me" --set RAD --tag Rengar
python CLI retrieve draw recycle --match any --legend UNL-183 --limit 20
python CLI retrieve --legend UNL-183 --type Unit --limit 20 --offset 20
```

`retrieve` always prints one `RetrievalResult` JSON object. No `--json` switch is needed. `card_ids` is an array of official set/collector codes, with one representative per named card; the result contains no card effects or descriptions. Load needed IDs with `card CODE --json` before secondary effect-based judgment. `total` counts all matching cards after scope filtering and deduplication, before pagination. Continue with the next offset while `has_more` is true. No-match results have `card_ids: []`, `total: 0`, and exit `0`; a page beyond the end also has no IDs, but preserves the nonzero total.

Keywords are separate positional arguments. Each argument is a literal substring; quote a phrase to keep it together. `--match all` (default) requires every keyword, possibly in different fields; `--match any` accepts at least one. No keywords means browse by filters. `%`, `_`, quotes and backslashes are literal characters, not SQL operators.

Filters and scope:

- `--colors COLOR ...` uses official domain names: Fury, Calm, Mind, Body, Chaos, Order, Colorless.
- `--color-mode any|all|within|exact`: any named color; all named colors; no colors outside the set (including domainless cards); or exactly the named color set. Default: `any`. Omit `--colors` for unrestricted colors.
- `--type Legend|Unit|Gear|Spell|Battlefield|Rune`
- `--set SETCODE`
- `--tag TAG`
- `--max-energy NUMBER`
- `--min-might NUMBER`
- `--legend CODE` resolves a Legend, restricts all card domains to its identity (domainless cards are allowed), and applies the local rules profile. Battlefield domains are exempt, matching the validator.
- `--legal` applies legal sets and ban lists without restricting Legend identity.
- `--limit NUMBER`
- `--offset NUMBER`

Retrieval covers `full_name`, `display_code`, tags and complete `effect_effective` inside SQLite, but does not transfer that text to the caller until `card` is used. It does not translate Chinese, expand synonyms, understand negation, or infer roles. Use English effect wording, try alternatives, and inspect full effects. Results are ordered deterministically by name/code, not strength or relevance; no strength/relevance scores are returned.

Without `--legend` or `--legal`, the scope includes the whole local database, including non-legal printings and banned cards. Scoped retrieval is still not whole-deck validation. See [retrieval.md](retrieval.md) for the schema and Python interface.

The previous `search` and `candidates` commands and style/core heuristic scores have been removed; do not invoke them.

## 4. Validate the canonical deck

Construct the JSON defined in [deck-schema.md](deck-schema.md), then run:

```text
python CLI validate /absolute/path/deck.json
```

The command always prints a JSON report. Accept the deck only when all of these are true:

- process exit code is `0`;
- `valid` is `true`;
- `errors` is empty;
- totals match the requested profile.

Explain warnings to the user. Fix errors in the canonical JSON and rerun validation; never silently discard a user-required core card.

## 5. Export for RiftAtlas

```text
python CLI export /absolute/path/deck.json --output /absolute/path/deck.riftatlas.txt
```

Omit `--output` to receive text on stdout. Use `--no-codes` only when the target importer rejects `[SET-NNN]` suffixes. Export validates again and refuses invalid decks by default.

## Required agent response

When handing off a deck, include:

1. style;
2. win condition;
3. operating plan;
4. core cards and why they are core;
5. validation profile and `rules_as_of` date;
6. RiftAtlas text or a link to the exported file.
