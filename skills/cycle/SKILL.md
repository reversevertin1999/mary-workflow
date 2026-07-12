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

3. If the command reports `refresh_required`, render `mw-init`, perform the incremental reread for every `project.changed_files` entry, apply a complete `submit_brief mode=cycle_refresh`, and run `cycle` again.
4. Report the archive path, new cycle, and updated project-brief version.
5. Tell the user the next step is `/mw-plan`.
