-- Procurement discovery evidence attached to a requisition.
-- Candidates are external observations only: not suppliers, payees, or contracts.
-- Apply via the backend migration runner; do not let agents write around it.

CREATE TABLE IF NOT EXISTS discovery_candidates (
    id           TEXT        PRIMARY KEY,
    requisition_id TEXT      NOT NULL REFERENCES requisitions(id),
    tenant_id    TEXT        NOT NULL,
    actor_id     TEXT        NOT NULL REFERENCES users(id),
    product_id   TEXT        NOT NULL,
    title        TEXT        NOT NULL,
    category     TEXT,
    offers_json  JSONB       NOT NULL,
    data_origin  TEXT        NOT NULL,
    retrieved_at TEXT        NOT NULL,
    linked_at    TIMESTAMPTZ NOT NULL,
    correlation_key TEXT     NOT NULL UNIQUE,
    CONSTRAINT discovery_candidates_origin_check
        CHECK (data_origin = 'external_channel3')
);

CREATE INDEX IF NOT EXISTS discovery_candidates_requisition_idx
    ON discovery_candidates (requisition_id, linked_at DESC);
