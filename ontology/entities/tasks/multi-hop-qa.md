---
title: multi-hop-qa
problem: [query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [multi-hop-qa]
industry: [general]
research_role: [foundational]
status: processed
---

# multi-hop-qa

## 任务定义
multi-hop-qa 指需要跨越多个实体与关系进行链式证据组合后完成回答的问答任务。

## 核心挑战
主要挑战包括长路径搜索、关键信息筛选、推理链一致性与复杂答案空间下的稳健回答。

## 相关方法
当前已识别的方法实例包括 PathMind，它在 formal ledger 中被明确投影为复杂多跳问答的目标方法。

## 相关机制
该任务典型依赖路径检索、路径优先级排序、多跳推理与结构化答案生成。

## 相关场景
当前页面聚焦研究任务，不单独建模稳定行业场景 formal 邻接。

## 相关 benchmark
当前相关 benchmark 包括 CWQ 与 WebQSP，但 formal benchmark 邻接由方法层统一承接。

## 相关论文
当前任务由 PathMind 论文提供直接支撑。

## 证据来源 / 关系索引
- PathMind.sections：ontology/entities/evidence/PathMind.sections.md
- PathMind.experiments：ontology/entities/evidence/PathMind.experiments.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections]]
  - edge_semantics: PathMind 在方法定义层面明确覆盖复杂多跳问答任务，本任务页由 sections 缓存支撑。
  - evidence: [[../evidence/PathMind.sections]]
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: PathMind 在复杂多跳问答 benchmark 上的表现为 multi-hop-qa 任务定位提供实验支撑。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：目标该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 旨在支持复杂多跳问题上的推理与回答，稳定覆盖 multi-hop-qa 任务。
  - evidence: [[../evidence/PathMind.sections]]
