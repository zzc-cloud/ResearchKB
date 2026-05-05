# PathMind Compile Pipeline Dry-Run Design

Date: 2026-05-03

## Summary

Run the newly designed three-skill knowledge compile pipeline end-to-end against one real, already-ingested standard method paper:

- input PDF: `raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`
- existing object/evidence/relation graph: PathMind mainline

The purpose is not to re-invent PathMind content. The purpose is to verify that the new compile chain can execute in a real repository with existing data, produce consumable outputs at each stage, and hand those outputs cleanly into the three governance gates.

## Pipeline under test

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

## Problem

The three-skill pipeline has been designed, but it has not yet been validated as a real integrated flow. ResearchKB already contains rich PathMind-related content, so the true risk is not “can the skills run in isolation?” but rather:

- can `paper-ingest` emit structured relation candidates in a real run?
- can `relation-reconciliation` consume those outputs without re-inferring everything from prose?
- can `page-projection-sync` update real pages in a bounded way?
- can the resulting outputs survive structural, ontology-semantic, and serving governance?

Until that is proven on a real paper with real preexisting graph state, the pipeline remains architectural theory rather than operational workflow.

## Why PathMind is the right dry-run target

PathMind is the best validation case because the repository already contains:
- the raw PDF
- `sections.md`, `refs.md`, `experiments.md`, and `full.md`
- Paper / Method / Concept / Task / Scenario / Benchmark / Evidence pages
- several relation-ledger categories
- serving-ready migrations and downstream graph context

This makes PathMind a high-context, dependency-rich example that is more likely to surface integration weaknesses than a blank-slate ingest would.

## Goals

- Validate that the three-skill compile chain can run in sequence on a real method-paper example.
- Allow real repository updates where the pipeline requires them, but keep the scope tightly bounded to PathMind-related outputs.
- Determine whether each stage produces outputs that the next stage can directly consume.
- Verify the end result against structural, ontology-semantic, and serving governance.
- Use the dry-run to identify which stage still needs interface or behavior refinement.

## Non-goals

- Rebuild all PathMind content from scratch.
- Expand unrelated knowledge lines while testing the pipeline.
- Do opportunistic cleanup outside the PathMind slice.
- Redesign the overall architecture again during this run.

## Allowed write scope

This dry-run may update:
- PathMind-adjacent relation ledgers
- PathMind object-page `Formal relations`
- strong-consistency frontmatter fields affected by ledger changes
- templated human-readable relation blocks on affected PathMind pages

This dry-run should not opportunistically update unrelated topics or perform broad prose rewrites.

## Core validation checkpoints

The dry-run is only considered meaningful if all six checkpoints are inspected.

### 1. `paper-ingest` output checkpoint

Must verify that the real run emits:
- `relation_candidates`
- `relation_exemptions`
- `updated_pages`
- `warnings`

If the skill still only mutates pages/relations without explicit structured relation output, the pipeline is not truly integrated.

### 2. `relation-reconciliation` consumption checkpoint

Must verify that it can consume the ingest output and emit:
- `already_present`
- `added_relations`
- `exemptions`
- `needs_human_review`
- `affected_pages`

If it still requires heavy manual interpretation of ingest artifacts, its interface is not mature enough.

### 3. `page-projection-sync` consumption checkpoint

Must verify that it can take:
- updated ledgers
- affected pages

and produce synchronized:
- `Formal relations`
- strong-consistency frontmatter
- templated human-readable relation sections

without wandering into unrelated editorial prose.

### 4. Structural checkpoint

`python3 scripts/lint_graph.py` must pass after the compile chain finishes.

### 5. Ontology-semantic checkpoint

`ontology-semantic-review` must be able to assess the result without needing to reinterpret the entire pipeline manually.

### 6. Serving-governance checkpoint

`serving-governance-review` must confirm that the updated PathMind-related pages remain or become valid serving surfaces.

## Success criteria

### Minimum success
- all three skills execute in order
- each stage emits explicit output
- lint passes

### Real success
- each stage’s output is directly usable by the next stage
- governance layers can evaluate the results without ad hoc reinterpretation
- only bounded, expected PathMind-adjacent files are touched
- no large manual patching is required between stages

If heavy human mediation is required to bridge stage boundaries, the pipeline is not yet truly “running end-to-end.”

## Failure interpretation

The dry-run should be read diagnostically.

### If failure occurs at `paper-ingest`
The output contract is not sufficiently explicit.

### If failure occurs at `relation-reconciliation`
The candidate schema or ledger diff rules are underspecified.

### If failure occurs at `page-projection-sync`
The affected-page contract or projection rules are underspecified.

### If failure occurs at governance
The compile chain may be producing outputs, but not semantically or serving-stably enough.

## Recommended execution discipline

- Treat this as an architecture-debugging run, not a content-authoring pass.
- Log what each stage received and emitted.
- Keep write scope narrow and intentional.
- Do not “fix around” interface problems silently; record where the contract broke.

## Recommendation

Proceed with a real PathMind dry-run in the current repository.

This is the smallest realistic integrated test of the new compile pipeline, and it should reveal whether the design has genuinely become operational or still requires additional contract refinement between stages.
