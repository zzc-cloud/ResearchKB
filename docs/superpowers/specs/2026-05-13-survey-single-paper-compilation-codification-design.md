# Survey single-paper compilation codification for ResearchKB

## Context
The recent repair work on the paper [A survey of large language model-augmented knowledge graphs for advanced complex product design](../../ontology/entities/papers/A%20survey%20of%20large%20language%20model-augmented%20knowledge%20graphs%20for%20advanced%20complex%20product%20design.md) exposed a gap between the intended ontology contract and the actual single-paper compilation pipeline.

The current chain

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

can already handle empirical method papers reasonably well, but survey papers with structured method coverage still require manual repair to reach the desired end state. In the LLM-KG-CPD case, we had to manually:

- materialize survey-covered Methods as `status: partial`
- add `surveys_method` relations
- add `supported_by` relations
- project those relations back into the survey page, Method pages, and Evidence pages
- align methods index entries
- teach lint that `surveys_method` is a valid Method paper anchor
- add human-readable representative paper anchors to the new partial Methods
- clean stale prose left by the earlier conservative ingest path

This shows the current pipeline is missing a first-class survey-compilation contract.

At the same time, not every survey paper has structured method coverage. Some surveys are mostly concept review, landscape synthesis, benchmark analysis, or challenge/future-work synthesis. Therefore the fix cannot be “all survey papers automatically emit `surveys_method` and representative paper artifacts.” The pipeline needs a graded coverage model.

The user has explicitly chosen a **wide detection threshold** for survey papers, but not a reckless one: the system should aggressively detect survey-covered methods, while still separating direct automatic admissions from candidates that require stronger reconciliation or human review.

## Goal
Codify survey-paper single-paper compilation so that the default daily pipeline can reach the repaired LLM-KG-CPD-style outcome automatically **when a survey actually contains stable structured method coverage**, while remaining conservative for surveys that do not.

## Non-goals
- Do not force every survey paper to emit formal `surveys_method` relations.
- Do not require all survey-mentioned methods to become formal Methods.
- Do not require all representative papers to become Formal Paper pages.
- Do not redesign the empirical method-paper path.
- Do not expand the ontology to direct `Task -> Scenario` or `Scenario -> Task` relations.

## Core design

### 1. Introduce a three-tier survey coverage model
Survey-paper compilation must classify method-like items into three tiers.

#### Tier A — direct survey-covered method candidates
These are safe for default automatic admission.

They must satisfy all of the following:
- stable reusable Method identity
- evidence that the survey structurally covers them rather than casually mentioning them
- enough local evidence to write a minimal `object_semantics`
- a stable representative paper can be identified

Examples of structural support include:
- method grouping tables
- taxonomy/grouping sections
- comparison matrices
- role-based coverage tables
- explicit coverage lists of named methods

For Tier A candidates, the default chain should automatically produce:
- partial Method pages
- `surveys_method` formal relations
- representative paper stub / anchor pages
- matching `cites` relations from the survey paper to those representative paper stubs
- `supported_by` relations
- page projections
- index projections
- lint-valid paper-anchor closure

#### Tier B — high-confidence survey method candidates
These have promising Method identity but insufficient confidence for immediate automatic formal admission.

Typical reasons:
- stable method name, but weak or partial structural grouping
- representative paper identified, but coverage semantics still borderline
- the survey seems to use the item as an example or representative work rather than a clear admitted method object

For Tier B candidates, the chain should automatically produce:
- `semantic_stub_candidates`
- candidate representative paper metadata
- explicit handoff into `relation-reconciliation`

But it should **not** automatically write formal `surveys_method`, paper stub, or `cites` ledgers at ingest time.

#### Tier C — needs-human-review survey candidates
These are not safe for automatic admission.

Typical reasons:
- only related-work mention
- title looks like a method, but object identity is unstable
- item is better understood as system, application, scenario, benchmark, or concept
- representative paper identity is weak or ambiguous

These should remain outside the default formal graph and be surfaced only as explicit review output.

### 2. Codify a survey-derived method admission contract
When a Tier A survey-covered method is materialized, the resulting partial Method must satisfy a stronger minimum contract than the current ad hoc behavior.

Required outputs:
- `status: partial` Method page
- incoming `surveys_method`
- outgoing `supported_by`
- human-readable `## 代表论文`
- at least one valid paper anchor

The paper anchor is two-layered:
- formal anchor: incoming `surveys_method` from the survey Paper
- human/provenance anchor: representative paper title in `## 代表论文`

If representative paper identity is stable, the pipeline should additionally create a representative Paper Stub / Anchor page so that future independent ingest has a stable landing point.

### 3. Add a survey-derived representative paper provenance contract
For Tier A survey-covered methods with stable representative papers, the default automatic pipeline should generate representative paper stubs and corresponding `cites` edges.

This contract is intentionally stronger than “Method has a source survey anchor” alone.

Default pattern:
- survey Paper `--surveys_method-->` partial Method
- survey Paper `--cites-->` representative Paper Stub / Anchor
- partial Method page names that representative paper in `## 代表论文`
- representative paper stub remains non-serving and lives only as an anchor unless later upgraded by full ingest

This does **not** make the representative paper a Formal Paper automatically.
It only provides stable paper-level provenance and a future upgrade target.

### 4. Keep wide detection, not wide admission
The user chose a wide default threshold. In practice, this should mean:
- the ingest stage aggressively tries to discover survey-covered methods
- but only Tier A gets default automatic admission
- Tier B must be explicitly handed off for reconciliation
- Tier C must remain review-only

This preserves automation without over-promoting noisy survey references into the formal graph.

## Changes required by pipeline stage

### A. `paper-ingest`
`paper-ingest` must gain a survey-specialized coverage-detection branch.

For survey/framework/taxonomy/landscape papers, it should:
1. detect structured method coverage signals
2. classify method-like objects into Tier A/B/C
3. emit normalized outputs for each tier

#### New ingest outputs for Tier A
For each direct survey-covered method candidate, emit:
- `surveys_method` candidate
- `supported_by` candidate
- `representative_paper_candidate`
- `paper_stub_candidate`
- `cites` candidate
- `object_semantics`
- `semantic_stub_candidate` with `serving_readiness_hint: partial`

#### New ingest outputs for Tier B
Emit:
- `high-confidence survey method candidate`
- optional representative paper metadata
- enough evidence metadata for reconciliation

#### New ingest outputs for Tier C
Emit:
- `needs-human-review survey candidate`
- explicit reason why default admission was rejected

#### Ingest prose/cache behavior
The generated evidence caches should stop emitting stale blanket prose like “this ingest does not promote high-volume survey references into `surveys_method`” once Tier A admissions have actually been materialized. Instead they should say:
- which subset was admitted now
- which remainder stayed deferred
- why the remainder was deferred

### B. `relation-reconciliation`
`relation-reconciliation` must no longer accept the following state as success:
- survey paper has Tier A coverage outputs
- but no `surveys_method` relations are added

For Tier A candidates it must:
- add `surveys_method`
- add `supported_by` if absent
- materialize representative paper stubs when needed
- add matching `cites`
- surface source survey page, Method pages, Evidence pages, and paper stub pages in `affected_pages`

For Tier B candidates it must:
- explicitly decide `add_now` vs `needs_human_review`
- never silently drop them just because ingest did not already formalize them

For representative paper stubs it must:
- keep them in stub/anchor semantics, not upgrade them to Formal Paper automatically
- ensure they are routable to papers index non-serving blocks

### C. `page-projection-sync`
This stage must formally support the survey-derived object cluster:
- source survey Paper page
- newly materialized partial Method pages
- representative paper stub pages
- supporting Evidence pages

It must automatically project:
- survey Paper outgoing `surveys_method`
- Method incoming `surveys_method`
- Method outgoing `supported_by`
- Evidence incoming `supported_by`
- representative paper stubs’ formal relations if they bear formal edges

It must also write the human-readable `## 代表论文` block when the ledger/evidence contract provides a representative paper anchor.

The LLM-KG-CPD repair showed that Evidence incoming projection is not optional; it must be part of the default projection contract for survey-derived `supported_by` edges.

### D. `index-sync`
`index-sync` must recognize survey-derived outputs as follows:
- partial Methods enter the Methods index default navigable block
- representative paper stubs enter the Papers index non-serving block
- nothing in this path should auto-promote a representative paper stub to default paper entry

### E. `python3 scripts/lint_graph.py`
Lint must be updated to match the codified ontology behavior.

Required changes:
1. Treat incoming `surveys_method` as a valid formal/partial Method paper anchor.
2. Validate that survey-derived `supported_by` edges are projected on both Method and Evidence pages.
3. If the codified path includes representative paper stubs and default `cites`, validate those stubs and citations as part of the survey-derived provenance closure.
4. Validate that materialized survey-derived partial Methods include a representative paper human-readable anchor section.

The purpose is to align lint with the graph standard rather than forcing future survey repairs to re-teach lint ad hoc.

### F. `ontology-semantic-review`
The semantic review skill must explicitly distinguish three valid survey states:
1. no structured method coverage → no `surveys_method` required
2. structured coverage with Tier A admissions → `surveys_method` required
3. borderline coverage → Tier B/Tier C review path allowed

It should flag as medium/high priority when:
- a survey has clear Tier A coverage but no `surveys_method`
- a materialized survey-derived Method lacks representative paper provenance
- a representative paper stub was wrongly upgraded to Formal Paper without independent ingest

### G. `serving-governance-review`
Serving governance must recognize the new valid survey-derived serving path:
- survey Paper → partial Method → Evidence
- survey Paper → representative paper stub (non-serving)

It must treat that as valid if:
- traversal is explicit
- statuses are correctly exposed
- paper stubs remain non-default serving
- readers/LLMs are not forced to fall back to relation ledgers to understand the next hop

## Required `ontology/graph-standard.md` changes
These rules belong in the normative ontology document, not only in skills.

### 1. `surveys_method` threshold clarification
Add explicit wording that:
- not every survey produces `surveys_method`
- only structured method coverage justifies direct formal admission
- ordinary related-work mention, trend discussion, or high-volume citation lists do not

### 2. Survey-derived method admission contract
Add a rule that a Method admitted through stable survey coverage may be `status: partial`, and must carry:
- formal survey Paper anchor
- representative paper human-readable anchor
- optional representative paper stub / anchor when paper identity is stable

### 3. Representative paper stub and `cites` contract for survey-derived methods
Add wording that when a survey-derived partial Method has a stable representative paper, the representative paper may be materialized as a Paper Stub / Anchor and linked by `cites` from the source survey Paper, without upgrading that stub to Formal Paper.

### 4. Minimum link obligation clarification for survey-derived partial Methods
Clarify that the “1 representative paper” minimum may be satisfied initially by:
- `## 代表论文` prose anchor
- plus representative paper stub / anchor when available
- without requiring immediate Formal Paper promotion

## Validation criteria
The codified pipeline is correct when a survey paper with LLM-KG-CPD-level structured method coverage can pass through the default chain and end in the repaired state automatically, including:
- partial Method materialization
- `surveys_method`
- `supported_by`
- representative paper anchor prose
- paper stub and `cites` closure
- page projections on survey / Method / Evidence pages
- index routing for Methods and non-serving Paper stubs
- clean lint
- semantic review acceptance
- serving governance acceptance

At the same time, a survey paper without stable structured method coverage must still compile successfully without being forced into artificial `surveys_method` output.

## Risks and mitigations

### Risk 1: over-admission of noisy survey mentions
Mitigation:
- three-tier coverage model
- only Tier A gets default automatic admission
- Tier B forced through reconciliation review
- Tier C remains review-only

### Risk 2: provenance bloat from too many paper stubs
Mitigation:
- only Tier A gets representative paper stubs by default
- stubs remain non-serving
- no automatic Formal Paper promotion

### Risk 3: ontology/skill/lint drift reappears
Mitigation:
- update `ontology/graph-standard.md`
- update all affected skills
- update lint in the same implementation track
- test the full daily survey chain end-to-end

## Recommended implementation order
1. Update `ontology/graph-standard.md` with the new survey-derived method admission and representative paper anchor rules.
2. Update `paper-ingest` output contract for Tier A/B/C survey coverage.
3. Update `relation-reconciliation` to materialize Tier A methods, representative paper stubs, and `cites`.
4. Update `page-projection-sync` and `index-sync` to project the expanded survey-derived graph.
5. Update `scripts/lint_graph.py` to validate the new normative contract.
6. Update semantic and serving governance expectations.
7. Validate using the LLM-KG-CPD survey as the reference case.
