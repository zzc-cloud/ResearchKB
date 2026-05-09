---
title: WebQSP
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, KGQA]
status: processed
---

# WebQSP

## Object semantics
- WebQSP 是用于评估知识图谱问答方法的 benchmark，当前被 [[../methods/PathMind|PathMind]] 与其代表论文直接用于性能和效率评测。

## benchmark 定义
- WebQSP 是知识图谱问答常用评测集，用于衡量问答准确率与 F1。

## 评测目标
- 检验方法在结构化问答上的命中率、答案覆盖与推理效率。

## 相关任务
- 主要面向 KGQA。

## 被哪些方法 / 论文使用
- [[../methods/PathMind|PathMind]]
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]

## 相关场景
- 一般性知识图谱问答。

## 证据来源
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：benchmark 证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存记录了 WebQSP 上的主结果与效率比较。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：使用该 benchmark 的论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文在 WebQSP 上报告主性能与效率结果。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：使用该 benchmark 的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: PathMind 在 WebQSP 上评估准确率、F1、调用次数和 token 开销。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
