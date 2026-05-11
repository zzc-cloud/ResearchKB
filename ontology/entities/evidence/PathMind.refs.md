---
title: PathMind.refs
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: refs
status: processed
year: 2026
venue: AAAI-26
---

# PathMind.refs

## Object semantics
- PathMind 论文的引用与上游路线证据页，承载关键相关工作、方法谱系定位与 formal citation grounding 的最小可审计摘要。

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../methods/RoG]]
- [[../methods/GNN-RAG]]
- [[../methods/GCR]]
- [[../methods/EPERM]]
- [[../methods/ToG]]

## 本节支撑什么
- 论文将已有 LLM-based KGR 方法划分为 retrieval-augmented 与 synergy-augmented 两大路线。
- RoG 被明确描述为 planning-retrieval-reasoning 的显式路径代表方法。
- GNN-RAG、GCR 与 EPERM 被明确作为 retrieval-augmented 路线中的代表性路径方法。
- ToG 被明确作为 synergy-augmented 路线中的代表性迭代交互方法。
- 参考文献页为关键 cites 目标和方法邻接候选提供可回查来源。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Related Work 明确将 RoG、GNN-RAG、GCR、EPERM 放入 retrieval-augmented 讨论，并指出这些路线都依赖从 KG 中取得的路径或子图信息。
- Related Work 明确将 ToG 放入 synergy-augmented 讨论，并强调其通过 LLM 与 KG 迭代交互发现推理路径。
- PathMind 自身以“Retrieve-Prioritize-Reason”组织方法，说明它与显式路径推理路线存在稳定谱系关系，同时也把另一类路径方法作为关键参照对象。
- References 页给出上述相关工作的正式题名与年份，可作为 cited paper placeholder 的来源锚点。

## 来源说明
- 来源于原始 PDF 的 Related Work、Experimental Settings 与 References 部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 引用与路线证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 引用证据页支撑 PathMind 的方法路线定位与关键比较对象。
  - evidence: [[../evidence/PathMind.refs]]
- `supported_by`：RoG（文档：`ontology/entities/methods/RoG.md`）：[[../methods/RoG]]
  - edge_semantics: 引用证据页支撑 RoG 作为显式 relational path reasoning 的代表方法语义。
  - evidence: [[../evidence/PathMind.refs]]
- `supported_by`：GNN-RAG（文档：`ontology/entities/methods/GNN-RAG.md`）：[[../methods/GNN-RAG]]
  - edge_semantics: 引用证据页支撑 GNN-RAG 作为 retrieval-augmented 图检索代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]
- `supported_by`：GCR（文档：`ontology/entities/methods/GCR.md`）：[[../methods/GCR]]
  - edge_semantics: 引用证据页支撑 GCR 作为 grounded reasoning path 代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]
- `supported_by`：EPERM（文档：`ontology/entities/methods/EPERM.md`）：[[../methods/EPERM]]
  - edge_semantics: 引用证据页支撑 EPERM 作为 evidence-path enhanced 代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]
- `supported_by`：ToG（文档：`ontology/entities/methods/ToG.md`）：[[../methods/ToG]]
  - edge_semantics: 引用证据页支撑 ToG 作为 synergy-augmented 代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]
