---
title: kgqa
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [foundational]
tags: [KGQA]
status: processed
---

# kgqa

## Object semantics
- kgqa 是基于知识图谱回答自然语言问题的研究任务，当前由 [[../methods/PathMind|PathMind]] 在标准 benchmark 上直接评估。

## 任务定义
- KGQA 关注如何把自然语言问题映射为知识图谱上的可回答推理过程。

## 核心挑战
- 需要兼顾实体链接、路径发现、关系组合与答案选择。

## 相关方法
- [[../methods/PathMind|PathMind]]

## 相关概念
- 相关概念包括路径优先化与重要推理路径。

## 相关场景
- 一般性知识图谱问答。

## 相关 benchmark
- 代表 benchmark 包括 WebQSP 与 CWQ。

## 证据来源 / 关系索引
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：任务证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存支撑 KGQA benchmark 上的任务表现与比较结果。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：面向该任务的论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文在 KGQA benchmark 上验证其方法表现。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `targets_task`：面向该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: PathMind 用于知识图谱问答中的结构化多跳推理。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
