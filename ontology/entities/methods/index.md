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
- LLM-KG collaboration framework for advanced complex product design 方法入口（文档：`ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`）：[[ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md]]
  - object_semantics: 集成方法框架，通过分层组织多模态设计数据、知识图谱能力与大语言模型能力，支持制造业语境下的人机协同复杂产品设计。
  - status: serving-ready
- BEAR 方法入口（文档：`ontology/entities/methods/BEAR.md`）：[[ontology/entities/methods/BEAR.md]]
  - object_semantics: BEAR 方法实例，代表 LLM 增强的知识图谱构建路线。
  - status: partial
- AutoKG 方法入口（文档：`ontology/entities/methods/AutoKG.md`）：[[ontology/entities/methods/AutoKG.md]]
  - object_semantics: AutoKG 方法实例，代表知识图谱自动生成路线。
  - status: partial
- ASKG 方法入口（文档：`ontology/entities/methods/ASKG.md`）：[[ontology/entities/methods/ASKG.md]]
  - object_semantics: ASKG 方法实例，代表 scholarly knowledge graph enhancement 路线。
  - status: partial
- OLaLa 方法入口（文档：`ontology/entities/methods/OLaLa.md`）：[[ontology/entities/methods/OLaLa.md]]
  - object_semantics: OLaLa 方法实例，代表 ontology matching 与 knowledge fusion 路线。
  - status: partial
- KG-CGT 方法入口（文档：`ontology/entities/methods/KG-CGT.md`）：[[ontology/entities/methods/KG-CGT.md]]
  - object_semantics: KG-CGT 方法实例，代表 KG-guided generation 路线。
  - status: partial
- RelMKG 方法入口（文档：`ontology/entities/methods/RelMKG.md`）：[[ontology/entities/methods/RelMKG.md]]
  - object_semantics: RelMKG 方法实例，代表知识图谱增强语言模型推理路线。
  - status: partial
- StructGPT 方法入口（文档：`ontology/entities/methods/StructGPT.md`）：[[ontology/entities/methods/StructGPT.md]]
  - object_semantics: StructGPT 方法实例，代表面向结构化数据的 LLM 推理路线。
  - status: partial
- CausalKGPT 方法入口（文档：`ontology/entities/methods/CausalKGPT.md`）：[[ontology/entities/methods/CausalKGPT.md]]
  - object_semantics: CausalKGPT 方法实例，代表制造业语境下的因果知识增强推理路线。
  - status: partial
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
