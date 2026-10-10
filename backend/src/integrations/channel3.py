"""Read-only Channel3 external-catalog discovery adapter.

Channel3 supplies externally observed product offers. It cannot create an
approved supplier, inventory record, contract, or payment recipient.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Protocol, Sequence

from backend.src.config.channel3 import Channel3Settings


class Channel3DiscoveryError(RuntimeError):
    """A safe, non-authoritative discovery failure for procurement workflows."""


class ProductSearchClient(Protocol):
    def search(self, **kwargs: Any) -> Any: ...


@dataclass(frozen=True)
class ExternalOffer:
    retailer: str | None
    url: str | None
    amount: str | None
    currency: str | None
    availability: str | None


@dataclass(frozen=True)
class ExternalCandidate:
    product_id: str
    title: str
    category: str | None
    offers: tuple[ExternalOffer, ...]
    data_origin: str
    retrieved_at: str


class Channel3Discovery:
    """Search product discovery data with explicit provenance and no authority."""

    def __init__(self, settings: Channel3Settings, products: ProductSearchClient | None = None) -> None:
        self._settings = settings
        if products is None:
            try:
                from channel3_sdk import Channel3
            except ImportError as error:  # pragma: no cover - runtime setup path
                raise Channel3DiscoveryError(
                    "Channel3 SDK is unavailable. Run `uv sync` after updating dependencies."
                ) from error
            products = Channel3(
                api_key=settings.api_key,
                language=settings.language or "en",
                country=settings.country or "US",
                currency=settings.currency or "USD",
            ).products
        self._products = products

    def search_goods(self, *, query: str, limit: int = 10, user_id: str | None = None) -> tuple[ExternalCandidate, ...]:
        """Discover candidates; callers persist any result only as an external snapshot."""
        if not query.strip():
            raise ValueError("Channel3 discovery needs a non-empty goods query.")
        if not 1 <= limit <= 30:
            raise ValueError("Channel3 search limit must be between 1 and 30.")
        request: dict[str, Any] = {"query": query.strip(), "limit": limit}
        config = self._settings.search_config()
        if config:
            request["config"] = config
        if user_id is not None:
            request["user_id"] = user_id
        try:
            page = self._products.search(**request)
        except Exception as error:
            raise Channel3DiscoveryError("External product discovery is unavailable; manual intake can continue.") from error
        products: Sequence[Any] = getattr(page, "items", page.get("products", ()) if isinstance(page, dict) else ())
        retrieved_at = datetime.now(UTC).isoformat()
        return tuple(self._candidate(product, retrieved_at) for product in products)

    @classmethod
    def _candidate(cls, product: Any, retrieved_at: str) -> ExternalCandidate:
        product_id = cls._string(cls._field(product, "id"))
        title = cls._string(cls._field(product, "title"))
        if not product_id or not title:
            raise Channel3DiscoveryError("Channel3 returned a product without an ID or title.")
        category = cls._field(product, "category")
        offers = tuple(cls._offer(offer) for offer in (cls._field(product, "offers") or ()))
        return ExternalCandidate(
            product_id=product_id,
            title=title,
            category=cls._string(cls._field(category, "slug") or cls._field(category, "title")),
            offers=offers,
            data_origin="external_channel3",
            retrieved_at=retrieved_at,
        )

    @classmethod
    def _offer(cls, offer: Any) -> ExternalOffer:
        price = cls._field(offer, "price")
        return ExternalOffer(
            retailer=cls._string(cls._field(offer, "domain")),
            url=cls._string(cls._field(offer, "url")),
            amount=cls._decimal_string(cls._field(price, "price") or cls._field(price, "amount")),
            currency=cls._string(cls._field(price, "currency")),
            availability=cls._string(cls._field(offer, "availability")),
        )

    @staticmethod
    def _field(value: Any, name: str) -> Any:
        return value.get(name) if isinstance(value, dict) else getattr(value, name, None)

    @staticmethod
    def _string(value: Any) -> str | None:
        return str(value) if value is not None and str(value) else None

    @staticmethod
    def _decimal_string(value: Any) -> str | None:
        if value is None:
            return None
        try:
            return format(Decimal(str(value)), "f")
        except (InvalidOperation, ValueError):
            return None
