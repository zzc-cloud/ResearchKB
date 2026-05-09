---
title: PathMind.refs
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: refs
venue: AAAI
year: 2026
status: processed
---

# PathMind.refs

## Object semantics
- 该证据页承载 PathMind 论文的关键引用、路线定位与上游方法 grounding 证据。

## 对应正式知识节点
- [[../methods/PathMind|PathMind]]

## 本节支撑什么
- 支撑 PathMind 与 RoG、GCR、EPERM、ToG 等方法路线的关系定位。
- 支撑论文的 cites 边与方法的 based_on 边。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Related Work 将 LLM-based KGR 分为 retrieval-augmented 与 synergy-augmented 两条主线。
- 论文明确把 RoG、GCR、EPERM 归在 retrieval-augmented 相关工作中，把 ToG 归在 synergy-augmented 相关工作中。
- 参考文献给出上述代表工作的正式题名与发表场所。

## 来源说明
- 来源于 Related Work、Experiments 的 baseline 列表与 References 页。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|PathMind PDF]]
  - edge_semantics: 该 refs 缓存抽取自 Related Work、baseline 列表与 References 页。
  - evidence: [[PathMind.refs]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: refs 缓存支撑 PathMind 的上游路线定位与关键引用关系。
  - evidence: [[PathMind.refs]]
