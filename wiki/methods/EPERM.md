---
title: EPERM
type: [衍生方法]
parent_methods: [路径导向知识图谱推理]
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [derived]
tags: [evidence path, 知识图谱问答]
status: stub
---

## 方法定义
一种通过增强证据路径来改进知识图谱问答推理的方法。

## 解决的核心问题
EPERM 通过强调证据路径的显式构造与利用，改善知识图谱问答中的证据支撑质量。

## 技术原理
EPERM 将答案推理建立在 evidence path 之上，通过增强路径级证据表示来提升问答过程的可靠性与可解释性。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：通过证据路径增强改进路径导向推理。
- 对后续工作的影响：[[PathMind]] 将其作为 evidence path 方向的关键上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]

## 代表论文
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[EPERM]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[EPERM]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

### Incoming
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --proposes--> [[EPERM]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
