# Card retrieval contract

The package is scripts/riftbound_retrieval/. The CLI uses the same API; there is no parallel implementation or compatibility layer. Only the keyword backend is implemented. Retrieval is separate from card hydration, relevance judgment and recommendations.

## Python API

Put this skill's scripts/ directory on the Python import path:

~~~python
from riftbound_retrieval import CardFilters, KeywordQuery, KeywordRetriever

retriever = KeywordRetriever("/absolute/path/to/cards.sqlite")
result = retriever.retrieve(KeywordQuery(
    keywords=("draw", "recycle"),
    match="any",
    filters=CardFilters(
        colors=("Body", "Fury"),
        color_mode="within",
        card_type="Spell",
        max_energy=4,
    ),
    limit=20,
    offset=0,
))

# Filtering transfers IDs, not full card records.
for card_id in result.card_ids:
    print(card_id)

# Only hydrate candidates whose effects you need to judge.
card = retriever.get_card(result.card_ids[0]) if result.card_ids else None
if card:
    print(card["energy"], card["power"], card["might"])
    print(card["domains"], card["effect_effective"])

payload = result.to_dict()
~~~

RetrievalQuery holds shared constraints and pagination. KeywordQuery adds literal keywords and ALL/ANY matching. A semantic backend can define its own query text/options without inheriting keyword assumptions.

The library does not guess database paths, Legend identity or rules. Supply CardFilters.allowed_domains for Legend identity and a dated RetrievalRules(profile, as_of, legal_sets, banned_cards, banned_battlefields) through the query's rules field. The CLI resolves these from its local data for --legend; --legal applies rules without identity.

## Result format

models.py is the authoritative type definition. All backends return RetrievalResult; to_dict() produces JSON-compatible values:

~~~text
schema_version: 1
retriever: backend name
query: actual request, including scope and pagination
card_ids: ["OGN-005", ...]
total: matching named cards, before pagination
has_more: whether another page remains
~~~

There are no effects, descriptions or synthetic strength scores in retrieval results. An empty result is successful and has an empty ID list. An out-of-range page preserves the full nonzero total.

Keyword retrieval reads text inside SQLite to match keywords, but only ID columns leave the database query. It does not call get_card. Each keyword argument is a literal substring/phrase; it does not support SQL, regex, synonym expansion, translation or effect reasoning. Results use stable name/code ordering, not relevance/strength ordering. The exact count is a count of literal matches, not all cards capable of fulfilling a player's intent.

## Card IDs and on-demand card information

Use a normalized official set/collector code: for example OGN-005, not ORG-005. [Riot's preview guide](https://playriftbound.com/en-us/news/announcements/what-to-expect-during-preview-season/) identifies Origins as OGN and explains alternate-art letter suffixes and overnumbered printings. The local source retains the full collector number and gallery URL for provenance.

Do not assume every code is exactly three digits: Rune, Token and Special codes can have R/T/SP prefixes. public_card_id removes the trailing set-size component but preserves those prefixes and collector suffixes. Never create a non-variant identity merely by deleting a letter or truncating digits.

For each named card, scope filters are applied first and an eligible representative is selected; keyword matching then uses that representative's full effective text, not an alternate's possibly abbreviated wording. No art/printing selector is exposed. The returned ID is an actual local card code, not an invented hash or card name. A reprint in another set has another printed code; filtering by set/rules can therefore select a different representative. This does not assert that Riot publishes one universal functional-card ID across all reprints.

get_card(card_id) is exact-ID lookup and returns the same full CardInfo shape as card CODE --json:

- Identity/name: display_code (the public ID), display_name, full_name, name, subtitle.
- Costs/stats: energy, power, might; missing values stay null, not zero.
- Colors/type: domains, domain, card_type, labels, tags.
- Full effects: effect_effective, effect_original, effect_corrected, has_errata.
- Provenance/printing: source_code, source_url, scraped_at, set_code, set_name, collector_number, rarity.

Effects are never truncated, summarized or invented. Inspect effect_effective before choosing cards or reasoning about their conditions. Unknown/ambiguous IDs fail explicitly instead of guessing by name.

## Color filters

Use official domain names Fury, Calm, Mind, Body, Chaos and Order. Colorless and an empty domain array both represent domainless cards for filtering.

| Mode | Example: Body/Fury requested |
| --- | --- |
| any | At least one of Body/Fury; a Body/Mind card also passes. |
| all | Must contain both Body and Fury; additional colors are allowed. |
| within | Every color must be Body/Fury; domainless cards also pass. |
| exact | Exactly Body/Fury, neither a subset nor a superset. |

Omit colors for unrestricted colors. colors=("Colorless",), color_mode="exact" selects domainless cards. Explicit color filters and Legend identity are intersected. Legend identity is a within filter and exempts Battlefields, matching the local validator; an explicit color filter still applies to Battlefields.

Domain/tag comparisons are case-insensitive and exact. Numeric bounds exclude missing stats. Legal-set and ban-list filters are optional, dated and applied before representative selection. They do not replace complete deck validation.

## Adding another backend

Implement BaseRetriever[YourQuery] with name, query_type, _retrieve(query) yielding ordered IDs, and get_card(card_id) for on-demand card information. The base class rejects unsupported query types and assembles deduplicated, counted, paginated ID results.

Backends must apply every requested filter/rule before paging and must not silently ignore unsupported constraints. Resolve art variants and printing scope before returning IDs. Keep model-based second-stage judgment outside this class; it can load the returned IDs when required.

The current keyword backend uses parameterized SQLite substring queries and short-lived read-only connections. It changes neither the source database nor managed data snapshots. It has no BM25/vector index and makes no claim of indexed large-corpus performance. The base materializes IDs for exact counting/paging, not full descriptions; a future indexed backend can implement efficient paging behind the same result contract.
