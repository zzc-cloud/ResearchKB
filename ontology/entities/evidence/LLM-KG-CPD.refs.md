---
title: LLM-KG-CPD.refs
short_name: LLM-KG-CPD
source_file: ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: refs
venue: Journal of Manufacturing Systems
year: 2025
status: processed
---

# LLM-KG-CPD.refs

## 对应正式知识节点
- [[../methods/LLM-KG collaboration framework for advanced complex product design]]

## 本节支撑什么
本缓存支撑该论文的文献谱系定位，尤其是复杂产品设计、制造业知识图谱、多模态设计数据处理、以及设计场景中的 LLM 增强路线，用于支撑方法页中的来源背景与结构化文献覆盖说明。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 参考文献覆盖了产品设计中的知识图谱融合、multimodal CAD / image / text integration、requirements engineering、design feedback generation、rule-based multimodal KG extraction、以及 LLM-augmented knowledge reasoning 等多个方向。
- 论文在整体论证中把复杂产品设计中的 LLM 角色组织为 feature encoder、reasoner、generator；把 KG 角色组织为 knowledge base、inference chain、validation device，并以相关文献为各角色提供 representative grounding。
- 与该方法最直接相关的先行工作包括 advanced vehicle design 中的 KG 融合、多模态设计插件、requirements reasoning、design quality analysis 与 design feedback generation 等路线。
- 当前 refs 缓存主要用于支撑总体框架的文献 grounding，并为当前已 materialize 的 survey-covered 方法（如 BEAR、AutoKG、ASKG）提供最小结构化 coverage provenance；其余高体量 survey 引文仍不批量升格为 formal `cites` 或 `surveys_method`，避免在未完成逐条 coverage 审计前引入噪声关系。

## 来源说明
- 原始来源：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
- 本缓存主要服务框架背景、先行工作 grounding 与后续 relation 扩展判断。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf`）：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
  - edge_semantics: LLM-KG-CPD.refs 直接来源于该 survey 论文的参考文献、表格归类与 related-work grounding 抽取。
  - evidence: [[LLM-KG-CPD.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`）：[[../methods/LLM-KG collaboration framework for advanced complex product design]]
  - edge_semantics: 该方法页中的文献 grounding、角色分工来源与先行工作脉络由 refs 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/BEAR.md`）：[[../methods/BEAR]]
  - edge_semantics: BEAR 在该 survey 中被纳入 LLM 增强 KG construction 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: [[LLM-KG-CPD.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/AutoKG.md`）：[[../methods/AutoKG]]
  - edge_semantics: AutoKG 在该 survey 中被纳入 LLM 增强 KG construction 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: [[LLM-KG-CPD.refs]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/ASKG.md`）：[[../methods/ASKG]]
  - edge_semantics: ASKG 在该 survey 中被纳入 knowledge extraction / graph enrichment 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: [[LLM-KG-CPD.refs]]
