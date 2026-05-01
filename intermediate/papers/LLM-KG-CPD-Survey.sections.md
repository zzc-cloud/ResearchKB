---
title: A survey of large language model-augmented knowledge graphs for advanced complex product design
short_name: LLM-KG-CPD-Survey
source_pdf: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: sections
status: parsed
venue: Journal of Manufacturing Systems
year: 2025
authors:
  - Xinxin Liang
  - Zuoxu Wang
  - Jihong Liu
---

# LLM-KG-CPD-Survey 结构化章节缓存

## 对应正式知识节点
- 论文：[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- 概念：[[LLM增强知识图谱]]、[[复杂产品设计]]、[[复杂产品设计中的LLM-KG协同框架]]
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]
- 基准：无统一 benchmark；以文献统计与应用阶段分析为主

> 本文件是该 survey 论文的默认分析入口。由于它属于综述 / 框架型论文，而非单一方法论文，因此本缓存优先服务结构梳理、分层框架提炼和综述结论复用。

## 1. 论文元数据
- 标题：A survey of large language model-augmented knowledge graphs for advanced complex product design
- 作者：Xinxin Liang, Zuoxu Wang, Jihong Liu
- 期刊：Journal of Manufacturing Systems 80 (2025) 883–901
- 年份：2025
- 关键词：Knowledge Graph, Large Language Model, Complex Product Design, Intelligent Manufacturing
- 论文类型判断：survey / framework / taxonomy-leaning review

## 2. 章节结构
1. Introduction
2. State-of-the-art analysis on LLM & KG studies
   - Systematic literature review process
   - Statistical analysis of the selected literature
   - Summary on the state-of-the-art LLM and KG studies
   - Research and analysis of industrial software design function
3. A framework of LLM-KG-collaboration in advanced complex product design
4. Data layer in LLM-KG collaborated product design
5. LLM-KG augmentation layer
   - KG and LLM roles in complex product design
   - From LLMs to complex product design domain LLMs
   - From common-sense KG to complex product design KG
6. Enhanced design capability layer
7. Design task layer
8. Advantages, limitations and future perspectives
9. Conclusion
10. References

## 3. Abstract 缓存
> 本节支撑 [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] 的综述定位与研究范围界定。

论文指出，在知识密集型复杂产品设计中，仅靠传统知识图谱及其推理方法已难以充分支撑 ill-defined design tasks。作者认为，大语言模型在自然语言理解、生成与协同交互上的优势，使其与知识图谱结合成为复杂产品设计中人机协同的重要方向。为填补该领域缺少系统综述的空白，作者筛选并分析了 2021–2024 年的 100 篇相关论文，对 LLM 与 KG 在复杂产品设计中的研究现状、主流技术、应用方式、技术框架、挑战与未来方向进行了系统总结，并提出一个面向复杂产品设计的 LLM-KG 协同框架。

## 4. Introduction 缓存
> 本节支撑 [[复杂产品设计]] 场景下为何需要 [[LLM增强知识图谱]]，以及该论文为何更适合作为 survey / framework 节点落库。

引言先强调复杂产品设计中的领域知识复用需求，以及知识图谱在设计知识表示、检索、推理和创新支持上的价值。随后指出当前基于 KG 的设计支持系统仍有明显局限：
- 训练数据标注成本高
- 高质量领域本体构建与维护困难
- 现有领域 KG 的语义理解能力不足，难以迁移到相近领域

作者认为，LLM 的预训练能力和自然语言理解能力可缓解上述问题，并帮助 KG 在知识建模、知识获取、知识融合与知识推理方面取得更强协同效果。论文提出三个研究问题：
1. LLM + KG 如何增强复杂工程产品的设计阶段？
2. 如何在复杂产品设计中部署 LLM 与 KG 以组织异构数据、增强设计能力、支撑设计任务？
3. 在设计流程中使用 LLM 与 KG 会带来哪些挑战与机会？

## 5. Literature Review & State-of-the-art 缓存
> 本节支撑该论文的“综述型证据来源”身份判断，以及文献筛选和路线归纳逻辑。

### 5.1 文献筛选流程
- 检索库：Scopus, Web of Science
- 检索库：Scopus, Web of Science
- 时间范围：2021–2024
- 初始结果：275 篇
- 缩减后：171 篇
- 最终纳入：100 篇
- 检索主题聚焦：complex product design / large language model / knowledge graph / knowledge engineering

### 5.2 文献统计结论
- 2023 年出现研究高峰，100 篇中有 81 篇集中于 2023 年。
- 国家分布上，中国最多，其次是美国、德国、澳大利亚。
- 期刊与会议分布显示该主题横跨制造、知识工程、NLP、AI 等多学科社区。

### 5.3 LLM / KG 技术总结
论文按架构将 LLM 分为：
- Decoder models
- Encoder models
- Encoder-decoder models
- Domain-specific models

并总结了 LLM 与 KG 在复杂产品设计中的多种角色：
- KG 作为 knowledge base
- KG 作为 inference chain
- KG 作为 validation device
- LLM 作为 feature encoder
- LLM 作为 reasoner
- LLM 作为 generator

## 6. Framework 缓存
> 本节支撑 [[复杂产品设计中的LLM-KG协同框架]] 这一核心框架概念的独立建模。

论文提出一个四层技术框架：
1. Data layer
2. KG & LLM collaboration layer
3. Enhanced design capability layer
4. Design task layer

此外，从 CPD-KG construction framework 的角度，又显式展示了：
- Ontology layer
- Data layer
- Validation layer
- Interaction layer
- Application layer

这说明论文的核心贡献之一不是单个方法，而是对复杂产品设计中 LLM-KG 协同系统的分层组织方式进行抽象，并将其扩展到从数据准备、知识建模、能力增强到任务执行的全链路框架。

## 7. Data Layer 缓存
> 本节支撑论文关于复杂产品设计中多源异构数据整合的论述，可回链到 [[复杂产品设计]] 与 [[LLM增强知识图谱]]。

作者认为 data layer 是后续所有层的基础，涉及：
- 结构化数据
- 传感器数据
- 非结构化文本
- 图像
- 3D 模型
- 历史设计案例
- 企业知识

重点在于多源、多模态、多学科知识资源的整合与预处理，为 KG 和 LLM 提供统一的设计知识基础。

## 8. KG-LLM Collaboration Layer 缓存
> 本节支撑 LLM 与 KG 的角色分工、相互增强机制以及从通用模型 / 通用 KG 向复杂产品设计领域特化的迁移逻辑。

作者把协同层概括为三个核心功能：
- KG 增强数据结构化、推理与系统适应能力
- LLM 提供编码、推理与内容生成能力
- 二者通过数据供给、推理基础与动态反馈形成协同闭环

论文还讨论：
- 从通用 LLM 向 complex product design domain LLM（CPD-LLM）迁移
- 从 common-sense KG 向 complex product design KG（CPD-KG）迁移
- 本体设计、术语一致性、跨学科概念融合的重要性

## 9. Enhanced Design Capability Layer 缓存
> 本节支撑论文关于“能力提升层”的总结，是这篇 survey 相对普通文献综述更偏框架型的重要证据。

增强设计能力层主要包括：
- Capability of integration
- Capability of understanding
- Reasoning capability
- Interaction capability
- Creativity / innovation capability

论文认为 LLM-KG 协同的价值不是只提升单点任务，而是系统性增强设计流程中的知识整合、理解、推理、交互和创新能力。

## 10. Design Task Layer 缓存
> 本节支撑论文关于复杂产品设计任务阶段化落地的分析。

论文将复杂产品设计任务拆到多个阶段，例如：
- Requirement analysis
- Conceptual design
- Embodiment design
- Prototyping & testing

并在每个阶段讨论 LLM-KG 协同如何介入，包括需求分析、概念生成、参数匹配、知识推理、仿真解释、自动测试报告生成等。

## 11. Advantages / Limitations / Future Work 缓存
> 本节支撑该论文的综述结论、研究空白判断与规范优化建议。

### 优势
- 多源异构知识整合与动态共享
- 设计自动化与决策效率提升
- 更深层语义理解与可解释推理
- 动态适应与知识演化
- 更自然的人机协同与交互式设计
- 跨领域创新与知识复用

### 局限
- 小模型向大模型迁移的成本与复杂性
- 可解释性与透明性不足
- 复杂产品设计领域中的 KG 持续维护与更新困难
- 高质量网络数据采集与合规问题

### 未来方向
- 更高质量的数据管理与协同机制
- 更强的可解释 AI 与可视化
- 领域知识与人类专家持续反馈闭环
- 实时监控与动态知识更新
- 合规的数据获取与保护机制

## 12. Conclusion 缓存
> 本节支撑该论文的最终定位：它是一个领域级 survey / framework 综述，而不是单一方法贡献论文。

作者总结认为，LLM 与 KG 的协同正在成为复杂产品设计智能化的重要路径。论文的关键价值不在于单一算法，而在于系统梳理了该方向的研究现状、角色分工、分层框架、任务阶段应用、优势局限和未来趋势，为后续构建更专门化的领域知识图谱与人机协同设计系统提供了基础路线图。

## 13. 适合后续复用的重点
- 若要判断该论文是否适合现有“方法论文”模板：优先读第 6、11、12 节
- 若要抽取 framework / taxonomy：优先读第 6、8、9、10 节
- 若要抽取 survey 结论与研究空白：优先读第 5、11、12 节
- 若要更新 ontology / graph-standard 以适配 survey 论文：优先读第 4、6、11 节
