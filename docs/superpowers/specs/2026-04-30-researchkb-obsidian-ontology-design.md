# ResearchKB Obsidian 图谱与本体化知识库设计

日期：2026-04-30

## 1. 目标

将 `ResearchKB` 从论文笔记型 wiki 升级为本体驱动的研究认知中枢，兼顾以下目标：

- 在 Obsidian 中形成清晰、稳定、可扩展的图谱网络
- 让论文、方法、概念、任务、场景、基准之间的关系可视化、可追溯
- 为后续的结构化问答、GraphRAG / OAG、本体约束推理提供知识底座
- 将论文 ingest 流程标准化，使新增内容自动符合图谱与本体规范

## 2. 总体架构

知识库采用三层结构，并辅以显式关系层：

### 2.1 本体语义层（T-Box）

用于定义研究领域中有哪些对象、对象之间允许有哪些关系、每类节点需要满足哪些约束。

建议新增目录：`wiki/ontology/`

本体层负责定义：

- 节点类型：Paper / Method / Concept / Task / Scenario / Benchmark / Evidence
- 关系类型：proposes / uses_concept / targets_task / applies_to / evaluated_on / improves_on / based_on / compared_with / cites / supported_by / sourced_from
- 节点最小链接义务
- ingest 检查规则
- 问答时的“事实 / 事理 / 证据”分层原则

### 2.2 事实实例层（A-Box）

正式知识节点沉淀在 `wiki/` 下的对象目录中：

- `wiki/papers/`
- `wiki/methods/`
- `wiki/concepts/`
- `wiki/tasks/`
- `wiki/scenarios/`
- `wiki/benchmarks/`

这些页面是知识图谱中的主体节点。

### 2.3 证据与来源层（Evidence / Source）

用于支撑“结论从何而来、关系根据什么建立”的可追溯能力：

- `intermediate/papers/`：结构化缓存与证据页
- `raw/`：原始 PDF 来源

`intermediate/` 不只是缓存，而是正式知识页的证据支撑层；`raw/` 仅作为源材料层，不直接承担主图谱语义组织职责。

### 2.4 关系层

用于将显式关系边集中登记、维护和审计：

- `wiki/relations/citation_graph.md`
- `wiki/relations/method_evolution.md`
- `wiki/relations/concept_links.md`
- `wiki/relations/task_method_map.md`
- `wiki/relations/evidence_index.md`

## 3. 节点类型规范

### 3.1 核心知识节点

- **Paper**：论文实例节点
- **Method**：方法节点
- **Concept**：概念节点
- **Scenario**：应用场景节点
- **Task**：研究任务节点
- **Benchmark**：数据集或评测基准节点

### 3.2 支撑节点

- **Relation Hub**：关系总表页
- **Evidence Cache**：中间缓存页

## 4. 关系类型规范

统一采用受控关系语义，以保证后续问答与图谱演化的一致性。

建议采用的核心关系：

- `proposes`：论文提出方法
- `uses_concept`：论文或方法使用某概念
- `targets_task`：论文或方法面向某研究任务
- `applies_to`：方法应用于某场景
- `evaluated_on`：论文或方法在某 benchmark 上评测
- `improves_on`：方法改进某已有方法
- `based_on`：方法基于某方法或上游范式
- `compared_with`：论文或方法的对比对象
- `cites`：论文引用论文
- `supported_by`：正式知识页由某 intermediate 缓存支撑
- `sourced_from`：知识页或缓存来源于某 raw PDF

落地方式分三层：

1. **图谱层**：用 `[[wikilink]]` 建立节点连边
2. **语义层**：在正文中使用稳定句式表达关系
3. **结构化层**：在 frontmatter 中保留受控字段

## 5. 命名与消歧规范

当前知识库中，方法页与论文页可能共享短名，例如 `PathMind`。为避免歧义：

- 文件名不强制增加前缀
- 正文中使用显式别名消歧

示例：

- `[[methods/PathMind|PathMind（方法）]]`
- `[[papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind（论文）]]`

原则：

- 论文页保留完整标题，便于溯源
- 方法页保留短名，便于演化链展示
- 正文显示文本显式区分“方法 / 论文 / 概念 / 任务”等语义角色

## 6. 每类页面的最小链接义务

### 6.1 论文页必须至少链接

- 1 个 Method
- 1 个 Concept
- 1 个 Task 或 Scenario
- 2 个相关论文或方法对比对象
- 1 个 Evidence Cache

### 6.2 方法页必须至少链接

- 1 篇代表论文
- 1 个父方法或上游范式
- 1 个子方法或对比方法
- 1 个 Concept
- 1 个 Task 或 Scenario

### 6.3 概念页必须至少链接

- 1 个 Method
- 1 篇 Paper
- 1 个相关概念或关系页

### 6.4 场景页必须至少链接

- 1 个 Task
- 2 个 Method
- 1 篇 Paper

### 6.5 Task / Benchmark 页必须至少链接

- 2 个 Paper 或 Method
- 1 个 Scenario 或 Concept

### 6.6 Intermediate 缓存页必须至少链接

- 回链 1 个正式 Paper
- 链接所有已识别核心 Method / Concept / Benchmark
- 标注来源 PDF

### 6.7 Raw PDF

- 不参与主图谱语义网络
- 仅作为 `sourced_from` 的源头

## 7. 目录职责与结构建议

保留当前主结构，并做职责增强：

### 正式知识层

- `wiki/papers/`
- `wiki/methods/`
- `wiki/concepts/`
- `wiki/scenarios/`
- `wiki/tasks/`
- `wiki/benchmarks/`
- `wiki/ontology/`

### 关系与综合层

- `wiki/relations/`
- `wiki/synthesis/`

### 证据层

- `intermediate/papers/`
- `raw/`

## 8. 关系页设计

### 8.1 `citation_graph.md`

维护论文之间的 `cites` 关系。

### 8.2 `method_evolution.md`

维护方法之间的 `based_on` 与 `improves_on` 关系。

### 8.3 `concept_links.md`

维护概念之间的上位 / 下位 / 并列 / 依赖关系。

### 8.4 `task_method_map.md`

新增，用于登记：

- 哪些任务对应哪些方法
- 哪些方法在何类任务中具有代表性

### 8.5 `evidence_index.md`

新增，用于登记：

- 每篇论文页由哪些 intermediate 缓存支撑
- 核心结论的证据位于哪个缓存页

## 9. 占位节点策略

允许存在少量未正式 ingest 的引用节点，但必须分级控制。

### 9.1 必须建立占位页的情况

满足任一条件即建：

- 被 3 个以上页面引用
- 是方法演化链关键节点
- 是多个方法的共同基线
- 后续大概率会成为重点 ingest 对象

### 9.2 可暂时悬空的情况

- 仅出现 1 次
- 只是背景性提及
- 对当前研究主线不关键

### 9.3 占位页内容要求

占位页应为正式节点，但保持极简，至少包含：

- 标题
- 节点类型
- 当前定位
- 与已有节点的关系
- “待后续正式摄入”的标注

## 10. Ingest 强制检查规则

每摄入一篇论文，必须执行以下检查：

### 10.1 节点识别

必须识别并落地：

- 论文节点
- 核心方法节点
- 核心概念节点
- 任务或场景节点
- benchmark 节点
- 关键上游工作节点

### 10.2 关系补全

必须补全至少这些关系：

- Paper → Method
- Paper → Concept
- Paper → Task / Scenario
- Paper → Benchmark
- Paper → Cited Papers
- Method → Parent / Peer / Child Methods

### 10.3 证据绑定

必须将以下内容绑定到 intermediate：

- 核心方法依据
- 实验结果依据
- 引用关系依据
- 关键结论依据

### 10.4 图谱 lint

至少检查：

1. 是否存在无 `[[wikilink]]` 的孤立页
2. 是否论文页缺少 Method / Concept / Task 链接
3. 是否新增高频悬空节点
4. 是否 `relations/` 未同步更新

## 11. Obsidian 图谱使用建议

图谱优先采用“混合均衡”视角，兼顾论文、方法、概念、任务、场景和基准。

建议在 Obsidian Graph View 中按路径着色：

- `wiki/papers`：论文
- `wiki/methods`：方法
- `wiki/concepts`：概念
- `wiki/tasks`：任务
- `wiki/scenarios`：场景
- `wiki/benchmarks`：基准
- `wiki/relations`：关系页
- `intermediate/papers`：证据层

默认全局图谱用于看结构，局部图谱用于追踪某个方法、论文或概念的邻接网络。

## 12. 第一阶段实施范围

第一阶段聚焦 `PathMind` 主线，目标是先跑通一条完整链路：

- 修正 `PathMind` 相关 wiki 页面，使其满足最小链接义务
- 为任务、benchmark、本体层建立骨架
- 将 `intermediate/papers/PathMind.*` 升级为证据层页面
- 更新关系页并处理关键悬空节点
- 沉淀长期可复用的 ingest 规范

## 13. 实施顺序建议

1. 新建 `wiki/tasks/`、`wiki/benchmarks/`、`wiki/ontology/`
2. 修正现有 `wiki/` 页面之间的链接网络
3. 修正 `intermediate/` 与正式知识页之间的回链
4. 新增 `task_method_map.md` 与 `evidence_index.md`
5. 识别并处理关键悬空节点
6. 将本设计固化为后续 ingest 规范

## 14. 预期效果

实施后，ResearchKB 将具备以下能力：

- Obsidian 中形成更清晰的多类型知识图谱
- 问题可以沿“实体 → 关系 → 证据”路径追溯回答
- 新论文 ingest 不再是孤立建页，而是自动并入统一认知网络
- 知识库从“研究资料仓库”升级为“本体驱动的研究认知中枢”
