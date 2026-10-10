"""Guarded domain writes for AgentLedger.

This module contains no provider credentials. It is the write boundary for
tenancy, approvals, audit, recovery, and notification outbox records.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any, Iterator
from uuid import uuid4

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from backend.src.config.database import database_url_from_environment
from backend.src.database.postgres import apply_foundation_migration


class DomainError(ValueError):
    """Raised when a requested state transition is not permitted."""


def utc_now() -> datetime:
    return datetime.now(UTC)


class FoundationStore:
    """PostgreSQL persistence and guarded domain transitions."""

    def __init__(self) -> None:
        self.database_url = database_url_from_environment()

    @contextmanager
    def _connection(self) -> Iterator[Connection]:
        connection = psycopg.connect(self.database_url, row_factory=dict_row)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        apply_foundation_migration()

    def _audit(
        self, connection: Connection, *, tenant_id: str, actor_id: str | None,
        action: str, target_type: str, target_id: str, correlation_key: str,
        before: dict[str, Any] | None = None, after: dict[str, Any] | None = None,
    ) -> str:
        event_id = str(uuid4())
        connection.execute(
            """
            INSERT INTO audit_events (
                id, tenant_id, actor_id, action, target_type, target_id,
                before_json, after_json, correlation_key, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                event_id, tenant_id, actor_id, action, target_type, target_id,
                Jsonb(before) if before else None,
                Jsonb(after) if after else None,
                correlation_key, utc_now(),
            ),
        )
        return event_id

    def seed_demo(self) -> None:
        """Create explicitly labelled, fictional identities; safe to call repeatedly."""
        self.initialize()
        now = utc_now()
        people = [
            ("usr-requester", "demo-tenant", "Avery Requester", "requester"),
            ("usr-owner", "demo-tenant", "Blair Business Owner", "business_owner"),
            ("usr-funding", "demo-tenant", "Casey Funding Owner", "funding_owner"),
            ("usr-admin", "demo-tenant", "Devon Administrator", "administrator"),
        ]
        with self._connection() as connection:
            for user_id, tenant_id, name, role in people:
                connection.execute(
                    """
                    INSERT INTO users (id, tenant_id, display_name, active, data_origin, created_at)
                    VALUES (%s, %s, %s, TRUE, 'demo_fixture', %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (user_id, tenant_id, name, now),
                )
                connection.execute(
                    """
                    INSERT INTO role_assignments (user_id, tenant_id, role)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, tenant_id, role) DO NOTHING
                    """,
                    (user_id, tenant_id, role),
                )

    def create_requisition(
        self, *, tenant_id: str, requester_id: str, business_owner_id: str,
        purpose: str, correlation_key: str,
    ) -> str:
        if not purpose.strip():
            raise DomainError("A requisition needs a requester-confirmed purpose.")
        requisition_id, now = str(uuid4()), utc_now()
        with self._connection() as connection:
            self._assert_active_user(connection, tenant_id, requester_id)
            self._assert_active_user(connection, tenant_id, business_owner_id)
            connection.execute(
                """
                INSERT INTO requisitions (
                    id, tenant_id, business_owner_id, requester_id, purpose,
                    status, version, data_origin, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, 'draft', 1, 'user_input', %s, %s)
                """,
                (requisition_id, tenant_id, business_owner_id, requester_id, purpose, now, now),
            )
            self._audit(
                connection, tenant_id=tenant_id, actor_id=requester_id,
                action="requisition.created", target_type="requisition", target_id=requisition_id,
                correlation_key=correlation_key, after={"status": "draft", "version": 1},
            )
        return requisition_id

    def submit_for_owner_review(self, *, requisition_id: str, actor_id: str, correlation_key: str) -> str:
        """Freeze the current version and route an approval to the assigned owner."""
        with self._connection() as connection:
            req = self._requisition(connection, requisition_id)
            if req["status"] in {"withdrawn", "approved"}:
                raise DomainError(f"Cannot submit a {req['status']} requisition.")
            self._assert_active_user(connection, req["tenant_id"], actor_id)
            approval_id, now = str(uuid4()), utc_now()
            connection.execute(
                "UPDATE requisitions SET status = 'awaiting_owner', updated_at = %s WHERE id = %s",
                (now, requisition_id),
            )
            connection.execute(
                """
                INSERT INTO approvals (
                    id, requisition_id, tenant_id, reviewed_version, owner_id,
                    status, decision_reason, decided_by, decided_at, created_at
                ) VALUES (%s, %s, %s, %s, %s, 'pending', NULL, NULL, NULL, %s)
                """,
                (approval_id, requisition_id, req["tenant_id"], req["version"], req["business_owner_id"], now),
            )
            self._audit(
                connection, tenant_id=req["tenant_id"], actor_id=actor_id,
                action="approval.requested", target_type="approval", target_id=approval_id,
                correlation_key=correlation_key,
                after={"reviewed_version": req["version"], "status": "pending"},
            )
            event_key = f"owner-review:{approval_id}:{req['business_owner_id']}"
            connection.execute(
                """
                INSERT INTO notification_outbox (
                    id, tenant_id, recipient_id, event_key, payload_json, status, created_at
                ) VALUES (%s, %s, %s, %s, %s, 'pending', %s)
                """,
                (
                    str(uuid4()), req["tenant_id"], req["business_owner_id"], event_key,
                    Jsonb({"approval_id": approval_id, "requisition_id": requisition_id}), now,
                ),
            )
            return approval_id

    def decide_approval(self, *, approval_id: str, actor_id: str, decision: str, reason: str, correlation_key: str) -> None:
        if decision not in {"approved", "rejected", "changes_requested"}:
            raise DomainError("Decision must be approved, rejected, or changes_requested.")
        if not reason.strip():
            raise DomainError("An explicit decision reason is required.")
        with self._connection() as connection:
            approval = connection.execute(
                "SELECT * FROM approvals WHERE id = %s", (approval_id,),
            ).fetchone()
            if approval is None:
                raise DomainError("Approval was not found.")
            req = self._requisition(connection, approval["requisition_id"])
            if actor_id != approval["owner_id"]:
                raise DomainError("Only the currently assigned business owner can decide this approval.")
            if approval["status"] != "pending" or req["version"] != approval["reviewed_version"]:
                raise DomainError("Approval is no longer current.")
            status = "approved" if decision == "approved" else "draft"
            now = utc_now()
            connection.execute(
                """
                UPDATE approvals
                SET status = %s, decision_reason = %s, decided_by = %s, decided_at = %s
                WHERE id = %s
                """,
                (decision, reason, actor_id, now, approval_id),
            )
            connection.execute(
                "UPDATE requisitions SET status = %s, updated_at = %s WHERE id = %s",
                (status, now, req["id"]),
            )
            self._audit(
                connection, tenant_id=req["tenant_id"], actor_id=actor_id,
                action=f"approval.{decision}", target_type="approval", target_id=approval_id,
                correlation_key=correlation_key,
                before={"status": "pending"}, after={"status": decision},
            )

    def withdraw_requisition(self, *, requisition_id: str, actor_id: str, correlation_key: str) -> None:
        with self._connection() as connection:
            req = self._requisition(connection, requisition_id)
            if actor_id != req["requester_id"]:
                raise DomainError("Only the requester may withdraw this prototype requisition.")
            if req["status"] == "approved":
                raise DomainError("Approved work needs a recall/compensation flow, not withdrawal.")
            now = utc_now()
            connection.execute(
                """
                UPDATE requisitions
                SET status = 'withdrawn', version = version + 1, updated_at = %s
                WHERE id = %s
                """,
                (now, requisition_id),
            )
            connection.execute(
                "UPDATE approvals SET status = 'revoked' WHERE requisition_id = %s AND status = 'pending'",
                (requisition_id,),
            )
            event_id = self._audit(
                connection, tenant_id=req["tenant_id"], actor_id=actor_id,
                action="requisition.withdrawn", target_type="requisition", target_id=requisition_id,
                correlation_key=correlation_key,
                before={"status": req["status"]}, after={"status": "withdrawn"},
            )
            connection.execute(
                """
                INSERT INTO recovery_journal (
                    id, tenant_id, original_action_id, action, status, outcome_evidence, created_at
                ) VALUES (%s, %s, %s, 'restore_draft', 'available', NULL, %s)
                """,
                (str(uuid4()), req["tenant_id"], event_id, now),
            )

    @staticmethod
    def _assert_active_user(connection: Connection, tenant_id: str, user_id: str) -> None:
        user = connection.execute(
            "SELECT 1 FROM users WHERE id = %s AND tenant_id = %s AND active = TRUE",
            (user_id, tenant_id),
        ).fetchone()
        if user is None:
            raise DomainError("User is not an active member of this tenant.")

    @staticmethod
    def _requisition(connection: Connection, requisition_id: str) -> dict[str, Any]:
        row = connection.execute(
            "SELECT * FROM requisitions WHERE id = %s", (requisition_id,),
        ).fetchone()
        if row is None:
            raise DomainError("Requisition was not found.")
        return row
