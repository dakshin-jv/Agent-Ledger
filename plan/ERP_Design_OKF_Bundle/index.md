---
okf_version: "0.2"
---

# ERP Design — Single Current OKF Bundle

Content revision **0.5.0** · Updated **7 October 2026** · Step 4 structure discussed · Goods-intake datasets and setup specified for review. Design only. No implementation is evidenced.

- [Start here](start-here.md) — Reading order, scope and update authority.
- [Progress](progress/tracker.md) — Current checkpoint and pending work.
- [History](log.md) — Dated changes.

# Product foundation

- [Product intent and design boundaries](foundation/product-intent.md) — User goals and the agreed pace for designing an agent-native commerce ERP.
- [Traditional ERP experience baseline](foundation/traditional-erp.md) — The modules, screen types and daily workflow used as the redesign baseline.
- [Traditional-to-agentic transformation map](foundation/transformation-map.md) — The four interaction classifications and initial mappings discussed before screen design.

# UI design

- [Agent visibility and human authority](design/agent-visibility.md) — Contextual agents, activity transparency and approval boundaries discussed for the ERP.
- [Home attention, pulse and active operations](design/attention-and-operations.md) — Decision-oriented attention items, role-aware business context and operational drill-down.
- [Commands and guided creation](design/command-interactions.md) — Four command intents, risk-aware outcomes and the structured alternative to language input.
- [Step 3 — Home interaction model](design/home.md) — The five Home zones and the intended first-screen feel from the discussion.
- [Six primary workspaces](design/navigation.md) — The current six-tab navigation proposal and how traditional modules map into it.
- [Workspace outlines beyond Home](design/workspace-outlines.md) — The limited sketches for Work, Orders, Money, Network and Intelligence without prematurely finalising them.

# Agent development

- [Shared business agents across screens](agents/shared-agent-model.md) — Business responsibilities, per-record runs and proposed screen-to-agent mapping.
- [Happy path first, then agent fallbacks](agents/workflow-method.md) — The agreed development sequence and reusable handling of external uncertainty.

# Service and data architecture

- [Business data, knowledge and model APIs](architecture/data-and-models.md) — Transactional storage versus discovery, retrieval and timeline presentation.
- [Astropods agents and Render orchestration](architecture/platform-ownership.md) — The proposed platform split and the backend controls required around it.
- [Priority services and meaningful product use](architecture/service-priorities.md) — The five explicit sponsor priorities and their planned business contributions.

# Progress and decisions

- [Requirements, working directions and unresolved choices](progress/decisions.md) — A decision register that distinguishes user instructions from proposals.
- [Unresolved design questions](progress/open-questions.md) — Material choices that future work must resolve instead of silently assuming.
- [ERP design progress](progress/tracker.md) — What is documented, what remains unvalidated and the next screen to design.
- [How to update the bundle](progress/update-playbook.md) — A maintenance workflow that preserves design authority, uncertainty and progress.

# Next steps

- [Future design step template](next-steps/design-step-template.md) — Reusable slots for future screen discussions, decisions, progress and validation.
- [First agent candidate — Procurement](next-steps/procurement-agent.md) — The proposed first happy path, service mapping and fallback slots awaiting detailed design.
- [Step 4 — Work / Attention Queue](next-steps/step-04-work.md) — An intentionally unfinished brief for the next screen, anchored in what was already discussed.

# Sources and format

- [ERP design discussion record](references/discussion-record.md) — A compact provenance record of the supplied conversation and the authority of its statements.
- [Google Open Knowledge Format v0.2](references/okf-format.md) — The official format source and the structural conventions used in this bundle.
- [Relationship to the earlier AgentLedger architecture](references/related-architecture.md) — Historical architecture context and explicit boundaries between old implementation recommendations and new ERP UX.
- [Session 2 — agent development and service priorities](references/session-02-agent-development.md) — The user directions and working architecture discussed after the initial bundle.


- [PayPal Sandbox and AI Toolkit](architecture/paypal-sandbox-toolkit.md) — Required payment integration and development tooling.

# Goods-intake datasets and setup

- [Demo dataset contracts](architecture/demo-dataset-design.md)
- [Service setup and human recovery gates](architecture/service-setup-design.md)
- [PayPal Sandbox datasets and setup](architecture/paypal-sandbox-dataset-setup.md)

- [Goods Specification Agent and owner notifications](agents/goods-specification-agent.md) — Happy path, structured output, fallbacks and recovery.

- [Scheduled owner notifications and RBAC](architecture/scheduled-owner-notifications.md) — Render service fit, backend schedule records and permission controls.
