# Materialize Strong Survey-Covered Methods for LLM-KG-CPD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Materialize the strongest eight survey-covered methods from the LLM-KG-CPD survey as partial Method pages and connect them with formal `surveys_method` relations.

**Architecture:** Add eight minimal `status: partial` Method pages, each admitted by one `surveys_method` edge from the survey paper and one `supported_by` edge to existing survey evidence. Then project those ledgers back into object pages, sync the methods index, and run lint plus governance checks without expanding into full paper ingest or downstream method relations.

**Tech Stack:** Obsidian Markdown pages, ResearchKB relation ledgers, Python graph lint script, Claude Code skills for projection/index/governance sync

---

## File map

### Create
- `ontology/entities/methods/BEAR.md` — partial Method page for BEAR
- `ontology/entities/methods/AutoKG.md` — partial Method page for AutoKG
- `ontology/entities/methods/ASKG.md` — partial Method page for ASKG
- `ontology/entities/methods/OLaLa.md` — partial Method page for OLaLa
- `ontology/entities/methods/KG-CGT.md` — partial Method page for KG-CGT
- `ontology/entities/methods/RelMKG.md` — partial Method page for RelMKG
- `ontology/entities/methods/StructGPT.md` — partial Method page for StructGPT
- `ontology/entities/methods/CausalKGPT.md` — partial Method page for CausalKGPT
- `docs/superpowers/checks/2026-05-13-llm-kg-cpd-surveys-method-smoke.md` — one-off verification checklist for this batch

### Modify
- `ontology/relations/surveys_method.md` — add eight Paper→Method survey coverage relations
- `ontology/relations/supported_by.md` — add eight Method→Evidence support relations
- `ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md` — refresh projections after ledger updates
- `ontology/entities/methods/index.md` — add eight new partial Method entries via managed block sync
- `ontology/log.md` — record the batch materialization

### Reuse without modification unless projection skills rewrite them
- `ontology/entities/evidence/LLM-KG-CPD.analysis.md`
- `ontology/entities/evidence/LLM-KG-CPD.refs.md`
- `ontology/relations/proposes.md`

---

### Task 1: Create the first four partial Method pages

**Files:**
- Create: `ontology/entities/methods/BEAR.md`
- Create: `ontology/entities/methods/AutoKG.md`
- Create: `ontology/entities/methods/ASKG.md`
- Create: `ontology/entities/methods/OLaLa.md`
- Test: `docs/superpowers/checks/2026-05-13-llm-kg-cpd-surveys-method-smoke.md`

- [ ] **Step 1: Write the failing checklist expectation**

```markdown
# LLM-KG-CPD surveys_method smoke check

## Expected missing files before implementation
- ontology/entities/methods/BEAR.md
- ontology/entities/methods/AutoKG.md
- ontology/entities/methods/ASKG.md
- ontology/entities/methods/OLaLa.md
```

- [ ] **Step 2: Run file existence check to verify failure**

Run: `for f in ontology/entities/methods/BEAR.md ontology/entities/methods/AutoKG.md ontology/entities/methods/ASKG.md ontology/entities/methods/OLaLa.md; do test -f "$f" && echo "UNEXPECTED $f exists" || echo "MISSING $f"; done`
Expected: four `MISSING ...` lines

- [ ] **Step 3: Write BEAR.md minimal partial page**

```markdown
---
title: BEAR
type: 集成方法
parent_methods: []
child_methods: []
problem: [graph-construction, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# BEAR

## Object semantics
BEAR 是一个利用大语言模型推进服务域知识图谱构建的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 BEAR 纳入 LLM 增强 KG construction 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
BEAR 代表一类以 LLM 参与知识图谱构建流程的命名方法对象。

## 待补充
后续需要独立 ingest BEAR 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 4: Write AutoKG.md minimal partial page**

```markdown
---
title: AutoKG
type: 集成方法
parent_methods: []
child_methods: []
problem: [graph-construction, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# AutoKG

## Object semantics
AutoKG 是一个面向知识图谱自动生成的 LLM-enhanced Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 AutoKG 纳入 LLM 增强 KG construction 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
AutoKG 代表一类把知识图谱生成过程自动化的命名方法对象。

## 待补充
后续需要独立 ingest AutoKG 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 5: Write ASKG.md minimal partial page**

```markdown
---
title: ASKG
type: 集成方法
parent_methods: []
child_methods: []
problem: [graph-construction, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# ASKG

## Object semantics
ASKG 是一个通过论文分解增强 scholarly knowledge graph 的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 ASKG 纳入 LLM 增强 knowledge extraction / graph enrichment 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
ASKG 代表一类利用学习与分解流程丰富知识图谱内容的命名方法对象。

## 待补充
后续需要独立 ingest ASKG 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 6: Write OLaLa.md minimal partial page**

```markdown
---
title: OLaLa
type: 集成方法
parent_methods: []
child_methods: []
problem: [ontology-alignment, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# OLaLa

## Object semantics
OLaLa 是一个利用大语言模型进行 ontology matching 的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 OLaLa 纳入 knowledge fusion / ontology matching 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
OLaLa 代表一类把 LLM 用于 ontology matching 与知识融合的命名方法对象。

## 待补充
后续需要独立 ingest OLaLa 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 7: Run file existence check to verify creation**

Run: `for f in ontology/entities/methods/BEAR.md ontology/entities/methods/AutoKG.md ontology/entities/methods/ASKG.md ontology/entities/methods/OLaLa.md; do test -f "$f" && echo "PASS $f" || echo "FAIL $f"; done`
Expected: four `PASS ...` lines

- [ ] **Step 8: Commit**

```bash
git add docs/superpowers/checks/2026-05-13-llm-kg-cpd-surveys-method-smoke.md \
  ontology/entities/methods/BEAR.md \
  ontology/entities/methods/AutoKG.md \
  ontology/entities/methods/ASKG.md \
  ontology/entities/methods/OLaLa.md
git commit -m "feat: add first LLM-KG-CPD survey methods"
```

### Task 2: Create the second four partial Method pages

**Files:**
- Create: `ontology/entities/methods/KG-CGT.md`
- Create: `ontology/entities/methods/RelMKG.md`
- Create: `ontology/entities/methods/StructGPT.md`
- Create: `ontology/entities/methods/CausalKGPT.md`
- Test: `docs/superpowers/checks/2026-05-13-llm-kg-cpd-surveys-method-smoke.md`

- [ ] **Step 1: Extend the checklist with the remaining missing files**

```markdown
## Expected missing files before Task 2
- ontology/entities/methods/KG-CGT.md
- ontology/entities/methods/RelMKG.md
- ontology/entities/methods/StructGPT.md
- ontology/entities/methods/CausalKGPT.md
```

- [ ] **Step 2: Run file existence check to verify failure**

Run: `for f in ontology/entities/methods/KG-CGT.md ontology/entities/methods/RelMKG.md ontology/entities/methods/StructGPT.md ontology/entities/methods/CausalKGPT.md; do test -f "$f" && echo "UNEXPECTED $f exists" || echo "MISSING $f"; done`
Expected: four `MISSING ...` lines

- [ ] **Step 3: Write KG-CGT.md minimal partial page**

```markdown
---
title: KG-CGT
type: 集成方法
parent_methods: []
child_methods: []
problem: [knowledge-acquisition, reasoning]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# KG-CGT

## Object semantics
KG-CGT 是一个通过 knowledge-graph guidance 支持内容生成的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 KG-CGT 纳入 LLM 与 KG 协同生成路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
KG-CGT 代表一类以知识图谱指导生成过程的命名方法对象。

## 待补充
后续需要独立 ingest KG-CGT 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 4: Write RelMKG.md minimal partial page**

```markdown
---
title: RelMKG
type: 集成方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# RelMKG

## Object semantics
RelMKG 是一个结合预训练语言模型与知识图谱进行复杂问答推理的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 RelMKG 纳入 knowledge reasoning 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
RelMKG 代表一类把语言模型与知识图谱耦合用于复杂 reasoning / QA 的命名方法对象。

## 待补充
后续需要独立 ingest RelMKG 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 5: Write StructGPT.md minimal partial page**

```markdown
---
title: StructGPT
type: 集成方法
parent_methods: []
child_methods: []
problem: [reasoning, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [general]
research_role: [integrated]
status: partial
---

# StructGPT

## Object semantics
StructGPT 是一个面向结构化数据推理的大语言模型框架型 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 StructGPT 纳入 knowledge reasoning 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
StructGPT 代表一类围绕 structured data reasoning 组织 LLM 推理流程的命名方法对象。

## 待补充
后续需要独立 ingest StructGPT 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 6: Write CausalKGPT.md minimal partial page**

```markdown
---
title: CausalKGPT
type: 集成方法
parent_methods: []
child_methods: []
problem: [reasoning, knowledge-acquisition]
method_family: [hybrid, llm]
scenario: []
research_task: []
industry: [manufacturing]
research_role: [integrated]
status: partial
---

# CausalKGPT

## Object semantics
CausalKGPT 是一个用因果知识增强大语言模型进行工业质量问题分析的 Method 实例。

## 当前定位
该页面由 LLM-KG-CPD survey 的结构化方法 coverage 支撑，当前先作为 partial Method materialize，等待后续独立 ingest 原论文。

## 与知识库现有内容的关系
当前知识库通过 LLM-KG-CPD survey 把 CausalKGPT 纳入 manufacturing-oriented knowledge reasoning 路线，用于补齐 survey paper 到 method graph 的 formal coverage。

## 最小定义/角色
CausalKGPT 代表一类以因果知识图谱增强语言模型分析复杂工业问题的命名方法对象。

## 待补充
后续需要独立 ingest CausalKGPT 原论文，以补齐方法原理、任务归属、场景与更细粒度 formal relations。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
```

- [ ] **Step 7: Run file existence check to verify creation**

Run: `for f in ontology/entities/methods/KG-CGT.md ontology/entities/methods/RelMKG.md ontology/entities/methods/StructGPT.md ontology/entities/methods/CausalKGPT.md; do test -f "$f" && echo "PASS $f" || echo "FAIL $f"; done`
Expected: four `PASS ...` lines

- [ ] **Step 8: Commit**

```bash
git add ontology/entities/methods/KG-CGT.md \
  ontology/entities/methods/RelMKG.md \
  ontology/entities/methods/StructGPT.md \
  ontology/entities/methods/CausalKGPT.md
git commit -m "feat: add remaining LLM-KG-CPD survey methods"
```

### Task 3: Add formal support relations for the eight methods

**Files:**
- Modify: `ontology/relations/supported_by.md`
- Test: `ontology/entities/evidence/LLM-KG-CPD.analysis.md`
- Test: `ontology/entities/evidence/LLM-KG-CPD.refs.md`

- [ ] **Step 1: Write the expected missing edges in the smoke checklist**

```markdown
## Expected supported_by edges to add
- [[BEAR]] --supported_by--> [[LLM-KG-CPD.refs]]
- [[AutoKG]] --supported_by--> [[LLM-KG-CPD.refs]]
- [[ASKG]] --supported_by--> [[LLM-KG-CPD.refs]]
- [[OLaLa]] --supported_by--> [[LLM-KG-CPD.analysis]]
- [[KG-CGT]] --supported_by--> [[LLM-KG-CPD.analysis]]
- [[RelMKG]] --supported_by--> [[LLM-KG-CPD.analysis]]
- [[StructGPT]] --supported_by--> [[LLM-KG-CPD.analysis]]
- [[CausalKGPT]] --supported_by--> [[LLM-KG-CPD.analysis]]
```

- [ ] **Step 2: Run grep to verify the edges are absent**

Run: `grep -n "\[\[BEAR\]\]\|\[\[AutoKG\]\]\|\[\[ASKG\]\]\|\[\[OLaLa\]\]\|\[\[KG-CGT\]\]\|\[\[RelMKG\]\]\|\[\[StructGPT\]\]\|\[\[CausalKGPT\]\]" ontology/relations/supported_by.md || true`
Expected: no output

- [ ] **Step 3: Append the first four `supported_by` ledger entries**

```markdown
- [[BEAR]] --supported_by--> [[LLM-KG-CPD.refs]]
  - source_path: ontology/entities/methods/BEAR.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
  - edge_semantics: BEAR 在该 survey 中被纳入 LLM 增强 KG construction 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[AutoKG]] --supported_by--> [[LLM-KG-CPD.refs]]
  - source_path: ontology/entities/methods/AutoKG.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
  - edge_semantics: AutoKG 在该 survey 中被纳入 LLM 增强 KG construction 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[ASKG]] --supported_by--> [[LLM-KG-CPD.refs]]
  - source_path: ontology/entities/methods/ASKG.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
  - edge_semantics: ASKG 在该 survey 中被纳入 knowledge extraction / graph enrichment 的结构化方法 coverage，当前由 refs 缓存中的文献 grounding 直接支撑。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[OLaLa]] --supported_by--> [[LLM-KG-CPD.analysis]]
  - source_path: ontology/entities/methods/OLaLa.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
  - edge_semantics: OLaLa 在该 survey 的结构化 role-based coverage 中被纳入 knowledge fusion / ontology matching 路线，当前由 analysis 缓存直接支撑。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
```

- [ ] **Step 4: Append the second four `supported_by` ledger entries**

```markdown
- [[KG-CGT]] --supported_by--> [[LLM-KG-CPD.analysis]]
  - source_path: ontology/entities/methods/KG-CGT.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
  - edge_semantics: KG-CGT 在该 survey 的结构化 role-based coverage 中被纳入 KG-guided generation 路线，当前由 analysis 缓存直接支撑。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[RelMKG]] --supported_by--> [[LLM-KG-CPD.analysis]]
  - source_path: ontology/entities/methods/RelMKG.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
  - edge_semantics: RelMKG 在该 survey 的结构化 role-based coverage 中被纳入 knowledge reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[StructGPT]] --supported_by--> [[LLM-KG-CPD.analysis]]
  - source_path: ontology/entities/methods/StructGPT.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
  - edge_semantics: StructGPT 在该 survey 的结构化 role-based coverage 中被纳入结构化数据 reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[CausalKGPT]] --supported_by--> [[LLM-KG-CPD.analysis]]
  - source_path: ontology/entities/methods/CausalKGPT.md
  - target_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
  - edge_semantics: CausalKGPT 在该 survey 的结构化 role-based coverage 中被纳入 manufacturing-oriented knowledge reasoning 路线，当前由 analysis 缓存直接支撑。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
```

- [ ] **Step 5: Run grep to verify the edges were added**

Run: `grep -n "\[\[BEAR\]\]\|\[\[AutoKG\]\]\|\[\[ASKG\]\]\|\[\[OLaLa\]\]\|\[\[KG-CGT\]\]\|\[\[RelMKG\]\]\|\[\[StructGPT\]\]\|\[\[CausalKGPT\]\]" ontology/relations/supported_by.md`
Expected: eight ledger edge hits

- [ ] **Step 6: Commit**

```bash
git add ontology/relations/supported_by.md
git commit -m "feat: support survey-covered LLM-KG-CPD methods"
```

### Task 4: Add formal `surveys_method` relations and update log

**Files:**
- Modify: `ontology/relations/surveys_method.md`
- Modify: `ontology/log.md`
- Test: `ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`

- [ ] **Step 1: Write the expected `surveys_method` edges in the smoke checklist**

```markdown
## Expected surveys_method edges to add
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[BEAR]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[AutoKG]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[ASKG]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[OLaLa]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[KG-CGT]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[RelMKG]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[StructGPT]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[CausalKGPT]]
```

- [ ] **Step 2: Run grep to verify the ledger is still empty**

Run: `grep -n "A survey of large language model-augmented knowledge graphs for advanced complex product design" ontology/relations/surveys_method.md || true`
Expected: no instance-edge output

- [ ] **Step 3: Replace the empty instance block with the eight ledger entries**

```markdown
## 实例边
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[BEAR]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/BEAR.md
  - edge_semantics: 该 survey 将 BEAR 纳入 LLM 增强 KG construction 的结构化方法 coverage，用于组织复杂产品设计中的知识图谱构建路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[AutoKG]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/AutoKG.md
  - edge_semantics: 该 survey 将 AutoKG 纳入 LLM 增强 KG construction 的结构化方法 coverage，用于组织复杂产品设计中的知识图谱自动生成路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[ASKG]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/ASKG.md
  - edge_semantics: 该 survey 将 ASKG 纳入 graph enrichment / scholarly KG enhancement 的结构化方法 coverage，用于组织相关知识抽取与图谱增强路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.refs
  - evidence_link: [[LLM-KG-CPD.refs]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.refs.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[OLaLa]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/OLaLa.md
  - edge_semantics: 该 survey 将 OLaLa 纳入 knowledge fusion / ontology matching 的结构化方法 coverage，用于组织 LLM 增强知识融合路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[KG-CGT]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/KG-CGT.md
  - edge_semantics: 该 survey 将 KG-CGT 纳入 KG-guided generation 的结构化方法 coverage，用于组织 LLM 与 KG 协同生成路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[RelMKG]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/RelMKG.md
  - edge_semantics: 该 survey 将 RelMKG 纳入 knowledge reasoning 的结构化方法 coverage，用于组织知识图谱增强语言模型推理路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[StructGPT]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/StructGPT.md
  - edge_semantics: 该 survey 将 StructGPT 纳入结构化数据 reasoning 的结构化方法 coverage，用于组织面向结构化数据的 LLM 推理路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[CausalKGPT]]
  - source_path: ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md
  - target_path: ontology/entities/methods/CausalKGPT.md
  - edge_semantics: 该 survey 将 CausalKGPT 纳入 manufacturing-oriented knowledge reasoning 的结构化方法 coverage，用于组织复杂产品设计中的工业因果分析路线，而不是把它作为首次提出的方法。
  - evidence: LLM-KG-CPD.analysis
  - evidence_link: [[LLM-KG-CPD.analysis]]
  - evidence_path: ontology/entities/evidence/LLM-KG-CPD.analysis.md
```

- [ ] **Step 4: Record the batch in ontology/log.md**

```markdown
- 2026-05-13：基于 LLM-KG-CPD survey 的结构化 coverage，新 materialize 八个 partial Method（BEAR、AutoKG、ASKG、OLaLa、KG-CGT、RelMKG、StructGPT、CausalKGPT），并补齐 `surveys_method` 与 `supported_by` formal relations。
```

- [ ] **Step 5: Run grep to verify the eight new survey edges exist**

Run: `grep -n "surveys_method--> \[\[BEAR\]\]\|surveys_method--> \[\[AutoKG\]\]\|surveys_method--> \[\[ASKG\]\]\|surveys_method--> \[\[OLaLa\]\]\|surveys_method--> \[\[KG-CGT\]\]\|surveys_method--> \[\[RelMKG\]\]\|surveys_method--> \[\[StructGPT\]\]\|surveys_method--> \[\[CausalKGPT\]\]" ontology/relations/surveys_method.md`
Expected: eight ledger edge hits

- [ ] **Step 6: Commit**

```bash
git add ontology/relations/surveys_method.md ontology/log.md
git commit -m "feat: admit survey-covered LLM-KG-CPD methods"
```

### Task 5: Sync projections, index, and run governance verification

**Files:**
- Modify: `ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `ontology/entities/methods/BEAR.md`
- Modify: `ontology/entities/methods/AutoKG.md`
- Modify: `ontology/entities/methods/ASKG.md`
- Modify: `ontology/entities/methods/OLaLa.md`
- Modify: `ontology/entities/methods/KG-CGT.md`
- Modify: `ontology/entities/methods/RelMKG.md`
- Modify: `ontology/entities/methods/StructGPT.md`
- Modify: `ontology/entities/methods/CausalKGPT.md`
- Modify: `ontology/entities/methods/index.md`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run page projection sync for the survey paper and the eight methods**

Run:
```bash
claude code --print "/skill page-projection-sync ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md ontology/entities/methods/BEAR.md ontology/entities/methods/AutoKG.md ontology/entities/methods/ASKG.md ontology/entities/methods/OLaLa.md ontology/entities/methods/KG-CGT.md ontology/entities/methods/RelMKG.md ontology/entities/methods/StructGPT.md ontology/entities/methods/CausalKGPT.md"
```
Expected: success report listing the survey paper and eight Method pages as synced

- [ ] **Step 2: Run index sync for the methods index**

Run:
```bash
claude code --print "/skill index-sync ontology/entities/methods/BEAR.md ontology/entities/methods/AutoKG.md ontology/entities/methods/ASKG.md ontology/entities/methods/OLaLa.md ontology/entities/methods/KG-CGT.md ontology/entities/methods/RelMKG.md ontology/entities/methods/StructGPT.md ontology/entities/methods/CausalKGPT.md"
```
Expected: success report showing `ontology/entities/methods/index.md` in `synced_indexes`

- [ ] **Step 3: Verify one representative Method page projection**

Run: `grep -n "surveys_method\|supported_by" ontology/entities/methods/BEAR.md`
Expected: one incoming `surveys_method` projection and one outgoing `supported_by` projection

- [ ] **Step 4: Verify the survey paper now projects outgoing survey coverage**

Run: `grep -n "surveys_method" "ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md"`
Expected: eight `surveys_method` projection hits

- [ ] **Step 5: Run graph lint**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Run ontology semantic review**

Run:
```bash
claude code --print "/skill ontology-semantic-review A survey of large language model-augmented knowledge graphs for advanced complex product design"
```
Expected: review report with `pass` or `pass-with-issues`, but no fail verdict on misused `surveys_method`

- [ ] **Step 7: Run serving governance review**

Run:
```bash
claude code --print "/skill serving-governance-review A survey of large language model-augmented knowledge graphs for advanced complex product design"
```
Expected: `pass` or `needs_fixes`; if `needs_fixes`, capture the exact pages before any further change

- [ ] **Step 8: Commit**

```bash
git add ontology/entities/papers/A\ survey\ of\ large\ language\ model-augmented\ knowledge\ graphs\ for\ advanced\ complex\ product\ design.md \
  ontology/entities/methods/BEAR.md \
  ontology/entities/methods/AutoKG.md \
  ontology/entities/methods/ASKG.md \
  ontology/entities/methods/OLaLa.md \
  ontology/entities/methods/KG-CGT.md \
  ontology/entities/methods/RelMKG.md \
  ontology/entities/methods/StructGPT.md \
  ontology/entities/methods/CausalKGPT.md \
  ontology/entities/methods/index.md
git commit -m "feat: project survey-covered LLM-KG-CPD methods"
```
