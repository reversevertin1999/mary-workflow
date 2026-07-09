---
name: cycle
description: Archive the current Mary Workflow cycle and reset active state. Use when the user invokes /mw-cycle.
---

# Mary Workflow: Cycle

Archive the current cycle into `.mary-workflow/cycles/<cycle>/` and start the next cycle.

## Procedure

1. Work from the user's current project root.
2. Run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py cycle
   ```

3. Report the archive path and new cycle.
4. Tell the user the next step is `/mw-plan`.

