# AgentLedger

## Problem

A commerce operator should state what they want done—create, check,
investigate, approve, or recover—and stay on that case: the lines, money,
owner, evidence, and next action. Home answers what needs me, what is
moving, and what happens next. Work is the inbox. Orders, Money, Network,
and Intelligence hold the same case from different sides. Chat drafts and
routes; it does not replace the ledger, permissions, or history.

## Approach

**Usual ERP.** Work is split by department (Sales, Purchase, Warehouse,
Finance, Vendors). Each task follows module → list → record → form →
approval → report. One commercial event—order, stock, PO, bill,
payment—is stored in several modules.

**Cost.** Completing that event requires screen hops and re-entry of the
same facts. Alerts arrive without a single owner. Overlaying chat does
not fix this: the ledger, who may approve, and the audit trail remain
scattered.

**Design.** Intent first, records second, modules third. Keep one case
end to end: the operator states intent; an agent drafts on that case;
the assigned owner accepts or returns the current version; funding is a
separate gate. The ledger holds lines, money, owner, and evidence. Home,
Work, Orders, Money, Network, and Intelligence are views of that case,
not separate products. Lists and forms remain for precise fields.
Agents run one isolated case at a time, only inside granted authority.
Every step has a recovery path (withdraw, undo, or reverse). Goods only
for now; services wait on data. Method:
[`plan/ERP_Design_OKF_Bundle/`](plan/ERP_Design_OKF_Bundle/).

Do not commit, deploy, connect providers, or make financial mutations unless
asked.

## Agent departments and workflows

Agents are **capabilities**, not pages. Finance functions are distinct from
cross-functional flows (OKF D-17). Stage is `docs` → `agents` → `refine`.
Status is `pending`, `inprogress`, or `complete`. Do not implement a row
the user has not authorized.

| Area | Kind | Stage | Status | Human developer remarks |
| --- | --- | --- | --- | --- |
| Orders / O2C | Cross-functional | docs | pending | |
| Procurement / P2P / S2P (goods) | Cross-functional | docs | inprogress | |
| Inventory / receiving | Operations | docs | pending | |
| AP | Finance | docs | pending | |
| AR | Finance | docs | pending | |
| Treasury | Finance | docs | pending | |
| R2R | Finance | docs | pending | |
| Suppliers / Network | Master data | docs | pending | |
| Customer service | Case work | docs | pending | |
| Analytics / Intelligence | Insight | docs | pending | |
| Administration | Settings | docs | pending | |

## Read this when

| Open | When | Not for |
| --- | --- | --- |
| [`docs/coding-agents.md`](docs/coding-agents.md) | New coding client, MCP/skill install, which MCP to enable this session | Provider API contracts or runtime adapter rules |
| [`docs/paypal.md`](docs/paypal.md) | Sandbox orders, invoices, refunds, Postman collection, payment adapter | Catalog search, deploy, UI grid |
| [`docs/render.md`](docs/render.md) | Deploy, env groups, PostgreSQL, Workflows, Cron, Render MCP | Provider catalog/search or Bryntum widgets |
| [`docs/channel3.md`](docs/channel3.md) | Product search, offers, provenance on catalog data | Payments or Render ops |
| [`docs/sarvam.md`](docs/sarvam.md) | STT/TTS/translate/LLM in a workflow | Persistence or payments |
| [`docs/elastic.md`](docs/elastic.md) | Retrieval, Agent Builder, index/API fallback | Transactional store |
| [`docs/typesafe.md`](docs/typesafe.md) | Typed extraction, routing, verification | Treating community MCP as runtime authority |
| [`docs/bryntum.md`](docs/bryntum.md) | Grid, TaskBoard, Scheduler, Gantt, bundle split | A second production grid |
| [`plan/BUILD_START_HERE.md`](plan/BUILD_START_HERE.md) | Scope, access checklist, execution order | Day-to-day adapter implementation |
| [`plan/ERP_Design_OKF_Bundle/`](plan/ERP_Design_OKF_Bundle/) | Workflows, UX, data contracts | Coding-agent MCP setup |
| [`plan/compare_top_tier_erp_sys/`](plan/compare_top_tier_erp_sys/) | How SAP/Oracle/etc. use agents vs this design | Provider setup or implementation |
