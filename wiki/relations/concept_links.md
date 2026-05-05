> 本页是正式关系账本：维护 `uses_concept` 及登记在本页的概念网络实例边。默认问答优先读取概念页、方法页、任务页或场景页；只有在概念网络治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../concepts/index|concepts/index]]、[[../methods/index|methods/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]
> 相关证据入口：[[evidence_index]]

## `uses_concept` 与概念网络实例边
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
  - reason: PathMind 的核心机制之一是路径优先化。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --uses_concept--> [[路径优先化]]`
  - reason: 论文将路径优先化作为核心机制显式建模。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind]] --uses_concept--> [[重要推理路径]]`
  - reason: PathMind 以识别和筛选重要推理路径为核心目标。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --uses_concept--> [[重要推理路径]]`
  - reason: 论文将 important reasoning paths 作为核心概念显式提出与使用。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind]] --applies_to--> [[知识图谱推理问答]]`
  - reason: PathMind 方法面向知识图谱推理问答场景落地。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --applies_to--> [[知识图谱推理问答]]`
  - reason: RoG 作为显式路径推理方法，用于知识图谱推理问答场景中的忠实推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --applies_to--> [[知识图谱推理问答]]`
  - reason: GCR 作为 grounded reasoning path 方法，面向知识图谱推理问答场景落地。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --applies_to--> [[知识图谱推理问答]]`
  - reason: EPERM 作为 evidence path 增强方法，面向知识图谱推理问答场景中的复杂问答推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[ToG]] --applies_to--> [[知识图谱推理问答]]`
  - reason: ToG 作为协同增强式方法，面向知识图谱推理问答中的多轮路径搜索场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[路径优先化]] --supports--> [[知识图谱推理问答]]`
  - reason: 路径优先化通过突出高价值证据路径支撑知识图谱推理问答场景中的答案推断。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[路径优先化]] --supports--> [[重要推理路径]]`
  - reason: 路径优先化机制直接服务于重要推理路径的识别与筛选。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[重要推理路径]] --supports--> [[knowledge-graph-reasoning]]`
  - reason: 重要推理路径为知识图谱推理提供关键证据链。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[重要推理路径]] --supports--> [[kgqa]]`
  - reason: 重要推理路径是复杂问答中的高价值证据链单元。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[重要推理路径]] --supports--> [[multi-hop-qa]]`
  - reason: 重要推理路径是多跳问答中的高价值证据链单元。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[重要推理路径]] --supports--> [[知识图谱推理问答]]`
  - reason: 重要推理路径为知识图谱推理问答场景提供关键证据链。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --uses_concept--> [[LLM增强知识图谱]]`
  - reason: 该 survey 系统梳理 LLM 增强知识图谱路线。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §3–5
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - reason: 该框架以 LLM 增强知识图谱作为系统级协同基础。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6–10
- `[[复杂产品设计中的LLM-KG协同框架]] --applies_to--> [[复杂产品设计]]`
  - reason: 该框架面向复杂产品设计场景落地。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6–10

## 说明
- 本页是概念网络与 `uses_concept` 实例边的正式账本。
- 由于 framework 统一按 concept 处理，本页维护 concept-to-concept、concept-to-scenario，以及 paper / method 到 concept 或 scenario 的补充语义边。
- `supports` / `depends_on` / `applies_to` 仅按 `graph-standard.md` 中登记的允许标签使用。
