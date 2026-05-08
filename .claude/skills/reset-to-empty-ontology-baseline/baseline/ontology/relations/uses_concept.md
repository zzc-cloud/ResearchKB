> 本页是正式关系账本：维护 `uses_concept` 实例边。默认问答优先读取概念页、方法页或论文页；只有在概念使用治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../entities/concepts/index|concepts/index]]、[[../entities/methods/index|methods/index]]、[[../entities/papers/index|papers/index]]
> 相关证据入口：[[supported_by]]

## `uses_concept` 实例边
- `uses_concept` 表示方法、论文或其他对象显式使用、依赖或采用某个概念作为其语义组成部分。
- 常见 source：`Method`、`Paper`、`Concept`
- 常见 target：`Concept`
- 若需要表达成立前提、解释基础或组成条件，应将这类强语义写入 `reason`，而不是额外拆分 formal relation。

## 实例边
