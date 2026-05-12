---
title: kgqa
problem: [query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [foundational]
status: processed
---

# kgqa

## 任务定义
kgqa 指在知识图谱或知识库上针对自然语言问题生成答案的研究任务。

## 核心挑战
主要挑战包括问题解析、多跳证据连接、噪声控制与答案生成时的逻辑一致性。

## 相关方法
当前已识别的方法实例包括 PathMind，且它在 formal ledger 中被明确建模为该任务的目标方法。

## 相关机制
与该任务相关的主要机制包括检索增强、路径选择、结构化提示与受约束推理。

## 相关场景
当前页面主要表达研究任务身份，不单独提升行业场景 formal 邻接。

## 相关 benchmark
当前相关 benchmark 包括 WebQSP 与 CWQ，但 formal 邻接由方法层统一承接。

## 相关论文
当前任务由 PathMind 论文提供直接支撑。

## 证据来源 / 关系索引
- PathMind.sections：ontology/entities/evidence/PathMind.sections.md
- PathMind.experiments：ontology/entities/evidence/PathMind.experiments.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections]]
  - edge_semantics: PathMind 在知识图谱问答任务框架中提出并评估，本任务页由 sections 缓存支撑。
  - evidence: [[../evidence/PathMind.sections]]
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: PathMind.experiments 记录了 KGQA 语境下的主要 benchmark 表现与推理质量结果。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `targets_task`：目标该任务的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 论文将 PathMind 放在知识图谱问答语境下评估，并以 KGQA 作为核心任务入口之一。
  - evidence: [[../evidence/PathMind.sections]]
