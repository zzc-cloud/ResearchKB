---
title: Formal Relation Projection, Evidence, and Serving Governance Design
date: 2026-05-07
tags:
  - spec
  - researchkb
  - ontology
  - relations
  - evidence
  - serving
status: draft
---

# Formal Relation Projection, Evidence, and Serving Governance Design

Date: 2026-05-07

## Summary

This spec defines a stricter serving and governance model for ResearchKB formal relations, Evidence pages, and object-page projections.

The confirmed direction is:

1. `ontology/relations/*.md` remains the only formal instance-edge truth source.
2. A formal relation instance is uniquely identified by the triple `relation_type + source + target`.
3. Object-page `Formal relations` sections are not a second ledger. They are adjacency projections generated from relation ledgers.
4. `Paper` is removed from the allowed source set of `supported_by`.
5. `Evidence` and `Paper` have no formal relation between them.
6. `Evidence` retains only `source_file` as its direct provenance anchor to the raw PDF.
7. Every wikilink that appears in an object page body must also appear in that page's `Formal relations` section.
8. Object-page `Formal relations` must use a semi-expanded projection format optimized for both Obsidian navigation and AI path resolution.
9. These rules are not authoring suggestions. They must be automatically maintained by the full compile pipeline:
   - `paper-ingest`
   - `relation-reconciliation`
   - `page-projection-sync`
   - structural governance
   - ontology semantic governance
   - serving governance

## Problem

The current representation has three coupled issues.

### 1. `Paper --supported_by--> Evidence` is semantically awkward

For `Paper`, the current `sections` / `refs` / `experiments` / `analysis` pages are not naturally "evidence supporting the existence of the paper." They are structured evidence caches compiled from the paper and used for verification, audit, and drill-down.

This makes `[[Paper]] --supported_by--> [[Evidence]]` feel like a modeling shortcut rather than a clean ontology relation.

### 2. Object-page `Formal relations` are hard to use in Obsidian and ambiguous for AI

The current projection style often uses complete edge strings inside backticks, such as:

```md
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
```

This causes two problems:

- Obsidian does not treat wikilinks inside code spans as clickable navigation links.
- AI sees a display string rather than a clearly structured projection with explicit local role, relation semantics, and document path.

### 3. Body wikilinks can drift away from the formal graph

If page bodies can introduce arbitrary extra wikilinks beyond those recorded in `Formal relations`, then:

- Obsidian navigation no longer matches formal ontology adjacency.
- AI sees a larger apparent graph than the governed formal graph.
- Topology expansion becomes less controlled and less auditable.

## Goals

- Keep relation ledgers as the only formal truth source for instance edges.
- Make object pages the default serving surface for graph navigation and constrained expansion.
- Ensure every projected adjacency supports both Obsidian navigation and AI path resolution.
- Remove semantically awkward Paper-to-Evidence formal modeling.
- Keep Evidence pages useful for verification without creating a second implicit graph.
- Enforce that clickable object links and formal ontology adjacency remain aligned.
- Turn these rules into compile-pipeline invariants rather than manual habits.

## Non-goals

- Introduce standalone markdown files for each individual relation instance.
- Make object pages jump back to a specific relation-ledger line during normal serving.
- Preserve legacy complete-edge projection formatting on object pages.
- Add a new formal relation between `Evidence` and `Paper`.
- Treat body prose as a second source of formal graph truth.

## Confirmed design decisions

### 1. Canonical truth layer

- `ontology/relations/*.md` is the only formal instance-edge truth source.
- Relation ledgers are authoritative for governance, repair, and truth checks.
- Object pages and Evidence pages do not define formal edges independently.

### 2. Formal relation identity

A formal relation instance is uniquely defined by:

- `relation_type`
- `source`
- `target`

That triple is the instance identity.

The following are instance attributes, not new instances:

- `reason`
- `evidence`
- `status`
- `note`

This means multiple evidence anchors or richer reasoning do not create multiple formal instances when the triple is unchanged.

### 3. Object-page serving model

Object pages remain the default navigation surface for most graph exploration.

The expected serving flow is:

1. enter an object domain index
2. resolve a governed object page
3. read the object page body and `Formal relations`
4. use adjacency semantics to choose the next expansion step
5. descend to Evidence pages only when verification is needed
6. read relation ledgers only in governance, repair, audit, or explicit truth-check scenarios

### 4. `supported_by` source-set contraction

`Paper` must be removed from the allowed source set of `supported_by`.

The intended remaining source set is:

- `Method`
- `Concept`
- `Task`
- `Scenario`
- `Benchmark`

`Evidence` remains the target.

Rationale:

- `supported_by` should mean that a governed knowledge object is backed by an Evidence page.
- For `Paper`, Evidence is better understood as compiled verification material, not as ontology support establishing the paper node itself.

### 5. No formal relation between `Evidence` and `Paper`

`Evidence` and `Paper` should not be connected by a formal edge.

Confirmed direction:

- no `Paper --supported_by--> Evidence`
- no new replacement formal relation between `Evidence` and `Paper`
- no body-only wikilink from Evidence to Paper

Instead:

- `Evidence` keeps `source_file`
- `source_file` anchors the page to the raw PDF
- formal graph connectivity from a paper to evidence-backed material remains indirect, through the paper's related `Method`, `Concept`, `Task`, `Scenario`, and `Benchmark` objects

### 6. `source_file` versus provenance

This spec treats `source_file` as the direct provenance anchor field on an Evidence page.

- `source_file` answers: which managed raw PDF this Evidence page comes from
- provenance is the broader traceability concept
- in this design, the formal page-level provenance anchor that must remain explicit is `source_file`

No additional formal Paper link is required to express provenance.

### 7. Body-wikilink restriction

For governed object pages, every wikilink appearing in the body must already appear in that page's `Formal relations` section.

This means:

- bodies may contain rich prose
- bodies may explain object semantics and neighbor semantics
- bodies may not introduce extra clickable ontology neighbors beyond the formal adjacency projection

The same rule applies to Evidence pages.

Consequences:

- clickable links in the page body are a subset of the page's formal projected neighbors
- Obsidian navigation remains aligned with formal ontology adjacency
- AI does not see a larger navigable graph than the formal serving graph

## Architecture

### 1. Relation ledger layer

Location:
- `ontology/relations/*.md`

Responsibilities:
- maintain canonical formal instance edges
- bind each triple to `reason`, `evidence`, `status`, and optional notes
- serve as governance truth for repair and audit

Canonical instance format remains:

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: ...
  - evidence: [[...]]
```

This format remains appropriate in ledgers because the ledger is a truth and governance surface, not the default click-navigation surface.

### 2. Object-page serving layer

Location:
- `ontology/entities/**/<object>.md`

Responsibilities:
- serve as the default entrypoint for governed graph navigation
- present local object semantics
- present governed local adjacency in a form usable by both humans and AI
- constrain expansion to typed formal neighbors

Object pages are not a second relation ledger. They are generated or synchronized projections.

### 3. Evidence verification layer

Location:
- `ontology/entities/evidence/*.md`

Responsibilities:
- preserve verifiable mechanism, experiment, citation, analysis, and provenance material
- support drill-down when a formal object claim needs checking
- expose only those ontology-object links that correspond to formal relations already recognized in the graph

Evidence pages are part of the serving layer, but they are not Paper-link navigation pages.

## Object-page body contract

### 1. Body function

The body of a governed object page should contain:

- the object's own semantic content
- explanations of why adjacent nodes are relevant
- concise local context that helps an AI decide whether to expand into a neighbor

### 2. Body link rule

Every object-page body wikilink must be present in `Formal relations`.

Allowed:
- richer prose than the formal relation section
- non-link text that references additional concepts without introducing clickable graph neighbors

Not allowed:
- extra object wikilinks with no formal relation projection
- body-only ontology navigation shortcuts

### 3. Why this matters

This rule binds together:

- formal graph adjacency
- Obsidian click navigation
- AI expansion candidate visibility

As a result, topology expansion remains governed rather than accidental.

## Evidence-page contract

### 1. Evidence role

An Evidence page is a structured verification artifact derived from a raw PDF and tied to formal ontology objects through supported formal relations.

### 2. Evidence must keep

- frontmatter with `source_file`
- structured evidence content
- `Formal relations`
- object links only for formally recognized adjacent ontology objects

### 3. Evidence must not do

- create a formal relation to `Paper`
- body-link a `Paper` note outside the formal graph
- act as an uncontrolled secondary navigation surface

### 4. Evidence body links

If an Evidence page body links:

- `[[../methods/...]]`
- `[[../concepts/...]]`
- `[[../tasks/...]]`
- `[[../scenarios/...]]`
- `[[../benchmarks/...]]`

those linked objects must already be present in the page's `Formal relations` section.

## Object-page `Formal relations` projection format

### 1. Requirements

The projection format must:

- optimize for Obsidian click navigation
- expose explicit neighbor document paths for AI
- state the current page's role in each section
- preserve relation type semantics
- help AI decide which neighbors are worth topological expansion

### 2. Section structure

Every governed object page must contain:

```md
## Formal relations

### Outgoing
当前对象作为 source；以下列出当前对象指向的邻接对象。

### Incoming
当前对象作为 target；以下列出指向当前对象的邻接对象。
```

These role sentences are required. They make the local edge direction explicit for AI without forcing each line to repeat the full source-target string.

### 3. Entry format

Each projected adjacency entry must use the semi-expanded form:

```md
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
```

Example:

```md
## Formal relations

### Outgoing
当前对象作为 source；以下列出当前对象指向的邻接对象。

- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]

### Incoming
当前对象作为 target；以下列出指向当前对象的邻接对象。

- `proposes`：由论文提出（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
```

### 4. Why this format is the target

Compared with the legacy complete-edge inline string:

```md
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
```

this format improves all target use cases:

#### For Obsidian
- the neighbor link is clickable
- the page works as an adjacency navigation surface
- no hidden non-clickable link inside code spans

#### For AI
- the current page role is explicit from section context
- the relation type is explicit
- the semantic label explains the meaning of expansion
- the neighbor document path is explicit in prose
- the display link provides the actual object anchor

#### For governance
- projection format becomes lintable
- body links can be checked against projected neighbors
- serving pages become more predictable and machine-consumable

### 5. What object pages should no longer use

Object-page `Formal relations` should no longer use complete source-target edge strings as the primary projection format.

Those remain appropriate in relation ledgers, but not in serving-page projections.

## Pipeline invariants

These rules must be enforced by the full compile pipeline, not merely recommended.

### 1. `paper-ingest`

Responsibilities:
- produce initial object candidates, Evidence candidates, and relation candidates
- generate early content close to target structure
- avoid prematurely claiming formal graph completion

Required invariants:
- do not default-generate `Paper --supported_by--> Evidence`
- do not create a formal `Evidence ↔ Paper` relation
- keep `source_file` on Evidence as the provenance anchor
- avoid introducing uncontrolled body wikilinks that later contradict formal projections

### 2. `relation-reconciliation`

Responsibilities:
- reconcile relation candidates into formal relation ledgers
- enforce formal instance identity at the triple level

Required invariants:
- relation instances deduplicate on `relation_type + source + target`
- `reason`, `evidence`, `status`, `note` attach to the canonical triple instance
- `supported_by` rejects `Paper` as a source type
- only the contracted allowed source types can produce `supported_by` formal edges

### 3. `page-projection-sync`

Responsibilities:
- project formal truth from ledgers into governed object pages and Evidence pages
- normalize page-local serving format

Required invariants:
- `Formal relations` sections are generated from ledgers, not manually trusted
- projection uses the semi-expanded path-explicit format defined in this spec
- `Outgoing` and `Incoming` role sentences are present
- body wikilinks are checked and normalized so they do not exceed the projected formal neighbor set
- legacy non-clickable complete-edge object-page formatting is removed during sync

### 4. Structural governance

Responsibilities:
- validate page structure and rendering-oriented consistency

Required checks:
- required sections exist
- `Formal relations` format matches the projection template
- body wikilinks are a subset of formal projected neighbors
- no legacy complete-edge object-page projection lines remain
- Evidence pages do not body-link `Paper`
- projected neighbors are internally resolvable to the expected note paths

### 5. Ontology semantic governance

Responsibilities:
- validate that object types and relation semantics are conceptually correct

Required checks:
- `supported_by` is only used for allowed source types
- `Paper` does not appear as a `supported_by` source
- Evidence links only formalized ontology objects, not merely mentioned ones
- no unnecessary formal relation is introduced just for navigation convenience

### 6. Serving governance

Responsibilities:
- validate that the resulting pages are actually suitable as serving surfaces for QA and exploration

Required checks:
- object pages provide usable one-hop formal adjacency
- semantic labels are informative enough for AI expansion decisions
- click navigation and formal graph adjacency stay aligned
- the page does not expose extra clickable ontology nodes beyond governed projections

## Required specification updates

This design implies follow-up changes to at least:

- [[CLAUDE]]
- [[ontology/graph-standard]]
- [[ontology/relations/supported_by]]
- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`
- structural lint / governance scripts
- ontology semantic governance skill logic
- serving governance skill logic

## Rollout plan

### Phase 1: normalize the rules

Update:
- [[CLAUDE]]
- [[ontology/graph-standard]]
- relation-ledger semantics for `supported_by`

Outcome:
- the ontology cognition layer and formal rule layer align with the new model

### Phase 2: update pipeline writers

Update:
- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`

Outcome:
- newly produced pages and ledgers automatically follow the new invariants

### Phase 3: upgrade governance checks

Update:
- structural lint
- ontology semantic governance
- serving governance

Outcome:
- non-conforming pages are rejected before they are treated as serving-ready

### Phase 4: migrate existing pages

Tasks:
- remove `Paper` as `supported_by` source where present
- remove Evidence-to-Paper navigation links
- replace legacy object-page complete-edge projections
- re-sync object pages to the new formal projection format
- repair body wikilinks that exceed formal adjacency

Outcome:
- existing served content converges to the same invariants as newly ingested content

## Acceptance criteria

This design is successfully implemented when all of the following are true:

1. No governed page contains `Paper --supported_by--> Evidence` as a formal edge.
2. No governed Evidence page uses a formal or body-only clickable link to connect itself to a Paper.
3. Every object-page body wikilink also appears in that page's `Formal relations` projection.
4. Every projected adjacency entry in object pages uses the semi-expanded path-explicit format.
5. `Outgoing` and `Incoming` sections always state the current page role explicitly.
6. Relation ledgers remain the only formal instance-edge truth source.
7. `page-projection-sync` can regenerate compliant `Formal relations` sections from ledgers alone.
8. Governance checks reject pages whose clickable ontology links exceed formal adjacency.
9. The compile chain automatically preserves these rules for newly processed papers.

## Recommendation

Adopt this design as a pipeline contract, not a documentation preference.

The key architectural principle is:

> relation ledgers own formal truth; object pages own governed local serving; Evidence pages own verification; pipeline automation keeps all three aligned.
