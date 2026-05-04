# CLAUDE.md agent global cognition entry design

- Date: 2026-05-04
- Topic: Add a global-cognition entry section to `CLAUDE.md` for agents
- Scope: Documentation-only design for `CLAUDE.md`

## Goal

Add a short, high-priority section to `CLAUDE.md` that gives agents a stable global mental model for the repository, so they can approach different task types with the right top-level understanding before following workflow details.

The section should improve agent orientation without creating a second normative source alongside `wiki/ontology/graph-standard.md`.

## Problem

The current `CLAUDE.md` already contains:
- clear normative-boundary guidance
- a four-layer architecture section
- task entrypoints and default reading order

What is still missing is a compact, explicit statement of how an agent should connect:
1. ontology cognition as the single core authority
2. global system cognition as the task-facing framing layer
3. the repository’s layered information surfaces

Without that bridge, an agent can still understand the rules locally while missing the higher-order model that explains how to apply those rules consistently across question answering, governance, ingest, repair, and synthesis tasks.

## Chosen approach

Add a new section immediately after the existing “知识库结构与规范边界” section and before the existing “ResearchKB 核心架构” section.

This new section should:
- declare ontology cognition as the only core cognitive center
- state that `CLAUDE.md` does not define a parallel normative system
- explain that global cognition exists to turn ontology constraints into an agent’s unified working perspective across task types
- summarize the repository as one knowledge system with four responsibility layers
- anchor the agent with a small number of high-value reading and interpretation rules

## Why this approach

This is the best fit for the current `CLAUDE.md` because:
- it complements existing workflow sections instead of duplicating them
- it preserves `wiki/ontology/graph-standard.md` as the sole authority for node, relation, evidence, projection, and exemption judgment
- it improves orientation for all task types, not only one workflow
- it creates a high-level frame that can govern how the later sections are read

## Alternatives considered

### Option 1 — Pure abstract overview only
Pros:
- very short
- low maintenance

Cons:
- too weak to guide behavior
- does not sufficiently prevent agents from confusing service surfaces with governance sources

### Option 2 — Abstract overview plus a few anchor rules
Recommended and chosen.

Pros:
- gives a durable mental model
- stays short enough for `CLAUDE.md`
- reinforces the most important distinctions between ontology authority, governance truth, service projections, evidence, and raw provenance

Cons:
- intentionally leaves detailed procedures to later sections

### Option 3 — Detailed task-by-task examples
Pros:
- very explicit for first-time readers

Cons:
- overlaps heavily with existing workflow sections
- risks turning the new section into a duplicate process manual
- weakens the purpose of the section as a high-level cognitive frame

## Recommended content structure

The new section should have three parts.

### 1. Positioning paragraph
State that:
- ontology cognition is the single core cognition of ResearchKB
- `wiki/ontology/graph-standard.md` is the only authority for legality judgment
- `CLAUDE.md` provides an agent-facing operating perspective, not a second ontology standard

### 2. Four-layer summary
Summarize the system as four responsibility layers:
1. ontology skeleton layer
2. ontology instance compilation layer
3. ontology governance layer
4. ontology application layer

This summary should describe layer roles at a high level, not restate all implementation details.

### 3. Anchor rules
Include a short bullet list that makes the following distinctions explicit:
- formal QA defaults to serving-ready object pages rather than scanning `wiki/relations/` first
- `wiki/relations/` is the governance truth source for formal instance edges
- `Formal relations` on object pages are the projected, QA-facing constrained read surface
- `intermediate/papers/` is the default evidence layer for mechanisms, experiments, citations, baselines, and provenance checks
- `raw/` is for source trace-back only and does not organize the main graph

## Proposed insertion point

Insert the section in `CLAUDE.md`:
- after the section beginning at `## 知识库结构与规范边界`
- before the section beginning at `## ResearchKB 核心架构`

This placement is important because it lets the agent first understand authority boundaries, then learn the unifying global frame, and only then read the detailed architecture and workflows.

## Proposed draft text

```md
## Agent 的全局认知入口

ResearchKB 的唯一核心认知中心是本体认知。`wiki/ontology/graph-standard.md` 定义合法节点、关系、证据、实例边、投影与豁免规则，是所有知识判定的唯一权威来源。`CLAUDE.md` 不提供另一套平行规范；它的作用，是把这套本体约束转化为 Agent 在不同任务中的统一工作视角。

Agent 在处理问答、治理、摄入、修复、综述等任务时，应始终先把当前任务放回同一个知识系统中理解，而不是把仓库视为一组离散 markdown 文件。默认应按以下四层来建立全局认知：

1. **本体骨架层**
   - 由 `wiki/ontology/graph-standard.md` 定义合法知识边界与判定规则。

2. **本体实例编译层**
   - 负责把原始论文编译为 `intermediate/papers/` 证据缓存、`wiki/relations/` 正式关系实例边，以及 `wiki/` serving-ready 对象页中的投影结果。

3. **本体治理层**
   - 负责通过结构治理、语义治理与 serving 治理，决定哪些知识变更可以进入正式图谱。

4. **本体应用层**
   - 负责基于治理通过后的正式知识进行问答、分析、探索与综述生成。

这四层不是四套独立系统，而是同一知识系统中的不同职责面。全局认知负责帮助 Agent 判断“当前任务位于哪一层、应先读取哪一层、何时需要向邻近层扩展”；具体的节点、关系、证据与合法性判定，始终以本体规范为准。

因此，Agent 应默认遵循以下认知锚点：
- 正式知识问答优先读取 serving-ready 对象页，而不是先扫描 `wiki/relations/`
- `wiki/relations/` 是正式关系实例边的治理真源，主要用于补边、修复、审计与一致性核对
- 对象页中的 `Formal relations` 是治理通过后供问答与受约束拓扑扩展消费的正式读取面
- `intermediate/papers/` 是机制、实验、引用、基线与 provenance 的默认证据层
- `raw/` 只用于来源回溯，不承担主图谱组织职责
```

## Scope boundaries

This change is documentation-only.

It does not:
- change ontology semantics
- change any skill behavior
- change linting behavior
- change relation-ledger mechanics
- change serving projection rules

## Validation criteria

The design is successful if the new section:
- reinforces ontology cognition as the single core authority
- does not create a second normative source in `CLAUDE.md`
- gives agents a reusable cross-task mental model
- helps distinguish object pages, ledgers, evidence caches, and raw sources by role
- fits naturally into the current `CLAUDE.md` without duplicating later workflow sections

## Notes from self-review

- No placeholders remain.
- The scope stays constrained to one `CLAUDE.md` insertion.
- The section is intentionally explanatory first, with only a few anchor rules.
- The content complements, rather than replaces, existing workflow and architecture sections.
