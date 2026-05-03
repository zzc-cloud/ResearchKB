# KG Reasoning High-Frequency Serving Batch Design

Date: 2026-05-03

## Summary

Define the next serving-layer migration subproject as a high-frequency batch for the KG reasoning mainline. Rather than broadening framework design again, this batch focuses on the most frequently referenced next-hop nodes that already appear in the existing serving-ready PathMind-centered graph.

Scope for this batch:

- Methods: `GCR`, `EPERM`, `ToG`
- Papers:
  - `Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models`
  - `An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering`
  - `Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation`
- Tasks: `kgqa`, `multi-hop-qa`
- Benchmark: `CWQ`
- Concept: `重要推理路径`

The purpose is to improve actual runtime QA coverage by turning the most likely next-hop pages into serving-ready pages, not to re-plan full-repository rollout.

## Problem

The serving framework is now broader, and a representative multi-type batch has reached serving-ready status. However, runtime QA along the KG reasoning mainline still frequently encounters high-value adjacent pages that remain legacy or only partially governed as serving surfaces.

This creates a practical gap:
- the serving architecture exists
- the representative batch proves the model works
- but the next most commonly traversed nodes are still not reliably serving-ready

The next step should therefore optimize coverage where it matters most: the highest-frequency next-hop nodes in the active KG reasoning graph.

## Goals

- Define a tightly scoped high-frequency migration batch.
- Prioritize nodes by real QA traversal value rather than directory order.
- Improve local serving-graph continuity around the existing PathMind-centered mainline.
- Require the same three governance gates for the whole batch.
- Keep scope small enough for one concrete implementation plan.

## Non-goals

- Re-specify the full serving architecture for all node types.
- Migrate all remaining nodes in the repository.
- Expand into unrelated thematic lines such as complex-product-design or other sparse survey branches.
- Change the previously defined three-layer governance model.

## Why this batch exists

This batch is the bridge between:
1. framework establishment
2. actual runtime coverage improvement

The point is not to prove the serving model again. The point is to make the default QA graph more connected for the most common KG reasoning questions.

## Batch selection rules

A node belongs in the high-frequency batch when it satisfies one or more of these:

### 1. Repeatedly linked from already serving-ready pages

If a node already appears in formal relations or human-readable sections on serving-ready pages, it is a likely runtime next-hop and should be migrated early.

### 2. It closes a reading-layer / formal-layer gap

If a page is already mentioned in human-readable sections but its own page is not yet serving-ready, the user and the LLM see an asymmetric graph. Those nodes are high priority.

### 3. It helps complete a local closed traversal loop

Pages should be chosen in groups that form a navigable local serving graph rather than as isolated one-off migrations.

## Selected batch

### Methods
- `wiki/methods/GCR.md`
- `wiki/methods/EPERM.md`
- `wiki/methods/ToG.md`

### Papers
- `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`

### Tasks
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`

### Benchmark
- `wiki/benchmarks/CWQ.md`

### Concept
- `wiki/concepts/重要推理路径.md`

## Why these nodes

These nodes are already present in the active KG reasoning serving graph:
- referenced from PathMind method/paper pages
- referenced from serving-ready task/scenario/benchmark/evidence pages
- likely to be traversed as the very next hop during QA

They are therefore higher value than lower-frequency pages that happen to exist elsewhere in the repository.

## Local serving-graph objective

This batch should create a stronger local graph around the current mainline:
- `PathMind`
- `路径优先化`
- `重要推理路径`
- `knowledge-graph-reasoning`
- `kgqa`
- `multi-hop-qa`
- `知识图谱推理问答`
- `WebQSP`
- `CWQ`
- `GCR`
- `EPERM`
- `ToG`

The goal is that QA starting from these nodes should stay inside serving-ready pages more often and fall back to legacy pages less often.

## Per-type migration expectations

### Method pages (`GCR`, `EPERM`, `ToG`)

Must provide:
- stable frontmatter
- readable sections covering method definition, problem, mechanism, evolution position, application scenarios, representative paper, concepts, evidence
- `Formal relations` covering at minimum:
  - `based_on`
  - `improves_on`
  - `targets_task`
  - `evaluated_on` when present in the ledger
  - incoming `proposes`
  - `applies_to` if ledger-backed

### Paper pages

Must provide:
- readable contribution / task / benchmark / citation / evidence sections
- `Formal relations` covering at minimum:
  - `proposes`
  - `targets_task`
  - `evaluated_on`
  - `cites`
  - `supported_by`
  - any ledger-backed `uses_concept`

### Task pages (`kgqa`, `multi-hop-qa`)

Must provide:
- readable method / concept / scenario / benchmark / paper coverage
- `Formal relations` centered on incoming:
  - `targets_task`
  - `supports`

### Benchmark page (`CWQ`)

Must provide:
- readable task / method / paper / scenario coverage
- `Formal relations` centered on incoming:
  - `evaluated_on`

### Concept page (`重要推理路径`)

Must provide:
- readable concept network, method, paper, task, scenario sections
- `Formal relations` centered on:
  - incoming `uses_concept`
  - outgoing `supports`

## Relation-ledger implications

This batch should not assume the current relation ledger is already complete enough for serving projection.

A required part of the batch is to identify and fill any missing formal edges that are necessary for truthful serving projection. That includes cases where:
- human-readable page content already claims a relation
- the serving page needs the relation for completeness
- but the ledger does not yet contain the formal edge

Ledger repair is therefore part of the batch whenever the missing edge is already justified by existing evidence caches.

## Recommended migration order

### Step 1: supporting concept/task/benchmark nodes
- `重要推理路径`
- `kgqa`
- `multi-hop-qa`
- `CWQ`

These are the shared convergence points for the batch and make later Method/Paper projections cleaner.

### Step 2: Method nodes
- `GCR`
- `EPERM`
- `ToG`

This establishes the method-level serving surfaces that most runtime traversals will hit.

### Step 3: Paper nodes
- the three corresponding paper pages

Paper pages usually have denser formal projections, so migrating them last reduces rework.

## Governance requirements

Every page in the batch must pass:

### 1. Structural governance
- `python3 scripts/lint_graph.py`

### 2. Ontology-semantic governance
- `ontology-semantic-review`

### 3. Serving governance
- `serving-governance-review`

No page in the batch is considered `serving-ready` without all three.

## Page-level acceptance criteria

A migrated page must satisfy all of the following:

1. **Structure complete**
   - required readable sections exist
   - `## Formal relations` exists
   - `### Outgoing` exists
   - `### Incoming` exists

2. **Formal projection complete**
   - all ledger-backed one-hop relations required for the page are projected

3. **Readable layer does not overclaim**
   - prose may summarize, but it must not imply formal neighbors that do not exist in the serving projection

4. **Evidence is traceable**
   - key edges expose evidence drill-down paths

## Batch-level acceptance criteria

The batch is complete only if:

1. the migrated pages individually satisfy page-level acceptance criteria
2. the batch passes all three governance gates
3. the local serving graph becomes materially more continuous
4. QA from current high-frequency entry nodes no longer falls back immediately to legacy pages for the migrated neighbors

## Failure conditions

### Page-level failure
- missing required formal edges
- readable/formal misalignment
- inadequate evidence drill-down
- unresolved ontology-semantic issues

### Batch-level failure
- pages individually look acceptable but still leave the local graph highly fragmented
- traversal from existing serving-ready pages still lands mostly on non-serving neighbors

## Expected outcome

After this batch:
- `PathMind`-centered KG reasoning QA should remain within serving-ready pages more often
- Paper ↔ Method ↔ Task ↔ Benchmark ↔ Concept traversal should become smoother
- the project will have moved from “framework established” to “runtime coverage visibly improved”

## Recommendation

Proceed with this high-frequency batch as the next migration subproject.

It is the smallest batch that should produce a noticeable improvement in actual QA graph continuity without reopening the full-repository rollout question.
