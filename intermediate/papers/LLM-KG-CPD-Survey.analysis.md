---
title: A survey of large language model-augmented knowledge graphs for advanced complex product design
short_name: LLM-KG-CPD-Survey
source_pdf: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf
cache_type: analysis
status: parsed
venue: Journal of Manufacturing Systems
year: 2025
---

# LLM-KG-CPD-Survey 分析与证据缓存

## 对应正式知识节点
- 论文：[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- 概念：[[LLM增强知识图谱]]、[[复杂产品设计中的LLM-KG协同框架]]
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]
- 基准：无统一 benchmark；本缓存作为文献统计 / 应用阶段 / 软件能力分析 / framework 支撑证据的 analysis 缓存

> 这是 survey / framework 论文默认使用的 `analysis.md`。该论文并无统一实验基准，因此本文件主要保留：文献筛选统计、任务阶段分布、工业软件能力差距分析、框架支撑证据。

## 1. 文献统计（替代数据集/benchmark）
> 本节支撑该论文作为 survey 的证据基础。
- 初筛：275 篇
- 二筛：171 篇
- 最终纳入：100 篇
- 时间跨度：2021–2024
- 2023 年是研究高峰（81 篇）

## 2. 国家 / 期刊 / 会议分布
> 本节支撑该方向在制造、知识工程和 AI 社区中的活跃度判断。
- 国家分布：中国最多，其次为美国、德国、澳大利亚
- 期刊分布：FCST 数量较多，其后包括 Applied Sciences、IEEE TKDE、IEEE Access 等
- 会议分布：ACM、ISWC、IEEE、ACL、AAAI、CCKS 等均有涉及

## 3. LLM 分类与应用角色
> 本节支撑该论文对 LLM 路线的系统综述身份，而不是单点模型比较。
- Decoder models
- Encoder models
- Encoder-decoder models
- Domain-specific models（如 BioBERT、FinBERT 等）

应用角色包括：
- feature encoder
- reasoner
- generator

## 4. 工业软件功能差距分析
> 本节支撑“为什么复杂产品设计需要 LLM-KG 协同框架”的实证背景。
论文通过工业软件分析指出：
- 现有工业软件在需求分析、概念设计、具身设计、测试验证等阶段都存在规则驱动、人工解释、跨域知识整合不足的问题。
- LLM-KG 技术被用来填补数据理解、知识关联、推理解释和自动化建议等能力缺口。

## 5. 分阶段任务支持证据
> 本节支撑该论文关于 design task layer 的场景落地分析。
覆盖阶段包括：
- Requirement analysis
- Conceptual design
- Embodiment design
- Prototyping & testing

每阶段都强调 KG 与 LLM 在知识获取、需求映射、参数匹配、推理验证、报告生成等方面的协同作用。

## 6. 优势、局限与未来方向
> 本节支撑 survey 论文最重要的综合结论。
### 优势
- 知识整合与动态共享
- 自动化与决策效率提升
- 更深语义理解与可解释推理
- 动态适应与知识演化
- 更自然的人机协同
- 跨领域知识复用

### 局限
- 大模型迁移成本
- 可解释性与透明性问题
- KG 更新维护难题
- 数据采集与合规约束

### 未来方向
- 更强可解释 AI 与可视化
- 实时知识更新与反馈闭环
- 领域知识与专家协同治理
- 合规的数据获取与共享机制

## 7. 为什么这篇论文验证了规范需要优化
> 本节直接服务你这次“验证通用性并优化规范”的目标。
- 当前 `analysis.md` 命名更适合 survey / framework 论文的第三类证据缓存。
- survey 论文缺少统一 benchmark，不适合强行绑定 `WebQSP` / `CWQ` 类节点。
- 更需要 framework / taxonomy / scenario / synthesis 类型节点支持。
- 说明现有规范可覆盖 survey，但应进一步抽象出 survey 专门模板与缓存约定。
