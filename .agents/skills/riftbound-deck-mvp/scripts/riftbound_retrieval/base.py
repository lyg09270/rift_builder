"""The retrieval template owns normalization, deduplication and pagination."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .models import CardInfo, RetrievalQuery, RetrievalResult


QueryT = TypeVar("QueryT", bound=RetrievalQuery)


class BaseRetriever(ABC, Generic[QueryT]):
    @property
    @abstractmethod
    def query_type(self) -> type[QueryT]:
        """The request type this backend actually supports."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable backend identifier recorded in every result."""

    def retrieve(self, query: QueryT) -> RetrievalResult:
        if not isinstance(query, self.query_type):
            raise ValueError(f"{self.name} requires {self.query_type.__name__}")
        card_ids = list(self._retrieve(query))
        if any(not isinstance(card_id, str) or not card_id for card_id in card_ids):
            raise ValueError("A retriever must return nonempty card IDs, not card records")
        seen: set[str] = set()
        unique = []
        for card_id in card_ids:
            key = card_id.casefold()
            if key not in seen:
                unique.append(card_id)
                seen.add(key)
        return RetrievalResult(
            retriever=self.name,
            query=query,
            card_ids=tuple(unique[query.offset:query.offset + query.limit]),
            total=len(unique),
        )

    @abstractmethod
    def _retrieve(self, query: QueryT) -> Iterable[str]:
        """Return ordered, scoped base-card IDs, without paging or hydration.

        Scope handling is a backend obligation, not a post-top-k filter.
        A ranked/indexed backend can override retrieve for efficient counting and
        paging, but must preserve the public result contract and these invariants.
        """

    @abstractmethod
    def get_card(self, card_id: str) -> CardInfo:
        """Load one full card record on demand; do not infer missing effects."""
