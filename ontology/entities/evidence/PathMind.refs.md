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
- PathMind 论文的引用与上游路线证据页，承载代表方法、对比基线与方法谱系定位的最小可审计摘要。

## 对应正式知识节点
- 该证据页主要支撑 PathMind 与上游代表工作的 cites 关系，以及 PathMind 相对 RoG 的方法演化定位。

## 本节支撑什么
- 论文将已有 LLM-based KGR 方法划分为 retrieval-augmented 与 synergy-augmented 两大路线。
- RoG、GCR、EPERM 被作为 retrieval-augmented 代表方法讨论。
- ToG 被作为 synergy-augmented 代表方法讨论。
- 参考文献页为 cites 账本与上游工作占位论文页提供可回查来源。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- retrieval-augmented 代表：RoG、GCR、EPERM、GNN-RAG。
- synergy-augmented 代表：ToG、KnowPath。
- PathMind 强调对已有推理路径路线的继承，同时通过路径优先化与偏好对齐减少噪声与交互开销。

## 来源说明
- 来源于 PathMind 原始 PDF 的 Related Work、Baselines 与 References 部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：PathMind 原文 PDF（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 该引用证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 本页支撑 PathMind 的上游路线定位与基线对比关系。
  - evidence: [[PathMind.refs|PathMind.refs]]
