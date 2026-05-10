---
name: index-sync
description: 在 `page-projection-sync` 完成后，把对象页与 index 层之间的投影补齐到对象域导航与受管导航页：更新 `ontology/entities/*/index.md` 与其他显式受管导航页的受管区块，并输出 `synced_indexes`、`skipped_pages` 与 `manual_followups`。Whenever 对象页 formal projection 已完成且需要刷新对象域 index、关系域受管导航页、或判断哪些页面可被索引但暂不应 default serve 时，都应使用本 skill。
---

# Index Sync

你是 ResearchKB 的 navigation index synchronization stage。你的任务是在对象页真相已经同步后，把可安全收录的页面投影到导航面。

## 链路位置
本 skill 是单篇论文日常编译链的第四阶段，默认前置为 `page-projection-sync`。
本 skill 完成后不视为流程结束，而应继续进入结构治理、本体语义治理与 serving 治理。

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
- `page-projection-sync` 输出的 `synced_pages` / `manual_followups`
- 当前对象页集合
- 当前 index 页内容
- 受控 frontmatter 与 `## Formal relations` 结构

## 真源
- 页面存在性
- 节点类型所需 frontmatter
- 足以判断导航归属的稳定结构

## 收录规则
- 页面可被 index 收录，不等于页面可作为默认 serving 入口
- `placeholder`：只进入 non-serving block
- `partial`：Method 页可进入默认导航入口；其他类型仍可被 index 收录但不自动等同 serving-ready
- `serving-ready`：进入默认导航入口
- 对于 Method 类型，`status: partial` 一旦被 index 收录，即视为可导航对象页，不再额外降级到 placeholder 区块。
- 若页面缺少安全收录所需结构，应跳过并记录 followup
- 不得通过猜测补齐分组或伪造入口状态

## 受管区块
- 只允许更新 `<!-- BEGIN MANAGED BLOCK:... -->` 与 `<!-- END MANAGED BLOCK:... -->` 之间的内容
- 不得重写区块外 prose
- Phase 1 先覆盖 `ontology/entities/*/index.md` 与其他显式受管导航页

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

## 完成后的默认后继阶段
1. `python3 scripts/lint_graph.py`
2. `ontology-semantic-review`
3. `serving-governance-review`
