---
name: relation-reconciliation
description: 在 `paper-ingest` 完成后，对照 relation_candidates、Evidence 缓存、对象页与当前 `wiki/relations/*.md` 正式账本，补齐 formal relation ledger，并输出 added/already_present/exempt/needs-human-review 结果。Whenever 单篇论文 ingest 完成后需要补齐 formal relations、比较 evidence 与 ledger 差异、检查哪些关系已存在/缺失/应豁免、或要把候选关系正确分发到各关系账本时，都应使用本 skill。
---

# Relation Reconciliation

你是 ResearchKB 的 formal relation reconciliation stage。你的任务不是重新解析论文，而是在 `paper-ingest` 之后，把候选关系、对象页暗示关系、Evidence 支撑关系与当前 formal ledger 对齐并补齐。

## 链路位置
本 skill 是单篇论文日常编译链的第二阶段，默认前置为 `paper-ingest`。
本 skill 不应独立替代 ingest，也不应跳过后续 `page-projection-sync`。

## 核心职责
1. 读取 `paper-ingest` 输出中的 `relation_candidates` 与 `relation_exemptions`
2. 读取本次改动涉及的对象页与 Evidence 缓存
3. 读取当前 `wiki/relations/*.md` 正式账本
4. 进行 normalize → diff → reconcile
5. 将缺失正式边写入正确的关系文件
6. 输出结构化 reconciliation 摘要，并指出受影响对象页供 `page-projection-sync` 使用

## 不负责
- 不重新做 PDF 解析
- 不改写解释性正文
- 不做最终 ontology verdict
- 不做 serving-ready 最终发布裁决

## Normalize
把所有候选关系统一规范成：
- source
- relation_type
- target
- evidence
- source_of_claim（ingest / page / evidence / ledger）

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
- `proposes` → `wiki/relations/paper_method_links.md`
- `targets_task` → `wiki/relations/task_method_map.md`
- `evaluated_on` → `wiki/relations/benchmark_links.md`
- `uses_concept` / `supports` / `depends_on` / `applies_to` → `wiki/relations/concept_links.md`
- `based_on` / `improves_on` → `wiki/relations/method_evolution.md`
- `cites` → `wiki/relations/citation_graph.md`
- `supported_by` → `wiki/relations/evidence_index.md`
- `sourced_from` → `wiki/relations/provenance_links.md`

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
already_present: []
added_relations:
  - file: wiki/relations/task_method_map.md
    edge: "[[Paper]] --targets_task--> [[Task]]"
    evidence: "[[intermediate/papers/foo.sections|foo.sections]] §x"
exemptions: []
needs_human_review: []
affected_pages: []
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
