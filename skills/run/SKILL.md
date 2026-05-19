---
name: run
description: Execute the first pending Mary Workflow task. Use when the user invokes /mw-run.
---

# Mary Workflow: Run

Load Mary Workflow's execution phase and complete the first pending task.

## Procedure

1. Work from the user's current project root.
2. Render execution context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-run
   ```

3. Treat the rendered output as the active instruction context.
4. Follow `mw-execute.md` exactly: verify `workflow.phase: EXECUTING`, inspect only current-task files, implement, validate, output `mark_task_done`, and apply it with `mary_workflow.py apply-action`.
5. If blocked, leave state in `EXECUTING` and explain the blocker.

