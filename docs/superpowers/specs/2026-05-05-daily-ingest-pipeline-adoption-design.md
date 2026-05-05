# Daily Ingest Pipeline Adoption Design

Date: 2026-05-05

## Summary

Adopt the validated compile pipeline as the default daily single-paper ingest workflow by updating only the minimal control-surface files:

1. `CLAUDE.md`
2. `.claude/skills/paper-ingest/SKILL.md`
3. `.claude/skills/relation-reconciliation/SKILL.md`
4. `.claude/skills/page-projection-sync/SKILL.md`
5. `wiki/ontology/graph-standard.md`
6. `scripts/lint_graph.py`

The purpose is not to introduce full harness automation or additional content migrations. The purpose is to make “处理论文” mean the complete explicit six-stage compile/governance chain by default:

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

## Problem

The compile pipeline has now been validated through:
- a standard method-paper dry-run
- a survey/framework-paper dry-run

But the default daily workflow still communicates “single-paper ingest” too narrowly. In practice, this leaves a failure mode where users or future sessions may stop after `paper-ingest`, leaving:
- formal relation ledgers incomplete
- object-page projections unsynchronized
- governance gates not yet run

This means the architecture exists, but it is not yet fully adopted as the repository’s default operational workflow.

## Goals

- Make the six-stage chain the default interpretation of daily single-paper ingest.
- Keep each stage explicit and inspectable rather than hiding the process behind black-box automation.
- Define clear stage outputs and stop conditions.
- Avoid expanding the scope into settings/hooks or unrelated content migrations.

## Non-goals

- Add automatic harness hooks.
- Change object-page content in this design pass.
- Change relation ledger content in this design pass.
- Redesign the ontology again.
- Add `wiki/ontology/index.md` changes in this minimal rollout.

## Why explicit stage progression matters

The value of the new daily workflow is not “more automation.” It is **less reliance on human memory** while preserving debugging visibility.

Without this adoption step, the repository remains vulnerable to:
- ingest finishing before ledger closure
- ledger closure happening before page projection sync
- governance being skipped or run against incomplete outputs

The repository is a governed ontology system, not a loose markdown collection. Therefore stage boundaries must remain visible even when the workflow becomes the default.

## The new default daily ingest chain

When the user says:
- 处理论文
- 摄入论文
- 落库论文
- 为某篇 PDF 建完整知识资产

that should default to the following explicit chain:

### Stage 1 — `paper-ingest`
Outputs:
- caches
- object-page candidates
- `relation_candidates`
- `relation_exemptions`
- `updated_pages`
- `warnings`

### Stage 2 — `relation-reconciliation`
Outputs:
- `already_present`
- `added_relations`
- `exemptions`
- `needs_human_review`
- `affected_pages`

### Stage 3 — `page-projection-sync`
Outputs:
- `synced_pages`
- `updated_sections`
- `manual_followups`

### Stage 4 — structural governance
- `python3 scripts/lint_graph.py`

### Stage 5 — ontology-semantic governance
- `ontology-semantic-review`

### Stage 6 — serving governance
- `serving-governance-review`

## User-visible milestones

The workflow should not dump every intermediate artifact onto the user, but it should expose clear milestones.

### After `paper-ingest`
Report:
- paper type guess
- caches generated
- relation candidate summary
- transition to relation reconciliation

### After `relation-reconciliation`
Report:
- whether ledger edges were added
- what was already present
- what was exempt
- whether any human review is needed
- transition to page projection sync

### After `page-projection-sync`
Report:
- which pages were synced
- which pages were no-op
- any manual followups
- transition to governance

### After governance
Report separately:
- structural governance result
- ontology-semantic review result
- serving-governance review result

## Required file changes

### 1. `CLAUDE.md`

Update the “处理单篇论文” workflow so it no longer frames `paper-ingest` as the whole operation. It should frame `paper-ingest` as the compile entrypoint of the full chain.

Also update the batch-paper section so “batch ingest” means repeating the full per-paper chain, not just invoking `paper-ingest` repeatedly without downstream closure.

### 2. `.claude/skills/paper-ingest/SKILL.md`

The skill should no longer end conceptually at “ingest complete.” It should explicitly hand off to `relation-reconciliation` and make clear that formal graph closure is not finished at the end of ingest.

### 3. `.claude/skills/relation-reconciliation/SKILL.md`

The skill should explicitly identify itself as the mandatory next stage after `paper-ingest`, and should explicitly hand off `affected_pages` to `page-projection-sync`.

### 4. `.claude/skills/page-projection-sync/SKILL.md`

The skill should explicitly identify itself as the third stage after reconciliation and clearly direct the workflow into the three governance gates once sync is complete.

### 5. `wiki/ontology/graph-standard.md`

Add a small normative section describing the single-paper compile chain so the architecture is not only documented in operational guidance, but also recognized at the ontology/process standard layer.

### 6. `scripts/lint_graph.py`

Add minimal contract checks so regressions are detected if any of the three core skill files stop mentioning the expected pipeline contract markers.

## Explicit stop conditions

Even though this becomes the default workflow, it is not unconditional.

The chain should allow interruption when:

1. `paper-ingest` returns `needs-skill-update`
2. `relation-reconciliation` returns substantial `needs_human_review`
3. `page-projection-sync` returns substantial `manual_followups`
4. any governance gate fails

This keeps the pipeline safe, observable, and debuggable.

## Why this scope is intentionally minimal

This design does **not** change:
- `wiki/ontology/index.md`
- existing object-page content
- relation ledger content
- harness settings or hooks

Those can come later. The immediate need is to align the repository’s default operational story with the compile chain that has now been proven to work.

## Success criteria

After this adoption pass:

1. “处理论文” means the full six-stage chain by default in project instructions and skills.
2. `paper-ingest` is clearly framed as an entrypoint, not the end of the workflow.
3. stage-to-stage handoff is explicit in the skill docs.
4. the workflow is defaulted, but not black-boxed.
5. lint protects the pipeline contract against silent regression.

## Recommendation

Proceed with this six-file minimal adoption pass.

It is the smallest change set that turns the compile pipeline from an experimentally validated architecture into the repository’s actual day-to-day ingest workflow.
