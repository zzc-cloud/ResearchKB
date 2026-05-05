# Formal Candidate Extraction Gap Fix Design

Date: 2026-05-05

## Summary

Fix the root cause behind missing formal relations after the standard ingest pipeline by strengthening candidate extraction and reconciliation rules rather than continuing to rely on post-hoc manual audits.

The key observation is that the compile pipeline now exists and works, but some relationships expressed clearly in migrated object pages still do not enter the formal graph because they are not systematically promoted into `relation_candidates` or revisited during reconciliation.

This design focuses on upgrading:
- `paper-ingest`
- `relation-reconciliation`

so that strong human-friendly semantic statements can be recognized as candidate formal edges when ontology rules allow it and evidence is sufficient.

## Problem

Recent audits showed that some links appearing in human-friendly relation blocks are not merely context-only — some of them should actually become formal relations, but they are not consistently captured by the standard ingest pipeline.

Examples include:
- method pages that clearly state a primary scenario but do not consistently produce `applies_to`
- paper pages that clearly name core concepts but do not always promote them into explicit `uses_concept`
- task-focused statements that should become `targets_task`
- framework concept pages that clearly name their scenario target but depend on later cleanup to formalize it

This means the formal graph can remain narrower than the page semantics, even when the evidence already exists.

## Root cause

The root cause is not that the evidence is missing.

The root cause is that the standard pipeline does not yet have a strong enough rule for upgrading some human-friendly high-semantic statements into formal relation candidates.

### Current pattern
- `paper-ingest` reliably extracts direct relations such as `proposes`, `supported_by`, `cites`, `sourced_from`
- but some strongly expressed page semantics remain only in human-friendly blocks
- `relation-reconciliation` mainly compares existing candidates, page-implied relations, evidence, and ledgers, but it still depends too heavily on the candidate set already being explicit
- `page-projection-sync` does not invent formal relations, so once these relations are missed earlier, they stay missing

## Goals

- Upgrade the candidate extraction rules for strong semantic statements.
- Upgrade reconciliation rules so these statements are re-audited if they still did not become explicit candidates.
- Reduce future dependence on post-hoc manual formal relation expansion.
- Keep the boundary between formal neighbors and context-only links clear.

## Non-goals

- Turn every human-friendly link into a candidate relation.
- Move candidate extraction into `page-projection-sync`.
- Redesign all relation types.
- Eliminate the relation-expansion audit workflow entirely.

## Guiding principle

Only a subset of human-friendly statements should be promoted into formal relation candidates.

The rule is:
> If a human-friendly block expresses a strong semantic relation, the ontology allows that relation type, and evidence is sufficient, then the relation should be promoted into candidate formal status upstream rather than discovered only later in audits.

## Priority candidate sources

The upgrade should focus on **strong semantic statements**, not general related-links blocks.

### 1. Method pages: primary scenario statements

Pattern:
- `主要场景：[[Scenario]]`

Expected candidate relation:
- `[[Method]] --applies_to--> [[Scenario]]`

This is the clearest recurring gap in the current migrated pages.

### 2. Paper pages: core concept statements

Pattern:
- `核心概念：[[Concept]]`
- or equivalent explicit wording in core contribution / method blocks

Expected candidate relation:
- `[[Paper]] --uses_concept--> [[Concept]]`

### 3. Paper pages: core/related task statements

Pattern:
- `相关任务：[[Task]]`
- `核心任务：[[Task]]`
- equivalent explicit wording in problem framing

Expected candidate relation:
- `[[Paper]] --targets_task--> [[Task]]`

### 4. Framework-concept pages: explicit scenario target statements

Pattern:
- `场景：[[Scenario]]`
- `面向：[[Scenario]]`

Expected candidate relation:
- `[[Concept]] --applies_to--> [[Scenario]]`

## What should NOT be upgraded automatically

These remain context-only unless separately justified:
- broad “相关方法 / 路线” blocks on concept pages
- comparison links
- background route mentions
- further-reading links
- benchmark pages linking tasks/scenarios where no formal relation type currently exists

## `paper-ingest` changes

### Add a stronger candidate-upgrade rule

When building `relation_candidates`, `paper-ingest` should explicitly scan for high-semantic statements in the generated or updated object-page candidate structures.

It should promote candidate edges when all are true:
1. the statement uses a strong semantic label such as
   - 主要场景
   - 核心概念
   - 核心任务 / 相关任务
   - 场景 / 面向（for framework concepts)
2. the ontology has a valid relation type
3. supporting evidence is available in the current caches

### Candidate promotion examples
- method “主要场景” → `applies_to`
- paper “核心概念” → `uses_concept`
- paper “相关任务” → `targets_task`
- framework concept “场景” → `applies_to`

## `relation-reconciliation` changes

### Add a strong-semantic re-audit layer

Even if `paper-ingest` misses one of these, `relation-reconciliation` should inspect the updated object pages for strong semantic labels and re-evaluate them as candidate formal edges.

This means reconciliation should not only compare:
- explicit `relation_candidates`
- evidence-backed edges
- current ledgers

It should also look for:
- high-priority semantic phrases in human-friendly blocks

### Reconciliation rule

If a strong semantic statement exists in an object page, and the ontology + evidence support a formal edge, but the edge is absent from both:
- `relation_candidates`
- the ledger

then classify it as:
- `add_now` if evidence is sufficient and relation type is unambiguous
- `needs_human_review` if evidence or granularity is still ambiguous

## Why this fix belongs upstream, not in page sync

`page-projection-sync` should not be responsible for discovering new formal relations. Its job is to project already accepted formal truth back onto pages.

If candidate promotion is not fixed in `paper-ingest` and `relation-reconciliation`, then page sync will always be downstream of a narrower-than-intended graph.

## Success criteria

After this fix:
- fewer valid formal edges are discovered only in late audit passes
- method→scenario `applies_to` becomes more consistent
- paper→concept `uses_concept` becomes more consistent
- paper→task `targets_task` becomes more consistent
- framework concept→scenario `applies_to` becomes more consistent
- the relation-expansion audit shifts from discovering obvious missing edges to auditing genuinely ambiguous boundaries

## Recommendation

Proceed with a focused upstream fix in `paper-ingest` and `relation-reconciliation`.

This is the highest-value correction because it addresses the actual root cause: some clearly formalizable page semantics are not entering the candidate relation pipeline early enough.
