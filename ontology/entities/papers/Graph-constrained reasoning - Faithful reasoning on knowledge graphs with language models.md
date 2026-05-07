---
title: Graph-constrained reasoning: Faithful reasoning on knowledge graphs with language models
problem: [reasoning, query-answering]
method_family: [llm, hybrid]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa]
industry: [general]
research_role: [foundational]
tags: [placeholder, cited-work, grounded-reasoning]
status: placeholder
---

> 导航：返回 [[index|papers/index]]；相关对象域 [[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../benchmarks/index|benchmarks/index]]。
>
> 相关 relation ledger：[[../relations/paper_method_links|paper_method_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/citation_graph|citation_graph]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 论文入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与 grounded reasoning 对比对象。

## 核心问题
- 如何在知识图谱推理中通过图约束提升 grounded reasoning 的忠实性。

## 主要贡献
- 提出 graph-constrained reasoning 路线，对显式路径推理施加图结构约束。

## 核心方法
- 对应方法：[[GCR]]

## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

## 应用场景
- [[知识图谱推理问答]]

## 相关基准
- [[WebQSP]]
- [[CWQ]]

## 与知识库其他内容的关联
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 相关方法：[[GCR]]

## 与知识库现有内容的关系
- 相关方法：[[GCR]]
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 关联任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 关联场景：[[知识图谱推理问答]]

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --proposes--> [[GCR]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

## 待补充
- 若后续补到原始论文的专属 Evidence 缓存，可进一步扩充方法细节与实验设定。

