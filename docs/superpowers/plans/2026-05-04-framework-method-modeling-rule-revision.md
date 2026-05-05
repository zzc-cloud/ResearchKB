# Framework/Method Modeling Rule Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `wiki/ontology/graph-standard.md` so framework / taxonomy keeps a default Concept landing path while explicitly allowing method-like frameworks to be modeled as Method when their dominant semantics are procedural, evaluative, or evolutionary.

**Architecture:** This is a single-file ontology wording change. The implementation updates three tightly-coupled sections in `wiki/ontology/graph-standard.md` together so the modeling axiom, Concept guidance, and survey/framework paper-type rules all express the same default-plus-exception rule.

**Tech Stack:** Markdown, `rg`, `python3 scripts/lint_graph.py`, git

---

## File map

- Modify: `wiki/ontology/graph-standard.md`
  - Owns the ontology authority text for modeling axioms, node-type guidance, relation rules, and link obligations.
- Verify: `scripts/lint_graph.py`
  - Structural graph validator used to confirm the ontology doc edit did not introduce repository-level governance regressions.

### Task 1: Revise the modeling axiom section

**Files:**
- Modify: `wiki/ontology/graph-standard.md:19-22`
- Verify: `wiki/ontology/graph-standard.md:19-23`

- [ ] **Step 1: Confirm the current axiom wording is still present**

Run:
```bash
rg -n "## survey / framework 建模公理|Framework 是 Concept 层知识产物|\[\[Paper\]\] --proposes--> \[\[Concept\]\]" wiki/ontology/graph-standard.md
```

Expected:
- a match for the section header
- a match for the absolute `Framework 是 Concept 层知识产物` line
- a match for the `Paper --proposes--> [[Concept]]` line

- [ ] **Step 2: Replace the axiom block with the approved default-plus-semantic-test wording**

Replace the current block:
```md
## survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task，也不上提为 Concept。
- Framework 是 Concept 层知识产物：默认落为 `concept_kind: framework`，不作为独立节点类型，也不写成 Method。
- 当论文的核心贡献是 framework / taxonomy 型知识结构时，应使用 `[[Paper]] --proposes--> [[Concept]]` 建模：Paper 表示论文载体，Concept 表示被提出的知识产物。
```

with:
```md
## survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task，也不上提为 Concept。
- Framework / taxonomy 若主要承担知识组织、分类、分层或解释框架语义，默认落为 Concept；其中 framework 可使用 `concept_kind: framework` 标记。
- Framework 若主要承担可执行方法流程、明确实验对比或方法演化语义，则应按 Method 处理，而不是机械落为 Concept。
- 当论文的核心贡献是 framework / taxonomy 型知识结构时，应根据其主要语义选择 `[[Paper]] --proposes--> [[Concept]]` 或 `[[Paper]] --proposes--> [[Method]]`：Paper 表示论文载体，Concept / Method 表示被提出的核心知识产物。
```

- [ ] **Step 3: Verify the new axiom wording is present and the old absolute rule is gone**

Run:
```bash
rg -n "Framework / taxonomy 若主要承担知识组织|Framework 若主要承担可执行方法流程|\[\[Paper\]\] --proposes--> \[\[Concept\]\].*\[\[Method\]\]" wiki/ontology/graph-standard.md && ! rg -n "Framework 是 Concept 层知识产物：默认落为 `concept_kind: framework`，不作为独立节点类型，也不写成 Method。" wiki/ontology/graph-standard.md
```

Expected:
- the three new matches are found
- the old absolute line has no match

- [ ] **Step 4: Commit the axiom update**

Run:
```bash
git add wiki/ontology/graph-standard.md && git commit -m "$(cat <<'EOF'
docs: revise framework modeling axiom

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected:
- a new commit is created containing only the approved axiom wording change so far

### Task 2: Revise the Concept guidance to match the axiom

**Files:**
- Modify: `wiki/ontology/graph-standard.md:194-199`
- Verify: `wiki/ontology/graph-standard.md:194-200`

- [ ] **Step 1: Confirm the current Concept framework wording is still present**

Run:
```bash
rg -n "concept_kind.*framework.*taxonomy|不要把 framework 落为 Method|框架型 / taxonomy 型概念落库" wiki/ontology/graph-standard.md
```

Expected:
- a match for the current `concept_kind` line
- a match for the `不要把 framework 落为 Method` line
- a match for the current concept landing rule

- [ ] **Step 2: Replace the Concept guidance block with the aligned wording**

Replace the current block:
```md
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- Framework 属于 Concept 层知识节点；默认使用 `concept_kind: framework`，不要把 framework 落为 Method。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库，而不是再拆分独立节点类型。
```

with:
```md
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- Framework 若主要承担知识组织、分类、分层或解释框架语义，默认使用 `concept_kind: framework` 作为 Concept 落库；若主要承担可执行方法流程、明确实验对比或方法演化语义，则应按 Method 处理。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库；但若其主语义是方法流程与评测对象，则可按 Method 建模，而不是机械归入 Concept。
```

- [ ] **Step 3: Verify the Concept section now uses the same semantic split as the axiom**

Run:
```bash
rg -n "默认使用 `concept_kind: framework` 作为 Concept 落库|则应按 Method 处理|而不是机械归入 Concept" wiki/ontology/graph-standard.md
```

Expected:
- all three new phrases match in the Concept section

- [ ] **Step 4: Commit the Concept guidance update**

Run:
```bash
git add wiki/ontology/graph-standard.md && git commit -m "$(cat <<'EOF'
docs: align framework concept guidance

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected:
- a new commit is created with the Concept-section alignment change

### Task 3: Revise the survey/framework paper-type rules

**Files:**
- Modify: `wiki/ontology/graph-standard.md:463-465`
- Verify: `wiki/ontology/graph-standard.md:463-465`

- [ ] **Step 1: Confirm the current survey/framework paper-type wording is still present**

Run:
```bash
rg -n "survey / benchmark 论文|应落为 Concept 层节点|优先把核心知识落为 Concept 节点中的框架型 / taxonomy 型概念" wiki/ontology/graph-standard.md
```

Expected:
- a match for the survey / benchmark line
- a match for the current Concept-only paper-type line
- a match for the current framework/taxonomy preference line

- [ ] **Step 2: Replace the paper-type block with the approved wording**

Replace the current block:
```md
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- survey 论文属于 Paper 层；若论文的核心知识产物是 framework / taxonomy，则应落为 Concept 层节点，并通过 `proposes` 与论文连接，而不是误写为 Task 或 Method。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先把核心知识落为 Concept 节点中的框架型 / taxonomy 型概念，并连接到 scenario / task / synthesis，而不是再拆分独立节点类型。
```

with:
```md
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- survey 论文属于 Paper 层；若论文的核心知识产物是 framework / taxonomy，则应按其主要语义落为 Concept 或 Method，并通过 `proposes` 与论文连接，而不是误写为 Task 或独立节点类型。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，若其主要承担知识组织、分类或解释语义，优先把核心知识落为 Concept 节点中的框架型 / taxonomy 型概念；若其主要承担可执行方法流程、实验对比或方法演化语义，则可按 Method 建模。
```

- [ ] **Step 3: Verify the paper-type rules no longer contradict the new axiom**

Run:
```bash
rg -n "应按其主要语义落为 Concept 或 Method|若其主要承担知识组织、分类或解释语义|若其主要承担可执行方法流程、实验对比或方法演化语义" wiki/ontology/graph-standard.md
```

Expected:
- all three new phrases match in the paper-type rules section

- [ ] **Step 4: Commit the paper-type rule update**

Run:
```bash
git add wiki/ontology/graph-standard.md && git commit -m "$(cat <<'EOF'
docs: align survey framework paper typing

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected:
- a new commit is created with the paper-type rule alignment change

### Task 4: Run repository verification and make the final integration commit

**Files:**
- Verify: `wiki/ontology/graph-standard.md`
- Verify: `scripts/lint_graph.py`

- [ ] **Step 1: Run a focused consistency grep across all three edited sections**

Run:
```bash
rg -n "可执行方法流程|实验对比|方法演化语义|Concept 或 Method|机械归入 Concept" wiki/ontology/graph-standard.md
```

Expected:
- matches appear in the modeling axiom section
- matches appear in the Concept section
- matches appear in the paper-type rules section

- [ ] **Step 2: Run the graph lint to ensure the repository still passes governance checks**

Run:
```bash
python3 scripts/lint_graph.py
```

Expected:
- exit status 0
- no new lint failures introduced by the ontology wording change

- [ ] **Step 3: Review the net diff before the final commit**

Run:
```bash
git diff -- wiki/ontology/graph-standard.md
```

Expected:
- the diff only shows the approved semantic-split wording in the three targeted sections
- no unrelated ontology content changed

- [ ] **Step 4: Create the final integration commit if the prior steps were executed without per-task commits**

Run:
```bash
git add wiki/ontology/graph-standard.md && git commit -m "$(cat <<'EOF'
docs: refine framework and method modeling rules

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected:
- a clean final commit exists containing the ontology wording revision

- [ ] **Step 5: Verify the working tree is clean**

Run:
```bash
git status --short
```

Expected:
- no staged or unstaged changes for `wiki/ontology/graph-standard.md`
- only unrelated pre-existing repo changes remain, if any

## Spec coverage check

- Modeling axiom update: covered by Task 1.
- Concept guidance alignment: covered by Task 2.
- Paper-type rule alignment: covered by Task 3.
- Internal consistency verification and repo validation: covered by Task 4.

## Notes for the implementer

- Do not introduce a new `Framework` node type.
- Do not change relation ownership or serving-ready projection rules.
- Keep the change limited to the three approved sections unless a contradiction is discovered during implementation.
- If `python3 scripts/lint_graph.py` fails for unrelated pre-existing reasons, record the failure and stop before claiming the ontology revision is complete.
