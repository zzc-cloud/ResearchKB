> 本页是正式关系账本：维护 `targets_task` 实例边。默认问答优先读取任务页或方法页；只有在任务映射治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../tasks/index|tasks/index]]、[[../methods/index|methods/index]]、[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]

## `targets_task` 实例边
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: PathMind 以知识图谱推理为核心任务定位。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: RoG 是知识图谱推理代表方法之一。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: GCR 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: EPERM 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[ToG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: ToG 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: 论文以知识图谱推理作为核心问题设定与验证任务之一。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - reason: PathMind 在知识图谱问答场景中验证方法有效性。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[kgqa]]`
  - reason: 论文以 KGQA 作为核心问题设定与验证任务之一。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[kgqa]]`
  - reason: RoG 是 KGQA 路线中的显式路径推理代表方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --targets_task--> [[kgqa]]`
  - reason: GCR 面向 KGQA 场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[kgqa]]`
  - reason: 该论文将 graph-constrained reasoning 用于 KGQA 场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - reason: EPERM 面向 KGQA 场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --targets_task--> [[kgqa]]`
  - reason: 该论文以 KGQA 为核心任务场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind]] --targets_task--> [[multi-hop-qa]]`
  - reason: PathMind 重点处理复杂多跳问答中的高价值路径选择。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[multi-hop-qa]]`
  - reason: 论文将复杂多跳问答作为核心验证任务之一。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[multi-hop-qa]]`
  - reason: RoG 面向多跳问答中的关系路径推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[ToG]] --targets_task--> [[multi-hop-qa]]`
  - reason: ToG 通过迭代搜索支持复杂多跳问答。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --targets_task--> [[multi-hop-qa]]`
  - reason: 该论文以复杂多跳问答作为核心验证任务之一。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[GCR]] --targets_task--> [[multi-hop-qa]]`
  - reason: GCR 面向 grounded 的多跳推理问答。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[multi-hop-qa]]`
  - reason: 该论文将 graph-constrained reasoning 用于多跳推理问答。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --targets_task--> [[multi-hop-qa]]`
  - reason: EPERM 面向多跳问答中的证据路径增强推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --targets_task--> [[multi-hop-qa]]`
  - reason: 该论文将证据路径增强用于复杂多跳问答推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --targets_task--> [[engineering-design-knowledge-management]]`
  - reason: 该 survey 以复杂产品设计中的知识管理与协同增强任务为综述对象。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §3–10

## 说明
- 本页是 `targets_task` 实例边的正式账本。
- 若某条关系仅涉及场景而非任务，应记录到对应知识页或后续场景关系文件，而不是混入本页。
