---
title: A survey of large language model-augmented knowledge graphs for advanced complex product design
short_name: LLM-KG-CPD-Survey
source_pdf: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: refs
status: parsed
venue: Journal of Manufacturing Systems
year: 2025
---

# LLM-KG-CPD-Survey 参考文献与关系缓存

## 对应正式知识节点
- 论文：[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- 概念：[[LLM增强知识图谱]]、[[复杂产品设计中的LLM-KG协同框架]]
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]
- 基准：无统一 benchmark；以文献筛选统计与代表性工作归纳为主

> 本文件服务 survey 论文的引用关系、代表性工作聚类和规范适配分析。与方法论文不同，这里更强调“路线簇 / 研究方向 / 代表工作”而不是单条方法演化链。

## 1. 论文自身元数据
- 标题：A survey of large language model-augmented knowledge graphs for advanced complex product design
- 类型：survey / framework / taxonomy-leaning review
- 文献时间范围：2021–2024
- 纳入论文数：100

## 2. 关键上游路线
> 本节支撑该论文的综述型引用结构，而不是单一方法的强基线对比结构。

- [[RoG]] / [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]：代表 KG 推理与可解释推理路线
- [[GCR]] / [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]：代表 graph-constrained reasoning 路线
- [[EPERM]] / [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]：代表 evidence path 增强路线
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs|GNN-RAG]]：代表图神经检索增强路线
- [[ToG]] / [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]：代表协同增强 / 交互式推理路线
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]：代表 LLM 生成推理路径路线
- CPD-LLM：代表复杂产品设计领域专用 LLM 路线
- CPD-KG：代表复杂产品设计领域专用 KG 路线

## 3. 与知识库当前最相关的综述结论
- LLM 与 KG 在复杂产品设计中更适合作为“协同框架”理解，而不是单独比较某个方法优劣。
- 对于该类 survey，`method_evolution.md` 不是最优主落点，`concept_links.md`、`ontology/graph-standard.md`、`scenarios/` 与 `synthesis/` 更关键。
- 这类论文的“benchmark”主要是文献筛选、统计归纳、阶段分析，而非统一数据集实验比较。
- 这类论文更需要“framework / taxonomy / role decomposition”式知识页，而不是硬套单方法模板。

## 4. 可直接复用到关系页的条目
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]：作为 LLM + KG 推理路线代表工作被纳入 survey。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]：作为 graph-constrained reasoning 代表工作被纳入 survey。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]：作为 evidence path 增强路线代表工作被纳入 survey。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]：作为图检索增强路线代表工作被纳入 survey。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]：作为协同增强路线代表工作被纳入 survey。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] → [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]：作为生成推理路径路线代表工作被纳入 survey。

## 5. 对规范通用性的直接信号
- 当前知识库规范已经允许 survey / benchmark 论文弱化单一方法节点要求，这是正确方向。
- 但还缺少“framework 节点 / taxonomy 节点”的正式页面模板。
- `experiments.md` 对这类论文不是天然核心缓存，后续可考虑允许 survey 论文将其降级为“statistics.md”或“landscape.md”。
- `task_method_map.md` 对这类论文的适配有限，更合适补充“task-framework-map”或“scenario-framework-map”。
