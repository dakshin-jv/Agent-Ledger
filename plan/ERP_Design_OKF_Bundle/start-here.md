---
type: Playbook
title: How to use this ERP design bundle
description: Reading order, scope, decision authority and instructions for continuing
  the design.
tags:
- erp
- design
- start-here.md
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
- id: okf
  resource: /references/okf-format.md
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Purpose

Capture the ERP experience discussed with Jaya, preserve the current design direction, and continue one screen at a time. The goal is a commerce-focused, agent-native ERP with a better user experience than the existing systems the user wants to replace.

This is a design knowledge bundle, not an implemented ERP, database schema or finished technical specification. Product name is unresolved; AgentLedger is a historical working name.

# Start here

1. Read [product intent](/foundation/product-intent.md) and [traditional ERP baseline](/foundation/traditional-erp.md).
2. Read [transformation approach](/foundation/transformation-map.md), then [navigation](/design/navigation.md).
3. Read [Home](/design/home.md), [commands](/design/command-interactions.md), and [agent visibility](/design/agent-visibility.md).
4. Check [progress](/progress/tracker.md) and [decisions](/progress/decisions.md).
5. Continue with [first-agent Procurement brief](/next-steps/procurement-agent.md) and [Step 4: Work](/next-steps/step-04-work.md); the first workflow/persona still needs confirmation.

# Reading and authority

- Explicit user requirements are recorded as requirements.
- Assistant proposals that the user chose to continue exploring are a working direction, not proof that every granular choice was approved.
- Mock amounts, counts, dates, company names and agent actions are examples, never real business data.
- `status: draft` is the OKF document lifecycle. `design_progress` is this bundle's custom planning field. Neither means software has been built.
- No human verification event is asserted for this newly generated bundle.
- A later explicit user decision takes priority; update affected concepts and [log](/log.md) rather than leaving conflicting versions as equally current.

# Continue without losing context

Use [the update playbook](/progress/update-playbook.md) after each discussion. Keep unresolved decisions visible. If a material decision is below the user's requested 95% confidence threshold, ask rather than choose silently; documentation can proceed with the uncertainty clearly marked.

# Format

The bundle targets [Google's OKF v0.2 reference](/references/okf-format.md). Unzip and begin with `index.md`; any agent that reads Markdown can follow the links. An OKF-aware consumer interprets paths beginning with `/` relative to this bundle.

# Updated reading path

Read [shared agents](/agents/shared-agent-model.md), [happy path and fallbacks](/agents/workflow-method.md), [platform ownership](/architecture/platform-ownership.md), [priority services](/architecture/service-priorities.md), and [data/models](/architecture/data-and-models.md) before defining the first agent.

Maintain this single bundle identity. Revise the current archive rather than creating separately named bundles for each session. Format version remains 0.2; content revision is now 0.2.0.

# Current goods-intake design checkpoint — revision 0.4.0

User selected goods only (supersedes the earlier both-goods-and-services discussion). Services deferred for lack of data. Demo-labelled internal datasets and PayPal Sandbox selected. Sarvam and TypeSafe both required. Human approval and recovery required at every step. Design only: do not build, seed, configure or call services in this delivery.

- [Dataset design](/architecture/demo-dataset-design.md)
- [Service setup, human approval and recovery](/architecture/service-setup-design.md)
- [PayPal datasets and setup](/architecture/paypal-sandbox-dataset-setup.md)

Goods-intake schema, forward/recovery transitions and scenario definitions are documented as proposals, not implemented or tested. No stock/contracts/policy datasets or API credentials have been supplied or verified. Next: review fixture configuration (country, currency, goods category, users and illustrative rules), then detailed specification-stage design. Future Codex implementation must update progress with evidence and preserve this single bundle.
