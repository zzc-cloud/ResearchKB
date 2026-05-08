---
title: Relation Instance and Object/Index Semantics Projection Redesign
date: 2026-05-08
tags:
  - spec
  - researchkb
  - ontology
  - relations
  - serving
  - projection
status: draft
---

# Relation Instance and Object/Index Semantics Projection Redesign

Date: 2026-05-08

## Summary

This spec redesigns the formal relation ledger model and the serving-layer projections built from it.

The new unified direction is:

1. relation ledger instance fields use `edge_semantics` and `evidence`
2. object-page `Formal relations` no longer act as neighbor-only summaries; they become direct projections of formal relation instances
3. each projected incoming / outgoing item must carry:
   - relation type
   - neighbor object
   - `edge_semantics`
   - `evidence`
4. repeated relation instances are not merged, even when `relation_type` and neighbor object are the same
5. `ontology/entities/<entity-domain>/index.md` entries stop using free-form trailing prose hooks and instead project a controlled object-level field, `object_semantics`, from object pages
6. the full compile pipeline must align to this model:
   - `paper-ingest`
   - `relation-reconciliation`
   - `page-projection-sync`
   - `index-sync`
   - structural governance
   - ontology semantic governance
   - serving governance

## Problem

The current system still mixes several different semantic styles across layers.

### 1. Relation ledgers use one semantic field, object pages use another pattern

Formal relation instances are currently written with a `reason` field, but object pages do not fully project relation-instance semantics. They often project only:

- relation type
- neighbor object
- sometimes evidence

This means the most important instance-level meaning — why the edge is true — is not reliably visible at the serving layer.

### 2. Object-page `Formal relations` are still too close to neighbor lists

Even after recent projection improvements, object-page incoming / outgoing sections still tend to behave like structured adjacency summaries rather than true projections of relation instances.

That causes loss of formal truth detail:

- edge-level semantics are not fully projected
- evidence is not always treated as a first-class projected field
- multiple distinct ledger instances can be conceptually collapsed into one displayed neighbor

### 3. Index pages use uncontrolled prose hooks rather than governed object semantics

In domain indexes such as `ontology/entities/papers/index.md`, entries currently end with free-form trailing summaries such as:

```md
- KnowPath 入口（文档：`...`）：[[...]] — PathMind 引用的生成推理路径上游论文，占位节点，状态=placeholder
```

That trailing segment is doing semantic work, but it is not represented as a governed field. This makes index entries inconsistent with the relation-ledger instance model and object-page serving model.

### 4. The compile pipeline no longer has a single semantic projection model

Today, the system effectively has three different semantic layers:

- relation ledger: instance semantics via `reason`
- object page: semi-structured relation projection
- index page: prose hook summaries

These layers are related, but not yet governed by the same representation contract.

## Goals

- Replace relation-instance `reason` with `edge_semantics`.
- Make object-page `Formal relations` a true projection of relation instances, not just neighbors.
- Require each projected relation instance to carry normalized evidence.
- Preserve instance multiplicity: no forced merging of repeated neighbor relations.
- Introduce `object_semantics` as the controlled object-level semantic field used to project domain-index entries.
- Align the full compile / sync / governance pipeline to the same semantic model.

## Non-goals

- Redesign the ontology node types themselves.
- Replace Obsidian wikilinks with another link system.
- Collapse relation ledgers into object pages.
- Merge repeated relation instances for readability.
- Introduce a second formal truth source.

## Confirmed design decisions

### 1. Relation-instance semantics field renaming

All formal relation instances move from `reason` to `edge_semantics`.

Canonical ledger form becomes:

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - edge_semantics: 该实例边为什么成立
  - evidence: [[证据页]]
```

This is not a cosmetic rename. It makes explicit that the field belongs to the relation instance itself, not to generic prose explanation.

### 2. Object-page `Formal relations` become relation-instance projections

Object-page incoming / outgoing sections are no longer interpreted as simple neighbor views.

They are instead defined as:

> projections of formal relation instances from the canonical relation ledger

This means every displayed item on an object page must preserve the core fields of the source relation instance.

### 3. Required projected fields on object pages

Each projected incoming / outgoing item must include:

- relation type
- neighbor object and path
- `edge_semantics`
- `evidence`

Recommended format:

```md
## Formal relations

### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。

- `targets_task`：任务目标（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
  - edge_semantics: 该方法被明确定位为知识图谱问答任务求解方法。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。

- `proposes`：由论文提出（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - edge_semantics: 论文首次提出 PathMind 作为核心方法框架。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]
```

### 4. No merging of repeated relation instances

If two formal relation instances share:

- the same `relation_type`
- the same neighbor object

but differ in:

- `edge_semantics`
- `evidence`
- or any instance-level meaning

then object pages must not merge them.

Each ledger instance projects to its own object-page item.

This keeps object pages aligned with formal truth rather than human-oriented deduplicated summaries.

### 5. Evidence projection is normalized

Object pages should not carry arbitrary raw evidence strings from ledgers.

Instead, the projected `evidence` field should use a normalized Evidence-link form:

```md
- evidence: [[../evidence/PathMind.sections|PathMind.sections]]
```

This keeps the object-page serving layer stable and machine-readable.

### 6. Domain-index entries project object-level semantics, not free prose hooks

Each object page must expose a governed object-level semantic field, `object_semantics`.

This field is the truth source for index-entry semantics.

The domain index then projects:

- object path
- wikilink
- `object_semantics`
- status / entry state

rather than hand-written hook prose.

This makes index entries structurally analogous to relation-instance projections:

- relation pages project `edge_semantics`
- index pages project `object_semantics`

### 7. `object_semantics` source location

`object_semantics` should be stored on the object page as a dedicated object-level semantic source.

Recommended form:

```md
## Object semantics
PathMind 是一个面向知识图谱推理的 Retrieve-Prioritize-Reason 框架，核心在于通过路径优先化识别重要推理路径，再引导 LLM 沿高价值路径完成推理。
```

This is preferred over a long frontmatter field because:

- it allows natural-language semantic content without overloading metadata
- it is readable to humans
- it remains a stable projection source for `index-sync`

## Architecture

### 1. Relation ledger layer

Location:
- `ontology/relations/*.md`

Responsibilities:
- remain the only formal truth source for instance edges
- store each instance with canonical source / relation / target shape
- store instance-level `edge_semantics`
- store instance-level `evidence`

Canonical ledger instance form becomes:

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - edge_semantics: ...
  - evidence: [[...]]
```

### 2. Object-page serving layer

Location:
- `ontology/entities/**/<object>.md`

Responsibilities:
- serve as the primary reading and exploration surface
- expose object-level semantics through `## Object semantics`
- expose relation-instance projections through `## Formal relations`
- preserve evidence and edge semantics for each projected instance

### 3. Index serving layer

Location:
- `ontology/entities/<entity-domain>/index.md`

Responsibilities:
- expose object discovery and domain entrypoints
- project controlled `object_semantics` from object pages
- stop relying on free-form trailing hook prose

### 4. Governance layer

Responsibilities:
- ensure relation ledger shape is consistent
- ensure object pages project full instance semantics
- ensure index pages project governed object semantics
- ensure these three surfaces remain aligned

## Compile-pipeline alignment

### 1. `paper-ingest`

`paper-ingest` must emit structured relation candidates that are rich enough to become relation-instance truth.

Each relation candidate should contain at least:

- relation type
- source object
- source path
- target object
- target path
- `edge_semantics`
- `evidence`
- evidence path

In parallel, object-page candidate content must include an object-level semantic source suitable for later index projection.

Expected effect:

- ingest no longer emits relation candidates that need semantic reconstruction downstream
- object pages gain a stable source for index semantics

### 2. `relation-reconciliation`

`relation-reconciliation` becomes the stage that converts relation candidates into fully governed formal relation instances.

It must:

- normalize candidate structure
- preserve `edge_semantics`
- preserve `evidence`
- write canonical relation ledgers with those fields
- treat each instance as separately projectable even when neighbor object repeats

Expected effect:

- ledger truth becomes fully projection-ready

### 3. `page-projection-sync`

`page-projection-sync` becomes the relation-instance projection stage.

It must project one ledger instance into one object-page item.

For each item, it must render:

- relation type
- neighbor object path and link
- `edge_semantics`
- normalized `evidence`

It must not deduplicate repeated neighbor instances.

Expected effect:

- object pages become a full serving mirror of relation-instance truth at one hop

### 4. `index-sync`

`index-sync` must stop treating trailing object hooks as free prose.

It must instead read the object page’s `object_semantics` source and project it into the domain index entry format.

Expected effect:

- index entries become governed object-instance projections
- index and object pages become semantically aligned

### 5. Structural governance

Structural governance must validate:

- relation ledger entries use `edge_semantics` and `evidence`
- object-page `Formal relations` items include `edge_semantics` and `evidence`
- repeated instance projections are not merged away
- domain index entries use projected `object_semantics` instead of arbitrary prose

### 6. Ontology semantic governance

Semantic governance must validate:

- `edge_semantics` correctly explains why a relation instance holds
- `evidence` actually supports that instance semantics
- `object_semantics` correctly describes the object instance identity
- object pages do not distort or compress relation truth beyond the allowed projection contract

### 7. Serving governance

Serving governance must validate:

- object pages remain readable despite more instance-level detail
- AI can use `edge_semantics` to choose topological expansion paths
- evidence remains a stable drill-down surface
- index pages remain lightweight enough for entry use while still semantically governed

## Object-page format contract

Every governed object page should contain:

1. object-level semantic source
2. human-readable content
3. governed relation-instance projection

Recommended high-level structure:

```md
# Object Title

## Object semantics
<object-level semantic truth source>

## Human-readable sections
...

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- ...
  - edge_semantics: ...
  - evidence: [[...]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- ...
  - edge_semantics: ...
  - evidence: [[...]]
```

## Index-entry format contract

Recommended future entry format:

```md
- KnowPath 入口（文档：`ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`）：[[ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
  - object_semantics: 生成推理路径方向的上游论文，占位节点。
  - status: placeholder
```

This is preferred over the current format:

```md
- KnowPath 入口（文档：`...`）：[[...]] — PathMind 引用的生成推理路径上游论文，占位节点，状态=placeholder
```

because it separates governed semantic fields from prose punctuation.

## Required spec changes

This redesign requires coordinated updates to at least:

- `ontology/graph-standard.md`
- `CLAUDE.md`
- all `ontology/relations/*.md` ledger files
- object-page templates / conventions under `ontology/entities/**`
- domain index conventions under `ontology/entities/*/index.md`
- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `.claude/skills/index-sync/SKILL.md`
- `scripts/lint_graph.py`
- ontology semantic review references and checks
- serving governance checks

## Acceptance criteria

This redesign is complete when all of the following are true:

1. Relation ledger instances use `edge_semantics` and `evidence` as canonical fields.
2. Object-page `Formal relations` project relation instances, not neighbor summaries.
3. Every projected object-page item includes neighbor, `edge_semantics`, and `evidence`.
4. Repeated neighbor relations with distinct instance semantics remain separate items.
5. Object pages expose a governed `object_semantics` source.
6. Domain-index entries project `object_semantics` rather than free-form trailing hook prose.
7. The full compile pipeline and all three governance exits enforce the same representation model.

## Recommendation

Adopt this redesign as a representation unification effort, not as an isolated formatting tweak.

The clean long-term split should be:

- **relation ledger** → relation-instance truth via `edge_semantics` + `evidence`
- **object page** → relation-instance serving projection
- **domain index** → object-instance serving projection via `object_semantics`
