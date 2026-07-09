---
name: mary-workflow
description: Run a v3 milestone workflow from `.mary-workflow/`. Use when the user invokes `/mw-init`, `/mw-plan`, `/mw-run`, `/mw-status`, `/mw-stop`, `/mw-debug`, `/mw-cycle`, or asks to run Mary workflow.
---

# Mary Workflow

Mary Workflow v3 keeps project-local state in `.mary-workflow/` and drives Codex through project understanding, milestone planning, automatic execution/review, debug recovery, cycle archives, and audit-friendly state updates.

## Commands

User-facing command surface:

- `/mw-init`: create `.mary-workflow/`, seed prompts, detect project structure/tech/test commands, write `project-brief.md`, and create v3 state.
- `/mw-init --reset`: remove and recreate `.mary-workflow/`.
- `/mw-plan`: run the adaptive interview gate, then write 1 to 7 milestones with clarifications.
- `/mw-run`: automatic main loop for current phase.
- `/mw-status`: read-only state dashboard.
- `/mw-stop`: pause while preserving state, logs, reports, and cycle.
- `/mw-debug`: manually load debug phase when the workflow is in `DEBUGGING`.
- `/mw-cycle`: archive the current cycle to `.mary-workflow/cycles/<cycle>/`, reset active short-term state, and point back to `/mw-plan`.

## Runtime Rules

1. Work from the user's current project directory.
2. v3 state files must contain `version: 3`; v1/v2 state files are rejected and require `/mw-init --reset`.
3. `init` defaults to Chinese, writes `.mary-workflow/project-brief.md`, then asks whether plan/run should use `zh`, `auto`, or `en`.
4. Project understanding corrections use `update_project`; do not hand-edit `state.yaml` or `project-brief.md`.
5. State updates go through `scripts/mary_workflow.py apply-action`.
6. Phase/action whitelist is enforced by the runtime:
   - `PLANNING`: `update_project`, `update_state`
   - `EXECUTING`: `mark_task_done`, `record_error`
   - `REVIEWING`: `set_phase`, `record_error`
   - `DEBUGGING`: `enqueue_fix_task`
7. `/mw-plan` with `plan.interview: on` must complete the adaptive interview gate before `update_state`: 0 to 3 progressive rounds, 3 to 5 necessary questions per active round, early stop when enough information is available, and `clarifications` covering every round/default.
8. `log.md` stays English for grep and audit stability. User-facing explanations follow `.mary-workflow/config.yaml` `output.language`.

## Memory Model

- Long-term memory: `.mary-workflow/project-brief.md` and the `project` section in `state.yaml`.
- Cycle-local short-term memory: milestones, reports, logs, leases, and clarifications.
- `/mw-cycle` archives short-term memory and starts the next cycle without planning new work.

## Codex Native Commands

Autocomplete is surfaced through command-specific sub-skills under `skills/`:

- `skills/init/SKILL.md` -> `/mw-init`
- `skills/plan/SKILL.md` -> `/mw-plan`
- `skills/run/SKILL.md` -> `/mw-run`
- `skills/status/SKILL.md` -> `/mw-status`
- `skills/stop/SKILL.md` -> `/mw-stop`
- `skills/debug/SKILL.md` -> `/mw-debug`
- `skills/cycle/SKILL.md` -> `/mw-cycle`

Command Markdown files also live under `commands/` for clients that support file-based command loading.

## File Contract

See `references/state-contract.md` for expected v3 files and state fields.
