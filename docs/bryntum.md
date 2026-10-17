# Bryntum

**Read when:** Grid, TaskBoard, Scheduler, Gantt, or frontend bundle split.

**Do not use for:** adding a second production grid. Bryntum Grid is the application grid.

## Role in Agent Ledger

The React/Vite UI in `frontend/app/` uses licensed/trial `@bryntum/*` npm packages. Bryntum MCP and skills are development aids. Persistence goes through the Agent Ledger API.

## Features

### Grid

Operational tables: attention queue, exceptions, approvals, and editable work-item data. [Grid docs](https://bryntum.com/products/grid/docs/)

### TaskBoard

Agent Board: work-item lifecycle, swimlanes, WIP limits, and human/agent ownership. [TaskBoard docs](https://bryntum.com/products/taskboard/docs/)

### Scheduler

Timelines for assignments, owner reviews, agent runs, and follow-ups. [Scheduler docs](https://bryntum.com/products/scheduler/docs/)

### Gantt

Plans, dependencies, critical path, and program-level coordination. [Gantt docs](https://bryntum.com/products/gantt/docs/)

### Skills over MCP

Load `bryntum` and `bryntum-react`. Add `bryntum-crud`, `bryntum-features`, or `bryntum-theming` when the task needs them. Skip Bryntum MCP unless documentation lookup is stuck.

### Deferred: lazy workspace bundles

The prototype imports Grid, TaskBoard, Scheduler, and Gantt in the initial bundle (a large production JavaScript asset). Split each workspace into a React view and load it when the user opens that workspace (`lazy` / `Suspense`).

- `AttentionView` owns Grid imports and styles
- `BoardView` owns TaskBoard
- `ScheduleView` owns Scheduler
- `PlanView` owns Gantt

Keep Bryntum configuration in the lazy-loaded view. Vite `optimizeDeps` helps the dev server; it does not reduce the production bundle. `manualChunks` can improve caching; lazy views solve initial-load cost.

Acceptance: default workspace loads without Scheduler or Gantt in the first network requests; each workspace loads once without CSS flash or StrictMode errors; `npm run build` emits separate async chunks.

### AG Grid evaluation

AG Grid / AG Studio is supplemental evaluation tooling. Do not build a duplicate production grid without a documented product decision. AG Grid MCP is development-only.

## Coding agent

- Skills: `bryntum`, `bryntum-react`; add feature skills as needed
- MCP: `bryntum` (optional); `ag-grid` only when a product decision calls for it
- Frontend default: skills, usually no MCP

## Runtime

`@bryntum/*` packages in the React app plus the Agent Ledger API. No Bryntum MCP at runtime.

## Secrets / env

Bryntum trial/licence is a product entitlement, not an `.env` API key. `AG_STUDIO_LICENSE_KEY` / `AG_STUDIO_TRIAL_EXPIRES_ON` are evaluation-only names in [`.env.example`](../.env.example).

Official links: [Bryntum MCP](https://mcp.bryntum.com) · [Agent skills](https://bryntum.com/agents/skills/) · [AG Grid](https://www.ag-grid.com/documentation/)

## Related

[`coding-agents.md`](coding-agents.md) · [`procurement.md`](procurement.md)
