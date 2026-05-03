---
title: RoG
type: [衍生方法]
parent_methods: [路径导向知识图谱推理]
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [derived]
tags: [路径生成, faithful reasoning, LLM]
status: stub
---

## 方法定义
一种显式生成关系推理路径以支持知识图谱忠实推理的方法。

## 解决的核心问题
RoG 通过把关系路径显式建模为中间推理结构，提升知识图谱推理的忠实性与可解释性。

## 技术原理
RoG 先围绕问题构造可候选的关系推理路径，再让语言模型沿显式路径完成推理与答案生成，从而避免完全隐式的黑箱推断。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：将关系路径作为中间推理结构显式生成。
- 对后续工作的影响：[[PathMind]] 将其作为路径导向基线和上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]

## 代表论文
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]

## Formal relations
### Outgoing
- `[[RoG]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- 无
