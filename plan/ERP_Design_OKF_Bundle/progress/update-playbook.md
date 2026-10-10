---
type: Playbook
title: How to update the bundle
description: A maintenance workflow that preserves design authority, uncertainty and
  progress.
tags:
- erp
- design
- progress
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: maintenance-ready
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Trigger

A new discussion, explicit user decision, changed requirement, prototype review or implementation result.

# Update procedure

1. Read the affected concept and current progress before changing it.
2. Identify whether the new input is an explicit user requirement, a working direction or a proposal.
3. Ask about material uncertainty rather than choosing silently, following the user's requested confidence rule.
4. Update the concept; retain accurate source attribution and its meaningful-change time.
5. Update decisions, open questions and tracker independently. A designed screen is not automatically a built screen.
6. Append a dated update to `log.md`, newest date first. Update applicable index descriptions and cross-links.
7. Check frontmatter parsing, non-empty type, reserved-file structure and local links before repackaging.

# Fields to preserve

Keep OKF metadata, source paths and unknown producer fields when round-tripping. `design_progress`, `bundle_revision` and `implementation_status` are local extensions; they do not replace OKF lifecycle or verification fields.

# Version policy for this project

Current bundle revision is 0.2.0; format version is 0.2. They are different numbers. Increment the bundle revision for meaningful content updates. Record new decisions without rewriting historical user instructions as if they were never given.

# Review and verification

Do not fabricate human sign-off or usability results. If a reviewer confirms a document against its sources, a verification event can be recorded with the actual reviewer and time. A structural validation does not prove the product design is correct.

Maintain one current bundle and replace its existing saved archive after updates; preserve its history rather than creating per-session duplicate bundles.
