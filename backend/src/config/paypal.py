"""Safe PayPal Sandbox configuration boundary.

Credentials are read only from the runtime environment. They are intentionally
not printed, persisted, or passed to model/agent code.
"""

from __future__ import annotations

from dataclasses import dataclass
import os


class PayPalConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class PayPalSandboxSettings:
    merchant_alias: str
    buyer_alias: str
    currency: str
    client_id: str
    client_secret: str
    environment: str = "sandbox"

    @classmethod
    def from_environment(cls) -> "PayPalSandboxSettings":
        values = {key: os.getenv(key, "").strip() for key in (
            "PAYPAL_ENVIRONMENT", "PAYPAL_SANDBOX_MERCHANT_ALIAS",
            "PAYPAL_SANDBOX_BUYER_ALIAS", "PAYPAL_SANDBOX_CURRENCY",
            "PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET",
        )}
        if values["PAYPAL_ENVIRONMENT"] != "sandbox":
            raise PayPalConfigurationError("Only PAYPAL_ENVIRONMENT=sandbox is permitted in this prototype.")
        required = [key for key, value in values.items() if not value]
        if required:
            raise PayPalConfigurationError(f"Missing PayPal Sandbox configuration: {', '.join(required)}")
        if len(values["PAYPAL_SANDBOX_CURRENCY"]) != 3 or not values["PAYPAL_SANDBOX_CURRENCY"].isalpha():
            raise PayPalConfigurationError("PAYPAL_SANDBOX_CURRENCY must be a three-letter currency code.")
        return cls(
            merchant_alias=values["PAYPAL_SANDBOX_MERCHANT_ALIAS"],
            buyer_alias=values["PAYPAL_SANDBOX_BUYER_ALIAS"],
            currency=values["PAYPAL_SANDBOX_CURRENCY"].upper(),
            client_id=values["PAYPAL_CLIENT_ID"],
            client_secret=values["PAYPAL_CLIENT_SECRET"],
        )

    @classmethod
    def merchant_from_environment(cls) -> "PayPalSandboxSettings":
        """Validate only what a merchant-side OAuth/readiness check requires.

        A buyer account and chosen transaction currency are intentionally not
        prerequisites for the primary merchant integration.
        """
        values = {key: os.getenv(key, "").strip() for key in (
            "PAYPAL_ENVIRONMENT", "PAYPAL_SANDBOX_MERCHANT_ALIAS",
            "PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET",
        )}
        if values["PAYPAL_ENVIRONMENT"] != "sandbox":
            raise PayPalConfigurationError("Only PAYPAL_ENVIRONMENT=sandbox is permitted in this prototype.")
        required = [key for key, value in values.items() if not value]
        if required:
            raise PayPalConfigurationError(f"Missing PayPal Sandbox configuration: {', '.join(required)}")
        return cls(
            merchant_alias=values["PAYPAL_SANDBOX_MERCHANT_ALIAS"],
            buyer_alias="", currency="", client_id=values["PAYPAL_CLIENT_ID"],
            client_secret=values["PAYPAL_CLIENT_SECRET"],
        )

    def safe_summary(self) -> dict[str, str]:
        """Metadata safe for a readiness report; it never exposes credentials."""
        return {
            "environment": self.environment,
            "merchant_alias": self.merchant_alias,
            "buyer_alias": self.buyer_alias,
            "currency": self.currency,
            "client_id_configured": "yes" if self.client_id else "no",
            "client_secret_configured": "yes" if self.client_secret else "no",
        }
