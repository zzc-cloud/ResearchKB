# CLAUDE Ontology Cognition Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `CLAUDE.md` so ontology cognition is split into ontology semantics, ontology layered structure, and ontology entry points, with explicit semantic descriptions of ontology objects and relation families for AI consumption.

**Architecture:** Keep all changes localized to `CLAUDE.md`. Replace the current mixed “本体认知” section with a three-part structure: first explain ontology object and relation semantics, then explain the layered architecture, then list the stable entry points. Preserve `ontology/graph-standard.md` as the normative authority by describing its role without duplicating rule details.

**Tech Stack:** Markdown, Obsidian wikilinks, ResearchKB ontology vocabulary, local grep-based verification.

---

## File map

- Modify: `CLAUDE.md`
  - Replace the current mixed ontology cognition section with a three-part structure
  - Add explicit object semantics and relation-family semantics
  - Separate layered-architecture description from entry-point lists
- Verify: `ontology/graph-standard.md`
  - Reference only as normative authority; do not modify in this task
- Test: `grep` on `CLAUDE.md`
- Test: manual read-through of the rewritten ontology cognition section

---

### Task 1: Rewrite `CLAUDE.md` ontology cognition into three sections

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read the current ontology cognition block before editing**

Confirm the current section still mixes:
- semantics-lite language
- layered architecture
- stable entry lists

Focus on the block from `## 本体认知` down to the `---` immediately before `## 全局认知`.

- [ ] **Step 2: Replace the entire current ontology cognition block with the approved three-part structure**

Replace the whole current `## 本体认知` block with this exact content:

```md
## 本体认知
- 本体认知是全局认知的核心认知底座。
- `CLAUDE.md` 负责给 AI 提供系统级本体认知入口：先理解本体中有什么对象与关系，再理解这些对象与关系如何分层组织，最后理解应从哪些稳定入口进入本体。

### 1. 本体语义描述

#### 1.1 对象语义
- `Paper`：可引用、可追溯的论文研究产物，是研究主张、方法提出与证据挂接的论文载体。
- `Method`：可复用的方法机制或技术路径，承载方法演化、任务适配与技术路线比较语义。
- `Concept`：概念、框架、taxonomy 等知识组织单元，承载定义、分类、框架解释与概念网络语义。
- `Task`：研究任务，承载“要解决什么问题”的任务抽象。
- `Scenario`：应用场景，承载“在哪种业务或应用上下文中使用”的场景语义。
- `Benchmark`：评测基准或数据集，承载“如何评价方法或论文”的评测语义。
- `Evidence`：结构化证据缓存，承载章节、实验、引用、分析等可回溯证据。
- `RawSource`：原始来源文件，只承担 provenance 与必要时回查职责，不承担默认知识组织职责。

这些对象不是目录分类，而是本体中的语义角色。

#### 1.2 关系语义
- 提出 / 产出关系：`proposes`
  - 表示论文提出了某个方法、概念或框架。
- 概念使用关系：`uses_concept`
  - 表示方法、论文或其他对象依赖某概念。
- 任务 / 场景指向关系：`targets_task`、`applies_to`
  - 表示方法或论文面向什么任务、适用于什么场景。
- 支持关系：`supports`、`supported_by`
  - 表示对象之间的支撑关系，以及对象与证据之间的证据支撑关系。
- 评测关系：`evaluated_on`
  - 表示方法或论文在哪些 benchmark 上被评估。
- 引用与来源关系：`cites`、`sourced_from`
  - 前者是论文间知识引用，后者是 evidence 到 raw source 的 provenance 绑定。
- 演化关系：method evolution 账本中的父子 / 上下游方法关系
  - 用于表达方法路线如何延展、继承或分化。

这些关系不是普通链接，而是在表达研究对象之间的不同语义连接。

### 2. 本体分层结构描述
- 规范层：`ontology/graph-standard.md`
  - 负责节点归类、关系合法性、frontmatter 受控字段、证据义务与豁免规则。
  - 它是唯一规范裁决依据，不是默认问答入口。
- 对象层：`ontology/entities/*/index.md` 与 serving-ready 对象页
  - 负责正式知识对象发现与默认问答读取。
  - 对象页中的 `Formal relations` 是默认的受约束拓扑扩展面。
- 关系层：`ontology/relations/*.md`
  - 负责 formal relation ledger、治理、修复、审计与 truth 校对。
  - 不作为所有问答的默认首入口。
- 证据层：`intermediate/papers/`
  - 负责机制、实验、引用、baseline、provenance 的核验。
  - 是对象层与关系层之下的证据支撑层。
- 原始来源层：`raw/`
  - 只承担原始来源回查职责，不进入默认导航主链。

### 3. 本体入口描述

#### 3.1 规范与判定入口
- 唯一规范页：[[graph-standard]]
- 所有节点、关系、字段、证据与豁免规则，一律以 [[graph-standard]] 为准。

#### 3.2 正式关系入口
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[paper_method_links]]
- [[benchmark_links]]
- [[provenance_links]]

#### 3.3 正式知识对象域入口
- Papers：[[entities/papers/index|ontology/entities/papers/index.md]]
- Methods：[[entities/methods/index|ontology/entities/methods/index.md]]
- Concepts：[[entities/concepts/index|ontology/entities/concepts/index.md]]
- Tasks：[[entities/tasks/index|ontology/entities/tasks/index.md]]
- Scenarios：[[entities/scenarios/index|ontology/entities/scenarios/index.md]]
- Benchmarks：[[entities/benchmarks/index|ontology/entities/benchmarks/index.md]]

#### 3.4 证据与原始来源入口
- 证据入口：`intermediate/papers/`
- 原始来源入口：`raw/`
```

- [ ] **Step 3: Verify the section split is explicit and complete**

Run:

```bash
grep -n "### 1\. 本体语义描述\|#### 1\.1 对象语义\|#### 1\.2 关系语义\|### 2\. 本体分层结构描述\|### 3\. 本体入口描述\|#### 3\.2 正式关系入口\|#### 3\.3 正式知识对象域入口" CLAUDE.md
```

Expected:
- One match for each required subsection heading
- No missing subsection labels

- [ ] **Step 4: Verify key ontology semantics are present**

Run:

```bash
grep -n "`Paper`：可引用、可追溯的论文研究产物\|`Method`：可复用的方法机制或技术路径\|`proposes`\|`supported_by`\|这些对象不是目录分类\|这些关系不是普通链接" CLAUDE.md
```

Expected:
- Matches for object semantics
- Matches for relation-family semantics
- Matches for the two explanatory summary lines

---

### Task 2: Verify the rewritten ontology cognition reads cleanly against the current workflow sections

**Files:**
- Verify: `CLAUDE.md`

- [ ] **Step 1: Check that the ontology cognition section no longer mixes layered structure and entry lists in the same subsection**

Run:

```bash
grep -n "### 规范与判定入口\|### 正式关系入口\|### 正式知识对象域入口\|### 证据与原始来源入口" CLAUDE.md
```

Expected:
- No matches, because those headings should now live under `### 3. 本体入口描述` as `####`-level subsections instead of being interleaved with layered-structure bullets

- [ ] **Step 2: Manually read the final structure in order**

Read the final `## 本体认知` section and confirm it now answers, in order:
1. 本体里有什么对象和关系
2. 这些对象和关系被组织在哪些层
3. 从哪些稳定入口进入这些层

Expected:
- The reading order is clear without jumping between semantics, layering, and entry lists
- `ontology/graph-standard.md` is described as the normative authority, not rewritten inline

- [ ] **Step 3: Verify the query workflow still points to the layered model consistently**

Run:

```bash
grep -n "先依据 `CLAUDE.md` 的本体分层导航" CLAUDE.md
```

Expected:
- One match in `### 查询与分析`
- The wording still aligns with the new `### 2. 本体分层结构描述`

---

## Self-review checklist

- Spec coverage:
  - ontology semantics added: Task 1
  - layered architecture separated from entry lists: Task 1
  - stable entry points preserved under a dedicated entry section: Task 1
  - workflow consistency checked after rewrite: Task 2
- Placeholder scan:
  - No `TODO`, `TBD`, or deferred wording
  - All replacement content and verification commands are concrete
- Consistency check:
  - `ontology/graph-standard.md` remains the normative authority
  - semantics, structure, and entry points are described in three distinct sections
  - current workflow text still references layered navigation consistently
