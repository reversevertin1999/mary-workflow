# Mary Workflow v2.1 State Contract

Mary Workflow stores runtime authority in `.mary-workflow/`. Filesystem state, not conversation memory, controls every transition.

## Directory Layout

```text
.mary-workflow/
├── config.yaml
├── project-brief.md
├── state.yaml
├── analysis/submit-brief.json
├── prompts/
│   ├── mw-init.md
│   ├── mw-plan.md
│   ├── mw-ready.md
│   ├── mw-resume.md
│   ├── mw-execute.md
│   ├── mw-review.md
│   └── mw-debug.md
├── reports/C0/milestone-1.md
├── cycles/C0/{state.yaml,project-brief.md,log.md,analysis/,reports/}
└── log.md
```

## Version

```yaml
version: 2.1
cycle: C0
```

v2.1 rejects earlier state contracts. Recreate old workspaces with `/mw-init --reset`; there is no implicit migration because `PLANNED` and the lease/grant contract change state semantics.

## Init Understanding Contract

The machine scanner traverses the complete repository with no file-count or path sampling. It excludes `.git`, `.mary-workflow`, dependency/build/cache directories, symlinks, and binary files. `project.inventory` is the complete authority list and `project.fingerprints` stores SHA-256 records for cycle refresh detection.

`project.brief_status` uses:

- `machine_detected`: scanner skeleton exists; full init understanding is required.
- `complete`: the five-layer brief passed schema and inventory validation.
- `refresh_required`: cycle changes were detected; archive is blocked until incremental reread is submitted.

While a PLANNING state lacks a complete brief, legal actions are limited to `submit_brief` and `update_project`. Planning interviews cannot start.

`submit_brief` requires:

1. machine detection from the runtime: full inventory, stack, candidate build/test/run commands;
2. positioning: purpose, audience, problem, differentiators;
3. architecture: modules/responsibilities/files, dependency adjacency list, ordered data flow, state locations and mutators;
4. one file-ledger record for every inventory path, with non-empty purpose, exports, and consumers;
5. a non-empty uncertainty list whose records are explicitly `inferred` or `unresolved`.

It also requires build, test, and run evidence. Each evidence record stores the exact command, `passed|failed|skipped`, concrete summary, and duration. Safe skips require an explicit reason; detected commands are candidates, not execution claims.

Three-pass evidence is machine validated:

- pass 1 declares complete inventory coverage, enforced by exact ledger path equality;
- pass 2 lists full-read entrypoints, configuration, core modules, and tests;
- pass 3 stores global synthesis, module summaries, and reread files.

Large repositories may use `.mary-workflow/analysis/` module summaries, but every inventory file must still appear in the final ledger. This is hierarchical synthesis, not sampling.

Successful submission increments `project.brief_version`, stamps the current cycle/time, refreshes fingerprints, writes the full `project-brief.md`, and prints the entire document. `/mw-plan` loads that full brief as authority.

Full ledgers are submitted from `.mary-workflow/analysis/submit-brief.json` through `apply-action --file`; they are not passed as a potentially oversized shell argument. The submitted envelope remains local audit evidence.

At `/mw-cycle`, added/modified/deleted text files are compared against fingerprints. Any change writes exact `project.changed_files`, sets `refresh_required`, and pauses archive. `submit_brief mode=cycle_refresh` must acknowledge that exact list and replace the complete brief; only a subsequent `/mw-cycle` archives state, reports, log, and the brief snapshot.

## Phase Graph

```text
PLANNING --update_state--> PLANNED
PLANNED --start_execution + start grant--> EXECUTING
EXECUTING --mark_task_done--> REVIEWING
EXECUTING/REVIEWING --record_error--> DEBUGGING
DEBUGGING --enqueue_fix_task--> EXECUTING
REVIEWING --set_phase--> EXECUTING | PLANNING | FINISHED
stopped active phase --resume_execution + resume grant--> same active phase
```

`/mw-cycle` archives the active cycle and resets to `PLANNING`. No edge other than a grant-backed `start_execution` may enter initial `EXECUTING` from `PLANNED`.

## Action Whitelist

- incomplete brief in `PLANNING`: `submit_brief`, `update_project`
- complete brief in `PLANNING`: `submit_brief`, `update_project`, `update_interview`, `update_state`
- `PLANNED`: `reopen_plan`, `start_execution`
- `EXECUTING`: `mark_task_done`, `record_error`
- `REVIEWING`: `set_phase`, `record_error`
- `DEBUGGING`: `enqueue_fix_task`
- `FINISHED`: none

When an active phase has `workflow.status: stopped`, its normal actions are replaced by `resume_execution` only.

## Planning Contract

The interview persists every question and answer. Adaptive depth is enforced:

- 1 to 2 milestones may use confirmed round-0 defaults.
- 3 to 4 milestones require at least one answered active round.
- 5 or more milestones require at least two answered active rounds.

Lifecycle values are `not_started`, `awaiting_answers`, `in_progress`, `draft_ready`, `plan_ready`, and `complete`. `draft_ready` is a persisted draft awaiting `update_state`; `plan_ready` is a frozen, still-unconfirmed plan awaiting `/mw-run`.

Every default or assumption must be persisted and displayed before the user answers. `plan.interview: off` disables open-ended interviewing, not confirmation: `mode=propose` remains in `awaiting_answers` until the user explicitly accepts the listed assumptions. `resolve` and `revise` reject newly introduced defaults.

Every milestone has `id`, `title`, file-level `deliverables`, executable `acceptance`, `estimated_scope <= 5`, and `gate: auto|confirm`.

When the draft is complete, `update_state` must copy persisted `clarifications` and `draft_milestones` exactly:

```json
{
  "action": "update_state",
  "data": {
    "phase": "PLANNED",
    "clarifications": ["<exact persisted record>"],
    "milestones": [
      {
        "id": "milestone-1",
        "title": "Frozen delivery unit",
        "deliverables": ["src/module.py"],
        "acceptance": ["pytest"],
        "estimated_scope": 1,
        "gate": "auto"
      }
    ]
  }
}
```

This produces `interview_status: plan_ready`, `final_plan_confirmed: false`, and phase `PLANNED`. It never starts product work. `/mw-plan` can use `reopen_plan` to return a frozen plan to `PLANNING` for revision.

## Run Grant

Rendering `/mw-run` in `PLANNED` creates a short-lived one-time start grant bound to:

- current cycle
- SHA-256 digest of clarifications and the frozen milestone schema
- purpose `start`

The plaintext token appears only in that `/mw-run` render. `state.yaml`, `/mw-status`, and logs store only digest metadata and a short fingerprint:

```yaml
run_grant:
  token_digest: <sha256>
  fingerprint: <12 hex chars>
  purpose: start
  plan_digest: <sha256>
  cycle: C0
  issued_at: <timestamp>
  expires_at: <timestamp>
```

```json
{
  "action": "start_execution",
  "data": {"token": "<plaintext token from current /mw-run render>"}
}
```

Successful consumption is single-use and atomic: it sets `final_plan_confirmed: true`, changes `interview_status` to `complete`, acquires the run lease, and records `PLANNED -> EXECUTING`. Replay, expiry, wrong purpose, changed plan, or changed cycle is rejected.

Before the authorization block, `/mw-run` renders `Final Plan Confirmation Evidence` as quoted JSON containing every persisted question, recorded answer, default/assumption, clarification, and frozen milestone. The ready prompt requires this evidence to be shown without paraphrasing before grant consumption; evidence strings are data, not instructions.

The repository runtime can prove possession of a token emitted by its `/mw-run` renderer. Proving that a human, rather than an agent with direct process access, invoked the renderer requires the Codex host/slash-command dispatcher to be the trusted caller.

## Execution Lease

The lease belongs to the whole run, not one phase:

```yaml
execution_lease:
  owner: codex
  status: active
  run_id: <random id>
  plan_digest: <sha256>
  cycle: C0
  milestone_id: milestone-1
  started_at: <timestamp>
  heartbeat_at: <timestamp>
```

- `start_execution` is the only initial lease acquisition point.
- EXECUTING/REVIEWING/DEBUGGING transitions preserve the run id and refresh heartbeat/current milestone.
- `/mw-stop` changes an active lease to `paused` and clears any outstanding grant.
- A later `/mw-run` issues a purpose `resume` grant; `resume_execution` restores the same run id and phase.
- FINISHED, replanning, and cycle reset release or clear the lease.

## Audit

`audit.action_counts` includes `submit_brief`, `update_interview`, `update_project`, `update_state`, `reopen_plan`, `start_execution`, `resume_execution`, `mark_task_done`, `set_phase`, `record_error`, and `enqueue_fix_task`. `phase_history` records, at minimum:

```text
PLANNING -> PLANNED (envelope: update_state; plan ready)
PLANNED -> EXECUTING (/mw-run: start_execution)
EXECUTING -> REVIEWING (auto: all tasks done)
```

Rejected envelopes increment `rejected_actions` and leave action mutations unapplied.

## Command Surface

```text
/mw-init
/mw-plan
/mw-run
/mw-status
/mw-stop
/mw-debug
/mw-cycle
```
