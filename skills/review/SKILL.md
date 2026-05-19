---
name: review
description: Review Mary Workflow changes and choose the next phase. Use when the user invokes /mw-review.
---

# Mary Workflow: Review

Load Mary Workflow's review phase and inspect completed work.

## Procedure

1. Work from the user's current project root.
2. Render review context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-review
   ```

3. Treat the rendered output as the active instruction context.
4. Follow `mw-review.md` exactly: verify `workflow.phase: REVIEWING`, inspect relevant changes, lead with findings, output `set_phase`, and apply it with `mary_workflow.py apply-action`.
5. Use `EXECUTING` for fixes, `PLANNING` for another cycle, and `FINISHED` when complete.

