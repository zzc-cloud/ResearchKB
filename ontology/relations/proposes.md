## 关系语义说明
- `proposes` 表示论文首次提出或正式定义某方法、可执行方法框架，或面向任务的可复用解决方案。
- 合法 source：`Paper`。
- 合法 target：`Method`。
- phase 1 不再为 framework / taxonomy / terminology 单独生成实体；若论文只提供组织性解释而不形成可复用方法，应保留在 prose / Evidence 中。
- 若提出语义同时包含框架拆解、机制细节或命名解释，应继续保留在 `edge_semantics` 中，而不是拆分新的 formal relation。

## 实例边
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]
  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_path: ontology/entities/methods/PathMind.md
  - edge_semantics: 论文正式提出 PathMind 这一 Retrieve-Prioritize-Reason 框架，作为面向知识图谱推理的可复用方法实例。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
