## 关系语义说明
- `sourced_from` 表示 Evidence 对象页来源于 `ontology/entities/raw-sources/files/` 下的受管原始文件。
- 合法 source：`Evidence`。
- 合法 target：`RawSource`。
- 正式知识页应优先通过 `supported_by` 连接到 Evidence，而不是直接连接原始 PDF。
- 若证据对象页尚未生成而必须临时登记来源，可例外使用 `status: placeholder` 暂存。

## 实例边
- [[PathMind.sections]] --sourced_from--> [[ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - source_path: ontology/entities/evidence/PathMind.sections.md
  - target_path: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
  - edge_semantics: sections 缓存直接抽取自 PathMind 原文的摘要、相关工作与方法章节。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind.refs]] --sourced_from--> [[ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - source_path: ontology/entities/evidence/PathMind.refs.md
  - target_path: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
  - edge_semantics: refs 缓存抽取自 Related Work、baseline 列表与 References 页。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind.experiments]] --sourced_from--> [[ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - source_path: ontology/entities/evidence/PathMind.experiments.md
  - target_path: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
  - edge_semantics: experiments 缓存抽取自主结果、消融、效率与案例分析章节。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
