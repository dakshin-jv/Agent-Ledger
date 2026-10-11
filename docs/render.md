# Render

**Read when:** deploy, environment groups, PostgreSQL, Workflows, Cron, or Render MCP.

**Do not use for:** provider catalog/search ([`channel3.md`](channel3.md)) or Bryntum widgets ([`bryntum.md`](bryntum.md)).

**Index (fetch one page, don’t dump all):** [docs](https://render.com/docs.md) · [coding-agent setup](https://render.com/agents.md) · [platform tasks](https://render.com/agents/tasks.md) · search `https://render.com/api/agent/docs-search?query=` · page `https://render.com/docs/{slug}.md`

## Role in Agent Ledger

Render hosts the API, Workflows, Cron, and PostgreSQL. Product agents = **Workflow tasks** (Python SDK). Coding agents (Cursor, Claude Code, Codex) use **Render MCP** for infra only.

## Features

Suggest only what exists on Render. MCP can **create**: web, static, cron, Postgres, Key Value. **Not via MCP:** Workflow, private service, worker — Blueprint/CLI/Dashboard ([MCP limits](https://render.com/docs/mcp-server)).

| Kind | Product | Doc |
| --- | --- | --- |
| Compute | [Service types](https://render.com/docs/service-types) | web, static, private, worker, cron, workflow |
| | [Web](https://render.com/docs/web-services) | public HTTP, `PORT`, TLS at edge |
| | [Private](https://render.com/docs/private-services) | private hostname only |
| | [Worker](https://render.com/docs/background-workers) | always-on, no ingress — prefer Workflows for on-demand agent runs |
| | [Cron](https://render.com/docs/cronjobs) | UTC schedule, exit when done |
| | [Static](https://render.com/docs/static-sites) | CDN; no server logic |
| | [Workflows](https://render.com/docs/workflows) | on-demand tasks; scales to zero |
| | [Plans](https://render.com/docs/compute-plans) | CPU/RAM; Workflow `flex`… on the **task** |
| | [Docker](https://render.com/docs/docker) · [native runtimes](https://render.com/docs/native-runtimes) | |
| Data | [Postgres](https://render.com/docs/postgresql) | SoR; [connect](https://render.com/docs/postgresql-creating-connecting) · [pool](https://render.com/docs/postgresql-connection-pooling) · [HA](https://render.com/docs/postgresql-high-availability) · [replicas](https://render.com/docs/postgresql-read-replicas) · [backups](https://render.com/docs/postgresql-backups) |
| | [Key Value](https://render.com/docs/key-value) | cache/queue; optional |
| | [Disks](https://render.com/docs/disks) | sticky FS; not for Workflows |
| Agent run | [First workflow](https://render.com/docs/workflows-get-started) · [define](https://render.com/docs/workflows-defining) · [trigger](https://render.com/docs/workflows-running) · [local](https://render.com/docs/workflows-local) · [limits](https://render.com/docs/workflows-limits) | [Python SDK](https://render.com/docs/workflows-sdk-python) · [TS SDK](https://render.com/docs/workflows-sdk-typescript) |
| Ship | [Deploys](https://render.com/docs/deploys) · [Blueprints](https://render.com/docs/infrastructure-as-code) · [YAML](https://render.com/docs/blueprint-spec) · [env](https://render.com/docs/configure-environment-variables) | [previews](https://render.com/docs/service-previews) · [preview envs](https://render.com/docs/preview-environments) — Workflows **skip** preview copy |
| Net | [Private network](https://render.com/docs/private-network) · [regions](https://render.com/docs/regions) · [domains](https://render.com/docs/custom-domains) · [health](https://render.com/docs/health-checks) | [scale](https://render.com/docs/scaling) · [jobs](https://render.com/docs/one-off-jobs) · [SSH](https://render.com/docs/ssh) |
| Observe | [Metrics](https://render.com/docs/service-metrics) · [logs](https://render.com/docs/logging) · [webhooks](https://render.com/docs/webhooks) | |
| Agent ops | [MCP](https://render.com/docs/mcp-server) · [CLI](https://render.com/docs/cli) · [API](https://render.com/docs/api) | [Cursor](https://render.com/agents/cursor.md) · [Claude Code](https://render.com/agents/claude.md) · [Codex](https://render.com/agents/codex.md) |
| Other | [Sandboxes](https://render.com/docs/sandboxes) · [Projects](https://render.com/docs/projects) · [plan features](https://render.com/docs/platform-features-by-plan) | HIPAA: no **new** Workflows in HIPAA workspaces ([FAQ](https://render.com/docs/workflows)) |

Compare runtimes: [cron vs worker vs workflow](https://render.com/articles/cron-jobs-vs-background-workers-vs-workflows).

### Web / API and private services

HTTP API + policy. `backend/routers/`, `backend/src/config/` (`DATABASE_URL`), domain in `backend/src/agents/`. Workflow tasks **HTTP to this API**. Bind `0.0.0.0:$PORT`.

### PostgreSQL

Writes only via `FoundationStore` + `backend/migrations/`. No task-level SQL. No write via MCP (`query_render_postgres` is **read-only**).

Mutation: auth, tenant, audit, idempotent `correlation_key`, recovery. Assigned owner + current version; funding separate; model ≠ approve/pay. Provenance labels. UTC. Decimals.

Services: **internal** URL, same region. Local: **external** + TLS.

### Workflows

**SDK = product agent.** MCP ≠ this.

1. `render>=1.0.1` (`import render`). Entrypoint ≠ web start.
2. `@app.task`, `TaskContext` first, JSON I/O, `app.start()`.
3. `await ctx.run(...)` same workflow. Timeout 30–86400s. Retries repeat effects → idempotent key. Timeout ≠ commit/pay retry.
4. Trigger: `Render` / `RenderAsync` + `RENDER_API_KEY`; slug `{workflow}/{task}`; or `POST /v1/task-runs`.
5. Local: `render workflows dev -- <start>`. Deploy: Blueprint `type: workflow` (no service `plan`) or CLI. **MCP cannot create Workflows.**
6. No `psycopg` in the task. Private-net to API/Postgres in-region (runs **initiate** connections; no inbound ports).

### Cron

UTC, no disk, no DB, HTTP API. Pair with Workflows for schedules ([FAQ](https://render.com/docs/workflows)).

### Key Value

Optional. No agent access unless you later need cache/queue.

### Planned internal MCP

Future **product** tools → our adapters. Not Render MCP. Not DB/pay.

### Render MCP (coding)

**MCP = Cursor / Claude Code / Codex infra.** [MCP](https://render.com/docs/mcp-server) · host `https://mcp.render.com/mcp`.

Use: workspace, create/list web/static/cron/Postgres/KV, env, deploy, logs, metrics, read-only SQL.

Don’t: author `@app.task`, create Workflow/private/worker, treat MCP as runtime.

Workspace first. Ops only. **Not deployed with the app.**

## Coding agent

| Job | Use |
| --- | --- |
| Write/run product agent | Python SDK + skill `render-workflows` |
| Create/inspect allowed resources | MCP `render` + `render-mcp` / `render-deploy` / `render-blueprints` / `render-postgres` / `render-cron-jobs` |
| Unknown feature | Fetch [docs.md](https://render.com/docs.md) or `docs-search` — don’t invent |

Connect MCP only for deploy/ops.

## Runtime

Web/API, Postgres, Workflows (SDK), Cron. Coding-agent MCP absent.

## Secrets / env

`DATABASE_URL`, `RENDER_API_KEY` ([`.env.example`](../.env.example)). Env groups. Workflow: API key + API URL, not a raw DB URL if the API owns the store.

Official: [Dashboard](https://dashboard.render.com/) · [docs](https://render.com/docs) · [MCP](https://render.com/docs/mcp-server) · [Postgres](https://render.com/docs/postgresql) · [Workflows](https://render.com/docs/workflows) · [Python SDK](https://render.com/docs/workflows-sdk-python) · [API](https://render.com/docs/api) · [CLI](https://render.com/docs/cli) · [Blueprint](https://render.com/docs/infrastructure-as-code)

## Related

[`coding-agents.md`](coding-agents.md) · [`plan/BUILD_START_HERE.md`](../plan/BUILD_START_HERE.md)
