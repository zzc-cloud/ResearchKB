# ResearchKB 索引

> 本索引采用“对象分层存储 + 多轴主题分类 + 演化关系维护”的组织方式。

## 0. 总览
- [[overview]]
- [[log]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[ontology/index|ontology]]
- [[graph-standard]]

## 1. 按研究问题

### 知识获取与构建
- [[LLM增强知识图谱]]
- [[engineering-design-knowledge-management]]

### 本体 / 模式建模
- [[ontology/index|ontology]]
- [[graph-standard]]
- [[复杂产品设计中的LLM-KG协同框架]]

### 对齐、融合与互操作
- 待补充

### 推理、查询与问答
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[PathMind|PathMind（方法）]]
- [[知识图谱推理问答]]
- [[路径优先化]]
- [[重要推理路径]]
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]
- [[WebQSP]]
- [[CWQ]]

### 表示学习与图学习
- [[PathMind|PathMind（方法）]]
- [[路径优先化]]

### 质量、治理与可信性
- 待补充

### 演化、维护与生命周期管理
- 待补充

### 评测、基准与综述
- [[WebQSP]]
- [[CWQ]]

## 2. 按方法范式

### 规则与符号方法
- 待补充

### 统计与概率方法
- 待补充

### 传统机器学习
- 待补充

### 表示学习
- [[路径优先化]]

### 图学习
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[PathMind|PathMind（方法）]]

### LLM 方法
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[PathMind|PathMind（方法）]]

### 混合方法
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[PathMind|PathMind（方法）]]

## 3. 按应用场景

### 金融
- 待补充

### 企业数据管理
- [[复杂产品设计]]
- [[engineering-design-knowledge-management]]

### 企业知识管理
- 待补充

### 智能问答与决策支持
- [[知识图谱推理问答]]
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[knowledge-graph-reasoning]]

### 其他行业
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design|LLM-KG-CPD Survey（论文）]]

## 4. 按知识对象

### 论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design|LLM-KG-CPD Survey（论文）]]

### 方法
- [[PathMind|PathMind（方法）]]

### 概念
- [[路径优先化]]
- [[重要推理路径]]
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]

### 任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]
- [[engineering-design-knowledge-management]]

### 场景
- [[知识图谱推理问答]]
- [[复杂产品设计]]

### 基准
- [[WebQSP]]
- [[CWQ]]

### 本体
- [[ontology/index|ontology]]
- [[graph-standard]]

### 关联关系
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]

### 综合分析
- 目录：`wiki/synthesis/`

## 5. 按方法演化

### 基础方法
- 待补充

### 衍生方法
- 待补充

### 集成方法
- [[PathMind|PathMind（方法）]]

### 场景化应用
- [[知识图谱推理问答]]
- [[kgqa]]

### 综述 / 基准
- [[WebQSP]]
- [[CWQ]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design|LLM-KG-CPD Survey（论文）]]

## 6. 维护约定
- 新页面优先放入对象目录，再通过 frontmatter 进入多轴分类。
- 研究问题轴是主导航，方法范式轴和场景轴用于交叉检索。
- `tags` 用于补充描述，正式分类以 frontmatter 结构化字段为准。
- 图谱规范以 [[graph-standard]] 为准，任务与证据关系分别汇总到 [[task_method_map]] 与 [[evidence_index]]。
