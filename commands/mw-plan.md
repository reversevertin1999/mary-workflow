---
description: Interview for boundaries, then plan Mary Workflow milestones.
argument-hint: [request]
---

# /mw-plan

Load Mary Workflow's planning phase, run the adaptive interview gate, and create 1 to 7 milestones.

## Instructions

1. From the project root, render planning context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-plan
   ```

2. Treat the rendered output as active instruction context.
3. Follow `mw-plan.md`: verify `workflow.phase: PLANNING`, run 0 to 3 progressive interview rounds when `plan.interview: on`, include all rounds/defaults in `clarifications`, produce milestones with `deliverables`, `acceptance`, and `estimated_scope`, output `update_state`, and apply it with `mary_workflow.py apply-action`.
4. Do not edit product code during planning.
