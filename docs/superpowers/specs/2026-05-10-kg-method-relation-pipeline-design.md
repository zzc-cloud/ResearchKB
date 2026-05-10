---
title: KG Method Relation Pipeline Optimization Design
date: 2026-05-10
tags:
  - design
  - researchkb
  - ontology
  - pipeline
  - method-relations
status: draft
---

# KG Method Relation Pipeline Optimization Design

## Summary

This design optimizes the ResearchKB single-paper compile pipeline around method-graph completeness rather than paper-only citation completeness.

The confirmed direction is:

1. `references_method` and `based_on` become the two core method-neighbor relations in the pipeline.
2. `evaluated_on` is narrowed globally to **Method -> Benchmark** only.
3. When a missing upstream object is stably identified as a Method by ingest-time evidence, it is materialized directly as a **partial Method**, not as a Method placeholder.
4. The only placeholder state retained in this area is **Paper placeholder** for unresolved citation targets that do not yet have stable Method identity.
5. partial Method pages are allowed into `navigation-entries` and therefore become directly navigable from method-domain indexes.
6. Method pages must expose both `based_on` and `references_method` in a dedicated evolution section instead of collapsing everything into one prose paragraph.
7. Object-page default wikilinks are simplified from `[[../x|Name]]` to `[[../x]]` while keeping explicit document-path hints in formal projections.

This is a pipeline-level correction, not a one-off PathMind patch.

## Problem

The current pipeline has five coupled gaps.

### 1. `references_method` is missing from the live compile path

Although `references_method` already exists in the ontology, the single-paper compile chain does not consistently extract, reconcile, materialize, and project it. As a result, many method-neighbor relations are either:

- lost entirely,
- incorrectly folded into `based_on`, or
- left only as paper-level `cites`.

This makes the method graph systematically thinner than the paper graph.

### 2. Missing upstream methods are not materialized as Method objects

When a paper clearly treats RoG / GCR / EPERM / ToG / KnowPath style neighbors as method-level comparison or reference targets, the current flow may still stop at paper placeholders or no page at all. That breaks method-evolution navigation and weakens ontology expansion around methods.

### 3. `evaluated_on` is too broad

The current contract still allows `Paper -> Benchmark`, which mixes publication-level evidence statements with benchmark usage as a method-level graph relation. The desired contract is narrower: `evaluated_on` should represent that a **Method** is evaluated on a benchmark.

### 4. Method pages do not present the two core neighbor types clearly

Current Method pages have only a loose “方法演化位置” narrative section. This does not clearly separate:

- strict lineage / upstream inheritance (`based_on`)
- key comparison / borrowing / route-reference neighbors (`references_method`)

As a result, the most important method-graph semantics are under-expressed in the human-readable serving layer.

### 5. Object-page default links are noisier than necessary

The current generated default form `[[../methods/RoG|RoG]]` is redundant in this vault because formal projections already carry explicit document paths. The default object-page link form should be simplified to the shortest Obsidian-jump form that still resolves correctly.

## Goals

- Make method-neighbor extraction first-class in the single-paper pipeline.
- Distinguish strictly between `based_on` and `references_method` at ingest, reconciliation, projection, lint, and review layers.
- Guarantee that method-level missing neighbors become navigable Method pages when their identity is stable.
- Narrow `evaluated_on` globally to `Method -> Benchmark`.
- Make Method pages clearly readable as evolution / reference surfaces.
- Simplify generated object-page wikilinks without losing path clarity.
- Preserve paper placeholders for citation connectivity where Method identity is still not stable.

## Non-goals

- Introduce a new pipeline stage solely for method-neighbor materialization.
- Remove `cites`; paper-level citation truth remains necessary.
- Make relation ledgers adopt the same display simplification immediately if not needed.
- Solve all serving-quality issues for every historical page in one pass.

## Confirmed design decisions

### 1. Global `evaluated_on` contraction

The ontology contract changes from:

- `Paper|Method -> Benchmark`

to:

- `Method -> Benchmark`

Implications:

- `ontology/graph-standard.md` must be updated.
- `ontology/relations/evaluated_on.md` must be updated.
- `paper-ingest` must stop producing `Paper -> Benchmark` relation candidates.
- `relation-reconciliation` must reject such candidates.
- `page-projection-sync` and `index-sync` must stop expecting paper-level benchmark adjacency.
- lint must reject `Paper` as an `evaluated_on` source.

### 2. Only two retained intermediate states in this area

For missing upstream neighbors, the design retains only:

- **partial Method**
- **Paper placeholder**

`Method placeholder` is removed.

Rationale:

- once a missing neighbor is stably identified as a Method and already participates in method-level formal relations, it should enter the graph as a real Method object, not as a weaker placeholder façade;
- paper placeholders remain useful only for paper-level citation connectivity when method identity is not yet stable.

### 3. partial Method is directly navigable

If a Method is partial but structurally valid, it may enter `navigation-entries` in the method domain index.

This design adopts the user-confirmed rule:

- **partial in index = navigable**

This means serving status and navigation status are not treated as the same question for Method partials. A partial Method may be directly reachable through index navigation even if it remains governance-incomplete in other ways.

### 4. `references_method` is a pipeline-core relation

`references_method` is no longer treated as an optional or weak afterthought in extraction logic. The pipeline must explicitly decide, for each method-neighbor candidate, whether it belongs to:

- `based_on`
- `references_method`
- `cites` only

The distinction is:

- `based_on`: strict upstream method lineage / inherited route / concrete method foundation
- `references_method`: key comparison object / borrowing route / method-level reference without lineage inheritance
- `cites`: paper-level reference when stable Method identity is absent

### 5. Object-page link simplification

For object pages and Evidence pages, the default generated link form becomes:

- `[[../methods/RoG]]`

instead of:

- `[[../methods/RoG|RoG]]`

The explicit document-path annotation remains in formal projection entries, so path clarity is preserved even after removing display-text duplication.

This simplification applies to:

- Paper
- Method
- Concept
- Task
- Scenario
- Benchmark
- Evidence
- domain indexes

Relation ledgers are not forced into the same simplification in this design unless required by implementation convenience.

## Pipeline redesign

## 1. `paper-ingest`

`paper-ingest` becomes responsible for explicit method-neighbor candidate extraction.

### New required outputs

For method papers, ingest must classify upstream method-neighbor evidence into:

- `based_on` candidates
- `references_method` candidates

It must also determine whether a missing target has enough stable Method identity to materialize as a partial Method.

### Candidate decision rules

A missing upstream target should be upgraded from paper-only reference into a method-level candidate only if all of the following are stable from the current paper:

1. the paper treats it as a Method rather than only as a cited paper;
2. the paper supports at least one clear method-level relation (`based_on`, `references_method`, or incoming `proposes`);
3. the paper provides a normal `object_semantics` statement for the Method target.

### `evaluated_on` behavior

Ingest no longer emits:

- `Paper -> Benchmark`

Instead it emits only:

- `Method -> Benchmark`

Paper pages may still discuss benchmarks in prose, but no formal benchmark edge is emitted from Paper.

## 2. `relation-reconciliation`

`relation-reconciliation` becomes the decisive stage for routing method-neighbor candidates.

### Responsibilities added

- separate `based_on` and `references_method`
- reject paper-level `evaluated_on`
- materialize missing upstream Methods as partial Method pages when their Method identity is stable
- keep `cites` for unresolved paper-only references

### Routing rules

- If the candidate expresses strict inherited route / upstream method foundation → `based_on`
- If it expresses comparison object / borrowed route / representative reference → `references_method`
- If only paper-level citation exists and Method identity is not stable → `cites`

### Materialization handoff

When a target Method page does not exist but the Method identity is stable, reconciliation produces a direct page-materialization handoff rather than leaving the graph unresolved.

## 3. `page-projection-sync`

`page-projection-sync` must synchronize the new method-neighbor structure back onto Method pages.

### Section redesign

The old section label:

- `## 方法演化位置`

is replaced with:

- `## 方法演化与参照关系`

This section contains two human-readable subgroups:

- 上游演化方法
- 关键参照方法

These are explanatory blocks. Formal truth still lives in `## Formal relations`.

### Derived-field rules

- `parent_methods` / `child_methods` derive only from `based_on`
- `references_method` never writes to `parent_methods` / `child_methods`

### Link simplification

All new object-page projection links generated by this stage use the simplified form `[[../x]]`.

## 4. `index-sync`

`index-sync` must treat partial Method pages as normal navigable entries in the method domain.

### Rules

- partial Method → `navigation-entries`
- Paper placeholder → remains in non-serving placeholder area
- no Method placeholder branch remains

This design deliberately aligns index behavior with the confirmed user rule that partial pages in index should already be navigable.

## partial Method materialization contract

A missing upstream Method is materialized as a **partial Method** when all of the following are available from the current paper:

1. stable Method identity
2. normal `object_semantics`
3. at least one stable formal relation
4. at least one valid Evidence anchor from `refs.md`, `sections.md`, or `experiments.md`

### Required structure

A partial Method page must contain:

- frontmatter with controlled fields
- `status: partial`
- `## Object semantics`
- `## 当前定位`
- `## 与知识库现有内容的关系`
- `## 最小定义/角色`
- `## 待补充`
- `## Formal relations`
- `### Outgoing`
- `### Incoming`

### Content principles

A partial Method is not a weak placeholder. It is a real Method object page with incomplete explanatory coverage.

Therefore:

- `object_semantics` should describe the Method normally
- formal relations should be real projected neighbors
- `待补充` records remaining missing narrative or evidence depth, not object-identity uncertainty

## Page-level presentation changes

## 1. Method pages

### Human-readable section change

Replace “方法演化位置” with:

- `## 方法演化与参照关系`

This section explains:

- which neighbors are true upstream lineage (`based_on`)
- which neighbors are key reference / comparison methods (`references_method`)

### Formal projection expectations

`## Formal relations` continues to project both relation types explicitly and separately.

## 2. Paper pages

Paper pages no longer expose formal `evaluated_on` outgoing edges. Benchmark discussion remains in prose only.

## 3. Benchmark pages

Benchmark pages receive only incoming `evaluated_on` from Method sources.

## 4. Object-page default links

Default body links and projected links on object pages become path-only Obsidian links:

- `[[../methods/RoG]]`
- `[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]`

The `|Display Name` suffix is removed by default.

## Validation and regression scope

## 1. Normative files

Update and verify:

- `ontology/graph-standard.md`
- `ontology/relations/evaluated_on.md`
- `ontology/relations/references_method.md`

## 2. Pipeline files

Update and verify:

- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `.claude/skills/index-sync/SKILL.md`
- `scripts/lint_graph.py`

## 3. PathMind regression

PathMind becomes the required regression sample. It must prove that:

- `references_method` is generated
- missing upstream methods such as RoG / GCR / EPERM / ToG / KnowPath are materialized as partial Methods when their Method identity is stable
- `Paper -> Benchmark` is no longer generated
- Method pages expose both relation families in the new evolution section
- object-page default links are simplified

## 4. Governance checks

### lint additions

lint must reject:

- `Paper` as `evaluated_on` source
- Method-neighbor unresolved targets that should have been materialized as partial Method
- newly generated object-page links that still default to `[[../x|Name]]`

### semantic review focus

semantic review must explicitly ask:

- is this truly `based_on`?
- should this instead be `references_method`?
- is this only `cites` because Method identity is not stable?

### serving review focus

serving review should stop treating partial Method visibility in method index as an automatic defect. Instead it should focus on whether the partial Method page remains structurally navigable and semantically legible.

## Success criteria

The redesign is successful when:

1. method papers produce explicit `based_on` / `references_method` method-neighbor output;
2. stable missing upstream methods no longer stay only as cited papers and instead become navigable partial Method pages;
3. `evaluated_on` is globally Method-only;
4. Method pages explain both lineage and reference neighbors clearly;
5. newly generated object pages default to the simplified Obsidian link form.

## Recommended implementation order

1. update ontology norms (`graph-standard`, `evaluated_on`, `references_method`)
2. update lint to enforce the new contracts
3. update `paper-ingest` candidate extraction and output contract
4. update `relation-reconciliation` routing and partial Method materialization
5. update `page-projection-sync` Method section generation and link simplification
6. update `index-sync` to allow partial Method into `navigation-entries`
7. run PathMind regression and governance review
