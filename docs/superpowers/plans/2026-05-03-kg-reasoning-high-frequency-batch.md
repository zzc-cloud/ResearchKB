# KG Reasoning High-Frequency Serving Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the highest-frequency next-hop KG reasoning nodes into serving-ready pages so the PathMind-centered QA graph stays inside governed serving surfaces more often.

**Architecture:** First expand the formal relation ledger where existing evidence already justifies missing edges needed by this batch. Then migrate the shared Concept/Task/Benchmark convergence nodes (`重要推理路径`, `kgqa`, `multi-hop-qa`, `CWQ`) before upgrading the three Method pages (`GCR`, `EPERM`, `ToG`) and their corresponding Paper pages. Verify each step with structure lint, then run ontology-semantic-review and serving-governance-review over the whole batch.

**Tech Stack:** Markdown knowledge pages, Python 3 (`scripts/lint_graph.py`), existing relation-ledger files under `wiki/relations/`, serving-governance-review skill, ontology-semantic-review skill.

---

## File map

### Relation-ledger files
- Modify: `wiki/relations/task_method_map.md`
  - Add any missing `targets_task` edges needed by the batch.
- Modify: `wiki/relations/benchmark_links.md`
  - Add any missing `evaluated_on` edges for `CWQ` batch completeness.
- Modify: `wiki/relations/concept_links.md`
  - Add any missing `uses_concept`, `supports`, or `applies_to` edges required by migrated pages.
- Modify: `wiki/relations/evidence_index.md`
  - Add any missing `supported_by` edges needed by new serving projections.
- Modify: `wiki/relations/paper_method_links.md`
  - Confirm or extend `proposes` edges for the three paper/method pairs if needed.

### Shared convergence pages
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/benchmarks/CWQ.md`

### Method pages
- Modify: `wiki/methods/GCR.md`
- Modify: `wiki/methods/EPERM.md`
- Modify: `wiki/methods/ToG.md`

### Paper pages
- Modify: `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- Modify: `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- Modify: `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `serving-governance-review`
- Test: `ontology-semantic-review`

---

### Task 1: Patch the relation ledger for batch-required edges

**Files:**
- Modify: `wiki/relations/task_method_map.md`
- Modify: `wiki/relations/benchmark_links.md`
- Modify: `wiki/relations/concept_links.md`
- Modify: `wiki/relations/evidence_index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add the missing `EPERM --targets_task--> multi-hop-qa` edge**

In `wiki/relations/task_method_map.md`, insert this block immediately after the existing `[[GCR]] --targets_task--> [[multi-hop-qa]]` edge:

```markdown
- `[[EPERM]] --targets_task--> [[multi-hop-qa]]`
  - reason: EPERM 面向多跳问答中的证据路径增强推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
```

- [ ] **Step 2: Add missing `evaluated_on` edges for `CWQ` batch completeness**

In `wiki/relations/benchmark_links.md`, append these edges after the existing `[[PathMind]] --evaluated_on--> [[CWQ]]` block:

```markdown
- `[[GCR]] --evaluated_on--> [[CWQ]]`
  - reason: GCR 在论文对比实验中使用 CWQ 作为评测基准。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §3
- `[[EPERM]] --evaluated_on--> [[CWQ]]`
  - reason: EPERM 在论文对比实验中使用 CWQ 作为评测基准。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §3
- `[[ToG]] --evaluated_on--> [[CWQ]]`
  - reason: ToG 在论文对比实验中使用 CWQ 作为评测基准。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §7
```

- [ ] **Step 3: Add concept/task/scenario edges needed by `重要推理路径` and task pages**

In `wiki/relations/concept_links.md`, insert these edges after the existing `[[重要推理路径]] --supports--> [[kgqa]]` edge:

```markdown
- `[[重要推理路径]] --supports--> [[multi-hop-qa]]`
  - reason: 重要推理路径是多跳问答中的高价值证据链单元。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[重要推理路径]] --supports--> [[知识图谱推理问答]]`
  - reason: 重要推理路径为知识图谱推理问答场景提供关键证据链。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
```

- [ ] **Step 4: Add supported-by edges required for the new high-frequency nodes**

In `wiki/relations/evidence_index.md`, insert these edges after the existing `[[知识图谱推理问答]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]` block if they do not yet exist:

```markdown
- `[[重要推理路径]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - reason: 重要推理路径概念与作用由 sections 缓存支撑。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §6
- `[[kgqa]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - reason: KGQA 任务定位由 sections 缓存支撑。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §4、§7
- `[[multi-hop-qa]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - reason: multi-hop-qa 任务定位由 sections 缓存支撑。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §4、§7
- `[[CWQ]] --supported_by--> [[intermediate/papers/PathMind.experiments|PathMind.experiments]]`
  - reason: CWQ 基准上的实验结果由 experiments 缓存支撑。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §1–3
```

- [ ] **Step 5: Run lint to verify the ledger still passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the ledger patch**

```bash
git add wiki/relations/task_method_map.md wiki/relations/benchmark_links.md wiki/relations/concept_links.md wiki/relations/evidence_index.md
git commit -m "docs: patch relation ledger for high-frequency serving batch"
```

---

### Task 2: Migrate the shared Concept node `重要推理路径`

**Files:**
- Modify: `wiki/concepts/重要推理路径.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the tail of `wiki/concepts/重要推理路径.md` with serving-ready sections**

Replace everything from `## 与其他概念的关系` onward with:

```markdown
## 与其他概念的关系
- [[路径优先化]]：识别重要推理路径的核心机制。
- [[knowledge-graph-reasoning]]：在该任务中承担关键证据链的语义角色。

## 相关方法
- [[PathMind]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关任务 / 场景
- 任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 场景：[[知识图谱推理问答]]

## 证据来源
- 概念关系：[[concept_links]]
- 结构化证据：[[intermediate/papers/PathMind.sections|PathMind.sections]]

## Formal relations
### Outgoing
- `[[重要推理路径]] --supports--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[重要推理路径]] --supports--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[重要推理路径]] --supports--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[重要推理路径]] --supports--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]

### Incoming
- `[[PathMind]] --uses_concept--> [[重要推理路径]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```

- [ ] **Step 2: Run lint to verify the Concept migration passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Concept migration**

```bash
git add wiki/concepts/重要推理路径.md
git commit -m "docs: migrate important reasoning paths concept"
```

---

### Task 3: Migrate the Task pages `kgqa` and `multi-hop-qa`

**Files:**
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the tail of `wiki/tasks/kgqa.md` with serving-ready task sections**

Replace everything from `## 相关方法` onward with:

```markdown
## 相关方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[EPERM]]

## 相关概念
- [[路径优先化]]
- [[重要推理路径]]

## 相关场景
- [[知识图谱推理问答]]

## 相关 benchmark
- [[WebQSP]]
- [[CWQ]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 证据来源 / 关系索引
- 方法映射：[[task_method_map]]
- 证据索引：[[evidence_index]]
- 结构化证据：[[intermediate/papers/PathMind.sections|PathMind.sections]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[重要推理路径]] --supports--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```

- [ ] **Step 2: Replace the tail of `wiki/tasks/multi-hop-qa.md` with serving-ready task sections**

Replace everything from `## 相关方法` onward with:

```markdown
## 相关方法
- [[PathMind]]
- [[RoG]]
- [[ToG]]
- [[GCR]]
- [[EPERM]]

## 相关概念
- [[路径优先化]]
- [[重要推理路径]]

## 相关场景
- [[知识图谱推理问答]]

## 相关 benchmark
- [[WebQSP]]
- [[CWQ]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]

## 证据来源 / 关系索引
- 方法映射：[[task_method_map]]
- 证据索引：[[evidence_index]]
- 结构化证据：[[intermediate/papers/PathMind.sections|PathMind.sections]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[重要推理路径]] --supports--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```

- [ ] **Step 3: Run lint to verify both Task migrations pass**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit the Task migrations**

```bash
git add wiki/tasks/kgqa.md wiki/tasks/multi-hop-qa.md
git commit -m "docs: migrate high-frequency task pages"
```

---

### Task 4: Migrate the Benchmark page `CWQ`

**Files:**
- Modify: `wiki/benchmarks/CWQ.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the tail of `wiki/benchmarks/CWQ.md` with serving-ready benchmark sections**

Replace everything from `## 相关任务` onward with:

```markdown
## 相关任务
- [[kgqa]]
- [[multi-hop-qa]]
- [[knowledge-graph-reasoning]]

## 被哪些方法 / 论文使用
- 方法：[[PathMind]]、[[GCR]]、[[EPERM]]、[[ToG]]
- 论文：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关场景
- [[知识图谱推理问答]]

## 证据来源
- [[evidence_index]]
- [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[EPERM]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[ToG]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
```

- [ ] **Step 2: Run lint to verify the Benchmark migration passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Benchmark migration**

```bash
git add wiki/benchmarks/CWQ.md
git commit -m "docs: migrate CWQ benchmark page"
```

---

### Task 5: Migrate the Method pages `GCR`, `EPERM`, and `ToG`

**Files:**
- Modify: `wiki/methods/GCR.md`
- Modify: `wiki/methods/EPERM.md`
- Modify: `wiki/methods/ToG.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Rewrite `wiki/methods/GCR.md` into the full serving-page structure**

Replace the body with:

```markdown
## 方法定义
一种利用图约束生成 grounded reasoning paths，以提升知识图谱推理忠实性的方法。

## 解决的核心问题
GCR 通过将图结构约束引入推理路径生成过程，减少语言模型在知识图谱推理中的自由漂移与错误跳转。

## 技术原理
GCR 强调 grounded reasoning path 的生成与约束，使推理过程既遵守图结构连接关系，又保留语言模型的语义表达能力。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：以 grounded 约束提升路径推理的可靠性。
- 对后续工作的影响：[[PathMind]] 将其作为 grounded path 方向的关键上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]

## 代表论文
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[GCR]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[GCR]] --applies_to--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --proposes--> [[GCR]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 2: Rewrite `wiki/methods/EPERM.md` into the full serving-page structure**

Replace the body with:

```markdown
## 方法定义
一种通过增强证据路径来改进知识图谱问答推理的方法。

## 解决的核心问题
EPERM 通过强调证据路径的显式构造与利用，改善知识图谱问答中的证据支撑质量。

## 技术原理
EPERM 将答案推理建立在 evidence path 之上，通过增强路径级证据表示来提升问答过程的可靠性与可解释性。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：通过证据路径增强改进路径导向推理。
- 对后续工作的影响：[[PathMind]] 将其作为 evidence path 方向的关键上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]

## 代表论文
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[EPERM]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[EPERM]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

### Incoming
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --proposes--> [[EPERM]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 3: Rewrite `wiki/methods/ToG.md` into the full serving-page structure**

Replace the body with:

```markdown
## 方法定义
一种通过 LLM 在知识图谱上迭代执行 beam search 以发现推理路径的协同增强式方法。

## 解决的核心问题
ToG 通过多轮交互式搜索提升复杂知识图谱问答中的深层路径发现能力。

## 技术原理
ToG 让语言模型与知识图谱进行多轮协同，逐步扩展、筛选并利用候选推理路径，以提升复杂问题下的搜索覆盖率。

## 方法演化位置
- 上游方法：[[协同增强式知识图谱推理]]
- 路线改进：通过多轮 LLM 交互与迭代搜索推进协同增强路线。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[multi-hop-qa]]
- 评测基准：[[CWQ]]

## 代表论文
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[ToG]] --based_on--> [[协同增强式知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --improves_on--> [[协同增强式知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[ToG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[ToG]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

### Incoming
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --proposes--> [[ToG]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 4: Run lint to verify the Method migrations pass**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit the Method migrations**

```bash
git add wiki/methods/GCR.md wiki/methods/EPERM.md wiki/methods/ToG.md
git commit -m "docs: migrate high-frequency method pages"
```

---

### Task 6: Migrate the Paper pages `GCR`, `EPERM`, and `ToG`

**Files:**
- Modify: `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- Modify: `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- Modify: `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the placeholder paper body for GCR with a serving-ready projection**

Replace the entire body after frontmatter with:

```markdown
## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与 grounded reasoning 对比对象。

## 核心问题
- 如何在知识图谱推理中通过图约束提升 grounded reasoning 的忠实性。

## 主要贡献
- 提出 graph-constrained reasoning 路线，对显式路径推理施加图结构约束。

## 核心方法
- 对应方法：[[GCR]]

## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

## 应用场景
- [[知识图谱推理问答]]

## 相关基准
- [[WebQSP]]
- [[CWQ]]

## 与知识库其他内容的关联
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 相关方法：[[GCR]]

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --proposes--> [[GCR]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 2: Replace the placeholder paper body for EPERM with a serving-ready projection**

Replace the entire body after frontmatter with:

```markdown
## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与证据路径增强对比对象。

## 核心问题
- 如何通过显式证据路径增强知识图谱问答中的答案推理可靠性。

## 主要贡献
- 提出 evidence path enhanced reasoning 路线，突出证据路径对问答推理的支撑作用。

## 核心方法
- 对应方法：[[EPERM]]

## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

## 应用场景
- [[知识图谱推理问答]]

## 相关基准
- [[WebQSP]]
- [[CWQ]]

## 与知识库其他内容的关联
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 相关方法：[[EPERM]]

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --proposes--> [[EPERM]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 3: Replace the placeholder paper body for ToG with a serving-ready projection**

Replace the entire body after frontmatter with:

```markdown
## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与协同增强式路线对比对象。

## 核心问题
- 如何通过 LLM 与知识图谱的多轮交互增强复杂问题下的推理路径搜索能力。

## 主要贡献
- 提出协同增强式的多轮搜索推理路线，提升复杂多跳场景下的路径探索深度。

## 核心方法
- 对应方法：[[ToG]]

## 相关任务
- [[knowledge-graph-reasoning]]
- [[multi-hop-qa]]

## 应用场景
- [[知识图谱推理问答]]

## 相关基准
- [[CWQ]]

## 与知识库其他内容的关联
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 相关方法：[[ToG]]

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --proposes--> [[ToG]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 4: Run lint to verify the Paper migrations pass**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit the Paper migrations**

```bash
git add "wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md" "wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md" "wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md"
git commit -m "docs: migrate high-frequency paper pages"
```

---

### Task 7: Run ontology-semantic-review and serving-governance-review for the whole batch

**Files:**
- Modify: none
- Test: skill outputs + `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run ontology-semantic-review on the migrated high-frequency batch**

Review this exact set:
- `wiki/concepts/重要推理路径.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/benchmarks/CWQ.md`
- `wiki/methods/GCR.md`
- `wiki/methods/EPERM.md`
- `wiki/methods/ToG.md`
- `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`

Expected result: relation placement, entity typing, and ontology positions are acceptable for the batch.

- [ ] **Step 2: Run serving-governance-review on the same batch**

Expected result: each page is `pass` or the review identifies exact remaining gaps that must be fixed before marking the batch serving-ready.

- [ ] **Step 3: Re-run lint after any fixes required by either review**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 8: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the final full governance check**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Verify the final scope is limited to the planned high-frequency batch files**

Run:

```bash
git diff -- \
  wiki/relations/task_method_map.md \
  wiki/relations/benchmark_links.md \
  wiki/relations/concept_links.md \
  wiki/relations/evidence_index.md \
  wiki/concepts/重要推理路径.md \
  wiki/tasks/kgqa.md \
  wiki/tasks/multi-hop-qa.md \
  wiki/benchmarks/CWQ.md \
  wiki/methods/GCR.md \
  wiki/methods/EPERM.md \
  wiki/methods/ToG.md \
  "wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md" \
  "wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md" \
  "wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md"
```

Expected: diff is limited to the intended high-frequency batch files.

- [ ] **Step 3: Commit any final verification-only fixes if needed**

Run:

```bash
git status --short
```

Expected: only planned files remain changed. If verification uncovered issues and you fixed them, commit with:

```bash
git add wiki/relations/task_method_map.md wiki/relations/benchmark_links.md wiki/relations/concept_links.md wiki/relations/evidence_index.md wiki/concepts/重要推理路径.md wiki/tasks/kgqa.md wiki/tasks/multi-hop-qa.md wiki/benchmarks/CWQ.md wiki/methods/GCR.md wiki/methods/EPERM.md wiki/methods/ToG.md "wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md" "wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md" "wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md"
git commit -m "chore: finalize high-frequency serving batch"
```

If no verification-only fixes were needed, do not create an extra commit.
