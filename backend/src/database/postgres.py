"""Postgres migration boundary for concurrent AgentLedger workflows."""

from __future__ import annotations

from pathlib import Path

from backend.src.config.database import database_url_from_environment


class PostgresMigrationError(RuntimeError):
    pass


def foundation_migration_sql() -> str:
    return (
        Path(__file__).resolve().parents[2]
        / "migrations"
        / "001_foundation_postgres.sql"
    ).read_text(encoding="utf-8")


def apply_foundation_migration() -> None:
    """Apply the idempotent foundation schema to the configured Postgres database."""
    try:
        import psycopg
    except ImportError as error:  # pragma: no cover - exercised only in deployment setup
        raise PostgresMigrationError("psycopg is unavailable; synchronize project dependencies first.") from error

    try:
        with psycopg.connect(database_url_from_environment()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(foundation_migration_sql())
    except Exception as error:
        raise PostgresMigrationError("Postgres foundation migration failed.") from error
