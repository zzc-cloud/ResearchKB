# Index Sync Pipeline Design

Date: 2026-05-05

## Summary

Repair the current single-paper ingest chain by introducing a dedicated `index-sync` stage between object-page projection and governance, so index maintenance becomes an explicit compile artifact rather than an implicit side effect.

The updated daily single-paper chain becomes:

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

This design covers immediately:
- `ontology/index.md`
- `ontology/entities/*/index.md`

It also defines a Phase 2 extension for:
- managed navigation blocks inside relation-ledger pages

It adopts **managed-block updates** rather than full-file regeneration, and separates three concerns that are currently blurred together:
- object truth projection
- navigation truth projection
- serving-surface governance

## Problem

The current ingest chain explicitly covers extraction, relation-ledger completion, object-page projection, structural governance, ontology-semantic governance, and serving governance, but it does not define **who owns index maintenance as a first-class contract**.

In practice, this creates a gap:
- `paper-ingest` historically mentions updating indexes, but that responsibility is mixed into a much broader compile stage.
- `page-projection-sync` owns projection back to object pages, but not navigation surfaces.
- `lint_graph.py` checks repository structure and navigation entry existence, but not comprehensive index completeness.
- `serving-governance-review` currently focuses on page serving quality, not whether index pages are safe and accurate as default navigation/QA entry surfaces.

The result is that index maintenance behaves like a soft convention rather than a governed stage of the compile pipeline.

## Goals

- Make index maintenance an explicit stage in the paper compile pipeline.
- Cover the full navigation surface, not only the system root index.
- Preserve human-authored index prose and grouping where appropriate.
- Use page existence plus structural fields as the sync truth source.
- Add structural lint for index completeness.
- Extend serving governance so index pages are reviewed as default navigation/QA entry surfaces.

## Non-goals

- Rebuild all index files from scratch on every run.
- Turn index pages into relation truth sources.
- Move relation-ledger prose maintenance into `index-sync`.
- Make `index-sync` responsible for fixing malformed pages.
- Collapse structural lint and serving governance into one gate.

## Why a dedicated stage is needed

There are three distinct projection/governance layers:

1. **Formal relation ledger → object pages**
2. **Object/ledger page set → navigation/index pages**
3. **Navigation/index pages → default serving entry review**

The current workflow treats the first layer explicitly via `page-projection-sync`, but the second layer has no dedicated owner. As a result, navigation correctness is hard to audit: when an index entry is stale or missing, it is unclear whether the problem belongs to ingest, projection, or governance.

A dedicated `index-sync` stage fixes that by making navigation projection observable and inspectable in the same way as relation reconciliation and page projection.

## Updated pipeline contract

### Stage 1 — `paper-ingest`
Outputs:
- intermediate caches
- object-page candidate updates
- `relation_candidates`
- `relation_exemptions`
- `updated_pages`
- `warnings`

Responsibility boundary:
- compile paper-derived knowledge artifacts
- do **not** own full index maintenance as a primary responsibility

### Stage 2 — `relation-reconciliation`
Outputs:
- ledger updates
- `added` / `already_present` / `exempt` / `needs_human_review`
- affected page set for downstream sync

Responsibility boundary:
- reconcile formal relation truth into ledgers
- do not sync object or index projections directly

### Stage 3 — `page-projection-sync`
Outputs:
- `synced_pages`
- `updated_sections`
- `manual_followups`

Responsibility boundary:
- sync formal graph truth back into object pages
- update `## Formal relations`
- update strong-consistency frontmatter such as `parent_methods` / `child_methods`
- update templated human relation blocks
- do **not** maintain index pages

### Stage 4 — `index-sync`
Outputs:
- `synced_indexes`
- `skipped_pages`
- `manual_followups`

Responsibility boundary:
- sync navigational projections into index surfaces
- maintain managed blocks only
- do not rewrite human-authored explanatory prose
- do not invent missing page structure

### Stage 5 — structural governance
- `python3 scripts/lint_graph.py`

Responsibility boundary:
- validate index structure completeness and navigation integrity
- do not decide serving quality

### Stage 6 — ontology-semantic governance
- `ontology-semantic-review`

Responsibility boundary:
- review ontology placement/semantics of nodes and relations
- not a replacement for structure lint or serving governance

### Stage 7 — serving governance
- `serving-governance-review`

Responsibility boundary:
- decide whether object pages and index pages are safe as default constrained-QA entry surfaces
- evaluate navigation/serving quality rather than raw structure existence

## `index-sync` design

### Inputs
`index-sync` should consume:
- affected object-page list from `page-projection-sync`
- current object-page files under `ontology/entities/**`
- current relation-ledger files under `ontology/relations/*.md`
- relevant page frontmatter
- projected `## Formal relations` structures
- current index-page contents

It should not consume raw PDFs or unreconciled relation candidates directly.

### Truth source
`index-sync` should use:
- page existence
- node-type-specific structural fields
- enough structure to determine navigation placement and entry status

It should **not** use:
- file existence alone
- post-governance approval as a prerequisite for all index updates

This means `index-sync` is allowed to update indexes before governance completes, but only when the page has enough structure to be placed safely.

### Coverage
`index-sync` should maintain:

1. **System root navigation**
   - `ontology/index.md`

2. **Domain indexes**
   - `ontology/entities/papers/index.md`
   - `ontology/entities/methods/index.md`
   - `ontology/entities/concepts/index.md`
   - `ontology/entities/tasks/index.md`
   - `ontology/entities/scenarios/index.md`
   - `ontology/entities/benchmarks/index.md`

3. **Relation-ledger navigation blocks**
   - managed navigation/aggregation blocks inside `ontology/relations/*.md`
   - not the ledger instance-edge truth prose itself

### Update strategy: managed blocks
`index-sync` should use managed-block updates rather than full-file regeneration.

That means:
- preserve human-authored introductions, notes, grouping rationale, and serving explanations
- update only designated managed sections between explicit markers
- avoid rewriting entire files
- avoid reordering unrelated human prose

This is important because index pages in ResearchKB are not only machine catalogs; they are also human-facing navigation and serving surfaces.

## Index eligibility rules

### A. Eligible for index inclusion
A page may be included in an index when:
- the file exists
- the node type is identifiable
- required frontmatter exists for that node type
- the page has enough structure for stable placement in the target index

Examples:
- a Paper page must expose enough structure to place it by title/role/problem area
- a Method page must expose at least its method type and core classification fields
- a Concept page may need `concept_kind` when the target index groups framework/taxonomy/general concepts separately

### B. Eligible as a default serving entry
A page may be surfaced as a default serving entry only when, in addition:
- it contains `## Formal relations`
- it contains `### Outgoing` and `### Incoming`
- its human-readable sections do not conflict with the projected formal structure
- it is not in an obviously non-ready state that would mislead users or QA traversal

This distinction matters:
- **indexable** does not automatically mean **safe to expose as a default serving entry**
- `index-sync` handles inclusion/projection
- `serving-governance-review` decides default serving exposure quality

## Examples of missing critical structure

When `index-sync` finds a page file but cannot safely place it, the issue is not “a random missing field.” It is missing structure required to decide whether and how the page belongs in navigation.

Typical cases include:
- a Paper page missing required controlled fields such as `problem`, `research_role`, or `status`
- a Method page missing `type`, or exposing `parent_methods` / `child_methods` that are not yet consistent with the formal ledger
- a Concept page missing the fields needed for grouped placement, such as `concept_kind`
- a page file existing without stable serving structure such as `## Formal relations`, `### Outgoing`, and `### Incoming`

In those cases, `index-sync` should not guess or repair the page. It should skip the unsafe placement and report a follow-up.

## `index-sync` output contract

Recommended structured output:

```yaml
status: success | partial | needs-human-review
synced_indexes:
  - path: ontology/index.md
    updated_blocks:
      - object-domain-navigation
      - relation-navigation
  - path: ontology/entities/methods/index.md
    updated_blocks:
      - canonical-list
      - grouped-navigation
skipped_pages:
  - path: ontology/entities/concepts/Foo.md
    reason: missing concept_kind needed for grouped placement
manual_followups:
  - path: ontology/entities/papers/Bar.md
    reason: page exists but lacks serving-ready formal relation structure
```

Interpretation:
- `synced_indexes`: which index surfaces were actually updated
- `skipped_pages`: which pages could not be safely placed into certain managed blocks and why
- `manual_followups`: which pages or index surfaces require later repair or governance attention

## Governance split for indexes

### Structural lint responsibilities
`scripts/lint_graph.py` should enforce the **index completeness baseline**, including checks such as:
- `ontology/index.md` exists and links to all domain indexes
- every domain directory has an `index.md`
- required managed-block markers exist in index files
- index links are not dead
- a page that satisfies minimal inclusion conditions is not silently absent from its domain index
- the root-to-domain navigation chain is intact

Structural lint should not judge whether a page is a high-quality default serving surface.

### Serving governance responsibilities
`serving-governance-review` should enforce the **navigation serving quality line**, including checks such as:
- whether indexes expose truly serving-ready pages as the default entry layer
- whether stub / placeholder / structurally incomplete pages are incorrectly promoted as default entries
- whether index grouping and wording conflict with actual page state
- whether the navigation promise “index → object page → Formal relations → adjacent object/Evidence pages” is actually realizable
- whether index surfaces distinguish “indexed but not default-serving” pages when needed rather than mixing them together

The boundary is:
- lint asks: **does the navigation structure exist and connect correctly?**
- serving review asks: **is this navigation safe and useful as a default QA surface?**

## Required file and contract changes

### 1. `CLAUDE.md`
Update the single-paper and batch-paper workflows so the default chain becomes:
- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`
- `index-sync`
- structural governance
- ontology-semantic governance
- serving governance

Also extend interruption conditions to include `index-sync` failure or substantial `manual_followups`.

### 2. `.claude/skills/paper-ingest/SKILL.md`
Revise the skill so index maintenance is no longer described as a primary responsibility of ingest.

`paper-ingest` should remain the compile entrypoint that produces pages, caches, and relation candidates, but it should hand off index maintenance to `index-sync` downstream.

### 3. `.claude/skills/page-projection-sync/SKILL.md`
Revise the skill so its responsibility ends at object-page projection.

Its documented successor chain should become:
- `index-sync`
- `python3 scripts/lint_graph.py`
- `ontology-semantic-review`
- `serving-governance-review`

### 4. `.claude/skills/index-sync/SKILL.md`
Add a new skill contract defining:
- when to use the stage
- expected inputs
- truth-source rules
- managed-block update strategy
- output schema
- handoff to lint and serving governance

### 5. `.claude/skills/serving-governance-review/SKILL.md`
Extend the skill so index pages are explicitly in scope as serving/navigation entry surfaces, not only object pages.

### 6. `scripts/lint_graph.py`
Add index completeness and managed-block integrity checks without expanding lint into serving-quality judgment.

### 7. `ontology/graph-standard.md`
Add a concise normative section clarifying that:
- index pages are navigation projections, not relation truth sources
- index managed blocks are maintained by `index-sync`
- indexability and serving-readiness are distinct states
- serving exposure is ultimately gated by serving governance

## Rollout strategy

### Phase 1
Cover:
- `ontology/index.md`
- `ontology/entities/*/index.md`

Do not yet attempt deep automation of complex human prose in relation-ledger pages. Only support managed navigation blocks there after the primary object-domain path is stable.

### Phase 2
Extend `index-sync` to relation-ledger navigation blocks after root and domain index behavior is stable.

This reduces rollout risk and addresses the highest-value navigation surfaces first.

## Explicit stop conditions

The chain should allow interruption when:
1. `paper-ingest` returns `needs-skill-update`
2. `relation-reconciliation` returns substantial `needs_human_review`
3. `page-projection-sync` returns substantial `manual_followups`
4. `index-sync` returns failure or substantial `manual_followups`
5. any governance gate fails

This keeps index maintenance observable and prevents hidden promotion of half-synced navigation.

## Success criteria

After this change:
1. the default paper compile chain explicitly includes `index-sync`
2. index maintenance has a dedicated contract owner
3. index pages are updated through managed blocks rather than ad hoc edits or full rewrites
4. structural lint catches missing index coverage and broken navigation structure
5. serving governance explicitly reviews index pages as default navigation/QA entry surfaces
6. `paper-ingest` and `page-projection-sync` no longer carry ambiguous index-maintenance ownership

## Recommendation

Proceed with a focused contract-first rollout:
1. update workflow/contracts
2. define managed-block conventions
3. add lint coverage
4. extend serving governance
5. implement `index-sync`

This is the clearest way to close the current pipeline gap without conflating object truth, navigation truth, and serving-surface quality.