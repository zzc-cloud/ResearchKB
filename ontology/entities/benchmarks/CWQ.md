---
title: CWQ
problem: [query-answering]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [kgqa, multi-hop-qa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, kgqa, multi-hop-qa]
status: processed
---

# CWQ

## Object semantics
- 面向复杂多跳知识图谱问答的标准 benchmark，用于评测方法在组合推理场景中的命中率与 F1 表现。

## benchmark 定义
- CWQ 是 PathMind 用于评测复杂多跳推理能力的两个主要基准之一。

## 评测目标
- 评估方法在复杂问答与多跳推理场景中的性能与稳健性。

## 相关任务
- kgqa
- multi-hop-qa

## 被哪些方法 / 论文使用
- [[../methods/PathMind]]
- PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## 相关场景
- 知识图谱推理问答

## 证据来源
- [[../evidence/PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 实验证据页支撑 CWQ 作为 PathMind 主要多跳评测基准。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 在 CWQ 上取得最优结果。
  - evidence: [[../evidence/PathMind.experiments]]
