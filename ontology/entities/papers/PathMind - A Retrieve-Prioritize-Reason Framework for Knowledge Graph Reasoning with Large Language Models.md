---
title: PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
authors: [Yu Liu, Xixun Lin, Yanmin Shang, Yangxi Li, Shi Wang, Yanan Cao]
year: 2026
venue: AAAI-26
problem: [reasoning, query-answering]
method_family: [hybrid, llm, gnn]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
tags: [PathMind, knowledge-graph-reasoning, kgqa, reasoning-path]
status: processed
---

# PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## Object semantics
- 一篇提出 PathMind 框架的 AAAI 2026 方法论文，核心贡献是通过重要推理路径优先化提升知识图谱推理中的忠实性、可解释性与效率。

## 核心问题
- 现有 retrieval-augmented 路线常无差别抽取路径，把不重要甚至误导性的路径一并输入 LLM。
- 现有 synergy-augmented 路线虽然能动态探索路径，但通常需要更大搜索空间与多次 LLM 调用。

## 主要贡献
- 提出 PathMind，将知识图谱推理组织为 Retrieve-Prioritize-Reason 三阶段流程。
- 设计语义感知的 path priority function，同时建模 accumulative cost 与 estimated future cost 以识别重要推理路径。
- 采用 task-specific instruction tuning 与 path-wise preference alignment 两阶段训练，使 LLM 更稳定地利用结构化推理路径。

## 核心方法
- 论文提出 [[../methods/PathMind]]，把 query subgraph retrieval、path prioritization 与 knowledge reasoning 串联为可复用方法框架。

## 相关任务
- knowledge-graph-reasoning
- kgqa
- multi-hop-qa

## 应用场景
- 论文强调知识图谱问答与复杂推理应用，但未给出足以稳定 materialize 为正式 Scenario 页的单一应用场景实例。

## 相关基准
- WebQSP
- CWQ

## 关键结论
- PathMind 在 WebQSP 与 CWQ 上均优于主要对比基线。
- WebQSP 上相对第二名 EPERM 有约 0.8% 的 Hits@1 提升。
- CWQ 上相对 GNN-RAG 有约 5.1% 的 Hits@1 与 3.9% 的 F1 提升。
- 路径优先化、alignment 与训练步骤都对性能有显著贡献。
- 在 WebQSP 上，PathMind 用一次 LLM 调用和较少输入 token 就实现了较好的性能/效率平衡。

## 引用了哪些重要工作
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
- [[Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph]]
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
- [[LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph]]
- [[Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation]]
- [[Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering]]
- [[Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models]]

## 被哪些论文引用（已知）
- 暂无。

## 与知识库其他内容的关联
- 该论文为 [[../methods/PathMind]] 提供提出关系与方法语义真源。
- 它也为知识图谱推理、知识图谱问答、多跳问答以及 WebQSP / CWQ 两个 benchmark 提供直接证据锚点。

## 证据来源
- PathMind.sections
- PathMind.refs
- PathMind.experiments

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `proposes`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 论文正式提出 PathMind 作为 retrieve-prioritize-reason 的知识图谱推理框架。
  - evidence: [[../evidence/PathMind.sections]]
- `cites`：Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning（文档：`ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`）：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
  - edge_semantics: 作为显式 relational path reasoning 的代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models（文档：`ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`）：[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
  - edge_semantics: 作为 grounded reasoning path 代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs（文档：`ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`）：[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
  - edge_semantics: 作为 retrieval-augmented 图检索代表方法被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering（文档：`ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`）：[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
  - edge_semantics: 作为 evidence-path enhanced 代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation（文档：`ontology/entities/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`）：[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
  - edge_semantics: 作为进一步扩展的 synergy-augmented 路线工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph（文档：`ontology/entities/papers/Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph.md`）：[[Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph]]
  - edge_semantics: 作为 ToG 论文的正式引用被纳入 citations。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs（文档：`ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`）：[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
  - edge_semantics: 作为 LLM-generated inference paths 的近期工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph（文档：`ontology/entities/papers/LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph.md`）：[[LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph]]
  - edge_semantics: 作为 retrieval-augmented 轻量推理基线被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation（文档：`ontology/entities/papers/Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation.md`）：[[Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation]]
  - edge_semantics: 作为 graph-based retrieval-augmented generation 的相关工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering（文档：`ontology/entities/papers/Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering.md`）：[[Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering]]
  - edge_semantics: 作为结构查询执行式知识库问答方法被引用。
  - evidence: [[../evidence/PathMind.refs]]
- `cites`：Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models（文档：`ontology/entities/papers/Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models.md`）：[[Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models]]
  - edge_semantics: 作为早期 structural query generation 路线工作被引用。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无

## 我的批注
- 这篇论文结构规整，是标准 empirical method paper，适合走 sections / refs / experiments 最小缓存集合。
