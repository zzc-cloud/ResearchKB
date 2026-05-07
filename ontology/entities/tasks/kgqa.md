---
title: KGQA
problem: [query-answering, reasoning]
method_family: [hybrid]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [application]
tags: [知识图谱问答, 研究任务]
---

> 导航：返回 [[index|tasks/index]]；相关对象域 [[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../benchmarks/index|benchmarks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 任务入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 任务定义
以自然语言问题为输入，在知识图谱中定位相关实体、关系与证据路径，并输出答案及其支撑依据的问答任务。

> 本页描述研究任务的目标与难点；对应的 [[知识图谱推理问答]] 用于汇总业务或系统层面的应用场景与方法落点。

## 核心关注点
- 如何将自然语言问题映射到图结构推理过程。
- 如何利用路径、子图与关系约束提高答案忠实性。
- 如何在开放问题表达与结构化图证据之间建立稳定桥梁。

## 相关方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[EPERM]]

## 相关概念
- [[路径优先化]]
- [[重要推理路径]]

## 相关场景
- [[知识图谱推理问答]]

## 相关 benchmark
- [[WebQSP]]
- [[CWQ]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 证据来源 / 关系索引
- 方法映射：[[task_method_map]]
- 证据索引：[[evidence_index]]
- 结构化证据：[[intermediate/papers/PathMind.sections|PathMind.sections]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[重要推理路径]] --supports--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
