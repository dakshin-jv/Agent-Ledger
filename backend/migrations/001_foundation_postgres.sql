-- AgentLedger authoritative foundation schema for Render Postgres.
-- Apply via the backend migration runner; do not let agents write around it.

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    data_origin TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS role_assignments (
    user_id TEXT NOT NULL REFERENCES users(id),
    tenant_id TEXT NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (user_id, tenant_id, role)
);

CREATE TABLE IF NOT EXISTS requisitions (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    business_owner_id TEXT NOT NULL REFERENCES users(id),
    requester_id TEXT NOT NULL REFERENCES users(id),
    purpose TEXT NOT NULL,
    status TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    data_origin TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    requisition_id TEXT NOT NULL REFERENCES requisitions(id),
    tenant_id TEXT NOT NULL,
    reviewed_version INTEGER NOT NULL,
    owner_id TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL,
    decision_reason TEXT,
    decided_by TEXT REFERENCES users(id),
    decided_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE (requisition_id, reviewed_version, owner_id)
);

CREATE TABLE IF NOT EXISTS audit_events (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    actor_id TEXT REFERENCES users(id),
    action TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    before_json JSONB,
    after_json JSONB,
    correlation_key TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS notification_outbox (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL REFERENCES users(id),
    event_key TEXT NOT NULL UNIQUE,
    payload_json JSONB NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS recovery_journal (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    original_action_id TEXT NOT NULL REFERENCES audit_events(id),
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    outcome_evidence TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS requisitions_tenant_status_idx
    ON requisitions (tenant_id, status, updated_at DESC);
CREATE INDEX IF NOT EXISTS approvals_owner_status_idx
    ON approvals (tenant_id, owner_id, status, created_at DESC);
CREATE INDEX IF NOT EXISTS notification_outbox_pending_idx
    ON notification_outbox (status, created_at)
    WHERE status = 'pending';
