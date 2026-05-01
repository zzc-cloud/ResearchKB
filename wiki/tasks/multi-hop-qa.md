---
title: Multi-hop QA
problem: [query-answering, reasoning]
method_family: [hybrid]
scenario: []
research_task: [multi-hop-qa]
industry: [general]
research_role: [application]
tags: [多跳问答, 研究任务]
---

## 任务定义
需要沿多个实体与关系跳转才能得到答案的问答任务，强调跨多步证据链的组合推理能力。

> 本页描述多跳问答这一研究任务；其应用化视角统一沉淀在 [[知识图谱推理问答]] 场景页中。

## 核心关注点
- 如何在多跳搜索空间中识别最关键的证据链。
- 如何避免随着 hop 数增加而急剧放大的路径噪声。
- 如何在多步推理中保持答案可解释性与资源效率。

## 相关方法
- [[PathMind]]
- [[RoG]]
- [[ToG]]
- [[GCR]]

## 相关概念
- [[路径优先化]]
- [[重要推理路径]]

## 相关场景
- [[知识图谱推理问答]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 关系索引
- 方法映射：[[task_method_map]]
- 证据索引：[[evidence_index]]
