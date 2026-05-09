# Methods Index

> 本页负责 Method 对象域导航：先定位正式方法实例，再进入具体方法页；placeholder 方法仅用于图谱解析，不作为默认入口。

## 1. 对象域说明
- 本域收录 Method 节点。
- 默认 serving-ready 的方法进入“导航入口”。
- placeholder 方法进入“其他实例（不可导航）”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- PathMind 入口（文档：`ontology/entities/methods/PathMind.md`）：[[ontology/entities/methods/PathMind]]
  - object_semantics: retrieve-prioritize-reason 集成方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa。
  - status: serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
- RoG 占位入口（文档：`ontology/entities/methods/RoG.md`）：[[ontology/entities/methods/RoG]]
  - object_semantics: PathMind 的显式路径推理上游方法占位节点。
  - status: placeholder
- GCR 占位入口（文档：`ontology/entities/methods/GCR.md`）：[[ontology/entities/methods/GCR]]
  - object_semantics: PathMind 的可靠路径生成上游方法占位节点。
  - status: placeholder
- EPERM 占位入口（文档：`ontology/entities/methods/EPERM.md`）：[[ontology/entities/methods/EPERM]]
  - object_semantics: PathMind 的 evidence-path 增强上游方法占位节点。
  - status: placeholder
<!-- END MANAGED BLOCK:non-serving-placeholders -->
