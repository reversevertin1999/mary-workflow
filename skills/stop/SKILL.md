---
name: stop
description: Stop Mary Workflow without deleting state. Use when the user invokes /mw-stop.
---

# Mary Workflow: Stop

Stop Mary Workflow while keeping state and logs.

## Procedure

1. If `.mary-workflow/state.yaml` is missing, ask the user to run `/mw-init`.
2. Run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py stop
   ```

3. Report the stopped status and current phase.

