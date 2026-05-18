---
name: mary-workflow
description: Run a minimal project-local prompt workflow from `.mary-workflow/`. Use when the user invokes `/mw:init`, `/mw:start`, `/mw:next`, `/mw:resume`, `/mw:status`, `/mw:stop`, or asks to run Mary workflow.
---

# Mary Workflow

Mary Workflow is a small serialized prompt pipeline. It keeps project-local state in `.mary-workflow/` and executes prompt files from `.mary-workflow/prompts/` in lexicographic order.

## Commands

Use `scripts/mary_workflow.py` for deterministic state operations:

```bash
python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py <command>
```

- `/mw:init`: create `.mary-workflow/` with `config.yaml`, `state.yaml`, `prompts/`, and `log.md`.
- `/mw:start`: initialize prompt ordering and set the workflow to the first pending prompt.
- `/mw:next` or `/mw:resume`: execute the current prompt, then advance state to the next prompt.
- `/mw:status`: show current status, progress, and prompt file.
- `/mw:stop`: set the workflow status to `stopped` and append a log entry.

## Runtime Rules

1. Before any command, work from the user's current project directory.
2. If `.mary-workflow/` is missing, run `/mw:init` when the user asked to initialize; otherwise tell the user to run `/mw:init`.
3. For state-only operations, use `scripts/mary_workflow.py`.
4. For `/mw:next` and `/mw:resume`, read the current prompt file, perform the user's project work requested by that prompt, then run:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py complete-current
   ```

5. Append important user-visible events to `.mary-workflow/log.md`.
6. User-facing output should follow the user's conversation language.

## Prompt Execution

When executing a prompt:

1. Read `.mary-workflow/state.yaml`.
2. Read `.mary-workflow/prompts/<current prompt>`.
3. Treat the prompt as the active user task.
4. Complete the task with normal Codex engineering discipline.
5. Mark the prompt complete with `complete-current`.
6. Report the result and the next prompt, if any.

## File Contract

See `references/state-contract.md` for the expected `.mary-workflow/` files and state fields.
