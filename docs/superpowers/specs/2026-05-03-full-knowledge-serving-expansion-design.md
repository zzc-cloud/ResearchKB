# Full Knowledge-Layer Serving Expansion Design

Date: 2026-05-03

## Summary

Expand the serving-layer model from Method/Paper to the full governed knowledge layer:

- `wiki/papers/`
- `wiki/methods/`
- `wiki/concepts/`
- `wiki/tasks/`
- `wiki/scenarios/`
- `wiki/benchmarks/`
- `intermediate/papers/` Evidence pages

The design keeps `wiki/relations/` as governance truth, requires all seven node types to expose a normalized `Formal relations` serving surface, allows human-readable sections to differ by node type, and adds a third governance gate dedicated to serving-readiness.

## Problem

The current serving-layer rollout only covers a small Method/Paper slice. That creates three scaling problems:

1. QA can traverse object pages reliably only for a subset of node types.
2. Relation-ledger truth and object-page serving quality are not yet generalized across the knowledge layer.
3. Existing governance covers structure (`scripts/lint_graph.py`) and ontology semantics (`ontology-semantic-review`), but not the distinct question of whether a governed page is a reliable QA serving surface.

If the long-term goal is object-page-driven constrained QA across the whole knowledge base, then every major node type must participate in the serving model, and serving-readiness must become a first-class release criterion.

## Goals

- Extend the serving-layer model to Paper, Method, Concept, Task, Scenario, Benchmark, and Evidence.
- Require a normalized `Formal relations` section on all seven node types.
- Keep human-readable relation sections differentiated by node type rather than forcing identical page layouts.
- Preserve `wiki/relations/` as governance truth.
- Expand governance into three explicit layers: structural, ontology-semantic, and serving-governance.
- Build the full specification and lint/review framework first, then migrate pages in batches.

## Non-goals

- Migrate every existing page in a single implementation pass.
- Collapse `wiki/relations/` into object pages.
- Make all node types share identical human-readable section structure.
- Replace `intermediate/papers/` Evidence pages with a different evidence model.

## Architecture

### 1. Governance truth layer

Location: `wiki/relations/`

Responsibilities:
- canonical instance-edge truth
- authoring and repair source of truth
- structural and semantic governance reference
- projection source for object-page serving surfaces

This layer remains authoritative, but should no longer be the default QA runtime read surface once pages are serving-ready.

### 2. Governed serving layer

Locations:
- `wiki/papers/`
- `wiki/methods/`
- `wiki/concepts/`
- `wiki/tasks/`
- `wiki/scenarios/`
- `wiki/benchmarks/`
- `intermediate/papers/` Evidence pages

Responsibilities:
- act as the default constrained-QA entry surface
- expose machine-readable local topology through `Formal relations`
- expose human-readable object-centric summaries tailored to node type
- align human-visible page content with AI-consumable relation projections

### 3. Provenance source layer

Location: `raw/`

Responsibilities:
- ultimate source tracking only
- not a default QA runtime layer
- consulted only when evidence caches are insufficient or provenance needs auditing

## Unified serving principle

All seven node types must expose:
1. frontmatter
2. human-readable object sections
3. `## Formal relations`

However, only the machine-readable layer is strongly unified. Human-facing sections should remain type-specific.

This yields a half-unified model:
- machine layer: standardized
- reading layer: differentiated by node semantics

## Per-type page design

### Paper

**Frontmatter role:** identity/classification only; avoid large derived relation lists.

**Human-readable sections:**
- 核心问题
- 主要贡献
- 核心方法 / 核心概念
- 相关任务
- 应用场景
- 相关基准
- 关键结论
- 引用了哪些重要工作
- 被哪些论文引用（已知）
- 与知识库其他内容的关联
- 证据来源

**Formal relations focus:**
- `proposes`
- `targets_task`
- `uses_concept`
- `evaluated_on`
- `cites`
- `supported_by`

### Method

**Frontmatter role:** identity/classification plus a very small set of derived fields.

Keep strong-consistency derived fields narrow at first:
- `parent_methods`
- `child_methods`

**Human-readable sections:**
- 方法定义
- 解决的核心问题
- 技术原理
- 方法演化位置
- 应用场景
- 代表论文
- 相关概念
- 证据来源
- 优势与局限
- 与其他方法的对比

**Formal relations focus:**
- `based_on`
- `improves_on`
- `targets_task`
- `uses_concept`
- `applies_to`
- `evaluated_on`
- `supported_by`
- incoming `proposes`

### Concept

**Frontmatter role:** identity/classification only in the first phase.

**Human-readable sections:**
- 概念定义
- 核心内涵
- 与其他概念的关系
- 相关方法
- 相关论文
- 相关任务 / 场景
- 证据来源

**Formal relations focus:**
- incoming/outgoing `uses_concept`
- `supports`
- `depends_on`
- `applies_to` for framework/taxonomy concepts
- `supported_by`
- incoming `proposes`

### Task

**Frontmatter role:** identity/classification only.

**Human-readable sections:**
- 任务定义
- 核心挑战
- 相关方法
- 相关概念
- 相关场景
- 相关 benchmark
- 相关论文
- 证据来源 / 关系索引

**Formal relations focus:**
- incoming `targets_task`
- incoming `supports`
- any explicit benchmark/task neighbor relations if standardized later
- `supported_by`

### Scenario

**Frontmatter role:** identity/classification only.

**Human-readable sections:**
- 场景描述
- 核心挑战
- 使用的主要方法 / 概念
- 相关任务
- 相关论文
- 相关 benchmark
- 证据来源

**Formal relations focus:**
- incoming `applies_to`
- incoming `supports`
- explicit relations to task/method/concept neighbors
- `supported_by`

### Benchmark

**Frontmatter role:** identity/classification only.

**Human-readable sections:**
- benchmark 定义
- 评测目标
- 相关任务
- 被哪些方法 / 论文使用
- 相关场景
- 证据来源

**Formal relations focus:**
- incoming `evaluated_on`
- `supported_by`

### Evidence

**Frontmatter role:** evidence identity and provenance metadata.

Keep:
- `title`
- `short_name`
- `source_pdf`
- `cache_type`
- `status`
- `venue`
- `year`

**Human-readable sections:**
- 对应正式知识节点
- 本节支撑什么
- 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 来源说明

**Formal relations focus:**
- incoming `supported_by`
- outgoing `sourced_from`

Evidence is the most special serving node because it is both a QA drill-down page and a provenance bridge.

## Unified `Formal relations` requirements

All types must use the same normalized shape:

```markdown
## Formal relations
### Outgoing
- `[[Source]] --relation_type--> [[Target]]`
  - evidence: [[Evidence]]

### Incoming
- `[[Source]] --relation_type--> [[Target]]`
  - evidence: [[Evidence]]
```

When a side has no relations, write:

```markdown
- 无
```

This section is the cross-type QA traversal surface.

## Governance model

Serving expansion requires three explicit governance layers.

### 1. Structural governance

Tool: `python3 scripts/lint_graph.py`

Responsibilities:
- file existence
- frontmatter basics
- section presence
- relation formatting
- parsable links
- automatable projection consistency/completeness checks

### 2. Ontology-semantic governance

Tool/skill: `ontology-semantic-review`

Responsibilities:
- entity typing correctness
- relation placement correctness
- ontology-level classification quality
- global semantic network reasonableness

### 3. Serving governance

New independent gate required.

Responsibilities:
- page serving completeness
- alignment between human-readable sections and `Formal relations`
- QA traversability from object pages without default ledger fallback
- release-readiness of migrated pages/batches as serving surfaces

Serving governance is a distinct release criterion and should not be reduced to either structure lint or ontology semantic review.

## Why a separate serving-governance gate is necessary

A page can be:
- structurally valid
- ontologically reasonable
- yet still be a poor QA serving surface

Examples of issues only a serving-governance gate should judge:
- `Formal relations` exists but is insufficient for reliable traversal
- human-readable sections mislead relative to formal projections
- local topology is too incomplete for default object-page-first QA
- a migrated batch is not ready to become the runtime serving default

This makes serving governance a separate publish gate rather than only an extension of the other two.

## Lint framework expansion

The current lint is sample-oriented. It should evolve toward a type-based serving framework.

### Required evolution

1. Discover page type by path:
- `wiki/papers/` → Paper
- `wiki/methods/` → Method
- `wiki/concepts/` → Concept
- `wiki/tasks/` → Task
- `wiki/scenarios/` → Scenario
- `wiki/benchmarks/` → Benchmark
- `intermediate/papers/` → Evidence

2. Maintain per-type rule tables:
- required headings
- required frontmatter keys
- allowed derived fields
- relation categories expected for the type
- whether incoming/outgoing may be empty

3. Validate per page:
- page structure
- frontmatter requirements
- `Formal relations` structure
- ledger-to-page projection consistency
- ledger-to-page projection completeness for migrated pages

### Two-phase lint strategy

Because the specification goes full-type before the content migration does, lint should support staged enforcement.

**Phase 1:** framework coverage
- knows all seven types
- validates structure and `Formal relations` format
- allows unmigrated pages to remain non-serving-ready

**Phase 2:** strict completeness
- for pages included in migration batches
- enforce formal projection completeness
- enforce strong-consistency derived fields

### Severity levels

Suggested output levels:

**Fatal**
- missing `Formal relations`
- illegal relation type
- missing evidence on required edges
- strong-consistency frontmatter mismatch

**Warning**
- incomplete human-readable summary blocks
- optional readable sections missing
- not-yet-migrated serving status

## Serving-governance review skill

Recommended future skill name:
- `serving-governance-review`

Suggested responsibilities:
- evaluate serving completeness
- evaluate serving readability alignment
- evaluate QA traversability
- evaluate batch release readiness

Suggested outputs:
- `pass`
- `needs_fixes`
- `blocked`

This skill should accept a page set, a batch, a directory, or a git diff.

## Rollout strategy

### Phase 1: governance architecture
- formally define the three governance layers
- define boundaries between lint, semantic review, and serving review

### Phase 2: full-type serving specification
- define frontmatter role per type
- define human-readable section templates per type
- define `Formal relations` requirements across all seven types
- define lint rule tables and serving-review expectations

### Phase 3: batch-based content migration
Migrate content by QA value and topological centrality, not directory order.

Recommended order:
1. Method / Paper
2. Concept / Task
3. Scenario / Benchmark
4. Evidence

### Phase 4: batch qualification
A batch becomes `serving-ready` only when it passes:
1. structural lint
2. ontology semantic review
3. serving governance review

## Migration-state handling

During rollout, the repository will contain mixed states:
- serving-ready pages
- partially migrated pages
- legacy pages

The system should expose this status explicitly rather than pretending all pages are equally ready.

Suggested lightweight statuses:
- `serving_status: ready`
- `serving_status: partial`
- `serving_status: legacy`

This can live in frontmatter or an external governance manifest, but the state must be queryable.

## QA behavior during migration

### For serving-ready pages
- object page → `Formal relations` → evidence drill-down

### For partial/legacy pages
- start from object page
- fall back to relation ledger only when page serving is incomplete
- surface that the page is not fully serving-ready

This prevents silent accuracy loss during rollout.

## End state

When rollout completes:
- all major node types are governed serving pages
- cross-type QA traversal happens through `Formal relations`
- `wiki/relations/` remains truth but recedes to governance/repair/audit workflows
- `intermediate/papers/` Evidence pages act as both serving evidence nodes and provenance bridges

At that point the repository becomes an object-page-driven knowledge system rather than a document collection augmented by a separate relation ledger.

## Recommendation

Adopt a full-type serving specification now, but migrate pages in batches.

Make serving-governance a distinct release gate, require `Formal relations` across all seven node types, and expand lint from sample-page validation to type-based serving validation. This preserves architectural clarity while avoiding a single risky all-pages-at-once rewrite.
