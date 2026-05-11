---
title: ToG
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# ToG

## Object semantics
- 一种通过 LLM 与知识图谱多轮交互进行路径搜索的 synergy-augmented 知识图谱推理方法。

## 当前定位
- 当前作为 PathMind 的关键参照方法候选被 materialize。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 synergy-augmented 代表方法参照。

## 最小定义/角色
- 论文明确将 ToG 描述为通过 beam search 在 KG 上迭代执行路径探索的代表性 synergy-augmented 方法。

## 待补充
- 其独立论文页、完整方法定义、实验细节与更多 formal 邻接仍待后续单篇 ingest 完成。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.refs（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: 引用证据页支撑 ToG 作为 synergy-augmented 代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 ToG 作为 synergy-augmented 代表方法进行路线比较。
  - evidence: [[../evidence/PathMind.refs]]
