import os
import unittest
from unittest.mock import patch

from backend.src.config.channel3 import Channel3ConfigurationError, Channel3Settings
from backend.src.agents.procurement import ProcurementDiscoveryAgent
from backend.src.integrations.channel3 import Channel3Discovery


class _Page:
    items = [{
        "id": "c3-product-1",
        "title": "Demo procurement monitor",
        "category": {"slug": "monitors"},
        "offers": [{
            "domain": "example-retailer.test",
            "url": "https://example-retailer.test/product/1",
            "price": {"price": "1250.00", "currency": "USD"},
            "availability": "InStock",
        }],
    }]


class _Products:
    def __init__(self) -> None:
        self.request = None

    def search(self, **kwargs):
        self.request = kwargs
        return _Page()


class Channel3Tests(unittest.TestCase):
    def test_requires_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(Channel3ConfigurationError):
                Channel3Settings.from_environment()

    def test_search_preserves_external_provenance_and_uses_locale_only_when_configured(self) -> None:
        products = _Products()
        discovery = Channel3Discovery(Channel3Settings(api_key="test-key"), products)

        candidates = discovery.search_goods(query="procurement monitor", limit=1, user_id="user-1")

        self.assertEqual(products.request, {"query": "procurement monitor", "limit": 1, "user_id": "user-1"})
        self.assertEqual(candidates[0].data_origin, "external_channel3")
        self.assertEqual(candidates[0].offers[0].amount, "1250.00")
        self.assertEqual(candidates[0].offers[0].retailer, "example-retailer.test")

    def test_configured_locale_is_passed_to_search(self) -> None:
        products = _Products()
        settings = Channel3Settings(api_key="test-key", country="GB", currency="GBP")
        Channel3Discovery(settings, products).search_goods(query="office chair")

        self.assertEqual(products.request["config"], {"country": "GB", "currency": "GBP"})

    def test_sdk_receives_valid_defaults_when_empty_environment_locale_is_present(self) -> None:
        with patch("channel3_sdk.Channel3") as client:
            Channel3Discovery(Channel3Settings(api_key="test-key"))

        client.assert_called_once_with(
            api_key="test-key", language="en", country="US", currency="USD"
        )

    def test_procurement_agent_keeps_discovery_read_only_and_user_attributed(self) -> None:
        products = _Products()
        agent = ProcurementDiscoveryAgent(Channel3Discovery(Channel3Settings(api_key="test-key"), products))

        candidates = agent.discover_external_options(
            goods_description="ergonomic keyboard", user_id="usr-requester", limit=1
        )

        self.assertEqual(products.request["user_id"], "usr-requester")
        self.assertEqual(candidates[0].data_origin, "external_channel3")


if __name__ == "__main__":
    unittest.main()
