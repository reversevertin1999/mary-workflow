---
name: paper
description: Manage Mary Workflow's v2.2 paper pipeline and perform contract-validated close reading from arXiv HTML or PDF. Use when the user invokes /mw-paper, asks to register or inspect a paper, asks to read a paper closely, supplies an arXiv id/URL or PDF, or applies paper stage transitions without plan/run authorization.
---

# Mary Workflow: Paper

Manage independent paper states and the `read` stage under `.mary-research/papers/`.

## Procedure

1. Work from the user's current project root; do not require `/mw-init`.
2. Use `scripts/mw_paper.py` for every state read and mutation.
3. Use `create`, `list`, `status`, and `apply-action` for low-level state operations.
4. Require a canonical paper id and SHA-256 fingerprint contract.
5. Apply stage changes only through `start_stage`, `complete_stage`, `fail_stage`, `reset_stage`, and `update_source` envelopes.
6. Preserve the dependency graph:
   - `read` has no stage dependency;
   - `summary` depends on `read`;
   - `slides` depends on `summary`;
   - `quiz` depends on `read` and `summary`, not `slides`.
7. Let source changes and stage resets mark already-started downstream stages `stale`; leave never-started stages `pending`.
8. Do not run milestone grants or leases. Paper state is independent from `.mary-workflow/` and survives `/mw-init --reset`.
9. For `/mw-paper read <source>`:
   - run `prepare-read --source <source>` (and `--paper-id` when needed);
   - read `read-context.json`, `parse-quality.json`, and all of `source.md`;
   - if quality is blocked, show all five statuses and evidence, then stop for explicit user direction;
   - otherwise write `paper-notes.md` using the exact ledger contract and run `complete-read`.
10. Copy source identity and parse quality from `read-context.json`; do not calculate or improvise those fields.
11. Keep `uncertainties` non-empty. Add every degraded or failed quality dimension to at least one uncertainty.
12. Pass `--override-quality --override-reason <reason>` only after the user explicitly accepts a displayed blocked report. Never infer consent.
13. Do not generate `summary.md`, `slides.md`, or `quiz-log.md`; those stages are not implemented yet.

Read `references/paper-notes-contract.md` before producing `paper-notes.md`. See `references/paper-state-contract.md` for state transitions.
