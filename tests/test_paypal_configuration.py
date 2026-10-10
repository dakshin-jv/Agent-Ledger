import os
import unittest
from unittest.mock import patch

from backend.src.config.paypal import PayPalConfigurationError, PayPalSandboxSettings


class PayPalSandboxSettingsTests(unittest.TestCase):
    def test_rejects_any_non_sandbox_environment(self) -> None:
        with patch.dict(os.environ, {"PAYPAL_ENVIRONMENT": "live"}, clear=True):
            with self.assertRaisesRegex(PayPalConfigurationError, "sandbox"):
                PayPalSandboxSettings.from_environment()

    def test_safe_summary_does_not_include_credential_values(self) -> None:
        environment = {
            "PAYPAL_ENVIRONMENT": "sandbox", "PAYPAL_SANDBOX_MERCHANT_ALIAS": "fictional-merchant",
            "PAYPAL_SANDBOX_BUYER_ALIAS": "fictional-buyer", "PAYPAL_SANDBOX_CURRENCY": "USD",
            "PAYPAL_CLIENT_ID": "client-secret-looking-id", "PAYPAL_CLIENT_SECRET": "actual-secret",
        }
        with patch.dict(os.environ, environment, clear=True):
            summary = PayPalSandboxSettings.from_environment().safe_summary()
        self.assertEqual(summary["environment"], "sandbox")
        self.assertNotIn("actual-secret", str(summary))
        self.assertNotIn("client-secret-looking-id", str(summary))

    def test_merchant_readiness_does_not_require_buyer_or_currency(self) -> None:
        environment = {
            "PAYPAL_ENVIRONMENT": "sandbox", "PAYPAL_SANDBOX_MERCHANT_ALIAS": "fictional-merchant",
            "PAYPAL_CLIENT_ID": "client-id", "PAYPAL_CLIENT_SECRET": "client-secret",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = PayPalSandboxSettings.merchant_from_environment()
        self.assertEqual(settings.merchant_alias, "fictional-merchant")
        self.assertEqual(settings.buyer_alias, "")


if __name__ == "__main__":
    unittest.main()
