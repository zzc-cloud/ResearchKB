---
title: multi-hop-qa
problem: [query-answering, reasoning]
method_family: [hybrid, llm, gnn]
scenario: []
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

## 相关机制
- 重要推理路径筛选

## 相关场景
- 常见于复杂知识图谱问答应用，但当前论文未给出足以单独 formalize 的稳定 Scenario 对象。

## 相关 benchmark
- CWQ

## 相关论文
- PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## 证据来源 / 关系索引
- [[../evidence/PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 实验证据页支撑复杂多跳问答上的性能与案例分析。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 方法重点处理复杂多跳问答中的重要路径筛选与推理。
  - evidence: [[../evidence/PathMind.experiments]]
