## 关系语义说明
- `references_method` 表示某方法将另一方法作为关键比较对象、借鉴路线或方法参照。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系与 `based_on` 一起构成方法图谱的核心邻接关系：`based_on` 表达严格谱系，`references_method` 表达参照与比较。
- `references_method` 不表示方法谱系继承，因此不驱动 `parent_methods` / `child_methods`。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。
- `references_method` 实例边除 `source_path` / `target_path` 外，还必须记录 `source_paper_path` 与 `target_paper_path`，用于标记该方法参照关系从哪篇论文抽取，以及 target method 对应的代表 / 参考论文。

## 实例边
- 无
