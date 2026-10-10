---
type: Reference
title: Relationship to the earlier AgentLedger architecture
description: Historical architecture context and explicit boundaries between old implementation
  recommendations and new ERP UX.
tags:
- erp
- design
- references
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: architecture
  resource: 'ChatGPT file: AgentLedger Technical Architecture Specification; library_file_id=libfile_d4ec3c8b78608191985ecdc45348342b'
  title: AgentLedger Technical Architecture Specification
- id: discussion
  resource: /references/discussion-record.md
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Existing artifact

The existing document is **AgentLedger Technical Architecture Specification**, created 6 October 2026. Its opening sections were read for scope comparison during this task. Source identity is recorded in frontmatter; the original file is not changed by this bundle.[^architecture]

# Important scope difference

The earlier brief framed a procurement-focused control plane and hackathon MVP: discovery, verification, recommendation, approval, sandbox payment, memory and audit. It explicitly limited the MVP rather than promising a full ERP replacement.[^architecture]

The latest discussion sets a broader product ambition: redesign an ERP experience step by step. These can coexist only if long-term product scope and first-release scope are clearly separated. The first-release boundary remains an open decision.

# Precedence for UX continuation

Use this bundle's current six-workspace direction and Home concept for continued ERP UX design. Do not reintroduce an older top-level menu without discussing the conflict. Do not infer that prior recommended libraries or sponsor integrations have been chosen or implemented for the new design.

# Historical project link

[PayPal AI Hackathon](https://paypalaihackathon.devpost.com/) is the project context from prior discussion. This task did not reverify rules, deadlines or sponsor requirements; those facts are intentionally not repeated as current requirements.

[^architecture]: AgentLedger Technical Architecture Specification; introductory product and scope sections read on 7 October 2026.
