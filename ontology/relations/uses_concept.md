## 关系语义说明
- `uses_concept` 表示论文或方法显式采用某概念作为定义、建模、机制设计或实现的一部分。
- 合法 source：`Paper`、`Method`。
- 合法 target：`Concept`。
- 方法与概念之间的正式关系默认优先使用该边，而不是 `based_on`。
- 若需要表达“以前提方式依赖该概念”，默认写入 `edge_semantics`，而不额外拆分 formal relation。

## 实例边
- 无
