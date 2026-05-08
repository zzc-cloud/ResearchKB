# CLAUDE Root Navigation Consolidation Design

- 日期：2026-05-06
- 状态：已确认设计，待 spec 审阅
- 范围：把系统级本体导航从 `ontology/index.md` 收束到 `CLAUDE.md`，并移除 `ontology/index.md` 作为默认入口与仓库对象

## 1. 背景

当前 ResearchKB 的系统级导航职责分散在两处：
- `CLAUDE.md` 负责说明全局工作流、查询顺序与默认读取策略
- `ontology/index.md` 负责列出规范层、对象层、关系层、证据层这些稳定入口

但在当前状态下，`ontology/index.md` 已经不再承担独立的判定逻辑或复杂导航编排，主要只是在重复表达“系统有哪些入口层、各层通向哪里”。这会带来三个问题：

1. 系统级导航认知被拆成两份，增加 agent 与人类读者的认知跳转成本。
2. skill / workflow 若要稳定依赖系统导航，还需要先约定 root index 这一额外入口对象。
3. `index-sync`、`serving-governance-review` 等技能会隐式把 `ontology/index.md` 当成一个持续存在的系统对象，导致导航契约和执行契约耦合在旧结构上。

用户本次确认的目标是：
- 把“本体是什么、系统入口层如何分工、何时下钻哪一层”统一收束到 `CLAUDE.md`
- 让后续 skill / workflow 直接依赖 `CLAUDE.md` 作为系统级导航锚点
- 在没有工具链硬依赖的前提下，直接删除 `ontology/index.md`

## 2. 设计目标

本次调整的目标如下：

1. `CLAUDE.md` 成为唯一系统级本体导航入口。
2. `ontology/graph-standard.md` 保持为唯一规范裁决依据，而不是默认导航首页。
3. `ontology/entities/*/index.md` 保持为对象域实例导航层。
4. `ontology/relations/*.md` 保持为 formal relation ledger / 治理账本层。
5. `intermediate/papers/` 保持为证据核验层。
6. `ontology/index.md` 退出默认工作流，并在迁移完成后直接删除。
7. `index-sync` 与 `serving-governance-review` 的 skill 文案同步改写，避免继续引用已删除的 root index 语义。

## 3. 非目标

本次设计不处理以下内容：
- 不修改 `ontology/graph-standard.md` 的本体规则本身
- 不重构 relation ledger 的格式或语义
- 不改写对象页正文结构
- 不改变 `page-projection-sync`、`relation-reconciliation` 的核心职责
- 不引入新的系统级导航页替代 `ontology/index.md`

## 4. 核心设计决策

### 4.1 `CLAUDE.md` 接管系统级导航职责

`CLAUDE.md` 的“本体认知”需要补齐一段系统级分层导航说明，明确以下层次及其职责：

- 规范层：`ontology/graph-standard.md`
- 对象层：`ontology/entities/*/index.md` 与 serving-ready 对象页
- 关系层：`ontology/relations/*.md`
- 证据层：`intermediate/papers/`
- 原始来源层：`raw/`

这段内容不仅要说明每一层“是什么”，还要说明：
- 默认应先进入哪一层
- 哪些问题应转向哪一层
- 何时做受约束拓扑扩展
- 何时必须回查 relation ledger 或证据层

### 4.2 `ontology/graph-standard.md` 的角色表述收窄为“规范裁决依据”

本次不再使用“唯一判定中枢”这类容易混淆入口、执行与裁决三种语义的表述。

统一改为：

> `ontology/graph-standard.md` 是唯一规范裁决依据。
> 凡涉及节点归类、关系合法性、frontmatter 受控字段、证据义务与豁免规则的描述，若与 `CLAUDE.md` 或其他导航 / 流程说明不一致，以它为准。

这样可以清楚地区分：
- `CLAUDE.md`：系统如何进入、按什么顺序读
- `ontology/graph-standard.md`：什么叫合法、冲突时如何裁决

### 4.3 `ontology/index.md` 完全退出体系并直接删除

`ontology/index.md` 不再保留为：
- 默认入口
- 兼容跳转页
- 受管导航页
- skill 的默认检查对象

删除后的系统结构中，不再存在 root ontology index 这一概念对象。

### 4.4 系统级默认读取顺序改为由 `CLAUDE.md` 直接判定

`CLAUDE.md` 的“查询与分析”段落需要从：
- 先读取 `ontology/index.md` 定位系统级导航入口

改为：
- 先依据 `CLAUDE.md` 中的本体分层导航判定当前问题属于哪一层，再进入相应层级

## 5. 新的导航角色模型

### 5.1 `CLAUDE.md`

`CLAUDE.md` 是系统级导航与任务入口判定层，负责：
- 判断当前问题是知识问答、治理、修复、摄入还是综述任务
- 判断当前问题应先进入规范层、对象层、关系层还是证据层
- 规定默认读取顺序与扩展顺序
- 规定何时读取 relation ledger、何时读取 evidence、何时才允许回看 `raw/`

它不负责：
- 定义建模合法性细则
- 列举所有实例
- 承担 formal graph truth 的账本真源职责

### 5.2 `ontology/graph-standard.md`

`ontology/graph-standard.md` 是唯一规范裁决依据，负责：
- 节点类型与建模公理
- frontmatter 受控字段
- 关系合法性
- 链接义务、证据要求与豁免规则

它不负责：
- 作为默认系统导航首页
- 作为实例导航目录
- 承担对象问答的默认阅读起点

### 5.3 `ontology/entities/*/index.md`

对象域 index 保持为对象域实例导航层，负责：
- 域内正式对象发现
- 域内默认入口组织
- 把读者导向 serving-ready 对象页

它们不负责：
- 系统级问题分流
- 建模合法性裁决
- relation ledger 真值校对

### 5.4 `ontology/relations/*.md`

relation ledger 保持为 formal relation ledger / 治理账本层，负责：
- formal graph truth 核对
- 治理、修复、审计场景下的账本检视
- 明确正式关系实例边的归属与存在性

它不负责：
- 通用知识问答的默认起点
- 系统级导航总入口

### 5.5 `intermediate/papers/`

证据层保持为机制、实验、引用、baseline、provenance 核验层。

它不负责：
- 正式对象导航
- 系统级入口分流

### 5.6 `raw/`

`raw/` 保持只读原始来源层，仅在上述层次不足以支持判断时才回查，不再视为默认导航主链的一部分。

## 6. `CLAUDE.md` 的具体改写方向

### 6.1 在“本体认知”中新增系统级分层导航说明

新增内容应覆盖：
- 系统有哪些层
- 每层的职责边界
- 默认读取顺序
- 进入 relation ledger / evidence / raw 的条件
- `ontology/graph-standard.md` 的“唯一规范裁决依据”定位

### 6.2 改写“查询与分析”段落

将现有第一步：
- 读取 `ontology/index.md` 定位系统级导航入口

改为类似：
- 先依据 `CLAUDE.md` 的本体分层导航判断当前问题应进入规范层、对象层、关系层、证据层还是原始来源层

其后的顺序应保持以下语义：
- 正式知识问答：对象域 index → serving-ready 对象页 → `Formal relations` → 必要时 Evidence
- formal graph truth / 治理 / 修复 / 审计：relation ledger 优先
- 机制、实验、引用、baseline、provenance 核验：Evidence 优先
- 只有在上述层都不足时才回看 `raw/`

### 6.3 改写 `index-sync` 在流水线中的职责描述

当前 `CLAUDE.md` 中若将 `index-sync` 描述为“把对象页与关系页的稳定结构同步到导航 index”，会让人误以为它仍维护系统总入口。

应改写为更精确的职责表述，例如：
- `index-sync` 负责把对象页投影同步到各对象域 index，并维护仍然存在的受管导航页

这要求 `CLAUDE.md` 中不再出现“root ontology index 是 index-sync 默认目标”的暗示。

## 7. skill 契约同步调整

### 7.1 `index-sync`

`index-sync` 的技能定义需要从“维护系统入口 + 域入口”改成“维护域入口与受管导航页”。

具体调整方向：
- 删除 `ontology/index.md` 作为自动同步对象
- 明确自动同步对象仅包括：
  - `ontology/entities/*/index.md` 中的受管区块
  - 仍然存在、且被明确声明为受管的域级 / 关系级导航页
- 结构化输出中的 `synced_indexes` 不再出现 `ontology/index.md`
- 技能描述不再使用“刷新系统入口”这样的措辞

新的 skill 语义应是：
- `index-sync` 维护对象页与 index 层之间的投影
- 这里的 index 层专指对象域 index 与显式存在的受管导航页
- 它不再承担系统总入口同步职责

### 7.2 `serving-governance-review`

`serving-governance-review` 需要摆脱对 root `ontology/index.md` 的默认依赖。

调整方向：
- 不再把 `ontology/index.md` 是否完整作为默认 gate 条件
- `Index navigation quality` 的检查对象收缩为：
  - `ontology/entities/*/index.md`
  - 仍然存在且被明确声明为 serving / navigation surface 的 index 页
- 重点检查：
  - 对象页是否是 serving-ready 问答入口
  - 对象页的 `Formal relations` 是否足以支持受约束扩展
  - 域内 index 是否把读者导到合适对象层
  - 治理 / 审计场景下是否能正确回到 relation ledger / evidence 层

也就是说，这个 skill 的默认判断对象应从“系统总入口 + 域入口”收窄为“默认 serving surface + 域内导航 surface”。

## 8. 删除 `ontology/index.md` 的迁移条件

虽然目标是直接推进到删除，但删除动作应以以下条件满足为前提：

1. `CLAUDE.md` 已显式接管系统级分层导航职责
2. `CLAUDE.md` 的“查询与分析”已不再引用 `ontology/index.md`
3. `index-sync` 的 skill 文案已不再把 `ontology/index.md` 视为默认投影目标
4. `serving-governance-review` 的 skill 文案已不再把 `ontology/index.md` 视为默认检查对象
5. 仓库中不存在仍要求 `ontology/index.md` 作为默认入口的运行时说明或人工流程说明

满足这些条件后，`ontology/index.md` 可直接删除，不保留兼容页。

## 9. 风险与应对

### 9.1 风险：旧 skill / 文档仍引用 root index

这是本次改动的主要风险。问题不在于文件删除本身，而在于旧文案会继续把已删除对象当成默认入口。

应对：
- 在实现中把 `CLAUDE.md`、`index-sync`、`serving-governance-review` 作为同一批契约更新
- 删除前先全仓搜索 `ontology/index.md` 与“system entry / root index / 导航入口”等旧措辞

### 9.2 风险：`graph-standard.md` 语义膨胀为导航首页

如果为了替代 root index 而把大量导航说明继续堆回 `graph-standard.md`，会重新混淆“规范裁决页”和“导航入口页”。

应对：
- 导航职责全部上移到 `CLAUDE.md`
- `graph-standard.md` 只保持规范裁决角色，不承担系统首页角色

### 9.3 风险：`index-sync` 被误读为 still owning root navigation

即使 root index 文件删除，如果 skill 定义仍然使用“刷新系统入口”等表述，后续 agent 仍会延续旧模型。

应对：
- 明确把 `index-sync` 重新命名为对象域 index / 受管导航页投影维护阶段的语义，而非系统总入口阶段

## 10. 成功标准

本次设计落地后，应达到以下状态：

1. `CLAUDE.md` 能独立完成系统级本体导航说明，无需再先跳到 `ontology/index.md`
2. `ontology/graph-standard.md` 被清晰表述为唯一规范裁决依据，而非默认系统入口
3. 对象问答默认路径为：对象域 index → serving-ready 对象页 → `Formal relations` → 必要时 Evidence
4. 治理 / 审计 / formal truth 查询默认路径为：relation ledger 优先
5. `index-sync` 与 `serving-governance-review` 的 skill 定义不再依赖 root `ontology/index.md`
6. `ontology/index.md` 被删除后，系统语义仍完整且更清晰

## 11. 与既有设计的关系

本设计会取代以下旧假设：
- 把 `ontology/index.md` 视为系统总入口的设计假设
- 把 root ontology index 视为 `index-sync` 默认维护对象的设计假设
- 把 root ontology index 视为 serving navigation gate 一部分的设计假设

它与既有导航设计不是完全无关，而是进一步收束：
- 系统级导航职责最终落在 `CLAUDE.md`
- 对象域导航职责保留在 `ontology/entities/*/index.md`
- 规范裁决职责保留在 `ontology/graph-standard.md`

## 12. 实施摘要

实现阶段应按以下顺序进行：
1. 改写 `CLAUDE.md` 的本体认知与查询/分析段落
2. 改写 `index-sync` skill
3. 改写 `serving-governance-review` skill
4. 全仓检查是否仍有 `ontology/index.md` 默认入口依赖
5. 删除 `ontology/index.md`
6. 运行结构与相关治理检查，确认导航契约已闭合
