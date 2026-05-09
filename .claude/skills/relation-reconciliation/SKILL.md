---
name: relation-reconciliation
description: 在 `paper-ingest` 完成后，对照 relation_candidates、Evidence 缓存、对象页与当前 `ontology/relations/*.md` 正式账本，补齐 formal relation ledger，并输出 added/already_present/exempt/needs-human-review 结果。Whenever 单篇论文 ingest 完成后需要补齐 formal relations、比较 evidence 与 ledger 差异、检查哪些关系已存在/缺失/应豁免、或要把候选关系正确分发到各关系账本时，都应使用本 skill。
---

# Relation Reconciliation

你是 ResearchKB 的 formal relation reconciliation stage。你的任务不是重新解析论文，而是在 `paper-ingest` 之后，把候选关系、对象页暗示关系、Evidence 支撑关系与当前 formal ledger 对齐并补齐。

## 链路位置
本 skill 是单篇论文日常编译链的第二阶段，默认前置为 `paper-ingest`。
本 skill 不应独立替代 ingest，也不应跳过后续 `page-projection-sync`。

## 核心职责
1. 读取 `paper-ingest` 输出中的 `relation_candidates` 与 `relation_exemptions`
2. 读取本次改动涉及的对象页与 Evidence 缓存
3. 读取当前 `ontology/relations/*.md` 正式账本
4. 进行 normalize → diff → reconcile
5. 将缺失正式边写入正确的关系文件
6. 输出结构化 reconciliation 摘要，并指出受影响对象页供 `page-projection-sync` 使用
7. 对 semantic stub candidates 给出下游 serving 状态建议，并把受影响的 stub 页显式交给投影阶段

## 不负责
- 不重新做 PDF 解析
- 不改写解释性正文
- 不做最终 ontology verdict
- 不做 serving-ready 最终发布裁决

## Normalize
把所有候选关系统一规范成：
- source_name
- source_type
- source_path
- relation_type
- target_name
- target_type
- target_path
- edge_semantics
- evidence_name
- evidence_path
- source_of_claim（ingest / page / evidence / ledger）

补充约束：
- 正式 relation 实例唯一按 `relation_type + source + target` 识别。
- `edge_semantics`、`evidence`、`status`、`note` 仅作为该实例属性，不构成新实例。
- `supported_by` 只允许 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 作为 source。
- 若候选关系试图把 `Paper` 作为 `supported_by` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
- 不得新增 Evidence 与 Paper 之间的 formal relation。

## Canonical ledger rendering
`relation-reconciliation` 是 relation ledger 的 canonical formatter。

relation 页固定由两部分组成：
1. `关系语义说明区`
2. `实例边账本区`

渲染规则：
- relation 页顶部的对象域导航和证据入口导航必须移除。
- 每条实例边主行必须渲染为：`[[source]] --relation_type--> [[target]]`
- 每条实例边子项必须固定按以下顺序输出：
  - `source_path: ...`
  - `target_path: ...`
  - `edge_semantics: ...`
  - `evidence: ...`
  - `evidence_link: [[...]]`
  - `evidence_path: ...`
- `source`、`target`、`evidence_link` 默认使用短 wikilink；若 basename 在 vault 中不唯一，则必须退化为带路径的 wikilink并保留原显示名。
- relation 页除主行 `source` / `target` 与 `evidence_link` 外，不得出现其他 wikilink。

## Diff
对比：
- candidate edges
- page-implied edges
- evidence-backed edges
- current formal ledger edges
- explicit exemptions

## Reconcile 输出分类
- `already_present`
- `add_now`
- `exempt`
- `needs_human_review`

## 强语义表述复核
除显式 `relation_candidates` 外，还必须复核已更新对象页中的强语义表述，重点包括：
- 方法页中的“主要场景”
- 论文页中的“核心概念”
- 论文页中的“核心任务 / 相关任务”
- framework 型 Concept 页中的“场景 / 面向”

若这些表述满足：
1. ontology 存在合法 relation type
2. 当前 evidence 足以支撑
3. formal ledger 中缺失对应边

则必须继续判断是否应补为 formal relation，而不是因 ingest 未显式列出就跳过。

### 复核后的判定规则
- 若 relation type 清晰、evidence 明确，则归入 `add_now`
- 若 relation type 合法但粒度或方向仍存在歧义，则归入 `needs_human_review`
- 不得因为该关系最初未出现在 `relation_candidates` 中就直接忽略

## Context-only 护栏
即使某页人类区块中出现大量 `[[wikilink]]`，也不得机械全部升级。 broad “相关方法 / 路线”、对比对象、背景路线、延伸阅读仍默认按 context-only 处理，除非存在单独明确的 formal relation 语义与证据支撑。

## Ledger routing
- `cites` → `ontology/relations/cites.md`
- `proposes` → `ontology/relations/proposes.md`
- `based_on` → `ontology/relations/based_on.md`
- `references_method` → `ontology/relations/references_method.md`
- `targets_task` → `ontology/relations/targets_task.md`
- `uses_concept` → `ontology/relations/uses_concept.md`
- `evaluated_on` → `ontology/relations/evaluated_on.md`
- `supported_by` → `ontology/relations/supported_by.md`
- `sourced_from` → `ontology/relations/sourced_from.md`

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
already_present: []
added_relations:
  - file: ontology/relations/targets_task.md
    edge: "[[Paper]] --targets_task--> [[Task]]"
    evidence: "[[ontology/entities/evidence/foo.sections|foo.sections]] §x"
exemptions: []
needs_human_review: []
affected_pages: []
affected_stub_pages: []
serving_status_recommendations:
  - path: ontology/entities/methods/RoG.md
    recommended_status: partial
    reason: stable minimal semantics exist, but default serving evidence is still insufficient
```

## 最小 rollout 建议
- 先在标准 empirical 方法论文上试跑（如 PathMind 类论文）。
- 再扩到 survey / framework 论文。
- 每次 reconciliation 完成后，都应将 `affected_pages` 交给 `page-projection-sync`，而不是停留在 ledger 已更新但页面未同步的状态。

## 完成后的默认后继阶段
当本 skill 完成 formal relation ledger 的补齐与对齐后：
- 必须把 `affected_pages` 交给 `page-projection-sync`
- 不应停留在“ledger 已更新但对象页尚未同步”的状态
- 对象页同步完成后，才进入 lint 与后续治理
