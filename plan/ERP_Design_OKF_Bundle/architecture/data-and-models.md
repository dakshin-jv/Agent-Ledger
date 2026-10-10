---
type: Data Architecture
title: Business data, knowledge and model APIs
description: Transactional storage versus discovery, retrieval and timeline presentation.
tags:
- erp
- agents
- architecture
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T16:14:35+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
- id: sarvam
  resource: https://docs.sarvam.ai/api-reference/authentication
- id: typesafe
  resource: https://api.typesafe.ai/docs
- id: elastic
  resource: https://paypalaihackathon.devpost.com/details/elastic
- id: secrets
  resource: https://docs.astropods.com/secrets
design_progress: proposed
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Proposed boundaries

| Layer | Service / choice | Role and constraint |
|---|---|---|
| External discovery | Channel3 | Product/retailer offers; external availability is not our warehouse stock |
| Searchable knowledge | Elastic | Policies, supplier documents, decisions and outcomes; retrieved facts may be stale |
| Transaction records | PostgreSQL proposed | Orders, stock, invoices, approvals, payments and workflow state; provider not selected |
| Operational visuals | Bryntum and AG Grid | Timeline/comparison UI fed by backend data; not the authoritative database |

Recheck current approvals, balances and payment states in authoritative records before committing. Store source references/times for external offers. Elasticsearch is planned as a retrieval layer, not an implicit replacement for ERP transactional consistency.

# Model API plan

The user has Sarvam and TypeSafe keys; no credentials were provided, used or tested. Sarvam is proposed for request interpretation/explanations and possible voice. TypeSafe/Jev is proposed for bounded classification or typed evaluation. Deterministic policy still governs permissions and money.

Server-side calls from Astropods agent code or Render tasks are a feasible integration approach. Native model-provider registration is not confirmed. Sarvam chat compatibility does not guarantee every agent framework supports every Sarvam feature; test the chosen client and model.

# Credentials

Use runtime secrets where calls execute: `SARVAM_API_KEY`, `TYPESAFE_API_KEY`, and needed service credentials. Keep keys out of browser bundles, prompts, shared examples and logs. Configure separately for Astropods and Render if both call a provider.

# Pending checks

One Sarvam request; one Jev evaluation; Astropods outbound calls; Render-to-agent authentication; result validation; rate limits; retry behaviour; selected SQL provider; knowledge freshness and tenant permissions. Model outputs alone do not grant approval.

# Database

Render PostgreSQL is the store. One backend owns persistent storage; agents and workflows use its APIs.
