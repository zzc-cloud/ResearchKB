---
title: ToG
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

# ToG

## Object semantics
- 一种通过 LLM 与知识图谱多轮交互进行路径搜索的 synergy-augmented 知识图谱推理方法。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 `references_method` 的协同增强路线代表方法引用。

## 最小定义/角色
- 代表多轮交互式推理路线，用于对照 PathMind 对低交互成本结构化推理的设计。

## 待补充
- 正式方法定义、独立 evidence 与完整 benchmark 邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 ToG 作为 synergy-augmented 代表方法进行路线比较。
  - evidence: [[../evidence/PathMind.refs]]
