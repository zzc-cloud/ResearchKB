# Relax CLAUDE relation-ledger lint design

## Goal
Adjust `scripts/lint_graph.py` so `CLAUDE.md` is checked only for workflow-level guidance into ontology and relation surfaces, while `wiki/ontology/graph-standard.md` remains the single authoritative place that defines which relation type is maintained in which relation ledger file.

## Why this change
The current lint treats `CLAUDE.md` as if it must enumerate specific relation-ledger filenames such as `task_method_map.md` and `evidence_index.md`. That is too rigid. `CLAUDE.md` is a workflow and execution guide, not the canonical registry of relation-ledger ownership. The ownership mapping already belongs in `wiki/ontology/graph-standard.md`.

## Scope
Included:
- Modify `scripts/lint_graph.py`
- Relax the `CLAUDE.md` lint from specific ledger filenames to workflow-level entry points
- Keep `graph-standard.md` checks and relation-ledger content checks intact

Excluded:
- No edits to `CLAUDE.md`
- No edits to `wiki/ontology/graph-standard.md`
- No changes to relation-ledger files under `wiki/relations/`
- No changes to non-CLAUDE lint assertions

## Terminology
For this change, “relation-ledger ownership” means the mapping from a relation type to the formal `wiki/relations/*.md` file that maintains its instance edges.

Examples:
- `cites` → `wiki/relations/citation_graph.md`
- `targets_task` → `wiki/relations/task_method_map.md`
- `proposes` → `wiki/relations/paper_method_links.md`

That mapping should be defined in `wiki/ontology/graph-standard.md`, not duplicated in `CLAUDE.md`.

## Proposed design

### 1. Narrow the responsibility of `CLAUDE.md` lint
Replace the current `CLAUDE_NEEDLES` expectations so they no longer require concrete ledger filenames like `task_method_map.md` or `evidence_index.md`.

After the change, the `CLAUDE.md` lint should only ensure that the workflow guide still points readers toward:
- the ontology authority surface (`wiki/ontology/`)
- the relation-ledger layer (`wiki/relations/` or equivalent repo-level wording)
- the lint command (`python3 scripts/lint_graph.py`)

This preserves the requirement that `CLAUDE.md` remain operationally useful without forcing it to mirror the ledger registry.

### 2. Keep ledger ownership validation in `graph-standard.md`
Do not relax `GRAPH_STANDARD_NEEDLES`.

The lint should continue to require that `wiki/ontology/graph-standard.md` explicitly documents which ledger files own `proposes`, `evaluated_on`, `supported_by`, and `sourced_from`, along with the other ontology-level invariants already enforced there.

This keeps the canonical ownership mapping in one place.

### 3. Keep instance-edge and ledger-file checks unchanged
Do not change:
- `RELATION_LEDGER_NEEDLES`
- the `sourced_from` placement check
- repository index checks
- evidence cache checks

The goal is only to remove duplicated ownership requirements from the `CLAUDE.md` lint, not to weaken graph-governance validation.

## File-level changes
- Modify: `scripts/lint_graph.py`

## Verification
1. Run `python3 scripts/lint_graph.py`
2. Confirm it no longer fails solely because `CLAUDE.md` omits specific ledger filenames
3. Confirm it still fails if ownership entries are removed from `wiki/ontology/graph-standard.md`

## Risks
- If the `CLAUDE.md` check becomes too loose, the workflow guide could drift and stop pointing users to the relation layer at all
- If the `graph-standard.md` checks were accidentally loosened at the same time, ownership rules could become underspecified

This design avoids both risks by relaxing only the `CLAUDE.md` side and leaving the ontology authority checks untouched.

## Success criteria
- `CLAUDE.md` no longer needs to enumerate specific ledger filenames to satisfy lint
- `graph-standard.md` remains the single authoritative registry of relation-ledger ownership
- Existing relation-ledger and instance-edge validations continue to run unchanged
