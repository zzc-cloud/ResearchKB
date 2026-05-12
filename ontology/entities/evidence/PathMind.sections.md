---
title: PathMind.sections
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: sections
venue: AAAI 2026
year: 2026
status: processed
---

# PathMind.sections

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../tasks/knowledge-graph-reasoning]]
- [[../tasks/kgqa]]
- [[../tasks/multi-hop-qa]]

## 本节支撑什么
本缓存支撑 PathMind 的方法定义、三段式框架结构、路径优先级机制，以及其面向 knowledge-graph-reasoning / kgqa / multi-hop-qa 的任务定位。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 论文把现有 LLM-based KGR 路线分为 retrieval-augmented 与 synergy-augmented 两类，并指出前者容易引入路径噪声，后者存在较高检索与 LLM 调用成本。
- PathMind 的核心架构由三个组件构成：Subgraph Retrieval、Path Prioritization、Knowledge Reasoning。
- 路径优先级函数同时建模累计代价 $d(q,e)$ 与未来代价 $f(e,a)$，用来识别重要推理路径，而不是无差别展开所有路径。
- 知识推理阶段采用两阶段训练：task-specific instruction tuning 与 path-wise preference alignment，以提升答案正确性与逻辑一致性。
- 论文明确将方法定位在 KG reasoning、KGQA 与多跳复杂问答场景。

## 来源说明
- 原始来源：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
- 对应正式论文页中的方法、任务与 benchmark 结论均可回查至本缓存。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: PathMind.sections 直接来源于 PathMind 原始 PDF 的章节与方法内容抽取。
  - evidence: [[PathMind.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 的方法定义、三段式框架与路径优先级机制由 sections 缓存直接支撑。
  - evidence: [[PathMind.sections]]
- `supported_by`：被该证据支撑的任务（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning]]
  - edge_semantics: PathMind 明确把其任务定位为知识图谱推理，本任务页由 sections 缓存支撑。
  - evidence: [[PathMind.sections]]
- `supported_by`：被该证据支撑的任务（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa]]
  - edge_semantics: PathMind 在知识图谱问答任务框架中提出并评估，本任务页由 sections 缓存支撑。
  - evidence: [[PathMind.sections]]
- `supported_by`：被该证据支撑的任务（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa]]
  - edge_semantics: PathMind 在方法定义层面明确覆盖复杂多跳问答任务，本任务页由 sections 缓存支撑。
  - evidence: [[PathMind.sections]]
