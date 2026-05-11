---
title: RoG
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# RoG

## Object semantics
- 一种显式推理路径导向的知识图谱推理方法，代表 retrieval-augmented 路线中的 relational path reasoning 方案。

## 当前定位
- 当前作为 PathMind 的稳定上游方法候选被 materialize。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 以强参照语义稳定指向。

## 最小定义/角色
- 该方法在论文中被描述为 planning-retrieval-reasoning framework，用于生成 relational paths，是 PathMind 重点比较的显式路径代表方法。

## 待补充
- 其独立论文页、完整方法定义、实验细节与更广泛的 formal graph 邻接仍待后续单篇 ingest 完成。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.refs（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: 引用证据页支撑 RoG 作为显式 relational path reasoning 的代表方法语义。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 RoG 作为显式 relational path reasoning 的上游代表方法进行路线参照。
  - evidence: [[../evidence/PathMind.refs]]
