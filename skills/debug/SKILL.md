---
name: debug
description: Convert the latest Mary Workflow error into a fix task. Use when the user invokes /mw-debug.
---

# Mary Workflow: Debug

Load Mary Workflow's debug phase and turn `last_error` into a repair task.

## Procedure

1. Work from the user's current project root.
2. Render debug context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-debug
   ```

3. Treat the rendered output as the active instruction context.
4. Follow `mw-debug.md` exactly: verify `workflow.phase: DEBUGGING`, inspect `last_error`, output one `enqueue_fix_task` action, and apply it with `mary_workflow.py apply-action`.
5. If the user supplied a new error but state is not `DEBUGGING`, record it first with `mary_workflow.py record-error`.

