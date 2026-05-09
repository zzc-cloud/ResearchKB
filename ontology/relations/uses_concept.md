## 关系语义说明
- `uses_concept` 表示论文或方法显式采用某概念作为定义、建模、机制设计或实现的一部分。
- 合法 source：`Paper`、`Method`。
- 合法 target：`Concept`。
- 方法与概念之间的正式关系默认优先使用该边，而不是 `based_on`。
- 若需要表达“以前提方式依赖该概念”，默认写入 `edge_semantics`，而不额外拆分 formal relation。

## 实例边
- [[PathMind]] --uses_concept--> [[路径优先化]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/concepts/路径优先化.md
  - edge_semantics: 方法把路径优先化作为从查询子图中识别高价值路径的显式决策机制。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --uses_concept--> [[重要推理路径]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/concepts/重要推理路径.md
  - edge_semantics: 方法将重要推理路径视为用于约束 LLM 推理的关键中间产物。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
