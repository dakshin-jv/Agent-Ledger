---
type: Decision Register
title: Requirements, working directions and unresolved choices
description: A decision register that distinguishes user instructions from proposals.
tags:
- erp
- design
- progress
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T16:14:35+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: checkpoint-recorded
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Decision authority

“Requirement” means explicitly stated by the user. “Working direction” means proposed in the discussion and used as the basis for the next step. It does not imply final granular approval.

| ID | Decision / constraint | Standing | Basis |
|---|---|---|---|
| R-01 | Design granularly and step by step | Requirement | User correction after ERP overview |
| R-02 | Do not create everything at once | Requirement | User pacing instruction |
| R-03 | Aim for an ERP with an experience capable of replacing existing ERPs | Requirement / product goal | User stated main goal |
| R-04 | Preserve progress and room for future steps | Requirement | Current bundle request |
| R-05 | Ask when materially below 95% confidence | Requirement | Earlier project instruction |
| R-06 | Use the actual OKF bundle format found online | Requirement | User response to format clarification |
| D-01 | Intent first, structured records and granular control underneath | Working direction | Two-layer proposal |
| D-02 | Home, Work, Orders, Money, Network, Intelligence | Working direction | Step 2 exploration |
| D-03 | Settings outside primary six tabs | Working direction | Step 2 proposal |
| D-04 | Home has five zones | Working direction | Step 3 exploration |
| D-05 | Retain direct UI and full-form access | Working direction | Guided creation proposal |
| D-06 | Financial/high-impact work gets a reviewable approval boundary | Working direction | Step 3 risk-aware behaviour |
| D-07 | Global command uses current record context | Working direction | Step 3 persistent-agent proposal |
| D-08 | Agents embedded throughout workspaces | Working direction | Step 2 / Step 3 proposal |
| D-09 | Next detailed screen is Work | Planned next step | End of Step 3 |

# Not decided

Final name; exact visual system; operational inventory destination; Agents or Automation destinations; detailed finance coverage; chosen industry; target role; autonomous authority; exact priority formula; final implementation stack.

# Future decision entry

Record a stable ID, question, alternatives, user decision, rationale, affected concepts, date and remaining uncertainty. Keep superseded decisions as history and make the current choice unambiguous. Use [the template](/next-steps/design-step-template.md).

# Session 2 additions

| ID | Direction | Standing |
|---|---|---|
| R-07 | Happy path first, fallback paths next | Explicit user direction |
| R-08 | Develop agent by agent | Explicit user direction |
| R-09 | Prioritise Channel3, Render, APIMatic, AG Grid, Bryntum | Explicit user direction |
| R-10 | Maintain one current OKF bundle | Explicit user direction |
| D-10 | Shared business agents across screens, isolated per-request runs | Working direction |
| D-11 | Astropods hosts agents; Render orchestrates | Proposed architecture explored with user; integration pending |
| D-12 | Sarvam language processing and Jev bounded evaluation | Proposed API roles; user reports available keys |
| D-13 | Elastic retrieval; SQL business truth; Bryntum UI | Proposed data boundary |
| D-14 | Procurement as first agent | Recommendation, not selected |

Earlier default deferral of Bryntum is superseded by R-09: design a meaningful timeline contribution in the first relevant workflow. Full six-tab navigation remains a working direction, not a finished UI.

# PayPal requirement update

- R-11: PayPal Sandbox is required for our project and the hackathon integration.
- R-12: PayPal AI Toolkit is an explicit user-required project tool; installation and usage pending.

# Enterprise / database decisions

- R-13: Design for enterprise requirements; product categories are examples.
- D-15: Render PostgreSQL is the store, behind one backend.
- D-16: Production scaling remains open.
- D-17: AP/AR/Treasury/R2R have distinct Finance responsibilities; O2C/P2P/S2P are cross-functional workflows.
- D-18: AG Studio is an analytics candidate only.

# Current goods-intake design checkpoint — revision 0.4.0

User selected goods only (supersedes the earlier both-goods-and-services discussion). Services deferred for lack of data. Demo-labelled internal datasets and PayPal Sandbox selected. Sarvam and TypeSafe both required. Human approval and recovery required at every step. Design only: do not build, seed, configure or call services in this delivery.

- [Dataset design](/architecture/demo-dataset-design.md)
- [Service setup, human approval and recovery](/architecture/service-setup-design.md)
- [PayPal datasets and setup](/architecture/paypal-sandbox-dataset-setup.md)

Goods-intake schema, forward/recovery transitions and scenario definitions are documented as proposals, not implemented or tested. No stock/contracts/policy datasets or API credentials have been supplied or verified. Next: review fixture configuration (country, currency, goods category, users and illustrative rules), then detailed specification-stage design. Future Codex implementation must update progress with evidence and preserve this single bundle.

# Specification owner routing checkpoint — revision 0.5.0

Business owner approves goods specifications for now; RBAC implementation planned. Non-owner action creates a pending owner review and notification; no proxy approval. Missing/unavailable owners remain pending for controlled assignment. Material edits, withdrawal and owner reassignment invalidate affected reviews; stale notifications cannot authorize execution. Intake funding authority remains distinct. See [Specification Agent](/agents/goods-specification-agent.md). Design-only; implementation and tests pending. Next: goods sourcing design.

# Latest scheduling and RBAC direction

RBAC will be implemented; current delivery is design only. Render Cron Jobs plus Workflows recommended for owner reminders/retries, with immediate initial notification via outbox. See [scheduled owner notifications](/architecture/scheduled-owner-notifications.md). This supersedes earlier RBAC-deferral wording. Delivery timing/channel and detailed permission policy await review.

# Draft rough spec reconciliation (2026-10-18)

Repo drafts `docs/agent-ledger-architecture-spec.md`, `docs/agent-ledger-department-matrix.md` and `docs/deployment/render.blueprint.draft.yaml` are proposals, not decisions. Where they conflict, the standing entry below holds until the user decides.

| ID | Draft proposal | Conflicts with | Standing until decided |
|---|---|---|---|
| P-01 | Next.js + AG Grid frontend | `frontend/app` React/Vite + Bryntum; `docs/bryntum.md` (AG Grid evaluation only) | Bryntum is the production UI; AG Grid evaluation only (D-18) |
| P-02 | Key Value queue for A2A tasks; Background Worker per department | D-15 Postgres sole store; outbox in Postgres | Postgres authoritative; Key Value only as optional cache/lock |
| P-03 | SQLite for local dev | BUILD_START_HERE step 4 | Render PostgreSQL locally too |
| P-04 | TypeSafe only when key set, else fallback | `docs/typesafe.md` (TypeSafe required) | TypeSafe required; fallback is degraded mode |
| P-05 | LangGraph + deepagents, one MCP server per department | `docs/render_agent_sdk.md` harness; backend policy adapter | Harness + policy adapter; per-department MCP pending review |
| P-06 | Ten departments incl. HR, Manufacturing, Projects | AGENTS.md capability table; goods-only scope; D-17 | Only authorised rows; extras parked |
| P-07 | Finance-first build order to Nov 12 | R-01/R-02/R-08; Procurement in progress | Procurement stays first |
| P-08 | Multi-provider Model Gateway | R-09 sponsor priorities | Sarvam + TypeSafe; gateway interface allowed |

Adoptable without conflict (still proposals): typed Pydantic decision contracts, money rail as sole PayPal caller, `plugin.yaml` permission manifest, real PayPal API names only.
