---
title: ToG
type: [衍生方法]
parent_methods: [协同增强式知识图谱推理]
child_methods: []
problem: [reasoning, query-answering]
method_family: [llm, hybrid]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [derived]
tags: [synergy-augmented, 多轮搜索, LLM]
status: stub
---

> 导航：返回 [[index|methods/index]]；相关对象域 [[../tasks/index|tasks/index]]、[[../concepts/index|concepts/index]]、[[../benchmarks/index|benchmarks/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/method_evolution|method_evolution]]、[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/paper_method_links|paper_method_links]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 方法入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 方法定义
一种通过 LLM 在知识图谱上迭代执行 beam search 以发现推理路径的协同增强式方法。

## 解决的核心问题
ToG 通过多轮交互式搜索提升复杂知识图谱问答中的深层路径发现能力。

## 技术原理
ToG 让语言模型与知识图谱进行多轮协同，逐步扩展、筛选并利用候选推理路径，以提升复杂问题下的搜索覆盖率。

## 方法演化位置
- 上游方法：[[协同增强式知识图谱推理]]
- 路线改进：通过多轮 LLM 交互与迭代搜索推进协同增强路线。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[multi-hop-qa]]
- 评测基准：[[CWQ]]

## 代表论文
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[ToG]] --based_on--> [[协同增强式知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --improves_on--> [[协同增强式知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[ToG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

### Incoming
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --proposes--> [[ToG]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
