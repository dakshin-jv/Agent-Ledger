"""Authoritative Postgres runtime configuration."""

from __future__ import annotations

import os


class DatabaseConfigurationError(ValueError):
    pass


def database_url_from_environment() -> str:
    """Return the Postgres connection URL without logging or transforming it."""
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise DatabaseConfigurationError("DATABASE_URL is required for the Postgres runtime.")
    if not url.startswith(("postgres://", "postgresql://")):
        raise DatabaseConfigurationError("DATABASE_URL must be a PostgreSQL connection URL.")
    return url
