---
title: LLM-KG-CPD.sections
short_name: LLM-KG-CPD
source_file: ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: sections
venue: Journal of Manufacturing Systems
year: 2025
status: processed
---

# LLM-KG-CPD.sections

## 对应正式知识节点
- [[../methods/LLM-KG collaboration framework for advanced complex product design]]

## 本节支撑什么
本缓存支撑该论文提出的 LLM-KG collaboration framework for advanced complex product design，包括四层总体框架、四个设计阶段映射，以及 LLM 与 KG 在复杂产品设计中的功能分工。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 论文将研究问题聚焦为三个方面：LLM 与 KG 如何增强 complex engineering products 的设计阶段、如何在 advanced complex product design 中组织异构数据并增强设计能力，以及设计流程中的主要挑战与机会。
- 论文基于 2021-2024 年筛选出的 100 篇文献开展系统综述，并以 requirement analysis、conceptual design、embodiment design、testing and validation 四个设计阶段组织应用图景。
- 论文提出一个四层技术框架：data layer、KG-LLM collaboration layer、enhanced design capability layer、design task layer。
- 在 KG-LLM collaboration layer 中，KG 被组织为 knowledge base、inference chain 与 validation device；LLM 被组织为 feature encoder、reasoner 与 generator。
- 论文明确把 advanced complex product design 视为 knowledge-intensive manufacturing 语境下的人机协同设计问题，而不是通用 KGQA 或 benchmark 驱动任务。

## 来源说明
- 原始来源：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
- 对应正式方法页中的总体框架、层次划分与设计阶段结论均可回查至本缓存。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf`）：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
  - edge_semantics: LLM-KG-CPD.sections 直接来源于该 survey 论文的摘要、问题设定、总体框架与分层结构抽取。
  - evidence: [[LLM-KG-CPD.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`）：[[../methods/LLM-KG collaboration framework for advanced complex product design]]
  - edge_semantics: 该方法页中的四层总体框架、设计阶段映射与 LLM/KG 角色分工由 sections 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.sections]]
