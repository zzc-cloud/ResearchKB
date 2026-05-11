---
title: PathMind.experiments
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: experiments
status: processed
year: 2026
venue: AAAI-26
---

# PathMind.experiments

## Object semantics
- PathMind 论文的实验与效率证据页，承载 benchmark 结果、消融、可扩展性与效率比较的最小可审计摘要。

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../tasks/kgqa]]
- [[../tasks/multi-hop-qa]]
- [[../benchmarks/WebQSP]]
- [[../benchmarks/CWQ]]

## 本节支撑什么
- PathMind 在 WebQSP 与 CWQ 上整体优于主要对比基线。
- 路径优先化、path-wise preference alignment 与训练阶段都对最终性能有显著贡献。
- PathMind 在复杂多跳问答上相较强基线有更明显提升。
- 与多轮交互类方法相比，PathMind 在效率上以更少的 LLM 调用与 token 取得更平衡的结果。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Table 1：PathMind 在 WebQSP 上达到 Hits@1 = 0.895、F1 = 0.728，在 CWQ 上达到 Hits@1 = 0.707、F1 = 0.614。
- Table 2：去掉 prioritization、alignment 或 training 后，WebQSP 与 CWQ 指标都显著下降。
- Table 3：important paths 策略明显优于 random paths 与 shortest paths。
- Table 5：在 WebQSP 上，PathMind 只需 1 次 LLM 调用、216 个输入 token，时间约 2.23s。
- Figure 5 与 Figure 6：案例分析与可扩展性分析表明，路径筛选对多跳推理的解释性与鲁棒性都有关键作用。

## 来源说明
- 来源于原始 PDF 的 Experiments、Ablation Study、Further Analysis、Case Study 与 Conclusion 部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 实验与效率证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 实验证据页支撑 PathMind 的性能、消融、可扩展性与效率结论。
  - evidence: [[../evidence/PathMind.experiments]]
- `supported_by`：kgqa（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa]]
  - edge_semantics: 实验证据页支撑该任务上的 benchmark 表现。
  - evidence: [[../evidence/PathMind.experiments]]
- `supported_by`：multi-hop-qa（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa]]
  - edge_semantics: 实验证据页支撑复杂多跳问答上的性能与案例分析。
  - evidence: [[../evidence/PathMind.experiments]]
- `supported_by`：WebQSP（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP]]
  - edge_semantics: 实验证据页支撑 WebQSP 作为论文中的主要评测 benchmark 之一。
  - evidence: [[../evidence/PathMind.experiments]]
- `supported_by`：CWQ（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ]]
  - edge_semantics: 实验证据页支撑 CWQ 作为论文中的主要复杂多跳评测 benchmark。
  - evidence: [[../evidence/PathMind.experiments]]
