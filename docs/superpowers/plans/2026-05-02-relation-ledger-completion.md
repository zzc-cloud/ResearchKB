# Relation Ledger Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Assign official ledgers for `proposes`, `evaluated_on`, and `sourced_from`, backfill the two existing ingested papers with those edges, and add lint guardrails so future ingests cannot silently omit the same relations.

**Architecture:** Keep the ontology stable and extend only the instance-edge layer. Add one ledger for paper-to-method/concept proposal edges, one for benchmark evaluation edges, and one for provenance edges; then narrow `evidence_index.md` back to `supported_by` only and teach `scripts/lint_graph.py` to require the new files plus representative seeded edges.

**Tech Stack:** Markdown knowledge base, Python 3 lint script, git

---

## File Structure

### Files to modify
- `wiki/ontology/graph-standard.md`
  - Broaden `proposes` to allow framework/taxonomy concepts, assign all three relation types to ledger files, and expose the new ledgers in the relation index.
- `wiki/relations/evidence_index.md`
  - Keep only `supported_by` edges and update the notes so provenance no longer lives here.
- `wiki/index.md`
  - Add the three new relation ledgers to top-level navigation and relation-object navigation.
- `scripts/lint_graph.py`
  - Require the new ledger files, assert the seeded edges exist, and forbid `sourced_from` from remaining in `evidence_index.md`.

### Files to create
- `wiki/relations/paper_method_links.md`
  - Formal ledger for `proposes` edges from papers to methods or framework/taxonomy concepts.
- `wiki/relations/benchmark_links.md`
  - Formal ledger for `evaluated_on` edges from papers/methods to benchmarks.
- `wiki/relations/provenance_links.md`
  - Formal ledger for `sourced_from` edges from evidence caches to raw PDFs.

### Files used as evidence during implementation
- `intermediate/papers/PathMind.sections.md`
- `intermediate/papers/PathMind.experiments.md`
- `intermediate/papers/PathMind.refs.md`
- `intermediate/papers/PathMind.full.md`
- `intermediate/papers/LLM-KG-CPD-Survey.sections.md`
- `intermediate/papers/LLM-KG-CPD-Survey.analysis.md`
- `intermediate/papers/LLM-KG-CPD-Survey.refs.md`
- `intermediate/papers/LLM-KG-CPD-Survey.full.md`

---

### Task 1: Assign relation ownership in the ontology spec

**Files:**
- Modify: `wiki/ontology/graph-standard.md:233-337`
- Test: `wiki/ontology/graph-standard.md`

- [ ] **Step 1: Run a failing check to capture the current mismatch**

```bash
grep -n "未归属\|paper_method_links\|benchmark_links\|provenance_links\|`proposes`：`\[\[Paper\]\] --proposes--> \[\[Method\]\]`" wiki/ontology/graph-standard.md
```

Expected: output includes the current “未归属” line for `proposes` / `evaluated_on`, does **not** include the three new ledger filenames in the relation-file assignment section, and shows `proposes` limited to `[[Method]]`.

- [ ] **Step 2: Update the relation definitions and file assignments**

Replace the relation-definition and file-assignment snippets with the following content:

```md
- `proposes`：`[[Paper]] --proposes--> [[Method|Concept]]`；表示论文首次提出或正式定义某方法，或提出 framework / taxonomy 型核心概念。
- `uses_concept`：`[[Paper|Method]] --uses_concept--> [[Concept]]`；表示论文或方法在定义、建模、机制设计或实现上依赖某概念。方法与概念之间的正式关系默认优先使用该边，而不是 `based_on`。
- `targets_task`：`[[Paper|Method]] --targets_task--> [[Task]]`；表示论文或方法主要面向的研究任务。
- `applies_to`：`[[Method|Concept]] --applies_to--> [[Scenario]]`；表示方法或框架型概念面向的应用场景。
- `evaluated_on`：`[[Paper|Method]] --evaluated_on--> [[Benchmark]]`；表示论文或方法在某基准上进行评测。
- `improves_on`：`[[Method]] --improves_on--> [[Method]]`；表示方法对既有方法形成明确改进。
- `based_on`：`[[Method]] --based_on--> [[Method]]`；表示方法建立在某个上游方法之上，只用于方法演化谱系，不指向概念、框架或场景。
- `cites`：`[[Paper]] --cites--> [[Paper]]`；表示论文对论文的显式引用。
- `supported_by`：`[[Paper|Method|Concept|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`；表示正式知识页由证据缓存支撑。
- `sourced_from`：`[[Evidence]] --sourced_from--> [[RawSource]]`；表示证据缓存来源于 `raw/` 下的原始文件。RawSource 节点默认使用 `[[raw/文件名.pdf]]` 形式命名，以保持与 `source_pdf` 路径和 provenance 账本一致。该关系默认主要落在 provenance 层，不要求正式知识页直接连接原始来源；若缓存尚未生成而必须临时登记来源，可例外使用 `status: placeholder` 暂存。
```

```md
## 关系文件分工
- 首批进入正式实例边层并已归属维护文件的关系类型如下：
  - `wiki/relations/citation_graph.md`：维护 `cites`
  - `wiki/relations/method_evolution.md`：维护 `based_on`、`improves_on`
  - `wiki/relations/task_method_map.md`：维护 `targets_task`
  - `wiki/relations/concept_links.md`：维护 `uses_concept`、`supports`、`depends_on`，以及 concept / paper / method 到 concept 或 scenario 的补充语义边
  - `wiki/relations/paper_method_links.md`：维护 `proposes`
  - `wiki/relations/benchmark_links.md`：维护 `evaluated_on`
  - `wiki/relations/evidence_index.md`：维护 `supported_by`
  - `wiki/relations/provenance_links.md`：维护 `sourced_from`
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 边；若出现正式知识页到 RawSource 的临时占位关系，需显式标注 `status: placeholder` 并尽快补齐对应 Evidence 缓存。
- 新增关系类型或未归属关系类型，必须先在本节明确“归属文件 + 维护范围”，再进入正式实例边维护。
```

Also extend the relation index at the end of the file so it contains:

```md
## 关系索引
- [[task_method_map]]
- [[evidence_index]]
- [[provenance_links]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[paper_method_links]]
- [[benchmark_links]]
```

- [ ] **Step 3: Re-run the ontology checks**

```bash
grep -n "未归属\|paper_method_links\|benchmark_links\|provenance_links\|`proposes`：`\[\[Paper\]\] --proposes--> \[\[Method\|Concept\]\]`" wiki/ontology/graph-standard.md
```

Expected: no “未归属” line remains, and output now includes all three new ledger filenames plus the broadened `proposes` definition.

- [ ] **Step 4: Commit the ontology change**

```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: assign relation ledger ownership"
```

Expected: commit succeeds and only stages the spec change for this task.

---

### Task 2: Create the new relation ledgers and move provenance out of `evidence_index.md`

**Files:**
- Create: `wiki/relations/paper_method_links.md`
- Create: `wiki/relations/benchmark_links.md`
- Create: `wiki/relations/provenance_links.md`
- Modify: `wiki/relations/evidence_index.md:1-69`
- Test: `wiki/relations/*.md`

- [ ] **Step 1: Run a failing check for the missing ledgers and misplaced provenance**

```bash
ls wiki/relations/paper_method_links.md wiki/relations/benchmark_links.md wiki/relations/provenance_links.md && grep -n "## `sourced_from` 实例边" wiki/relations/evidence_index.md
```

Expected: `ls` fails because the three ledger files do not exist yet, and `grep` finds `sourced_from` still living in `evidence_index.md`.

- [ ] **Step 2: Create `wiki/relations/paper_method_links.md`**

Write this file exactly:

```md
## `proposes` 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - reason: 该论文首次提出 Retrieve-Prioritize-Reason 的 PathMind 方法。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - reason: 该 survey 提出并系统解释复杂产品设计中的 LLM-KG 协同分层框架。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6

## 说明
- 本页是 `proposes` 实例边的正式账本。
- `proposes` 允许 `Paper -> Method` 与 `Paper -> Concept`；后者主要用于 framework / taxonomy 型核心知识产物。
```

- [ ] **Step 3: Create `wiki/relations/benchmark_links.md`**

Write this file exactly:

```md
## `evaluated_on` 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]`
  - reason: 论文在 WebQSP 上报告主要实验结果与对比结果。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §1–3
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]`
  - reason: 论文在 CWQ 上报告主要实验结果与对比结果。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §1–3
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
  - reason: PathMind 方法使用 WebQSP 作为正式评测基准。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §1–3
- `[[PathMind]] --evaluated_on--> [[CWQ]]`
  - reason: PathMind 方法使用 CWQ 作为正式评测基准。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] §1–3

## 说明
- 本页是 `evaluated_on` 实例边的正式账本。
- empirical 论文与方法默认在此登记 benchmark 绑定。
- survey / framework / taxonomy 论文若无统一 benchmark，可按规范豁免，不强制造边。
```

- [ ] **Step 4: Create `wiki/relations/provenance_links.md`**

Write this file exactly:

```md
## `sourced_from` 实例边
- `[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: sections 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] frontmatter `source_pdf`
- `[[intermediate/papers/PathMind.experiments|PathMind.experiments]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: experiments 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] frontmatter `source_pdf`
- `[[intermediate/papers/PathMind.refs|PathMind.refs]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: refs 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] frontmatter `source_pdf`
- `[[intermediate/papers/PathMind.full|PathMind.full]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: full 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.full|PathMind.full]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: sections 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: analysis 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: refs 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: full 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]] frontmatter `source_pdf`

## 说明
- 本页是 `sourced_from` 实例边的正式账本。
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 关系。
- 正式知识页应优先通过 `supported_by` 连接到 Evidence，而不是直接连接原始 PDF。
```

- [ ] **Step 5: Rewrite `wiki/relations/evidence_index.md` so it keeps only `supported_by`**

Replace the file contents with:

```md
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

- [ ] **Step 6: Verify the ledgers and provenance split**

```bash
ls wiki/relations/paper_method_links.md wiki/relations/benchmark_links.md wiki/relations/provenance_links.md && grep -n "## `sourced_from` 实例边" wiki/relations/evidence_index.md && grep -n "## `sourced_from` 实例边" wiki/relations/provenance_links.md
```

Expected: `ls` succeeds, the grep against `evidence_index.md` returns no matches, and the grep against `provenance_links.md` finds the provenance heading.

- [ ] **Step 7: Commit the ledger split**

```bash
git add wiki/relations/paper_method_links.md wiki/relations/benchmark_links.md wiki/relations/provenance_links.md wiki/relations/evidence_index.md
git commit -m "docs: add missing relation ledgers"
```

Expected: commit succeeds with the three new ledgers and the narrowed evidence index.

---

### Task 3: Expose the new ledgers in repository navigation

**Files:**
- Modify: `wiki/index.md:5-15`
- Modify: `wiki/index.md:136-141`
- Test: `wiki/index.md`

- [ ] **Step 1: Run a failing navigation check**

```bash
grep -n "paper_method_links\|benchmark_links\|provenance_links" wiki/index.md
```

Expected: no matches, because the new ledgers are not yet linked from the index.

- [ ] **Step 2: Add the new links to the overview and relation sections**

Update the overview block to:

```md
## 0. 总览
- [[overview]]
- [[log]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[provenance_links]]
- [[paper_method_links]]
- [[benchmark_links]]
- [[ontology/index|ontology]]
- [[graph-standard]]
```

Update the “### 关联关系” block to:

```md
### 关联关系
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[provenance_links]]
- [[paper_method_links]]
- [[benchmark_links]]
```

- [ ] **Step 3: Verify the new navigation links**

```bash
grep -n "paper_method_links\|benchmark_links\|provenance_links" wiki/index.md
```

Expected: six matches total — three in the overview block and three in the relation block.

- [ ] **Step 4: Commit the index update**

```bash
git add wiki/index.md
git commit -m "docs: index new relation ledgers"
```

Expected: commit succeeds with only the navigation change for this task.

---

### Task 4: Add lint guardrails for the new ledgers and seeded edges

**Files:**
- Modify: `scripts/lint_graph.py:17-25`
- Modify: `scripts/lint_graph.py:206-315`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the lint script and capture the current blind spot**

```bash
python3 scripts/lint_graph.py
```

Expected: PASS even though the script does not yet require `paper_method_links.md`, `benchmark_links.md`, or `provenance_links.md`, and does not prevent `sourced_from` from living in `evidence_index.md`.

- [ ] **Step 2: Extend `REQUIRED_FILES` and add new validation tables**

Insert these snippets into `scripts/lint_graph.py`.

First, extend `REQUIRED_FILES` to:

```python
REQUIRED_FILES = [
    'wiki/ontology/graph-standard.md',
    'wiki/relations/citation_graph.md',
    'wiki/relations/method_evolution.md',
    'wiki/relations/concept_links.md',
    'wiki/relations/task_method_map.md',
    'wiki/relations/evidence_index.md',
    'wiki/relations/paper_method_links.md',
    'wiki/relations/benchmark_links.md',
    'wiki/relations/provenance_links.md',
    'scripts/lint_graph.py',
]
```

Then add these constants near the existing `GRAPH_STANDARD_NEEDLES` block:

```python
INDEX_NEEDLES = [
    '[[paper_method_links]]',
    '[[benchmark_links]]',
    '[[provenance_links]]',
]

GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    'paper_method_links.md',
    'benchmark_links.md',
    'provenance_links.md',
    '`wiki/relations/paper_method_links.md`：维护 `proposes`',
    '`wiki/relations/benchmark_links.md`：维护 `evaluated_on`',
    '`wiki/relations/evidence_index.md`：维护 `supported_by`',
    '`wiki/relations/provenance_links.md`：维护 `sourced_from`',
]

RELATION_LEDGER_NEEDLES = {
    'wiki/relations/paper_method_links.md': [
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]',
        '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]',
    ],
    'wiki/relations/benchmark_links.md': [
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]',
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]',
        '[[PathMind]] --evaluated_on--> [[WebQSP]]',
        '[[PathMind]] --evaluated_on--> [[CWQ]]',
    ],
    'wiki/relations/provenance_links.md': [
        '[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]',
        '[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]',
    ],
}
```

- [ ] **Step 3: Add the actual validation logic**

Insert this logic after the existing `GRAPH_STANDARD_NEEDLES` check and before the final wiki page scan:

```python
index_text = read_text('wiki/index.md')
for needle in INDEX_NEEDLES:
    if needle not in index_text:
        errors.append(f'missing {needle} in wiki/index.md')

for rel, needles in RELATION_LEDGER_NEEDLES.items():
    text = read_text(rel)
    for needle in needles:
        if needle not in text:
            errors.append(f'missing relation edge {needle} in {rel}')

if '## `sourced_from` 实例边' in read_text('wiki/relations/evidence_index.md'):
    errors.append('sourced_from must live in wiki/relations/provenance_links.md, not wiki/relations/evidence_index.md')
```

- [ ] **Step 4: Run the lint script again and verify the new checks pass**

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded` and the summary object. If it fails, fix the file contents before continuing; do **not** weaken the new checks.

- [ ] **Step 5: Commit the lint guardrails**

```bash
git add scripts/lint_graph.py
git commit -m "test: guard relation ledger completeness"
```

Expected: commit succeeds with only the lint script change.

---

### Task 5: Final verification and paper-ingest risk assessment

**Files:**
- Test: `wiki/ontology/graph-standard.md`
- Test: `wiki/relations/*.md`
- Test: `wiki/index.md`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the full verification suite**

```bash
python3 scripts/lint_graph.py && grep -n "未归属" wiki/ontology/graph-standard.md && grep -n "## `sourced_from` 实例边" wiki/relations/provenance_links.md && grep -n "paper_method_links\|benchmark_links\|provenance_links" wiki/index.md
```

Expected:
- `python3 scripts/lint_graph.py` prints `PASS: graph lint succeeded`
- `grep -n "未归属"` returns no matches
- `grep -n "## `sourced_from` 实例边"` finds the provenance ledger heading
- `grep -n "paper_method_links\|benchmark_links\|provenance_links"` finds the new navigation links

- [ ] **Step 2: Check the exact seeded edges exist**

```bash
grep -n "PathMind.*--proposes-->.*\[\[PathMind\]\]" wiki/relations/paper_method_links.md && \
grep -n "PathMind.*--evaluated_on-->.*\[\[WebQSP\]\]" wiki/relations/benchmark_links.md && \
grep -n "LLM-KG-CPD-Survey.sections.*--sourced_from-->.*raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf" wiki/relations/provenance_links.md
```

Expected: all three grep commands return one matching line each.

- [ ] **Step 3: Record the paper-ingest follow-up assessment in your handoff summary**

Use this exact conclusion in your final handoff message:

```text
paper-ingest 以后仍可能在“生成正式关系边”这一步漏掉 proposes / evaluated_on / sourced_from，因为这次修复只补了账本归属和 lint 护栏，没有直接改写 ingest 流程本身。现在的变化已经能把同类遗漏从“静默漏边”变成“lint 可见失败”；如果后续希望 ingest 自动写出这些边，还需要单独更新 paper-ingest 的关系落账步骤。
```

- [ ] **Step 4: Create the final implementation commit**

```bash
git add wiki/ontology/graph-standard.md wiki/relations/paper_method_links.md wiki/relations/benchmark_links.md wiki/relations/provenance_links.md wiki/relations/evidence_index.md wiki/index.md scripts/lint_graph.py
git commit -m "feat: complete relation ledger coverage"
```

Expected: commit succeeds with the final integrated state. If earlier task commits were already created, skip this step and instead provide the existing commit hashes in the handoff.
