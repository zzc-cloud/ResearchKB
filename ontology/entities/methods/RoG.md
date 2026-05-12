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
RoG 是 retrieval-augmented knowledge graph reasoning 路线中的方法实例，强调 faithful and interpretable graph reasoning。

## 当前定位
该页面由 PathMind 论文中的 related-work 与 baseline 证据稳定支撑，当前作为可正式链接的 partial Method 存在。

## 与知识库现有内容的关系
PathMind 把 RoG 作为关键参照方法与强比较对象之一，用于界定重要路径识别相对传统路径检索的增量价值。

## 最小定义/角色
RoG 代表一类显式利用图上推理路径来支持 LLM 推理的 retrieval-augmented KGR 方法。

## 待补充
后续需要独立 ingest RoG 原论文，以补齐完整方法原理、实验表现与更细粒度任务归属。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: RoG 作为 PathMind 论文中的关键 retrieval-augmented 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：将其作为关键参照的方法（文档：`ontology/entities/methods/PathMind.md`）：[[PathMind]]
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/RoG: Faithful and Interpretable Large Language Model Reasoning on Graphs.md
  - edge_semantics: PathMind 把 RoG 作为 retrieval-augmented KGR 路线中的关键参照与强比较对象，用于凸显重要路径识别的增量价值。
  - evidence: [[../evidence/PathMind.refs]]
