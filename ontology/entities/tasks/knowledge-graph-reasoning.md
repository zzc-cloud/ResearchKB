---
title: knowledge-graph-reasoning
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [KGR, reasoning]
status: processed
---

# knowledge-graph-reasoning

## Object semantics
- knowledge-graph-reasoning 是在知识图谱上进行逻辑推断或结构化问答的核心研究任务，当前由 [[../methods/PathMind|PathMind]] 等方法直接面向。

## 任务定义
- 该任务关注如何利用知识图谱中的实体、关系与结构信息推断答案或新知识。

## 核心挑战
- 搜索空间大、路径噪声多、推理链选择困难，且 LLM 与 KG 的协同成本较高。

## 相关方法
- [[../methods/PathMind|PathMind]]

## 相关概念
- 相关概念包括路径优先化与重要推理路径。

## 相关场景
- 一般性 KGQA 与复杂多跳问答。

## 相关 benchmark
- 代表 benchmark 包括 WebQSP 与 CWQ。

## 证据来源 / 关系索引
- [[../evidence/PathMind.sections|PathMind.sections]]
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：任务证据（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections|PathMind.sections]]
  - edge_semantics: sections 缓存给出知识图谱推理任务设定与 PathMind 的任务定位。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `supported_by`：任务证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存补充了该任务在标准 benchmark 上的性能与效率表现。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：面向该任务的论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文将知识图谱推理作为总任务设定。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `targets_task`：面向该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: PathMind 直接面向知识图谱推理总任务。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
