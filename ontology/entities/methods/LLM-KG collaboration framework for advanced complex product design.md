---
title: LLM-KG collaboration framework for advanced complex product design
type: 集成方法
parent_methods: []
child_methods: []
problem: [knowledge-acquisition, reasoning, evolution-maintenance]
method_family: [hybrid, llm, symbolic]
scenario: []
research_task: []
industry: [manufacturing]
research_role: [integrated]
status: processed
---

# LLM-KG collaboration framework for advanced complex product design

## Object semantics
这是一个面向 advanced complex product design 的集成方法框架，通过分层组织多模态设计数据、知识图谱能力与大语言模型能力，来支持制造业语境下的人机协同设计。

## 方法定义
该方法把复杂产品设计中的 LLM 与 KG 协同组织为一个四层框架：data layer、KG-LLM collaboration layer、enhanced design capability layer、design task layer。

## 解决的核心问题
该框架旨在解决复杂产品设计中多源多模态数据难以统一组织、设计知识难以复用、语义理解与推理能力不足、自动验证能力弱、以及跨阶段设计协同成本高的问题。

## 技术原理
在 data layer，框架汇聚文本、图像、传感器、3D 模型、规则与历史案例等多模态设计数据。在 KG-LLM collaboration layer，KG 被组织为 knowledge base、inference chain 与 validation device，LLM 被组织为 feature encoder、reasoner 与 generator。在 enhanced design capability layer，框架提升更深层语义理解、设计推理、交互式协同与生成式设计能力。在 design task layer，框架把能力落到 requirement analysis、conceptual design、embodiment design 与 testing and validation 四个设计阶段。论文还用 CPD-LLM 与 CPD-KG 两个子框架补充说明领域大模型构建与复杂产品设计知识图谱构建路径。

## 方法演化与参照关系
### 上游演化方法
当前 formal ledger 中没有足够证据把该框架追溯为某一个严格 `based_on` 的上游方法。它更像是对复杂产品设计、知识图谱与大语言模型多条路线的综合组织。

### 关键参照方法
当前已基于该 survey 的结构化 coverage materialize 出一批最稳的 partial Method（如 BEAR、AutoKG、ASKG、OLaLa、KG-CGT、RelMKG、StructGPT、CausalKGPT），用于表达其已被系统覆盖的方法主线。其余高体量 survey 覆盖中的文献暂不批量升格为 `references_method`；后续若对更多具体设计方法完成独立 materialization，可再根据结构化 coverage 追加方法参照关系。

## 应用场景
该方法稳定定位于 manufacturing 语境下的 advanced complex product design、intelligent manufacturing 与人机协同设计，但当前知识库的 Scenario 受控词尚未提供与之严格对齐的正式场景节点，因此本次只保留行业与 prose 级表达，不生成 `applied_in` formal relation。

## 代表论文
代表论文为 A survey of large language model-augmented knowledge graphs for advanced complex product design。

## 相关机制
核心机制包括多模态设计数据整合、知识存储与动态更新、推理链与验证装置、LLM 的特征编码与推理生成分工、以及围绕 CPD-LLM 与 CPD-KG 的领域化模型与知识图谱构建流程。

## 证据来源
- LLM-KG-CPD.sections：ontology/entities/evidence/LLM-KG-CPD.sections.md
- LLM-KG-CPD.analysis：ontology/entities/evidence/LLM-KG-CPD.analysis.md
- LLM-KG-CPD.refs：ontology/entities/evidence/LLM-KG-CPD.refs.md

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/LLM-KG-CPD.sections.md`）：[[../evidence/LLM-KG-CPD.sections]]
  - edge_semantics: 该方法的四层总体框架、设计阶段映射与 LLM/KG 角色分工由 sections 缓存直接支撑。
  - evidence: [[../evidence/LLM-KG-CPD.sections]]
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/LLM-KG-CPD.analysis.md`）：[[../evidence/LLM-KG-CPD.analysis]]
  - edge_semantics: 该方法的工业软件缺口分析、角色分类、局限与未来方向由 analysis 缓存直接支撑。
  - evidence: [[../evidence/LLM-KG-CPD.analysis]]
- `supported_by`：证据支撑（文档：`ontology/entities/evidence/LLM-KG-CPD.refs.md`）：[[../evidence/LLM-KG-CPD.refs]]
  - edge_semantics: 该方法的文献 grounding、先行工作脉络与代表性角色来源由 refs 缓存直接支撑。
  - evidence: [[../evidence/LLM-KG-CPD.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `proposes`：提出该方法的论文（文档：`ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`）：[[../papers/A survey of large language model-augmented knowledge graphs for advanced complex product design]]
  - edge_semantics: 论文提出一个面向 advanced complex product design 的四层 LLM-KG collaboration framework，并以 CPD-LLM 与 CPD-KG 子框架细化其实现路径。
  - evidence: [[../evidence/LLM-KG-CPD.sections]]

## 优势与局限
该框架的优势在于把复杂产品设计中的数据、知识、推理、验证与生成能力统一组织到同一个协同视角下，并明确区分了 KG 与 LLM 的职责分工。其局限在于目前更偏框架化综合，尚未沉淀为单一 benchmark 驱动的方法评测范式，同时当前知识库的 Task / Scenario 受控词对制造业设计阶段的表达仍不够贴合。

## 与其他方法的对比
相比通用知识图谱推理方法，该框架不是围绕问答或图推理 benchmark 优化，而是围绕 manufacturing 语境下的设计协同、跨模态数据组织与知识复用进行框架级整合。相比纯 LLM 或纯 KG 方案，它强调二者在 perception、reasoning、validation 与 dynamic update 上的互补协作。
