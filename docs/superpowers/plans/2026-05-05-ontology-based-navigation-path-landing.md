# Ontology-Based Navigation Path Landing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the ontology-based navigation path in ResearchKB by adding domain indexes, relation-ledger navigation headers, and lightweight entity-page navigation blocks while keeping serving-ready object pages as the default reading entry.

**Architecture:** First update the two global routing documents so the navigation policy and system entry are explicit. Then add all six object-domain index pages as mixed instance directories. After that, retrofit relation ledgers with governance-aware navigation headers and retrofit entity pages with lightweight back-links to their domain index, related ledgers, and evidence surfaces. Finish by running graph lint and manually verifying navigation closure through representative paths.

**Tech Stack:** Markdown knowledge pages under `wiki/`, ontology authority in `wiki/ontology/graph-standard.md`, relation ledgers under `wiki/relations/`, evidence cache pages under `intermediate/papers/`, Python 3 lint script `scripts/lint_graph.py`.

---

## File map

### Global navigation policy and router
- Modify: `CLAUDE.md`
  - Tighten the written navigation policy so it matches the agreed layered path and explicitly distinguishes object-page serving entry from relation-ledger truth source.
- Modify: `wiki/ontology/index.md`
  - Convert the current page into a stricter system router that points to graph standard, the six object-domain indexes, relation ledgers, and recommended reading paths.

### Object-domain indexes to create
- Create: `wiki/papers/index.md`
- Create: `wiki/methods/index.md`
- Create: `wiki/concepts/index.md`
- Create: `wiki/tasks/index.md`
- Create: `wiki/scenarios/index.md`
- Create: `wiki/benchmarks/index.md`

### Relation ledgers to retrofit with navigation headers
- Modify: `wiki/relations/citation_graph.md`
- Modify: `wiki/relations/method_evolution.md`
- Modify: `wiki/relations/concept_links.md`
- Modify: `wiki/relations/task_method_map.md`
- Modify: `wiki/relations/evidence_index.md`
- Modify: `wiki/relations/paper_method_links.md`
- Modify: `wiki/relations/benchmark_links.md`
- Modify: `wiki/relations/provenance_links.md`

### Entity pages to retrofit with navigation blocks
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- Modify: `wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
- Modify: `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- Modify: `wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`
- Modify: `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Modify: `wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
- Modify: `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`
- Modify: `wiki/methods/EPERM.md`
- Modify: `wiki/methods/GCR.md`
- Modify: `wiki/methods/PathMind.md`
- Modify: `wiki/methods/RoG.md`
- Modify: `wiki/methods/ToG.md`
- Modify: `wiki/methods/协同增强式知识图谱推理.md`
- Modify: `wiki/methods/检索增强式知识图谱推理.md`
- Modify: `wiki/methods/路径导向知识图谱推理.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Modify: `wiki/benchmarks/CWQ.md`
- Modify: `wiki/benchmarks/WebQSP.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: manual navigation spot-checks on representative paths through ontology index, object-domain indexes, entity pages, relation ledgers, and evidence links
- Test: `git diff --stat`
- Test: `git status --short`

---

### Task 1: Update the global navigation policy in `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Read the current navigation sections before editing**

Read and align these sections in `CLAUDE.md`:
- `## 知识库结构与规范边界`
- `## Agent 的全局认知入口`
- `## 面向用户问题的默认认知方式`
- `## 查询与分析默认顺序`

Confirm the document already contains these anchor ideas and keep them, but tighten wording around:
- `CLAUDE.md` = policy and default path
- `wiki/ontology/index.md` = router
- object pages = serving entry
- `wiki/relations/*.md` = truth source for governance/review
- `intermediate/papers/` = evidence drill-down

- [ ] **Step 2: Replace the navigation-boundary bullets with explicit layered wording**

Use this exact replacement block inside `## 知识库结构与规范边界`:

```md
`CLAUDE.md` 负责：
- 全局本体基础认知
- 用户问题的判定与探查策略
- 工作流入口
- 执行约束
- 默认导航顺序与跨层读取原则

`wiki/ontology/graph-standard.md` 是本体规范的**唯一权威来源**，也是解决具体问题时的**本体结构认知与判定中枢**。负责：
- 本体结构认知与节点 / 关系 / 证据判定规则
- 节点模板
- frontmatter 受控字段
- 关系类型
- 实例边格式
- 关系文件分工
- 最小链接义务
- 证据要求
- 豁免规则

`wiki/ontology/index.md` 负责系统级导航：
- 规范导航：指向 `graph-standard`
- 对象域导航：指向 `wiki/papers/index.md`、`wiki/methods/index.md`、`wiki/concepts/index.md`、`wiki/tasks/index.md`、`wiki/scenarios/index.md`、`wiki/benchmarks/index.md`
- 关系域导航：指向 `wiki/relations/*.md` 正式关系账本
- 推荐读取路径：按问答、治理、证据核验等场景给出默认路由

`wiki/<对象域>/index.md` 负责对象域内导航：
- 组织该对象域的核心实例入口
- 提供主题分组与完整实例清单
- 指向与该对象域最相关的 relation ledger

`wiki/relations/*.md` 负责正式关系治理导航：
- 作为 formal relation ledger 的真源读取面
- 在治理、修复、审计、真源核对场景下锚定关系实例
- 必要时帮助回链到对象域与相关实例
```

- [ ] **Step 3: Replace the default-reading-order list with the finalized routing path**

Inside `## 查询与分析默认顺序`, use this ordered list:

```md
1. 读取 `wiki/ontology/index.md` 定位系统级导航入口
2. 根据问题类型进入对应 `wiki/<对象域>/index.md`，锁定候选正式实例
3. 读取对应 serving-ready 对象页，作为默认问答入口
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展
5. 如涉及机制、实验、引用、基线、统计分析或 provenance 核验，优先读取对应 Evidence 页与 `intermediate/papers/`
6. 如处于治理、修复、审计场景，或需核对 formal graph truth，再读取 `wiki/relations/*.md`
7. 必要时才回看 `raw/`
```

- [ ] **Step 4: Run lint to make sure the policy edit did not introduce markdown or graph-reference issues**

Run: `python3 scripts/lint_graph.py`
Expected: PASS, or failures unrelated to `CLAUDE.md` structure.

- [ ] **Step 5: Commit the global-policy edit**

```bash
git add CLAUDE.md
git commit -m "docs: clarify ontology navigation policy"
```

### Task 2: Convert `wiki/ontology/index.md` into the strict system router

**Files:**
- Modify: `wiki/ontology/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the current object-entry section so it points to domain indexes, not raw directories**

Replace the current `## 3. 正式知识对象入口` block with:

```md
## 3. 正式知识对象域入口
- Papers：[[../papers/index|wiki/papers/index.md]]
- Methods：[[../methods/index|wiki/methods/index.md]]
- Concepts：[[../concepts/index|wiki/concepts/index.md]]
- Tasks：[[../tasks/index|wiki/tasks/index.md]]
- Scenarios：[[../scenarios/index|wiki/scenarios/index.md]]
- Benchmarks：[[../benchmarks/index|wiki/benchmarks/index.md]]
```

- [ ] **Step 2: Rewrite the task-oriented routing section with explicit layered path language**

Replace `## 4. 按任务进入` with:

```md
## 4. 按任务进入
- 想做受约束知识问答 → 先进入对应 `wiki/<对象域>/index.md` 锁定正式对象，再读取 serving-ready 对象页，并按 `Formal relations` 扩展；需要证据细节时再下钻对应 Evidence 页
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式对象知识 → 对应对象域 index → 对象页
- 想看治理用正式关系账本 → 对应 `wiki/relations/*.md`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `docs/`
```

- [ ] **Step 3: Rewrite the recommended paths so the first-stop reading surface is consistent**

Replace `## 5. 推荐阅读路径` with:

```md
## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → 本页 → 对应对象域 index → 代表对象页 → 必要时 Evidence / relation ledger

### 回答知识问题
对象域 index → serving-ready 对象页 → `Formal relations` → 邻接对象页 / Evidence 页 → 必要时 relation ledger

### 治理知识变更
[[graph-standard]] → relation ledger → 变更对象页 / Evidence 页 → 必要时对象域 index 回链
```

- [ ] **Step 4: Run lint after the router rewrite**

Run: `python3 scripts/lint_graph.py`
Expected: FAIL only because the six object-domain index pages do not exist yet, or PASS if they already exist.

- [ ] **Step 5: Commit the router rewrite**

```bash
git add wiki/ontology/index.md
git commit -m "docs: route ontology navigation through domain indexes"
```

### Task 3: Create all six object-domain index pages

**Files:**
- Create: `wiki/papers/index.md`
- Create: `wiki/methods/index.md`
- Create: `wiki/concepts/index.md`
- Create: `wiki/tasks/index.md`
- Create: `wiki/scenarios/index.md`
- Create: `wiki/benchmarks/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Create `wiki/papers/index.md` with the full mixed-layout content**

Create this file:

```md
# Papers Index

> 本页负责 Paper 对象域导航：先定位论文实例，再进入论文页；如需正式关系真源，再转到相关 relation ledger。

## 1. 对象域说明
- 本域收录正式 Paper 节点。
- 默认先从论文页读取核心问题、贡献、关系与证据入口，再按需要扩展到方法、概念、任务、场景与 benchmark。

## 2. 核心入口
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]

## 3. 按主题分组
### KG 推理 / KGQA 主线
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]

### 综述 / 复杂产品设计主线
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]

## 4. 完整实例清单
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]

## 5. 相关关系账本
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/citation_graph|citation_graph]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 2: Create `wiki/methods/index.md` with the full mixed-layout content**

Create this file:

```md
# Methods Index

> 本页负责 Method 对象域导航：先定位方法实例，再进入方法页；formal 演化边与任务/概念/benchmark 真源在相关 relation ledger。

## 1. 对象域说明
- 本域收录正式 Method 节点。
- 默认从方法页读取方法定义、演化位置、相关任务、相关概念与证据来源。

## 2. 核心入口
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[ToG]]

## 3. 按主题分组
### 路径导向路线
- [[路径导向知识图谱推理]]
- [[RoG]]
- [[GCR]]
- [[EPERM]]
- [[PathMind]]

### 协同增强路线
- [[协同增强式知识图谱推理]]
- [[ToG]]

### 检索增强路线
- [[检索增强式知识图谱推理]]

## 4. 完整实例清单
- [[EPERM]]
- [[GCR]]
- [[PathMind]]
- [[RoG]]
- [[ToG]]
- [[协同增强式知识图谱推理]]
- [[检索增强式知识图谱推理]]
- [[路径导向知识图谱推理]]

## 5. 相关关系账本
- [[../relations/method_evolution|method_evolution]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 3: Create `wiki/concepts/index.md` with the full mixed-layout content**

Create this file:

```md
# Concepts Index

> 本页负责 Concept 对象域导航：先定位概念实例，再进入概念页；formal 概念网络真源在 `concept_links`。

## 1. 对象域说明
- 本域收录正式 Concept 节点，包括一般概念与 framework 型概念。
- 默认从概念页读取概念定义、相关方法、相关论文、相关任务 / 场景与证据入口。

## 2. 核心入口
- [[路径优先化]]
- [[重要推理路径]]
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]

## 3. 按主题分组
### 路径推理核心概念
- [[路径优先化]]
- [[重要推理路径]]

### LLM-KG / framework 主线
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]

## 4. 完整实例清单
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]
- [[路径优先化]]
- [[重要推理路径]]

## 5. 相关关系账本
- [[../relations/concept_links|concept_links]]
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 4: Create `wiki/tasks/index.md` with the full mixed-layout content**

Create this file:

```md
# Tasks Index

> 本页负责 Task 对象域导航：先定位任务实例，再进入任务页；formal 方法映射真源在 `task_method_map`。

## 1. 对象域说明
- 本域收录正式 Task 节点。
- 默认从任务页读取任务定义、核心挑战、相关方法、相关概念、相关 benchmark 与证据入口。

## 2. 核心入口
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]
- [[engineering-design-knowledge-management]]

## 3. 按主题分组
### KG 推理 / 问答任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

### 设计知识管理任务
- [[engineering-design-knowledge-management]]

## 4. 完整实例清单
- [[engineering-design-knowledge-management]]
- [[kgqa]]
- [[knowledge-graph-reasoning]]
- [[multi-hop-qa]]

## 5. 相关关系账本
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 5: Create `wiki/scenarios/index.md` and `wiki/benchmarks/index.md` with the full mixed-layout content**

Create `wiki/scenarios/index.md`:

```md
# Scenarios Index

> 本页负责 Scenario 对象域导航：先定位场景实例，再进入场景页；formal 场景相关边目前主要分散锚定在对象页与 `concept_links` / `task_method_map` 中。

## 1. 对象域说明
- 本域收录正式 Scenario 节点。
- 默认从场景页读取场景描述、核心挑战、主要方法 / 概念、相关任务与证据入口。

## 2. 核心入口
- [[知识图谱推理问答]]
- [[复杂产品设计]]

## 3. 按主题分组
### 知识图谱推理场景
- [[知识图谱推理问答]]

### 复杂产品设计场景
- [[复杂产品设计]]

## 4. 完整实例清单
- [[复杂产品设计]]
- [[知识图谱推理问答]]

## 5. 相关关系账本
- [[../relations/concept_links|concept_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

Create `wiki/benchmarks/index.md`:

```md
# Benchmarks Index

> 本页负责 Benchmark 对象域导航：先定位 benchmark 实例，再进入 benchmark 页；formal benchmark 绑定真源在 `benchmark_links`。

## 1. 对象域说明
- 本域收录正式 Benchmark 节点。
- 默认从 benchmark 页读取基准定义、相关任务、被哪些方法 / 论文使用，以及证据入口。

## 2. 核心入口
- [[WebQSP]]
- [[CWQ]]

## 3. 按主题分组
### KGQA / 多跳问答基准
- [[WebQSP]]
- [[CWQ]]

## 4. 完整实例清单
- [[CWQ]]
- [[WebQSP]]

## 5. 相关关系账本
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 6: Run lint after creating all six index pages**

Run: `python3 scripts/lint_graph.py`
Expected: PASS, or only failures caused by yet-unretrofitted links in later tasks.

- [ ] **Step 7: Commit the object-domain indexes**

```bash
git add wiki/papers/index.md wiki/methods/index.md wiki/concepts/index.md wiki/tasks/index.md wiki/scenarios/index.md wiki/benchmarks/index.md
git commit -m "docs: add ontology object domain indexes"
```

### Task 4: Add governance-aware navigation headers to every relation ledger

**Files:**
- Modify: `wiki/relations/citation_graph.md`
- Modify: `wiki/relations/method_evolution.md`
- Modify: `wiki/relations/concept_links.md`
- Modify: `wiki/relations/task_method_map.md`
- Modify: `wiki/relations/evidence_index.md`
- Modify: `wiki/relations/paper_method_links.md`
- Modify: `wiki/relations/benchmark_links.md`
- Modify: `wiki/relations/provenance_links.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Prepend the standard ledger header to `citation_graph.md` and `paper_method_links.md`**

Insert this block at the top of `wiki/relations/citation_graph.md`:

```md
> 本页是正式关系账本：维护 `cites` 实例边。默认问答优先读取 `wiki/papers/index.md` → 论文页；只有在治理、修复、审计或 formal truth 核对时优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]
```

Insert this block at the top of `wiki/relations/paper_method_links.md`:

```md
> 本页是正式关系账本：维护 `proposes` 实例边。默认问答优先读取论文页或方法 / 概念页；只有在 formal graph truth 核对或治理场景下优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]、[[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]
> 相关证据入口：[[evidence_index]]
```

- [ ] **Step 2: Prepend the standard ledger header to `method_evolution.md` and `task_method_map.md`**

Insert this block at the top of `wiki/relations/method_evolution.md`:

```md
> 本页是正式关系账本：维护 `based_on` / `improves_on` 实例边。默认问答优先读取 `wiki/methods/index.md` → 方法页；只有在演化链治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../methods/index|methods/index]]
> 相关证据入口：[[evidence_index]]
```

Insert this block at the top of `wiki/relations/task_method_map.md`:

```md
> 本页是正式关系账本：维护 `targets_task` 实例边。默认问答优先读取任务页或方法页；只有在任务映射治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../tasks/index|tasks/index]]、[[../methods/index|methods/index]]、[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]
```

- [ ] **Step 3: Prepend the standard ledger header to `concept_links.md`, `benchmark_links.md`, `evidence_index.md`, and `provenance_links.md`**

Insert this block at the top of `wiki/relations/concept_links.md`:

```md
> 本页是正式关系账本：维护 `uses_concept` 及登记在本页的概念网络实例边。默认问答优先读取概念页、方法页、任务页或场景页；只有在概念网络治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../concepts/index|concepts/index]]、[[../methods/index|methods/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]
> 相关证据入口：[[evidence_index]]
```

Insert this block at the top of `wiki/relations/benchmark_links.md`:

```md
> 本页是正式关系账本：维护 `evaluated_on` 实例边。默认问答优先读取 benchmark 页、方法页或论文页；只有在 benchmark 绑定治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../benchmarks/index|benchmarks/index]]、[[../methods/index|methods/index]]、[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]
```

Insert this block at the top of `wiki/relations/evidence_index.md`:

```md
> 本页是正式关系账本：维护 `supported_by` 实例边。默认问答优先读取对象页；只有在证据绑定核对、治理、修复或审计时优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]、[[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../benchmarks/index|benchmarks/index]]
> 相关 provenance 入口：[[provenance_links]]
```

Insert this block at the top of `wiki/relations/provenance_links.md`:

```md
> 本页是正式关系账本：维护 `sourced_from` provenance 实例边。默认问答不以本页作为首入口；只有在 Evidence 来源回溯、治理、修复或真源核对时优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]
```

- [ ] **Step 4: Run lint after all relation-ledger headers are added**

Run: `python3 scripts/lint_graph.py`
Expected: PASS.

- [ ] **Step 5: Commit the relation-ledger retrofit**

```bash
git add wiki/relations/citation_graph.md wiki/relations/method_evolution.md wiki/relations/concept_links.md wiki/relations/task_method_map.md wiki/relations/evidence_index.md wiki/relations/paper_method_links.md wiki/relations/benchmark_links.md wiki/relations/provenance_links.md
git commit -m "docs: add relation ledger navigation headers"
```

### Task 5: Add navigation blocks to all paper pages

**Files:**
- Modify: all files under `wiki/papers/` listed in the File map
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add the standard paper navigation block to `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`**

Insert this block immediately after the frontmatter:

```md
> 导航：返回 [[index|papers/index]]；相关对象域 [[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../benchmarks/index|benchmarks/index]]。
>
> 相关 relation ledger：[[../relations/paper_method_links|paper_method_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/citation_graph|citation_graph]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 论文入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 2: Add the same paper navigation pattern to the other seven paper pages**

Insert the same three-paragraph block immediately after frontmatter in:
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- `wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
- `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- `wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`
- `wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
- `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`

- [ ] **Step 3: Run lint after the paper-page retrofit**

Run: `python3 scripts/lint_graph.py`
Expected: PASS.

- [ ] **Step 4: Commit the paper-page retrofit**

```bash
git add wiki/papers/*.md
git commit -m "docs: add navigation blocks to paper pages"
```

### Task 6: Add navigation blocks to all method and concept pages

**Files:**
- Modify: all files under `wiki/methods/` and `wiki/concepts/` listed in the File map
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add the standard method navigation block to `wiki/methods/PathMind.md` and the other seven method pages**

Insert this block immediately after frontmatter in every file under `wiki/methods/`:

```md
> 导航：返回 [[index|methods/index]]；相关对象域 [[../tasks/index|tasks/index]]、[[../concepts/index|concepts/index]]、[[../benchmarks/index|benchmarks/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/method_evolution|method_evolution]]、[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/paper_method_links|paper_method_links]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 方法入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 2: Add the standard concept navigation block to all four concept pages**

Insert this block immediately after frontmatter in every file under `wiki/concepts/`:

```md
> 导航：返回 [[index|concepts/index]]；相关对象域 [[../methods/index|methods/index]]、[[../tasks/index|tasks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/concept_links|concept_links]]、[[../relations/paper_method_links|paper_method_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 概念入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 3: Run lint after the method/concept retrofit**

Run: `python3 scripts/lint_graph.py`
Expected: PASS.

- [ ] **Step 4: Commit the method/concept retrofit**

```bash
git add wiki/methods/*.md wiki/concepts/*.md
git commit -m "docs: add navigation blocks to method and concept pages"
```

### Task 7: Add navigation blocks to all task, scenario, and benchmark pages

**Files:**
- Modify: all files under `wiki/tasks/`, `wiki/scenarios/`, and `wiki/benchmarks/` listed in the File map
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add the standard task navigation block to all four task pages**

Insert this block immediately after frontmatter in every file under `wiki/tasks/`:

```md
> 导航：返回 [[index|tasks/index]]；相关对象域 [[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../benchmarks/index|benchmarks/index]]、[[../scenarios/index|scenarios/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/task_method_map|task_method_map]]、[[../relations/concept_links|concept_links]]、[[../relations/benchmark_links|benchmark_links]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 任务入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 2: Add the standard scenario navigation block to both scenario pages**

Insert this block immediately after frontmatter in every file under `wiki/scenarios/`:

```md
> 导航：返回 [[index|scenarios/index]]；相关对象域 [[../tasks/index|tasks/index]]、[[../methods/index|methods/index]]、[[../concepts/index|concepts/index]]、[[../papers/index|papers/index]]。
>
> 相关 relation ledger：[[../relations/concept_links|concept_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready 场景入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 3: Add the standard benchmark navigation block to both benchmark pages**

Insert this block immediately after frontmatter in every file under `wiki/benchmarks/`:

```md
> 导航：返回 [[index|benchmarks/index]]；相关对象域 [[../tasks/index|tasks/index]]、[[../methods/index|methods/index]]、[[../papers/index|papers/index]]、[[../scenarios/index|scenarios/index]]。
>
> 相关 relation ledger：[[../relations/benchmark_links|benchmark_links]]、[[../relations/task_method_map|task_method_map]]、[[../relations/evidence_index|evidence_index]]。
>
> 本页是默认 serving-ready benchmark 入口；formal graph truth 以 relation ledger 为准，证据细节下钻 `intermediate/papers/`。
```

- [ ] **Step 4: Run lint after the task/scenario/benchmark retrofit**

Run: `python3 scripts/lint_graph.py`
Expected: PASS.

- [ ] **Step 5: Commit the task/scenario/benchmark retrofit**

```bash
git add wiki/tasks/*.md wiki/scenarios/*.md wiki/benchmarks/*.md
git commit -m "docs: add navigation blocks to task scenario benchmark pages"
```

### Task 8: Verify navigation closure end to end

**Files:**
- Modify: none unless a minimal wording fix is needed
- Test: `python3 scripts/lint_graph.py`
- Test: `git diff --stat`
- Test: `git status --short`

- [ ] **Step 1: Run graph lint on the final state**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Manually verify the representative navigation path for the PathMind line**

Open and inspect this path in order:
1. `wiki/ontology/index.md`
2. `wiki/methods/index.md`
3. `wiki/methods/PathMind.md`
4. `wiki/relations/method_evolution.md`
5. `wiki/relations/task_method_map.md`
6. `wiki/relations/concept_links.md`
7. `wiki/relations/benchmark_links.md`
8. `intermediate/papers/PathMind.sections`

Confirm all of these are now true:
- ontology index points to the methods index
- methods index points to `PathMind`
- `PathMind.md` points back to methods index and out to the relevant ledgers
- the ledgers point back to the appropriate object-domain indexes
- evidence links remain reachable from the object page and the ledgers

- [ ] **Step 3: Manually verify the representative navigation path for the survey/framework line**

Open and inspect this path in order:
1. `wiki/ontology/index.md`
2. `wiki/papers/index.md`
3. `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
4. `wiki/concepts/index.md`
5. `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
6. `wiki/relations/paper_method_links.md`
7. `wiki/relations/concept_links.md`
8. `intermediate/papers/LLM-KG-CPD-Survey.sections`

Confirm all of these are now true:
- ontology index points to the papers index and concepts index
- the survey paper points to its related concept/object domains and ledgers
- the framework concept points back to concepts index and out to the right ledgers
- the ledgers explain they are governance truth, not the default reading entry
- evidence drill-down remains intact

- [ ] **Step 4: Verify the edit scope before handoff**

Run: `git diff --stat`
Expected: only navigation docs, relation ledgers, object-domain indexes, and entity-page navigation blocks changed.

Run: `git status --short`
Expected: modified files limited to the planned scope; no unrelated new files beyond the six indexes.

- [ ] **Step 5: Keep the branch ready for review and do not auto-commit anything beyond the task commits**

There is no extra code step here. Stop after verification and present the diff summary for review.
