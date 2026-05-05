> 本页是正式关系账本：维护 `proposes` 实例边。默认问答优先读取论文页或方法 / 概念页；只有在 formal graph truth 核对或治理场景下优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]、[[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]
> 相关证据入口：[[evidence_index]]

## `proposes` 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - reason: 该论文首次提出 Retrieve-Prioritize-Reason 的 PathMind 方法。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]] --proposes--> [[RoG]]`
  - reason: 该论文提出 RoG 方法，作为显式关系推理路径的代表方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --proposes--> [[GCR]]`
  - reason: 该论文提出 graph-constrained reasoning 的 GCR 方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --proposes--> [[EPERM]]`
  - reason: 该论文提出 evidence path enhanced reasoning 的 EPERM 方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --proposes--> [[ToG]]`
  - reason: 该论文提出协同增强式的 ToG 方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - reason: 该 survey 提出并系统解释复杂产品设计中的 LLM-KG 协同分层框架。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6

## 说明
- 本页是 `proposes` 实例边的正式账本。
- `proposes` 允许 `Paper -> Method` 与 `Paper -> Concept`。
- Survey 始终保留在 Paper 层；若论文提出的是 framework / taxonomy 型核心知识产物，应以 `Paper -> Concept` 记录，不把 framework 记成 Method。
