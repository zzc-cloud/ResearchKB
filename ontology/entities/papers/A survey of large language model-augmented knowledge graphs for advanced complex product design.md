---
title: A survey of large language model-augmented knowledge graphs for advanced complex product design
authors: Xinxin Liang, Zuoxu Wang, Jihong Liu
year: 2025
venue: Journal of Manufacturing Systems
problem: [knowledge-acquisition, reasoning, benchmark-survey]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [manufacturing]
research_role: [survey]
status: processed
---

# A survey of large language model-augmented knowledge graphs for advanced complex product design

## Object semantics
这是一篇 survey 型 Paper，系统综述了 advanced complex product design 中 LLM 与 KG 的协同研究，并提出一个四层 LLM-KG 协同复杂产品设计框架作为结构化综合结果。

## 核心问题
论文关注如何在 knowledge-intensive 的复杂产品设计中，把 LLM 的感知、推理与生成能力，与 KG 的结构化知识表示、推理链与动态维护能力结合起来，以提升设计效率、语义理解、验证能力与多源知识复用水平。

## 主要贡献
论文首先对 2021-2024 年间 100 篇相关文献进行了系统综述与统计分析。其后，论文提出了一个面向 advanced complex product design 的四层 LLM-KG 协同框架，并进一步给出 CPD-LLM 与 CPD-KG 两个子框架，用于说明如何构建领域化设计大模型与复杂产品设计知识图谱。论文最后总结了该路线的关键优势、主要限制与未来发展方向。

## 核心方法
本文不是单一 benchmark 驱动的实验方法论文，而是提出一个可复用的框架化技术方案：以 data layer 汇聚多源多模态设计数据，以 KG-LLM collaboration layer 组织知识存储、推理与生成分工，以 enhanced design capability layer 提升理解、推理、交互与生成能力，并在 design task layer 中落到需求分析、概念设计、具身设计与测试验证等设计阶段。

## 相关任务
论文覆盖的是复杂产品设计流程中的设计阶段任务，而非当前知识库内以 KGQA、multi-hop QA、graph completion 为代表的研究任务型目标。它更接近制造业复杂产品设计中的框架化设计协同问题。

## 应用场景
论文的核心应用语境是 advanced complex product design 与 intelligent manufacturing，强调产品设计、工程知识复用、人机协同设计与跨模态设计数据整合。

## 相关基准
论文没有提出统一 benchmark，也没有围绕单一数据集开展 formal benchmark evaluation；它主要提供系统综述、统计分析、工业软件差距分析与框架化综合。因此本次 ingest 不生成 `evaluated_on` formal relation。

## 关键结论
LLM 与 KG 的协同在复杂产品设计中具有明显互补性：KG 更适合承担结构化知识组织、推理验证与动态更新，LLM 更适合承担特征编码、复杂语义理解、推理生成与交互式内容生成。论文同时指出，该方向当前仍受限于模型迁移成本、可解释性、知识图谱维护成本与合规数据采集难题，但仍具备较强的制造业落地潜力。

## 引用了哪些重要工作
论文广泛回顾了复杂产品设计中的知识图谱构建、多模态设计数据处理、需求工程、设计反馈生成、跨模态语义理解与 LLM 增强知识推理等路线。当前最重要的价值在于这些文献被重新组织进一个统一的 LLM-KG 协同设计框架：BEAR、AutoKG 与 ASKG 代表 LLM 增强的图谱构建与图谱增强路线；OLaLa 代表 ontology matching 与 knowledge fusion 路线；KG-CGT 代表 KG-guided generation 路线；RelMKG、StructGPT 与 CausalKGPT 代表知识图谱增强推理路线，而不是单条引用关系本身。

## 被哪些论文引用（已知）
当前知识库中尚未登记该论文的后续被引关系。

## 与知识库其他内容的关联
这篇论文把知识库的关注范围从通用知识图谱推理进一步扩展到 manufacturing 语境下的复杂产品设计，为后续摄入设计知识图谱、领域化设计大模型、设计验证与多模态工程数据相关论文提供了一个新的框架入口。

## 证据来源
- LLM-KG-CPD.sections：ontology/entities/evidence/LLM-KG-CPD.sections.md
- LLM-KG-CPD.analysis：ontology/entities/evidence/LLM-KG-CPD.analysis.md
- LLM-KG-CPD.refs：ontology/entities/evidence/LLM-KG-CPD.refs.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `proposes`：提出的方法（文档：`ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`）：[[../methods/LLM-KG collaboration framework for advanced complex product design]]
  - edge_semantics: 论文提出一个面向 advanced complex product design 的四层 LLM-KG collaboration framework，并以 CPD-LLM 与 CPD-KG 子框架细化其实现路径。
  - evidence: [[../evidence/LLM-KG-CPD.sections]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/BEAR.md`）：[[../methods/BEAR]]
  - edge_semantics: 该 survey 将 BEAR 纳入 LLM 增强 KG construction 的结构化方法 coverage，用于组织复杂产品设计中的知识图谱构建路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/AutoKG.md`）：[[../methods/AutoKG]]
  - edge_semantics: 该 survey 将 AutoKG 纳入 LLM 增强 KG construction 的结构化方法 coverage，用于组织复杂产品设计中的知识图谱自动生成路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/ASKG.md`）：[[../methods/ASKG]]
  - edge_semantics: 该 survey 将 ASKG 纳入 graph enrichment / scholarly KG enhancement 的结构化方法 coverage，用于组织相关知识抽取与图谱增强路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/OLaLa.md`）：[[../methods/OLaLa]]
  - edge_semantics: 该 survey 将 OLaLa 纳入 knowledge fusion / ontology matching 的结构化方法 coverage，用于组织 LLM 增强知识融合路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/KG-CGT.md`）：[[../methods/KG-CGT]]
  - edge_semantics: 该 survey 将 KG-CGT 纳入 KG-guided generation 的结构化方法 coverage，用于组织 LLM 与 KG 协同生成路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/RelMKG.md`）：[[../methods/RelMKG]]
  - edge_semantics: 该 survey 将 RelMKG 纳入 knowledge reasoning 的结构化方法 coverage，用于组织知识图谱增强语言模型推理路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/StructGPT.md`）：[[../methods/StructGPT]]
  - edge_semantics: 该 survey 将 StructGPT 纳入结构化数据 reasoning 的结构化方法 coverage，用于组织面向结构化数据的 LLM 推理路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
- `surveys_method`：系统覆盖的方法（文档：`ontology/entities/methods/CausalKGPT.md`）：[[../methods/CausalKGPT]]
  - edge_semantics: 该 survey 将 CausalKGPT 纳入 manufacturing-oriented knowledge reasoning 的结构化方法 coverage，用于组织复杂产品设计中的工业因果分析路线，而不是把它作为首次提出的方法。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无

## 我的批注
这篇论文的主要建模价值不在于新增一个 narrow algorithm，而在于为 manufacturing 语境下的 LLM-KG 协同设计提供了一个可复用的框架总览。相比单篇实验论文，它更适合作为后续领域摄入与方法组织的总入口。
