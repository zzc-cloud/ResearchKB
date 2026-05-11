## 关系语义说明
- `applied_in` 表示方法被明确应用、部署、验证或定位在某个应用场景中。
- 合法 source：`Method`。
- 合法 target：`Scenario`。
- 该关系用于表达应用语境归属，而不是研究任务归属；研究任务应继续使用 `targets_task`。
- Paper 页中的场景信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Scenario` formal edge。

## 实例边
- [[PathMind]] --applied_in--> [[企业知识图谱问答]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/scenarios/企业知识图谱问答.md
  - edge_semantics: 方法在企业知识图谱问答场景中结合路径优先化与结构化推理完成复杂问答。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
