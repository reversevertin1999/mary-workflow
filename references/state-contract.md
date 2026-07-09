# Mary Workflow v3 State Contract

Mary Workflow stores runtime files in `.mary-workflow/`.

## Directory Layout

```text
.mary-workflow/
├── config.yaml
├── project-brief.md
├── state.yaml
├── prompts/
│   ├── mw-plan.md
│   ├── mw-execute.md
│   ├── mw-review.md
│   └── mw-debug.md
├── reports/
│   └── C0/
│       └── milestone-1.md
├── cycles/
│   └── C0/
│       ├── state.yaml
│       ├── log.md
│       └── reports/
│           └── milestone-1.md
└── log.md
```

## State Version

`state.yaml` must contain:

```yaml
version: 3
cycle: C0
```

Mary Workflow v3 rejects v1/v2 state files. Use `/mw-init --reset` to recreate old projects.

## Config

```yaml
workflow:
  name: Mary Workflow
  prompt_glob: prompts/*.md
output:
  language: zh
plan:
  interview: on
  interview.max_rounds: 3
  interview.questions_per_round: "3-5"
```

`output.language` controls user-visible language for plan/run/debug/status/stop. `zh` is the default, `auto` follows the conversation, and `en` forces English.

## Core State Shape

```yaml
version: 3
cycle: C0

workflow:
  status: idle
  phase: PLANNING
  started_at:
  updated_at:

project:
  root: "/path/to/project"
  brief: ".mary-workflow/project-brief.md"
  language: zh
  structure:
    - "README.md"
  tech_stack:
    - "python"
  test_commands:
    - "pytest"

planning:
  clarifications:
    - "验收方式：pytest"

current:
  index: 0
  prompt_file: mw-plan.md
  milestone_id:

progress:
  completed: 0
  total: 0

execution_lease:
  owner:
  milestone_id:
  started_at:

milestones:
  - id: milestone-1
    status: pending
    title: "Implement one independently verifiable slice"
    deliverables:
      - "src/module.py"
    acceptance:
      - "pytest"
    estimated_scope: 2
    gate: auto
    review: ""

audit:
  action_counts:
    update_project: 0
    update_state: 0
    mark_task_done: 0
    set_phase: 0
    record_error: 0
    enqueue_fix_task: 0
  rejected_actions: 0
  phase_history:
    - "PLANNING -> EXECUTING (envelope: update_state)"
```

## Action Whitelist

- `PLANNING`: `update_project`, `update_state`
- `EXECUTING`: `mark_task_done`, `record_error`
- `REVIEWING`: `set_phase`, `record_error`
- `DEBUGGING`: `enqueue_fix_task`
- `FINISHED`: no mutating actions

`update_project` is the only legal way to correct init project understanding. It may update `structure`, `tech_stack`, `test_commands`, and `language`, then rewrites `.mary-workflow/project-brief.md`.

## Plan Interview

When `plan.interview: on`, `/mw-plan` must complete the interview gate before `update_state`.

Rules:

- 0 to 3 progressive rounds, capped by `plan.interview.max_rounds`.
- Each active round asks 3 to 5 targeted questions.
- A question is allowed only when its answer can change milestone decomposition or acceptance criteria.
- Later rounds must anchor to the previous answer and the remaining uncertainty.
- Small 1 to 2 milestone tasks may use 0 to 1 round with stated defaults.
- Large 5+ milestone tasks may use 2 to 3 rounds when uncertainty remains.
- The planner may stop early with `信息已足够，剩余采用默认值：...`.

`update_state` must include `data.clarifications` summarizing all rounds, answers, and defaults; missing or empty clarifications are rejected.

```json
{
  "action": "update_state",
  "data": {
    "phase": "EXECUTING",
    "clarifications": [
      "Round 1: 用户确认验收方式为 pytest",
      "Defaults: 未指定性能目标，默认以测试通过为准"
    ],
    "milestones": [
      {
        "id": "milestone-1",
        "title": "Concrete milestone",
        "deliverables": ["relative/path.ext"],
        "acceptance": ["pytest"],
        "estimated_scope": 2,
        "gate": "auto"
      }
    ]
  }
}
```

## Cycle Archive

`/mw-cycle` archives current short-term memory into `.mary-workflow/cycles/<cycle>/`, resets active milestones/reports/log, increments `cycle`, and tells the user to run `/mw-plan`.

Project brief is long-term memory and remains in the active root. Milestones, reports, logs, leases, and clarifications are cycle-local.

## Command Surface

v3 exposes seven commands:

```text
/mw-init
/mw-plan
/mw-run
/mw-status
/mw-stop
/mw-debug
/mw-cycle
```
