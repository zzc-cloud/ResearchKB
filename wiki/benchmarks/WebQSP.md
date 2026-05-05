---
title: WebQSP
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa, multi-hop-qa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, KGQA, 多跳问答]
---

> 导航：返回 [[index|benchmarks/index]]；相关对象域 [[../tasks/index|tasks/index]]、[[../methods/index|methods/index]]、[[../papers/index|papers/index]]、[[../scenarios/index|scenarios/index]]。
>
> 相关 relation ledger：[[../relations/benchmark_links|benchmark_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready benchmark 入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 基准定义
面向知识图谱问答的经典评测基准，用于衡量方法在结构化图问答任务中的答案命中率与推理质量。

## 相关任务
- [[kgqa]]
- [[multi-hop-qa]]
- [[knowledge-graph-reasoning]]

## 被哪些方法 / 论文使用
- 方法：[[PathMind]]、[[RoG]]、[[GCR]]、[[EPERM]]
- 论文：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关场景
- [[知识图谱推理问答]]

## 证据来源
- [[evidence_index]]
- [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[RoG]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[EPERM]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
