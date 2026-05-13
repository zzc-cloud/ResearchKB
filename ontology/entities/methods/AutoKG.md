---
title: AutoKG
type: 集成方法
parent_methods: []
child_methods: []
problem: [graph-construction, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# AutoKG

## Object semantics
AutoKG 是一个面向知识图谱自动生成的 LLM-enhanced Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 AutoKG 纳入 LLM 增强 KG construction 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
AutoKG 代表一类把知识图谱生成过程自动化的命名方法对象。

## 待补充
后续需要独立 ingest AutoKG 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## 代表论文
代表论文为 AutoKG: Efficient Automated Knowledge Graph Generation for Language Models。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/LLM-KG-CPD.refs.md`）：[[../evidence/LLM-KG-CPD.refs]]
  - edge_semantics: AutoKG 在该 survey 中被纳入 LLM 增强 KG construction 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `surveys_method`：系统覆盖该方法的综述论文（文档：`ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`）：[[../papers/A survey of large language model-augmented knowledge graphs for advanced complex product design]]
  - edge_semantics: 该 survey 将 AutoKG 纳入 LLM 增强 KG construction 的结构化方法 coverage，用于组织复杂产品设计中的知识图谱自动生成路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]
