"""Backend-independent requests and results for card retrieval."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Literal, TypedDict


CARD_TYPES = ("Legend", "Unit", "Gear", "Spell", "Battlefield", "Rune")
COLORS = ("Fury", "Calm", "Mind", "Body", "Chaos", "Order", "Colorless")


class CardInfo(TypedDict):
    source_code: str
    display_code: str
    name: str
    subtitle: str
    full_name: str
    display_name: str
    set_code: str
    set_name: str
    collector_number: str
    rarity: str
    domain: str
    domains: list[str]
    card_type: str
    labels: list[str]
    tags: list[str]
    energy: float | None
    power: float | None
    might: float | None
    effect_original: str
    effect_corrected: str
    effect_effective: str
    has_errata: bool
    source_url: str
    scraped_at: str


@dataclass(frozen=True)
class CardFilters:
    colors: tuple[str, ...] | None = None
    color_mode: Literal["any", "all", "within", "exact"] = "any"
    card_type: str | None = None
    set_code: str | None = None
    tag: str | None = None
    max_energy: float | None = None
    min_might: float | None = None
    # None means unrestricted; () permits only domainless cards.
    allowed_domains: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        for name in ("card_type", "set_code", "tag"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be a nonempty string")
        if self.card_type is not None and self.card_type.casefold() not in {t.casefold() for t in CARD_TYPES}:
            raise ValueError(f"Unknown card type: {self.card_type}")
        for name in ("max_energy", "min_might"):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0
            ):
                raise ValueError(f"{name} must be a finite nonnegative number")
        if self.allowed_domains is not None:
            _check_strings(self.allowed_domains, "allowed_domains")
        if self.colors is not None:
            _check_strings(self.colors, "colors")
        if self.color_mode not in ("any", "all", "within", "exact"):
            raise ValueError("color_mode must be any, all, within or exact")
        for values in (self.colors, self.allowed_domains):
            if values is not None and any(v.casefold() not in {c.casefold() for c in COLORS} for v in values):
                raise ValueError("Unknown color/domain")


def _check_strings(values: tuple[str, ...], name: str) -> None:
    if not isinstance(values, tuple) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValueError(f"{name} must be a tuple of nonempty strings")


@dataclass(frozen=True)
class RetrievalRules:
    profile: str
    as_of: str
    legal_sets: tuple[str, ...]
    banned_cards: tuple[str, ...] = ()
    banned_battlefields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.profile or not self.as_of:
            raise ValueError("Rules need a profile and as_of date")
        for name in ("legal_sets", "banned_cards", "banned_battlefields"):
            _check_strings(getattr(self, name), name)


@dataclass(frozen=True)
class RetrievalQuery:
    """Shared constraints only; backend-specific query content lives in subclasses."""

    filters: CardFilters = field(default_factory=CardFilters)
    rules: RetrievalRules | None = None
    limit: int = 20
    offset: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.filters, CardFilters):
            raise ValueError("filters must be CardFilters")
        if self.rules is not None and not isinstance(self.rules, RetrievalRules):
            raise ValueError("rules must be RetrievalRules or None")
        for name, minimum in (("limit", 1), ("offset", 0)):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
                raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class KeywordQuery(RetrievalQuery):
    # Each entry is a literal keyword/phrase, not a SQL, regex or FTS expression.
    keywords: tuple[str, ...] = ()
    match: Literal["all", "any"] = "all"

    def __post_init__(self) -> None:
        super().__post_init__()
        _check_strings(self.keywords, "keywords")
        if self.match not in ("all", "any"):
            raise ValueError("match must be all or any")


@dataclass(frozen=True)
class RetrievalResult:
    retriever: str
    query: RetrievalQuery
    card_ids: tuple[str, ...]
    total: int
    schema_version: int = field(default=1, init=False)

    @property
    def has_more(self) -> bool:
        return self.query.offset + len(self.card_ids) < self.total

    def to_dict(self) -> dict:
        def json_value(value):
            if isinstance(value, dict):
                return {key: json_value(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [json_value(item) for item in value]
            return value

        data = json_value(asdict(self))
        data["has_more"] = self.has_more
        return data
