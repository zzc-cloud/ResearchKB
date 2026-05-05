# Survey Serving Template Gap Fix Design

Date: 2026-05-03

## Summary

Fix the survey/framework/template gap exposed by the second dry-run of the new compile pipeline. The problem is not that `paper-ingest` or `relation-reconciliation` failed. The problem is that survey-mainline pages are still largely reading pages rather than serving-ready pages, so `page-projection-sync` lacks a sufficiently explicit target shape.

This design focuses on four aligned template branches within the current ontology:

1. survey paper template
2. framework-flavored concept template
3. scenario template for survey-driven domains
4. task template for survey-driven domains

The immediate goal is to make the second dry-run capable of reaching `pipeline-ran-end-to-end` rather than stopping at `pipeline-ran-with-manual-bridges`.

## Problem

The second dry-run on:
- `A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf`

showed that:
- `paper-ingest` could emit `relation_candidates`
- `relation-reconciliation` could preserve exemptions and reconcile formal ledger state
- but `page-projection-sync` had no strong serving-ready page templates for the survey mainline pages it needed to update

The gap is therefore not at extraction or formal-ledger closure. It is at the page-template and projection layer.

## Correct ontology distinction

A key clarification:
- **survey** is a Paper-level research role or paper type
- **framework** is a knowledge product / semantic object type

These are not the same level.

Therefore the right design is not a single “survey/framework page type.” Instead:
- survey remains a Paper-level variant
- framework remains a Concept-level variant
- scenario and task templates must be tuned to consume framework-led survey outputs

## Goals

- Define a dedicated serving template for survey papers.
- Define a dedicated serving template for framework-flavored concept pages.
- Define scenario and task serving templates that work in survey/framework mainlines.
- Keep framework within the current Concept node type rather than introducing a new top-level node type.
- Make `page-projection-sync` capable of recognizing and synchronizing these variants.

## Non-goals

- Introduce a brand-new `Framework` node type.
- Rewrite all survey pages in the repository.
- Expand this fix to unrelated topic lines.
- Turn `page-projection-sync` into a general prose rewriter.

## Root cause

The current survey-mainline pages are mostly readable and semantically useful, but they are missing a sufficiently explicit projection target for serving sync:
- no stable `Formal relations` contract in some pages
- no variant-specific human-readable section expectations
- no formal distinction between general concept pages and framework-type concept pages

As a result, `page-projection-sync` can identify affected pages but cannot fully and confidently synchronize them.

## Proposed fix

### 1. Survey paper template

Applies to:
- `wiki/papers/`
- `research_role: survey`

Purpose:
- represent the survey as a paper-node serving surface
- treat framework / taxonomy / landscape content as the paper’s semantic outputs, not as methods

**Human-readable sections should emphasize:**
- 核心问题
- 主要贡献
- 核心框架 / 核心概念
- 相关任务
- 应用场景
- 关键结论
- 引用了哪些重要工作
- 与知识库其他内容的关联
- 综述证据来源

**Formal relations should emphasize:**
- `proposes` to framework/concept nodes
- `uses_concept`
- `targets_task`
- `cites`
- `supported_by`
- explicit omission of `evaluated_on` when exempt

### 2. Framework-flavored concept template

Applies to:
- Concept nodes
- recommended marker: `concept_kind: framework`

This avoids introducing a new top-level node type while still giving framework concepts their own template behavior.

**Human-readable sections should emphasize:**
- 框架定义
- 层级结构 / 组成部分
- 核心内涵
- 相关概念
- 相关场景
- 相关任务
- 相关论文
- 证据来源

**Formal relations should emphasize:**
- incoming `proposes`
- outgoing `uses_concept`
- outgoing `applies_to`
- outgoing/incoming `supports`
- `supported_by`

### 3. Scenario template for survey/framework mainlines

Applies to:
- scenario pages that are fed primarily by framework/survey outputs

**Human-readable sections should emphasize:**
- 场景描述
- 核心挑战
- 使用的主要框架 / 概念 / 方法
- 相关任务
- 相关论文
- 证据来源
- 开放问题

**Formal relations should emphasize:**
- incoming `applies_to`
- incoming `supports`
- optional `supported_by`

### 4. Task template for survey/framework mainlines

Applies to:
- task pages whose main upstream content is survey/framework-driven rather than method-benchmark-driven

**Human-readable sections should emphasize:**
- 任务定义
- 核心挑战
- 相关框架 / 概念
- 相关场景
- 相关论文
- 证据来源 / 关系索引

**Formal relations should emphasize:**
- incoming `targets_task`
- incoming `supports`
- optional `supported_by`

## Why not introduce a `Framework` node type now

Although framework and survey are not the same layer, the current ontology can still model framework cleanly without a new top-level node type.

The lower-risk approach is:
- keep node type = `Concept`
- add / standardize `concept_kind: framework`
- branch template, serving, and sync behavior based on that marker

This preserves ontology stability while fixing the real serving problem.

## Required changes

### A. `wiki/ontology/graph-standard.md`
Add or revise:
- survey paper template branch
- framework-concept template branch
- survey-driven scenario/task template branches
- guidance that `concept_kind: framework` is the preferred marker

### B. `page-projection-sync`
Enhance variant handling so the skill can tell the difference between:
- general concept pages
- framework concept pages
- survey paper pages
- standard task/scenario pages vs survey-driven task/scenario pages

### C. Representative pages to update
This fix should be grounded in the current survey mainline:
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- `wiki/scenarios/复杂产品设计.md`
- `wiki/tasks/engineering-design-knowledge-management.md`

## Success criteria

After this fix:
- `page-projection-sync` has explicit target shapes for the survey/framework mainline
- the five representative pages above can be synchronized without manual ambiguity
- the survey dry-run should be able to advance from `pipeline-ran-with-manual-bridges` to `pipeline-ran-end-to-end`
- no new ontology type is required to achieve this

## Recommendation

Proceed with a focused template-gap fix rather than redesigning the overall pipeline again.

The pipeline already proved that ingest and reconciliation are viable. The remaining blocker is that survey-mainline pages do not yet expose a strong enough serving-ready target for projection sync. Fixing that template layer is the smallest, highest-value step.
