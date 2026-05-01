# Graph Standard

## 节点类型
- Paper：论文实例节点
- Method：方法节点
- Concept：概念节点
- Framework：当论文的核心贡献是分层框架、角色划分或 taxonomy 时，可优先以概念页或独立框架页承载
- Task：研究任务节点
- Scenario：应用场景节点
- Benchmark：数据集或评测基准节点
- Evidence：`intermediate/` 下的结构化证据缓存

## 关系类型
- `proposes`：论文提出方法
- `uses_concept`：论文或方法依赖概念
- `targets_task`：论文或方法面向任务
- `applies_to`：方法应用于场景
- `evaluated_on`：论文或方法在基准上评测
- `improves_on`：方法改进已有方法
- `based_on`：方法基于上游范式或方法
- `cites`：论文引用论文
- `supported_by`：正式知识页由证据缓存支撑
- `sourced_from`：知识页或缓存来源于原始 PDF

## 节点判定规则
- 核心方法：在论文贡献、方法或实验章节中被独立描述，并直接支撑主要结论的方法。
- 关键上游工作：被当前论文作为方法借鉴、强基线对比、理论基础或路线分界点反复引用的工作。
- 高价值悬空节点：虽然尚未正式落库，但已在多个页面中重复出现、或是方法演化链关键节点、或是多个方法共享的共同基线。
- 高频出现：默认指在 3 个及以上正式知识页或关系页中被显式链接。

## 论文类型与豁免规则
- empirical 论文：默认需要任务、benchmark、实验结果与引用关系的完整绑定。
- theoretical / position 论文：若无实验或 benchmark，可豁免 benchmark 节点与 experiments 缓存，但仍需绑定核心方法、概念、上游工作与证据来源。
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- framework / taxonomy 论文：若主要贡献是分层框架、角色划分或研究地图，可优先把核心知识落到 concept / framework / scenario / synthesis，而不是强制抽取单一方法页。
- 如某篇论文不适合完整满足默认最小链接义务，应在页面或缓存中显式写明缺省原因，避免形式化凑数。

## 最小链接义务
- 论文页通常至少链接：1 个方法、1 个概念、1 个任务或场景、2 个相关论文或方法、1 个证据缓存；若知识库仍处于早期阶段，可先满足核心一跳关系并在后续 ingest 中补齐。
- 方法页通常至少链接：1 篇代表论文、1 个父方法或上游范式、1 个子方法或对比方法、1 个概念、1 个任务或场景；若上下游节点尚未正式落库，可先保留明确占位说明。
- 概念 / Framework 页至少链接：1 篇论文、1 个相关任务或场景、1 个关系页或证据页；若承担框架型主落点，可不强制绑定单一方法页。
- 场景页至少链接：1 个任务、2 个方法或框架 / 概念节点、1 篇论文。
- Task / Benchmark 页至少链接：2 个论文或方法 / 框架节点、1 个场景或概念；若当前只有单条主线，可先围绕主线节点建立最小可视网络。
- Evidence 缓存页必须回链正式论文页，并链接关键方法、概念、任务与基准；对于 survey / framework 论文，可用“统计 / 分层 / 综述证据”替代统一 benchmark 结果。

## 链接质量要求
- `[[wikilink]]` 不是计数项，链接必须附带最小关系语义说明，例如“提出 / 对比 / 应用 / 支撑 / 验证 / 关联任务”。
- 论文页若同时涉及同名论文节点与方法节点，应优先使用带别名或带路径的写法消歧。
- 当对象尚无正式方法页、但必须保留关系时，应使用占位论文页或占位说明，而不是伪造方法节点。

## 证据要求
- 方法机制优先绑定 `sections.md` 或 `full.md`。
- empirical 论文的实验结果优先绑定 `experiments.md`。
- 引用与基线关系优先绑定 `refs.md`。
- 对 survey / benchmark / framework / taxonomy / dataset 论文，第三类缓存默认使用 `analysis.md`，用于承载统计、landscape、阶段分析、software-gap 分析或 framework 支撑证据。
- 原始 PDF 仅作为最终来源，不直接承担主图谱组织职责。

## 关系索引
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
