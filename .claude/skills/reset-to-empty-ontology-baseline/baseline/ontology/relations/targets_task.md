> 本页是正式关系账本：维护 `targets_task` 实例边。默认问答优先读取任务页、方法页或论文页；只有在任务映射治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../entities/tasks/index|tasks/index]]、[[../entities/methods/index|methods/index]]、[[../entities/papers/index|papers/index]]
> 相关证据入口：[[supported_by]]

## `targets_task` 实例边
- `targets_task` 表示方法或论文明确面向某个研究任务。
- 常见 source：`Method`、`Paper`
- 常见 target：`Task`
- 与应用场景相关的落地语义默认写入对象页 `scenario`、正文或 `reason`，而不再单独拆分 formal relation。

## 实例边
