---
title: GNN-RAG
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm, gnn]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# GNN-RAG

## Object semantics
- 一种以图神经检索为核心的 retrieval-augmented 知识图谱推理方法，用于在 topic entities 与答案候选之间检索最短路径。

## 当前定位
- 当前作为 PathMind 的关键参照方法候选被 materialize。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 retrieval-augmented 代表方法参照。

## 最小定义/角色
- 论文明确把 GNN-RAG 放入 retrieval-augmented 代表方法集合，并用它作为 PathMind 在 CWQ 上的重要强基线对照。

## 待补充
- 其独立论文页、完整方法定义、实验设置与更多 formal relation 仍待后续单篇 ingest 完成。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.refs（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: 引用证据页支撑 GNN-RAG 作为 retrieval-augmented 图检索代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - evidence: [[../evidence/PathMind.refs]]
