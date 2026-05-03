---
title: GCR
type: [衍生方法]
parent_methods: [路径导向知识图谱推理]
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [derived]
tags: [grounded reasoning, graph constraints, LLM]
status: stub
---

## 方法定义
一种利用图约束生成 grounded reasoning paths，以提升知识图谱推理忠实性的方法。

## 解决的核心问题
GCR 通过将图结构约束引入推理路径生成过程，减少语言模型在知识图谱推理中的自由漂移与错误跳转。

## 技术原理
GCR 强调 grounded reasoning path 的生成与约束，使推理过程既遵守图结构连接关系，又保留语言模型的语义表达能力。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：以 grounded 约束提升路径推理的可靠性。
- 对后续工作的影响：[[PathMind]] 将其作为 grounded path 方向的关键上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]

## 代表论文
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[GCR]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --applies_to--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --proposes--> [[GCR]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
