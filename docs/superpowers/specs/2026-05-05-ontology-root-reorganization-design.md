# Ontology Root Reorganization Design

Date: 2026-05-05
Status: Proposed

## Summary

This design restructures ResearchKB from a `wiki/`-rooted knowledge layout into an `ontology/`-rooted knowledge system. The new structure makes ontology the single top-level knowledge root, promotes navigation and specification entrypoints to the root of that tree, and groups all serving-ready object domains under an explicit `entities/` layer.

The target structure is:

```text
ontology/
  index.md
  graph-standard.md
  entities/
    papers/
    methods/
    concepts/
    tasks/
    scenarios/
    benchmarks/
  relations/
```

## Goals

- Replace `wiki/` as the formal knowledge root with `ontology/`
- Promote the current navigation and specification entrypoints to:
  - `ontology/index.md`
  - `ontology/graph-standard.md`
- Add an explicit `entities/` layer for all serving-ready object domains
- Preserve the existing six object domains:
  - `papers`
  - `methods`
  - `concepts`
  - `tasks`
  - `scenarios`
  - `benchmarks`
- Preserve `relations/` as the formal relation-ledger source of truth
- Allow a staged migration with a temporary transition period

## Non-goals

This reorganization does not:

- redefine node types
- redefine relation types
- change frontmatter schema semantics
- change the serving/governance split
- change the role of `relations/` as the governance truth source
- introduce additional directory layers such as `navigation/`, `standards/`, or `governance/`

## Motivation

The current structure mixes two competing roots:

- `wiki/` acts as the physical container for all knowledge assets
- `wiki/ontology/` contains the highest-order navigation and ontology specification entrypoints

That makes the ontology layer semantically central but physically nested. The reorganization resolves this mismatch by making ontology the explicit system root.

Adding `entities/` also clarifies the distinction between:

- ontology-wide navigation/specification
- serving-ready object pages
- formal governance ledgers

This gives the repository a cleaner conceptual model without changing the underlying ontology model itself.

## Current-to-target mapping

### Entrypoints

- `wiki/ontology/index.md` → `ontology/index.md`
- `wiki/ontology/graph-standard.md` → `ontology/graph-standard.md`

### Object domains

- `wiki/papers/*` → `ontology/entities/papers/*`
- `wiki/methods/*` → `ontology/entities/methods/*`
- `wiki/concepts/*` → `ontology/entities/concepts/*`
- `wiki/tasks/*` → `ontology/entities/tasks/*`
- `wiki/scenarios/*` → `ontology/entities/scenarios/*`
- `wiki/benchmarks/*` → `ontology/entities/benchmarks/*`

### Relation ledgers

- `wiki/relations/*` → `ontology/relations/*`

## Final architecture

### 1. Root entrypoints

#### `ontology/index.md`

The single navigation entrypoint.

Responsibilities:
- route readers and agents to the right knowledge area
- explain where to start for question answering, governance, or evidence lookup
- avoid embedding detailed ontology rules

#### `ontology/graph-standard.md`

The single ontology specification authority.

Responsibilities:
- define allowed node types, relation types, controlled fields, evidence, exemptions, and ledger rules
- remain the sole normative source
- not be diluted by parallel specification documents elsewhere

### 2. Entity layer

#### `ontology/entities/*`

The serving-ready formal object layer.

Responsibilities:
- host formal object pages consumed by question answering, analysis, and survey generation
- preserve current object-domain separation
- make the object layer explicit and distinct from governance ledgers

Subdirectories:
- `ontology/entities/papers/`
- `ontology/entities/methods/`
- `ontology/entities/concepts/`
- `ontology/entities/tasks/`
- `ontology/entities/scenarios/`
- `ontology/entities/benchmarks/`

### 3. Relation layer

#### `ontology/relations/*`

The formal relation-ledger governance layer.

Responsibilities:
- remain the source of truth for formal relation instances
- support reconciliation, repair, audit, and consistency checks
- remain separate from serving-ready object pages

## Migration strategy

The migration should be executed in four phases.

### Phase 1: Physical directory migration

Create the target structure and move files into their final locations.

Scope:
- rename `wiki/` root semantics to `ontology/`
- promote `index.md` and `graph-standard.md` to the ontology root
- move six object domains under `ontology/entities/`
- move relation ledgers under `ontology/relations/`

Do not in this phase:
- redesign page content structures
- revise frontmatter models
- change relation modeling rules
- perform opportunistic architectural cleanup

Success criteria:
- the target directory structure exists
- old paths are no longer the canonical real paths
- no duplicate `ontology/ontology`-style nesting remains

### Phase 2: System-level path migration

Update all machine- and workflow-relevant references.

Priority files:
- `CLAUDE.md`
- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- ontology-governance related skill docs
- `scripts/lint_graph.py`
- any workflow, template, or automation referencing `wiki/...`

Goals:
- ingest resolves entity destinations under `ontology/entities/...`
- reconciliation resolves ledgers under `ontology/relations/...`
- projection resolves serving pages under `ontology/entities/...`
- lint and governance scripts scan the correct root layout

### Phase 3: Content-layer link and wording cleanup

Update human-facing links and displayed path language.

Scope:
- `ontology/index.md`
- object-domain index pages
- object pages
- relation pages
- displayed path labels and explanatory wording still referring to `wiki/...`

Goals:
- users entering via navigation no longer see stale `wiki/` mental models
- entity and relation layers are described consistently with the new structure

### Phase 4: Governance and regression verification

Validate that the new structure is stable.

Checks:
- run structural lint and governance checks
- verify navigation entrypoints
- verify object-page and relation-ledger cross navigation
- spot-check all six entity domains
- confirm skill docs no longer direct workflows to stale paths

## Implementation constraints

### Keep the specification authority singular

`ontology/graph-standard.md` must remain the only ontology authority. This migration changes location, not normative ownership.

### Add only one new structural layer

The reorganization adds `entities/` and stops there. Avoid introducing nested grouping beyond that layer.

### Fix executable references before polishing prose

Workflow-critical references must be updated before broad documentation cleanup.

### Allow transitional wording residue, but not transitional execution assumptions

Temporary stale prose is tolerable during migration. Core workflows relying on stale `wiki/...` paths are not.

## Risks

### 1. Workflow-document drift

The repository relies heavily on skill-driven workflows. If skills still describe `wiki/...`, future ingest, reconciliation, and projection work will continue to encode the wrong structure.

Mitigation:
- treat workflow skills as Phase 2 critical work

### 2. Script path assumptions

Lint or governance scripts may still assume `wiki/` roots.

Mitigation:
- update scripts immediately after directory migration
- do not postpone executable path fixes behind content cleanup

### 3. Content-level stale mental models

Links may continue to work after relocation while still displaying stale `wiki/...` wording.

Mitigation:
- run a dedicated Phase 3 wording and path cleanup sweep

### 4. Dual-root confusion during transition

A partial migration can leave contributors speaking in ontology terms while automation still behaves as if `wiki/` is canonical.

Mitigation:
- update `CLAUDE.md` early
- explicitly restate the new root, entity layer, and relation layer in workflow docs

## Acceptance criteria

### Structural acceptance

The repository must stabilize on:

```text
ontology/
  index.md
  graph-standard.md
  entities/
    papers/
    methods/
    concepts/
    tasks/
    scenarios/
    benchmarks/
  relations/
```

And:
- `wiki/` is no longer used as the formal knowledge root
- duplicated ontology nesting is removed
- all six object domains live under `ontology/entities/`
- all formal ledgers live under `ontology/relations/`

### Workflow acceptance

The following must align with the new structure:
- `CLAUDE.md`
- core ingest / reconciliation / projection skills
- `scripts/lint_graph.py`
- any root-level automation depending on knowledge paths

### Cognitive acceptance

The repository must present a coherent knowledge model:
- formal object pages default to `ontology/entities/*`
- formal ledgers default to `ontology/relations/*`
- the single navigation entrypoint is `ontology/index.md`
- the single specification authority is `ontology/graph-standard.md`

## Recommended execution order

1. create the target ontology tree
2. move `index.md` and `graph-standard.md`
3. move the six object domains under `ontology/entities/`
4. move `relations/`
5. update `CLAUDE.md`
6. update core workflow skills
7. update `scripts/lint_graph.py`
8. update navigation, object pages, and relation-page wording/links
9. run regression and governance verification

## Conclusion

This reorganization is justified if it is treated as a knowledge-root restructuring, not a superficial rename. The correct scope is:

- ontology becomes the single top-level knowledge root
- object domains move under `ontology/entities/`
- relation ledgers remain under `ontology/relations/`
- navigation and ontology specification entrypoints are promoted to the ontology root
- migration proceeds in stages with workflow integrity prioritized over wording cleanup

In short, ResearchKB moves from a `wiki/` container with an embedded ontology subdomain to an ontology-rooted knowledge system with explicit entity and relation layers.
