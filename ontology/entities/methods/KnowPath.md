---
title: KnowPath
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# KnowPath

## Object semantics
- 一种利用 LLM 生成推理路径的知识图谱推理方法，代表生成式 inference-path 路线。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 `references_method` 的生成式路径代表方法引用。

## 最小定义/角色
- 代表生成式推理路径方法，用于对照 PathMind 的显式路径优先化设计。

## 待补充
- 正式方法定义、独立 evidence 与更多方法邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 KnowPath 作为 LLM 生成推理路径方向代表方法进行参照。
  - evidence: [[../evidence/PathMind.refs]]
