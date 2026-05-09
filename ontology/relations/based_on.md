## 关系语义说明
- `based_on` 表示某方法以另一方法或方法路线作为上游基础、继承对象或直接借鉴来源。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系强调继承与借鉴，不自动等同于性能或能力上的改进。
- 若需要表达改进、增强、优化等增量语义，应写入 `edge_semantics`，而不是额外拆分 formal relation。

## 实例边
- [[PathMind]] --based_on--> [[RoG]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/RoG.md
  - edge_semantics: PathMind 延续了显式关系路径驱动推理的 retrieval-augmented 路线。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
