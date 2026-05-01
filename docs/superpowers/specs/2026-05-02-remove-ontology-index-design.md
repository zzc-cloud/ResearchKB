# Remove ontology index landing page design

## Goal
Delete `wiki/ontology/index.md` and fold its lightweight navigation role into `wiki/ontology/graph-standard.md`, while preserving ontology discoverability from the main wiki index.

## Why this change
`wiki/ontology/index.md` currently acts only as a shallow navigation hub. The actual authority for ontology rules already lives in `wiki/ontology/graph-standard.md`, and the formal relation ledgers already live in `wiki/relations/`. Keeping a separate ontology landing page adds one more entry point without adding distinct semantics.

## Scope
This change is intentionally narrow.

Included:
- Delete `wiki/ontology/index.md`
- Replace all `[[ontology/index|ontology]]` links in `wiki/index.md` with `[[graph-standard|ontology]]`
- Add a short navigation block near the top of `wiki/ontology/graph-standard.md` that points to the formal relation ledgers
- Verify no remaining runtime documentation paths depend on `wiki/ontology/index.md`
- Run `python3 scripts/lint_graph.py`

Excluded:
- No restructuring of ontology rules
- No changes to relation semantics or ledger formats
- No broader rewrite of `wiki/index.md`
- No compatibility redirect page

## Proposed design

### 1. Single ontology authority entry point
After this change, `wiki/ontology/graph-standard.md` will serve both as:
- the normative ontology specification
- the user-facing ontology entry point

This keeps authority and discovery aligned in one place.

### 2. Main index link consolidation
In `wiki/index.md`, every ontology entry currently pointing to `[[ontology/index|ontology]]` will instead point directly to `[[graph-standard|ontology]]`.

This preserves the existing user-facing label `ontology` while removing the extra hop.

### 3. Lightweight navigation at the top of graph-standard
A short block will be added near the top of `wiki/ontology/graph-standard.md` to link the reader to the key formal relation ledgers:
- `[[task_method_map]]`
- `[[evidence_index]]`
- `[[citation_graph]]`
- `[[method_evolution]]`
- `[[concept_links]]`

This is intentionally brief. It should restore the useful “hub” behavior from the deleted page without duplicating ontology content.

## File-level changes
- Delete: `wiki/ontology/index.md`
- Modify: `wiki/index.md`
- Modify: `wiki/ontology/graph-standard.md`

## Verification
1. Search for remaining references to `wiki/ontology/index.md` and `[[ontology/index|ontology]]`
2. Confirm ontology links in `wiki/index.md` now point to `[[graph-standard|ontology]]`
3. Run `python3 scripts/lint_graph.py`

## Risks
- Historical planning docs may still mention `wiki/ontology/index.md`
- If any future navigation assumes a dedicated ontology landing page, it will now need to use `graph-standard` directly

These are acceptable because the change deliberately removes the separate landing page abstraction.

## Success criteria
- `wiki/ontology/index.md` is gone
- Main wiki navigation still exposes ontology clearly
- `graph-standard.md` remains the single authoritative ontology page
- Lint passes after the change
