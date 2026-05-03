# Method/Paper Serving Layer Design

Date: 2026-05-03

## Summary

Reframe ResearchKB into a three-layer model:

1. `wiki/relations/` remains the authoritative instance-edge source for authoring and governance.
2. Governed `wiki/methods/` and `wiki/papers/` pages become the default serving layer for constrained knowledge QA.
3. `intermediate/papers/` remains the evidence layer for mechanism, experiment, citation, and provenance verification.

The core change is to stop treating `wiki/relations/` as the default runtime read path for QA. Instead, QA should anchor on a key entity, read its governed object page, expand through a normalized `Formal relations` section, and only descend into `intermediate/papers/` when evidence verification is required.

## Problem

The current system mixes two concerns:

- `wiki/relations/` acts as the formal graph ledger.
- entity pages act as human-readable object pages with partial relation projections.

This creates ambiguity about which layer should be used during question answering. If QA must always read `wiki/relations/`, then entity pages are not sufficient serving surfaces. If QA skips `wiki/relations/` without stronger guarantees, completeness and ontology-instance accuracy can degrade.

The desired model is:

- `wiki/relations/` stays as governance truth.
- entity pages align with that truth tightly enough that both humans and LLMs can use them directly.
- QA no longer needs to read `wiki/relations/` by default.

## Goals

- Keep `wiki/relations/` as the authoritative source for formal instance edges.
- Upgrade Method and Paper pages into governed serving pages for QA.
- Align human-visible entity pages with AI-consumable formal relation content.
- Preserve completeness and ontology-instance accuracy.
- Make entity-centric constrained exploration the default QA path.

## Non-goals

- Redesign all node types in the first phase.
- Replace `intermediate/papers/` as the evidence layer.
- Remove or flatten the relation ledger.
- Expand the first rollout beyond Method and Paper pages.

## Architecture

### 1. Authoring and governance truth layer

Location: `wiki/relations/`

Responsibilities:
- maintain canonical instance edges
- bind relation type, direction, and evidence
- support linting, ontology governance, projection validation, and repair

This layer remains the authoritative graph truth, but is no longer the default QA runtime surface.

### 2. Governed serving layer

Location: `wiki/methods/`, `wiki/papers/`

Responsibilities:
- serve as the default object-centric entrypoint for constrained QA
- present relation information in both human-readable and machine-readable form
- expose enough local topology that QA can expand from an entity page without reading `wiki/relations/` by default

Each governed Method/Paper page should contain:
- frontmatter: compact structured summary derived from the ledger
- human-friendly relation sections: readable object-centric views
- `Formal relations` section: normalized machine-readable relation projection

### 3. Evidence layer

Location: `intermediate/papers/`

Responsibilities:
- support verification of mechanisms, experiments, references, baselines, and provenance
- remain the drill-down layer when QA needs evidence backing rather than only topology

## Entity page design

### Frontmatter role

Frontmatter should no longer be treated as hand-maintained relation truth. It should be a compact structured projection derived from the relation ledger.

Keep in frontmatter:
- identity/classification fields such as `title`, `type`, `problem`, `industry`, `research_role`
- a very small set of high-value derived fields

For the first phase, derived relation fields should stay narrow:
- Method: `parent_methods`, `child_methods`

Do not expand frontmatter into a second relation ledger. Most relation content should stay out of metadata and instead appear in page relation views.

### Human-friendly relation sections

These sections are optimized for reading and navigation.

Method pages should expose object-centric views such as:
- upstream methods
- downstream methods
- related tasks
- related concepts
- application scenarios
- representative papers
- key evidence

Paper pages should expose views such as:
- proposed methods or concepts
- target tasks
- used concepts
- evaluation benchmarks
- key cited work
- key evidence caches

These sections may summarize or group relations for readability, but must not conflict with the authoritative ledger.

### Formal relations section

Each Method/Paper page should also contain a normalized `Formal relations` section designed for direct LLM consumption.

Required properties:
- explicit relation type
- explicit direction
- split into outgoing and incoming relations
- evidence links preserved
- fixed format with minimal prose

Illustrative shape:

```markdown
## Formal relations

### Outgoing
- `[[PathMind]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```

This section is the serving-time formal graph surface for QA. It is not a prose summary.

## Governance requirements

To allow QA to skip `wiki/relations/` by default, governance must validate more than simple non-conflict.

### 1. Projection consistency

Validate that:
- derived frontmatter fields match the ledger
- the `Formal relations` section matches the ledger in node identity, relation type, direction, and evidence linkage
- human-friendly sections do not contradict the ledger

### 2. Projection completeness

Validate that the relevant one-hop formal relations for a Method/Paper entity are projected into the page according to serving rules.

This includes:
- required frontmatter projections for designated derived fields
- complete one-hop projection into the `Formal relations` section
- preservation of both outgoing and incoming formal edges
- preservation of evidence entrypoints

Human-friendly sections may summarize, but the `Formal relations` section must be complete enough for QA traversal.

### 3. QA consumability

Validate that the page is not only correct but also usable as a serving surface.

Check for:
- stable `Formal relations` section presence
- predictable outgoing/incoming structure
- normalized edge formatting
- resolvable evidence links
- enough one-hop topology to support constrained expansion

## QA workflow redesign

### Previous mental model

A linear path such as:
- `wiki/ontology/index.md`
- `wiki/ontology/graph-standard.md`
- `wiki/relations/`
- formal object pages
- `intermediate/papers/`

### New default model

1. identify candidate key entities from the user question
2. resolve the entity type and object page
3. read the entity page
4. use frontmatter plus the `Formal relations` section for one-hop constrained expansion
5. assess whether the explored topology is sufficient
6. expand to adjacent entities only when needed
7. descend into `intermediate/papers/` when mechanism, experiment, citation, or evidence verification is needed
8. answer with explicit separation between formal conclusions, evidence-backed conclusions, and remaining inferences

### Role of index and graph standard

`wiki/ontology/index.md` remains the navigation and entry rule layer.

`wiki/ontology/graph-standard.md` remains the ontology and legality layer.

They still matter, but they should not force a fixed runtime sequence where QA must read `wiki/relations/` before object pages. The primary runtime serving surface becomes governed Method/Paper pages.

## Query expansion discipline

Constrained expansion should follow typed edges rather than arbitrary links.

Examples:
- evolution questions prioritize `based_on`, `improves_on`, and neighboring Method entities
- task-fit questions prioritize `targets_task`, `applies_to`, `uses_concept`
- paper contribution questions prioritize `proposes`, `targets_task`, `uses_concept`, `evaluated_on`, `cites`

The LLM should stop expanding once the required entities, formal relations, and evidence anchors are sufficient for the question.

## Required documentation changes

### `wiki/ontology/index.md`

Clarify that:
- governed object pages are the default QA entrypoint
- `wiki/relations/` is the governance ledger entrypoint
- `intermediate/papers/` is the evidence entrypoint

### `wiki/ontology/graph-standard.md`

Add or revise sections to define:
- truth layer vs serving layer separation
- Method/Paper projection requirements
- `Formal relations` section requirements
- governance checks for consistency, completeness, and QA consumability
- constrained QA consumption rules

### `CLAUDE.md`

Update workflow guidance so that:
- QA defaults to anchored exploration from governed object pages
- governance still treats `wiki/relations/` as formal truth
- `wiki/relations/` is no longer part of the default QA read path

## Rollout plan

### Phase 1: normalize the rules
- update `wiki/ontology/graph-standard.md`
- update `wiki/ontology/index.md`
- update `CLAUDE.md`

### Phase 2: define serving templates
- define a standard Method page structure
- define a standard Paper page structure
- define which relations project to frontmatter, human-friendly sections, and `Formal relations`

### Phase 3: upgrade governance
- add projection consistency checks
- add projection completeness checks
- add QA consumability checks

### Phase 4: migrate a small sample set
- migrate a few high-frequency Method pages such as `PathMind`, `RoG`
- migrate their associated Paper pages
- validate whether QA can answer without reading `wiki/relations/`

### Phase 5: switch default QA behavior
- make governed Method/Paper pages the default serving layer
- keep `wiki/relations/` in governance and repair workflows

### Phase 6: evaluate broader adoption
- only after Method/Paper stabilizes, evaluate Concept/Task/Scenario/Benchmark serving layers

## Tradeoffs

### Benefits
- aligns human-visible pages with AI-consumable formal content
- makes QA more entity-centric and natural
- preserves strong governance by keeping the ledger authoritative
- removes unnecessary runtime dependency on `wiki/relations/` for governed QA

### Costs
- entity pages become more structured and less free-form
- governance complexity increases because projection completeness must be checked
- template discipline becomes much more important

## Recommendation

Adopt the serving-layer model for Method and Paper pages first.

Keep `wiki/relations/` as the governance truth, but make governed object pages the default runtime QA surface. Use the `Formal relations` section as the machine-readable serving projection and `intermediate/papers/` as the evidence drill-down layer.
