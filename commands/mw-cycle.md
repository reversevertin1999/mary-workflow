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

2. Report the archived cycle and the new active cycle.
3. Tell the user the next command is `/mw-plan`.

