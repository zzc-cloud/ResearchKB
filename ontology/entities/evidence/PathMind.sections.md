---
title: PathMind.sections
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: sections
venue: AAAI
year: 2026
status: processed
---

# PathMind.sections

## Object semantics
- 该证据页承载 PathMind 论文的章节级机制证据，覆盖任务设定、三模块框架、路径优先函数与训练策略。

## 对应正式知识节点
- [[../methods/PathMind|PathMind]]
- [[../concepts/路径优先化|路径优先化]]
- [[../concepts/重要推理路径|重要推理路径]]
- [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]

## 本节支撑什么
- 支撑 PathMind 的 Retrieve-Prioritize-Reason 三阶段框架。
- 支撑路径优先化与重要推理路径两个核心概念。
- 支撑论文和方法对知识图谱推理总任务的定位。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Abstract 与 Introduction 指出两类现有缺陷：等权路径检索会引入噪声，多轮交互式搜索成本过高。
- Methodology 将 PathMind 分为子图检索、路径优先化、知识推理三个模块。
- Path prioritization 通过累计代价与未来代价共同定义路径优先函数，用于选择最重要的推理路径。
- Knowledge reasoning 采用 task-specific instruction tuning 与 path-wise preference alignment 两阶段训练。

## 来源说明
- 来源于 PathMind 原文的首页、相关工作、方法部分与优先化模块。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|PathMind PDF]]
  - edge_semantics: 该 sections 缓存直接抽取自 PathMind 原文的摘要、相关工作与方法章节。
  - evidence: [[PathMind.sections]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: sections 缓存支撑 PathMind 的三模块结构、优先函数与训练策略。
  - evidence: [[PathMind.sections]]
- `supported_by`：被支撑的概念（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化|路径优先化]]
  - edge_semantics: sections 缓存定义了路径优先化及其优先函数。
  - evidence: [[PathMind.sections]]
- `supported_by`：被支撑的概念（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径|重要推理路径]]
  - edge_semantics: sections 缓存解释了重要推理路径如何约束 LLM 推理。
  - evidence: [[PathMind.sections]]
- `supported_by`：被支撑的任务（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - edge_semantics: sections 缓存给出了知识图谱推理任务设定与 PathMind 的任务定位。
  - evidence: [[PathMind.sections]]
