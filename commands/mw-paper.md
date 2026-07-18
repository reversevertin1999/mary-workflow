---
description: Manage paper state or perform contract-validated close reading from arXiv HTML/PDF.
argument-hint: [read|create|list|status|apply-action] [source/options]
---

# /mw-paper

Manage project-local paper workspaces without entering the milestone workflow authorization flow.

## Instructions

1. Work from the user's current project root. `/mw-init` is not required.
2. Route low-level `$ARGUMENTS` to the paper runtime:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mw_paper.py <subcommand> <options>
   ```

3. Supported state subcommands:
   - no arguments: run `list`;
   - `list`: list registered paper ids;
   - `status [paper-id]`: run `status`, adding `--paper-id` when supplied;
   - `create --source <locator> --fingerprint <sha256> [--paper-id <id>]`: create an independent paper state;
   - `apply-action [paper-id]`: apply one `start_stage`, `complete_stage`, `fail_stage`, `reset_stage`, or `update_source` envelope with `--json` or `--file`.
4. For `read <source>`:
   - run `python ~/.codex/skills/mary-workflow/scripts/mw_paper.py prepare-read --source <source>`;
   - inspect `read-context.json` and the full `parse-quality.json`;
   - if `gate=blocked`, report the five dimensions and evidence, then end the response without creating notes;
   - otherwise read all of `source.md`, create `paper-notes.md` per `references/paper-notes-contract.md`, and run `complete-read`.
5. A later explicit user quality override may be completed with `complete-read --override-quality --override-reason <reason>`. The initial read request is not override consent.
6. Treat `.mary-research/papers/<paper-id>/state.json` as authority. Never hand-edit it or `read-context.json`.
7. Do not invoke `/mw-plan`, `/mw-run`, grants, or execution leases for paper actions.
8. Do not produce summary, slides, or quiz artifacts before their implementation stages.
