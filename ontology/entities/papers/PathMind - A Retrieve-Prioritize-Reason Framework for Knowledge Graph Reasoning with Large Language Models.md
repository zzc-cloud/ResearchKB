---
title: PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
authors: [Yu Liu, Xixun Lin, Yanmin Shang, Yangxi Li, Shi Wang, Yanan Cao]
year: 2026
venue: AAAI
problem: [reasoning, query-answering]
method_family: [hybrid, llm, gnn]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [integrated]
tags: [PathMind, KGR, KGQA, LLM]
status: processed
---

# PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models

## Object semantics
- 该论文提出 [[../methods/PathMind|PathMind]] 方法，并把 [[../concepts/路径优先化|路径优先化]] 与 [[../concepts/重要推理路径|重要推理路径]] 明确用于 LLM 驱动的知识图谱推理。

## 核心问题
- 面向 [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]] 的 LLM-based KGR 方法，常在等权路径检索与高交互搜索成本之间权衡不足。

## 主要贡献
- 提出 [[../methods/PathMind|PathMind]]，以 retrieve-prioritize-reason 三段式组织推理流程。
- 将 [[../concepts/路径优先化|路径优先化]] 作为显式中间机制，用于从查询子图中筛出 [[../concepts/重要推理路径|重要推理路径]]。
- 在 [[../benchmarks/WebQSP|WebQSP]] 与 [[../benchmarks/CWQ|CWQ]] 上验证该方法对复杂问答任务的效果与效率。

## 核心方法
- 核心知识产物是 [[../methods/PathMind|PathMind]]，其由子图检索、路径优先化和知识推理三个组件构成。

## 相关任务
- [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
- [[../tasks/kgqa|kgqa]]
- [[../tasks/multi-hop-qa|multi-hop-qa]]

## 相关 benchmark
- [[../benchmarks/WebQSP|WebQSP]]
- [[../benchmarks/CWQ|CWQ]]

## 关键结论
- PathMind 通过语义感知的路径优先函数识别关键推理路径，在 WebQSP 与 CWQ 上优于强基线。
- 与多轮 agentic 搜索路线相比，它用更少的 LLM 调用与 token 完成更稳定的推理。
- 路径优先化对复杂多跳问题更关键，且在更强 backbone 上仍保持增益。

## 引用了哪些重要工作
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning on Knowledge Graphs|RoG]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with large language models|GCR]]
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering|EPERM]]
- [[Think-on-Graph - Deep and Responsible Reasoning of Large Language Model on Knowledge Graph|ToG]]

## 被哪些论文引用（已知）
- 暂无知识库内已登记的后续引用。

## 与知识库其他内容的关联
- 该论文与 [[../methods/PathMind|PathMind]]、[[../concepts/路径优先化|路径优先化]]、[[../concepts/重要推理路径|重要推理路径]] 共同构成一条面向 [[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]] 的 PathMind 主线。

## 证据来源
- 章节级机制证据：PathMind.sections
- 引用与路线定位证据：PathMind.refs
- 实验与效率证据：PathMind.experiments

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `proposes`：提出的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: 论文将 PathMind 定义为 Retrieve-Prioritize-Reason 主框架的核心方法实例。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `proposes`：提出的概念（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化|路径优先化]]
  - edge_semantics: 论文把路径优先化作为筛选关键推理路径的核心机制。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `proposes`：提出的概念（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径|重要推理路径]]
  - edge_semantics: 论文将重要推理路径定义为应优先暴露给 LLM 的高价值路径。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - edge_semantics: 论文将知识图谱推理作为总任务设定。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
  - edge_semantics: 论文在 KGQA benchmark 上验证其路径优先化推理能力。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa|multi-hop-qa]]
  - edge_semantics: 论文特别面向多跳问答中的复杂路径推理。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]
  - edge_semantics: 论文使用 WebQSP 评估 PathMind 在问答场景中的准确率与 F1。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ|CWQ]]
  - edge_semantics: 论文使用 CWQ 检验 PathMind 在复杂多跳问答中的性能、可解释性与可扩展性。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `cites`：上游论文（文档：`ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning on Knowledge Graphs.md`）：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning on Knowledge Graphs|RoG]]
  - edge_semantics: 论文将 RoG 作为 retrieval-augmented 路线中显式关系路径推理的关键上游。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `cites`：上游论文（文档：`ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with large language models.md`）：[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with large language models|GCR]]
  - edge_semantics: 论文将 GCR 作为可靠路径生成路线的重要比较对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `cites`：上游论文（文档：`ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`）：[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering|EPERM]]
  - edge_semantics: 论文将 EPERM 作为 evidence-path 增强路线的重要 retrieval baseline。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `cites`：上游论文（文档：`ontology/entities/papers/Think-on-Graph - Deep and Responsible Reasoning of Large Language Model on Knowledge Graph.md`）：[[Think-on-Graph - Deep and Responsible Reasoning of Large Language Model on Knowledge Graph|ToG]]
  - edge_semantics: 论文将 ToG 作为 synergy-augmented 路线的代表方法进行对照。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
