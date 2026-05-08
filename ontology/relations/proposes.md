## 关系语义说明
- `proposes` 表示论文提出了某个正式知识产物。
- 合法 source：`Paper`。
- 合法 target：`Method`、`Concept`。
- 若 framework / taxonomy 的主语义是知识组织或解释框架，target 通常是 `Concept`；若主语义是方法流程或演化路线，target 通常是 `Method`。
- 若提出语义同时包含框架拆解、机制细节或命名解释，应继续保留在 `edge_semantics` 中，而不是拆分新的 formal relation。

## 实例边
- 无
