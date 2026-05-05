---
title: PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
short_name: PathMind
source_pdf: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: refs
status: parsed
---

# PathMind 参考文献与基线缓存

## 对应正式知识节点
- 论文：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 方法：[[PathMind]]
- 概念：[[路径优先化]]、[[重要推理路径]]
- 任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 基准：[[WebQSP]]、[[CWQ]]

> 本文件用于后续引用关系登记、方法演化梳理与基线比较，避免重复从 PDF 尾部或实验表中重新抽取。

## 1. 论文自身元数据
> 本节支撑 [[PathMind]] 的来源标识与基础引用信息，可回链到正式论文页与原始 PDF。
- 标题：PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
- 会议：AAAI-26
- 年份：2026

## 2. 关键基线方法
> 本节支撑 [[PathMind]] 的基线对比网络与 [[citation_graph]] 中的上游工作登记。
- [[RoG]]
- [[GCR]]
- [[EPERM]]
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs|GNN-RAG]]
- [[ToG]]
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
- [[KD-CoT]]
- [[PoG]]

## 3. 与知识库当前最相关的基线/上游工作
> 本节支撑 [[PathMind]] 在方法演化链上的上游定位，以及后续占位节点的补全优先级。
### RoG
- 论文内角色：retrieval-augmented 路径推理代表方法
- 当前知识库定位：[[路径导向知识图谱推理]]
- 用途：对比显式关系路径生成与 PathMind 的路径价值排序

### GCR
- 论文内角色：grounded reasoning path 代表方法
- 当前知识库定位：[[路径导向知识图谱推理]]
- 用途：对比 grounded path 与 [[PathMind]] 的可学习路径优先级

### EPERM
- 论文内角色：evidence path 增强代表方法
- 当前知识库定位：[[路径导向知识图谱推理]]
- 用途：对比证据路径增强与重要路径筛选

### GNN-RAG
- 论文内角色：GNN 驱动的检索增强方法
- 当前知识库定位：[[检索增强式知识图谱推理]]
- 用途：对比子图检索效率与单轮调用成本

### ToG
- 论文内角色：synergy-augmented 代表方法
- 当前知识库定位：[[协同增强式知识图谱推理]]
- 用途：对比多轮交互搜索与 [[PathMind]] 的单轮推理范式

### KnowPath
- 论文内角色：LLM 生成推理路径方向的近期工作
- 当前知识库定位：待建方法或待建论文节点
- 用途：对比“生成路径”与“优先化路径”的路线差异

## 4. 当前可直接用于 citation_graph 的引用条目
> 本节支撑 [[citation_graph]] 的增量更新，可直接复用到关系登记文件。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]：方法借鉴，作为 retrieval-augmented 路径推理代表工作。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]：方法借鉴，作为 grounded reasoning path 代表工作。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]：方法借鉴，作为 evidence path 增强代表工作。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]：对比实验，作为 GNN 检索增强代表工作。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]：方法对比，作为 synergy-augmented 代表工作。
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] → [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]：方法对比，作为 LLM 生成推理路径方向的近期工作。

## 5. 后续待补节点
> 本节支撑后续 ingest 的补全优先级，避免关键上游节点长期游离在主图谱之外。
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]] 论文页或方法页
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs|GNN-RAG]] 论文页或方法页
- [[KD-CoT]] / [[PoG]] 占位节点
- 这些基线论文的正式摘要页
