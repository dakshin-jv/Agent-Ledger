"""Server-side configuration for Channel3 product discovery."""

from __future__ import annotations

from dataclasses import dataclass
import os


class Channel3ConfigurationError(ValueError):
    """Raised when required Channel3 discovery configuration is absent or invalid."""


@dataclass(frozen=True)
class Channel3Settings:
    api_key: str
    language: str | None = None
    country: str | None = None
    currency: str | None = None

    @classmethod
    def from_environment(cls) -> "Channel3Settings":
        api_key = os.getenv("CHANNEL3_API_KEY", "").strip()
        if not api_key:
            raise Channel3ConfigurationError("CHANNEL3_API_KEY is required for product discovery.")
        language = cls._optional("CHANNEL3_LANGUAGE")
        country = cls._optional("CHANNEL3_COUNTRY")
        currency = cls._optional("CHANNEL3_CURRENCY")
        if language is not None and len(language) != 2:
            raise Channel3ConfigurationError("CHANNEL3_LANGUAGE must be an ISO 639-1 code.")
        if country is not None and (len(country) != 2 or not country.isalpha()):
            raise Channel3ConfigurationError("CHANNEL3_COUNTRY must be a two-letter country code.")
        if currency is not None and (len(currency) != 3 or not currency.isalpha()):
            raise Channel3ConfigurationError("CHANNEL3_CURRENCY must be a three-letter currency code.")
        return cls(
            api_key=api_key,
            language=language.lower() if language else None,
            country=country.upper() if country else None,
            currency=currency.upper() if currency else None,
        )

    @staticmethod
    def _optional(name: str) -> str | None:
        value = os.getenv(name, "").strip()
        return value or None

    def search_config(self) -> dict[str, str]:
        """Send only locale fields that have been explicitly verified/configured."""
        return {
            key: value
            for key, value in {
                "language": self.language,
                "country": self.country,
                "currency": self.currency,
            }.items()
            if value is not None
        }

    def safe_summary(self) -> dict[str, str]:
        return {
            "api_key_configured": "yes" if self.api_key else "no",
            "language": self.language or "default",
            "country": self.country or "default",
            "currency": self.currency or "default",
        }
