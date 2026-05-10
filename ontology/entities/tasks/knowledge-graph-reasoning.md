---
title: knowledge-graph-reasoning
problem: [reasoning]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [kgr, reasoning]
status: processed
---

# knowledge-graph-reasoning

## Object semantics
- 以知识图谱为结构化知识基础，通过关系路径与图结构推断新知识或回答复杂查询的研究任务。

## 任务定义
- 该任务关注如何利用知识图谱中的实体、关系与路径完成结构化推理。

## 核心挑战
- 关键挑战包括噪声路径筛选、复杂多跳搜索、推理忠实性与答案解释性。

## 相关方法
- [[../methods/PathMind]]

## 相关概念
- 路径优先化
- 重要推理路径

## 相关场景
- 知识图谱推理问答

## 相关 benchmark
- WebQSP
- CWQ

## 相关论文
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 证据来源 / 关系索引
- [[../evidence/PathMind.sections]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.sections（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections]]
  - edge_semantics: 本任务页由章节级证据页支撑其问题建模与研究目标。
  - evidence: [[../evidence/PathMind.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 以知识图谱推理为总体任务定位。
  - evidence: [[../evidence/PathMind.sections]]
- `targets_task`：PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - edge_semantics: 论文将知识图谱推理作为核心任务定位。
  - evidence: [[../evidence/PathMind.sections]]
