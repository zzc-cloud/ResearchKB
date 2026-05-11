# Methods Index

> 本页负责 Method 对象域导航：先定位正式方法实例，再进入具体方法页；placeholder 方法仅用于图谱解析，不作为默认入口。

## 1. 对象域说明
- 本域收录 Method 节点。
- `status: processed` 与 `status: partial` 的 Method 均可进入“导航入口”。
- Paper placeholder 不承担方法域导航；若方法身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- PathMind 入口（文档：`ontology/entities/methods/PathMind.md`）：[[ontology/entities/methods/PathMind]]
  - object_semantics: 一种面向知识图谱推理的 retrieve-prioritize-reason 集成方法，通过路径优先排序与路径偏好对齐引导 LLM 使用高价值推理路径。
  - status: serving-ready
- RoG 入口（文档：`ontology/entities/methods/RoG.md`）：[[ontology/entities/methods/RoG]]
  - object_semantics: 一种显式推理路径导向的知识图谱推理方法，代表 retrieval-augmented 路线中的关系路径推理方案。
  - status: partial
- GCR 入口（文档：`ontology/entities/methods/GCR.md`）：[[ontology/entities/methods/GCR]]
  - object_semantics: 一种 grounded reasoning path 知识图谱推理方法，代表 grounded 路线的参考方法。
  - status: partial
- EPERM 入口（文档：`ontology/entities/methods/EPERM.md`）：[[ontology/entities/methods/EPERM]]
  - object_semantics: 一种 evidence path enhanced 知识图谱问答方法，代表 evidence-path 增强路线。
  - status: partial
- ToG 入口（文档：`ontology/entities/methods/ToG.md`）：[[ontology/entities/methods/ToG]]
  - object_semantics: 一种通过 LLM 与知识图谱多轮交互进行路径搜索的 synergy-augmented 知识图谱推理方法。
  - status: partial
- KnowPath 入口（文档：`ontology/entities/methods/KnowPath.md`）：[[ontology/entities/methods/KnowPath]]
  - object_semantics: 一种利用 LLM 生成推理路径的知识图谱推理方法，代表生成式 inference-path 路线。
  - status: partial
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
