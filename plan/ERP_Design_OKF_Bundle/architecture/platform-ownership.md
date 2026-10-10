---
type: Architecture Decision
title: Astropods agents and Render orchestration
description: The proposed platform split and the backend controls required around
  it.
tags:
- erp
- agents
- architecture
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
- id: astropods-spec
  resource: https://docs.astropods.com/astropods-package-spec
- id: render-workflows
  resource: https://render.com/docs/workflows
design_progress: proposed
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Current direction

Astropods for hosting agent code; Render Workflows for coordinating execution. The user proposed this split and the conversation evaluated it as sensible. Integration is not built or live-tested.

| Component | Proposed responsibility |
|---|---|
| Astropods | Run bounded business agents with their tools and model clients |
| Sarvam / TypeSafe Jev | Language processing / structured evaluation inside server-side code |
| Render Workflows | Dispatch agent calls, chain tasks, timeouts and configured safe retries |
| ERP backend | Authenticate, enforce policy, validate changes and expose business APIs |
| Transactional database | Authoritative orders, stock, approvals, payments and workflow state |
| Frontend | Commands, decisions, status and granular record access |

Render calls an authenticated HTTP endpoint exposed by the hosted agent. This is a custom integration design, not a verified native connector. Request/result schema, authentication and async result mechanism need specification.

# Procurement handoff proposal

ERP saves request → Render invokes Procurement → agent returns recommendation and evidence → backend creates approval item in Work. While approval is pending, save state and finish the task. When approved, the backend starts continuation; the authorised payment service executes and confirms the outcome.

# Ownership rules

- Backend permissions apply before consequential actions.
- Keep one authoritative workflow state in the transactional database.
- Render task status and Astropods run status feed operational visibility; neither alone proves business completion.
- Avoid retrying purchases or payments solely because an agent call timed out.
- Apply duplicate-action protection and verify uncertain external outcomes.
- Do not assume Render provides a complete business approval state machine automatically.

# First integration check

Render → authenticated Astropods endpoint → structured result → saved ERP record. Next test approval continuation. Both are pending, without actual keys or deployments in this task.
