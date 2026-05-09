---
title: CWQ
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [multi-hop-qa, kgqa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, CWQ, multi-hop]
status: processed
---

# CWQ

## Object semantics
- CWQ 是强调复杂多跳问答的 benchmark，当前被 [[../methods/PathMind|PathMind]] 与其代表论文直接用于检验复杂推理能力。

## benchmark 定义
- CWQ 是复杂 WebQuestions 基准，重点检验多跳知识图谱问答能力。

## 评测目标
- 检验方法在复杂多跳问答中的命中率、F1、可解释性与可扩展性。

## 相关任务
- 主要关联 KGQA 与 multi-hop-qa。

## 被哪些方法 / 论文使用
- [[../methods/PathMind|PathMind]]
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]

## 相关场景
- 复杂知识图谱问答。

## 证据来源
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：benchmark 证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存记录了 CWQ 上的主结果、消融和案例分析。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：使用该 benchmark 的论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文在 CWQ 上报告复杂多跳问答的主性能与分析结果。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：使用该 benchmark 的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: PathMind 在 CWQ 上检验复杂多跳问答中的性能、可解释性与扩展性。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
