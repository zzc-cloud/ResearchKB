---
name: relation-reconciliation
description: 在 `paper-ingest` 产出 relation candidates、Evidence 缓存与对象页候选后，对照 `ontology/relations/*.md` 正式账本补齐 formal relation ledger，并输出 added/already_present/exempt/needs-human-review 结果。仅当编排型 skill `process-paper` 已将当前任务推进到 relation reconciliation 阶段，或用户明确要求只做 formal relation ledger 补齐 / 修复时，才应使用本 skill；不要把它当作“处理论文”完整请求的默认入口。
---

# Relation Reconciliation

你是 ResearchKB 的 formal relation reconciliation stage。你的任务不是重新解析论文，而是在 `paper-ingest` 之后，把候选关系、对象页暗示关系、Evidence 支撑关系与当前 formal ledger 对齐并补齐。

## 链路位置
本 skill 是单篇论文编译链中的 relation reconciliation 阶段，默认前置为 `paper-ingest`。
默认由编排型 skill `process-paper` 在 ingest 之后调用；当用户明确要求只做 formal relation ledger 补齐 / 修复时，也可直接使用本 skill。

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
- `supported_by` 只允许 `Method`、`Task`、`Scenario`、`Benchmark` 作为 source。
- 若候选关系试图把 `Paper` 作为 `supported_by` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
- `evaluated_on` 只接收 `Method -> Benchmark`；若候选关系试图把 `Paper` 作为 `evaluated_on` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
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
  - `source_paper_path: ...`（仅 `references_method` 必填）
  - `target_paper_path: ...`（仅 `references_method` 必填）
  - `edge_semantics: ...`
  - `evidence: ...`
  - `evidence_link: [[...]]`
  - `evidence_path: ...`
- `references_method` 之外的 relation types 仍使用不含 paper-path 字段的基础 child-field 集合；不得把这两个 paper path 字段泛化为所有 relation ledger 的全局要求。
- `source`、`target`、`evidence_link` 默认使用短 wikilink；若 basename 在 vault 中不唯一，则必须退化为带路径的 wikilink并保留原显示名。
- relation 页除主行 `source` / `target` 与 `evidence_link` 外，不得出现其他 wikilink。

## Diff
对比：
- candidate edges
- page-implied edges
- evidence-backed edges
- current formal ledger edges
- explicit exemptions

若缺失 target Method 页但其 Method 身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页；并且当前论文已提供正常 `object_semantics`、至少一条正式方法关系与至少一个有效 Evidence anchor 时，不得退回为 Method placeholder。

## Reconcile 输出分类
- `already_present`
- `add_now`
- `exempt`
- `needs_human_review`

## 强语义表述复核
除显式 `relation_candidates` 外，还必须复核已更新对象页中的强语义表述，重点包括：
- 方法页中的“主要场景”
- 论文页中的“核心机制”
- 论文页中的“核心任务 / 相关任务”
- survey 论文中的方法 coverage

若这些表述满足：
1. ontology 存在合法 relation type
2. 当前 evidence 足以支撑
3. formal ledger 中缺失对应边

则必须继续判断是否应补为 formal relation，而不是因 ingest 未显式列出就跳过。

### 复核后的判定规则
- 若 relation type 清晰、evidence 明确，则归入 `add_now`
- 若 relation type 合法但粒度或方向仍存在歧义，则归入 `needs_human_review`
- survey 论文中的方法 coverage 若属于系统梳理、分类、比较或 landscape 结构，应优先判断是否补为 `surveys_method`，而不是停留在 `cites`。
- 若 survey 论文在 ingest 输出中已声明 Tier A survey-covered method candidates，则 `relation-reconciliation` 不得接受“空的 `surveys_method` ledger”直接过关。
- 对于 Tier A candidates，必须默认补齐：`surveys_method`、必要的 `supported_by`、representative paper stub / anchor，以及与 representative paper 对应的 `cites`。
- 对于 Tier B candidates，必须显式判定 `add_now` 或 `needs-human-review`；不得因 ingest 未直接 formalize 而静默跳过。
- 对于 Tier C candidates，允许停留在 review 输出，不自动 materialize。
- `surveys_method` 不得用于首次提出方法；若论文对方法的关系是“首次提出/正式定义”，应落为 `proposes`。
- 若某方法通过 `surveys_method` 已稳定进入图谱，而当前论文又以结构化 coverage 明确给出其任务或场景归属，则应继续判断是否补为 `targets_task` 或 `applied_in`；不得因为该方法来自 survey paper 就默认降级为 context-only。
- 若候选关系试图直接把 `Task` 与 `Scenario` 相连，则默认归入 `needs_human_review` 或直接视为当前规范下的非法关系，而不是直接落账。
- 不得因为该关系最初未出现在 `relation_candidates` 中就直接忽略

## Context-only 护栏
即使某页人类区块中出现大量 `[[wikilink]]`，也不得机械全部升级。 broad “相关方法 / 路线”、对比对象、背景路线、延伸阅读仍默认按 context-only 处理，除非存在单独明确的 formal relation 语义与证据支撑。

## Ledger routing
- `cites` → `ontology/relations/cites.md`
- `proposes` → `ontology/relations/proposes.md`
- `surveys_method` → `ontology/relations/surveys_method.md`
- `based_on` → `ontology/relations/based_on.md`
- `references_method` → `ontology/relations/references_method.md`
- `targets_task` → `ontology/relations/targets_task.md`
- `applied_in` → `ontology/relations/applied_in.md`
- `evaluated_on` → `ontology/relations/evaluated_on.md`
- `supported_by` → `ontology/relations/supported_by.md`
- `sourced_from` → `ontology/relations/sourced_from.md`

方法邻接分流规则：
- 严格谱系才进 `based_on`
- 比较 / 借鉴 / 路线参照进 `references_method`
- 若仅存在论文级引用事实且 Method 身份不稳定，则保留在 `cites`
- 对于 `references_method`：若实例边声明了 `source_paper_path` 与 `target_paper_path`，则必须同时验证 `ontology/relations/cites.md` 中存在对应 `Paper --cites--> Paper` 实例；否则归入 `needs_human_review`，不得直接落为 fully valid formal edge。
- 当 survey-derived partial `Method` 默认生成 representative paper stub / anchor 时，source survey Paper 应同步生成指向该 representative paper 的 `cites`。
- 若 Tier A survey-derived `Method` 已落为 formal partial Method，但 representative paper stub 已生成且 `cites` 缺失，则该 provenance 闭环不完整，至少应进入 `needs-human-review`。
- `references_method` 的 target paper 若当前仅由 citation / provenance 需要支撑，应保留或创建为 `Paper Stub / Anchor`，而不是自动升级为 Formal Paper。
- placeholder cited paper target 应保留为 Paper Stub / Anchor，而不是自动升级为 Formal Paper。
- partial `Method` 可以依赖 target paper stub 作为弱锚点；不得因为 target paper 尚未成为 Formal Paper 就回退已稳定的方法 identity。
- 仅有普通 related-work mention 时，可保留在 `cites` 并按需创建 paper stub，但不得自动 materialize 为 partial `Method`。

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
already_present: []
added: []
exempt: []
needs_human_review: []
affected_pages: []
affected_stub_pages: []
materialized_partial_methods: []
materialized_paper_stubs: []
deferred_survey_candidates: []
serving_status_recommendations:
  - path: ontology/entities/methods/RoG.md
    recommended_status: partial
    reason: stable Method identity and formal relation exist, but explanatory coverage remains incomplete
```

字段约定：
- `added`：本轮新写入 formal ledger 的正式实例边；每项至少包含 `file`、`edge`、`evidence`。
- `exempt`：按规范豁免、不应落账的关系或对象。
- `needs_human_review`：存在方向、粒度、身份或 ledger 路由歧义的候选。
- 不再使用 `added_relations`、`exemptions`、`needs-human-review` 作为主交接字段名。

## 最小 rollout 建议
- 先在标准 empirical 方法论文上试跑（如 PathMind 类论文）。
- 再扩到 survey / framework 论文。
- 每次 reconciliation 完成后，都应将 `affected_pages` 交给 `page-projection-sync`，而不是停留在 ledger 已更新但页面未同步的状态。
- `affected_pages` must include both source and target object pages for every reconciled formal relation instance whose corresponding page file exists.
- 若某对象页已承接 formal relation 且同时出现在 `affected_stub_pages` 中，它仍必须同时出现在 `affected_pages` 中；`affected_stub_pages` 只做辅助分类，不替代对象页同步清单。
- 对于 `cites` 指向的 placeholder paper target，创建占位页后不得停在“仅可解析”状态，必须继续进入 `page-projection-sync`。
