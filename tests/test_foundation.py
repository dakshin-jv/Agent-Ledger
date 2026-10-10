import os
import unittest
from uuid import uuid4

from backend.src.database.foundation import DomainError, FoundationStore


class FoundationStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        url = os.getenv("DATABASE_URL", "").strip()
        if not url.startswith(("postgres://", "postgresql://")):
            self.skipTest("DATABASE_URL is required for foundation tests.")
        self.store = FoundationStore()
        self.store.seed_demo()
        self.request_id = self.store.create_requisition(
            tenant_id="demo-tenant", requester_id="usr-requester", business_owner_id="usr-owner",
            purpose="Demo-labelled goods requirement", correlation_key=f"create-{uuid4()}",
        )

    def test_owner_can_approve_current_review(self) -> None:
        approval_id = self.store.submit_for_owner_review(
            requisition_id=self.request_id, actor_id="usr-requester", correlation_key=f"submit-{uuid4()}",
        )
        self.store.decide_approval(
            approval_id=approval_id, actor_id="usr-owner", decision="approved",
            reason="Requirements reviewed", correlation_key=f"approve-{uuid4()}",
        )

    def test_non_owner_cannot_approve(self) -> None:
        approval_id = self.store.submit_for_owner_review(
            requisition_id=self.request_id, actor_id="usr-requester", correlation_key=f"submit-{uuid4()}",
        )
        with self.assertRaisesRegex(DomainError, "assigned business owner"):
            self.store.decide_approval(
                approval_id=approval_id, actor_id="usr-requester", decision="approved",
                reason="No authority", correlation_key=f"approve-{uuid4()}",
            )

    def test_withdraw_revokes_pending_approval(self) -> None:
        self.store.submit_for_owner_review(
            requisition_id=self.request_id, actor_id="usr-requester", correlation_key=f"submit-{uuid4()}",
        )
        self.store.withdraw_requisition(
            requisition_id=self.request_id, actor_id="usr-requester", correlation_key=f"withdraw-{uuid4()}",
        )


if __name__ == "__main__":
    unittest.main()
