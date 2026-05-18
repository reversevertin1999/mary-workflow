# Mary Execute Phase

> 中文说明：这是“执行阶段”。AI 会读取第一个未完成任务，完成对应代码修改和验证，然后把该任务标记为 done。下面的英文是给 AI 稳定执行的协议；命令、状态值和文件名保持英文。

## Agent Protocol

You are the implementer for Mary Workflow.

### Goal

Read the first unfinished task from `.mary-workflow/state.yaml`, implement it in the project, verify the change, and mark that task as done.

### Procedure

1. From the project root, find the next pending task:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py next-task
   ```

2. If there is no pending task, stop execution and let the workflow move to `REVIEWING`.
3. Implement only the current task. Keep unrelated refactors out of the change.
4. Run focused validation that matches the files you changed.
5. If the implementation is complete, mark the task done:

   ```bash
   python ~/.codex/skills/mary-workflow/scripts/mary_workflow.py done-task --id task-1
   ```

6. If validation fails or the task is blocked, do not mark the task done. Explain the blocker and leave the workflow in `EXECUTING`.

### Output

Summarize what changed, what validation ran, and whether another task remains.

## 中文说明

这个阶段负责“动手做一个任务”。它一次只处理一个未完成任务，避免多个任务混在一起导致改动边界不清。

- 输入：`.mary-workflow/state.yaml` 里的第一个 `pending` 任务。
- 执行：实现当前任务，并运行匹配改动范围的验证。
- 成功：调用 `done-task --id task-1` 把任务标记为 `done`。
- 失败：不要标记完成，说明阻塞原因，阶段保持在 `EXECUTING`。
- 自动流转：最后一个任务完成后，脚本会把阶段切到 `REVIEWING`。

使用时要注意：示例里的 `task-1` 只是例子，真实执行时应该使用 `next-task` 输出的任务 id。

机器协议请继续保留英文：

- 任务状态：`pending`、`done`
- 阶段名：`EXECUTING`、`REVIEWING`
- 命令名：`next-task`、`done-task`
