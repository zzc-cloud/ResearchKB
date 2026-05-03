# Knowledge Compile Pipeline Design

Date: 2026-05-03

## Summary

Redesign the ResearchKB single-paper ingest pipeline into an explicit three-skill compile chain followed by three governance gates:

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

The goal is to stop treating relation completeness and page-serving alignment as incidental side effects of ingest. Instead, ingest should emit structured relation candidates, reconciliation should close the formal relation ledger, and page projection sync should realign governed object pages with the updated ledger.

## Problem

The current workflow can successfully extract a paper, generate intermediate caches, and update some object pages and relation ledgers. But the repository keeps surfacing a recurring failure mode:

- evidence exists
- object pages mention relations in prose
- some formal relations are present
- but the relation ledgers are still incomplete
- and the pages are no longer aligned with the formal graph truth

This means the existing pipeline is not closed. Missing relations are often discovered later by serving migration, lint refinement, or manual QA work rather than being reconciled as part of the ingest pipeline itself.

This is not just a `paper-ingest` extraction bug. It is a pipeline design problem.

## Goals

- Preserve `paper-ingest` as the single-paper ontology-instance compile entrypoint.
- Add an explicit post-ingest relation reconciliation stage.
- Add an explicit page projection sync stage after ledger updates.
- Separate extraction, formal-ledger reconciliation, and page projection into distinct responsibilities.
- Ensure the final output of a paper compile is ready for structural, ontology-semantic, and serving governance.

## Non-goals

- Rebuild all legacy content immediately.
- Turn `paper-ingest` into a monolithic “do everything” skill.
- Make `page-projection-sync` rewrite interpretive prose or editorial analysis.
- Replace existing governance layers with a single gate.

## Why the current process breaks down

The current workflow bundles too many concerns into ingest-time behavior:
- extracting paper content
- creating evidence caches
- generating or updating object pages
- writing some relation ledger entries
- implicitly hoping the whole graph is now complete

But graph completeness and page-serving alignment are not local properties of a single paper. They are graph-level properties.

As serving-ready requirements expanded, the old ingest boundary stopped being sufficient. The result is a recurring mismatch between:
- evidence-backed claims
- relation ledgers
- object-page projections

## Proposed architecture

### 1. `paper-ingest`

Role:
- single-paper ontology-instance compiler

Responsibilities:
- parse the paper
- determine paper type
- generate `intermediate/papers/*` caches
- generate or update object-page candidates
- identify direct and high-confidence formal relation candidates
- emit structured `relation_candidates` and `relation_exemptions`

It answers:
> What objects and relation candidates does this paper directly justify?

### 2. `relation-reconciliation`

Role:
- formal relation completion and ledger alignment stage

Responsibilities:
- read `paper-ingest` outputs
- compare relation candidates against current ledgers
- compare evidence-backed claims against current ledgers
- detect missing formal edges
- route new edges to the correct `wiki/relations/*.md` ledger file
- distinguish between already-present edges, add-now edges, exempt edges, and human-review edges
- report affected object pages that now need projection sync

It answers:
> After incorporating this paper into the graph, which formal edges are still missing or unresolved?

### 3. `page-projection-sync`

Role:
- relation-ledger to object-page projection synchronizer

Responsibilities:
- read the updated formal ledgers
- update `## Formal relations`
- update strong-consistency frontmatter fields
- update templated human-readable relation sections
- leave interpretive prose alone

It answers:
> Once the formal graph is updated, how should the affected object pages be realigned with that truth?

## Compile chain

The new compile chain becomes:

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`

Only after those three should the output be handed to governance:

4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

## `paper-ingest` minimal upgrade

The minimum viable upgrade to `paper-ingest` is not “generate more pages.” It is “emit better structured relation output.”

### New required output blocks

`paper-ingest` should extend its structured completion summary with:

```yaml
relation_candidates:
  proposes:
    - source: "[[Paper]]"
      target: "[[Method]]"
      evidence: "[[intermediate/papers/foo.sections|foo.sections]] §x"
  targets_task: []
  evaluated_on: []
  uses_concept: []
  supported_by: []
  cites: []
  applies_to: []
  based_on: []
  improves_on: []
  sourced_from: []

relation_exemptions:
  - relation_type: evaluated_on
    reason: no unified benchmark; exempt by graph-standard
```

### Candidate confidence tiers

The skill should distinguish three categories:

1. **direct relations**
   - clear, immediately ledger-writable
   - examples: `proposes`, `supported_by`, `cites`, `sourced_from`

2. **high-confidence candidate relations**
   - strongly supported but still graph-sensitive
   - examples: `based_on`, `improves_on`, `applies_to`, `uses_concept`

3. **needs-human-review relations**
   - ambiguous node type, relation direction, or granularity

This gives downstream reconciliation a real contract rather than forcing it to infer everything from prose.

## `relation-reconciliation` design

### Inputs

It should consume four classes of input:

1. `paper-ingest` structured outputs
   - `relation_candidates`
   - `relation_exemptions`
   - `updated_pages`
   - `warnings`

2. changed object pages
   - `wiki/papers/`
   - `wiki/methods/`
   - `wiki/concepts/`
   - `wiki/tasks/`
   - `wiki/scenarios/`
   - `wiki/benchmarks/`

3. changed evidence caches
   - `sections.md`
   - `refs.md`
   - `experiments.md`
   - `analysis.md`
   - `full.md`

4. current relation ledgers
   - `citation_graph.md`
   - `method_evolution.md`
   - `concept_links.md`
   - `task_method_map.md`
   - `benchmark_links.md`
   - `evidence_index.md`
   - `paper_method_links.md`
   - `provenance_links.md`

### Core operations

It should do three things:

#### A. Normalize
Convert inputs into a common edge representation such as:
- source
- relation_type
- target
- evidence
- source_of_claim

#### B. Diff
Compare:
- candidate edges
- page-implied edges
- evidence-backed edges
- current formal ledger edges
- explicit exemptions

#### C. Reconcile
Classify edges into:
- `already_present`
- `add_now`
- `exempt`
- `needs_human_review`

### Required output

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

### Ledger routing rules

The skill must route edges according to `graph-standard.md`:
- `proposes` → `paper_method_links.md`
- `targets_task` → `task_method_map.md`
- `evaluated_on` → `benchmark_links.md`
- `uses_concept` / `supports` / `depends_on` / `applies_to` → `concept_links.md`
- `based_on` / `improves_on` → `method_evolution.md`
- `cites` → `citation_graph.md`
- `supported_by` → `evidence_index.md`
- `sourced_from` → `provenance_links.md`

### Additional responsibility: detect prose-ledger drift

The skill should also report when object pages already imply a relation in readable sections, but the formal ledger lacks the edge. This is one of the most common sources of downstream serving inconsistency.

## `page-projection-sync` design

### Purpose

After the formal ledgers are reconciled, object pages must be reprojected so humans and LLMs read aligned relation surfaces.

### Inputs
- updated formal ledgers
- `relation-reconciliation` output
- affected object pages

### Automatically synchronized content

#### 1. `Formal relations`
- `### Outgoing`
- `### Incoming`
- evidence lines
- `- 无` when needed

#### 2. Strong-consistency frontmatter
- currently includes:
  - `parent_methods`
  - `child_methods`
- can expand later to other explicitly declared strong-consistency fields

#### 3. Templated human-readable relation sections
Examples:
- related methods
- related tasks
- related concepts
- related benchmarks
- representative papers
- evidence sources

### Not automatically synchronized

This skill should not rewrite:
- method explanation prose
- problem framing prose
- strengths/limitations analysis
- key conclusions
- editorial commentary
- human notes

It is a projection synchronizer, not a general page author.

### Suggested output

```yaml
status: success | partial | needs-human-review
synced_pages:
  - path: wiki/methods/Foo.md
    updated_sections:
      - formal_relations
      - frontmatter
      - human_relation_blocks
manual_followups:
  - path: wiki/papers/Bar.md
    reason: interpretive prose not auto-synced
```

## Governance remains downstream

The new compile chain does not replace governance. It prepares better inputs for governance.

### Structural governance
- `python3 scripts/lint_graph.py`
- validates structure, format, required sections, and automatable projection constraints

### Ontology-semantic governance
- `ontology-semantic-review`
- validates entity typing, relation placement, and ontology position

### Serving governance
- `serving-governance-review`
- validates serving completeness, alignment, traversability, and release readiness

## Recommended rollout order

### Phase 1: update `paper-ingest` output contract
Do not yet rewrite the whole skill flow. First, make relation candidates and exemptions explicit.

### Phase 2: create draft `relation-reconciliation` skill
Implement the normalize → diff → reconcile workflow and output contract.

### Phase 3: create draft `page-projection-sync` skill
Implement the projection sync boundary and affected-page workflow.

### Phase 4: run one or two sample paper pipelines end-to-end
Use a standard empirical method paper first.

### Phase 5: integrate with the three governance gates
Ensure the pipeline hands off cleanly to lint, ontology semantic review, and serving governance review.

## Why this split is worth it

This design prevents three common failure modes:

1. `paper-ingest` becoming an oversized monolith
2. relation completeness being discovered too late
3. object pages drifting away from formal graph truth after ledger updates

The split also makes each layer independently improvable:
- extraction quality can improve without changing page sync logic
- relation reconciliation can improve without reopening PDF parsing
- page projection can improve without changing formal-ledger rules

## Recommendation

Adopt the three-skill compile chain:
- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`

Use `paper-ingest` for direct paper understanding, `relation-reconciliation` for formal graph closure, and `page-projection-sync` for human/LLM page alignment. Then keep lint, ontology semantic review, and serving governance review as downstream publish gates.
