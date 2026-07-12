---
description: Archive the current Mary Workflow cycle and reset active state.
---

# /mw-cycle

Archive the current cycle and start the next one. This command only archives and resets; it does not plan new work.

## Instructions

1. From the project root, run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py cycle
   ```

2. If output reports `refresh_required`, do not claim the cycle was archived. Render `mw-init`, reread every listed changed file, submit a complete `mode: cycle_refresh` brief, then run `cycle` again.
3. Report the archived cycle, new active cycle, and evolved project-brief version.
4. Tell the user the next command is `/mw-plan`.
