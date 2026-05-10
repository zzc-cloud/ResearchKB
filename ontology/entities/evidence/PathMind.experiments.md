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
- PathMind 论文的实验与效率证据页，承载 benchmark 结果、消融、可解释案例与效率对比的最小可审计摘要。

## 对应正式知识节点
- 该证据页主要支撑 PathMind 在 WebQSP 与 CWQ 上的评测、知识图谱问答相关任务，以及 benchmark 页的正式语义。

## 本节支撑什么
- PathMind 在 WebQSP 与 CWQ 上优于主要基线。
- 去掉路径优先化、alignment 或两阶段训练都会明显降低性能。
- 与 synergy-augmented 方法相比，PathMind 以更少 LLM 调用与 token 获得有竞争力或更优的结果。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- WebQSP：PathMind 的 Hits@1 为 0.895，F1 为 0.728。
- CWQ：PathMind 的 Hits@1 为 0.707，F1 为 0.614。
- 消融显示路径优先化与路径偏好对齐都对性能有显著贡献。
- 效率表显示 PathMind 在 WebQSP 上只需一次调用与较少 token。

## 来源说明
- 来源于 PathMind 原始 PDF 的 Experiments、Ablation、Scalability 与 Efficiency 部分。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：PathMind 原文 PDF（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: 该实验证据缓存直接编译自 PathMind 原始论文 PDF。
  - evidence: [[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：PathMind 方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 本页支撑 PathMind 的性能、消融、可扩展性与效率主张。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
- `supported_by`：kgqa（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa]]
  - edge_semantics: 本页支撑该方法在知识图谱问答任务上的效果。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
- `supported_by`：multi-hop-qa（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa]]
  - edge_semantics: 本页支撑该方法在复杂多跳问答上的性能表现。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
- `supported_by`：知识图谱推理问答（文档：`ontology/entities/scenarios/知识图谱推理问答.md`）：[[../scenarios/知识图谱推理问答]]
  - edge_semantics: 本页支撑该研究场景下的性能、可解释案例与效率比较。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
- `supported_by`：WebQSP（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP]]
  - edge_semantics: 本页支撑 WebQSP 作为 PathMind 主要评测基准之一。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
- `supported_by`：CWQ（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ]]
  - edge_semantics: 本页支撑 CWQ 作为 PathMind 主要评测基准之一。
  - evidence: [[PathMind.experiments|PathMind.experiments]]
