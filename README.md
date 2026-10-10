# AgentLedger

AgentLedger is an agent-native enterprise commerce ERP prototype. The first
implemented workflow is a safe foundation for goods procurement:
tenant-scoped records, owner-controlled approvals, audit events,
notification outbox entries, and recovery records on Render PostgreSQL.

## Local setup

This project uses Python 3.13+ and `uv`.

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

Copy `.env.example` to `.env` only when configuring local provider access.
Never commit `.env`; it contains credentials. PayPal configuration is
Sandbox-only, and no payment execution is part of the current foundation.

## Current scope

Start with [`AGENTS.md`](AGENTS.md). Product and workflow design is in
[`plan/ERP_Design_OKF_Bundle/`](plan/ERP_Design_OKF_Bundle/) and
[`plan/BUILD_START_HERE.md`](plan/BUILD_START_HERE.md). Service contracts
are in [`docs/`](docs/).

External integrations, deployment, notifications, and payment execution remain
separate, explicitly authorised milestones.
