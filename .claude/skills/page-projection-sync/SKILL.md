---
name: page-projection-sync
description: 在 formal relation ledger 更新后，把最新 ledger 投影同步回对象页：更新 `Formal relations`、强一致 frontmatter 和模板化人类关系区块。Whenever relation-reconciliation 已补齐 formal ledger，需要让对象页重新与账本对齐、更新 serving-ready 页面投影、同步 `parent_methods` / `child_methods` 等强一致字段，或批量刷新页面中的关系区块时，都应使用本 skill。
---

# Page Projection Sync

你是 ResearchKB 的 page projection synchronization stage。你的任务是在 relation ledger 已更新后，把 formal graph truth 同步回对象页。

## 链路位置
本 skill 是单篇论文日常编译链的第三阶段，默认前置为 `relation-reconciliation`。
本 skill 完成后不视为流程结束，而应继续进入 `index-sync` 与后续三层治理出口。

## 自动同步内容
1. `## Formal relations`（使用半展开 serving projection 格式，而不是完整边字符串）
2. 强一致 frontmatter（当前包括 `parent_methods` / `child_methods`）
3. 模板化人类友好关系区块（相关方法、相关任务、相关概念、相关 benchmark、代表论文、证据来源等）
4. `## 方法演化与参照关系`（Method 页的人类可读方法邻接区块）

Method 页中的“方法演化位置”应重构为“方法演化与参照关系”，并分成两个模板化子区块：
- 上游演化方法：解释 `based_on`
- 关键参照方法：解释 `references_method`

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
- `paper-ingest` 产出的 `semantic_stub_candidates`
- `relation-reconciliation` 产出的 `serving_status_recommendations`

输入约束：
- `page-projection-sync` 读取 canonical relation ledger record，但不定义 relation 页 markdown 表示。
- 它只消费 source、target、relation、edge_semantics、evidence truth，并把这些 formal relation truth 投影回对象页。
- 它不得依赖 relation 页顶部导航说明或旧的 `edge_semantics + evidence` 简化记录形态。

## `Formal relations` 投影格式
- 页面必须保留 `### Outgoing` 与 `### Incoming`。
- `### Outgoing` 后必须写：`当前对象作为 source；以下列出当前对象指向的 relation 实例。`
- `### Incoming` 后必须写：`当前对象作为 target；以下列出指向当前对象的 relation 实例。`
- 每条投影边必须写成：
  - `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
    - `edge_semantics`: ...
    - `evidence`: [[relative/path/to/evidence|Evidence Name]]
- 对象页与 Evidence 页默认生成 `[[../x]]` 而不是 `[[../x|Name]]` 形式的相对 wikilink；文档路径信息继续保留在 `（文档：`...`）` 提示中。
- `supported_by` 投影只依赖 source、target Evidence 与 `reason`；不得假设 ledger 中存在重复的 `- evidence:` 行。
- 每条 relation ledger 实例边必须逐条投影到对象页；即使同一邻接对象重复，若 `edge_semantics` 或 `evidence` 不同，也不得合并。
- 不再使用 ``[[Source]] --relation--> [[Target]]`` 作为对象页或 Evidence 页的默认 serving projection 格式。
- 正文中的所有 wikilink 必须是 `Formal relations` 已出现对象链接的子集。
- Evidence 页正文不允许直接链接回 Paper。

## 变体识别规则
- semantic stub / partial 页：若 ingest 已稳定提供最小对象语义，但证据仍不足以支持 full serving-ready 页面，则应写回最小语义骨架：`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`，并同步 `status: partial` 或 `status: placeholder`。
- survey 论文页：优先同步 `proposes`、`surveys_method`、`cites`，并保留任务、场景的人类区块与豁免信息；不得把 survey-paper 对既有方法的 coverage 误投影为 `proposes`。
- survey / framework 主线的 Scenario 页：若存在正式场景邻接，应同步 incoming `applied_in`，并重排人类区块为“主要方法”优先。
- survey / framework 主线的 Task 页：优先同步 incoming `targets_task`，并重排人类区块为“相关框架 / 场景 / 论文”优先。

## 强一致派生规则
- `based_on` → formal relation + `parent_methods` / `child_methods` 强一致派生
- `references_method` → formal relation only，不写入 `parent_methods` / `child_methods`

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_pages:
  - path: ontology/entities/methods/Foo.md
    updated_sections:
      - formal_relations
      - frontmatter
      - human_relation_blocks
manual_followups:
  - path: ontology/entities/papers/Bar.md
    reason: interpretive prose not auto-synced
```

## 变体同步边界
- survey / framework 变体允许重排模板化人类区块，但不得自动改写“关键结论”“我的批注”“开放问题”等解释性正文。
- 若页面缺少该变体所需的人类区块，应标记为 `manual_followups`，而不是擅自生成长篇 prose。

## 最小 rollout 建议
- 先在已具备 serving-ready 基础模板的 Method / Paper 页试跑。
- 然后扩到 Task / Scenario / Benchmark / Evidence。
- 同步完成后，必须再交给 lint、ontology-semantic-review 与 serving-governance-review。

## 完成后的默认后继阶段
当本 skill 完成对象页投影同步后，默认进入以下后继阶段：
1. `index-sync`
2. `python3 scripts/lint_graph.py`
3. `ontology-semantic-review`
4. `serving-governance-review`

若其中任一阶段失败，则本次论文处理流程不得视为正式入图完成。
