---
title: LLM-KG-CPD.analysis
short_name: LLM-KG-CPD
source_file: ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: analysis
venue: Journal of Manufacturing Systems
year: 2025
status: processed
---

# LLM-KG-CPD.analysis

## 对应正式知识节点
- [[../methods/LLM-KG collaboration framework for advanced complex product design]]

## 本节支撑什么
本缓存支撑这篇 survey 的统计分析、工业软件缺口分析、LLM/KG 角色分类、挑战总结与未来方向判断，用于支撑方法页中的框架价值、局限与设计治理语义。

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 文献筛选流程从 Scopus 与 Web of Science 初始检索 275 篇论文，经筛选后保留 100 篇用于统计与综合分析。
- 论文指出近四年研究热度快速提升，尤其在 2023 年达到显著增长，说明 LLM+KG 在复杂产品设计中的研究动量正在形成。
- Table 2 指出当前工业产品设计软件在动态知识集成、语义互联、自动验证与跨模态理解方面存在显著缺口，LLM-KG integration 被视为主要补洞路径。
- Table 3 与 Table 4 将 LLM 与 KG 的角色分别组织为 feature encoder / reasoner / generator 与 knowledge base / inference chain / validation device，为后续框架化建模提供了结构化语义。
- 论文把主要局限总结为大模型迁移成本、可解释性不足、KG 持续维护困难以及高质量网络化数据采集的合规挑战。
- 未来方向包括提升计算与分析基础设施、增强模型可解释性、建设动态更新机制、以及在合法合规前提下改进多源数据获取。

## 来源说明
- 原始来源：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
- 本缓存主要服务总体框架价值判断、局限性总结与 future-perspective 证据支撑。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf`）：[[../raw-sources/files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]
  - edge_semantics: LLM-KG-CPD.analysis 直接来源于该 survey 论文的统计图表、工业软件分析、角色分类、挑战与未来方向抽取。
  - evidence: [[LLM-KG-CPD.analysis]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`）：[[../methods/LLM-KG collaboration framework for advanced complex product design]]
  - edge_semantics: 该方法页中的框架价值、局限总结、工业软件缺口分析与角色分类由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/OLaLa.md`）：[[../methods/OLaLa]]
  - edge_semantics: OLaLa 在该 survey 的结构化 role-based coverage 中被纳入 knowledge fusion / ontology matching 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/KG-CGT.md`）：[[../methods/KG-CGT]]
  - edge_semantics: KG-CGT 在该 survey 的结构化 role-based coverage 中被纳入 KG-guided generation 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/RelMKG.md`）：[[../methods/RelMKG]]
  - edge_semantics: RelMKG 在该 survey 的结构化 role-based coverage 中被纳入 knowledge reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/StructGPT.md`）：[[../methods/StructGPT]]
  - edge_semantics: StructGPT 在该 survey 的结构化 role-based coverage 中被纳入结构化数据 reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
- `supported_by`：被该证据支撑的方法（文档：`ontology/entities/methods/CausalKGPT.md`）：[[../methods/CausalKGPT]]
  - edge_semantics: CausalKGPT 在该 survey 的结构化 role-based coverage 中被纳入 manufacturing-oriented knowledge reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: [[LLM-KG-CPD.analysis]]
