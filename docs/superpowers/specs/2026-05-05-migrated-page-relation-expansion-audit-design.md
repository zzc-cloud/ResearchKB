# Migrated Page Relation Expansion Audit Design

Date: 2026-05-05

## Summary

Audit only serving-ready or otherwise migrated pages to determine whether links appearing in human-friendly relation blocks should:

1. remain as already-formalized neighbors
2. be promoted into additional `Formal relations` / relation-ledger entries
3. be downgraded to context-only, non-formal navigation references

The purpose is to answer a structural question before changing link policy:

> Is the current `Formal relations` surface too narrow, or are human-friendly blocks over-linking beyond the formal graph?

## Problem

Obsidian graph inflation currently comes from human-friendly relation blocks using `[[wikilink]]` for both:
- true formal neighbors
- non-formal reading/navigation/context neighbors

Before tightening or removing those links, we must first determine which of them actually deserve formalization. Otherwise we risk deleting links that should instead become explicit formal graph edges.

## Scope

This audit applies **only** to pages that are already serving-ready or have already been migrated to the serving-layer model.

It explicitly excludes:
- untouched legacy pages
- raw PDFs
- unrelated topic lines not yet in the serving migration set

## Goals

- Audit migrated pages page-by-page.
- Compare three surfaces for each page:
  1. human-friendly relation blocks
  2. `Formal relations`
  3. current `wiki/relations/*.md` formal ledgers
- Classify each human-friendly `[[link]]` into one of three categories:
  - `already-formalized`
  - `should-be-formalized`
  - `context-only`
- Produce both a page-by-page view and a relation-type summary view.

## Non-goals

- Change link policy yet.
- Rewrite pages yet.
- Add or remove formal relations yet.
- Audit unmigrated legacy pages.

## Why this audit must happen first

There are two possible explanations for graph inflation:

1. the human-friendly blocks are over-linking beyond the intended formal graph
2. the current formal graph is too narrow and should include more relation types or more edges

Without an audit, any “fix” is premature. Tightening links too early could erase relationships that actually deserve formalization.

## Audit inputs per page

Each migrated page is evaluated against three sources:

### 1. Human-friendly relation blocks
Examples:
- related methods
- related tasks
- related concepts
- related scenarios
- representative papers
- evidence sources
- background routes

### 2. `Formal relations`
The page’s normalized `## Formal relations` block.

### 3. Current formal ledgers
Relevant files in `wiki/relations/*.md`.

## Classification rules

For each human-friendly `[[wikilink]]`, classify using the following rules.

### A. `already-formalized`
A link is `already-formalized` only if all are true:
- the page’s `Formal relations` contains the matching one-hop neighbor
- the formal relation ledger contains the corresponding formal edge
- the relation type is clear

### B. `should-be-formalized`
A link is `should-be-formalized` only if all are true:
- the human-friendly block expresses a relationship that the ontology can legally model
- current evidence is sufficient to support formalization
  - evidence cache exists, or
  - the page contains a sufficiently explicit minimum relation statement
- the edge is currently missing from `Formal relations` and/or the formal ledger

### C. `context-only`
A link is `context-only` if any of the following holds:
- it is primarily background, route context, comparison, or further reading
- there is no appropriate formal relation type in the ontology
- evidence is insufficient
- even if relevant, it should not be treated as a one-hop formal neighbor

## Output format

The audit should produce two views.

### 1. Page-by-page audit cards
For each page:
- page path
- human-friendly links examined
- `already-formalized`
- `should-be-formalized`
- `context-only`
- short conclusion

### 2. Relation-type summary
Aggregate all `should-be-formalized` findings by relation type, such as:
- `uses_concept`
- `targets_task`
- `applies_to`
- `supports`
- `cites`
- `supported_by`

This lets the repository decide whether the current formal graph is systematically too narrow in specific categories.

## Initial audit scope

### PathMind / high-frequency migrated set
- `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- `wiki/methods/PathMind.md`
- `wiki/concepts/路径优先化.md`
- `wiki/concepts/重要推理路径.md`
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/benchmarks/WebQSP.md`
- `wiki/benchmarks/CWQ.md`

### Survey / framework migrated set
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- `wiki/scenarios/复杂产品设计.md`
- `wiki/tasks/engineering-design-knowledge-management.md`

## Known expected patterns

### Likely `context-only`
Examples like:
- `PathMind`
- `RoG`
- `GCR`
- `ToG`
inside broad “相关方法 / 路线” blocks on concept pages where no one-hop formal relation exists.

### Likely `already-formalized`
Examples like:
- survey paper → framework concept (`proposes`)
- survey paper → concept (`uses_concept`)
- survey paper → task (`targets_task`)
- framework concept → scenario (`applies_to`)

These should already map cleanly to the formal graph.

## Success criteria

This audit is successful if it produces:

1. a reliable page-by-page classification for all migrated pages in scope
2. a relation-type summary of all `should-be-formalized` findings
3. a clear answer to whether formal graph coverage is too narrow in specific categories
4. a clean separation between links that should become formal and links that should be downgraded to context-only

## Recommendation

Perform this audit before changing link policy or pruning wikilinks.

Only after the audit should the repository decide whether to:
- expand `Formal relations`
- add new formal relation instances
- or demote certain human-friendly links into plain-text context links

This sequencing minimizes the risk of deleting links that should have been formalized instead.
