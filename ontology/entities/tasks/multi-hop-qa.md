---
title: multi-hop-qa
problem: [query-answering, reasoning]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [multi-hop-qa]
industry: [general]
research_role: [foundational]
tags: [multi-hop-qa]
status: processed
---

# multi-hop-qa

## Object semantics
- 需要跨越多条关系链整合分散证据后再作答的复杂问答研究任务。

## 任务定义
- 该任务要求系统在多跳证据链中识别关键路径并完成组合推理。

## 核心挑战
- 主要挑战包括组合爆炸、无关路径噪声、推理稳定性与长链解释性。

## 相关方法
- [[../methods/PathMind]]

## 相关概念
- 重要推理路径

## 相关场景
- 知识图谱推理问答

## 相关 benchmark
- CWQ

## 相关论文
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 证据来源 / 关系索引
- [[../evidence/PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 本任务页由实验证据页支撑其多跳推理性能与案例解释。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 重点处理复杂多跳问答中的路径筛选与推理。
  - evidence: [[../evidence/PathMind.experiments]]
- `targets_task`：PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - edge_semantics: 论文强调复杂多跳问答中的重要路径选择。
  - evidence: [[../evidence/PathMind.experiments]]
