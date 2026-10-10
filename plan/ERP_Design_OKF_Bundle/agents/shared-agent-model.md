---
type: Agent Architecture
title: Shared business agents across screens
description: Business responsibilities, per-record runs and proposed screen-to-agent
  mapping.
tags:
- erp
- agents
- agents
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: proposed
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# User direction

Develop one agent at a time. Define responsibility and happy path, then fallback behaviour, rather than introducing a separate agent for every page.

# Working model

A screen presents work. An agent performs a business task. A workflow coordinates steps, records and authority. Share agent capabilities while isolating each request's context, run and history. A per-order workspace does not imply a separately coded or deployed agent per order.

| Screen | Proposed agent involvement |
|---|---|
| Home | Routing assistant and summaries from active workflows |
| Work | Shared decision queue and handoffs from all agents |
| Orders | Sales, Procurement or Fulfilment according to the workflow |
| Money | Finance workflows for payment and reconciliation |
| Network | Relevant agents use customer, supplier, product and location records |
| Intelligence | Analytics assistance using permitted data |
| Settings | Structured administration; no dedicated agent required initially |

This mapping is a proposal. Only the first agent should be developed before adding specialised agents. The first-agent recommendation is Procurement; user selection remains pending.

# Shared services

Permissions, deterministic policies, business records, workflow state, tools, evidence, audit history and Work item delivery. Shared services do not imply unrestricted access to all company data.

# Contract to define for each agent

Business outcome; required inputs; permitted reads and actions; structured outputs; evidence; happy-path steps; review boundary; completion; fallback states; handoffs; affected screens. Model recommendation, human approval and confirmed execution are distinct events.

See [workflow method](/agents/workflow-method.md), [platform ownership](/architecture/platform-ownership.md), and [Procurement brief](/next-steps/procurement-agent.md).
