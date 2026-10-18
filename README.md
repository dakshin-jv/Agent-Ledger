# AgentLedger

AgentLedger is an in-progress agent-native commerce ERP. The operator states intent and stays on one case: lines, money, owner, evidence, and next action. Goods procurement is the first journey. Design is in [`plan/ERP_Design_OKF_Bundle/`](plan/ERP_Design_OKF_Bundle/). Code holds a Render PostgreSQL foundation (tenant scope, approvals, audit, recovery) and a procurement discovery adapter.

## Status

Goods procurement is in progress. Services and the other departments are not built yet. Payments and deploy stay separately authorised.

Stage and status: [`AGENTS.md`](AGENTS.md). Checkpoint: [`plan/ERP_Design_OKF_Bundle/progress/tracker.md`](plan/ERP_Design_OKF_Bundle/progress/tracker.md).

## Read next

| If you need | Open |
| --- | --- |
| What the product is | [`plan/ERP_Design_OKF_Bundle/start-here.md`](plan/ERP_Design_OKF_Bundle/start-here.md) |
| Build order and access | [`plan/BUILD_START_HERE.md`](plan/BUILD_START_HERE.md) |
| How agents work in this repo | [`AGENTS.md`](AGENTS.md) |
| Coding agent setup | [`docs/coding-agents.md`](docs/coding-agents.md) |
| One provider | The matching file in [`docs/`](docs/) |
| Comparison with other ERPs | [`docs/compare_top_tier_erp_sys/`](docs/compare_top_tier_erp_sys/) |

## External tools

Local: Git, Node.js 18+, Python 3.13, `uv`, Render CLI, Postman. Install notes: [`docs/coding-agents.md`](docs/coding-agents.md).

Providers: [PayPal Sandbox](docs/paypal.md), [Channel3](docs/channel3.md), [Render](docs/render.md), [Sarvam](docs/sarvam.md), [TypeSafe](docs/typesafe.md), [Bryntum](docs/bryntum.md), [Elastic](docs/elastic.md). Access and credentials: [`plan/BUILD_START_HERE.md`](plan/BUILD_START_HERE.md).

## Setup

### Codebase

Python 3.13+ and `uv`.

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

Copy `.env.example` to `.env` for local provider access. Never commit `.env`.

From `frontend/app`: `npm install`, then `npm run build`.

### Coding agent

Pick one client, open its config, then follow [`docs/coding-agents.md`](docs/coding-agents.md). Point the agent at [`AGENTS.md`](AGENTS.md) before it edits. Shared skills: [`.agents/skills/`](.agents/skills/).

| Client | Open |
| --- | --- |
| Cursor | [`.cursor/mcp.json`](.cursor/mcp.json) |
| Codex | [`.codex/config.toml`](.codex/config.toml) |
| Claude Code | [`.mcp.json`](.mcp.json) |
