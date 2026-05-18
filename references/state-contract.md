# Mary Workflow State Contract

Mary Workflow stores project-local runtime files in `.mary-workflow/`.

## Directory Layout

```text
.mary-workflow/
├── config.yaml
├── state.yaml
├── prompts/
│   ├── 001-example.md
│   └── 002-example.md
└── log.md
```

## `state.yaml`

```yaml
workflow:
  status: idle
  started_at:
  updated_at:

current:
  index: 0
  prompt_file:

progress:
  completed: 0
  total: 0
```

Status values:

- `idle`: initialized but not started.
- `running`: prompt execution is active.
- `stopped`: user paused the workflow.
- `completed`: all prompts have completed.

## Prompt Ordering

Prompt files live in `.mary-workflow/prompts/` and must use the `.md` extension. Execution order is lexicographic, so numeric prefixes are recommended:

```text
001-scan.md
002-plan.md
003-implement.md
```
