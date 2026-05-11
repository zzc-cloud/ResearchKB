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
- PathMind 论文的章节级结构化证据页，承载问题设定、三阶段方法结构与核心机制的最小可审计摘要。

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../tasks/knowledge-graph-reasoning]]

## 本节支撑什么
- 论文将 LLM-based KGR 的主要瓶颈归纳为无差别路径检索噪声与多轮交互成本。
- PathMind 采用 Retrieve-Prioritize-Reason 三阶段框架，将子图检索、路径优先化与知识推理串联起来。
- Path prioritization 以累积代价和未来代价共同建模重要推理路径。
- Knowledge reasoning 通过 task-specific instruction tuning 与 path-wise preference alignment 提升答案准确性与逻辑一致性。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Abstract 与 Introduction 明确提出：现有 retrieval-augmented 方法常把不重要路径一并输入 LLM，而 synergy-augmented 方法通常带来更高的搜索与调用开销。
- Figure 2 与 Methodology 给出三模块结构：Subgraph Retrieval、Path Prioritization、Knowledge Reasoning。
- 路径优先分数由 $d(q, e)$ 与 $f(e, a)$ 共同决定，用于优先选择对推理最关键的路径。
- 论文把知识图谱推理表述为结构化 reasoning task，并在后续实验中用 WebQSP 与 CWQ 验证其问答与多跳能力。

## 来源说明
- 来源于原始 PDF 的 Abstract、Introduction、Related Work、Methodology 与 Conclusion 部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 章节级证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../evidence/PathMind.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 章节级证据页支撑 PathMind 的问题设定、三阶段结构与核心机制。
  - evidence: [[../evidence/PathMind.sections]]
- `supported_by`：knowledge-graph-reasoning（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning]]
  - edge_semantics: 章节级证据页支撑该任务在论文中的问题建模与研究目标。
  - evidence: [[../evidence/PathMind.sections]]
