---
title: Knowledge Graph Reasoning
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [知识图谱推理, 研究任务]
---

> 导航：返回 [[index|tasks/index]]；相关对象域 [[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../benchmarks/index|benchmarks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 任务入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 任务定义
面向知识图谱中的实体、关系与路径结构，围绕给定查询进行多跳推断、答案定位或缺失知识补全的研究任务。

> 本页描述研究任务本身；与之对应的 [[知识图谱推理问答]] 更强调任务落地时的人机交互、应用约束与系统视角。

## 核心关注点
- 如何在图结构约束下完成忠实推理。
- 如何控制候选路径噪声并识别高价值证据。
- 如何在准确率、可解释性与推理成本之间取得平衡。

## 相关方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[EPERM]]
- [[ToG]]

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
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[重要推理路径]] --supports--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
