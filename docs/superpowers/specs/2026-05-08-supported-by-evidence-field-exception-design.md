---
title: Supported By Evidence Field Exception Design
date: 2026-05-08
tags:
  - spec
  - researchkb
  - ontology
  - relations
  - supported-by
status: draft
---

# Supported By Evidence Field Exception Design

Date: 2026-05-08

## Summary

This spec defines a single relation-type exception for ResearchKB formal instance-edge formatting:

- For all formal relation types except `supported_by`, `- evidence:` remains required.
- For `supported_by`, `- evidence:` is no longer allowed.
- The reason is structural: the target of `supported_by` is already an `Evidence` object, so repeating the same object again in `- evidence:` is redundant and increases semantic confusion.

The goal is to make the full compile pipeline consistent with this rule:

- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`
- structural governance
- ontology semantic governance
- serving governance

## Problem

Current `supported_by` ledger entries use the same canonical relation-record format as all other relation types:

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: ...
  - evidence: [[...]]
```

For most relation types, this is clear:

- `target` = the neighboring ontology object
- `evidence` = the evidence anchor proving the relation

But for `supported_by`, the target is already an `Evidence` object:

```md
- `[[路径优先化]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`
  - reason: 路径优先化概念定义由 sections 证据页支撑。
  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]
```

In this pattern:

- the relation target is `PathMind.sections`
- the `evidence` field is also `PathMind.sections`

So the entry repeats the same object in two structural roles.

This creates a conceptual problem:

1. readers can no longer easily distinguish “relation target” from “evidence field”
2. the ledger format suggests there are two distinct evidence-bearing objects when there is only one
3. the repetition adds no new information in the current model

## Goals

- Remove structural redundancy from `supported_by` ledger entries.
- Make `supported_by` semantically clearer than the current target-plus-identical-evidence pattern.
- Preserve the existing canonical relation format for all other relation types.
- Keep the change narrowly scoped to one relation type.
- Align all pipeline stages and governance surfaces with the new rule.

## Non-goals

- Redesign all relation instance formatting.
- Introduce fine-grained evidence anchors or nested evidence blocks.
- Add optional evidence-field behavior for `supported_by`.
- Change object-page semi-expanded serving projection format.

## Confirmed design decision

### Core rule

`supported_by` becomes a relation-type exception:

- `reason` remains required
- `evidence` is forbidden
- target must remain an `Evidence` object

### Allowed `supported_by` ledger form

```md
- `[[路径优先化]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`
  - reason: 路径优先化概念定义由 sections 证据页支撑。
```

### Forbidden `supported_by` ledger form

```md
- `[[路径优先化]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`
  - reason: 路径优先化概念定义由 sections 证据页支撑。
  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]
```

### Other relation types remain unchanged

The following still require explicit `- evidence:`:

- `cites`
- `proposes`
- `based_on`
- `targets_task`
- `uses_concept`
- `evaluated_on`
- `sourced_from`

## Why this is the right boundary

### 1. Better than merely tolerating redundancy

If the system only “accepts” the duplicated `evidence` field but keeps generating it, the semantic confusion remains permanent. That would preserve uniform formatting at the cost of clarity.

### 2. Better than redesigning all relation records

A whole-ledger redesign would be too large for the actual problem. The confusion is isolated to one relation type because only `supported_by` elevates an `Evidence` object directly into the target position.

### 3. Better than allowing optional `evidence` for `supported_by`

Optionality would increase ambiguity:

- some `supported_by` entries would include `evidence`
- some would omit it
- readers and pipeline stages would still need to reason about both forms

A strict exception is cleaner:

- `supported_by`: no `evidence`
- everything else: `evidence` required

## Compile-pipeline alignment

### 1. `paper-ingest`

`paper-ingest` does not directly own formal truth, but it emits candidates and shapes page drafts.

It must align to the new rule by:

- continuing to emit `supported_by` candidates where appropriate
- not treating `supported_by` as a relation type that needs an extra `evidence` field in its candidate expression or narrative examples
- continuing to treat the target Evidence object as the support anchor

Expected effect:

- `supported_by` candidates remain available downstream
- no early-stage duplication pressure remains in the ingest contract

### 2. `relation-reconciliation`

This is the most important generation-stage change.

It must enforce:

- for non-`supported_by` relations:
  - `reason` required
  - `evidence` required
- for `supported_by`:
  - `reason` required
  - `evidence` forbidden
  - target must be an `Evidence` object

Expected effect:

- formal ledgers become the first place where the new rule is actually materialized
- reconciliation becomes the canonical place that prevents regressions

### 3. `page-projection-sync`

Object-page and Evidence-page serving projections do not normally expose ledger `- evidence:` lines directly, but this stage still consumes the ledger structure.

It must align by:

- not assuming `supported_by` entries contain `- evidence:`
- deriving `supported_by` projections from source, target Evidence, and reason only
- preserving all existing semi-expanded serving projection rules

Expected effect:

- projections remain stable
- no serving-page logic depends on a field that is no longer valid for `supported_by`

### 4. Structural governance

Structural governance must harden the rule, not merely allow it.

Required checks:

- non-`supported_by` relation entries still require `- evidence:`
- `supported_by` relation entries must not include `- evidence:`
- `supported_by` targets must remain Evidence pages

Expected effect:

- the new formatting rule becomes enforceable rather than advisory

### 5. Ontology semantic governance

Semantic governance must update its review model:

- absence of `- evidence:` in `supported_by` is not an error
- presence of `- evidence:` in `supported_by` should be treated as semantically unclear or outdated formatting
- source-type and target-type checks remain unchanged

Expected effect:

- semantic review no longer mistakes the new canonical form for an omission

### 6. Serving governance

Serving governance changes minimally, but it must understand the new truth surface:

- `supported_by` entries in ledgers no longer repeat target Evidence in an `evidence` field
- object-page serving projections remain interpretable because they already project `supported_by` through target Evidence links

Expected effect:

- serving review continues to focus on readability and traversability, without preserving obsolete ledger assumptions

## Required spec changes

This design requires updates to:

- `ontology/graph-standard.md`
- `ontology/relations/supported_by.md`
- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `scripts/lint_graph.py`
- `.claude/skills/ontology-semantic-review/SKILL.md`
- `.claude/skills/serving-governance-review/SKILL.md`

Likely supporting eval / checklist updates:

- `.claude/skills/relation-reconciliation/evals/*`
- `.claude/skills/page-projection-sync/evals/*`
- semantic review references if they explicitly describe relation-record expectations

## Governance wording recommendation

The new normative wording should say:

```md
- 默认情况下，正式实例边必须显式提供 `- evidence:` 字段，指向该关系成立的直接证据锚点。
- `supported_by` 属于例外关系：其 target 必须为 Evidence 对象，且不再允许重复书写 `- evidence:`。
- `supported_by` 的支撑语义由 source、target Evidence 与 `reason` 三者共同构成。
```

This wording is intentionally strict:

- not optional
- not “may omit”
- explicitly forbids duplicated `evidence` on `supported_by`

## Acceptance criteria

This change is complete when all of the following are true:

1. `supported_by` entries in `ontology/relations/supported_by.md` no longer carry `- evidence:` lines.
2. Other relation ledgers still require `- evidence:`.
3. `relation-reconciliation` treats `supported_by` as a no-`evidence` exception.
4. `page-projection-sync` no longer assumes `supported_by` ledger entries include `evidence`.
5. structural governance rejects `supported_by` entries that still repeat `- evidence:`.
6. ontology semantic governance accepts the new `supported_by` form as canonical.
7. serving governance remains green on pages generated from the revised ledger model.

## Recommendation

Adopt this as a strict relation-type exception rather than a soft optional rule.

The clean conceptual split should be:

- `supported_by`: target is the Evidence object; no duplicated `evidence` field
- all other relation types: target is not Evidence; explicit `evidence` remains required
