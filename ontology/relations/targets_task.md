## 关系语义说明
- `targets_task` 表示方法明确面向某个研究任务。
- 合法 source：`Method`。
- 合法 target：`Task`。
- Paper 页中的任务定位保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- 与应用场景相关的落地语义，若已稳定到方法层则应使用 `applied_in`；否则可写入对象页 `scenario`、正文或 `edge_semantics`。

## 实例边
- [[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/knowledge-graph-reasoning.md
  - edge_semantics: 方法以知识图谱推理为总体任务定位。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/kgqa.md
  - edge_semantics: 方法在知识图谱问答任务中被验证。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
- [[PathMind]] --targets_task--> [[multi-hop-qa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/multi-hop-qa.md
  - edge_semantics: 方法重点处理复杂多跳问答中的路径筛选与推理。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
