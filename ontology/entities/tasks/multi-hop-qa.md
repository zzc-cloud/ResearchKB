---
title: multi-hop-qa
problem: [query-answering, reasoning]
method_family: [hybrid]
scenario: []
research_task: [multi-hop-qa]
industry: [general]
research_role: [foundational]
tags: [multi-hop-qa]
status: processed
---

# multi-hop-qa

## Object semantics
- multi-hop-qa 是需要跨多条关系链整合证据后回答问题的研究任务，当前由 [[../methods/PathMind|PathMind]] 作为重点能力目标。

## 任务定义
- 该任务要求系统通过多跳路径连接主题实体、关系线索与候选答案。

## 核心挑战
- 关键在于识别正确推理链并避免噪声路径误导答案生成。

## 相关方法
- [[../methods/PathMind|PathMind]]

## 相关概念
- 相关概念包括路径优先化与重要推理路径。

## 相关场景
- 复杂知识图谱问答。

## 相关 benchmark
- 代表 benchmark 包括 CWQ。

## 证据来源 / 关系索引
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：任务证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存支撑复杂多跳问答上的任务表现与案例分析。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：面向该任务的论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文强调其对复杂多跳问答的增益。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `targets_task`：面向该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: PathMind 通过优先关键推理路径来处理多跳问答。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
