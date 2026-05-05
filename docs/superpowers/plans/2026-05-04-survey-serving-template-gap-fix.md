# Survey Serving Template Gap Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add survey-paper, framework-concept, survey-driven scenario, and survey-driven task serving templates so the survey/mainline dry-run can advance from `pipeline-ran-with-manual-bridges` to `pipeline-ran-end-to-end`.

**Architecture:** First update `wiki/ontology/graph-standard.md` so the ontology explicitly distinguishes survey-paper templates from framework-flavored concept templates and gives scenario/task pages variant-specific serving shapes. Then teach `page-projection-sync` about these variants. Finally, migrate the five current representative survey-mainline pages so the new templates are exercised by real pages and can be rechecked through lint plus governance review.

**Tech Stack:** Markdown page templates in `wiki/`, skill definitions in `.claude/skills/`, Python 3 lint script (`scripts/lint_graph.py`), existing ontology-semantic-review and serving-governance-review gates.

---

## File map

### Standards and sync skill
- Modify: `wiki/ontology/graph-standard.md`
  - Add survey-paper serving branch, framework-concept branch, and survey-driven scenario/task branch guidance.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Add variant-specific handling for survey papers, framework concepts, survey-driven scenario pages, and survey-driven task pages.

### Representative survey-mainline pages
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `ontology-semantic-review`
- Test: `serving-governance-review`

---

### Task 1: Extend `graph-standard.md` with survey/framework serving template branches

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add explicit survey-paper guidance to the Paper section**

In `wiki/ontology/graph-standard.md`, directly after the current Paper body-structure list, insert:

```markdown
survey / framework 型 Paper 补充规则：
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架 / 核心概念、相关任务、应用场景、关键结论、综述证据来源。
- 这类 Paper 的 `Formal relations` 重点为：`proposes`（到 framework / concept）、`uses_concept`、`targets_task`、`cites`、`supported_by`。
- 若无统一 benchmark，必须显式以 `relation_exemptions` 说明 `evaluated_on` 按规范豁免，而不是伪造 benchmark formal edge。
```

- [ ] **Step 2: Add explicit framework-concept guidance to the Concept section**

In the `### Concept` section, after the current explanation bullets, insert:

```markdown
framework 型 Concept 补充规则：
- 若 `concept_kind: framework`，页面应优先描述：框架定义、层级结构 / 组成部分、相关概念、相关场景、相关任务、相关论文、证据来源。
- framework 型 Concept 的 `Formal relations` 重点为：incoming `proposes`、outgoing `uses_concept`、outgoing `applies_to`、outgoing / incoming `supports`、`supported_by`。
```

- [ ] **Step 3: Add survey-driven scenario/task serving guidance**

After the `### Task` body structure block, insert:

```markdown
survey / framework 主线的 Task 补充规则：
- 若任务页主要由 survey / framework 节点驱动，而非方法-基准驱动，人类区块应优先突出：相关框架 / 概念、相关场景、相关论文、证据来源 / 关系索引。
- `Formal relations` 重点为 incoming `targets_task`、incoming `supports`，以及必要时的 `supported_by`。
```

After the `### Scenario` body structure block, insert:

```markdown
survey / framework 主线的 Scenario 补充规则：
- 若场景页主要由 framework / survey 节点供给，人类区块应优先突出：使用的主要框架 / 概念 / 方法、相关任务、相关论文、证据来源。
- `Formal relations` 重点为 incoming `applies_to`、incoming `supports`，以及必要时的 `supported_by`。
```

- [ ] **Step 4: Run lint to confirm the standard still passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit the standard update**

```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: add survey serving template rules"
```

---

### Task 2: Teach `page-projection-sync` about survey/framework variants

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: inspect the skill file; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add variant-specific handling bullets to the sync skill**

In `.claude/skills/page-projection-sync/SKILL.md`, after `## 输入`, insert:

```markdown
## 变体识别规则
- survey 论文页：优先同步 `proposes`、`uses_concept`、`targets_task`、`cites`、`supported_by`，并保留 `evaluated_on` 豁免信息。
- framework 型 Concept 页：优先同步 incoming `proposes`、outgoing `uses_concept`、outgoing `applies_to`、`supports`、`supported_by`。
- survey / framework 主线的 Scenario 页：优先同步 incoming `applies_to`、incoming `supports`，并重排人类区块为“主要框架 / 概念 / 方法”优先。
- survey / framework 主线的 Task 页：优先同步 incoming `targets_task`、incoming `supports`，并重排人类区块为“相关框架 / 概念 / 场景 / 论文”优先。
```

- [ ] **Step 2: Add a scope guard to prevent prose overreach**

Append this block near the end of the skill file:

```markdown
## 变体同步边界
- survey / framework 变体允许重排模板化人类区块，但不得自动改写“关键结论”“我的批注”“开放问题”等解释性正文。
- 若页面缺少该变体所需的人类区块，应标记为 `manual_followups`，而不是擅自生成长篇 prose。
```

- [ ] **Step 3: Run lint to confirm the skill doc still satisfies repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit the sync-skill update**

```bash
git add .claude/skills/page-projection-sync/SKILL.md
git commit -m "docs: add survey-aware projection sync rules"
```

---

### Task 3: Upgrade the representative survey paper page

**Files:**
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the evidence tail with serving-ready survey-paper structure**

Replace the block from `## 与知识库其他内容的关联` through `## 我的批注` with:

```markdown
## 与知识库其他内容的关联
- 核心框架：[[复杂产品设计中的LLM-KG协同框架]]
- 核心概念：[[LLM增强知识图谱]]
- 主要场景：[[复杂产品设计]]
- 相关任务：[[engineering-design-knowledge-management]]
- 关键引用对象：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]、[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]、[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]、[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]、[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]、[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]

## 综述证据来源
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 引用与路线缓存：[[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- 分析与统计缓存：[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]

## Formal relations
### Outgoing
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --targets_task--> [[engineering-design-knowledge-management]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]

### Incoming
- 无

## Relation exemptions
- `evaluated_on`：按综述 / framework 论文规范豁免，无统一 benchmark。

## 我的批注
> 这篇论文的重要意义不在“证明某个模型更强”，而在于它暴露了知识库设计不能只围绕方法论文组织：对于 framework / survey / taxonomy 论文，概念、场景、任务阶段、角色划分和 research gaps 才是主知识资产。
```

- [ ] **Step 2: Run lint after the survey paper update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 4: Upgrade the framework-flavored concept pages

**Files:**
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add `concept_kind: framework` to the framework concept page frontmatter**

In `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`, update frontmatter from:

```yaml
title: 复杂产品设计中的LLM-KG协同框架
problem: [ontology-modeling, benchmark-survey, reasoning]
```

to:

```yaml
title: 复杂产品设计中的LLM-KG协同框架
concept_kind: framework
problem: [ontology-modeling, benchmark-survey, reasoning]
```

- [ ] **Step 2: Replace the tail of `wiki/concepts/LLM增强知识图谱.md` with serving-ready concept sections**

Replace everything from `## 与其他概念的关系` onward with:

```markdown
## 与其他概念的关系
- [[复杂产品设计中的LLM-KG协同框架]]：该框架是 LLM增强知识图谱在复杂产品设计中的分层化表达。
- [[复杂产品设计]]：是该概念的重要行业落地场景。
- [[路径优先化]]：二者都体现 LLM 与图结构知识协同，但后者是方法级概念，前者是系统级协同概念。

## 相关方法 / 路线
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[ToG]]

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关任务 / 场景
- 任务：[[engineering-design-knowledge-management]]
- 场景：[[复杂产品设计]]

## 证据来源
- 概念关系：[[concept_links]]
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
```

- [ ] **Step 3: Replace the tail of `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md` with framework-ready concept sections**

Replace everything from `## 与其他概念的关系` onward with:

```markdown
## 与其他概念的关系
- [[LLM增强知识图谱]]：这是该概念在复杂产品设计场景中的具体框架化落地。
- [[复杂产品设计]]：框架面向的核心场景。
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]：该框架首先以 survey 论文形式被系统提出与归纳。

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]

## 相关场景与任务
- 场景：[[复杂产品设计]]
- 任务：[[engineering-design-knowledge-management]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]

## Formal relations
### Outgoing
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- `[[复杂产品设计中的LLM-KG协同框架]] --applies_to--> [[复杂产品设计]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]

### Incoming
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
```

- [ ] **Step 4: Run lint after the framework concept updates**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 5: Upgrade the survey-driven scenario and task pages

**Files:**
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the tail of `wiki/scenarios/复杂产品设计.md` with survey-ready scenario sections**

Replace everything from `## 使用的主要方法 / 框架` onward with:

```markdown
## 使用的主要方法 / 框架 / 概念
- [[复杂产品设计中的LLM-KG协同框架]] — 将数据层、协同层、能力层与任务层整合为系统框架。
- [[LLM增强知识图谱]] — 作为复杂设计中的系统级知识协同范式。
- [[PathMind]] — 虽非该领域专用方法，但代表了 LLM + KG 方法论文如何在推理任务中形成结构化证据链。

## 相关任务
- [[engineering-design-knowledge-management]]

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 分析与统计缓存：[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[复杂产品设计中的LLM-KG协同框架]] --applies_to--> [[复杂产品设计]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
```

- [ ] **Step 2: Replace the tail of `wiki/tasks/engineering-design-knowledge-management.md` with survey-ready task sections**

Replace everything from `## 相关方法 / 框架` onward with:

```markdown
## 相关框架 / 概念
- [[复杂产品设计中的LLM-KG协同框架]]
- [[LLM增强知识图谱]]

## 相关场景
- [[复杂产品设计]]

## 相关论文
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]

## 证据来源 / 关系索引
- 方法映射：[[task_method_map]]
- 证据索引：[[evidence_index]]
- 结构化章节缓存：[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
- 分析与统计缓存：[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --targets_task--> [[engineering-design-knowledge-management]]`
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]
```

- [ ] **Step 3: Run lint after the survey-driven scenario/task updates**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 6: Re-run the survey dry-run governance checks

**Files:**
- Modify: none unless review identifies a minimal fix
- Test: `python3 scripts/lint_graph.py`, `ontology-semantic-review`, `serving-governance-review`

- [ ] **Step 1: Run `python3 scripts/lint_graph.py` on the updated survey mainline**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Run `ontology-semantic-review` on the survey mainline pages**

Review this exact set:
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- `wiki/scenarios/复杂产品设计.md`
- `wiki/tasks/engineering-design-knowledge-management.md`
- related `concept_links.md`, `paper_method_links.md`, `task_method_map.md`, `evidence_index.md`, `provenance_links.md`

Expected: no framework/survey ontology-layer confusion and no relation-placement errors.

- [ ] **Step 3: Run `serving-governance-review` on the same survey mainline pages**

Expected: the review can now judge these pages against an explicit serving target shape instead of flagging template ambiguity.

- [ ] **Step 4: If a minimal fix is required by either review, apply only that fix and rerun lint**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 7: Final verification and verdict upgrade

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Re-evaluate the second dry-run verdict against the updated template state**

Confirm whether the survey dry-run now satisfies:

```text
- page-projection-sync has explicit target shapes
- the five representative survey-mainline pages can be synchronized without template ambiguity
- lint passes
- ontology-semantic-review and serving-governance-review can evaluate the resulting pages without treating template shape as missing
```

- [ ] **Step 2: Produce one explicit survey dry-run verdict**

Use one of:
- `pipeline-ran-end-to-end`
- `pipeline-ran-with-manual-bridges`
- `pipeline-did-not-run-cleanly`

Expected: the survey mainline should now be able to reach `pipeline-ran-end-to-end`, unless a review finds a new concrete blocker.

- [ ] **Step 3: Do not auto-commit this work unless separately requested**

Run:

```bash
git status --short
```

Expected: working tree remains available for user review.
