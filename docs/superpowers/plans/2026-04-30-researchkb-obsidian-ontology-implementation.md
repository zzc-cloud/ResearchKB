# ResearchKB Obsidian Graph & Ontology Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the current PathMind-centered ResearchKB into an ontology-driven, Obsidian-friendly knowledge network with repeatable ingest rules and evidence-backed links.

**Architecture:** Keep `wiki/` as the formal knowledge layer, add `tasks/`, `benchmarks/`, and `ontology/` as explicit ontology-backed node types, upgrade `intermediate/` into an evidence layer with backlinks, and centralize semantic edges in `wiki/relations/`. Encode the standard into `CLAUDE.md` and a lightweight lint script so future paper ingest follows the same graph contract.

**Tech Stack:** Markdown, Obsidian wikilinks, YAML frontmatter, Python 3, git

---

### Task 1: Create ontology-supporting node directories and seed pages

**Files:**
- Create: `wiki/tasks/knowledge-graph-reasoning.md`
- Create: `wiki/tasks/kgqa.md`
- Create: `wiki/tasks/multi-hop-qa.md`
- Create: `wiki/benchmarks/WebQSP.md`
- Create: `wiki/benchmarks/CWQ.md`
- Create: `wiki/ontology/index.md`
- Create: `wiki/ontology/graph-standard.md`

**Step 1: Create the task node for knowledge graph reasoning**

```markdown
---
title: Knowledge Graph Reasoning
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [知识图谱推理, 研究任务]
---

## 任务定义
...

## 相关方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]

## 相关场景
- [[知识图谱推理问答]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
```

**Step 2: Create the `kgqa` and `multi-hop-qa` task nodes with backlinks to the same PathMind cluster**

Use the same structure, but tailor the task definition and link sections to `[[PathMind]]`, `[[知识图谱推理问答]]`, and the PathMind paper.

**Step 3: Create the `WebQSP` and `CWQ` benchmark nodes**

```markdown
---
title: WebQSP
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa, multi-hop-qa]
industry: [general]
research_role: [benchmark]
tags: [benchmark, KGQA]
---

## 基准定义
...

## 相关任务
- [[kgqa]]
- [[multi-hop-qa]]

## 代表方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]

## 代表论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
```

**Step 4: Create the ontology pages**

`wiki/ontology/index.md` should be a navigation page linking to `[[graph-standard]]`, `[[task_method_map]]`, and `[[evidence_index]]`.

`wiki/ontology/graph-standard.md` should summarize:
- node types
- relation types
- minimum link obligations
- evidence expectations

**Step 5: Verify the new pages exist and have wikilinks**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
paths = [
  'wiki/tasks/knowledge-graph-reasoning.md',
  'wiki/tasks/kgqa.md',
  'wiki/tasks/multi-hop-qa.md',
  'wiki/benchmarks/WebQSP.md',
  'wiki/benchmarks/CWQ.md',
  'wiki/ontology/index.md',
  'wiki/ontology/graph-standard.md',
]
for p in paths:
    text = Path(p).read_text()
    assert '[[' in text, f'no wikilinks in {p}'
print('PASS: seed ontology/task/benchmark pages created')
PY
```
Expected: `PASS: seed ontology/task/benchmark pages created`

**Step 6: Commit**

```bash
git add wiki/tasks wiki/benchmarks wiki/ontology
git commit -m "feat: add ontology task and benchmark nodes"
```

---

### Task 2: Update the main wiki navigation to expose the new node types

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/overview.md`

**Step 1: Add `tasks`, `benchmarks`, and `ontology` to `wiki/index.md`**

Add new sections under “按知识对象” and “按研究问题”, using wikilinks instead of only Markdown links.

```markdown
### 任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

### 基准
- [[WebQSP]]
- [[CWQ]]

### 本体
- [[ontology/index|ontology]]
- [[graph-standard]]
```

**Step 2: Replace key plain Markdown links with Obsidian wikilinks where possible**

Keep navigational readability, but prefer links like:

```markdown
- [[overview]]
- [[log]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
```

**Step 3: Add one ontology-aware paragraph to `wiki/overview.md`**

Describe the vault as:
- formal knowledge layer
- evidence layer
- relation layer
- ontology layer

Include links to `[[PathMind]]`, `[[知识图谱推理问答]]`, `[[graph-standard]]`.

**Step 4: Verify the new node types are reachable from the index**

Run:
```bash
grep -n "knowledge-graph-reasoning\|WebQSP\|graph-standard" wiki/index.md wiki/overview.md
```
Expected: matching lines in both files.

**Step 5: Commit**

```bash
git add wiki/index.md wiki/overview.md
git commit -m "feat: expose ontology nodes in wiki navigation"
```

---

### Task 3: Upgrade the formal PathMind pages to satisfy the graph contract

**Files:**
- Modify: `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Modify: `wiki/methods/PathMind.md`
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`

**Step 1: Patch the PathMind paper page**

Ensure it explicitly links:
- method: `[[methods/PathMind|PathMind（方法）]]`
- concepts: `[[路径优先化]]`, `[[重要推理路径]]`
- tasks: `[[knowledge-graph-reasoning]]`, `[[kgqa]]`, `[[multi-hop-qa]]`
- scenario: `[[知识图谱推理问答]]`
- benchmarks: `[[WebQSP]]`, `[[CWQ]]`
- evidence: `[[intermediate/papers/PathMind.sections|PathMind.sections]]`, `[[intermediate/papers/PathMind.refs|PathMind.refs]]`

**Step 2: Patch the PathMind method page**

Add or tighten sections for:
- representative paper backlink
- benchmark links
- task links
- concept links
- evidence links

Add a short “证据来源” section like:

```markdown
## 证据来源
- 结构化章节缓存：[[intermediate/papers/PathMind.sections|PathMind.sections]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]
```

**Step 3: Patch the concept pages**

In both concept pages, add links to:
- task node(s)
- scenario node
- relation hub (`[[concept_links]]` or `[[method_evolution]]` as appropriate)
- evidence cache

**Step 4: Patch the scenario page**

Ensure `知识图谱推理问答` links to:
- `[[knowledge-graph-reasoning]]`
- `[[kgqa]]`
- `[[multi-hop-qa]]`
- `[[WebQSP]]`
- `[[CWQ]]`
- `[[PathMind]]`, `[[RoG]]`, `[[GCR]]`
- the PathMind paper

**Step 5: Verify all five pages meet minimum link obligations**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
checks = {
  'wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md': ['[[PathMind', '[[路径优先化]]', '[[knowledge-graph-reasoning]]', '[[WebQSP]]', '[[intermediate/papers/PathMind.sections'],
  'wiki/methods/PathMind.md': ['[[知识图谱推理问答]]', '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]', '[[路径优先化]]'],
  'wiki/concepts/路径优先化.md': ['[[PathMind]]', '[[knowledge-graph-reasoning]]'],
  'wiki/concepts/重要推理路径.md': ['[[PathMind]]', '[[知识图谱推理问答]]'],
  'wiki/scenarios/知识图谱推理问答.md': ['[[PathMind]]', '[[knowledge-graph-reasoning]]', '[[WebQSP]]'],
}
for path, needles in checks.items():
    text = Path(path).read_text()
    for needle in needles:
        assert needle in text, f'missing {needle} in {path}'
print('PASS: PathMind cluster meets minimum graph contract')
PY
```
Expected: `PASS: PathMind cluster meets minimum graph contract`

**Step 6: Commit**

```bash
git add wiki/papers/PathMind* wiki/methods/PathMind.md wiki/concepts/路径优先化.md wiki/concepts/重要推理路径.md wiki/scenarios/知识图谱推理问答.md
git commit -m "feat: connect PathMind pages into ontology graph"
```

---

### Task 4: Upgrade intermediate caches into evidence-layer nodes

**Files:**
- Modify: `intermediate/papers/PathMind.sections.md`
- Modify: `intermediate/papers/PathMind.refs.md`
- Modify: `intermediate/papers/PathMind.experiments.md`
- Modify: `intermediate/papers/PathMind.full.md`

**Step 1: Add a backlink block to each cache**

Use a consistent section near the top:

```markdown
## 对应正式知识节点
- 论文：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 方法：[[PathMind]]
- 概念：[[路径优先化]]、[[重要推理路径]]
- 任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 基准：[[WebQSP]]、[[CWQ]]
```

**Step 2: Wikilink the key upstream methods and papers inside the cache bodies**

At minimum convert repeated names to links for:
- `[[RoG]]`
- `[[GCR]]`
- `[[EPERM]]`
- `[[GNN-RAG]]` or the exact existing page title if you add a placeholder paper instead
- `[[ToG]]`
- `[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]`
- `[[WebQSP]]`
- `[[CWQ]]`

**Step 3: Add evidence intent lines to the cache sections**

Examples:

```markdown
> 本节支撑 [[PathMind]] 的方法定义与 [[路径优先化]] 的关键机制描述。
```

```markdown
> 本节支撑 [[PathMind]] 在 [[WebQSP]] 与 [[CWQ]] 上的实验结论。
```

**Step 4: Verify every PathMind cache links back to the formal paper and at least one benchmark**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
for p in Path('intermediate/papers').glob('PathMind*.md'):
    text = p.read_text()
    assert '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]' in text, p
    assert '[[WebQSP]]' in text or '[[CWQ]]' in text, p
print('PASS: PathMind evidence caches backlink into formal graph')
PY
```
Expected: `PASS: PathMind evidence caches backlink into formal graph`

**Step 5: Commit**

```bash
git add intermediate/papers/PathMind.sections.md intermediate/papers/PathMind.refs.md intermediate/papers/PathMind.experiments.md intermediate/papers/PathMind.full.md
git commit -m "feat: convert PathMind caches into evidence nodes"
```

---

### Task 5: Add relation hubs and reduce critical dangling links with placeholder paper nodes

**Files:**
- Modify: `wiki/relations/citation_graph.md`
- Modify: `wiki/relations/method_evolution.md`
- Modify: `wiki/relations/concept_links.md`
- Create: `wiki/relations/task_method_map.md`
- Create: `wiki/relations/evidence_index.md`
- Create: `wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
- Create: `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- Create: `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- Create: `wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
- Create: `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`
- Create: `wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`

**Step 1: Create placeholder paper nodes for the six cited upstream works**

Use a compact placeholder template:

```markdown
---
title: Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning
status: placeholder
research_role: [foundational]
tags: [placeholder, cited-work]
---

## 当前定位
- 当前作为 [[PathMind]] 的关键上游工作与对比对象。

## 与知识库现有内容的关系
- 相关方法：[[RoG]]
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- 关联任务：[[knowledge-graph-reasoning]]、[[kgqa]]

## 待补充
- 正式摘要页、实验设定、方法贡献。
```

**Step 2: Expand `citation_graph.md` into explicit semantic edge records**

Keep the current list, but make sure each cited paper now resolves to an actual page.

**Step 3: Create `task_method_map.md`**

Record mappings like:

```markdown
## 任务到方法
- [[knowledge-graph-reasoning]]
  - [[PathMind]]
  - [[RoG]]
  - [[GCR]]
- [[kgqa]]
  - [[PathMind]]
  - [[EPERM]]
```

**Step 4: Create `evidence_index.md`**

Record mappings like:

```markdown
## 论文证据索引
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - 方法机制：[[intermediate/papers/PathMind.sections|PathMind.sections]] §7.3
  - 实验结果：[[intermediate/papers/PathMind.experiments|PathMind.experiments]] §3-7
  - 引用与基线：[[intermediate/papers/PathMind.refs|PathMind.refs]] §2-5
```

**Step 5: Update `method_evolution.md` and `concept_links.md`**

Add explicit backlinks from:
- `[[PathMind]]` to `[[路径优先化]]`
- `[[路径优先化]]` to `[[重要推理路径]]`
- `[[knowledge-graph-reasoning]]` / `[[kgqa]]` where the relationship matters

**Step 6: Verify there are no critical dangling links in the PathMind citation cluster**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
required = [
  'wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md',
  'wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md',
  'wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md',
  'wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md',
  'wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md',
  'wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md',
  'wiki/relations/task_method_map.md',
  'wiki/relations/evidence_index.md',
]
for p in required:
    assert Path(p).exists(), p
print('PASS: citation placeholders and relation hubs created')
PY
```
Expected: `PASS: citation placeholders and relation hubs created`

**Step 7: Commit**

```bash
git add wiki/relations wiki/papers/Reasoning\ on\ Graphs* wiki/papers/Graph-constrained\ reasoning* wiki/papers/An\ Evidence\ Path* wiki/papers/Gnn-rag* wiki/papers/Think-on-Graph\ 2.0* wiki/papers/KnowPath*
git commit -m "feat: add relation hubs and citation placeholders"
```

---

### Task 6: Encode the ontology graph standard into the project ingest contract

**Files:**
- Modify: `CLAUDE.md`
- Modify: `docs/plans/2026-04-30-researchkb-obsidian-ontology-design.md`

**Step 1: Update the directory tree in `CLAUDE.md`**

Add:
- `wiki/tasks/`
- `wiki/benchmarks/`
- `wiki/ontology/`
- new relation pages in `wiki/relations/`

**Step 2: Update the paper summary template in `CLAUDE.md`**

Extend the template with explicit sections for:
- 任务节点
- benchmark 节点
- evidence cache backlinks

Include examples like:

```markdown
## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]

## 实验证据
- [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
```

**Step 3: Update Workflow A in `CLAUDE.md`**

Add mandatory steps:
- create/update task nodes
- create/update benchmark nodes
- write to `task_method_map.md`
- write to `evidence_index.md`
- run graph lint after ingest

**Step 4: Add a short “本体化图谱规范” note to the design doc**

Reference the actual repository files (`wiki/ontology/graph-standard.md`, `scripts/lint_graph.py`) so the design doc points to the implemented contract.

**Step 5: Verify `CLAUDE.md` now requires graph-aware ingest**

Run:
```bash
grep -n "tasks/\|benchmarks/\|evidence_index\|task_method_map\|graph lint" CLAUDE.md
```
Expected: matching lines covering all five keywords.

**Step 6: Commit**

```bash
git add CLAUDE.md docs/plans/2026-04-30-researchkb-obsidian-ontology-design.md
git commit -m "docs: codify ontology graph ingest contract"
```

---

### Task 7: Add a lightweight graph lint script and run full verification

**Files:**
- Create: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

**Step 1: Write the failing lint script skeleton**

The script should check:
- required directories exist
- required PathMind files exist
- new relation hubs exist
- each core page contains required wikilinks
- each PathMind intermediate cache back-links the formal paper

Skeleton:

```python
from pathlib import Path
import sys

errors = []

REQUIRED_PATHS = [
    'wiki/tasks/knowledge-graph-reasoning.md',
    'wiki/benchmarks/WebQSP.md',
    'wiki/ontology/graph-standard.md',
    'wiki/relations/task_method_map.md',
    'wiki/relations/evidence_index.md',
]

for rel in REQUIRED_PATHS:
    if not Path(rel).exists():
        errors.append(f'missing file: {rel}')

# Add content checks here.

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('PASS: graph lint succeeded')
```

**Step 2: Run the script and make sure it fails before finishing the remaining checks**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected early in development: `FAIL` with missing file or missing link messages.

**Step 3: Implement the remaining checks and rerun until it passes**

Add assertions for:
- PathMind paper contains method / concept / task / benchmark / evidence links
- PathMind method contains paper / concept / scenario links
- PathMind caches contain the formal paper backlink
- `CLAUDE.md` mentions tasks, benchmarks, and graph lint

**Step 4: Run the final verification commands**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: `PASS: graph lint succeeded`

Run:
```bash
python3 - <<'PY'
from pathlib import Path
count = 0
with_links = 0
for p in Path('wiki').rglob('*.md'):
    text = p.read_text(errors='ignore')
    count += 1
    if '[[' in text:
        with_links += 1
print({'wiki_pages': count, 'with_wikilinks': with_links})
PY
```
Expected: all substantive `wiki/*.md` pages include wikilinks.

**Step 5: Manually verify in Obsidian**

Open the vault and inspect:
- Global graph: new colors/groups for papers, methods, concepts, tasks, benchmarks, relations, intermediate
- Local graph for `PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models`

Expected neighbors include:
- `PathMind`
- `路径优先化`
- `重要推理路径`
- `知识图谱推理问答`
- `knowledge-graph-reasoning`
- `kgqa`
- `multi-hop-qa`
- `WebQSP`
- `CWQ`
- `PathMind.sections`
- `PathMind.refs`

**Step 6: Commit**

```bash
git add scripts/lint_graph.py
git commit -m "chore: add graph lint verification"
```

---

### Task 8: Final branch review before broader rollout

**Files:**
- Review: `git diff --stat`
- Review: all modified files above

**Step 1: Review the full diff**

Run:
```bash
git diff --stat
```
Expected: only ontology/task/benchmark/relation/index/cache/CLAUDE/script files changed.

**Step 2: Run the full lint again**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: `PASS: graph lint succeeded`

**Step 3: Sanity-check the PathMind cluster one last time**

Run:
```bash
grep -R "PathMind.sections\|WebQSP\|knowledge-graph-reasoning\|evidence_index" wiki intermediate CLAUDE.md
```
Expected: matches across paper/method/scenario/cache/relations/project manual.

**Step 4: Prepare the handoff summary**

Include:
- what new node types were added
- which current dangling links were resolved
- which future ingest steps are now mandatory
- what still remains outside phase 1 (for example, richer upstream paper summaries)

**Step 5: Commit**

```bash
git add wiki intermediate CLAUDE.md scripts docs/plans
git commit -m "feat: establish ontology-driven Obsidian graph foundation"
```
