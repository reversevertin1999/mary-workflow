---
name: status
description: Show Mary Workflow status without mutating state. Use when the user invokes /mw-status.
---

# Mary Workflow: Status

Show current Mary Workflow state.

## Procedure

1. Work from the user's current project root.
2. Render status context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-status
   ```

3. Report status, phase, progress, current prompt, current task, and tasks.
4. Do not mutate `.mary-workflow/state.yaml`.

