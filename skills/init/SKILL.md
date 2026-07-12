---
name: init
description: Initialize or reset Mary Workflow v2.1 in the current project. Use when the user invokes /mw-init or asks to initialize Mary workflow.
---

# Mary Workflow: Init

Initialize the project-local `.mary-workflow/` workspace.

## Procedure

1. Work from the user's current project root.
2. Run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py init
   ```

3. If the user passes `--reset`, run `init --reset`.
4. Render init understanding context:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_codex.py mw-init
   ```

5. Follow `mw-init.md`: complete the full three-pass read, execute safe build/test/run validation, write the full envelope to `.mary-workflow/analysis/submit-brief.json`, and apply the machine-validated `submit_brief` with `--file`.
6. Present the entire `.mary-workflow/project-brief.md` to the user, then ask for factual corrections and `zh`/`auto`/`en` preference.
7. On an existing v2.1 project, preserve state, refresh prompts, and perform incremental reread when `brief_status: refresh_required`; earlier contracts require `--reset`.
8. Do not hand off to `/mw-plan` until `project_brief_status: complete`.
