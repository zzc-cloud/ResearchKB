---
title: PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
authors: [Yu Liu, Xixun Lin, Yanmin Shang, Yangxi Li, Shi Wang, Yanan Cao]
year: 2026
venue: AAAI-26
problem: [reasoning, query-answering]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
tags: [PathMind, knowledge-graph-reasoning, kgqa, llm, reasoning-path]
status: processed
---

# PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## Object semantics
- 一篇提出 PathMind 框架的 AAAI 2026 方法论文，核心贡献是以 retrieve-prioritize-reason 范式提升知识图谱推理中的忠实性、可解释性与效率。

## 核心问题
- 现有 retrieval-augmented KGR 方法容易无差别引入噪声路径，synergy-augmented 方法则常带来更高的搜索与交互开销。

## 主要贡献
- 提出 PathMind 框架，将 KGR 划分为子图检索、路径优先化与知识推理三个阶段。
- 设计同时考虑累积代价与未来代价的路径优先函数，用于识别重要推理路径。
- 通过 task-specific instruction tuning 与 path-wise preference alignment 提升回答质量与逻辑一致性。

## 核心方法
- 论文提出 [[../methods/PathMind]] 方法，并显式使用 [[../concepts/路径优先化]] 与 [[../concepts/重要推理路径]] 两个核心概念。

## 相关任务
- 论文主要面向 [[../tasks/knowledge-graph-reasoning]]、[[../tasks/kgqa]] 与 [[../tasks/multi-hop-qa]]。

## 应用场景
- 论文以知识图谱推理问答作为主要研究场景。

## 相关基准
- 论文在 WebQSP 与 CWQ 上验证效果。

## 关键结论
- PathMind 在 WebQSP 与 CWQ 上均优于主要基线，并以更少输入 token 保持高质量推理。

## 引用了哪些重要工作
- 论文将 [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]、[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]、[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]、[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]、[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] 与 [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]] 作为关键相关工作。

## 被哪些论文引用（已知）
- 暂无。

## 与知识库其他内容的关联
- 该论文为 [[../methods/PathMind]] 提供提出关系与方法语义真源，并为路径优先化、重要推理路径与知识图谱推理任务提供正式支撑。

## 证据来源
- PathMind.sections
- PathMind.refs
- PathMind.experiments

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `proposes`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 论文提出 PathMind 作为 retrieve-prioritize-reason 的知识图谱推理框架。
  - evidence: [[../evidence/PathMind.sections]]
- `targets_task`：knowledge-graph-reasoning（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning]]
  - edge_semantics: 论文将知识图谱推理作为核心任务定位。
  - evidence: [[../evidence/PathMind.sections]]
- `targets_task`：kgqa（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa]]
  - edge_semantics: 论文在知识图谱问答场景中验证方法有效性。
  - evidence: [[../evidence/PathMind.experiments]]
- `targets_task`：multi-hop-qa（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa]]
  - edge_semantics: 论文强调复杂多跳问答中的重要路径选择。
  - evidence: [[../evidence/PathMind.experiments]]
- `uses_concept`：路径优先化（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化]]
  - edge_semantics: 论文将路径优先化作为核心机制，用于识别高价值推理路径。
  - evidence: [[../evidence/PathMind.sections]]
- `uses_concept`：重要推理路径（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径]]
  - edge_semantics: 论文以重要推理路径作为结构化推理与解释的关键对象。
  - evidence: [[../evidence/PathMind.sections]]
- `cites`：Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning（文档：`ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`）：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
  - edge_semantics: 作为 retrieval-augmented 路线中的显式推理路径代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models（文档：`ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`）：[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
  - edge_semantics: 作为 grounded reasoning path 代表方法被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering（文档：`ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`）：[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
  - edge_semantics: 作为 evidence path 增强的代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs（文档：`ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`）：[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
  - edge_semantics: 作为图检索增强代表方法被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation（文档：`ontology/entities/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`）：[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
  - edge_semantics: 作为 synergy-augmented 路线代表方法被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs（文档：`ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`）：[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
  - edge_semantics: 作为 LLM 生成推理路径方向的近期工作被引用。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
