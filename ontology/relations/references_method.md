## 关系语义说明
- `references_method` 表示某方法将另一方法作为关键比较对象、借鉴路线或方法参照。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系不表示方法谱系继承，因此不驱动 `parent_methods` / `child_methods`。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。

## 实例边
- [[PathMind]] --references_method--> [[GCR]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/GCR.md
  - edge_semantics: PathMind 将 GCR 作为可靠路径生成路线的重要比较与借鉴对象。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind]] --references_method--> [[EPERM]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/EPERM.md
  - edge_semantics: PathMind 将 EPERM 作为 evidence-path 增强路线的重要比较与借鉴对象。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
