---
type: Interaction Pattern
title: Agent visibility and human authority
description: Contextual agents, activity transparency and approval boundaries discussed
  for the ERP.
tags:
- erp
- design
- design
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
design_progress: concept-discussed
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Embedded agents

Agents appear inside the work users are doing: an order workspace, supplier record, payment or global command. A separate Agents destination is unresolved, not required for everyday task completion.

# Activity stream

Show proposed, ongoing and completed work with honest labels. Examples from the discussion: inventory variance detected; payment matched to invoice; updated supplier pricing requested; inventory reallocated for three orders. These are fictional activity examples.

Each event can expose: why it happened; data used; action taken; evidence quality or confidence where meaningful; result; undo or escalation where supported. Undo is conditional, never promised for an irreversible payment or external communication.

# Human authority

The agent prepares information and performs permitted work. The user retains required approval authority. Exact role permissions, automatic-action limits and financial approval policy are pending.

Do not present a recommendation as an executed action. Do not show money moved until execution has been confirmed. Display observable steps and concise decision explanations, not hidden model reasoning.

# Decisions still needed

Which tasks can run automatically? Who can approve which commitments? What constitutes a failed, stalled, cancelled or partially completed run? How does the user pause, override or recover? Which data and decisions enter the audit record? These are future detailed design items.
