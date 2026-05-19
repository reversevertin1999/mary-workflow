---
name: plan
description: Plan Mary Workflow tasks. Use when the user invokes /mw-plan or asks Mary to split a request into workflow tasks.
---

# Mary Workflow: Plan

Load Mary Workflow's planning phase and create the task list.

## Procedure

1. Work from the user's current project root.
2. Render planning context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-plan
   ```

3. Treat the rendered output as the active instruction context.
4. Follow `mw-plan.md` exactly: verify `workflow.phase: PLANNING`, create 1 to 3 tasks, output an `update_state` action, and apply it with `mary_workflow.py apply-action`.
5. Do not edit product code during planning unless explicitly requested.

