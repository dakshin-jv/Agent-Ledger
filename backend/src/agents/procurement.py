"""Procurement-facing, read-only external goods discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from backend.src.config.channel3 import Channel3Settings
from backend.src.integrations.channel3 import Channel3Discovery, ExternalCandidate


class GoodsDiscovery(Protocol):
    def search_goods(self, *, query: str, limit: int = 10, user_id: str | None = None) -> tuple[ExternalCandidate, ...]: ...


@dataclass(frozen=True)
class ProcurementDiscoveryAgent:
    """Find external candidates without granting supplier or payment authority."""

    discovery: GoodsDiscovery

    @classmethod
    def from_environment(cls) -> "ProcurementDiscoveryAgent":
        return cls(Channel3Discovery(Channel3Settings.from_environment()))

    def discover_external_options(
        self, *, goods_description: str, user_id: str, limit: int = 10
    ) -> tuple[ExternalCandidate, ...]:
        return self.discovery.search_goods(
            query=goods_description,
            limit=limit,
            user_id=user_id,
        )
