---
title: WebQSP
problem: [query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [kgqa, multi-hop-qa]
industry: [general]
research_role: [benchmark]
status: processed
---

# WebQSP

## benchmark 定义
WebQSP 是知识库问答领域的经典 benchmark，用于评测方法在真实问题回答上的表现。

## 评测目标
该 benchmark 主要考察方法在知识图谱问答中的答案命中率与整体回答质量。

## 相关任务
当前主要关联 kgqa 与 multi-hop-qa 任务，但本页不直接维护 benchmark 到 task 的 formal relation；这类关联主要通过共享的方法邻接体现，例如某方法既在 WebQSP 上评测，又以这些任务为目标。

## 被哪些方法 / 论文使用
当前知识库中，PathMind 明确在该 benchmark 上进行了评测，并作为 formal `evaluated_on` source 投影到本页。

## 相关场景
当前 benchmark 页面不单独提升稳定场景 formal 邻接。

## 证据来源
- PathMind.experiments：ontology/entities/evidence/PathMind.experiments.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: PathMind.experiments 记录了 WebQSP 上的主要实验结果与效率分析。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：在该基准上评测的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 在 WebQSP 上进行主要性能、效率与可扩展性评测。
  - evidence: [[../evidence/PathMind.experiments]]
