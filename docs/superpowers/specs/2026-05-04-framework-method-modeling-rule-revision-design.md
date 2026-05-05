# Framework/Method Modeling Rule Revision Design

Date: 2026-05-04

## Summary

Revise the framework / taxonomy modeling rule in `wiki/ontology/graph-standard.md` so that:
- framework / taxonomy remains a default Concept-side modeling path
- method-like frameworks are explicitly allowed to be modeled as Method when their dominant semantics are procedural, evaluative, or evolutionary
- the document stays internally consistent across the modeling axiom, the Concept section, and the paper-type exemption section

This is a narrow ontology wording fix, not a broader ontology redesign.

## Problem

The current wording in `wiki/ontology/graph-standard.md` treats framework as Concept with an effectively absolute rule:
- the modeling axiom says framework should not be written as Method
- the Concept section repeats that framework should not be modeled as Method
- the paper-type rules say survey-produced framework / taxonomy outputs should be connected to Concept rather than Method

This is stable for survey-style semantic frameworks, but too rigid for framework-labeled contributions that behave like methods:
- they define executable procedural steps
- they are compared experimentally against alternatives
- they sit on a method evolution chain

Under the current wording, those objects are forced into Concept even when Method semantics would fit better.

## Goals

- Keep the ontology default that framework / taxonomy does not become a new top-level node type.
- Preserve Concept as the default landing place for organization / classification / explanation frameworks.
- Add an explicit Method-side exception for method-like frameworks.
- Make the wording internally consistent in all affected sections.

## Non-goals

- Introduce a new `Framework` node type.
- Redesign the rest of the ontology.
- Change relation ledger ownership or serving-ready projection rules.
- Force existing framework-flavored Concept pages to migrate unless their dominant semantics are method-like.

## Chosen approach

Adopt a **default + semantic test** rule:

1. If a framework / taxonomy primarily organizes knowledge, categories, layers, roles, or explanations, model it as Concept.
2. If a framework primarily defines executable method flow, is evaluated experimentally, or participates in method evolution semantics, model it as Method.
3. Keep `Paper --proposes-->` as the main carrier relation, where the target may now be either Concept or Method depending on dominant semantics.

This keeps the ontology simple while preventing mechanical downgrading of method-like frameworks into Concept.

## Why this approach

### Option A: Minimal exception sentence only
Pros:
- smallest diff
- lowest disruption

Cons:
- leaves the surrounding wording structurally absolute
- makes the exception feel secondary and easy to overlook

### Option B: Default + semantic test
Pros:
- makes the decision rule explicit
- matches real variation in framework-labeled research artifacts
- still preserves Concept as the default path

Cons:
- slightly more visible wording change

### Option C: Keep axiom unchanged and explain later
Pros:
- most conservative

Cons:
- preserves the main contradiction
- readers will still be misled by the earlier absolute statement

Recommendation: **Option B**.

## Required document changes

Update these three locations together so the ontology remains internally consistent:

1. `wiki/ontology/graph-standard.md` modeling axiom section
2. `wiki/ontology/graph-standard.md` Concept section
3. `wiki/ontology/graph-standard.md` paper-type and exemption rules

## Proposed wording

### A. Modeling axiom section

Replace the current framework lines with:

```md
## survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task，也不上提为 Concept。
- Framework / taxonomy 若主要承担知识组织、分类、分层或解释框架语义，默认落为 Concept；其中 framework 可使用 `concept_kind: framework` 标记。
- Framework 若主要承担可执行方法流程、明确实验对比或方法演化语义，则应按 Method 处理，而不是机械落为 Concept。
- 当论文的核心贡献是 framework / taxonomy 型知识结构时，应根据其主要语义选择 `[[Paper]] --proposes--> [[Concept]]` 或 `[[Paper]] --proposes--> [[Method]]`：Paper 表示论文载体，Concept / Method 表示被提出的核心知识产物。
```

### B. Concept section

Revise the framework-specific Concept guidance to:

```md
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- Framework 若主要承担知识组织、分类、分层或解释框架语义，默认使用 `concept_kind: framework` 作为 Concept 落库；若主要承担可执行方法流程、明确实验对比或方法演化语义，则应按 Method 处理。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库；但若其主语义是方法流程与评测对象，则可按 Method 建模，而不是机械归入 Concept。
```

### C. Paper-type and exemption rules

Revise the survey / framework lines to:

```md
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- survey 论文属于 Paper 层；若论文的核心知识产物是 framework / taxonomy，则应按其主要语义落为 Concept 或 Method，并通过 `proposes` 与论文连接，而不是误写为 Task 或独立节点类型。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，若其主要承担知识组织、分类或解释语义，优先把核心知识落为 Concept 节点中的框架型 / taxonomy 型概念；若其主要承担可执行方法流程、实验对比或方法演化语义，则可按 Method 建模。
```

## Decision rule

When deciding between Concept and Method for a framework-labeled object, use dominant semantics rather than the author-facing label alone.

Prefer **Concept** when the object mainly provides:
- taxonomy
- layered architecture for explanation
- role decomposition
- semantic organization
- analytical framing

Prefer **Method** when the object mainly provides:
- executable steps or pipeline
- procedural mechanism
- direct experimental comparison target
- explicit improvement / inheritance relation to other methods

## Expected impact

- Survey and taxonomy knowledge products still land cleanly in Concept.
- Method-like frameworks can participate naturally in:
  - `based_on`
  - `improves_on`
  - `evaluated_on`
  - `parent_methods` / `child_methods`
- The ontology avoids creating empty or awkward Concept nodes for artifacts that are actually methodological.

## Risks and mitigations

### Risk: Overusing Method for anything called framework
Mitigation:
- keep Concept as the default
- require dominant procedural / evaluative / evolutionary semantics before choosing Method

### Risk: Existing concept pages become ambiguous
Mitigation:
- this change is interpretive, not a forced migration rule
- existing pages only need reconsideration when their dominant semantics are clearly method-like

## Success criteria

- The modeling axiom no longer states an absolute ban on framework-as-Method.
- The Concept section and paper-type rules use the same semantic split.
- Readers can decide Concept vs Method for framework-labeled objects without contradiction.
- No new top-level ontology type is introduced.
