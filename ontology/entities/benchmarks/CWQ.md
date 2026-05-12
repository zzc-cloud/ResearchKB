---
title: CWQ
problem: [query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [kgqa, multi-hop-qa]
industry: [general]
research_role: [benchmark]
status: processed
---

# CWQ

## benchmark 定义
CWQ 是复杂知识图谱问答 benchmark，用于评测方法在多跳复杂查询上的推理能力。

## 评测目标
该 benchmark 重点考察复杂问题上的答案命中率、回答覆盖度与多跳推理能力。

## 相关任务
当前主要关联 kgqa 与 multi-hop-qa 任务，但本页不直接维护 benchmark 到 task 的 formal relation；这类关联主要通过共享的方法邻接体现，例如某方法既在 CWQ 上评测，又以这些任务为目标。

## 被哪些方法 / 论文使用
当前知识库中，PathMind 明确在该 benchmark 上进行了评测，并在复杂推理条件下展示了正式 benchmark 优势。

## 相关场景
当前 benchmark 页面不单独提升稳定场景 formal 邻接。

## 证据来源
- PathMind.experiments：ontology/entities/evidence/PathMind.experiments.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: PathMind.experiments 记录了 CWQ 上的主要实验结果、案例分析与扩展性结论。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `evaluated_on`：在该基准上评测的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 在 CWQ 上验证复杂多跳推理表现，并展示对复杂问题的优势。
  - evidence: [[../evidence/PathMind.experiments]]
