## 方法演化树
- [[检索增强式知识图谱推理]]
  - └─ [[路径导向知识图谱推理]]
      - ├─ [[RoG]]（改进点：显式生成关系推理路径；代表论文：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]）
      - ├─ [[GCR]]（改进点：生成 grounded 的可靠推理路径；代表论文：[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]）
      - ├─ [[EPERM]]（改进点：增强证据路径；代表论文：[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]）
      - └─ [[PathMind]]（改进点：通过 [[路径优先化]] 识别 [[重要推理路径]]，并结合 LLM 对齐训练；代表论文：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]；关联任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]）
- [[协同增强式知识图谱推理]]
  - └─ [[ToG]]（改进点：通过多轮 LLM 交互与迭代搜索发现推理路径；代表论文：[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]）

## 说明
- 本页维护方法之间的 `based_on` / `improves_on` 关系。
- 当前演化树优先收录已在知识库中形成稳定方法节点的路线；仅出现在引用图中的上游工作会先保留在 [[citation_graph]] 与占位论文页中，待方法节点正式落库后再纳入本树。
- 相关任务映射见 [[task_method_map]]，证据索引见 [[evidence_index]]。
