---
title: PathMind.refs
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: refs
venue: AAAI 2026
year: 2026
status: processed
---

# PathMind.refs

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../methods/RoG]]
- [[../methods/GCR]]
- [[../methods/EPERM]]
- [[../methods/GNN-RAG]]

## 本节支撑什么
本缓存支撑 PathMind 与 retrieval-augmented KGR 路线中关键参照方法之间的引用与方法参照关系，包括 RoG、GCR、EPERM 与 GNN-RAG。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Related Work 明确把 RoG、GCR、EPERM 与 GNN-RAG 列为 retrieval-augmented methods 的代表工作。
- 论文使用这些方法作为路线参照与比较基线，但正文并未给出足够强的继承语义把它们提升为严格 `based_on`。
- 论文引用中包含：RoG (Faithful and Interpretable Large Language Model Reasoning on Graphs, ICLR 2024)、GCR (Graph-constrained reasoning, ICLR 2025)、EPERM (An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering, AAAI 2025)、GNN-RAG (Graph neural retrieval for efficient large language model reasoning on knowledge graphs, ACL 2025)。

## 来源说明
- 原始来源：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
- 本缓存主要服务 `cites` 与 `references_method` 的 formal relation 判定。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: PathMind.refs 直接来源于 PathMind 原始 PDF 的 related work 与 references 抽取。
  - evidence: [[PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 的方法参照对象与 related-work 路线定位由 refs 缓存直接支撑。
  - evidence: [[PathMind.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/RoG.md`）：[[../methods/RoG]]
  - edge_semantics: RoG 作为 PathMind 论文中的关键 retrieval-augmented 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[PathMind.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/GCR.md`）：[[../methods/GCR]]
  - edge_semantics: GCR 作为 PathMind 论文中的关键 retrieval-augmented 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[PathMind.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/EPERM.md`）：[[../methods/EPERM]]
  - edge_semantics: EPERM 作为 PathMind 论文中的关键 evidence-path 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[PathMind.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/GNN-RAG.md`）：[[../methods/GNN-RAG]]
  - edge_semantics: GNN-RAG 作为 PathMind 论文中的关键 graph-neural retrieval 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[PathMind.refs]]
