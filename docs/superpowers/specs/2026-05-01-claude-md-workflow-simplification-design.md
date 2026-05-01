# ResearchKB CLAUDE.md workflow simplification design

- Date: 2026-05-01
- Topic: Simplify `CLAUDE.md` by moving normative schema details out of it

## Goal

Turn `CLAUDE.md` into a project handbook that focuses on role, workflow entrypoints, and repository-specific constraints, while moving normative graph/schema details to `wiki/ontology/graph-standard.md`.

## Problem

The current `CLAUDE.md` mixes three layers:

1. project-level policy and operating boundaries
2. execution flow already embodied in skills
3. ontology and schema rules that belong in a canonical graph standard

This creates duplicate maintenance surfaces. In particular, the repeated frontmatter guidance, controlled vocabulary, and node-template requirements overlap with what should be centrally governed by `wiki/ontology/graph-standard.md`.

## Chosen approach

Use an entrypoint-and-principles `CLAUDE.md`, with schema authority concentrated in `wiki/ontology/graph-standard.md`.

### What stays in `CLAUDE.md`

- Role definition and project mission
- Repository structure overview
- High-level page family descriptions
- User intent to workflow mapping
- Explicit skill routing, including naming `paper-ingest`
- Project constraints and execution boundaries
- Priority of `wiki/ontology/graph-standard.md`
- Read/write boundaries such as `raw/` being read-only
- Repository-specific expectations around incremental updates, relations, and evidence usage
- Short template skeletons only where they help orientation

### What moves conceptually to `wiki/ontology/graph-standard.md`

- Controlled frontmatter fields and allowed values
- Node-type-specific frontmatter requirements
- Minimum linking obligations
- Evidence binding rules
- Canonical relation expectations
- Other normative graph-structure rules that should have a single source of truth

### What is removed from `CLAUDE.md`

- Step-by-step ingest instructions
- Detailed cache template breakdowns
- Repeated procedural descriptions for paper, method, concept, task, scenario, and relation updates
- Large blocks of frontmatter recommendations that duplicate graph/schema policy
- Long lint and review checklists that belong in skills or canonical standards

## Alternatives considered

### Option 1 — Entrypoint only, with schema authority centralized
Recommended and chosen.

Pros:
- Minimizes duplication with skills and standards
- Makes `CLAUDE.md` more stable over time
- Keeps project policy separate from execution mechanics
- Keeps ontology rules in one canonical place

Cons:
- Less self-contained for a first-time reader

### Option 2 — Keep detailed template guidance in `CLAUDE.md`
Pros:
- Easier to scan in one file

Cons:
- Continues double maintenance
- Increases drift risk between handbook and standard

### Option 3 — Move everything to `graph-standard.md`
Pros:
- Maximum consolidation

Cons:
- Blurs the distinction between project handbook and ontology standard
- Makes `graph-standard.md` carry non-normative operational guidance

## Resulting structure

The simplified `CLAUDE.md` should contain:

1. role and mission
2. repository map
3. brief page-family guidance
4. concise relation-index overview
5. workflow entrypoints
6. execution principles

Template sections for papers, methods, concepts, and scenarios should be reduced to:
- a short explanation of purpose
- a compact skeleton example if useful
- an explicit statement that frontmatter fields, allowed values, and linking obligations are governed by `wiki/ontology/graph-standard.md`

The canonical `wiki/ontology/graph-standard.md` should be treated as the home for:
- node types
- relation types
- node judgment rules
- exemptions by paper type
- minimum linking obligations
- link quality rules
- evidence rules

## Scope

This change is intentionally documentation-only.

It does not:
- modify any skill
- change the ontology semantics themselves
- change linting behavior
- change file layout in `wiki/` or `intermediate/`

## Validation criteria

The rewrite is successful if:
- `CLAUDE.md` no longer duplicates the ingest skill’s internal steps
- `CLAUDE.md` no longer carries large normative frontmatter blocks that should live in the graph standard
- the document still clearly routes common user intents
- project-specific constraints remain explicit
- `wiki/ontology/graph-standard.md` remains the authoritative normative source

## Notes from self-review

- No placeholders remain.
- The scope is constrained to a documentation rewrite.
- The chosen structure cleanly separates handbook responsibilities from graph-standard responsibilities.
