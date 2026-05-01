---
title: A survey of large language model-augmented knowledge graphs for advanced complex product design
authors: [Xinxin Liang, Zuoxu Wang, Jihong Liu]
year: 2025
venue: Journal of Manufacturing Systems
problem: [knowledge-acquisition, benchmark-survey, ontology-modeling]
method_family: [llm, hybrid]
scenario: []
research_task: [engineering-design-knowledge-management]
industry: [manufacturing]
research_role: [survey]
tags: [知识图谱, 大语言模型, 复杂产品设计, 智能制造, survey, framework]
status: processed
paper_type: survey
---

## 核心问题
> 这篇论文系统梳理了 LLM 与知识图谱在复杂产品设计中的协同方式、能力分层、应用阶段和主要挑战，试图为复杂产品设计场景建立一个可解释的技术框架与研究地图。

## 主要贡献
- 系统综述了 2021–2024 年 LLM 与 KG 在复杂产品设计中的 100 篇相关研究。
- 给出复杂产品设计中 LLM-KG 协同的分层框架，包括 data layer、KG & LLM collaboration layer、enhanced design capability layer 与 design task layer。
- 归纳了 KG 与 LLM 在复杂产品设计中的典型角色分工，如 knowledge base / inference chain / validation device 与 feature encoder / reasoner / generator。
- 总结了该方向的优势、局限与未来发展方向，为后续领域本体、设计知识图谱与人机协同系统建设提供路线图。

## 核心方法 / 框架
> 这篇论文不提出单一核心方法，而是提出一套面向复杂产品设计的协同框架与综述型 taxonomy。
- 核心框架：[[复杂产品设计中的LLM-KG协同框架]]
- 相关概念：[[LLM增强知识图谱]]、[[复杂产品设计]]
- 相关任务：[[engineering-design-knowledge-management]]
- 技术路线：文献筛选 → 统计分析 → 路线归纳 → 框架分层 → 优势 / 局限 / 未来方向总结

## 应用场景
- 场景：[[复杂产品设计]]
- 任务阶段：需求分析、概念设计、具身设计、原型测试与验证
- 证据形式：文献统计、阶段映射、工业软件功能差距分析、框架图示

## 关键结论
- 这篇论文的核心价值在于“组织领域”，而不是提出单一算法。
- 复杂产品设计中的 LLM-KG 协同应被理解为框架级能力系统，而不是单点模型增强。
- KG 与 LLM 的角色分工可被稳定拆分为知识底座、推理链、验证机制与特征编码、推理、生成三类功能。
- 该方向的主要挑战集中在可解释性、动态知识维护、数据合规与领域特化模型构建。
- 这类 survey 论文验证了当前知识库规范必须支持 framework / taxonomy / survey 类型节点，而不能只围绕方法论文组织。

## 引用了哪些重要工作
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]] — 作为 KG 推理与可解释推理代表路线被 survey 纳入。
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] — 作为 graph-constrained reasoning 代表工作被纳入。
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] — 作为 evidence path 路线代表工作被纳入。
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]] — 作为图检索增强路线代表工作被纳入。
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] — 作为协同增强路线代表工作被纳入。
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]] — 作为生成推理路径路线代表工作被纳入。

## 被哪些论文引用（已知）
- 待补充

## 与知识库其他内容的关联
- 与 [[复杂产品设计中的LLM-KG协同框架]] 的关系：该论文提出并系统解释了这一分层框架。
- 与 [[LLM增强知识图谱]] 的关系：给出了领域应用中的角色划分与能力结构。
- 与 [[复杂产品设计]] 的关系：将该场景作为 LLM-KG 协同落地的核心应用域。
- 与 [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] 的关系：二者都涉及 LLM + KG，但 PathMind 是单方法论文，而本文是领域综述 / framework 论文，说明知识库规范必须同时覆盖两类论文。

## 实验证据 / 综述证据
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 引用与路线缓存：[[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- 分析与统计缓存：[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]

## 我的批注
> 这篇论文的重要意义不在“证明某个模型更强”，而在于它暴露了知识库设计不能只围绕方法论文组织：对于 framework / survey / taxonomy 论文，概念、场景、任务阶段、角色划分和 research gaps 才是主知识资产。
