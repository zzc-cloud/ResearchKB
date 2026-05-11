---
title: kgqa
problem: [query-answering]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [kgqa]
industry: [general]
research_role: [foundational]
tags: [kgqa]
status: processed
---

# kgqa

## Object semantics
- 以知识图谱为知识源，通过结构化检索与推理回答自然语言问题的研究任务。

## 任务定义
- 该任务关注如何从知识图谱中检索相关结构并生成正确答案。

## 核心挑战
- 关键挑战包括问题解析、候选路径筛选、多跳推理与答案忠实性。

## 相关方法
- [[../methods/PathMind]]

## 相关机制
- 高价值推理路径筛选

## 相关场景
- 企业知识图谱问答

## 相关 benchmark
- WebQSP
- CWQ

## 相关论文
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 证据来源 / 关系索引
- [[../evidence/PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 本任务页由实验证据页支撑其问答性能与任务适配性。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 在知识图谱问答任务中被验证。
  - evidence: [[../evidence/PathMind.experiments]]
- `targets_task`：PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - edge_semantics: 论文在知识图谱问答场景中验证方法有效性。
  - evidence: [[../evidence/PathMind.experiments]]
