---
name: resume
description: Resume Mary Workflow from the current phase. Use when the user invokes /mw-resume.
---

# Mary Workflow: Resume

Resume Mary Workflow. This is the same runtime behavior as `/mw-next`.

## Procedure

1. Work from the user's current project root.
2. Render the current phase context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-resume
   ```

3. Treat the rendered output as the active instruction context.
4. Follow the loaded phase prompt and update state only through `mary_workflow.py apply-action`.
5. If phase is `FINISHED`, report completion and do not mutate state.

