# Survey/Framework Ontology Clarification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the ontology state unambiguously that survey papers live in the Paper layer and framework knowledge products live in the Concept layer.

**Architecture:** Keep the change minimal and normative. Tighten the authoritative ontology wording in `wiki/ontology/graph-standard.md`, then align the `proposes` ledger note in `wiki/relations/paper_method_links.md` so future ingest and governance work read the same rule from both the ontology and the relation source. Existing representative pages already follow the intended modeling, so verify them rather than rewriting them.

**Tech Stack:** Markdown knowledge pages, relation ledgers in `wiki/relations/`, `rg`, and `python3 scripts/lint_graph.py`.

---

## File map

### Normative ontology source
- Modify: `wiki/ontology/graph-standard.md`
  - Clarify that survey is always a Paper-layer node.
  - Clarify that framework is a Concept-layer knowledge product using `concept_kind: framework`.
  - Remove wording that can be misread as "framework is a Paper type".
  - Tighten the `proposes` description so `Paper -> Concept` is the explicit path for framework outputs.

### Companion relation-ledger note
- Modify: `wiki/relations/paper_method_links.md`
  - Restate that `proposes` supports `Paper -> Concept` for framework knowledge products and that framework should not be modeled as Method.

### Verification surface
- Verify only: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Verify only: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Test: `python3 scripts/lint_graph.py`
- Test: `rg -n "survey|framework|concept_kind|proposes" wiki/ontology/graph-standard.md wiki/relations/paper_method_links.md`

---

### Task 1: Tighten the authoritative ontology wording

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`
- Test: `rg -n "Survey|Framework|survey|framework|concept_kind|proposes" wiki/ontology/graph-standard.md`

- [ ] **Step 1: Add an explicit modeling-axioms block near the node-type definitions**

In `wiki/ontology/graph-standard.md`, immediately after the `## 节点类型` list, insert:

```markdown
## survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task，也不上提为 Concept。
- Framework 是 Concept 层知识产物：默认落为 `concept_kind: framework`，不作为独立节点类型，也不写成 Method。
- 当论文的核心贡献是 framework / taxonomy 型知识结构时，应使用 `[[Paper]] --proposes--> [[Concept]]` 建模：Paper 表示论文载体，Concept 表示被提出的知识产物。
```

- [ ] **Step 2: Replace the ambiguous Paper-side heading and bullets**

In `wiki/ontology/graph-standard.md`, replace this block:

```markdown
survey / framework 型 Paper 补充规则：
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架 / 核心概念、相关任务、应用场景、关键结论、综述证据来源。
- 这类 Paper 的 `Formal relations` 重点为：`proposes`（到 framework / concept）、`uses_concept`、`targets_task`、`cites`、`supported_by`。
- 若无统一 benchmark，必须显式以 `relation_exemptions` 说明 `evaluated_on` 按规范豁免，而不是伪造 benchmark formal edge。
```

with:

```markdown
survey Paper / framework-taxonomy 核心贡献论文补充规则：
- Survey 始终作为 Paper 节点建模；不要把 survey 误写为 Task 或 Concept。
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架 / 核心概念、相关任务、应用场景、关键结论、综述证据来源。
- 当论文提出的主知识资产是 framework / taxonomy 时，Paper 仍是论文载体；对应知识产物优先落为 Concept 节点，并通过 `proposes` 连接。
- 这类 Paper 的 `Formal relations` 重点为：`proposes`（到 framework / concept）、`uses_concept`、`targets_task`、`cites`、`supported_by`。
- 若无统一 benchmark，必须显式以 `relation_exemptions` 说明 `evaluated_on` 按规范豁免，而不是伪造 benchmark formal edge。
```

- [ ] **Step 3: Make the Concept-side framework rule explicit**

In the `### Concept` section of `wiki/ontology/graph-standard.md`, replace this explanation block:

```markdown
说明：
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库，而不是再拆分独立节点类型。
- framework 型 Concept 补充规则：
  - 若 `concept_kind: framework`，页面应优先描述：框架定义、层级结构 / 组成部分、相关概念、相关场景、相关任务、相关论文、证据来源。
  - framework 型 Concept 的 `Formal relations` 重点为：incoming `proposes`、outgoing `uses_concept`、outgoing `applies_to`、outgoing / incoming `supports`、`supported_by`。
```

with:

```markdown
说明：
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- Framework 属于 Concept 层知识节点；默认使用 `concept_kind: framework`，不要把 framework 落为 Method。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库，而不是再拆分独立节点类型。
- framework 型 Concept 补充规则：
  - 若 `concept_kind: framework`，页面应优先描述：框架定义、层级结构 / 组成部分、相关概念、相关场景、相关任务、相关论文、证据来源。
  - framework 型 Concept 的 `Formal relations` 重点为：incoming `proposes`、outgoing `uses_concept`、outgoing `applies_to`、outgoing / incoming `supports`、`supported_by`。
```

- [ ] **Step 4: Tighten the `proposes` relation definition**

In `wiki/ontology/graph-standard.md`, replace this line:

```markdown
- `proposes`：`[[Paper]] --proposes--> [[Method|Concept]]`；表示论文首次提出或正式定义某方法，或提出 framework / taxonomy 型核心概念。
```

with:

```markdown
- `proposes`：`[[Paper]] --proposes--> [[Method|Concept]]`；表示论文首次提出或正式定义某方法，或提出 framework / taxonomy 型核心概念。Survey 保持为 Paper 层节点；framework / taxonomy 等核心知识产物优先作为 Concept 节点承接。
```

- [ ] **Step 5: Tighten the paper-type guidance near the exemption rules**

In the `## 论文类型与豁免规则` block of `wiki/ontology/graph-standard.md`, insert this bullet immediately after the existing `survey / benchmark 论文` bullet:

```markdown
- survey 论文属于 Paper 层；若论文的核心知识产物是 framework / taxonomy，则应落为 Concept 层节点，并通过 `proposes` 与论文连接，而不是误写为 Task 或 Method。
```

- [ ] **Step 6: Run the ontology verification commands**

Run:

```bash
python3 scripts/lint_graph.py && rg -n "survey|framework|concept_kind|proposes" wiki/ontology/graph-standard.md
```

Expected:
- `PASS: graph lint succeeded`
- `rg` output shows the new modeling-axiom text, the renamed Paper guidance heading, the explicit framework-as-Concept line, and the tightened `proposes` line.

- [ ] **Step 7: Commit the ontology clarification**

```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: clarify survey and framework ontology roles"
```

---

### Task 2: Align the `proposes` ledger note with the ontology

**Files:**
- Modify: `wiki/relations/paper_method_links.md`
- Test: `python3 scripts/lint_graph.py`
- Test: `rg -n "Paper -> Method|Paper -> Concept|framework|Method" wiki/relations/paper_method_links.md`

- [ ] **Step 1: Replace the note block with explicit Paper/Concept wording**

In `wiki/relations/paper_method_links.md`, replace this note block:

```markdown
## 说明
- 本页是 `proposes` 实例边的正式账本。
- `proposes` 允许 `Paper -> Method` 与 `Paper -> Concept`；后者主要用于 framework / taxonomy 型核心知识产物。
```

with:

```markdown
## 说明
- 本页是 `proposes` 实例边的正式账本。
- `proposes` 允许 `Paper -> Method` 与 `Paper -> Concept`。
- Survey 始终保留在 Paper 层；若论文提出的是 framework / taxonomy 型核心知识产物，应以 `Paper -> Concept` 记录，不把 framework 记成 Method。
```

- [ ] **Step 2: Verify the ledger wording and repository lint**

Run:

```bash
python3 scripts/lint_graph.py && rg -n "Paper -> Method|Paper -> Concept|framework|Method" wiki/relations/paper_method_links.md
```

Expected:
- `PASS: graph lint succeeded`
- `rg` output shows the new three-line note block, including the explicit `Survey 始终保留在 Paper 层` sentence.

- [ ] **Step 3: Commit the ledger-note clarification**

```bash
git add wiki/relations/paper_method_links.md
git commit -m "docs: align proposes ledger with ontology roles"
```

---

### Task 3: Verify that the representative survey/framework pages already conform

**Files:**
- Verify only: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Verify only: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Test: `python3 scripts/lint_graph.py`
- Test: `rg -n "research_role: \[survey\]|concept_kind: framework|--proposes-->" wiki/papers/A\ survey\ of\ large\ language\ model-augmented\ knowledge\ graphs\ for\ advanced\ complex\ product\ design.md wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`

- [ ] **Step 1: Confirm the survey page stays in the Paper layer**

Run:

```bash
rg -n "research_role: \[survey\]|title: A survey of large language model-augmented knowledge graphs for advanced complex product design" wiki/papers/A\ survey\ of\ large\ language\ model-augmented\ knowledge\ graphs\ for\ advanced\ complex\ product\ design.md
```

Expected:
- A hit for `research_role: [survey]`
- No file move and no node-type rewrite needed

- [ ] **Step 2: Confirm the framework page stays in the Concept layer**

Run:

```bash
rg -n "concept_kind: framework|title: 复杂产品设计中的LLM-KG协同框架" wiki/concepts/复杂产品设计中的LLM-KG协同框架.md
```

Expected:
- A hit for `concept_kind: framework`
- No rename to Method and no directory move needed

- [ ] **Step 3: Confirm the bridge relation is `Paper -> Concept`**

Run:

```bash
rg -n "A survey of large language model-augmented knowledge graphs for advanced complex product design.*--proposes-->.*复杂产品设计中的LLM-KG协同框架" wiki/papers/A\ survey\ of\ large\ language\ model-augmented\ knowledge\ graphs\ for\ advanced\ complex\ product\ design.md wiki/relations/paper_method_links.md
```

Expected:
- One hit in the paper page Formal relations
- One hit in `wiki/relations/paper_method_links.md`

- [ ] **Step 4: Run the final verification sweep**

Run:

```bash
python3 scripts/lint_graph.py && rg -n "survey|framework|concept_kind|proposes" wiki/ontology/graph-standard.md wiki/relations/paper_method_links.md
```

Expected:
- `PASS: graph lint succeeded`
- Updated ontology and ledger wording present
- No additional page edits required for the representative survey/framework pair

- [ ] **Step 5: Commit the verification checkpoint**

```bash
git commit --allow-empty -m "docs: verify survey and framework modeling examples"
```

---

## Self-review

### Spec coverage
- Requirement `survey 是 Paper 层` is covered in Task 1 Step 1, Step 2, and Task 3 Step 1.
- Requirement `framework 是 Concept 层的知识产物` is covered in Task 1 Step 1, Step 3, Step 4, and Task 3 Step 2.
- Requirement `Paper 只是 framework 的提出者` is covered in Task 1 Step 1, Step 2, Step 4, Task 2 Step 1, and Task 3 Step 3.
- Requirement `在本项目中修正这两点` is covered by changing the authoritative ontology file plus the companion `proposes` ledger note, then verifying the representative pages already comply.

### Placeholder scan
- No `TODO`, `TBD`, or "implement later" placeholders remain.
- Every modification step includes the exact replacement text.
- Every verification step includes an exact command and expected result.

### Type consistency
- `survey` is consistently described as Paper-layer only.
- `framework` is consistently described as Concept-layer only via `concept_kind: framework`.
- The bridge relation is consistently `[[Paper]] --proposes--> [[Concept]]`.

Plan complete and saved to `docs/superpowers/plans/2026-05-04-survey-framework-ontology-clarification.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
