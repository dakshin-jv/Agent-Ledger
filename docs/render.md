# Render

**Read when:** deploy, environment groups, PostgreSQL, Workflows, Cron, or Render MCP.

**Do not use for:** provider catalog/search ([`channel3.md`](channel3.md)) or Bryntum widgets ([`bryntum.md`](bryntum.md)).

## Role in Agent Ledger

Render is the deployment and orchestration platform: web/API, private services, workers, Workflows, and Cron. Render PostgreSQL is the store for tenants, work items, approvals, audit records, payment references, and concurrent workflow state.

## Features

### Web / API and private services

Agents live in `backend/src/agents/` and run on Render. Application routes live in `backend/routers/`. Configuration is in `backend/src/config/` (`database.py` → `DATABASE_URL`).

### PostgreSQL

Guarded writes go through `FoundationStore` (`backend/src/database/foundation.py`) and the migration in `backend/migrations/001_foundation_postgres.sql` (`backend/src/database/postgres.py`). There is no agent-facing database MCP and no raw SQL bypass.

Every meaningful mutation needs authorization, tenant isolation, an audit event, an idempotent correlation key, and a defined recovery path where applicable. Business-owner approval needs the assigned current owner and current reviewed version; a role is not enough; funding authority is a separate gate. Model and provider outputs are proposals or evidence, never permission to approve, pay, change ownership, or skip controls. Keep provenance labels (`demo_fixture`, `user_input`, `external_channel3`, `paypal_sandbox`). Unknown is not zero. Money as decimals; UTC timestamps.

Services on Render use the **internal** database URL; local development uses the **external** URL in `.env`.

### Workflows

Durable orchestration for agent jobs, retries, and downstream calls. Workflows invoke authenticated backend APIs after policy checks. Not an MCP server.

### Cron

Scheduled reminders and dispatch in UTC. Cron must not open the database; it calls authenticated backend APIs.

### Key Value

Optional future queue, cache, rate-limit, or short-lived coordination. No direct agent access. Provision only when the workload needs it.

### Planned internal MCP

A future private Render service for domain-safe agent tools (case summaries, approved catalog search, evidence, propose specification, request approval, schedule follow-up). It must call backend adapters and enforce tenant scope, approval, audit, and idempotency. Not a database or payment gateway.

### Render MCP (coding)

Inspect and operate services, deploys, logs, and supported resources. OAuth preferred; scope to the intended workspace. This MCP can change infrastructure — use it only for ops/deploy tasks. The deployed app uses Render services and environment groups, not the coding-agent MCP.

## Coding agent

- Skills: `render-deploy`, `render-blueprints`, `render-env-vars`, `render-postgres`, `render-workflows`, `render-cron-jobs`, `render-debug`, …; start with `render-mcp` if MCP is not connected
- MCP: `render`
- Connect only for deploy/ops work

## Runtime

Render services, PostgreSQL, Workflows, and Cron. Coding-agent Render MCP is not part of the deployed runtime.

## Secrets / env

`DATABASE_URL`, `RENDER_API_KEY` (names in [`.env.example`](../.env.example)). Inject the same secrets through Render environment groups.

Official links: [Dashboard](https://dashboard.render.com/) · [Docs](https://render.com/docs) · [MCP](https://render.com/docs/mcp-server) · [PostgreSQL](https://render.com/docs/postgresql) · [Workflows](https://render.com/docs/workflows)

## Related

[`coding-agents.md`](coding-agents.md) · [`plan/BUILD_START_HERE.md`](../plan/BUILD_START_HERE.md)
