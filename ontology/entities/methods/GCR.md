---
title: GCR
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

# GCR

## Object semantics
GCR 是 retrieval-augmented knowledge graph reasoning 路线中的方法实例，强调 graph-constrained reasoning 与 faithful reasoning。

## 当前定位
该页面由 PathMind 论文中的 related-work 与 baseline 证据稳定支撑，当前作为可正式链接的 partial Method 存在。

## 与知识库现有内容的关系
PathMind 把 GCR 作为关键参照方法与强比较对象之一，用于说明约束式推理路径生成的已有路线。

## 最小定义/角色
GCR 代表一类使用 graph-constrained reasoning 生成推理路径、以支持知识图谱问答的 retrieval-augmented 方法。

## 待补充
后续需要独立 ingest GCR 原论文，以补齐完整方法原理、实验表现与更细粒度任务归属。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: GCR 作为 PathMind 论文中的关键 retrieval-augmented 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：将其作为关键参照的方法（文档：`ontology/entities/methods/PathMind.md`）：[[PathMind]]
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/Graph-constrained reasoning: Faithful reasoning on knowledge graphs with language models.md
  - edge_semantics: PathMind 把 GCR 作为 graph-constrained reasoning 路线中的关键参照方法，而非严格上游谱系来源。
  - evidence: [[../evidence/PathMind.refs]]
