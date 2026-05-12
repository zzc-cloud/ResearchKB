---
title: PathMind.experiments
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: experiments
venue: AAAI 2026
year: 2026
status: processed
---

# PathMind.experiments

## 对应正式知识节点
- [[../methods/PathMind]]
- [[../benchmarks/WebQSP]]
- [[../benchmarks/CWQ]]
- [[../tasks/kgqa]]
- [[../tasks/multi-hop-qa]]

## 本节支撑什么
本缓存支撑 PathMind 在 WebQSP 与 CWQ 上的评测结果、消融实验、路径排序策略分析、可扩展性分析与效率评估。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 主结果表明，PathMind 在 WebQSP 上取得 Hits@1 0.895、F1 0.728，在 CWQ 上取得 Hits@1 0.707、F1 0.614。
- 消融实验显示，去掉 path prioritization、alignment 或两阶段训练都会显著降低性能，说明重要路径识别与路径偏好对齐都对性能关键。
- 路径排序策略对比表明，important paths 明显优于 random paths 与 shortest paths。
- 效率评估显示，PathMind 在 WebQSP 上只需 1 次 LLM 调用和 216 tokens，优于多轮交互式 synergy 路线，同时保持较强性能。
- 可扩展性分析显示，该方法在不同 hop 与答案数量条件下保持较强鲁棒性。

## 来源说明
- 原始来源：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
- 本缓存主要服务 `evaluated_on`、benchmark 结论与实验支撑型 `supported_by`。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
  - edge_semantics: PathMind.experiments 直接来源于 PathMind 原始 PDF 的实验与案例分析抽取。
  - evidence: [[PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 的性能、效率与消融结论由 experiments 缓存直接支撑。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被该证据支撑的任务（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa]]
  - edge_semantics: PathMind.experiments 记录了 KGQA 语境下的主要 benchmark 表现与推理质量结果。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被该证据支撑的任务（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa]]
  - edge_semantics: PathMind 在复杂多跳问答 benchmark 上的表现为 multi-hop-qa 任务定位提供实验支撑。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被该证据支撑的 benchmark（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP]]
  - edge_semantics: PathMind.experiments 记录了 WebQSP 上的主要实验结果与效率分析。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被该证据支撑的 benchmark（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ]]
  - edge_semantics: PathMind.experiments 记录了 CWQ 上的主要实验结果、案例分析与扩展性结论。
  - evidence: [[PathMind.experiments]]
