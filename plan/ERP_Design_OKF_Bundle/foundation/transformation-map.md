---
type: Design Method
title: Traditional-to-agentic transformation map
description: The four interaction classifications and initial mappings discussed before
  screen design.
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

# Method

For each traditional action, document the current steps and classify the new interaction before drawing the page.

| Classification | Meaning |
|---|---|
| Keep normal UI | Precise browsing or control remains useful |
| UI + agent assistance | Keep structured interaction, reduce manual work |
| Agent first + human review | Agent prepares a result; user checks and commits |
| Automatic within granted authority | Agent executes under an explicitly defined policy |

These are design categories. Specific actions and authority thresholds still need validation.

# Initial mappings discussed

| Action | Traditional experience | Proposed experience | Current classification |
|---|---|---|---|
| Create sales order | Navigate to New Order and fill fields | Express intent → agent drafts → user confirms | Agent first + review |
| Check inventory | Stock screen and filters | Ask whether an order can be fulfilled across locations | Agent-assisted read; keep stock view |
| Create PO | Procurement form | Detect shortage and propose a PO | Agent first + review |
| Approve PO | Approval inbox | Decision brief, evidence, risk and recommendation | UI + agent assistance |
| Find report | Locate report and set filters | Ask business question → answer, evidence and chart | Agent first; keep repeatable reports |
| Track order issue | Open multiple modules | Order workspace with context and agent timeline | UI + agent assistance |
| Reconcile payment | Manual finance matching | Match candidates and surface exceptions | Automatic matching proposed; posting authority open |

# Retain / compress / replace

Retain structured records, lists, precise fields, audit history and specialist controls. Compress navigation and repetitive form completion. Replace fragmented alerts with contextual decisions. Automate only the work supported by granted authority.

# To extend this map

Use [the future-step template](/next-steps/design-step-template.md). For each action add: user role, trigger, input, record affected, agent assistance, review boundary, resulting state and failure recovery. These fields are a proposed documentation template, not a completed workflow specification.
