---
title: RoG
type: 基础方法
parent_methods: []
child_methods: [PathMind]
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# RoG

## Object semantics
- 一种显式推理路径导向的知识图谱推理方法，代表 retrieval-augmented 路线中的关系路径推理方案。

## 当前定位
- 当前作为 PathMind 的严格上游演化方法。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 `based_on` 上游方法引用。

## 最小定义/角色
- 代表显式路径推理路线，为 PathMind 的路径优先化扩展提供上游方法基础。

## 待补充
- 正式方法定义、独立 evidence 与更多邻接方法页。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `based_on`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 延续显式推理路径路线，并在其上加入路径优先化与偏好对齐机制。
  - evidence: [[../evidence/PathMind.refs]]
