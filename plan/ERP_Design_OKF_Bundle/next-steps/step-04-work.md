---
type: Design Brief
title: Step 4 — Work / Attention Queue
description: An intentionally unfinished brief for the next screen, anchored in what
  was already discussed.
tags:
- erp
- design
- next-steps
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
design_progress: next-not-started
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Status and scope

Initial queue and detail structure discussed; detailed scenario design pending. Continue it alongside the first agent happy path, before expanding other workflows.

# Existing direction

Work consolidates tasks, notifications requiring action, approvals, exceptions, investigations and agent handoffs. It is the user's operational inbox. Home previews attention; Work provides the full queue.

Previously proposed views: **Needs me / Agents working / Waiting / Completed**. These are seed labels, not final status definitions or a backend enum.

# Examples to choose from

- Order #4821 may miss delivery: review the fulfilment agent's explanation.
- ₹8.4L supplier payment requires approval: review finance context.
- Inventory discrepancy detected: investigate underlying evidence.

All examples are fictional. Choose one with the user as the first detailed journey.

# Design session sequence

1. Confirm first role and first scenario.
2. Decide queue organisation, filtering, ownership and priority.
3. Design the compact work item and the detail view.
4. Define evidence, recommendation, alternatives and missing data.
5. Define the user action, agent continuation and authoritative result.
6. Add waiting, failure, retry, empty and completed states.
7. Check return-to-Home and linked-record navigation.
8. Review with the user, update decisions and progress.

This sequence is a proposed facilitation plan, not an approved UI design.

# Room to fill in next

| Design slot | Current content |
|---|---|
| Role and scenario | Pending user answer |
| Above-the-fold layout | Pending |
| Queue item contents | Pending |
| Priority rules | Pending |
| Detail / decision brief | Pending |
| Primary and secondary actions | Pending |
| Approval / execution feedback | Pending |
| Agent handoff / continuation | Pending |
| Status and ownership | Pending |
| Loading / empty / error states | Pending |
| Granular record access | Pending |
| Validation findings | Pending |

# Completion gate

Finish a coherent interaction journey, specify where structured ERP control remains, resolve materially uncertain choices, and record the user's decisions before treating Work as a completed design. An implementation milestone requires separate build and verification evidence.

# Session 2 interaction additions

Views are proposed by who acts next: Needs me (current user decision), Agents working (active execution), Waiting (another person or external event), Completed (confirmed outcome). Business-item status and agent-run status are separate.

Compact item fields: business issue; impact; next decision; responsible party; deadline; Review options. Example shortage: 188 missing units for Order #4821, decision needed before dispatch. Values are illustrative.

Detail sequence: what happened → supporting evidence/missing data → available options/consequences → required decision → continuation and expected outcome. Link granular records from here. Persona, layout, action semantics and exact statuses remain open.

Develop in conjunction with [Procurement candidate](/next-steps/procurement-agent.md), [shared agents](/agents/shared-agent-model.md) and [workflow method](/agents/workflow-method.md).

# Bryntum-centred Agent Board plan

## Intent

Evolve Work into an **Agent Board**: one operational workspace that lets a
person see what needs a decision, what autonomous agents are doing, when people
and agents are available, and how a case is progressing against its commitments.
It is not a generic to-do list. A simple task list would hide the difference
between a human decision, an agent execution, a planned commitment and an
external wait.

The proposed navigation label remains **Work**. The workspace title is **Agent
Board**, with four purpose-specific views:

| View | Bryntum component | User question it answers |
|---|---|---|
| Attention | AG Grid initially; linked board card where useful | What needs my decision or intervention now? |
| Board | TaskBoard | What is each agent or workstream doing next? |
| Schedule | Scheduler | Who or which agent has capacity, and when is work expected? |
| Plan | Gantt | What are the milestones, dependencies, dates and critical path for this case? |

Gantt is for a dependency-aware case plan, TaskBoard is for work flow, and
Scheduler is for time and capacity. Do not force all three questions into one
component or duplicate their data as independent sources of truth.

## Naming discussion to resolve first

Use the following terms consistently in the UI, API and audit trail. They are
proposals for review, not adopted domain enums.

| Concept | Proposed name | Meaning | Must not be confused with |
|---|---|---|---|
| The workspace | Agent Board | The cross-agent operational view for a person or team | A separate autonomous agent product |
| A user-facing unit of work | Work item | A decision, exception, handoff, investigation or follow-up | An agent process or a calendar event |
| A workflow lane | Workstream | A related set of work items for one case or outcome | A permission boundary |
| A card on the flow board | Board card | The TaskBoard representation of a work item | The authoritative record |
| An executing capability | Agent run | One isolated invocation with inputs, outputs, state and audit evidence | The business status of its work item |
| A scheduled commitment | Schedule block | A Scheduler event assigned to one or more human/agent resources | A confirmation that work was completed |
| A dependency-aware planned step | Plan task | A Gantt task with dates, dependencies and progress | Every small checklist item |
| A date with no invented duration | Milestone | A due, approval or delivery point | A scheduled activity |
| Transfer of responsibility | Handoff | Ownership moves between a person, team or agent | Reassignment of approval authority |
| Human authority | Decision | An approval, rejection, request for change or escalation | An automated recommendation |

Recommended user-facing language for the current seed views is **Needs my
decision**, **Agent work in progress**, **Waiting**, and **Completed**. These
describe the next actor; they are not a replacement for the business lifecycle
or agent-run lifecycle.

Naming choices to decide in the first design review:

1. Confirm **Agent Board** as the workspace title, or choose an alternative
   such as *Operations Board* or *Work Orchestration*.
2. Confirm whether users see *work item* or the friendlier *action* in compact
   UI copy. Keep `work_item` as the technical term unless the data contract is
   deliberately changed.
3. Decide whether an agent is shown by capability name (for example,
   *Procurement Agent*) or by the active `agent run` name in day-to-day views.
4. Define labels for terminal-but-not-successful outcomes: *cancelled*,
   *failed*, *blocked* and *superseded* must not be collapsed into *completed*.

## Agent Board information model

One backend work record feeds the views below. Bryntum components are
interactive projections; they do not become the system of record or grant
authority.

```text
Case / business record
  └─ Workstream
       ├─ Work item ── owner, next actor, priority, evidence, decision state
       │    ├─ Agent run(s) ── isolated execution state, inputs, outputs, audit
       │    ├─ Schedule block(s) ── resources, start/end, availability context
       │    └─ Plan task(s) ── duration, dependency, milestone, progress
       └─ Handoffs / notifications / recovery records
```

Required separations:

- A work item may be waiting while its last agent run has succeeded.
- An agent run may be active while the work item is not actionable by the
  current user.
- A schedule block expresses an intended reservation, not approval or
  completion.
- A Gantt dependency expresses planning logic, not permission for an agent to
  execute the next step.
- A drag, resize or status change creates a versioned proposal. Backend RBAC,
  ownership, case state and audit checks decide whether it is persisted.

## View designs and native Bryntum capabilities

### 1. Attention and Board — TaskBoard

Use TaskBoard for the agent-facing flow board. Initial columns can be
**Ready**, **In progress**, **Waiting**, **Needs decision**, and **Done**, while
the Attention list keeps the current-user subset prominent. Columns are a view
of work-item flow, not agent-run states.

- Group cards by `workstream`, `case`, or responsible capability using
  TaskBoard swimlanes after the grouping is chosen.
- Show only concise operational facts on each card: next action, owner/agent,
  due signal, impact, evidence state and linked case.
- Open a detail panel for evidence, alternatives, authority, audit history and
  recovery rather than putting hidden reasoning on the card.
- Use native column filtering/filter bar before inventing a custom task filter.
- If per-column WIP limits are desired, enforce them with an explicit backend
  policy and TaskBoard `beforeTaskDrop`; Bryntum does not provide a built-in
  WIP-limit configuration.

### 2. Agent capacity — Scheduler

Use Scheduler only where dates and finite capacity are meaningful: owner review
slots, procurement follow-ups, delivery/inspection windows and bounded agent
execution reservations. Resources can represent people, teams and named agent
capabilities, but they must carry a clearly labelled resource type.

- Display a current-time line, configured working/non-working periods and
  relevant time zones.
- Keep all deadlines in UTC in the backend and display them in the selected
  user time zone.
- Let rescheduling propose changed schedule blocks; do not silently change the
  case commitment or approval deadline.
- Do not fabricate an agent's availability merely because an agent can execute
  asynchronously. Capacity estimates need an evidenced rule.

### 3. Case plan — Gantt

Use Gantt for a selected case or workstream when it has genuine duration,
dependencies or milestones. It should expose the path from intake through
specification, sourcing, owner decision and follow-up, without asserting dates
that have not been accepted.

- Model approval and delivery dates as milestones unless there is a supported
  duration.
- Use finish-to-start dependencies only where the next task truly cannot begin
  earlier. Do not use a dependency merely to make the chart look sequential.
- Enable the built-in dependency, task edit, task tooltip, critical path,
  baseline, progress-line and undo/redo capabilities only after their business
  semantics are agreed.
- Preserve a baseline when a plan is approved; a current plan edit must remain
  traceable and must not overwrite the approved baseline.
- Schedule changes are proposals requiring backend validation, a correlation
  key, audit event and recovery path.

## Delivery plan

| Stage | Outcome | Decisions / work | Exit evidence |
|---|---|---|---|
| 0. Naming workshop | Shared vocabulary | Resolve the four naming choices above and choose the first persona/case | Recorded terms, disallowed synonyms and owner |
| 1. Domain contract | Stable shared model | Define work-item, agent-run, schedule-block, plan-task, milestone and handoff identifiers; ownership, versions, correlation keys and audit events | API/data-contract review and fixture examples |
| 2. Attention baseline | Actionable human queue | Implement the existing Needs-me list and detail; link to the case and evidence | Role/tenant checks and empty/error/failed states tested |
| 3. TaskBoard | Flow view of the same work | Map work-item flow to columns, choose swimlane policy, support authorised card movement | Card move becomes an audited backend proposal and refreshes all views |
| 4. Scheduler | Capacity/timing view | Define resource types, calendars, time zone display and reschedule policy | Accepted schedule mutation remains consistent with Work and Plan |
| 5. Gantt | Dependency-aware case plan | Define approved tasks/milestones/dependencies, baseline and critical-path rules | Backend-validated dependency/date edits and recovery behaviour tested |
| 6. Cross-view operation | One coherent board | Deep links, filters, live refresh strategy, access rules and conflict handling | A single procurement case can be followed across all four views |
| 7. Demo hardening | Honest demo | Seed labelled data, permission/error/loading states, undo boundaries and accessibility review | Repeatable scenario with no unverified automatic authority |

## First vertical slice

Start with the goods-procurement specification journey already being designed:

1. A requester submits a goods specification.
2. The Specification Agent creates an evidence-backed draft and an `agent run`.
3. The resulting `work item` appears in **Needs my decision** for the assigned
   business owner.
4. A Board card shows the owner-review flow; a Schedule block shows the review
   target only if a real due policy exists.
5. The Gantt plan shows specification review as a milestone or a bounded task,
   then a true dependency into sourcing after approval.
6. The owner's decision is recorded by the backend. The agent may continue
   only under its existing authorised workflow contract.

This slice demonstrates why all three Bryntum views exist while retaining a
single controlled business workflow.

## Open questions before implementation

- Which role owns the first Agent Board: procurement owner, operations manager
  or founder?
- What is the first case type: specification approval, sourcing exception or
  delivery risk?
- Which agent capabilities deserve a Scheduler resource, and what evidence
  supports their capacity estimate?
- Which plan edits may be proposed by an agent, and which require human
  approval before scheduling changes take effect?
- What event source will refresh concurrent board/schedule/plan views without
  losing a user's in-progress edit?
- Which Bryntum products are covered by the selected evaluation or production
  entitlement, and how will the demo remain compliant after it expires?

No frontend framework, component package, schedule data or automation has been
selected or implemented by this plan. Confirm the naming workshop and first
vertical slice before scaffold or licence-dependent package work begins.
