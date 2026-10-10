# Coding agents

**Read when:** setting up Cursor, Codex, or Claude Code; installing skills; choosing which MCP to enable this session.

**Do not use for:** provider API contracts, runtime adapter rules, or domain write paths. Those live in the service files linked from `AGENTS.md`.

## Layers

| Layer | What it is | Who uses it |
| --- | --- | --- |
| **Skills** | On-demand instructions; cheap in context | Coding agent while editing the repo |
| **MCP (coding)** | Docs search, sandbox probes, Render ops | Coding agent; connect only for the current task |
| **Runtime platform** | Render services, PostgreSQL, Workflows, Cron | Deployed application and `backend/src/agents/` |
| **Runtime integration** | Backend policy adapter → provider MCP or SDK/API | Production agents; never raw model-to-provider |

Keep skills installed. Enable **one** relevant MCP server per workstream.

## Client config

MCP registrations, OAuth grants, and local CLI tools are not shared between coding agents. Repository files travel through Git; each client needs its own local setup.

| Coding agent | MCP config | Shared skills |
| --- | --- | --- |
| Cursor | `.cursor/mcp.json` | `.agents/skills/` |
| Codex | `.codex/config.toml` | `.agents/skills/` |
| Claude Code | `.mcp.json` | `.agents/skills/` |

Install provider skills into `.agents/skills/` (and `skills-lock.json`). Do not copy or symlink them into `.claude/skills/`, `.codex/skills/`, or `.cursor/skills/`.

Launch local MCP servers with `.env` via `envFile` or a wrapper; never commit secrets. Host docs: [Codex MCP](https://developers.openai.com/learn/docs-mcp), [Cursor MCP](https://docs.cursor.com/context/model-context-protocol), [Claude Code MCP](https://docs.anthropic.com/en/docs/mcp).

## Local tools

| Tool | Why | Install |
| --- | --- | --- |
| Git | Source control | [git-scm.com](https://git-scm.com/downloads) |
| Node.js 18+ and npm | React/Vite, Bryntum, local stdio MCPs | [nodejs.org](https://nodejs.org/) |
| Python 3.13 and `uv` | Backend, tests, migrations, Python MCPs | [uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Render CLI | Deploy/diagnostics and Render skill install | [Render CLI](https://render.com/docs/cli) |
| Postman desktop or CLI | PayPal collection outside the agent chat | [Postman](https://www.postman.com/downloads/) |

Tests: `uv run python -m unittest discover -s tests -v`. Call out migrations, new env vars, and new integrations at handoff. Credentials stay in the ignored `.env`; `.env.example` holds names only. Render uses environment groups.

## Skills to install

| Skill / plugin | When | Source |
| --- | --- | --- |
| Render skill set | Deploy, blueprints, env, PostgreSQL, workflows, debug | [Render skills](https://github.com/render-oss/skills) · `render skills install` |
| `bryntum` + `bryntum-react` | Grid, TaskBoard, Scheduler, Gantt | [Bryntum skills](https://github.com/bryntum/skills) |
| `channel3-api` | Catalog search and Channel3 SDK work | [Channel3 skills](https://github.com/channel3-ai/skills) |
| `typesafe-ai` | Typed extraction, routing, verification | [TypeSafe docs](https://docs.typesafe.ai/llms.txt) |
| APIMatic PayPal context plugin | PayPal API contract while writing adapters | [APIMatic installer](https://github.com/apimatic/context-plugins-installer) |

## MCP catalog

Do not place API keys in committed MCP JSON/TOML. Use `.env` or provider OAuth.

| Suggested name | Purpose | Transport | Auth and safety |
| --- | --- | --- | --- |
| `postman` | Collections, including PayPal's public collection | Remote [Postman MCP](https://learning.postman.com/docs/reference/postman-api/postman-mcp-server/overview) | Per-client auth; Sandbox PayPal environments |
| `paypal-sandbox` | Supervised PayPal Sandbox exploration | Local [`@paypal/mcp`](https://github.com/paypal/paypal-mcp-server) or [hosted](https://developer.paypal.com/ai-tools/mcp-server) | Sandbox only; no unrestricted financial tools on deployed agents |
| `render` | Services, deploys, logs, resources | Remote `https://mcp.render.com/mcp` | OAuth; can change infrastructure |
| `elastic-docs` | Official Elastic documentation | Remote `https://www.elastic.co/docs/_mcp/` | Docs only; no business data |
| `elastic-agent-builder` | Bounded search / Agent Builder work | [Agent Builder MCP](https://www.elastic.co/docs/solutions/search/agent-builder/mcp-server) | Least-privilege API key |
| `channel3` | Catalog exploration during procurement work | Remote `https://mcp.trychannel3.com` | API key from `.env`; persist through backend |
| `sarvam` | Language and voice discovery | Local stdio [Sarvam MCP](https://docs.sarvam.ai/api/developer-tools/mcp) | `SARVAM_API_KEY`; production via adapter |
| `typesafe` | Development assistance | Community adapter; [TypeSafe API](https://docs.typesafe.ai/) is authoritative | Not an official hosted data MCP |
| `bryntum` | Component documentation | Remote `https://mcp.bryntum.com` | Docs/dev only |
| `ag-grid` | Grid evaluation when a product decision calls for it | Local [AG Grid MCP](https://github.com/ag-grid/ag-mcp) | Bryntum Grid is the application grid |
| `context7` | Third-party library docs | Remote `https://mcp.context7.com/mcp` | Docs only; no secrets in queries |

## Quick picks

| Task type | Skills | MCP |
| --- | --- | --- |
| Frontend / Bryntum | `bryntum`, `bryntum-react` (+ feature skills) | Usually none |
| Backend domain / `foundation.py` | — | None |
| Render deploy or debug | Relevant `render-*` skills | `render` |
| PayPal integration | APIMatic plugin | `paypal-sandbox` (optionally `postman`) |
| Channel3 / Sarvam / Elastic | Matching skill where it exists | Matching provider MCP for that session only |
| TypeSafe judgments | `typesafe-ai` | `typesafe` only for experiments |
| General library docs | — | `context7` |

## Service map

Full skill/MCP/runtime rules live in the service file. Use this table only to pick a file:

| Working on… | Open |
| --- | --- |
| Approvals, audit, tenancy, `FoundationStore`, PostgreSQL | [`render.md`](render.md) |
| Deploy, env groups, Workflows, Cron | [`render.md`](render.md) |
| PayPal sandbox, Postman, payment adapter | [`paypal.md`](paypal.md) |
| Catalog search | [`channel3.md`](channel3.md) |
| Language / voice | [`sarvam.md`](sarvam.md) |
| Retrieval / Agent Builder | [`elastic.md`](elastic.md) |
| Typed extraction / routing | [`typesafe.md`](typesafe.md) |
| Grid, TaskBoard, Scheduler, Gantt | [`bryntum.md`](bryntum.md) |

## Completion check

1. Install local tools and open this repository.
2. Restore `.env` from the secure credentials source; do not commit it.
3. Install skills/plugins for that coding agent.
4. Add MCPs for the current task, authenticate, and confirm they are connected.
5. Read `AGENTS.md`, this file, and the service file for the task. Run backend tests and the frontend build before changing application behavior.
6. Runtime provider calls go through the policy adapter. Never expose MCP or SDK/API directly to an untrusted model.

## Operating model

When a provider offers an official MCP and an SDK/API, prefer MCP through the Agent Ledger policy adapter. Keep the SDK/API as a tested fallback for unsupported MCP capabilities, outages, webhooks, or deterministic background work. Financial actions require approval, idempotency, and audit. An autonomous agent must never receive unrestricted payment, refund, payout, dispute, or raw database access.

## Related

[`AGENTS.md`](../AGENTS.md) · [`.env.example`](../.env.example)
