## 关系语义说明
- `targets_task` 表示方法明确面向某个研究任务。
- 合法 source：`Method`。
- 合法 target：`Task`。
- Paper 页中的任务定位保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- 与应用场景相关的落地语义，若已稳定到方法层则应使用 `applied_in`；否则可写入对象页 `scenario`、正文或 `edge_semantics`。

## 实例边
- 无
