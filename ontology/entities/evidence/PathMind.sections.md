---
title: PathMind.sections
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: sections
status: processed
year: 2026
venue: AAAI-26
---

# PathMind.sections

## Object semantics
- PathMind 论文的章节级结构化证据页，承载问题定义、三模块方法设计与主要实验主张的最小可审计摘要。

## 对应正式知识节点
- 该证据页主要支撑 PathMind 方法、PathMind 论文、路径优先化、重要推理路径，以及知识图谱推理相关任务与场景页的最小正式语义。

## 本节支撑什么
- 论文将知识图谱推理建模为 retrieve-prioritize-reason 三阶段流程。
- 核心机制包括子图检索、基于累积代价与未来代价的路径优先化、以及面向路径的两阶段训练。
- 方法面向 knowledge-graph-reasoning、kgqa 与 multi-hop-qa，并在 WebQSP 与 CWQ 上给出主要实验结果。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 问题设定：现有 retrieval-augmented 方法容易无差别抽取路径，synergy-augmented 方法又带来较高交互成本。
- 方法结构：PathMind 由 Subgraph Retrieval、Path Prioritization、Knowledge Reasoning 三部分组成。
- 路径优先化：优先分数由累积代价与未来代价共同决定，用于识别重要推理路径。
- 推理训练：先做 task-specific instruction tuning，再做 path-wise preference alignment。

## 来源说明
- 来源于 PathMind 原始 PDF 的摘要、引言、方法与结论部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：PathMind 原文 PDF（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 该章节级证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind 方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 本页支撑 PathMind 的问题设定、三模块结构与路径优先化机制。
  - evidence: [[PathMind.sections|PathMind.sections]]
- `supported_by`：路径优先化（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化]]
  - edge_semantics: 本页支撑路径优先化的定义、优先函数与其在方法中的角色。
  - evidence: [[PathMind.sections|PathMind.sections]]
- `supported_by`：重要推理路径（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径]]
  - edge_semantics: 本页支撑重要推理路径作为高价值推理证据链的定义与作用。
  - evidence: [[PathMind.sections|PathMind.sections]]
- `supported_by`：knowledge-graph-reasoning（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning]]
  - edge_semantics: 本页支撑该论文对知识图谱推理任务的问题建模与总体目标。
  - evidence: [[PathMind.sections|PathMind.sections]]
- `supported_by`：知识图谱推理问答（文档：`ontology/entities/scenarios/知识图谱推理问答.md`）：[[../scenarios/知识图谱推理问答]]
  - edge_semantics: 本页支撑知识图谱推理问答作为该方法的主要使用场景。
  - evidence: [[PathMind.sections|PathMind.sections]]
