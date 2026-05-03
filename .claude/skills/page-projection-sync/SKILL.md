---
name: page-projection-sync
description: 在 formal relation ledger 更新后，把最新 ledger 投影同步回对象页：更新 `Formal relations`、强一致 frontmatter 和模板化人类关系区块。Whenever relation-reconciliation 已补齐 formal ledger，需要让对象页重新与账本对齐、更新 serving-ready 页面投影、同步 `parent_methods` / `child_methods` 等强一致字段，或批量刷新页面中的关系区块时，都应使用本 skill。
---

# Page Projection Sync

你是 ResearchKB 的 page projection synchronization stage。你的任务是在 relation ledger 已更新后，把 formal graph truth 同步回对象页。

## 自动同步内容
1. `## Formal relations`
2. 强一致 frontmatter（当前包括 `parent_methods` / `child_methods`）
3. 模板化人类友好关系区块（相关方法、相关任务、相关概念、相关 benchmark、代表论文、证据来源等）

## 不自动同步
- 方法解释性正文
- 核心问题分析
- 优势与局限
- 关键结论
- 批注与综述判断

## 输入
- 更新后的 formal ledgers
- `relation-reconciliation` 输出
- 受影响对象页列表

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_pages:
  - path: wiki/methods/Foo.md
    updated_sections:
      - formal_relations
      - frontmatter
      - human_relation_blocks
manual_followups:
  - path: wiki/papers/Bar.md
    reason: interpretive prose not auto-synced
```

## 最小 rollout 建议
- 先在已具备 serving-ready 基础模板的 Method / Paper 页试跑。
- 然后扩到 Concept / Task / Scenario / Benchmark / Evidence。
- 同步完成后，必须再交给 lint、ontology-semantic-review 与 serving-governance-review。
