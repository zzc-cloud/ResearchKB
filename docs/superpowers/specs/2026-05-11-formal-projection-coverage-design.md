# Formal Projection Coverage Enforcement Design

日期：2026-05-11

## 1. 目标

收紧 ResearchKB 当前 formal relation → object page 投影链路，使其满足以下原则：

1. 只要 formal relation ledger 中存在一条合法 instance edge，且该 edge 的 source / target 对应对象页已经存在，就必须把该 edge 投影到对象页。
2. 对象页投影必须保持双侧结构：
   - source 页承接 `### Outgoing`
   - target 页承接 `### Incoming`
3. `status: placeholder` / `status: partial` 不再构成跳过 formal projection 的理由。
4. lint 必须直接基于 relation ledger 真源校验对象页 projection 完整性，而不是只靠正文 wikilink 侧面发现缺口。
5. `RawSource` 这类非对象页 target 必须被显式豁免，不被误当作普通对象页 projection 缺失。

本设计的重点不是重写 projection compiler，而是补全当前编译链合同、placeholder 分层语义与 lint 守门，使 formal graph truth 到对象页 serving surface 的覆盖变成可执行约束。

## 2. 当前问题

PathMind dry run 暴露出一个明确漏洞：

- relation ledger 中的 `cites` instance 已经存在；
- source 论文页正确写回了 outgoing projection；
- target cited paper placeholder 页被创建出来了；
- 但这些 target placeholder 页没有写回 `## Formal relations` / `### Incoming`；
- lint 也没有把这类缺口显式拦下。

全量排查当前 ledgers 后，问题分布呈现出明确模式：

- `cites`：11/11 条 target placeholder paper 缺 formal projection；
- `proposes` / `references_method` / `targets_task` / `evaluated_on` / `supported_by`：当前未发现同类问题；
- `sourced_from` 看似异常，但根因是 target 为 RawSource 文件路径而非普通对象页，属于豁免对象，不是同类 serving 问题。

这说明当前不是所有 relation type 都失效，而是：

> **formal-bearing placeholder paper targets 没有被纳入严格 projection 合同。**

更具体地说，当前存在三个断点：

1. `relation-reconciliation` 只要求输出 `affected_pages`，但没有明确要求 source 与 target 对象页必须同时纳入。
2. `page-projection-sync` 虽然要求双侧 projection，但对 placeholder / stub 页的 formal-bearing 合同不够明确。
3. `lint_graph.py` 只在页面已经存在 `## Formal relations` 时校验 projection contract，导致“已有 formal edge，但页面无 formal block”的情况漏检。

## 3. 设计原则

本设计采用以下原则：

### 3.1 ledger truth 优先
- relation ledger 是 formal instance edge 的唯一真源。
- 对象页 projection 是 ledger truth 的服务层投影，而不是可选补充。

### 3.2 页面存在性优先于状态
- 只要 source / target 对应对象页文件存在，就必须校验并维护 formal projection。
- `processed` / `partial` / `placeholder` 只影响 serving readiness，不影响 formal projection 义务。

### 3.3 双侧投影是对象页合同，不是 relation 双向化
- formal relation 仍然只在 ledger 中记录单向 instance edge。
- target 页上的 `Incoming` 是同一条 edge 的镜像 serving projection，不构成反向 formal edge。

### 3.4 placeholder 允许 non-serving，但不允许 formal blind spot
- placeholder 可以不是默认 serving-ready 页面；
- 但一旦它已经承接 formal relation，就不能再缺失 formal projection。

### 3.5 非对象页 target 必须显式豁免
- `RawSource` 文件路径、受管 PDF、以及未来类似非对象页 target，不应被误纳入普通对象页 projection 合同。
- 豁免必须是显式的类型规则，而不是靠 lint 误判后人工解释。

## 4. 总体方案

采用方案 C：

1. **收紧 relation-reconciliation 输出合同**：任何 formal edge 的 source / target 对象页都必须纳入 `affected_pages`。
2. **收紧 page-projection-sync placeholder 合同**：只要对象页存在且承接 formal relation，就必须写 `## Formal relations`、`### Outgoing`、`### Incoming`。
3. **在 lint 中新增 ledger → object page 对账**：直接逐条校验 source / target 投影是否存在，并为 placeholder formal-bearing 页提供显式报错。
4. **保留 RawSource 等特殊 target 的明确豁免**。

本方案不新增新主阶段，不重写 relation ledger canonical 格式，也不修改 index-sync 的核心职责；它只补 formal projection coverage 合同与可执行守门。

## 5. relation-reconciliation 合同调整

目标文件：
- `.claude/skills/relation-reconciliation/SKILL.md`

### 5.1 `affected_pages` 的新定义
当前 `affected_pages` 只被描述为“受影响对象页列表”，定义不够严格。

改为：

- 对每条新增或已确认存在的 formal relation instance：
  - 若 `source_path` 指向对象页，则该页必须加入 `affected_pages`
  - 若 `target_path` 指向对象页，则该页必须加入 `affected_pages`
- 不区分页面状态：`processed` / `partial` / `placeholder` 都必须纳入
- `affected_pages` 去重后输出

### 5.2 `affected_stub_pages` 的角色
- `affected_stub_pages` 继续保留，用于显式标记 stub / partial / placeholder 页面
- 但它只能作为辅助分类，不能替代 `affected_pages`
- 任何出现在 `affected_stub_pages` 中的对象页，如果它承接了 formal edge，也必须同时出现在 `affected_pages`

### 5.3 与 cited placeholder papers 的关系
- 对于 `cites` 指向的 placeholder paper target：
  - 创建页面只是第一步
  - 该页面必须进入 `affected_pages`
  - downstream 不得只同步 source 论文页而跳过 cited target page

### 5.4 输出契约建议补语
建议在 skill 中显式写出：

> `affected_pages` must include both source and target object pages for every reconciled formal relation instance whose corresponding page file exists.

这样可以把当前 “只同步 source 页” 从隐含假设转为明确违约。

## 6. page-projection-sync 合同调整

目标文件：
- `.claude/skills/page-projection-sync/SKILL.md`

### 6.1 新的基础规则
新增明确规则：

- 只要对象页存在，且它在 current formal ledger 中作为任一 instance edge 的 source 或 target 出现，就必须生成 formal projection。
- 该规则对 `processed` / `partial` / `placeholder` 一视同仁。

### 6.2 placeholder 分层语义
将 placeholder 页区分为两类：

#### A. 纯占位页
- 页面存在，但尚未承接 formal relation instance
- 允许仅保留最小骨架：
  - `status: placeholder`
  - `## 当前定位`
  - `## 与知识库现有内容的关系`
  - `## 待补充`

#### B. formal-bearing placeholder 页
- 页面已经是某条 formal relation 的 source 或 target
- 即使仍为 `status: placeholder`，也必须具备：
  - `## Formal relations`
  - `### Outgoing`
  - `### Incoming`
  - 与当前 formal neighbor set 一致的正文 wikilink 约束

### 6.3 双侧 projection 合同
对于任何 formal-bearing 对象页：
- 必须保留 `### Outgoing` 与 `### Incoming`
- 对应侧无实例时必须显式写 `- 无`
- 不允许只写单侧而省略另一侧标题

### 6.4 与 semantic stub / partial 的关系
- 当前 skill 已支持 semantic stub / partial 页最小语义骨架
- 本次不改变这部分主方向
- 只增加一条更严格的规则：
  - **有 formal relation truth 的 stub/placeholder/partial 页，必须同时具备 formal projection**

### 6.5 RawSource 豁免
- 若 target 是 `ontology/entities/raw-sources/files/*.pdf` 这类 RawSource 文件路径：
  - source Evidence 页仍必须投影 outgoing `sourced_from`
  - target 不要求拥有对象页式 `Incoming`
- 该豁免必须写入 skill，避免 downstream 把 RawSource 文件误当普通对象页

## 7. lint 守门设计

目标文件：
- `scripts/lint_graph.py`

### 7.1 新增 ledger → object page coverage 校验
在现有结构校验、projection contract 校验之外，新增一层直接基于 relation ledger 的逐边对账：

对每条 canonical relation instance record：
- 读取 `source_path`
- 读取 `target_path`
- 读取 relation type

然后执行：

#### source 校验
若 `source_path` 指向正式对象页：
- 页面必须存在 `## Formal relations`
- 页面 `### Outgoing` 中必须存在对应 relation instance 的投影项
- 否则报错：
  - `missing Formal relations on source page for ledger edge`
  - 或 `missing outgoing projection for ledger edge`

#### target 校验
若 `target_path` 指向正式对象页：
- 页面必须存在 `## Formal relations`
- 页面 `### Incoming` 中必须存在对应 relation instance 的投影项
- 否则报错：
  - `missing Formal relations on target page for ledger edge`
  - 或 `missing incoming projection for ledger edge`

#### 非对象页 target 豁免
若 `target_path` 指向 RawSource / PDF / 非对象页目标：
- 不要求 target projection
- 只要求 source outgoing 正确

### 7.2 “存在对象页”优先于 status
新的 lint 规则不依据 `status: placeholder|partial|processed` 决定是否校验 formal projection。

改为：

> 只要 ledger 指向的对象页文件存在，就必须校验 formal projection。

这样：
- `placeholder` 不再绕过 formal coverage 守门
- `partial` 也不能绕过
- 页面状态只用于 serving 层分级，而不是 graph truth 投影豁免

### 7.3 对账键
本次 lint 对账最小实现建议按以下键匹配：
- relation type
- 邻接对象 document path
- 方向（Outgoing / Incoming）

这可以保证：
- source 页不会把应在 incoming 的关系写错到 outgoing
- target 页不会只出现“同对象有链接”却缺 relation type

`edge_semantics` 和 `evidence` 仍沿用现有字段存在性校验；本次不要求先做全文级精确字符串对账，以避免 lint 过脆。

### 7.4 placeholder 专门报错
新增一条对 formal-bearing placeholder 页的显式错误：

- 若某个 `status: placeholder` 的对象页在任一 relation ledger 中出现为 source 或 target，
- 但页面缺少：
  - `## Formal relations`
  - `### Outgoing`
  - `### Incoming`
- 则直接报：
  - `formal-bearing placeholder page missing formal relations contract`

这能让当前 `cites` target placeholder 漏洞在 lint 输出中一眼可见，而不是等正文 wikilink 或 serving review 旁敲侧击。

### 7.5 现有正文 wikilink 校验的角色调整
保留现有：
- 正文 wikilink 必须是 `Formal relations` 的子集
- Evidence 正文不允许直链 Paper

但它们改为第二道门：
- 第一层是 ledger → page formal coverage 校验
- 第二层才是正文一致性校验

这样即使某页正文没有任何 wikilink，也不能再靠“静默无正文链接”逃过 formal projection 缺失问题。

## 8. 规范层调整

目标文件：
- `ontology/graph-standard.md`

### 8.1 Formal-bearing placeholder 合同
需要在 placeholder / partial 相关规则中补一条明确规范：

- `status: placeholder` 仅表示对象尚非 default serving-ready entry
- 若该页已经承接 formal relation instance，则必须具备 formal projection 合同
- formal projection 合同至少包括：
  - `## Formal relations`
  - `### Outgoing`
  - `### Incoming`
  - 空侧显式 `- 无`

### 8.2 页面存在性优先
需要补充：

- formal relation 投影义务由“页面是否存在 + 是否承接 formal relation”决定
- 而不是由页面状态决定

### 8.3 RawSource 豁免说明
在 `sourced_from` 或 projection 契约附近补充：
- RawSource 文件是 provenance target，不进入普通对象页双侧 projection 合同
- 但 source Evidence 页仍必须维护 outgoing `sourced_from`

## 9. 回归与质量清单调整

目标文件：
- `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- `.claude/skills/page-projection-sync/evals/regression-samples.json`
- `.claude/skills/relation-reconciliation/evals/regression-samples.json`

### 9.1 需要新增的回归样例
至少新增两类：

#### A. cited placeholder paper target
- 给定：`Paper --cites--> Placeholder Paper`
- 预期：
  - source 页有 outgoing `cites`
  - target placeholder paper 页有 incoming `cites`
  - target placeholder 页拥有 `## Formal relations`

#### B. sourced_from RawSource target
- 给定：`Evidence --sourced_from--> RawSource PDF`
- 预期：
  - source Evidence 页有 outgoing `sourced_from`
  - 不要求 RawSource 文件作为对象页承接 incoming

### 9.2 quality checklist 补项
补充显式核查项：
- `affected_pages` must include both source and target object pages
- placeholder pages that bear formal relations must still receive `Formal relations` projection
- RawSource targets are exempt from object-page incoming projection

## 10. 实现范围

本设计预计修改以下文件：

- `ontology/graph-standard.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `scripts/lint_graph.py`
- `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- `.claude/skills/page-projection-sync/evals/regression-samples.json`
- `.claude/skills/relation-reconciliation/evals/regression-samples.json`

## 11. 明确不做的事

本次设计不包含：

- 重写 relation ledger canonical 格式
- 新增独立 projection compiler 脚本
- 批量自动修复所有已坏对象页内容
- 改写 index-sync 主逻辑
- 改 serving-ready / partial / legacy 的导航层级
- 修改 relation 页的治理定位

本次只做三件事：

1. **合同补全**：formal-bearing 对象页不得缺 formal projection
2. **lint 加固**：ledger truth 直接约束对象页 coverage
3. **豁免显式化**：RawSource 等非对象页 target 不再混入普通投影合同

## 12. 风险与收益

### 收益
- formal relation truth 与对象页 serving surface 的一致性变成可执行约束
- cited placeholder paper 不再成为 projection blind spot
- 后续新增 relation type 时，source-only sync 漏洞更难再次出现
- serving review 不再需要替 formal coverage 缺口兜底

### 风险
- lint 会变得更严格，短期内可能一次性暴露一批历史遗留 placeholder 页面问题
- placeholder 的“最小合同”被拆成纯占位与 formal-bearing 两类后，需要 skill 与规范保持一致，否则会产生新的语义漂移
- 若未来出现新的非对象页 target 类型，需要同步补充豁免规则，避免被误报

## 13. 推荐落地顺序

1. 先修改 `relation-reconciliation` 与 `page-projection-sync` 合同
2. 再修改 `graph-standard`，把 formal-bearing placeholder 规则写成规范
3. 然后给 `lint_graph.py` 增加 ledger → page coverage 校验与 RawSource 豁免
4. 最后补 eval checklist / regression samples

这样能保证：
- 先统一流程语言
- 再统一规范裁决
- 最后再把规则落成可执行守门

## 14. 验收标准

设计落地后，应满足以下验收条件：

1. 对每条 formal relation instance，若 source / target 对应对象页存在，则两侧 projection 均被写回。
2. cited placeholder paper target 不再出现“正文提到被引用，但无 incoming formal projection”的状态。
3. `status: placeholder` 的 formal-bearing 页面若缺 `Formal relations`，lint 必须失败。
4. `sourced_from` 指向 RawSource PDF 时，lint 不要求 target 侧对象页 projection。
5. 现有 `proposes` / `references_method` / `targets_task` / `evaluated_on` / `supported_by` 等正常关系不因新规则被误判。

## 15. 最终判断

这是一次 **formal projection coverage contract** 的收口，而不是 serving 模型重做。

它解决的是：

> ledger truth 已存在，但对象页 serving projection 没有被强制覆盖到所有已存在对象页。

通过把 source+target 覆盖写入 reconciliation 与 sync 合同，再由 lint 直接对账 ledger truth，本设计能把当前 `cites -> placeholder paper target` 暴露出的局部漏洞，上升为全链路可执行的通用约束。
