---
name: relation-reconciliation
description: 在 `paper-ingest` 完成后，对照 relation_candidates、Evidence 缓存、对象页与当前 `wiki/relations/*.md` 正式账本，补齐 formal relation ledger，并输出 added/already_present/exempt/needs-human-review 结果。Whenever 单篇论文 ingest 完成后需要补齐 formal relations、比较 evidence 与 ledger 差异、检查哪些关系已存在/缺失/应豁免、或要把候选关系正确分发到各关系账本时，都应使用本 skill。
---

# Relation Reconciliation

你是 ResearchKB 的 formal relation reconciliation stage。你的任务不是重新解析论文，而是在 `paper-ingest` 之后，把候选关系、对象页暗示关系、Evidence 支撑关系与当前 formal ledger 对齐并补齐。

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
