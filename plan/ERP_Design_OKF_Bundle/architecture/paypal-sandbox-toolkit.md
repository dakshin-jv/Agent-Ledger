---
type: Integration Requirement
title: PayPal Sandbox and AI Toolkit
description: Required PayPal integration, development tooling and hackathon submission
  checkpoint.
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:48:53+00:00'
sources:
- id: user
  resource: 'User instruction in this conversation on 7 October 2026: make sure to
    use PayPal sandbox and PayPal toolkit'
- id: hackathon
  resource: https://paypalaihackathon.devpost.com/
- id: toolkit
  resource: https://github.com/paypal/AI-Toolkit
bundle_revision: 0.5.0
implementation_status: not-evidenced
---

# Required for our project

The user explicitly requires PayPal Sandbox and PayPal AI Toolkit. Both are required project choices; Toolkit is not being asserted as compulsory for every hackathon entrant.

# Official checkpoint

The hackathon requires meaningful PayPal plus AI integration using the free sandbox environment, a working prototype, documentation, public licensed source, and a public YouTube demo under three minutes. A hosted build or complete run instructions must let judges use it. Partner tools are optional under the event requirements, while our five priorities remain explicit project choices.[^hackathon]

# Toolkit role

PayPal AI Toolkit supports coding agents with API guidance, skills, hooks and sandbox MCP operations. It is not our ERP agent orchestration engine.[^toolkit]

# Planned implementation

- Configure sandbox buyer and merchant accounts and credentials.
- Install and use the PayPal AI Toolkit in the selected coding-agent environment; record its actual contribution.
- Retain APIMatic as a priority for complementary API context.
- Implement a supported sandbox payment journey, with policy and approval before execution.
- Save provider IDs and confirmed outcomes; distinguish pending, failed and unknown states.
- Prevent duplicate execution and verify uncertain outcomes before retry.
- Show sandbox status clearly in the UI and demo.
- Keep secrets server-side.

These are planned controls, not completed integrations. Confirm the merchant/payment model before coding. Channel3 discovery does not authorise payment to arbitrary discovered retailers. See [Procurement](/next-steps/procurement-agent.md).

# Pending evidence

Toolkit installation/use; sandbox configuration; end-to-end transaction; authoritative outcome update; duplicate protection; approved happy path; payment fallbacks. Next remains the first-agent happy-path specification.

[^hackathon]: Official hackathon overview checked 7 October 2026.
[^toolkit]: Official PayPal AI Toolkit repository checked 7 October 2026.
