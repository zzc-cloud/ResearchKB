## 关系语义说明
- `proposes` 表示论文提出了某个正式知识产物。
- 合法 source：`Paper`。
- 合法 target：`Method`、`Concept`。
- 若 framework / taxonomy 的主语义是知识组织或解释框架，target 通常是 `Concept`；若主语义是方法流程或演化路线，target 通常是 `Method`。
- 若提出语义同时包含框架拆解、机制细节或命名解释，应继续保留在 `edge_semantics` 中，而不是拆分新的 formal relation。

## 实例边
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]
  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_path: ontology/entities/methods/PathMind.md
  - edge_semantics: 论文将 PathMind 定义为 Retrieve-Prioritize-Reason 主框架的核心方法实例。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[路径优先化]]
  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_path: ontology/entities/concepts/路径优先化.md
  - edge_semantics: 论文把路径优先化作为筛选关键推理路径的核心机制。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[重要推理路径]]
  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_path: ontology/entities/concepts/重要推理路径.md
  - edge_semantics: 论文将重要推理路径定义为应优先暴露给 LLM 的高价值路径。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
