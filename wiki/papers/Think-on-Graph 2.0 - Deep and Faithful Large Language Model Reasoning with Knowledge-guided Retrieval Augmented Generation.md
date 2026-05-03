---
title: Think-on-Graph 2.0: Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation
problem: [reasoning, query-answering]
method_family: [llm, hybrid]
scenario: []
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
tags: [placeholder, cited-work, synergy-augmented]
status: placeholder
---

## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与协同增强式路线对比对象。

## 核心问题
- 如何通过 LLM 与知识图谱的多轮交互增强复杂问题下的推理路径搜索能力。

## 主要贡献
- 提出协同增强式的多轮搜索推理路线，提升复杂多跳场景下的路径探索深度。

## 核心方法
- 对应方法：[[ToG]]

## 相关任务
- [[knowledge-graph-reasoning]]
- [[multi-hop-qa]]

## 应用场景
- [[知识图谱推理问答]]

## 相关基准
- [[CWQ]]

## 与知识库其他内容的关联
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 相关方法：[[ToG]]

## 与知识库现有内容的关系
- 相关方法：[[ToG]]
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 关联任务：[[knowledge-graph-reasoning]]、[[multi-hop-qa]]
- 关联场景：[[知识图谱推理问答]]

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --proposes--> [[ToG]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

## 待补充
- 若后续补到原始论文的专属 Evidence 缓存，可进一步扩充方法细节与实验设定。

