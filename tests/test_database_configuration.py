import os
import unittest
from unittest.mock import patch

from backend.src.config.database import DatabaseConfigurationError, database_url_from_environment
from backend.src.database.postgres import foundation_migration_sql


class DatabaseConfigurationTests(unittest.TestCase):
    def test_requires_postgres_url(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(DatabaseConfigurationError):
                database_url_from_environment()

    def test_accepts_postgres_url(self) -> None:
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@host/database"}, clear=True):
            self.assertEqual(database_url_from_environment(), "postgresql://user:pass@host/database")

    def test_migration_has_concurrency_and_outbox_controls(self) -> None:
        schema = foundation_migration_sql()
        self.assertIn("UNIQUE (requisition_id, reviewed_version, owner_id)", schema)
        self.assertIn("notification_outbox", schema)
        self.assertIn("correlation_key TEXT NOT NULL UNIQUE", schema)


if __name__ == "__main__":
    unittest.main()
