# Methods Index

> 本页负责 Method 对象域导航：先定位正式方法实例，再进入具体方法页；placeholder 方法仅用于图谱解析，不作为默认入口。

## 1. 对象域说明
- 本域收录 Method 节点。
- `status: processed` 与 `status: partial` 的 Method 均可进入“导航入口”。
- Paper placeholder 不承担方法域导航；若方法身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- PathMind 方法入口（文档：`ontology/entities/methods/PathMind.md`）：[[ontology/entities/methods/PathMind.md]]
  - object_semantics: PathMind 方法实例，通过 Retrieve-Prioritize-Reason 流程显式识别重要推理路径以支持知识图谱推理。
  - status: serving-ready
- RoG 方法入口（文档：`ontology/entities/methods/RoG.md`）：[[ontology/entities/methods/RoG.md]]
  - object_semantics: RoG 方法实例，代表强调 faithful and interpretable graph reasoning 的 retrieval-augmented KGR 路线。
  - status: partial
- GCR 方法入口（文档：`ontology/entities/methods/GCR.md`）：[[ontology/entities/methods/GCR.md]]
  - object_semantics: GCR 方法实例，代表 graph-constrained reasoning 的 retrieval-augmented KGR 路线。
  - status: partial
- EPERM 方法入口（文档：`ontology/entities/methods/EPERM.md`）：[[ontology/entities/methods/EPERM.md]]
  - object_semantics: EPERM 方法实例，代表 evidence-path enhanced reasoning 的知识图谱问答路线。
  - status: partial
- GNN-RAG 方法入口（文档：`ontology/entities/methods/GNN-RAG.md`）：[[ontology/entities/methods/GNN-RAG.md]]
  - object_semantics: GNN-RAG 方法实例，代表以图神经检索提升知识图谱推理效率的 retrieval-augmented 路线。
  - status: partial
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
