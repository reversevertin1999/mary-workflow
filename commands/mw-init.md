---
description: Initialize or reset Mary Workflow v2.1 in the current project.
argument-hint: [--reset]
---

# /mw-init

Initialize Mary Workflow in the current project directory.

## Instructions

1. Run from the user's current project root:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py init
   ```

2. If `$ARGUMENTS` contains `--reset`, run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py init --reset
   ```

3. Render the full init understanding context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-init
   ```

4. Follow `mw-init.md`: read the complete text inventory in three passes, run safe build/test/run commands, write the full `submit_brief` envelope to `.mary-workflow/analysis/submit-brief.json`, and apply it with `--file`.
5. Present the entire generated `.mary-workflow/project-brief.md`, not only its path or a short summary.
6. Ask whether the user wants later plan/run output in `zh`, `auto`, or `en`; if they answer, apply `update_project` with `language`.
7. On an existing v2.1 project, refresh prompts and follow `brief_status`: complete briefs are displayed, changed projects require incremental reread, and earlier state contracts require `--reset`.
8. Tell the user `/mw-plan` is available only after `project_brief_status: complete`.
