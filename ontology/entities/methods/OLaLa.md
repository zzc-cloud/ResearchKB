---
title: OLaLa
type: 集成方法
parent_methods: []
child_methods: []
problem: [ontology-alignment, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# OLaLa

## Object semantics
OLaLa 是一个利用大语言模型进行 ontology matching 的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 OLaLa 纳入 knowledge fusion / ontology matching 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
OLaLa 代表一类把 LLM 用于 ontology matching 与知识融合的命名方法对象。

## 待补充
后续需要独立 ingest OLaLa 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## 代表论文
代表论文为 OLaLa: Ontology Matching with Large Language Models。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/LLM-KG-CPD.analysis.md`）：[[../evidence/LLM-KG-CPD.analysis]]
  - edge_semantics: OLaLa 在该 survey 的结构化 role-based coverage 中被纳入 knowledge fusion / ontology matching 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `surveys_method`：系统覆盖该方法的综述论文（文档：`ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`）：[[../papers/A survey of large language model-augmented knowledge graphs for advanced complex product design]]
  - edge_semantics: 该 survey 将 OLaLa 纳入 knowledge fusion / ontology matching 的结构化方法 coverage，用于组织 LLM 增强知识融合路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
