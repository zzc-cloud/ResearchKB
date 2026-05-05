# Serving Compatibility Cleanup Design

Date: 2026-05-04

## Summary

Clean up the compatibility residue left behind after the serving-layer migration and dry-runs by updating `scripts/lint_graph.py` to expect the new serving section names and removing duplicate compatibility-only sections from migrated pages.

This is not a content redesign. It is a convergence pass that realigns:
- serving-ready page templates
- lint expectations
- actual page headings

The goal is to eliminate duplicated blocks that exist only to satisfy outdated lint expectations while preserving formal relations, ontology semantics, and serving behavior.

## Problem

Several migrated pages currently contain duplicate or overlapping sections such as:
- `关系索引与证据` and `证据来源`
- `相关场景与任务` and `相关任务 / 场景`
- `相关方法 / 框架` and `相关框架 / 概念`
- `证据索引` and `证据来源`
- `实验证据 / 综述证据` and `证据来源`

These are not conceptual errors. They are compatibility artifacts.

The root cause is that page content has already moved toward the newer serving template names, while `scripts/lint_graph.py` still hard-checks several legacy section headings. As a result, migrated pages keep both the new serving sections and the old compatibility headings at the same time.

## Goals

- Make the new serving section names the single canonical expectation.
- Update `scripts/lint_graph.py` so it no longer requires legacy compatibility headings.
- Remove duplicate compatibility-only sections from already migrated pages.
- Preserve all formal relation content, ontology meaning, and serving readiness.

## Non-goals

- Redesign page semantics.
- Change formal relation ledgers.
- Rewrite interpretive prose.
- Expand serving migration to new pages.

## Root cause

The problem is not that the pages are wrong. The problem is that the lint contract and the page templates are out of sync.

### Current state
- pages have been migrated toward new serving-friendly headings
- lint still expects several old headings
- pages therefore keep both forms to stay green

### Consequence
- duplicate sections
- noisier pages
- reduced readability
- harder maintenance

## Cleanup principle

This cleanup should operate under two rules:

1. **Fix the source of the duplication first**
   - update lint expectations to the new canonical serving headings

2. **Then remove only the compatibility residue**
   - do not alter actual knowledge content
   - do not touch formal relations unless a heading move requires it

## Canonical heading direction

The following heading directions should become canonical.

### Concept pages
- canonical: `证据来源`
- remove compatibility-only: `关系索引与证据`

### Task pages
- canonical for survey-driven tasks: `相关框架 / 概念`
- canonical for method-driven tasks: `相关方法`
- canonical evidence/index block: `证据来源 / 关系索引`
- remove compatibility-only: `关系索引`

### Scenario pages
- canonical: `相关任务`
- canonical: `使用的主要方法 / 框架 / 概念` when the page is survey/framework-driven
- remove compatibility-only: `关联任务`

### Benchmark pages
- canonical: `证据来源`
- remove compatibility-only: `证据索引`

### Survey paper pages
- canonical readable evidence blocks: `综述证据来源` plus `证据来源` only if the repository still needs one generic cross-type block
- remove compatibility-only: `实验证据 / 综述证据`

## Scope of page cleanup

This pass should clean only pages that have already been migrated and currently carry compatibility residue.

### PathMind / high-frequency set
- `wiki/concepts/路径优先化.md`
- `wiki/concepts/重要推理路径.md`
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/benchmarks/WebQSP.md`
- `wiki/benchmarks/CWQ.md`

### Survey mainline set
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- `wiki/scenarios/复杂产品设计.md`
- `wiki/tasks/engineering-design-knowledge-management.md`

## Lint update requirements

`script/lint_graph.py` should be updated so that:

- migrated serving pages are checked against the new canonical headings
- legacy compatibility headings are no longer required
- page-type expectations reflect current serving variants rather than older transitional names

The lint update must happen before compatibility-only sections are removed from the pages.

## Page cleanup rules

When removing duplicates:
- keep the newer serving heading
- keep all meaningful content
- merge useful bullets if needed
- remove only the redundant compatibility-only wrapper

Do not:
- rewrite explanatory prose
- change formal relation semantics
- rename nodes
- add unrelated content

## Success criteria

After this cleanup:

1. `scripts/lint_graph.py` no longer depends on legacy section names.
2. migrated pages no longer retain duplicate compatibility-only sections.
3. page readability improves without changing formal knowledge content.
4. lint still passes.
5. ontology-semantic-review and serving-governance-review remain stable or improve.

## Recommendation

Proceed with a synchronized cleanup: update lint expectations and page headings together.

Doing only one side would either keep the page duplication in place or break the build. The correct fix is to realign the contract and the content at the same time.
