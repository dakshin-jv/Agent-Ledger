"""Postgres migration boundary for concurrent AgentLedger workflows."""

from __future__ import annotations

from pathlib import Path

from backend.src.config.database import database_url_from_environment


class PostgresMigrationError(RuntimeError):
    pass


def _migrations_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "migrations"


def all_migration_sql() -> list[tuple[str, str]]:
    """Return (filename, sql) pairs for every numbered migration, sorted."""
    migrations_dir = _migrations_dir()
    files = sorted(migrations_dir.glob("[0-9]*.sql"))
    return [(f.name, f.read_text(encoding="utf-8")) for f in files]


def foundation_migration_sql() -> str:
    """Return the original foundation SQL (kept for backward compat)."""
    return (_migrations_dir() / "001_foundation_postgres.sql").read_text(encoding="utf-8")


def apply_foundation_migration() -> None:
    """Apply all numbered, idempotent migrations in order."""
    try:
        import psycopg
    except ImportError as error:  # pragma: no cover - exercised only in deployment setup
        raise PostgresMigrationError("psycopg is unavailable; synchronize project dependencies first.") from error

    try:
        with psycopg.connect(database_url_from_environment()) as connection:
            with connection.cursor() as cursor:
                for _name, sql in all_migration_sql():
                    cursor.execute(sql)
    except Exception as error:
        raise PostgresMigrationError("Postgres foundation migration failed.") from error
