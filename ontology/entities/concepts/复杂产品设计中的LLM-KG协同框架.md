---
title: 复杂产品设计中的LLM-KG协同框架
concept_kind: framework
problem: [ontology-modeling, benchmark-survey, reasoning]
method_family: [llm, hybrid]
scenario: []
research_task: [engineering-design-knowledge-management]
industry: [manufacturing]
research_role: [integrated]
tags: [framework, complex product design, LLM, KG, taxonomy]
---

> 导航：返回 [[index|concepts/index]]；相关对象域 [[../methods/index|methods/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/concept_links|concept_links]]、[[../relations/paper_method_links|paper_method_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 概念入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。

## 概念定义
一种将复杂产品设计中的多源数据、知识图谱、大语言模型、设计能力增强与任务执行按层组织的协同框架，用于解释 LLM 与 KG 如何在设计流程中形成系统级互补。

## 核心内涵
- 典型四层：data layer、KG & LLM collaboration layer、enhanced design capability layer、design task layer。
- 在更细粒度上，还可进一步分解出 ontology、validation、interaction、application 等层。
- 其核心贡献不是单点算法，而是解释复杂设计中知识组织、推理、验证、交互与执行如何联动。

## 与其他概念的关系
- [[LLM增强知识图谱]]：这是该概念在复杂产品设计场景中的具体框架化落地。
- [[复杂产品设计]]：框架面向的核心场景。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]：该框架首先以 survey 论文形式被系统提出与归纳。

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]

## 相关任务 / 场景
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]

## Formal relations
### Outgoing
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[复杂产品设计中的LLM-KG协同框架]] --applies_to--> [[复杂产品设计]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]

### Incoming
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
