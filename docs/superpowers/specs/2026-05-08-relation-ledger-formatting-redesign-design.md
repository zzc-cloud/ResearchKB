---
title: Relation Ledger Formatting Redesign Design
date: 2026-05-08
tags:
  - spec
  - researchkb
  - ontology
  - relations
  - ledger
  - formatting
status: draft
---

# Relation Ledger Formatting Redesign Design

Date: 2026-05-08

## Summary

This spec redesigns the content format of ResearchKB formal relation ledger pages so they behave as stable governance-oriented instance-edge ledgers rather than mixed navigation pages.

The redesign applies across the full compile pipeline:

- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`
- structural governance
- ontology semantic governance
- serving governance

The new model keeps relation ledgers readable like object instance pages, but narrows their purpose:

- relation pages retain a relation-semantic explanation section
- relation pages retain a formal instance-edge ledger section
- relation pages stop acting as Obsidian navigation hubs
- Obsidian jumps become tightly constrained to formal edge endpoints and evidence links only
- every edge record explicitly includes AI-locatable document paths for source, target, and evidence

## Problem

Current relation pages mix several roles in one document:

- relation-semantic explanation
- navigation to related domains and evidence entry points
- formal instance-edge truth
- human-readable edge justification

For example, current ledgers such as `targets_task.md` include:

- top-of-page wikilinks for related object domains and evidence entry points
- edge records whose source/target are only represented as wikilinks
- evidence represented only as wikilinks
- no explicit stable document-path fields for all linked objects

This creates four problems.

### 1. Relation ledgers contain too many non-truth navigation affordances

The page becomes visually and semantically noisy because relation truth is mixed with Obsidian-oriented convenience links that are not part of the formal instance-edge payload.

### 2. AI-facing path resolution is under-specified

A wikilink is useful for Obsidian traversal, but it does not by itself give a stable, explicit document path surface for downstream AI consumption, auditing, and deterministic parsing.

### 3. The relation page format is not explicit enough as a governed compile output

The current shape looks hand-authored rather than compile-managed. The new pipeline goal is stronger: relation pages should be recognizable governed products of the full ingest → reconciliation → projection → governance chain.

### 4. Allowed jump surfaces are not clearly bounded

Today, relation pages expose jumps in explanatory areas that are not necessary for the ledger’s formal function. This increases graph noise and weakens the distinction between object serving pages and governance ledgers.

## Goals

- Redefine relation pages as stable, governed formal ledgers.
- Keep a meaningful relation-semantic explanation section.
- Remove top-of-page navigation blocks and other non-essential jump surfaces.
- Make source and target visible both as Obsidian-jumpable links and as explicit document paths.
- Make evidence visible as plain name, Obsidian jump, and explicit document path.
- Constrain all allowed wikilinks to a small, deterministic set.
- Apply the rule across the full automated compile pipeline and all governance layers.

## Non-goals

- Redesign object-page serving projections.
- Turn relation pages into default knowledge-serving entry pages.
- Introduce additional relation-specific rendering variants beyond the agreed uniqueness fallback rule.
- Add new formal relation types.
- Replace relation semantics in `ontology/graph-standard.md`; that file remains the normative ontology source.

## Confirmed design decisions

### 1. Relation page structure

Each relation ledger page must contain exactly two logical sections:

1. a relation-semantic explanation section
2. an instance-edge ledger section

The relation-semantic explanation section is necessary and may be more than minimal. Its role is to help humans and AI determine:

- what the relation means
- which source types are legal
- which target types are legal
- which nearby meanings should remain in `reason`
- which nearby meanings should be expressed in object-page frontmatter or prose instead of becoming formal edges

The instance-edge ledger section is the formal truth surface for relation instances.

### 2. Top-of-page navigation block removal

The current top-of-page navigation-style explanation block should be removed.

Specifically, relation pages should no longer include:

- object-domain navigation links
- evidence-entry navigation links
- other pure navigation-oriented explanatory links

This information is not needed in the ledger surface and should not be retained as plain-text scaffolding unless it directly serves relation-semantic interpretation.

### 3. Allowed Obsidian jump surfaces

Relation pages may contain Obsidian jumps only in the following places:

- the `source` endpoint in the instance-edge main line
- the `target` endpoint in the instance-edge main line
- the `evidence_link` child field

All other places must not contain wikilinks, including:

- top explanation blocks
- relation-semantic explanation prose
- `source_path`
- `target_path`
- `reason`
- `evidence`
- `evidence_path`
- any other explanatory or structural line

### 4. Canonical instance-edge format

Each relation instance must use this fixed child-field order:

1. `source_path`
2. `target_path`
3. `reason`
4. `evidence`
5. `evidence_link`
6. `evidence_path`

Canonical example:

```md
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: 文档路径：ontology/entities/methods/PathMind.md
  - target_path: 文档路径：ontology/entities/tasks/kgqa.md
  - reason: PathMind 在知识图谱问答任务上验证有效性。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: 文档路径：ontology/entities/evidence/PathMind.sections.md
```

This ordering is fixed and should be treated as canonical for generation, linting, and governance.

### 5. Path-field wording

All path fields must use the explicit wording prefix:

- `文档路径：...`

This applies to:

- `source_path`
- `target_path`
- `evidence_path`

### 6. Evidence field structure

Evidence must be split into three fields:

- `evidence`: stable plain-text evidence name
- `evidence_link`: Obsidian jump only
- `evidence_path`: explicit AI-locatable document path

This separates three concerns cleanly:

- readable name
- vault navigation
- deterministic path resolution

### 7. Short wikilink default with uniqueness fallback

The default rendering rule is:

- prefer short wikilinks for `source`, `target`, and `evidence_link`
- if the note basename is not globally unique in the vault, automatically fall back to a path-based wikilink with explicit display text

Examples:

Preferred short-link form:

```md
[[PathMind]]
[[kgqa]]
[[PathMind.sections]]
```

Fallback form when basename is not unique:

```md
[[../entities/methods/PathMind|PathMind]]
[[../entities/tasks/kgqa|kgqa]]
[[../entities/evidence/PathMind.sections|PathMind.sections]]
```

This rule applies uniformly to:

- `source`
- `target`
- `evidence_link`

### 8. Relation pages should resemble object pages structurally, not semantically

The user requirement was to reference the style of object instance pages such as `ontology/entities/scenarios/知识图谱推理问答.md`.

This spec interprets that requirement narrowly and intentionally:

- relation pages should adopt a stable sectioned structure
- relation pages should adopt stable field ordering
- relation pages should support both human reading and machine extraction
- relation pages should not imitate object-page knowledge-serving prose structure

In other words, relation pages become structured governance ledgers, not object-description pages.

## Recommended relation-page template

A relation ledger should follow this general shape:

```md
# <relation_name>

## 关系语义说明
- <formal meaning>
- <legal source types>
- <legal target types>
- <boundary with nearby meanings>
- <what belongs in reason instead of another formal edge>
- <what belongs in object-page fields or prose instead of this ledger>

## 实例边
- [[Source]] --relation_name--> [[Target]]
  - source_path: 文档路径：ontology/entities/...
  - target_path: 文档路径：ontology/entities/...
  - reason: ...
  - evidence: ...
  - evidence_link: [[...]]
  - evidence_path: 文档路径：ontology/entities/evidence/....md
```

The semantic-explanation section may vary by relation type, but the instance-edge record format must remain fixed.

## Why this is the right boundary

### 1. Better than leaving relation pages as mixed navigation-plus-ledger documents

The current hybrid structure makes relation truth harder to scan and harder to validate mechanically. Removing non-essential jump surfaces increases clarity and keeps relation pages aligned with their governance role.

### 2. Better than eliminating semantic explanation entirely

The user confirmed that the semantic explanation is necessary, not optional. It helps both humans and AI determine where relation instances belong and how object instances should be interpreted relative to the ledger.

### 3. Better than converting everything into pure path text

Pure path text would help deterministic location but would weaken Obsidian usability. The agreed combined structure preserves both use cases:

- Obsidian traversal where needed
- explicit path localization everywhere needed

### 4. Better than adding a new post-processing normalization stage

The format should become part of the canonical compile product, not a later cosmetic rewrite. Therefore it should be owned inside the existing compile chain rather than in a new standalone relation-format stage.

## Compile-pipeline alignment

### 1. `paper-ingest`

`paper-ingest` should not directly render final relation markdown, but it must emit normalized candidate metadata rich enough to support final rendering.

Required candidate-level fields:

- `relation`
- `source_name`
- `source_type`
- `source_path`
- `target_name`
- `target_type`
- `target_path`
- `reason`
- `evidence_name`
- `evidence_path`

`paper-ingest` should not lock in final short-link versus path-link rendering. That rendering choice belongs downstream when the formal ledger is written.

Expected effect:

- ingest remains responsible for semantic extraction
- ingest stops leaking presentation concerns into relation truth generation

### 2. `relation-reconciliation`

`relation-reconciliation` becomes the canonical relation-ledger formatter.

It must:

- reconcile candidate relation truth against current ledgers
- write relation pages using the new canonical edge-record format
- maintain or rewrite the relation-semantic explanation section according to the new page role
- decide short wikilink versus fallback path-based wikilink for source, target, and evidence link

For every written or normalized edge record, it must output:

- main line with linked `source` and `target`
- `source_path`
- `target_path`
- `reason`
- `evidence`
- `evidence_link`
- `evidence_path`

Expected effect:

- relation ledger formatting becomes a first-class reconciliation responsibility
- relation pages become stable compile products rather than ad hoc markdown surfaces

### 3. `page-projection-sync`

`page-projection-sync` should consume formal relation truth, not define relation-ledger markdown shape.

It must:

- continue reading relation truth from ledgers
- avoid relying on outdated assumptions about free-form relation-page prose or older edge record shapes
- continue projecting source/target/relation/reason/evidence truth back into object-page `Formal relations` sections and strong-consistency frontmatter

Expected effect:

- relation pages remain the governance truth surface
- object pages remain the serving-ready projection surface
- markdown representation concerns stay localized to the ledger-writing stage

### 4. Structural governance

Structural governance must harden this format rather than merely tolerate it.

Required checks:

- relation pages do not contain the old top navigation block
- relation pages only expose wikilinks in allowed locations
- every instance-edge record has a main edge line
- every instance-edge record includes `source_path`
- every instance-edge record includes `target_path`
- every instance-edge record includes `reason`
- every instance-edge record includes `evidence`
- every instance-edge record includes `evidence_link`
- every instance-edge record includes `evidence_path`
- child-field order is exactly:
  - `source_path`
  - `target_path`
  - `reason`
  - `evidence`
  - `evidence_link`
  - `evidence_path`
- every path field begins with `文档路径：`
- any wikilink outside main-line endpoints and `evidence_link` is an error

Expected effect:

- relation ledger formatting becomes enforceable and regression-resistant

### 5. Ontology semantic governance

Ontology semantic governance must extend its review scope.

It should validate:

- the relation-semantic explanation section remains consistent with `ontology/graph-standard.md`
- each instance belongs in the correct relation ledger
- source and target types match the relation’s legal ontology contract
- nearby semantics that should be in `reason` have not been incorrectly promoted into other formal edges
- the explanation section supports edge placement judgment rather than introducing renewed navigation noise

Expected effect:

- semantic governance reviews both edge correctness and relation-ledger semantic framing

### 6. Serving governance

Serving governance changes less than other stages, but it still must recognize the new separation of concerns.

It should validate:

- relation pages remain governance-oriented truth pages rather than default serving entry pages
- object pages remain the primary human-facing serving surfaces
- relation-ledger machine fields do not bleed into object-page serving projections in a way that hurts readability

Expected effect:

- relation pages become more machine-friendly and governance-friendly
- object pages remain more human-friendly and answer-serving-friendly

## Required spec and implementation updates

This design requires updates to at least:

- `ontology/graph-standard.md`
- `ontology/relations/*.md` templates and/or managed content strategy
- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `scripts/lint_graph.py`
- `.claude/skills/ontology-semantic-review/SKILL.md`
- `.claude/skills/serving-governance-review/SKILL.md`

Likely supporting updates:

- `.claude/skills/relation-reconciliation/evals/*`
- `.claude/skills/page-projection-sync/evals/*`
- semantic-review references if they encode relation-page formatting expectations
- serving-governance references if they encode outdated relation-ledger assumptions

## Normative wording recommendation

The normative wording should be updated along the following lines:

```md
- formal relation ledger 页面应收敛为受管关系真源页，固定由“关系语义说明区”和“实例边账本区”构成。
- relation 页中的 Obsidian 跳转仅允许出现在实例边主行的 source、target，以及子项中的 `evidence_link`。
- 每条正式实例边必须按固定顺序显式提供：`source_path`、`target_path`、`reason`、`evidence`、`evidence_link`、`evidence_path`。
- `source_path`、`target_path`、`evidence_path` 必须使用 `文档路径：` 前缀提供显式文档路径。
- `source`、`target`、`evidence_link` 默认使用短 wikilink；若 basename 在 vault 中不唯一，则必须退化为带路径的 wikilink。
- relation 页顶部的对象域导航、证据入口导航及其他非必要跳转不再保留。
- `paper-ingest` 负责产生可渲染的规范化 relation candidate 元数据；`relation-reconciliation` 负责 relation ledger 的最终格式写盘；`page-projection-sync` 只消费 formal relation truth，不定义 relation 页表示层。
```

## Implementation order recommendation

The lowest-risk implementation sequence is:

1. define the canonical relation-ledger template and generation contract
2. update `relation-reconciliation` to render the canonical format
3. update `page-projection-sync` to consume the normalized truth safely
4. update structural governance and semantic governance to prevent regressions
5. update serving governance expectations to reflect the new relation-page role

This order is recommended because relation-ledger formatting truth is owned by reconciliation. If that stage is not updated first, downstream governance can only react to unstable output instead of protecting a stable contract.
