# Relation-Type Ledger Architecture Redesign

- 日期：2026-05-06
- 状态：已确认设计，待 spec 审阅
- 范围：把 `ontology/relations/` 从按关系簇 / 账本职责组织，重构为按单一 relation type 组织的正式 ledger 体系

## 1. 背景

当前 `ontology/relations/` 采用混合式组织：
- 有的 ledger 文件已经接近单关系，例如 `paper_method_links.md`、`benchmark_links.md`
- 有的 ledger 文件承载多个关系类型，例如 `concept_links.md` 中混合维护 `uses_concept`、`supports`、`depends_on`，以及补充语义边；`method_evolution.md` 同时维护 `based_on` 与 `improves_on`

这种结构虽然能表达治理分工，但会给 AI 带来一个明确问题：
- 在 `CLAUDE.md` 中，AI 能理解 relation semantics，例如 `proposes`、`uses_concept`、`supported_by`
- 但进入 relations 层时，AI 仍需额外记住“这个 relation type 实际归属哪个 ledger 文件”

换句话说，当前结构缺少：

> relation type → formal ledger file

的直观一一映射。

用户本次确认的目标是：
- relation ledger 体系应以“结构最清晰”为优先目标
- 每种 relation type 都应有自己的正式 ledger 文件
- 让 AI 能直接从 relation semantics 映射到同名 formal truth source

## 2. 设计目标

1. `ontology/relations/` 重构为按 relation type 1:1 组织。
2. 每个正式 relation type 都有且只有一个正式 ledger 文件。
3. 旧的簇型 ledger 文件退出正式真源体系。
4. `CLAUDE.md`、`ontology/graph-standard.md`、skill、lint、page projection、对象页引用都与新的 relation-type ledger 体系对齐。
5. relation semantics、ledger file、formal truth source 三者形成稳定一一映射。

## 3. 非目标

- 不在本轮保留长期新旧双轨 ledger 体系
- 不新增第二套 formal truth source
- 不把 relation ledger 文件扩写为新的规范真源
- 不在本轮引入新的 relations 总索引页作为必须对象

## 4. 目标信息架构

重构后，`ontology/relations/` 中的正式 ledger 文件为：

- `cites.md`
- `proposes.md`
- `based_on.md`
- `improves_on.md`
- `targets_task.md`
- `uses_concept.md`
- `depends_on.md`
- `supports.md`
- `applies_to.md`
- `evaluated_on.md`
- `supported_by.md`
- `sourced_from.md`

核心规则为：

> 每个正式 relation type 都有且只有一个正式 ledger 文件。

这使 AI 可以直接建立：
- relation semantics
- relation file
- formal truth source

三者的一一映射。

## 5. 旧账本替代关系

### 5.1 直接拆解的旧账本

- `ontology/relations/method_evolution.md`
  - 拆为：`based_on.md`、`improves_on.md`

- `ontology/relations/concept_links.md`
  - 拆为：`uses_concept.md`、`depends_on.md`、`supports.md`、`applies_to.md`

- `ontology/relations/paper_method_links.md`
  - 重构为：`proposes.md`

### 5.2 基本 1:1 但建议重命名统一的旧账本

- `citation_graph.md` → `cites.md`
- `task_method_map.md` → `targets_task.md`
- `benchmark_links.md` → `evaluated_on.md`
- `evidence_index.md` → `supported_by.md`
- `provenance_links.md` → `sourced_from.md`

重构后，不再混用：
- 语义簇命名
- 业务命名
- relation type 命名

而统一采用 relation type 命名法。

## 6. 影响面

### 6.1 规范层
必须修改：
- `ontology/graph-standard.md`

需要把当前“关系文件分工”从按簇组织，改成：
- 每个 relation type 对应唯一 ledger 文件
- 每个 ledger 文件名直接等于 relation type

### 6.2 全局认知层
必须修改：
- `CLAUDE.md`

需要更新：
- relation semantics 与 ledger file 的衔接方式
- 正式关系入口列表
- relation type → file 的认知映射

### 6.3 关系实例层
必须修改：
- `ontology/relations/*.md`

需要：
- 创建新的 relation-type ledger 文件
- 迁移旧文件中的实例边
- 让新文件成为唯一正式真源

### 6.4 对象页 / Evidence 投影层
需要修改：
- `ontology/entities/**`
- `intermediate/papers/**`

原因：
- 直接引用旧 ledger 文件名的地方需要改到新 relation-type 文件
- Formal relations 的上游真源模型已变化

### 6.5 skill 与流程层
必须修改：
- `relation-reconciliation`
- `page-projection-sync`
- `index-sync`
- `serving-governance-review`
- `paper-ingest`

原因：
- relation 分发、projection、serving review、ingest 合约都对旧 ledger 文件名和旧归属模型有依赖

### 6.6 lint / 脚本层
必须修改：
- `scripts/lint_graph.py`

原因：
- 它当前硬编码旧 ledger 文件名和旧分工规则

## 7. 迁移顺序与过渡策略

本次重构采用：

> 先改规范与认知，再迁真源，再改技能与脚本，最后清理旧文件。

### 阶段 1：更新规范与全局认知
修改：
- `ontology/graph-standard.md`
- `CLAUDE.md`

目标：
- 先定义新 relation-type ledger 架构
- 让 AI 认知层与规范层先对齐

### 阶段 2：创建新的 relation-type ledger 文件
在 `ontology/relations/` 下创建 12 个 relation-type ledger 文件。

目标：
- 先准备好新的真源容器
- 每个文件都具备统一页头与最小语义说明

### 阶段 3：迁移实例边
把旧 ledger 中的实例边迁移到新的 relation-type 文件：
- `concept_links.md` → `uses_concept.md` / `depends_on.md` / `supports.md` / `applies_to.md`
- `method_evolution.md` → `based_on.md` / `improves_on.md`
- `paper_method_links.md` → `proposes.md`
- 其余旧文件迁到对应 relation-type 文件

目标：
- 完成 formal truth source 迁移
- 从该阶段起，新 relation-type 文件成为正式真源

### 阶段 4：更新 skill 与脚本
修改：
- relation reconciliation
- page projection
- serving review
- ingest
- lint

目标：
- 写入 / 读取 / 校验路径全部转向新的 relation-type ledger

### 阶段 5：更新对象页 / evidence / 文档引用
处理旧 ledger 文件名引用。

### 阶段 6：删除旧 ledger 文件
只有在：
- 真源已迁移
- skill 已切换
- lint 已切换
- 对象页 / evidence 引用已切换

后，才删除旧簇型 ledger 文件。

### 过渡策略
本轮不建议长期双轨。
可以短暂保留旧文件作为迁移过渡壳，但：
- 旧文件不得继续承载正式实例边正文
- 新 relation-type 文件一旦承接实例边，即成为唯一正式真源

## 8. relation-type ledger 文件统一模板
每个新 relation ledger 文件应同时承担：
1. 该 relation type 的正式真源账本
2. 该 relation type 的治理 / 修复 / 审计读取面
3. 该 relation type 的最小语义说明页

### 统一结构

#### A. 页头说明
- 本页是正式关系账本：维护某 relation type 实例边
- 默认问答优先读取对象页；治理、修复、审计、真源核对时优先读取本页
- 相关对象域
- 相关证据入口

#### B. 关系语义说明
- 说明该 relation type 表达什么语义
- 说明常见 source / target 组合
- 如易混淆，说明与邻近 relation type 的区别

#### C. 实例边正文
采用 canonical 格式：

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: ...
  - evidence: [[...]]
```

#### D. 可选边界说明
- 当前不承载哪些语义
- 哪些对象关系虽然 prose 上存在，但不应在该 ledger 落 formal edge

### 关键原则
relation-type ledger 文件里保留最小语义说明，但不复制 `graph-standard.md` 的完整规范。

- `ontology/graph-standard.md` 负责规范裁决
- `CLAUDE.md` 负责 AI 认知层语义与入口说明
- 各 relation ledger 文件只负责该 relation type 的最小语义说明 + 真源账本身份说明

## 9. 风险与规避策略

### 9.1 双真源错觉
风险：
- 新 relation-type 文件已有实例边，但旧簇型文件仍保留正式实例边正文

规避：
- 新文件一旦承接实例边，即成为唯一正式真源
- 旧文件过渡期只允许保留迁移提示或空壳说明，不允许继续承载正式实例边正文

### 9.2 关系语义分裂
风险：
- `CLAUDE.md`、`graph-standard.md`、relation ledger 页头给出不同关系定义

规避：
- `graph-standard.md` 负责规范裁决
- `CLAUDE.md` 负责认知与入口
- relation ledger 页头只作最小语义说明，不另起规范

### 9.3 拆解 `concept_links` 时丢失概念网络语义背景
风险：
- 机械拆分后，原本共享的概念网络语义背景消失

规避：
- 在 relation-type ledger 页头中写相关对象域
- 在 `CLAUDE.md` 和 `graph-standard.md` 中保留上层关系语义说明
- 真源按 relation type 拆，认知层仍允许按语义簇理解

### 9.4 skill 与 ledger 迁移不同步
风险：
- skill 继续写旧账本，或 lint 继续校验旧账本

规避：
- 新 relation-type ledger 文件、relation 分发规则、projection 规则、lint 校验规则视为同批切换对象

### 9.5 对象页投影失配
风险：
- ledger 已换，但对象页 `Formal relations` 或派生字段仍使用旧模型

规避：
- relation ledger 重构后，必须重新跑 page projection，以新 relation-type ledger 为上游重建对象页投影

### 9.6 文件名清晰但 relations 目录可浏览性变差
风险：
- 文件变多后，人工或 AI 需要先知道自己要找什么 relation

规避：
- 在 `CLAUDE.md` 中维护 relation type → file 的认知入口列表
- 每个 relation-type ledger 页头都列相关对象域
- 如未来需要，可再单独设计 `ontology/relations/index.md`，但不是本轮必须对象

## 10. 成功标准

1. 每个正式 relation type 都有且只有一个正式 ledger 文件。
2. 旧簇型 ledger 不再承载正式实例边正文。
3. `CLAUDE.md`、`graph-standard.md`、skill、lint、projection 规则都与 relation-type ledger 体系对齐。
4. AI 可以直接从 relation semantics 映射到同名 ledger 文件。
5. 迁移完成后，formal truth source、认知入口、运行时执行链三者重新闭合。
