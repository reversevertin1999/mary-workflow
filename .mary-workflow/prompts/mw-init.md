# Mary Init Understanding Phase

## Language Policy

推理过程、进度叙述和用户可见回答必须遵守 `.mary-workflow/config.yaml` 的 `output.language`：默认 `zh` 一律中文，`auto` 跟随会话，`en` 使用英文。机器字段、命令、路径、JSON key 和日志保持英文。

## Goal

Build a complete, evidence-backed project understanding. Read every machine-inventoried text file without a sampling budget. The only physical limit is context size; solve that with module-level synthesis, never by dropping files.

## Status Gate

Read `project.brief_status` and `project.changed_files` from state:

- `machine_detected`: perform the full three-pass initial analysis and submit `mode: initial`.
- `refresh_required`: reread every added/modified file, account for deleted files, update affected architecture and ledger entries, then submit the complete updated brief with `mode: cycle_refresh`.
- `complete`: display the full existing `project-brief.md`. Only submit `mode: correction` when the user supplied evidence that requires a correction.

Do not plan milestones or edit product files during init understanding.

## Pass 1: Full Inventory

1. Use `project.inventory` as the authority list. Do not truncate, sample, or use only a directory tree.
2. Read every listed file completely. Binary and ML artifact files, dependency directories, `.git`, `.mary-workflow`, `config.yaml` `init.ignore` globs, and project-root `.maryignore` globs are already excluded by the machine scanner. The remaining inventory is exhaustive.
3. Produce exactly one ledger record per inventory path:
   - what the file is responsible for;
   - what it exports or provides;
   - which files, modules, commands, or users consume it.
4. Explicitly write `(none discovered)` where a file has no exports or known consumers. Empty fields are forbidden.

## Pass 2: Deep Read

Read entrypoints, configuration, core modules, and tests in full. Follow imports, command dispatch, and calls until you can state:

- where data enters, each important transformation, and where it leaves;
- where state is stored and exactly which components mutate it;
- how build, test, and run commands connect to the implementation.

Record the exact files used for each deep-read category. If a category does not exist, record a non-empty sentinel such as `(none found: no test files in inventory)`.

## Pass 3: Synthesis

Write the positioning and architecture from the evidence, without copying the previous conversation summary. If synthesis exposes a gap, reread the relevant files before submission and record them in `pass3.reread_files`.

For a repository too large for one context window, write module summaries under `.mary-workflow/analysis/`, complete every module, then synthesize from those module summaries. This is hierarchical full coverage, not sampling.

## Validation By Execution

Run detected or repository-documented build, test, and run commands when sandbox-safe. Record command, status, duration, and concrete output summary. If a command is unavailable or unsafe, use `status: skipped` and state the exact reason; never report a guessed command as executed.

## Submit Brief Envelope

Submit all five layers through `apply-action`. `file_ledger` must exactly cover `project.inventory`; omissions and extra paths are rejected. `uncertainties` is mandatory and may contain only `inferred` or `unresolved` records.

Because a full ledger may exceed the operating system's command-line length, write the complete envelope to `.mary-workflow/analysis/submit-brief.json` and submit it with:

```bash
python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py apply-action \
  --file .mary-workflow/analysis/submit-brief.json
```

Do not inline a full repository ledger into a `--json` shell argument. Keep the submitted JSON as audit evidence.

```json
{
  "action": "submit_brief",
  "data": {
    "mode": "initial",
    "positioning": {
      "purpose": "What the project does",
      "audience": "Who uses it",
      "problem": "What problem it solves",
      "differentiators": "How it differs from alternatives"
    },
    "architecture": {
      "modules": [
        {
          "name": "module name",
          "responsibility": "module responsibility",
          "files": ["relative/path"]
        }
      ],
      "dependency_graph": ["caller -> dependency: reason"],
      "data_flow": ["Step 1: input enters through ..."],
      "state_management": ["state location -> mutator: mutation"]
    },
    "file_ledger": [
      {
        "path": "relative/path",
        "purpose": "one-line responsibility",
        "exports": ["symbol or (none discovered)"],
        "used_by": ["consumer or (none discovered)"]
      }
    ],
    "uncertainties": [
      {
        "topic": "inference or unresolved point",
        "status": "inferred",
        "detail": "evidence and what remains uncertain"
      }
    ],
    "validation": [
      {
        "kind": "build",
        "command": "exact command or skipped:<reason>",
        "status": "passed",
        "summary": "concrete output summary",
        "duration": "12.3s"
      },
      {
        "kind": "test",
        "command": "pytest",
        "status": "passed",
        "summary": "47 passed, 2 skipped",
        "duration": "12s"
      },
      {
        "kind": "run",
        "command": "exact command or skipped:<reason>",
        "status": "skipped",
        "summary": "exact safety or environment reason",
        "duration": "0s"
      }
    ],
    "analysis_evidence": {
      "pass1_inventory_complete": true,
      "pass2": {
        "entrypoints": ["relative/path"],
        "configuration": ["relative/path"],
        "core_modules": ["relative/path"],
        "tests": ["relative/path"]
      },
      "pass3": {
        "synthesis": "How module evidence supports the global understanding",
        "module_summaries": [
          {"module": "module name", "summary": "complete module summary"}
        ],
        "reread_files": ["relative/path or (none required: synthesis was internally consistent)"]
      },
      "reviewed_changed_files": []
    }
  }
}
```

For `cycle_refresh`, set `reviewed_changed_files` to exactly the machine-provided `project.changed_files` entries, including `added:`, `modified:`, and `deleted:` prefixes. Submit a complete replacement brief, preserving still-valid ledger records only after checking them against the new inventory.

After successful submission, read and present the entire `.mary-workflow/project-brief.md` to the user. Do not reduce the result to a path or short summary. Then ask for corrections and language preference; `/mw-plan` is allowed only after the brief is complete.
