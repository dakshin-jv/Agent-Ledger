---
type: Reference
title: Google Open Knowledge Format v0.2
description: The official format source and the structural conventions used in this
  bundle.
tags:
- erp
- design
- references
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: google-okf
  resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
  title: Open Knowledge Format v0.2
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Format source

Use [GoogleCloudPlatform / knowledge-catalog: OKF SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), version 0.2, checked on 7 October 2026.[^google-okf]

# Bundle profile

An OKF bundle is a directory of Markdown concepts. Each concept here has parseable YAML frontmatter and a non-empty `type`. `index.md` and `log.md` are reserved. Root `index.md` declares `okf_version: "0.2"`; subordinate indexes have no frontmatter. Logs use dated entries, newest first.[^google-okf]

Concepts carry descriptive fields, source provenance, generated metadata and lifecycle status. Internal links beginning with `/` resolve from the bundle root. Producer-defined keys capture design progress. No runtime, database or viewer is required.[^google-okf]

No `verified` human event is claimed. All concept lifecycles are draft pending review. The format allows arbitrary descriptive concept types, so Screen Design, Decision Register and Progress Tracker are appropriate producer choices.[^google-okf]

[^google-okf]: Official OKF v0.2 specification.
