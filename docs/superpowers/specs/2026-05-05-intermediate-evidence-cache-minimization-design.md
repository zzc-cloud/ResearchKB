# Intermediate Evidence Cache Minimization Design

Date: 2026-05-05

## Summary

Retain `intermediate/papers/` as the formal Evidence cache layer, but reduce it to a hard-minimum cache set keyed by paper type.

The new default is:

- empirical papers → `sections + refs + experiments`
- survey / framework / taxonomy papers → `sections + refs + analysis`
- theoretical / position papers → `sections + refs`

`full` is removed as a formal cache type.

This change preserves the existing ontology separation between `Paper` and `Evidence`, keeps `wiki/papers/` as the serving-ready Paper layer, and makes `intermediate/papers/` a smaller, more auditable, more lintable Evidence layer.

## Problem

The current architecture correctly separates:
- `wiki/papers/` as the formal Paper serving layer
- `intermediate/papers/` as the reusable Evidence layer

That separation is still desirable and should remain.

The problem is not the existence of `intermediate/papers/` itself. The problem is that the cache layer currently has weak size and type boundaries. In particular, `full` has not established a distinct evidence responsibility. In current usage it behaves mostly like a slightly longer restatement of content already covered by `sections`, while also introducing extra links, extra provenance maintenance, and extra opportunities for drift.

This creates three system problems:

1. Evidence cache growth is not tightly bounded by ontology role.
2. Some cache types risk duplicating Paper-page narrative instead of serving a distinct evidence function.
3. Lint and workflow rules cannot enforce a stable minimum cache contract per paper type.

## Goals

- Keep `intermediate/papers/` as a distinct Evidence layer.
- Hard-limit cache generation to the minimum set that has distinct evidence value.
- Remove `full` as a formal cache type.
- Encode paper-type-to-cache-set rules in ontology/process standards.
- Make provenance independent of any special full-text cache.
- Make cache expectations lintable and pipeline-stable.

## Non-goals

- Merge `Paper` and `Evidence` into a single node type.
- Turn `wiki/papers/` into the primary evidence cache layer.
- Rewrite all existing object pages for style.
- Introduce a new family of replacement cache types.
- Re-ingest the entire repository in this pass.

## Why `intermediate/papers/` should remain

The repository ontology explicitly distinguishes `Paper` and `Evidence`. That distinction is still correct.

`wiki/papers/` should remain the serving-ready Paper layer used for default question answering and formal object consumption. `intermediate/papers/` should remain the Evidence layer used for:
- mechanism verification
- experiments and metrics lookup
- citation and baseline grounding
- provenance tracing
- cross-page evidence reuse by methods, tasks, concepts, benchmarks, and scenarios

Removing the separate Evidence layer would weaken evidence granularity, blur `supported_by` semantics, and make cross-node reuse depend on narrative Paper pages rather than dedicated evidence artifacts.

Therefore this design does not collapse layers. It narrows the Evidence layer to its minimum justified footprint.

## Cache minimization decision

### Hard-minimum cache sets

The repository should enforce the following required cache sets:

#### 1. Empirical papers
Required caches:
- `sections`
- `refs`
- `experiments`

Rationale:
- `sections` carries mechanism and chapter-structured evidence.
- `refs` carries citation, baseline, and upstream-work evidence.
- `experiments` carries benchmark, metric, ablation, efficiency, and result evidence.

#### 2. Survey / framework / taxonomy papers
Required caches:
- `sections`
- `refs`
- `analysis`

Rationale:
- these papers often do not have a conventional experiment package that deserves `experiments`
- their third evidence surface is usually landscape synthesis, categorization, stage analysis, framework decomposition, or benchmark-survey evidence
- `analysis` is the right carrier for that non-empirical third evidence role

#### 3. Theoretical / position papers
Required caches:
- `sections`
- `refs`

Rationale:
- these papers may lack experimental sections that support formal `evaluated_on` or result claims
- they still need mechanism/argument structure and citation grounding

## Removal of `full`

`full` should be removed as a formal cache type.

### Reasoning

A cache type deserves to exist only if it has a distinct evidence responsibility that is not already provided by the retained cache set.

In current repository usage, `full` does not demonstrate that role:
- it is rarely referenced outside a few explicit links
- it is not required to support core formal relations
- it is not the unique carrier of experiments, citations, or mechanism evidence
- its provenance role can be replaced cleanly by direct Evidence-to-RawSource links

Therefore `full` adds maintenance cost without establishing independent ontology value.

### Replacement rule

There is no replacement cache for `full` in this design.

If a future workflow genuinely requires a new cache type, that type must be introduced by updating ontology/process standards first, with an explicit evidence responsibility. It must not be reintroduced ad hoc through a new file in `intermediate/papers/`.

## Evidence responsibilities by cache type

### `sections`
Purpose:
- chapter structure
- core mechanism description
- chapter-level summaries sufficient to support formal relation auditing

Must do:
- preserve section-level organization
- carry enough structured detail to support method/concept/task/scenario/benchmark relations

Must not do:
- become a near-full-paper rewrite
- become a second narrative Paper page
- accumulate long cross-section prose that adds no new audit value

Working rule:
> If additional `sections` content does not improve formal-relation auditability or section-level reusability, it should not be added.

### `refs`
Purpose:
- explicit citation grounding
- baseline and upstream-work evidence
- method-lineage and related-work support where citation evidence is primary

### `experiments`
Purpose:
- benchmark bindings
- metrics
- ablations
- efficiency comparisons
- result interpretation for empirical papers

Constraint:
- this is the normal third cache for empirical papers
- it should not be replaced by `analysis` for standard empirical cases

### `analysis`
Purpose:
- landscape analysis
- framework decomposition
- taxonomy/stage synthesis
- benchmark-survey or non-unified-evaluation evidence

Constraint:
- `analysis` is only for survey / framework / taxonomy / benchmark-landscape style papers
- it is not a general “extra summary” cache
- it is not the normal third cache for empirical papers

## Provenance rules after `full` removal

`full` must no longer be the implicit provenance anchor.

New rule:
- every formal Evidence cache may directly carry
  - `[[intermediate/papers/<short_name>.<cache_type>]] --sourced_from--> [[raw/<pdf>]]`

Implications:
- provenance does not depend on the existence of a special full-text cache
- `sections`, `refs`, `experiments`, and `analysis` are all valid provenance-bearing Evidence nodes
- deleting `full` does not weaken traceability so long as retained caches preserve `source_pdf` and provenance ledger links

## Redundancy retirement rule

Add a general retirement rule for cache governance:

> If a cache type does not carry an independent evidence responsibility and does not provide non-replaceable structured audit value relative to existing cache types, it must not be maintained as a formal cache type.

This rule is broader than `full`. It is intended to prevent future drift into redundant cache forms such as summary-like or notes-like pages that duplicate existing Evidence roles.

## Required repository changes

### 1. `wiki/ontology/graph-standard.md`
Update the standard to:
- remove `full` from the allowed/recognized formal cache set
- encode the required cache-set mapping by paper type
- define the boundaries of `sections`
- define the boundaries of `analysis`
- define the redundancy retirement rule
- update provenance guidance so all retained Evidence caches can be direct `sourced_from` nodes

### 2. `CLAUDE.md`
Update project instructions so `intermediate/papers/` is described as a minimal Evidence cache layer, not a broad working-draft space.

It should no longer imply a normal “high-fidelity draft” cache as part of standard ingest output.

### 3. Ingest / compile skill docs
Update relevant skills so they:
- no longer generate `full` by default
- choose cache outputs according to paper type
- treat the minimum cache-set contract as part of compile correctness

### 4. `scripts/lint_graph.py`
Add or strengthen checks for:
- paper-type-specific minimum cache sets
- forbidden presence of `cache_type: full`
- forbidden object-page references to `*.full`
- forbidden provenance dependencies on `*.full`
- appearance of undeclared new cache types

### 5. Existing content cleanup
Perform a focused cleanup pass to:
- delete existing `*.full.md`
- remove “high-fidelity draft” references from object pages
- migrate `provenance_links.md` away from `full --sourced_from--> raw`
- align remaining Evidence links with the minimized cache model

## Migration strategy

This should be a controlled contraction, not a content-expansion effort.

Recommended order:

1. Update standards first.
2. Update skill and pipeline expectations second.
3. Update lint rules third.
4. Clean up existing references and legacy `full` files last.

This order prevents the repository from landing in an ambiguous half-state where generation rules, standards, and enforcement disagree.

## Success criteria

The change is successful when all of the following are true:

1. No formal cache in the repository uses `cache_type: full`.
2. `intermediate/papers/` contains only recognized minimal Evidence cache types.
3. Empirical, survey/framework/taxonomy, and theoretical/position papers each have an explicit required cache-set rule.
4. `wiki/papers/`, provenance ledgers, standards, skills, and lint all use the same cache-type contract.
5. `supported_by` and `sourced_from` remain auditable without relying on `full`.
6. New cache types cannot be introduced informally without a prior standards update.

## Risks and controls

### Risk 1: `sections` regrows into `full`
Control:
- define `sections` boundaries explicitly in the standard
- treat excess narrative duplication as a governance violation
- document in skill guidance that `sections` is not a replacement for `full`

### Risk 2: `analysis` is misused as a general extra-summary page
Control:
- restrict `analysis` to survey / framework / taxonomy / benchmark-landscape style papers
- prohibit it as the default third cache for standard empirical papers

### Risk 3: provenance becomes inconsistent during migration
Control:
- migrate provenance links before deleting legacy references
- require retained Evidence pages to remain provenance-capable

### Risk 4: standards, skills, and lint diverge
Control:
- land standard, skill, and lint changes in the same migration pass
- do not leave cache minimization as an undocumented convention

## Recommendation

Proceed with a hard-minimum Evidence cache model:
- keep `intermediate/papers/`
- remove `full`
- enforce cache-set rules by paper type
- move provenance onto retained Evidence caches
- use standards + skills + lint together to prevent regression

This is the smallest architecture-preserving change that reduces redundancy without weakening ontology separation, evidence auditability, or serving-layer clarity.
