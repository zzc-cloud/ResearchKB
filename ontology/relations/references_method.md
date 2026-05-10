## 关系语义说明
- `references_method` 表示某方法将另一方法作为关键比较对象、借鉴路线或方法参照。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系不表示方法谱系继承，因此不驱动 `parent_methods` / `child_methods`。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。

## 实例边
- 无
