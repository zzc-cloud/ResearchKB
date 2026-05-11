---
title: WebQSP
problem: [query-answering]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [kgqa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, kgqa]
status: processed
---

# WebQSP

## Object semantics
- 面向知识图谱问答的标准 benchmark，用于评测方法在结构化问答中的正确率与覆盖表现。

## benchmark 定义
- WebQSP 是 PathMind 用于评测知识图谱问答能力的两个主要基准之一。

## 评测目标
- 评估方法在知识图谱问答任务上的 answer hit 与 F1 表现。

## 相关任务
- kgqa

## 被哪些方法 / 论文使用
- [[../methods/PathMind]]
- PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## 相关场景
- 企业知识图谱问答

## 证据来源
- [[../evidence/PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 实验证据页支撑 WebQSP 作为 PathMind 评测基准之一。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 在 WebQSP 上取得最优结果。
  - evidence: [[../evidence/PathMind.experiments]]
