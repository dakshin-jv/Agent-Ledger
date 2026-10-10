---
type: Source Record
title: Session 2 — agent development and service priorities
description: The user directions and working architecture discussed after the initial
  bundle.
tags:
- erp
- agents
- references
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Source and authority

This is a summary of the visible follow-up conversation on 7 October 2026, not a verbatim transcript. No live provider integration or implementation was performed.

# Explicit user directions

- Develop the happy path first, then fallback paths for each agent.
- Develop agent by agent.
- Give high importance to Channel3, Render, APIMatic, AG Grid and Bryntum while building an innovative application and services.
- Add and modify this existing bundle; maintain a single OKF bundle.
- User reports having Sarvam and TypeSafe API keys. No keys were supplied or tested.

# Discussion and proposals

Step 4 Work began: Needs me, Agents working, Waiting and Completed; ownership-based views; a queue item with business issue, impact, next decision, responsible party, timing and primary action. Detail progresses through what happened, evidence, options, decision and next outcome. First user role is unresolved.

Agents are proposed around business responsibilities and shared across screens. A per-order agent workspace holds isolated execution context and history rather than requiring a separately authored agent for every order. A global assistant can initially route requests.

Astropods agent hosting plus Render workflow orchestration was proposed and explored positively. This is the current architecture direction to evaluate, not a tested deployment. Sarvam and TypeSafe/Jev can be called by server-side code; built-in native provider support was not confirmed.

Channel3 supplies external discovery data; Elastic supplies searchable knowledge; Bryntum is the schedule/timeline UI. PostgreSQL is proposed for transactional records, not selected by the user. Procurement was recommended as the first workflow; the user has not explicitly selected the first workflow or persona.

# Scope limits

Ten commerce workflow families were suggested as an initial grouping, not an exhaustive scenario count or an approved build scope. Unknown external events must produce visible waiting/review states rather than indefinite autonomous execution. Detailed state contracts, endpoint authentication, SDK versions and payment execution model remain open.
