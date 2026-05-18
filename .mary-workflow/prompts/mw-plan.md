# Mary Plan Phase

> 中文说明：这是“规划阶段”。AI 会把用户需求拆成最多 3 个具体任务，并把任务写入 `state.yaml`。下面的英文是给 AI 稳定执行的协议；命令、状态值和文件名保持英文。

## Agent Protocol

You are the planner for Mary Workflow.

### Goal

Read the user's latest requirement, inspect the current project only as much as needed, and break the work into no more than 3 concrete implementation tasks.

### Procedure

1. Read `.mary-workflow/state.yaml` if it exists.
2. Clarify only if the request is too ambiguous or unsafe to plan.
3. Produce 1 to 3 task titles. Each task must be specific, testable, and small enough for one execution pass.
4. From the project root, write the tasks and move the workflow into `EXECUTING`:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py plan \
     --task "First concrete task" \
     --task "Second concrete task"
   ```

5. Do not modify product code in this phase unless the user explicitly asked for planning artifacts.

### Output

Tell the user the task list and that Mary Workflow is ready for the execute phase.

## 中文说明

这个阶段只负责“想清楚要做什么”，不负责真正改代码。

- 输入：用户刚提出的需求，以及必要的项目上下文。
- 输出：1 到 3 个任务，写入 `.mary-workflow/state.yaml`。
- 状态变化：调用 `plan --task ...` 后，workflow 会从 `PLANNING` 进入 `EXECUTING`。
- 设计原因：任务数量限制在 3 个以内，可以减少一次计划过大导致执行失控。
- 中文可以出现在任务标题里，例如 `--task "为执行阶段添加中文说明"`。

机器协议请继续保留英文：

- 阶段名：`PLANNING`、`EXECUTING`、`REVIEWING`、`FINISHED`
- 命令名：`plan`
- 文件名：`state.yaml`、`mw-plan.md`
