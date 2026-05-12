---
title: knowledge-graph-reasoning
problem: [reasoning]
method_family: [hybrid, llm]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
status: processed
---

# knowledge-graph-reasoning

## 任务定义
knowledge-graph-reasoning 指在知识图谱上基于实体、关系与路径进行可追溯推理，以回答查询或推断新知识。

## 核心挑战
核心挑战包括候选推理路径规模巨大、路径噪声高、逻辑一致性难以保持，以及如何把结构化 KG 信号有效传递给 LLM。

## 相关方法
当前已识别的方法实例包括 PathMind，其 formal 角色是该任务的直接目标方法之一。

## 相关机制
与该任务强相关的机制包括子图检索、路径排序、路径约束推理与多跳证据聚合。

## 相关场景
当前页面主要承载研究任务语义，尚未补入稳定的行业场景 formal 邻接。

## 相关 benchmark
当前相关 benchmark 包括 WebQSP 与 CWQ，但本页不直接维护 task 到 benchmark 的 formal relation；相关 benchmark 主要通过共享的方法邻接体现，例如某方法既以 knowledge-graph-reasoning 为目标，又在这些 benchmark 上评测。

## 相关论文
当前任务由 PathMind 论文提供直接支撑。

## 证据来源 / 关系索引
- PathMind.sections：ontology/entities/evidence/PathMind.sections.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections]]
  - edge_semantics: PathMind 明确把其任务定位为知识图谱推理，本任务页由 sections 缓存支撑。
  - evidence: [[../evidence/PathMind.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：目标该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 被明确设计为知识图谱推理框架，直接服务于 knowledge-graph-reasoning 任务。
  - evidence: [[../evidence/PathMind.sections]]
