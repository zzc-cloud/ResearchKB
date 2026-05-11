# Remove Concept Entity from Phase-1 Ontology Design

## Context
ResearchKB is currently trying to use a single ontology layer for both direct paper extraction and higher-order conceptual abstraction. In practice, the `Concept` entity has become the largest source of phase-1 extraction ambiguity. It overlaps with `Method`, sometimes with `Task`, and has required a dedicated relation family (`uses_concept`) whose source/target legality has repeatedly conflicted with the surrounding ontology contract.

The user's direction is now explicit: ResearchKB should optimize for a **phase-1 method graph**, not a mixed method-plus-concept ontology. Even for survey papers, the user's priority is to extract the concrete methods, tasks, scenarios, benchmarks, and evidence-supported method relations described in the paper. Any later “concept layer” should be treated as a separate second-phase abstraction built on top of a stable phase-1 graph, not as part of direct ingest.

That means phase 1 should remove `Concept` entirely rather than continue trying to narrow or partially retain it.

## Goal
Redefine the live ResearchKB ontology as a phase-1 method graph by removing the `Concept` entity and the `uses_concept` relation from the formal ontology, pages, navigation, and processing skills.

## Non-goals
- Do not introduce the second-phase concept layer in this change.
- Do not replace `Concept` with a new entity type in phase 1.
- Do not preserve a reduced or “special-case” concept domain.
- Do not attempt to solve future abstraction-layer design in this phase.

## Design decisions

### 1. Phase 1 becomes a method-fact ontology
The phase-1 ontology should contain only entities that are directly and relatively stably extractable from papers:
- `Paper`
- `Method`
- `Task`
- `Scenario`
- `Benchmark`
- `Evidence`
- `RawSource`

Remove:
- `Concept`

Rationale:
- These retained entities are closer to direct paper facts and lower-variance ontology judgments.
- `Concept` is more interpretive and should be deferred until there is a stable base graph to abstract from.

### 2. Remove `uses_concept` from the formal relation set
The phase-1 formal relation set should become:
- `proposes` (`Paper -> Method`)
- `based_on` (`Method -> Method`)
- `references_method` (`Method -> Method`)
- `targets_task` (`Method -> Task`)
- `applied_in` (`Method -> Scenario`)
- `evaluated_on` (`Method -> Benchmark`)
- `supported_by`
- `cites`
- `sourced_from`

Remove:
- `uses_concept`

Rationale:
- Once `Concept` is removed, `uses_concept` no longer has a valid target class.
- Mechanism- or terminology-level descriptions should stay in Method, Paper, or Evidence prose during phase 1.

### 3. Reinterpret framework / taxonomy / terminology content in phase 1
Phase 1 should not create standalone concept objects for frameworks, taxonomies, or mechanism terms.

Use these rules instead:
- If the paper contributes an executable or reusable technical workflow, model it as `Method`.
- If the paper introduces organizing terminology, framework language, taxonomy labels, or analytical distinctions that are not themselves reusable methods, keep them in `Paper` / `Method` / `Evidence` prose only.
- Do not force such items into new phase-1 entities.

Rationale:
- This keeps phase 1 grounded in reusable technical objects and avoids premature abstraction.

### 4. Survey papers remain compatible with a method-graph-first phase
Removing `Concept` does not prevent survey-paper ingestion.

In phase 1, survey papers should still be compiled by extracting:
- discussed or grouped methods
- task coverage
- scenario coverage
- benchmark coverage
- citation and method-reference structure
- evidence-backed comparative framing where it maps cleanly onto existing relation families

What phase 1 should not do for survey papers:
- create standalone concept pages for every recurring term
- create ontology-level conceptual abstractions during direct ingest

Rationale:
- The user’s goal is for survey papers to enrich the method graph first; conceptual abstraction comes later.

### 5. Defer conceptual abstraction entirely to phase 2
The current change should say nothing operational about phase 2 beyond one boundary statement:
- phase 2 may later build a concept/abstraction layer derived from the stable phase-1 graph

But phase 1 should not contain any active traces of that future layer in:
- ontology contracts
- entity domains
- formal relation families
- ingest requirements
- serving assumptions

Rationale:
- The user explicitly does not want phase 2 reflected yet.
- Mentioning future abstractions only as an implementation note prevents phase-1 ontology drift.

## Consequences

### Positive
- Removes the largest current source of extraction ambiguity.
- Simplifies ontology classification during ingest.
- Removes the need to decide `Concept vs Method` and `Concept vs Task` during phase 1.
- Eliminates `uses_concept`, which has been a recurring source of contract conflicts.
- Makes survey ingestion focus on method structure instead of abstract terminology.

### Accepted trade-offs
- Phase 1 loses standalone concept pages.
- Users will no longer navigate directly to concept objects in the live ontology.
- Framework / taxonomy terms that are not methods will remain in prose rather than as first-class phase-1 entities.
- Some explanatory power moves from formal graph structure into page narrative and evidence pages.

## Files and system areas affected

### Ontology contract
Update `ontology/graph-standard.md` to:
- remove `Concept` from node types
- remove all `Concept`-specific object-page contract sections
- remove `uses_concept` from formal relation definitions
- rewrite any references to framework/taxonomy modeling so phase 1 either maps them to `Method` or keeps them in prose
- update minimal-link and serving rules that currently mention Concept

### Entity domains
Remove or retire the phase-1 domain:
- `ontology/entities/concepts/`
- `ontology/entities/concepts/index.md`
- all concept object pages under that directory

### Relation ledgers
Remove:
- `ontology/relations/uses_concept.md`

Update any relation guidance or governance docs that still assume `uses_concept` exists.

### Live pages
Remove concept references from live serving pages where they currently appear as formal neighbors or required sections.
This includes at least:
- Method pages that currently project `uses_concept`
- Paper pages whose prose or Formal relations depend on concept pages
- Task / Scenario pages that mention Concept as a live ontology domain instead of prose-only terminology

### Processing and governance skills
Update ingest, reconciliation, projection, review, and serving guidance so they no longer:
- classify candidates as `Concept`
- emit `uses_concept`
- require concept pages in phase 1
- treat concept pages as a serving domain

## Migration principle
This is a **phase-1 ontology contraction**, not a reinterpret-everything exercise.

The migration rule should be:
- if a former Concept is actually a reusable technical workflow, re-evaluate it as `Method`
- otherwise, remove it as a formal entity and preserve its information in prose / evidence only

This avoids inventing replacement entity types just to preserve prior structure.

## Verification expectations
Implementation should verify that after the change:
- no `Concept` entity domain remains in the live phase-1 ontology
- no `uses_concept` relation ledger remains
- no ontology rule still requires Concept classification in phase 1
- ingest/review/projection skills do not emit or expect Concept / `uses_concept`
- existing pages remain lint-clean and semantically coherent after concept removal

## Scope boundary
This design is intentionally strict:
- phase 1 removes Concept completely
- phase 2 is not designed here
- the current system should behave as though Concept does not exist

That hard boundary is the whole point of the redesign.