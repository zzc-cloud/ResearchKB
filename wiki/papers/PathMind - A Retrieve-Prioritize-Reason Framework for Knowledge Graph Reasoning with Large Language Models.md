---
title: PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
authors: [Yu Liu, Xixun Lin, Yanmin Shang, Yangxi Li, Shi Wang, Yanan Cao]
year: 2026
venue: AAAI-26
problem: [reasoning, query-answering, graph-learning]
method_family: [gnn, llm, hybrid]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [integrated]
tags: [知识图谱推理, LLM, 多跳问答, 路径优先化, 可解释推理]
status: processed
---

## 核心问题
> 这篇论文解决如何让大语言模型在知识图谱推理中既保持较高准确率，又减少噪声路径干扰，并提供更忠实、可解释的推理证据。

## 主要贡献
- 提出 PathMind，一个面向 LLM-based KGR 的 Retrieve-Prioritize-Reason 框架。
- 在子图检索之后引入路径优先化机制，用累计成本与未来成本联合识别重要推理路径。
- 采用任务指令微调与路径偏好对齐的双阶段训练，使 LLM 更稳定地利用重要路径完成推理。
- 在 WebQSP 与 CWQ 上同时提升推理性能，并以更少的 LLM 调用和 token 完成推理。

## 核心方法
> 论文通过“先取相关子图、再筛关键路径、最后引导 LLM 推理”的三阶段流程解决复杂知识图谱推理问题。
- 方法名称：[[PathMind]] / [[methods/PathMind|PathMind（方法）]]
- 核心概念：[[路径优先化]]、[[重要推理路径]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 技术路线：子图检索 → GNN 表征学习 → 路径优先化 → 任务指令微调 → 路径偏好对齐

## 应用场景
- 场景：[[知识图谱推理问答]]
- 相关基准：[[WebQSP]]、[[CWQ]]
- 数据集/实验环境：[[WebQSP]]、[[CWQ]]；LLM 主干为 Llama3.1-8B；PyTorch；2×NVIDIA A800 GPU

## 关键结论
- PathMind 在 WebQSP 上达到 Hits@1 0.895、F1 0.728，在 CWQ 上达到 Hits@1 0.707、F1 0.614。
- 路径优先化是最关键模块；去掉 prioritization 后性能显著下降。
- 与随机路径或最短路径相比，重要路径策略在两个基准上都显著更优。
- 相比多轮协同式方法，PathMind 只需 1 次 LLM 调用即可取得更优或相当的结果。
- 该方法在复杂多跳问答中表现尤其突出，说明“重要路径识别”比“扩大候选路径集合”更关键。

## 引用了哪些重要工作
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]] — 作为 retrieval-augmented 路径推理代表方法，用于比较显式路径推理与可解释性。
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] — 作为 grounded reasoning path 代表方法，用于对比忠实推理能力。
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] — 作为 evidence path 增强代表方法，用于对比路径证据建模。
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]] — 作为 GNN 检索增强代表方法，用于对比图结构检索效率。
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] — 作为 synergy-augmented 方向代表方法，用于对比交互式搜索范式。
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]] — 作为 LLM 生成推理路径方向的近期工作，用于横向比较路径构造思路。

## 被哪些论文引用（已知）
- 待补充

## 与知识库其他内容的关联
- 与 [[methods/PathMind|PathMind（方法）]] 的关系：该论文提出并验证了该方法。
- 与 [[路径优先化]] 的关系：将其作为核心机制显式建模。
- 与 [[重要推理路径]] 的关系：提出“important reasoning paths”作为支撑忠实推理的关键概念。
- 与 [[知识图谱推理问答]] 的关系：方法主要面向复杂多跳知识图谱问答任务。
- 与 [[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]] 的关系：为这些任务提供结构化路径推理与对齐训练方案。

## 证据来源
- 结构化章节缓存：[[intermediate/papers/PathMind.sections|PathMind.sections]]
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]
> 这篇论文的重要性不在于“又做了一种 KG + LLM”，而在于把研究重点从检索更多路径推进到识别更有价值的路径，是 retrieval-augmented KGR 向精细路径控制演化的代表工作。
