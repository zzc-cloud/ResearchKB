---
title: EPERM
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

# EPERM

## Object semantics
EPERM 是 retrieval-augmented knowledge graph reasoning 路线中的方法实例，强调 evidence path enhanced reasoning。

## 当前定位
该页面由 PathMind 论文中的 related-work 与 baseline 证据稳定支撑，当前作为可正式链接的 partial Method 存在。

## 与知识库现有内容的关系
PathMind 把 EPERM 作为关键参照方法与强比较对象之一，用于比较重要路径识别与证据路径增强推理的差异。

## 最小定义/角色
EPERM 代表一类围绕 evidence path selection 与 reasoning enhancement 设计的知识图谱问答方法。

## 待补充
后续需要独立 ingest EPERM 原论文，以补齐完整方法原理、实验表现与更细粒度任务归属。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: EPERM 作为 PathMind 论文中的关键 evidence-path 参照方法，由 refs 缓存中的 related-work 与 citation 证据支撑。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：将其作为关键参照的方法（文档：`ontology/entities/methods/PathMind.md`）：[[PathMind]]
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md
  - edge_semantics: PathMind 把 EPERM 作为 evidence-path enhanced reasoning 路线中的关键比较方法与借鉴对象。
  - evidence: [[../evidence/PathMind.refs]]
