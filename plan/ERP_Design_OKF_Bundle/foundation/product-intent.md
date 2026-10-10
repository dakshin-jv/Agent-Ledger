---
type: Product Brief
title: Product intent and design boundaries
description: User goals and the agreed pace for designing an agent-native commerce
  ERP.
tags:
- erp
- design
- foundation
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# User requirements

- Think step by step and design the UI feel from scratch.
- Inspect traditional ERP interactions at a granular level before deciding what to remove, replace with agents, or retain in both modes.
- Do not create everything at once.
- Record how the traditional experience works, how many tabs it has, and what each contains.
- Aim for the best user experience for a new ERP that can replace existing ERPs.
- Preserve discussion and progress so subsequent design work can resume.
- Ask questions when not 95% confident; do not silently turn guesses into decisions.

# Current product direction

The earlier commerce-OS ambition is now being developed through an ERP experience. Current interaction principle: **intent first, records second, modules third**.

| Layer | User experience | Purpose |
|---|---|---|
| Intent / agent experience | Ask, create, check, investigate, act | Reduce navigation and manual coordination |
| Operational workspace | Review an order, payment, issue or supplier in context | Keep the user close to the business outcome |
| Granular system of record | Inspect fields, lines, accounting, permissions and history | Support precision, control and auditability |

Keep a structured operational system underneath. A conversational interface alone does not satisfy the design direction.

# Boundaries still open

The replacement ambition is a long-term product goal. Industry, initial user roles, migration scope, localisation, full accounting coverage, manufacturing, HR and hackathon implementation scope remain unresolved. Do not infer that the six visible tabs cover every enterprise requirement.

The [earlier technical architecture](/references/related-architecture.md) supplies historical context. This bundle updates the UX direction without automatically selecting or rewriting its implementation stack.
