## Scope rules
- Review only nodes and relations touched by the current change.
- Do not restate the whole ontology.
- Structural validity is assumed to be checked by `scripts/lint_graph.py` first.
- Focus on semantic errors such as:
  - survey as task
  - framework as method
  - concept-to-paper relation placed inside concept graph
  - citation relation placed in method evolution
  - duplicate or conflicting node identity
  - relation directionality inconsistent with existing conventions
  - node granularity mismatch (e.g. framework treated as atomic concept, or scenario treated as task)
  - synonym / near-duplicate concepts that should likely merge or be distinguished explicitly

## Classification guidance
- Paper: a publication artifact
- Method: a reusable technical approach
- Concept: a stable semantic unit
- Framework: a layered or role-based organizing structure
- Task: a problem to solve, not a paper type
- Scenario: a domain or application context
- Benchmark: a dataset/evaluation target
- Evidence: a support cache, not a domain node

## Decision heuristics
- If a node mainly describes a research output form (survey / benchmark / dataset paper), prefer `research_role` or paper typing, not `Task`.
- If a node mainly organizes multiple layers, roles, or stages, prefer `Framework` / concept-level placement over `Method`.
- If a relation expresses “this paper supports / surveys / explains this concept”, prefer concept page evidence or `evidence_index.md`, not `concept_links.md`.
- If a relation expresses literature ancestry rather than actual technical lineage, prefer `citation_graph.md`, not `method_evolution.md`.
