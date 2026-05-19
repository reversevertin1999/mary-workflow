---
name: init
description: Initialize Mary Workflow in the current project. Use when the user invokes /mw-init or asks to initialize Mary workflow.
---

# Mary Workflow: Init

Initialize the project-local `.mary-workflow/` workspace.

## Procedure

1. Work from the user's current project root.
2. Run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py init
   ```

3. If the user explicitly asks for example prompts, run `init --with-examples`.
4. Report the created state and tell the user the next step is `/mw-start` or `/mw-plan`.

