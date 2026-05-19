---
name: start
description: Start Mary Workflow and enter the planning phase. Use when the user invokes /mw-start.
---

# Mary Workflow: Start

Start Mary Workflow for the current project.

## Procedure

1. If `.mary-workflow/state.yaml` is missing, ask the user to run `/mw-init`.
2. Run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py start
   ```

3. Report status, phase, current prompt, and progress.
4. Do not edit product code in this command.

