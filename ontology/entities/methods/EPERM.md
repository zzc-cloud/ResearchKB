---
title: EPERM
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa]
industry: [general]
research_role: [foundational]
status: partial
---

# EPERM

## Object semantics
- 一种 evidence path enhanced 知识图谱问答方法，代表 evidence-path 增强路线。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 `references_method` 代表方法引用。

## 最小定义/角色
- 代表 evidence-path 增强设计，用于对照 PathMind 的路径重要性建模与结构化推理方案。

## 待补充
- 正式方法定义、独立 evidence 与更多任务邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 EPERM 作为 evidence path 增强代表方法进行参照与比较。
  - evidence: [[../evidence/PathMind.refs]]
