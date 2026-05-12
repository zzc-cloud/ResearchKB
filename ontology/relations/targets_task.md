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
  - edge_semantics: PathMind 被明确设计为知识图谱推理框架，直接服务于 knowledge-graph-reasoning 任务。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/kgqa.md
  - edge_semantics: 论文将 PathMind 放在知识图谱问答语境下评估，并以 KGQA 作为核心任务入口之一。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --targets_task--> [[multi-hop-qa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/multi-hop-qa.md
  - edge_semantics: PathMind 旨在支持复杂多跳问题上的推理与回答，稳定覆盖 multi-hop-qa 任务。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
