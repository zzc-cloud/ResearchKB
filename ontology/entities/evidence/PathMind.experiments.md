---
title: PathMind.experiments
short_name: PathMind
source_file: ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: experiments
venue: AAAI
year: 2026
status: processed
---

# PathMind.experiments

## Object semantics
- 该证据页承载 PathMind 在 WebQSP 与 CWQ 上的主结果、消融、可扩展性与效率证据。

## 对应正式知识节点
- [[../methods/PathMind|PathMind]]
- [[../benchmarks/WebQSP|WebQSP]]
- [[../benchmarks/CWQ|CWQ]]

## 本节支撑什么
- 支撑 PathMind 与论文对 KGQA / multi-hop-qa 的任务定位。
- 支撑论文与方法对 WebQSP、CWQ 的 evaluated_on 关系。
- 支撑 benchmark 页与任务页的性能、效率和可扩展性说明。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Table 1：PathMind 在 WebQSP 上 Hits@1/F1 为 0.895/0.728，在 CWQ 上 Hits@1/F1 为 0.707/0.614。
- Table 2：去掉 prioritization、alignment 或 training 都会显著降低性能，说明路径优先化和两阶段训练都是关键组件。
- Table 3 与 Figure 4：重要路径优先于随机路径和最短路径，且节点选择数 K=3 更合适。
- Table 5：PathMind 在 WebQSP 上只需 1 次 LLM 调用与 216 tokens，效率优于多轮 synergy-augmented 方法。
- Figure 5 与 Case Study：PathMind 在复杂案例中能抽取更符合人类直觉的关键路径。

## 来源说明
- 来源于 Experiments、Ablation、Further Analysis、Efficiency 与 Case Study 章节。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|PathMind PDF]]
  - edge_semantics: 该 experiments 缓存抽取自主结果、消融、效率与案例分析章节。
  - evidence: [[PathMind.experiments]]
### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被支撑的方法（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
  - edge_semantics: experiments 缓存支撑 PathMind 的性能、效率、消融与扩展性结论。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被支撑的任务（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - edge_semantics: experiments 缓存补充了知识图谱推理总任务在标准 benchmark 上的表现。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被支撑的任务（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
  - edge_semantics: experiments 缓存支撑 KGQA 任务上的 benchmark 结果与比较。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被支撑的任务（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa|multi-hop-qa]]
  - edge_semantics: experiments 缓存支撑复杂多跳问答任务上的表现与案例分析。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被支撑的 benchmark（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]
  - edge_semantics: experiments 缓存记录了 WebQSP 上的主结果与效率比较。
  - evidence: [[PathMind.experiments]]
- `supported_by`：被支撑的 benchmark（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ|CWQ]]
  - edge_semantics: experiments 缓存记录了 CWQ 上的主结果、消融和案例分析。
  - evidence: [[PathMind.experiments]]
