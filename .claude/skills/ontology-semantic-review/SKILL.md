---
name: ontology-semantic-review
description: Review newly ingested or recently modified ResearchKB knowledge-graph content for semantic correctness after paper-ingest and after scripts/lint_graph.py passes. Use this whenever the user asks to review whether newly added papers, concepts, frameworks, tasks, scenarios, or relations are placed correctly in the ontology, whether a git diff introduced bad entity classifications or bad relation placement, or whether an ingest result is semantically reasonable even though the structure is valid. This skill is for post-ingest ontology/knowledge-graph governance, not for PDF extraction or basic linting.
---

# Ontology Semantic Review

## Purpose
Use this skill after `paper-ingest` and after `python3 scripts/lint_graph.py` passes. Your job is to review semantic correctness, not structural existence.

## Read first
- `wiki/ontology/graph-standard.md`
- `wiki/relations/citation_graph.md`
- `wiki/relations/method_evolution.md`
- `wiki/relations/concept_links.md`
- `wiki/relations/task_method_map.md`
- `wiki/relations/evidence_index.md`
- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`

## Inputs
Review using:
1. the current git diff or modified file list
2. the ontology and relation files above
3. the specific changed wiki/intermediate pages

## Review focus
Check:
- entity classification correctness
- relation placement correctness
- ontology position correctness
- consistency with existing graph
- duplicate / conflicting / pseudo-relations
- relation directionality and granularity mismatch when relevant

## Judgment guidance
- Prefer the smallest semantic correction that restores ontology consistency.
- Distinguish paper support relations from ontology-level concept relations.
- Use the report rubric in `references/review-output-template.md`; do not invent ad-hoc verdict meanings.

## Output
Do not rewrite the ontology yourself. Output a structured review report with the exact template in `references/review-output-template.md`.
