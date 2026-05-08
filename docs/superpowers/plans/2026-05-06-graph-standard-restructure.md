# Graph Standard Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `ontology/graph-standard.md` into a cleaner normative standard that keeps ontology/page/governance contracts while removing duplicated workflow and over-detailed consumption guidance.

**Architecture:** Treat this as a document-boundary refactor, not an ontology rewrite. Rebuild the file around six stable sections, move process/routing details out of the standard, and reduce repeated survey/framework and serving-surface explanations by replacing them with short principle statements or cross-references.

**Tech Stack:** Markdown, Obsidian wikilinks, grep, `python3 scripts/lint_graph.py`

---

## File Map

- **Modify:** `ontology/graph-standard.md`
  - Project-level normative source for ontology rules, page contracts, formal relation ledger contracts, serving/governance acceptance criteria, and quality floor rules.
- **Reference only:** `CLAUDE.md`
  - Holds workflow routing, compile-chain sequencing, interruption conditions, and operational reading paths that should not be duplicated into `graph-standard.md`.
- **Reference only:** `ontology/index.md`
  - Holds navigation entrypoints for the standard, relation ledgers, and object-domain indexes.
- **Create:** `docs/superpowers/plans/2026-05-06-graph-standard-restructure.md`
  - This implementation plan.

---

### Task 1: Rename the document and add a positioning section

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Verify the current title and absence of the new positioning section**

Run:
```bash
grep -n "^# " ontology/graph-standard.md && grep -n "^## 1\. 文档定位" ontology/graph-standard.md || true
```
Expected:
- First command prints `# Graph Standard`
- Second command prints nothing

- [ ] **Step 2: Replace the title and insert the positioning section immediately after it**

Apply this exact markdown at the top of `ontology/graph-standard.md`:
```md
# ResearchKB Graph Standard

## 1. 文档定位
- 本文是 ResearchKB 的规范真源，用于定义节点、关系、证据、投影与治理验收标准。
- 执行流程、编译链顺序与运行路由由 `CLAUDE.md` 负责，不在本文重复展开。
- 系统级与对象域导航入口由 `ontology/index.md` 及各对象域 index 承担；本文只保留少量“如何消费规范”的原则性说明。
```

- [ ] **Step 3: Verify the new header block is present**

Run:
```bash
grep -n "^# ResearchKB Graph Standard$" ontology/graph-standard.md && grep -n "^## 1\. 文档定位$" ontology/graph-standard.md
```
Expected:
- Both lines are found exactly once

- [ ] **Step 4: Commit the title and positioning update**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: add graph standard positioning"
```
Expected:
- A new commit is created successfully

---

### Task 2: Rebuild the top-level section skeleton

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Inspect the current top-level heading layout**

Run:
```bash
grep -n "^## " ontology/graph-standard.md
```
Expected:
- Existing `##` headings print in historical order, including mixed ontology, ledger, serving, and consumption sections

- [ ] **Step 2: Rewrite the top-level heading order to the six-section structure**

Reorganize the file so the `##` headings appear in this exact order:
```md
## 1. 文档定位
## 2. 本体基础
## 3. 对象页契约
## 4. 关系账本与证据契约
## 5. 服务层与治理契约
## 6. 质量底线与消费原则
```

Move existing content under those containers as follows:
```md
## 2. 本体基础
### 2.1 节点类型
### 2.2 survey / framework 建模公理
### 2.3 关系类型

## 3. 对象页契约
### 3.1 Frontmatter 受控字段
### 3.2 通用填写原则
### 3.3 Paper
### 3.4 Method
### 3.5 Concept
### 3.6 Task
### 3.7 Benchmark
### 3.8 Scenario
### 3.9 Evidence

## 4. 关系账本与证据契约
### 4.1 实例边层
### 4.2 实例边记录格式
### 4.3 关系文件分工
### 4.4 概念网络补充边标签
### 4.5 实例边维护规则
### 4.6 冗余 cache 判废规则
### 4.7 证据要求

## 5. 服务层与治理契约
### 5.1 治理真源层与服务层
### 5.2 全类型服务层投影规则
### 5.3 Formal relations 区块规范
### 5.4 Serving 迁移状态
### 5.5 服务层治理校验要求
### 5.6 三层治理出口

## 6. 质量底线与消费原则
### 6.1 节点判定规则
### 6.2 论文类型与豁免规则
### 6.3 最小链接义务
### 6.4 链接质量要求
### 6.5 问答消费规则
### 6.6 Index 导航投影层
### 6.7 关系索引
```

- [ ] **Step 3: Verify the new top-level order**

Run:
```bash
grep -n "^## " ontology/graph-standard.md
```
Expected:
- Only the six top-level sections appear, in the exact order shown above

- [ ] **Step 4: Commit the section skeleton reorganization**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: reorganize graph standard sections"
```
Expected:
- A new commit is created successfully

---

### Task 3: Normalize subsection headings under ontology and entity-page contracts

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Confirm the subsection names still use the old mixed heading style**

Run:
```bash
grep -n "^### " ontology/graph-standard.md
```
Expected:
- Existing `###` headings include old labels such as `### Paper`, `### Method`, `### Concept`, and contract-related headings without section numbering

- [ ] **Step 2: Rename subsection headings to match the new grouped structure without changing their normative content**

Use these exact subsection headings under the new containers:
```md
## 2. 本体基础
### 2.1 节点类型
### 2.2 survey / framework 建模公理
### 2.3 关系类型

## 3. 对象页契约
### 3.1 Frontmatter 受控字段
### 3.2 通用填写原则
### 3.3 Paper
### 3.4 Method
### 3.5 Concept
### 3.6 Task
### 3.7 Benchmark
### 3.8 Scenario
### 3.9 Evidence
```

Move the existing bodies for these sections under the renamed headings unchanged except where later tasks explicitly deduplicate wording.

- [ ] **Step 3: Verify the ontology and entity-page subsection headings are in place**

Run:
```bash
grep -n "^### 2\.\|^### 3\." ontology/graph-standard.md
```
Expected:
- The command prints subsection headings from `### 2.1` through `### 3.9`

- [ ] **Step 4: Commit the subsection-heading normalization**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: normalize graph standard subsection headings"
```
Expected:
- A new commit is created successfully

---

### Task 4: Move relation-ledger and evidence sections under a single contract group

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Verify the relation/evidence contract sections are still scattered**

Run:
```bash
grep -n "^## .*实例边\|^## .*关系文件分工\|^## .*概念网络补充边标签\|^## .*冗余 cache 判废规则\|^## .*证据要求" ontology/graph-standard.md
```
Expected:
- The command prints these sections in a scattered or transitional order

- [ ] **Step 2: Group the relation-ledger and evidence sections under `## 4. 关系账本与证据契约`**

Ensure the following subsection sequence appears contiguously:
```md
## 4. 关系账本与证据契约
### 4.1 实例边层
### 4.2 实例边记录格式
### 4.3 关系文件分工
### 4.4 概念网络补充边标签
### 4.5 实例边维护规则
### 4.6 冗余 cache 判废规则
### 4.7 证据要求
```

Move the existing bodies for:
- instance edge layer
- canonical record format
- relation file ownership
- concept-network supplemental labels
- maintenance rules
- cache retirement rules
- evidence requirements

without changing their rule meaning.

- [ ] **Step 3: Verify the contract group is contiguous**

Run:
```bash
grep -n "^## 4\.\|^### 4\." ontology/graph-standard.md
```
Expected:
- The output shows `## 4. 关系账本与证据契约` followed by `### 4.1` through `### 4.7` in order

- [ ] **Step 4: Commit the relation/evidence regrouping**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: regroup ledger and evidence contracts"
```
Expected:
- A new commit is created successfully

---

### Task 5: Move serving and governance rules into a dedicated contract group

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Inspect the current serving-related sections**

Run:
```bash
grep -n "^## .*治理真源层与服务层\|^## .*全类型服务层投影规则\|^## .*Formal relations 区块规范\|^## .*Serving 迁移状态\|^## .*服务层治理校验要求\|^## .*三层治理出口" ontology/graph-standard.md
```
Expected:
- Serving-related sections print, but may not yet be grouped as one dedicated contract block

- [ ] **Step 2: Group them under `## 5. 服务层与治理契约`**

Ensure this exact subsection order:
```md
## 5. 服务层与治理契约
### 5.1 治理真源层与服务层
### 5.2 全类型服务层投影规则
### 5.3 Formal relations 区块规范
### 5.4 Serving 迁移状态
### 5.5 服务层治理校验要求
### 5.6 三层治理出口
```

Move the current bodies under these numbered subsections. Do not change the rule meaning in:
- frontmatter-as-derived summary rules
- `Formal relations` canonical format rules
- serving-ready / partial / legacy definitions
- governance validation requirements

- [ ] **Step 3: Verify the serving/governance subsection order**

Run:
```bash
grep -n "^## 5\.\|^### 5\." ontology/graph-standard.md
```
Expected:
- The output shows `## 5. 服务层与治理契约` followed by `### 5.1` through `### 5.6`

- [ ] **Step 4: Commit the serving/governance regrouping**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: regroup serving governance contracts"
```
Expected:
- A new commit is created successfully

---

### Task 6: Move quality-floor content into the final principles section

**Files:**
- Modify: `ontology/graph-standard.md`
- Reference: `CLAUDE.md`
- Reference: `ontology/index.md`

- [ ] **Step 1: Inspect the current quality-floor and consumer-facing sections**

Run:
```bash
grep -n "^## .*节点判定规则\|^## .*论文类型与豁免规则\|^## .*最小链接义务\|^## .*链接质量要求\|^## .*问答消费规则\|^## .*Index 导航投影层\|^## .*关系索引" ontology/graph-standard.md
```
Expected:
- The listed sections print, possibly mixed with older wording and routing detail

- [ ] **Step 2: Group these sections under `## 6. 质量底线与消费原则`**

Use this exact structure:
```md
## 6. 质量底线与消费原则
### 6.1 节点判定规则
### 6.2 论文类型与豁免规则
### 6.3 最小链接义务
### 6.4 链接质量要求
### 6.5 问答消费规则
### 6.6 Index 导航投影层
### 6.7 关系索引
```

Keep the quality-floor rules intact. Later tasks will compress the two principle sections and remove repeated classification wording.

- [ ] **Step 3: Verify the final grouped section exists**

Run:
```bash
grep -n "^## 6\.\|^### 6\." ontology/graph-standard.md
```
Expected:
- The output shows `## 6. 质量底线与消费原则` followed by `### 6.1` through `### 6.7`

- [ ] **Step 4: Commit the quality/principles regrouping**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: regroup graph standard quality principles"
```
Expected:
- A new commit is created successfully

---

### Task 7: Compress duplicated serving-surface and consumption guidance

**Files:**
- Modify: `ontology/graph-standard.md`
- Reference: `CLAUDE.md`
- Reference: `ontology/index.md`

- [ ] **Step 1: Verify the current repeated truth-source and consumption prose**

Run:
```bash
grep -n "默认问答\|默认读取\|治理.*账本\|服务层\|导航投影层" ontology/graph-standard.md
```
Expected:
- Multiple lines appear across the instance-edge, serving-layer, and consumption sections describing similar ideas

- [ ] **Step 2: Replace the three principle sections with shorter, non-operational wording**

Use this wording for the instance-edge principle block:
```md
### 4.1 实例边层
- 实例边（instance edge）是两个具体知识节点之间的显式关系记录，不等同于关系类型定义本身。
- `ontology/relations/` 是正式维护实例边账本的唯一治理真源。
- 治理通过后，对象页中的 `## Formal relations` 作为默认服务读取面；自然语言说明与 `[[wikilink]]` 仅作辅助，不替代正式关系账本。
```

Use this wording for the serving-layer boundary block:
```md
### 5.1 治理真源层与服务层
- `ontology/relations/` 作为正式实例边的治理真源，用于治理、修复、审计与 formal graph truth 核对。
- 治理通过后的对象页与 Evidence 页共同构成默认知识服务层；其中对象页承载正式关系读取面，Evidence 页承载机制、实验、引用与 provenance 核验。
```

Use this wording for the knowledge-consumption principles:
```md
### 6.5 问答消费规则
- 正式知识问答默认基于治理后的对象页及其 `## Formal relations` 展开，而不是直接把 `ontology/relations/` 作为默认读取起点。
- 若需核验机制、实验、引用、基线或 provenance，再下钻对应 Evidence 页。
- `ontology/relations/` 主要用于治理、修复与审计场景。
```

Use this wording for the index-projection principles:
```md
### 6.6 Index 导航投影层
- `ontology/entities/*/index.md` 与其他显式受管导航页是导航投影层，不是 formal relation truth source。
- 页面“可被 index 收录”和“可作为默认 serving 入口暴露”是两个不同状态。
```

Remove from `graph-standard.md` any wording that explicitly assigns managed-block maintenance, compile routing, or validator ownership to specific skills or tools.

- [ ] **Step 3: Verify the compressed wording is in place and the old operational phrases are gone**

Run:
```bash
grep -n "^### 4\.1\|^### 5\.1\|^### 6\.5\|^### 6\.6" ontology/graph-standard.md && ! grep -n "index-sync\|CLAUDE\.md 负责系统级导航\|问答运行时默认先读治理后的对象页" ontology/graph-standard.md
```
Expected:
- The four subsection headings print
- The negative grep succeeds because those older operational phrases are no longer present

- [ ] **Step 4: Commit the compressed principle sections**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: compress graph standard consumption principles"
```
Expected:
- A new commit is created successfully

---

### Task 8: Remove repeated classification prose and duplicate edge-label semantics

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Verify the current repeated survey/framework and edge-label explanations**

Run:
```bash
grep -n "survey 论文属于 Paper 层\|分层框架、角色划分或 taxonomy\|`supports`：概念或框架\|`depends_on`：概念依赖" ontology/graph-standard.md
```
Expected:
- The repeated classification and repeated edge-label definitions are found

- [ ] **Step 2: Replace the repeated paper-type classification prose with a cross-reference and trim concept-network labels to scope rules only**

In `### 6.2 论文类型与豁免规则`, replace the two repeated classification bullets with this single bullet:
```md
- survey / framework / taxonomy 的节点归类与 `proposes` 落点，遵循前文“survey / framework 建模公理”；如某篇论文不适合完整满足默认最小链接义务，应在页面或缓存中显式写明缺省原因，避免形式化凑数。
```

In `### 4.4 概念网络补充边标签`, use this exact content:
```md
### 4.4 概念网络补充边标签
- `supports`、`depends_on` 的语义见前文“关系类型”。
- 上述标签当前仅可在 `ontology/relations/concept_links.md` 中使用；若要扩展到其他关系文件，必须先在 `### 4.3 关系文件分工` 完成登记。
```

- [ ] **Step 3: Verify the duplicated wording is removed**

Run:
```bash
grep -n "遵循前文“survey / framework 建模公理”\|`supports`、`depends_on` 的语义见前文“关系类型”" ontology/graph-standard.md && ! grep -n "survey 论文属于 Paper 层\|分层框架、角色划分或 taxonomy\|`supports`：概念或框架\|`depends_on`：概念依赖" ontology/graph-standard.md
```
Expected:
- The new cross-reference lines are found
- The old duplicated prose is gone

- [ ] **Step 4: Commit the deduplication changes**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: deduplicate graph standard modeling rules"
```
Expected:
- A new commit is created successfully

---

### Task 9: Run final verification and consistency checks

**Files:**
- Modify: `ontology/graph-standard.md` if the checks reveal issues

- [ ] **Step 1: Verify the final heading skeleton and key principles**

Run:
```bash
grep -n "^# ResearchKB Graph Standard$\|^## 1\. 文档定位$\|^## 2\. 本体基础$\|^## 3\. 对象页契约$\|^## 4\. 关系账本与证据契约$\|^## 5\. 服务层与治理契约$\|^## 6\. 质量底线与消费原则$" ontology/graph-standard.md
```
Expected:
- The title and all six top-level sections print exactly once

- [ ] **Step 2: Run graph lint to catch structural breakage**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected:
- The command completes successfully without new structural failures caused by the document reorganization

- [ ] **Step 3: Search for process content that should no longer live in the standard**

Run:
```bash
! grep -n "paper-ingest\|relation-reconciliation\|page-projection-sync\|index-sync\|serving-governance-review\|ontology-semantic-review" ontology/graph-standard.md
```
Expected:
- The command succeeds because process sequencing and skill-role duplication are no longer present in the standard, except where governance gate names remain in `### 5.6 三层治理出口`
```

If Step 3 fails only because `### 5.6 三层治理出口` still lists the three governance gates, rerun with this narrower check instead:
```bash
! grep -n "单篇论文编译链\|paper-ingest 负责\|relation-reconciliation 负责\|page-projection-sync 负责\|index-sync 负责" ontology/graph-standard.md
```
Expected:
- The narrower check succeeds

- [ ] **Step 4: Fix any lint or structure issues uncovered by the checks**

If any issue appears, make the smallest possible markdown edit to resolve it, then rerun:
```bash
python3 scripts/lint_graph.py && grep -n "^## " ontology/graph-standard.md
```
Expected:
- Lint passes and the heading layout remains intact

- [ ] **Step 5: Commit the final verified restructure**

Run:
```bash
git add ontology/graph-standard.md && git commit -m "docs: finalize graph standard restructure"
```
Expected:
- A final commit is created successfully
