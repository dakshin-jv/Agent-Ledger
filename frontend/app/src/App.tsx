import { useRef, useState } from 'react'
import { BryntumGantt, BryntumGanttProjectModel } from '@bryntum/gantt-react'
import { BryntumGrid } from '@bryntum/grid-react'
import { BryntumScheduler } from '@bryntum/scheduler-react'
import { BryntumTaskBoard } from '@bryntum/taskboard-react'

type View = 'attention' | 'board' | 'schedule' | 'plan'

const views: Array<{ id: View; label: string; description: string }> = [
  { id: 'attention', label: 'Attention', description: 'Decisions and exceptions needing a person' },
  { id: 'board', label: 'Board', description: 'Agent work moving through its operational flow' },
  { id: 'schedule', label: 'Schedule', description: 'Review windows and agent-capacity commitments' },
  { id: 'plan', label: 'Plan', description: 'Dependencies and milestones for the selected case' },
]

function App() {
  const [activeView, setActiveView] = useState<View>('attention')
  const [gridProps] = useState(() => ({
    data: [
      { id: 1, workItem: 'Approve goods specification', case: 'REQ-4821', nextActor: 'Priya Shah', status: 'Needs decision', due: 'Today', impact: 'Dispatch risk' },
      { id: 2, workItem: 'Validate alternative supplier', case: 'REQ-4821', nextActor: 'Procurement Agent', status: 'In progress', due: 'Today', impact: 'Cost review' },
      { id: 3, workItem: 'Confirm warehouse inspection', case: 'REC-203', nextActor: 'Receiving team', status: 'Waiting', due: '14 Oct', impact: 'Quality hold' },
    ],
    columns: [
      { text: 'Work item', field: 'workItem', flex: 2, editor: { type: 'textfield', required: true } },
      { text: 'Case', field: 'case', width: 110 },
      { text: 'Next actor', field: 'nextActor', flex: 1 },
      { text: 'Status', field: 'status', width: 150 },
      { text: 'Due', field: 'due', width: 90 },
      { text: 'Impact', field: 'impact', flex: 1 },
    ],
  }))
  const [boardProps] = useState(() => ({
    columns: [
      { id: 'ready', text: 'Ready' },
      { id: 'progress', text: 'In progress' },
      { id: 'waiting', text: 'Waiting' },
      { id: 'decision', text: 'Needs decision' },
      { id: 'done', text: 'Done' },
    ],
    columnField: 'flowState',
    swimlaneField: 'workstream',
    tasks: [
      { id: 11, name: 'Validate supplier evidence', flowState: 'progress', workstream: 'Procurement' },
      { id: 12, name: 'Approve goods specification', flowState: 'decision', workstream: 'Procurement' },
      { id: 13, name: 'Book inspection window', flowState: 'ready', workstream: 'Receiving' },
      { id: 14, name: 'Collect carrier update', flowState: 'waiting', workstream: 'Receiving' },
      { id: 15, name: 'Draft owner briefing', flowState: 'done', workstream: 'Procurement' },
    ],
  }))
  const [schedulerProps] = useState(() => ({
    startDate: '2026-10-12',
    endDate: '2026-10-17',
    viewPreset: 'dayAndWeek',
    barMargin: 8,
    columns: [{ text: 'Assigned to', field: 'name', width: 180 }],
    resources: [
      { id: 'owner', name: 'Business owner' },
      { id: 'procurement', name: 'Procurement Agent' },
      { id: 'receiving', name: 'Receiving team' },
    ],
    events: [
      { id: 21, resourceId: 'owner', name: 'Specification review', startDate: '2026-10-13T09:30', duration: 90, durationUnit: 'minute' },
      { id: 22, resourceId: 'procurement', name: 'Supplier evidence check', startDate: '2026-10-13T11:00', duration: 2, durationUnit: 'hour' },
      { id: 23, resourceId: 'receiving', name: 'Inspection window', startDate: '2026-10-15T10:00', duration: 3, durationUnit: 'hour' },
    ],
  }))
  const [ganttProjectProps] = useState(() => ({
    startDate: '2026-10-12',
    autoSetConstraints: true,
    tasks: [
      {
        id: 100,
        name: 'REQ-4821 — Goods procurement',
        expanded: true,
        children: [
          { id: 101, name: 'Prepare specification evidence', startDate: '2026-10-12', duration: 1 },
          { id: 102, name: 'Business-owner review', duration: 1 },
          { id: 103, name: 'Start sourcing', duration: 2 },
          { id: 104, name: 'Supplier shortlist due', duration: 0 },
        ],
      },
    ],
    dependencies: [
      { from: 101, to: 102 },
      { from: 102, to: 103 },
      { from: 103, to: 104 },
    ],
  }))
  const ganttProject = useRef(null)
  const currentView = views.find((view) => view.id === activeView)!

  return (
    <main className="agent-board">
      <header className="app-header">
        <div>
          <p className="eyebrow">AgentLedger / Work</p>
          <h1>Agent Board</h1>
          <p className="subtitle">One operational view for decisions, agent runs, capacity, and case plans.</p>
        </div>
        <span className="environment">Demo data · trial components</span>
      </header>

      <nav aria-label="Agent Board views" className="view-tabs">
        {views.map((view) => (
          <button
            aria-current={activeView === view.id ? 'page' : undefined}
            className={activeView === view.id ? 'active' : undefined}
            key={view.id}
            onClick={() => setActiveView(view.id)}
            type="button"
          >
            {view.label}
          </button>
        ))}
      </nav>

      <section aria-labelledby="view-title" className="workspace">
        <div className="workspace-heading">
          <div>
            <h2 id="view-title">{currentView.label}</h2>
            <p>{currentView.description}</p>
          </div>
          <span className="scope">REQ-4821</span>
        </div>

        <div className="bryntum-host">
          {activeView === 'attention' && (
            <BryntumGrid {...gridProps} cellEditFeature filterBarFeature height="100%" stripeFeature />
          )}
          {activeView === 'board' && (
            <BryntumTaskBoard {...boardProps} autoGenerateSwimlanes height="100%" />
          )}
          {activeView === 'schedule' && (
            <BryntumScheduler
              {...schedulerProps}
              eventEditFeature
              eventTooltipFeature
              height="100%"
              timeRangesFeature={{ showCurrentTimeLine: true }}
            />
          )}
          {activeView === 'plan' && (
            <>
              <BryntumGanttProjectModel ref={ganttProject} {...ganttProjectProps} />
              <BryntumGantt
                barMargin={8}
                columns={[{ text: 'Plan task', field: 'name', flex: 1, type: 'name' }]}
                criticalPathsFeature={{ disabled: false }}
                dependencyEditFeature
                height="100%"
                project={ganttProject}
                taskEditFeature
                taskTooltipFeature
                viewPreset="weekAndDayLetter"
              />
            </>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
