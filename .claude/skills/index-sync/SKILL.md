---
name: index-sync
description: 在 `page-projection-sync` 完成后，把对象页与 index 层之间的投影补齐到对象域导航与受管导航页：更新 `ontology/entities/*/index.md` 与其他显式受管导航页的受管区块，并输出 `synced_indexes`、`skipped_pages` 与 `manual_followups`。仅当编排型 skill `process-paper` 已将当前任务推进到 index sync 阶段，或用户明确要求只刷新 index / 受管导航页、或判断哪些页面可被索引但暂不应 default serve 时，才应使用本 skill；不要把它当作“处理论文”完整请求的默认入口。
---

# Index Sync

你是 ResearchKB 的 navigation index synchronization stage。你的任务是在对象页真相已经同步后，把可安全收录的页面投影到导航面。

## 链路位置
本 skill 是单篇论文编译链中的 index sync 阶段，默认前置为 `page-projection-sync`。
默认由编排型 skill `process-paper` 在对象页 projection 完成后调用；当用户明确要求只刷新 index / 受管导航页时，也可直接使用本 skill。

## 自动同步内容
1. `ontology/entities/*/index.md` 中的 `core-entry`、`grouped-navigation` 与 `canonical-list` 受管区块
2. relation-ledger 导航受管区块
3. 其他被显式声明为受管的域级 / 关系级导航页

对象域入口项不再使用自由 trailing hook prose。每个对象入口项必须从对象页真源投影：
- object_path
- object_wikilink
- object_semantics
- status

## 不自动同步
- 对象页解释性正文
- relation ledger 实例边正文
- index 页的人类导读、综述判断与非受管备注

## 输入
- `page-projection-sync` 输出的 `projected_pages` / `manual_followups`
- 当前对象页集合
- 当前 index 页内容
- 受控 frontmatter 与 `## Formal relations` 结构

输入约束：
- `projected_pages` 是 `page-projection-sync` 的唯一主交接字段；不要继续使用 `synced_pages`。

## 真源
- 页面存在性
- 节点类型所需 frontmatter
- 足以判断导航归属的稳定结构

## 收录规则
- 页面可被 index 收录，不等于页面可作为默认 serving 入口
- `placeholder`：只进入 non-serving block
- `placeholder` Paper 只进入 non-serving block，并作为 `Paper Stub / Anchor` 理解；它承担 relation / provenance 锚点职责，但不自动进入默认 paper serving 入口。
- cited-work placeholder paper 被后续正式 ingest 之前，应保持原路径并原地升级，而不是新建第二个 Formal Paper 页面。
- `partial`：Method 页可进入默认导航入口；其他类型仍可被 index 收录但不自动等同 serving-ready
- `serving-ready`：进入默认导航入口
- 对于 Method 类型，`status: partial` 一旦被 index 收录，即视为可导航对象页，不再额外降级到 placeholder 区块。
- survey-derived `status: partial` Method 默认进入 Methods index 的默认导航入口。
- survey-derived representative paper stubs 默认进入 Papers index 的 non-serving block。
- 仅因其承担 survey-derived method provenance 而创建的 paper stub，不得自动提升为 papers index 默认入口。
- non-default-serving 收录块与 `partial` 导航入口并不天然代表“有问题的页面”；它们也可能是当前规范允许的合法服务层中间状态，供 serving-governance 在后续阶段按上下文判断，而不是自动视为待修复信号。
- 若页面缺少安全收录所需结构，应跳过并记录 followup
- 不得通过猜测补齐分组或伪造入口状态

## 受管区块
- 只允许更新 `<!-- BEGIN MANAGED BLOCK:... -->` 与 `<!-- END MANAGED BLOCK:... -->` 之间的内容
- 不得重写区块外 prose
- 当前先覆盖 `ontology/entities/*/index.md` 与其他显式受管导航页

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_indexes:
  - path: ontology/entities/papers/index.md
    updated_blocks:
      - core-entry
skipped_pages: []
manual_followups: []
```
