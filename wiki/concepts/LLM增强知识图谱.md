---
title: LLM增强知识图谱
problem: [knowledge-acquisition, ontology-modeling, reasoning]
method_family: [llm, hybrid]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
tags: [LLM, 知识图谱, 协同框架, 人机协同]
---

> 导航：返回 [[index|concepts/index]]；相关对象域 [[../methods/index|methods/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/concept_links|concept_links]]、[[../relations/paper_method_links|paper_method_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 概念入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 概念定义
LLM增强知识图谱指知识图谱与大语言模型之间形成双向增强关系：知识图谱提供结构化知识、推理链与验证能力，LLM 提供编码、推理、生成与交互能力，从而共同支撑更复杂的知识密集型任务。

## 核心内涵
- KG 可作为 knowledge base、inference chain、validation device 与 dynamic KG。
- LLM 可作为 feature encoder、reasoner、generator。
- 二者的协同价值不只是问答，而是知识组织、设计推理、知识更新与人机协作能力的系统提升。

## 与其他概念的关系
- [[复杂产品设计中的LLM-KG协同框架]]：该框架是 LLM增强知识图谱在复杂产品设计中的分层化表达。
- [[复杂产品设计]]：是该概念的重要行业落地场景。
- [[路径优先化]]：二者都体现 LLM 与图结构知识协同，但后者是方法级概念，前者是系统级协同概念。

## 相关方法 / 路线
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[ToG]]

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关任务 / 场景
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]

## 证据来源
- 概念关系：[[concept_links]]
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
