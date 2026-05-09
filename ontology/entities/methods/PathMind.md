---
title: PathMind
type: [集成方法]
parent_methods: [RoG]
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm, gnn]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [integrated]
tags: [PathMind, KGR, KGQA, reasoning-path]
status: processed
---

# PathMind

## Object semantics
- PathMind 是一个面向 [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]] 的 retrieve-prioritize-reason 集成方法，用于先检索子图、再识别关键路径、最后引导 LLM 推理。

## 方法定义
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]] 提出的该方法，通过路径优先化把更关键的证据路径显式提供给 LLM。

## 解决的核心问题
- 在 [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]] 与 [[../tasks/multi-hop-qa|multi-hop-qa]] 中，等权路径检索容易引入噪声，而多轮 agent 搜索又代价较高。

## 技术原理
- 方法先从查询相关子图中检索候选路径，再通过 [[../concepts/路径优先化|路径优先化]] 识别 [[../concepts/重要推理路径|重要推理路径]]，最后把这些路径作为推理输入交给 LLM。

## 方法演化位置
- PathMind 延续了 [[RoG]] 的显式路径推理思路；对于 [[GCR]] 与 [[EPERM]]，当前更适合作为关键比较与借鉴路线，而不是严格的父方法链。

## 应用场景
- 主要用于一般性的知识图谱问答与复杂多跳推理场景。

## 代表论文
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]

## 相关概念
- [[../concepts/路径优先化|路径优先化]]
- [[../concepts/重要推理路径|重要推理路径]]

## 证据来源
- [[../evidence/PathMind.sections|PathMind.sections]]
- [[../evidence/PathMind.refs|PathMind.refs]]
- [[../evidence/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `based_on`：上游方法（文档：`ontology/entities/methods/RoG.md`）：[[RoG]]
  - edge_semantics: PathMind 延续了显式关系路径驱动推理的 retrieval-augmented 路线。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `references_method`：比较 / 借鉴方法（文档：`ontology/entities/methods/GCR.md`）：[[GCR]]
  - edge_semantics: PathMind 将 GCR 作为可靠路径生成路线的重要比较与借鉴对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `references_method`：比较 / 借鉴方法（文档：`ontology/entities/methods/EPERM.md`）：[[EPERM]]
  - edge_semantics: PathMind 将 EPERM 作为 evidence-path 增强路线的重要比较与借鉴对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `uses_concept`：核心概念（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化|路径优先化]]
  - edge_semantics: 方法把路径优先化作为从查询子图中识别高价值路径的显式决策机制。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `uses_concept`：核心概念（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径|重要推理路径]]
  - edge_semantics: 方法将重要推理路径视为用于约束 LLM 推理的关键中间产物。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - edge_semantics: PathMind 面向知识图谱推理总任务。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
  - edge_semantics: PathMind 在 KGQA benchmark 上回答结构化问答查询。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa|multi-hop-qa]]
  - edge_semantics: PathMind 重点处理依赖多跳关系链的复杂问答。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]
  - edge_semantics: PathMind 在 WebQSP 上评估准确率、F1、调用次数和 token 开销。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ|CWQ]]
  - edge_semantics: PathMind 在 CWQ 上评估复杂多跳问答中的性能、可解释性与可扩展性。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `supported_by`：机制证据（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections|PathMind.sections]]
  - edge_semantics: sections 缓存支撑 PathMind 的三模块结构、优先函数与训练策略。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `supported_by`：引用证据（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs|PathMind.refs]]
  - edge_semantics: refs 缓存支撑 PathMind 的路线定位、上游方法比较与关键引用关系。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `supported_by`：实验证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]
  - edge_semantics: experiments 缓存支撑 PathMind 的主结果、消融、可扩展性与效率结论。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `proposes`：提出论文（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]
  - edge_semantics: 论文把 PathMind 命名并定义为核心方法产物。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]

## 优势与局限
- 相比等权 retrieval 路线，它能更聚焦关键推理路径；相比多轮搜索路线，它显著降低 LLM 调用成本。
- 该方法仍依赖查询子图质量与路径优先函数学习质量。

## 与其他方法的对比
- 相较基于路径检索的上游方法，它更强调路径重要性建模；相较 synergy-augmented 方法，它减少了大搜索空间下的多轮交互成本。
