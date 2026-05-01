# Relations Instance-Edge Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish `wiki/relations/` as the canonical Markdown-maintained instance-edge layer, and update `wiki/ontology/graph-standard.md` so edge-instance maintenance becomes a formal ontology rule.

**Architecture:** Keep the repository Markdown-first. `wiki/ontology/graph-standard.md` defines the instance-edge schema, per-file ownership, and maintenance rules; `wiki/relations/*.md` stores concrete edge records using one uniform syntax; `CLAUDE.md` remains a handbook that points to the graph standard instead of duplicating edge rules.

**Tech Stack:** Markdown, Obsidian wikilinks, repository documentation conventions, `python3 scripts/lint_graph.py`, `rg`

---

## File Structure

**Modify:**
- `wiki/ontology/graph-standard.md` — add canonical instance-edge rules, per-file ownership, record syntax, concept-link labels, and maintenance constraints
- `wiki/relations/citation_graph.md` — rewrite into canonical `cites` edge ledger
- `wiki/relations/method_evolution.md` — rewrite into canonical `based_on` / `improves_on` edge ledger
- `wiki/relations/task_method_map.md` — rewrite into canonical `targets_task` edge ledger
- `wiki/relations/concept_links.md` — rewrite into canonical concept-network / `uses_concept` edge ledger
- `wiki/relations/evidence_index.md` — rewrite into canonical `supported_by` edge ledger
- `CLAUDE.md` — tighten the relation-maintenance pointer if needed so the handbook does not duplicate edge-instance rules

**No new files required for this change.**

---

### Task 1: Add instance-edge rules to the graph standard

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Verify: `wiki/ontology/graph-standard.md`

- [ ] **Step 1: Confirm the current relation-type section and relation-page inventory**

Run:
```bash
rg -n '^## 关系类型|^## 关系索引|citation_graph|method_evolution|task_method_map|concept_links|evidence_index' wiki/ontology/graph-standard.md
```
Expected: matches for the existing relation-type section and the current relation index entries.

- [ ] **Step 2: Insert an instance-edge-layer section after the node/frontmatter rules**

Add this Markdown block to `wiki/ontology/graph-standard.md`:

```markdown
## 实例边层
- 实例边（instance edge）是两个具体知识节点之间的显式关系记录，不等同于关系类型定义本身。
- `wiki/relations/` 是正式维护实例边账本的唯一位置。
- 节点页中的自然语言说明、`[[wikilink]]` 与综述性表述可以辅助理解，但不能替代 `wiki/relations/` 中的正式实例边记录。
- 查询、分析、拓扑探索与后续图谱扩展，应优先依据实例边账本，而不是仅从正文 prose 推断关系。
```

- [ ] **Step 3: Insert the canonical edge-record format section**

Add this Markdown block to `wiki/ontology/graph-standard.md`:

```markdown
## 实例边记录格式
正式实例边统一使用以下格式：

```markdown
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: 关系成立原因
  - evidence: [[证据页]]
```

可选字段：

```markdown
  - status: verified | placeholder
  - note: 补充上下文
```

说明：
- 第一行是实例边主记录，必须包含主体节点、关系类型、客体节点。
- `reason` 必填，用一句话说明该关系为何成立。
- `evidence` 必填，默认指向 `intermediate/` 下的证据缓存；如需要可在链接后补充节号。
- `status` 仅在占位边或待确认边场景下填写；默认省略即视为 `verified`。
- `note` 仅用于不能放入 `reason` 的短补充，不替代 `reason`。
```

- [ ] **Step 4: Add per-file ownership rules**

Add this Markdown block to `wiki/ontology/graph-standard.md`:

```markdown
## 关系文件分工
- `wiki/relations/citation_graph.md`：维护 `cites`
- `wiki/relations/method_evolution.md`：维护 `based_on`、`improves_on`
- `wiki/relations/task_method_map.md`：维护 `targets_task`
- `wiki/relations/concept_links.md`：维护 `uses_concept` 与概念网络中的补充语义边
- `wiki/relations/evidence_index.md`：维护 `supported_by`

新增关系类型时，必须显式指定其归属文件；未归属的关系类型不能进入正式实例边层。
```

- [ ] **Step 5: Add concept-network relation labels and edge-maintenance rules**

Add this Markdown block to `wiki/ontology/graph-standard.md`:

```markdown
## 概念网络补充边标签
- `supports`：概念或框架为另一个概念、任务或场景提供支撑语义
- `depends_on`：概念依赖另一个概念才能成立或解释

上述标签仅在 `wiki/relations/concept_links.md` 中使用；若未来出现更细粒度关系，应先在本规范中登记后再使用。

## 实例边维护规则
- 同一文件内，不允许出现完全重复的主体 / 关系类型 / 客体三元组。
- 同一对节点若存在不同关系类型，应保留为不同实例边记录。
- 无证据的实例边默认无效；只有在论文类型豁免明确适用时，才允许使用 `status: placeholder` 暂存。
- prose 可作为说明，但正式关系判断以实例边记录为准。
- 每次 ingest 或知识页更新后，应同步检查对应 `wiki/relations/*.md` 是否需要增量更新。
```

- [ ] **Step 6: Verify the graph standard contains all new sections**

Run:
```bash
rg -n '^## 实例边层|^## 实例边记录格式|^## 关系文件分工|^## 概念网络补充边标签|^## 实例边维护规则' wiki/ontology/graph-standard.md
```
Expected: five matches, one for each new section.

- [ ] **Step 7: Commit the graph-standard change**

Run:
```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: define canonical ontology edge records"
```
Expected: one new commit containing only the graph-standard update.

---

### Task 2: Normalize `citation_graph.md` into canonical `cites` records

**Files:**
- Modify: `wiki/relations/citation_graph.md`
- Verify: `wiki/relations/citation_graph.md`

- [ ] **Step 1: Replace the current freeform citation lines with explicit edge records**

Rewrite `wiki/relations/citation_graph.md` to this exact structure:

```markdown
## `cites` 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - reason: 方法借鉴，作为 retrieval-augmented 路径推理代表工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - reason: 方法借鉴，作为 grounded reasoning path 代表工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]`
  - reason: 方法借鉴，作为 evidence path 增强代表工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]`
  - reason: 对比实验，作为 GNN 检索增强代表工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - reason: 方法对比，作为 synergy-augmented 代表工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]`
  - reason: 方法对比，作为 LLM 生成推理路径方向的近期工作。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - reason: 作为 LLM + KG 推理路线代表工作被 survey 纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - reason: 作为 graph-constrained reasoning 代表工作被纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]`
  - reason: 作为 evidence path 路线代表工作被纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]`
  - reason: 作为图检索增强路线代表工作被纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - reason: 作为协同增强路线代表工作被纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --cites--> [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]`
  - reason: 作为生成推理路径路线代表工作被纳入。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5

## 说明
- 本页是 `cites` 实例边的正式账本。
- 引用关系的正文说明可以出现在论文页或 `refs.md` 缓存中，但正式实例边以本页为准。
```

- [ ] **Step 2: Verify that all citation edges now use the canonical syntax**

Run:
```bash
rg -n -- '--cites-->' wiki/relations/citation_graph.md
```
Expected: 12 matches, one for each citation edge.

- [ ] **Step 3: Commit the citation-graph rewrite**

Run:
```bash
git add wiki/relations/citation_graph.md
git commit -m "docs: normalize citation edge ledger"
```
Expected: one new commit containing only the citation ledger rewrite.

---

### Task 3: Normalize method, task, and concept relation ledgers

**Files:**
- Modify: `wiki/relations/method_evolution.md`
- Modify: `wiki/relations/task_method_map.md`
- Modify: `wiki/relations/concept_links.md`
- Verify: `wiki/relations/method_evolution.md`
- Verify: `wiki/relations/task_method_map.md`
- Verify: `wiki/relations/concept_links.md`

- [ ] **Step 1: Rewrite `method_evolution.md` as explicit `based_on` / `improves_on` records**

Rewrite the file to include this edge inventory:

```markdown
## `based_on` / `improves_on` 实例边
- `[[路径导向知识图谱推理]] --based_on--> [[检索增强式知识图谱推理]]`
  - reason: 路径导向路线建立在检索增强式知识图谱推理范式之上。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §2–5
- `[[RoG]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: RoG 采用显式关系推理路径作为核心机制。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[RoG]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过显式生成关系推理路径推进路径导向路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[GCR]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: GCR 采用 grounded reasoning path 路线。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 以 grounded 约束提升推理路径可靠性。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[EPERM]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: EPERM 采用 evidence path 增强路径推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过证据路径增强改进路径导向推理。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[PathMind]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: PathMind 属于路径导向知识图谱推理路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过路径优先化与对齐训练提升路径导向推理质量。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[ToG]] --based_on--> [[协同增强式知识图谱推理]]`
  - reason: ToG 属于协同增强式知识图谱推理路线。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[ToG]] --improves_on--> [[协同增强式知识图谱推理]]`
  - reason: 通过多轮 LLM 交互与迭代搜索推进协同增强路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5

## 说明
- 本页是 `based_on` / `improves_on` 实例边的正式账本。
- 如需保留树形阅读体验，可在实例边之下补充非规范性概览，但不能替代边记录。
```

- [ ] **Step 2: Rewrite `task_method_map.md` as explicit `targets_task` records**

Rewrite the file to include this edge inventory:

```markdown
## `targets_task` 实例边
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: PathMind 以知识图谱推理为核心任务定位。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: RoG 是知识图谱推理代表方法之一。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: GCR 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: EPERM 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[ToG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: ToG 面向知识图谱推理任务。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - reason: PathMind 在知识图谱问答场景中验证方法有效性。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[kgqa]]`
  - reason: RoG 是 KGQA 路线中的显式路径推理代表方法。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --targets_task--> [[kgqa]]`
  - reason: GCR 面向 KGQA 场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --targets_task--> [[kgqa]]`
  - reason: EPERM 面向 KGQA 场景。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[PathMind]] --targets_task--> [[multi-hop-qa]]`
  - reason: PathMind 重点处理复杂多跳问答中的高价值路径选择。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[RoG]] --targets_task--> [[multi-hop-qa]]`
  - reason: RoG 面向多跳问答中的关系路径推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[ToG]] --targets_task--> [[multi-hop-qa]]`
  - reason: ToG 通过迭代搜索支持复杂多跳问答。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[GCR]] --targets_task--> [[multi-hop-qa]]`
  - reason: GCR 面向 grounded 的多跳推理问答。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --targets_task--> [[engineering-design-knowledge-management]]`
  - reason: 该 survey 以复杂产品设计中的知识管理与协同增强任务为综述对象。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §3–10

## 说明
- 本页是 `targets_task` 实例边的正式账本。
- 若某条关系仅涉及场景而非任务，应记录到对应知识页或后续场景关系文件，而不是混入本页。
```

- [ ] **Step 3: Rewrite `concept_links.md` as explicit concept-network / `uses_concept` records**

Rewrite the file to include this edge inventory:

```markdown
## `uses_concept` 与概念网络实例边
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
  - reason: PathMind 的核心机制之一是路径优先化。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind]] --uses_concept--> [[重要推理路径]]`
  - reason: PathMind 以识别和筛选重要推理路径为核心目标。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[路径优先化]] --supports--> [[重要推理路径]]`
  - reason: 路径优先化机制直接服务于重要推理路径的识别与筛选。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[重要推理路径]] --supports--> [[knowledge-graph-reasoning]]`
  - reason: 重要推理路径为知识图谱推理提供关键证据链。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[重要推理路径]] --supports--> [[kgqa]]`
  - reason: 重要推理路径是复杂问答中的高价值证据链单元。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §1、§7
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --uses_concept--> [[LLM增强知识图谱]]`
  - reason: 该 survey 系统梳理 LLM 增强知识图谱路线。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §3–5
- `[[复杂产品设计中的LLM-KG协同框架]] --uses_concept--> [[LLM增强知识图谱]]`
  - reason: 该框架以 LLM 增强知识图谱作为系统级协同基础。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6–10
- `[[复杂产品设计中的LLM-KG协同框架]] --applies_to--> [[复杂产品设计]]`
  - reason: 该框架面向复杂产品设计场景落地。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6–10

## 说明
- 本页是概念网络与 `uses_concept` 实例边的正式账本。
- `supports` / `applies_to` 仅按 `graph-standard.md` 中登记的允许标签使用。
```

- [ ] **Step 4: Verify that the three ledgers now expose explicit edge records**

Run:
```bash
rg -n -- '--(based_on|improves_on|targets_task|uses_concept|supports|applies_to)-->' wiki/relations/method_evolution.md wiki/relations/task_method_map.md wiki/relations/concept_links.md
```
Expected: matches in all three files, covering the rewritten ledgers.

- [ ] **Step 5: Commit the method/task/concept ledger rewrites**

Run:
```bash
git add wiki/relations/method_evolution.md wiki/relations/task_method_map.md wiki/relations/concept_links.md
git commit -m "docs: normalize ontology relation ledgers"
```
Expected: one new commit containing the three ledger rewrites.

---

### Task 4: Normalize the evidence ledger and align CLAUDE.md

**Files:**
- Modify: `wiki/relations/evidence_index.md`
- Modify: `CLAUDE.md`
- Verify: `wiki/relations/evidence_index.md`
- Verify: `CLAUDE.md`

- [ ] **Step 1: Rewrite `evidence_index.md` as explicit `supported_by` records**

Rewrite the file to include this structure:

```markdown
## `supported_by` 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - reason: 方法机制证据。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.experiments|PathMind.experiments]]`
  - reason: 实验结果证据。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §3–7
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 引用与基线证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]]`
  - reason: 综述定位与框架抽象证据。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §3–10
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]]`
  - reason: 规范优化启示与上游工作引用证据。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] §5
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --supported_by--> [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]]`
  - reason: 统计 / landscape 分析证据。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] §1–7
- `[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用与实验对比证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - reason: 作为上游代表工作的引用证据。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–5

## 说明
- 本页是 `supported_by` 实例边的正式账本。
- 若某正式知识页绑定多个证据缓存，应拆成多条独立实例边。
```

- [ ] **Step 2: Tighten the CLAUDE relation-handbook section into a single pointer if it still contains extra maintenance detail**

Ensure `CLAUDE.md` keeps only a short pointer like this:

```markdown
## 关联关系文件规范

`wiki/relations/` 下的实例边维护规范、关系文件分工与正式记录格式，统一以 `wiki/ontology/graph-standard.md` 为准。
```

- [ ] **Step 3: Verify the evidence ledger and CLAUDE pointer**

Run:
```bash
rg -n -- '--supported_by-->' wiki/relations/evidence_index.md && rg -n '^## 关联关系文件规范|graph-standard.md' CLAUDE.md
```
Expected: explicit `supported_by` records in the evidence file and a short relation pointer in `CLAUDE.md`.

- [ ] **Step 4: Commit the evidence and CLAUDE alignment changes**

Run:
```bash
git add wiki/relations/evidence_index.md CLAUDE.md
git commit -m "docs: align evidence ledger and handbook pointers"
```
Expected: one new commit containing the evidence-ledger rewrite and CLAUDE alignment.

---

### Task 5: Run repository verification and review the final graph shape

**Files:**
- Verify: `wiki/ontology/graph-standard.md`
- Verify: `wiki/relations/citation_graph.md`
- Verify: `wiki/relations/method_evolution.md`
- Verify: `wiki/relations/task_method_map.md`
- Verify: `wiki/relations/concept_links.md`
- Verify: `wiki/relations/evidence_index.md`
- Verify: `CLAUDE.md`

- [ ] **Step 1: Run the graph lint script**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: no new graph-structure regressions caused by the relation-ledger rewrites.

- [ ] **Step 2: Verify canonical edge patterns across all relation files**

Run:
```bash
rg -n -- '--(cites|based_on|improves_on|targets_task|uses_concept|supports|applies_to|supported_by)-->' wiki/relations
```
Expected: matches in all five relation ledgers using the canonical syntax.

- [ ] **Step 3: Inspect git diff to confirm only the intended documentation files changed**

Run:
```bash
git diff -- wiki/ontology/graph-standard.md wiki/relations/citation_graph.md wiki/relations/method_evolution.md wiki/relations/task_method_map.md wiki/relations/concept_links.md wiki/relations/evidence_index.md CLAUDE.md
```
Expected: diff limited to the seven documentation files in scope.

- [ ] **Step 4: Create a final integration commit**

Run:
```bash
git add wiki/ontology/graph-standard.md wiki/relations/citation_graph.md wiki/relations/method_evolution.md wiki/relations/task_method_map.md wiki/relations/concept_links.md wiki/relations/evidence_index.md CLAUDE.md
git commit -m "docs: establish canonical ontology edge ledgers"
```
Expected: a final commit that captures the integrated Markdown-first instance-edge layer.

---

## Spec Coverage Check

- Canonical instance-edge rules in `graph-standard.md` → Task 1
- Relation-type file ownership → Task 1
- Citation ledger normalization → Task 2
- Method / task / concept ledger normalization → Task 3
- Evidence ledger normalization → Task 4
- `CLAUDE.md` alignment → Task 4
- Repository verification → Task 5

No spec gaps remain.

## Placeholder Scan

- No `TODO`, `TBD`, or deferred placeholders remain.
- Every file in scope is named explicitly.
- Every relation file rewrite includes exact target edge inventories.

## Type Consistency Check

- Canonical edge first line always uses `[[Source]] --relation_type--> [[Target]]`
- Required fields always remain `reason` and `evidence`
- Optional fields stay `status` and `note`
- Owned relation types stay consistent across graph standard and relation ledgers
