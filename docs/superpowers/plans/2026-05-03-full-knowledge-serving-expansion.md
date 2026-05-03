# Full Knowledge-Layer Serving Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generalize the serving-layer model, governance rules, and migration framework from Method/Paper pages to Paper, Method, Concept, Task, Scenario, Benchmark, and Evidence.

**Architecture:** First update the written standards so all seven node types have explicit serving-layer rules and a third serving-governance gate. Then refactor `scripts/lint_graph.py` from sample-page checks into a type-based serving validator with migration-state awareness. Finally, migrate one representative page per newly added type (Concept, Task, Scenario, Benchmark, Evidence) so the new rules are exercised end-to-end before broader batch rollout.

**Tech Stack:** Markdown knowledge pages, Python 3 (`scripts/lint_graph.py`), existing ResearchKB ontology and relation-ledger conventions, skill-based governance (`ontology-semantic-review`).

---

## File map

### Governance and standards
- Modify: `wiki/ontology/index.md`
  - Clarify that object-page-first QA applies across all serving-ready node types, not only Method/Paper.
- Modify: `wiki/ontology/graph-standard.md`
  - Extend serving-layer rules, per-type section expectations, full-type `Formal relations` requirements, migration-state handling, and the third governance gate.
- Modify: `CLAUDE.md`
  - Update QA workflow and governance language to cover all seven node types and serving-review gating.

### Serving review skill
- Create: `.claude/skills/serving-governance-review/SKILL.md`
  - Define the new review gate for serving-surface quality and release-readiness.

### Lint framework
- Modify: `scripts/lint_graph.py`
  - Replace page-specific serving checks with path/type discovery, per-type requirements, migration-state awareness, and cross-type `Formal relations` validation.

### Representative migrated pages
- Modify: `wiki/concepts/路径优先化.md`
  - Add serving-layer sections and `Formal relations`.
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
  - Add serving-layer sections and `Formal relations`.
- Modify: `wiki/scenarios/知识图谱推理问答.md`
  - Add serving-layer sections and `Formal relations`.
- Modify: `wiki/benchmarks/WebQSP.md`
  - Add serving-layer sections and `Formal relations`.
- Modify: `intermediate/papers/PathMind.sections.md`
  - Add serving-friendly evidence sections and `Formal relations`.

### Design and plan artifacts
- Create: `docs/superpowers/plans/2026-05-03-full-knowledge-serving-expansion.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `python3 - <<'PY' ... PY` targeted parser smoke checks while refactoring lint

---

### Task 1: Expand ontology index to full-type serving entrypoints

**Files:**
- Modify: `wiki/ontology/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Update `wiki/ontology/index.md` so the QA entrypoint covers all serving-ready node types**

Replace the current `## 4. 按任务进入` and `## 5. 推荐阅读路径` text with:

```markdown
## 4. 按任务进入
- 想做受约束知识问答 → 先定位 serving-ready 对象页（`wiki/papers/`、`wiki/methods/`、`wiki/concepts/`、`wiki/tasks/`、`wiki/scenarios/`、`wiki/benchmarks/`、`intermediate/papers/`），再按页面中的 Formal relations 区块扩展；需要证据细节时优先下钻对应 Evidence 页
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式对象知识 → 对应 `wiki/` 对象页或 Evidence 页
- 想看治理用正式关系账本 → `wiki/relations/`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `docs/`

## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → `wiki/relations/` → 代表对象页 → `intermediate/papers/`

### 回答知识问题
serving-ready 对象页 → Formal relations 区块 → 邻接对象页 / Evidence 页 → 必要时治理账本

### 治理知识变更
[[graph-standard]] → `wiki/relations/` → 变更对象页 / Evidence 页 → `intermediate/papers/`
```

- [ ] **Step 2: Run lint and verify the updated navigation file still passes baseline governance**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the ontology index update**

```bash
git add wiki/ontology/index.md
git commit -m "docs: extend ontology serving entrypoints"
```

---

### Task 2: Extend graph-standard to all seven serving node types

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-layer coverage for Concept, Task, Scenario, Benchmark, and Evidence sections**

In `wiki/ontology/graph-standard.md`, update the body templates as follows.

For `### Concept`, replace the current `正文标准结构` with:

```markdown
正文标准结构：
- 概念定义
- 核心内涵
- 与其他概念的关系
- 相关方法
- 相关论文
- 相关任务 / 场景
- 证据来源
- Formal relations
```

For `### Scenario`, replace the current `正文标准结构` with:

```markdown
正文标准结构：
- 场景描述
- 核心挑战
- 使用的主要方法 / 概念
- 相关任务
- 相关论文
- 相关 benchmark
- 证据来源
- Formal relations
- 开放问题
```

For `### Evidence`, insert this `正文标准结构` block after the existing constraints:

```markdown
正文标准结构：
- 对应正式知识节点
- 本节支撑什么
- 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 来源说明
- Formal relations
```
```

- [ ] **Step 2: Add new `### Task` and `### Benchmark` sections if they are currently absent from the standard**

Insert the following sections before `### Scenario`:

```markdown
### Task
必填字段：`title`、`problem`、`industry`、`research_role`

推荐字段：`method_family`、`scenario`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 任务名称
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [研究任务]
---
```

正文标准结构：
- 任务定义
- 核心挑战
- 相关方法
- 相关概念
- 相关场景
- 相关 benchmark
- 相关论文
- 证据来源 / 关系索引
- Formal relations

### Benchmark
必填字段：`title`、`problem`、`industry`、`research_role`

推荐字段：`method_family`、`scenario`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 基准名称
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [benchmark]
tags: [benchmark]
---
```

正文标准结构：
- benchmark 定义
- 评测目标
- 相关任务
- 被哪些方法 / 论文使用
- 相关场景
- 证据来源
- Formal relations
```
```

- [ ] **Step 3: Extend the serving-layer governance sections to all seven types and add migration-state handling**

Replace the current serving-layer prose block beginning at `## Method / Paper 服务层投影规则` with:

```markdown
## 全类型服务层投影规则
- Paper、Method、Concept、Task、Scenario、Benchmark、Evidence 页必须同时包含：frontmatter、面向人类的关系区块、`## Formal relations` 规范化关系区块。
- frontmatter 只承载紧凑结构化摘要，不承担手写关系真源职责；其派生字段必须来自正式关系账本。
- Method 的 `parent_methods` / `child_methods` 继续作为首批强一致派生字段，必须与 `wiki/relations/method_evolution.md` 保持一致。
- 其他类型前期默认不强制扩张大量派生字段，优先把正式关系投影收敛到 `## Formal relations`。
- 面向人类的关系区块按节点类型差异化组织，但不得与正式关系账本冲突。
- `## Formal relations` 必须覆盖该实体的一跳正式关系投影，作为问答时的正式关系读取面。

## Formal relations 区块规范
- 区块标题固定为 `## Formal relations`。
- 所有 serving-ready 节点类型都必须包含 `### Outgoing` 与 `### Incoming` 两个子区块；无内容时显式写 `- 无`。
- 每条关系使用 canonical 三元组格式：`- `[[Source Node]] --relation_type--> [[Target Node]]``。
- 每条关系至少附带一个 `- evidence: [[证据页]]` 行；必要时可补 `- note:`，但应避免 prose 污染区块。
- 该区块供问答时的受约束拓扑探索直接消费，不以综述性表达代替。

## Serving 迁移状态
- serving-ready：页面已通过结构治理、本体语义治理与 serving 治理，可作为默认问答入口。
- partial：页面已开始迁移，但 `Formal relations` 或人类区块尚未达到默认 serving 质量线。
- legacy：页面仍处于旧格式，仅可作为过渡期参考页。
- 迁移状态可放在 frontmatter 或外部治理清单中，但必须能被治理流程识别。

## 服务层治理校验要求
- 除结构合法性外，还必须校验七类节点页的投影一致性、投影完备性与问答可消费性。
- 投影一致性：frontmatter 派生字段、`## Formal relations` 与正式关系账本一致；人类关系区块不得冲突。
- 投影完备性：属于该实体的一跳正式关系，必须按规则投影到 `## Formal relations`；指定派生字段必须回填到 frontmatter。
- 问答可消费性：页面必须存在稳定的 `## Formal relations`、`### Outgoing`、`### Incoming` 结构，以及可回溯 evidence 入口。
```
```

- [ ] **Step 4: Add a third governance gate section naming serving governance explicitly**

Insert the following section after the serving-governance requirements:

```markdown
## 三层治理出口
- 结构治理：`python3 scripts/lint_graph.py`
- 本体语义治理：`ontology-semantic-review`
- serving 治理：`serving-governance-review`

其中 serving 治理是独立发布门槛，不等同于结构 lint，也不等同于本体语义审查。
```
```

- [ ] **Step 5: Run lint and verify the standard still passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the graph-standard expansion**

```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: define full knowledge-layer serving rules"
```

---

### Task 3: Update CLAUDE.md for all-type serving-ready QA

**Files:**
- Modify: `CLAUDE.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Expand QA-serving language from Method/Paper-only to all serving-ready node types**

Replace the `### 基本原则` block with:

```markdown
### 基本原则
- 正式知识问答默认优先看 serving-ready 对象页（`wiki/papers/`、`wiki/methods/`、`wiki/concepts/`、`wiki/tasks/`、`wiki/scenarios/`、`wiki/benchmarks/`、`intermediate/papers/`）
- 正式关系治理与修复优先看 `wiki/relations/`
- 论文细节、实验、引用与机制优先看 Evidence 页与 `intermediate/papers/`
- 原始 PDF 仅在必要时回源，不作为默认工作入口
```

- [ ] **Step 2: Expand the “需要哪些信息层” bullets and query-order flow**

Replace the current information-layer bullets with:

```markdown
4. **需要哪些信息层**
   - `wiki/ontology/index.md` 定位导航入口
   - serving-ready 的正式对象页承载默认问答服务层
   - `wiki/relations/` 用于正式关系治理、修复与审计
   - Evidence 页与 `intermediate/papers/` 核验证据
   - `raw/` 仅在必要时回源
```

Replace the `## 查询与分析默认顺序` section with:

```markdown
## 查询与分析默认顺序

当用户提问知识库内容时，默认按以下顺序：

1. 读取 `wiki/ontology/index.md` 定位导航入口
2. 锁定关键实体并读取对应的 serving-ready 正式对象页
3. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展
4. 如涉及机制、实验、引用、基线、统计分析或 provenance 核验，优先读取对应 Evidence 页与 `intermediate/papers/`
5. 如处于治理、修复、审计场景，或需核对投影真源，再读取 `wiki/relations/`
6. 必要时才回看 `raw/`
7. 回答时区分：
   - 正式知识结论
   - 证据缓存结论
   - 治理账本结论（仅在实际查询 relation ledger 时）
   - 待核验推断

回答知识库问题时：
- 默认把 serving-ready 对象页作为正式问答服务层来源。
- 必要时读取 Evidence 页与 `intermediate/papers/` 做证据核验。
- 仅在治理、修复、审计或真源核对场景下读取 `wiki/relations/`。
- 回答中必须区分：正式知识结论、证据缓存结论、治理账本结论（若使用）、待核验推断。
- 若属于探索发现，不要把候选知识伪装成正式事实。
```
```

- [ ] **Step 3: Add explicit serving-governance gate language to the workflow sections**

Replace the `### 查询与分析` block and add a serving-governance bullet under `### 检查知识库`:

```markdown
### 查询与分析
当我提问知识库内容时：
- 先做本体判定
- 再定位关键实体并读取对应的 serving-ready 正式对象页
- 默认基于 `Formal relations` 做受约束扩展，并在需要时核验证据
- 仅在治理、修复、审计或真源核对场景下查看 `wiki/relations/`
- 回答时说明依据来源
```

```markdown
- 除结构校验与本体语义问题外，还要评估页面是否达到 serving-ready 的问答入口质量线
```
```

- [ ] **Step 4: Update the anti-pattern and execution-principle language**

Replace the first execution principle and one anti-pattern bullet with:

```markdown
1. **skill 负责流程，`CLAUDE.md` 提供本体全局基础认知与执行框架，`wiki/ontology/graph-standard.md` 作为本体结构认知与判定中枢；具体问题所需的本体实例，应进一步从 serving-ready 正式对象页与 Evidence 页中定位、核验与扩展；仅在治理、修复、审计或真源核对场景下回查 `wiki/relations/`。**
```

```markdown
- 把 serving-ready 尚未完成的页面当成默认问答入口，或把治理账本读取流程机械套用到所有问答
```
```

- [ ] **Step 5: Run lint and verify CLAUDE.md still passes repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the CLAUDE.md expansion**

```bash
git add CLAUDE.md
git commit -m "docs: extend QA workflow to all serving types"
```

---

### Task 4: Create the `serving-governance-review` skill

**Files:**
- Create: `.claude/skills/serving-governance-review/SKILL.md`
- Test: inspect skill file in editor; no runtime command required

- [ ] **Step 1: Create the new skill directory and file**

Create `.claude/skills/serving-governance-review/SKILL.md` with this content:

```markdown
# Serving Governance Review

Review migrated knowledge pages to decide whether they are ready to serve as default constrained-QA entry surfaces.

## Use this when
- A batch of Paper / Method / Concept / Task / Scenario / Benchmark / Evidence pages has been migrated to the serving-layer model.
- You need to decide whether pages are `serving-ready`, `partial`, or `legacy`.
- Structural lint and ontology semantic review have already been run or are available.

## Inputs
- A git diff, file list, directory, or migration batch description.

## What to check
1. **Serving completeness**
   - Does every migrated page have `## Formal relations`, `### Outgoing`, and `### Incoming`?
   - Are the required one-hop relations present for the node type?
   - Are evidence links present and useful for drill-down?

2. **Serving readability alignment**
   - Do the human-readable sections match the formal projection?
   - Is there prose that would mislead a reader or LLM relative to the formal edges?

3. **QA traversability**
   - Can an LLM identify the next-hop nodes and relation types directly from the page?
   - Are there missing key neighbors that would force runtime fallback to `wiki/relations/`?

4. **Release readiness**
   - Is this page or batch safe to promote as the default QA serving surface?

## Output states
- `pass`: serving-ready
- `needs_fixes`: structurally or semantically usable, but not ready as default serving surface
- `blocked`: should not be promoted to serving-ready

## Constraints
- Do not redo structure lint.
- Do not redo ontology-semantic-review.
- Focus only on the distinct serving-surface quality gate.
```
```

- [ ] **Step 2: Verify the new skill file exists with the expected name**

Run: `ls .claude/skills/serving-governance-review`
Expected: `SKILL.md`

- [ ] **Step 3: Commit the new skill**

```bash
git add .claude/skills/serving-governance-review/SKILL.md
git commit -m "feat: add serving governance review skill"
```

---

### Task 5: Refactor `scripts/lint_graph.py` into a type-based serving validator

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write a small failing parser smoke test in a Python one-liner before refactoring**

Run this command before editing the file:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('wiki/concepts/路径优先化.md').read_text(encoding='utf-8')
assert '## Formal relations' in text, 'expected failure before Concept migration'
PY
```

Expected: FAIL with `AssertionError: expected failure before Concept migration`

- [ ] **Step 2: Replace sample-page-only serving constants with type-based rules plus migration sample coverage**

In `scripts/lint_graph.py`, replace the current `SERVING_PAGES` block with a split model:

```python
SERVING_TYPE_RULES = {
    'paper': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {},
    },
    'method': {
        'required_headings': ['## 相关概念', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
    'concept': {
        'required_headings': ['## 相关任务 / 场景', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'task': {
        'required_headings': ['## 相关 benchmark', '## 证据来源 / 关系索引', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'scenario': {
        'required_headings': ['## 相关任务', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'benchmark': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'evidence': {
        'required_headings': ['## 对应正式知识节点', '## 本节支撑什么', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
}

SERVING_READY_SAMPLES = {
    'wiki/methods/PathMind.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('PathMind', 'based_on', '路径导向知识图谱推理'),
            ('PathMind', 'improves_on', '路径导向知识图谱推理'),
            ('PathMind', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind', 'targets_task', 'kgqa'),
            ('PathMind', 'targets_task', 'multi-hop-qa'),
            ('PathMind', 'uses_concept', '路径优先化'),
            ('PathMind', 'uses_concept', '重要推理路径'),
            ('PathMind', 'applies_to', '知识图谱推理问答'),
            ('PathMind', 'evaluated_on', 'WebQSP'),
            ('PathMind', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
        ],
    },
    'wiki/methods/RoG.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('RoG', 'based_on', '路径导向知识图谱推理'),
            ('RoG', 'improves_on', '路径导向知识图谱推理'),
            ('RoG', 'targets_task', 'knowledge-graph-reasoning'),
            ('RoG', 'targets_task', 'kgqa'),
            ('RoG', 'targets_task', 'multi-hop-qa'),
        ],
    },
    'wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md': {
        'page_type': 'paper',
        'expected_frontmatter': {},
        'required_edges': [
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'kgqa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'multi-hop-qa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '路径优先化'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '重要推理路径'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'WebQSP'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.sections|PathMind.sections'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.experiments|PathMind.experiments'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.refs|PathMind.refs'),
        ],
    },
    'wiki/concepts/路径优先化.md': {'page_type': 'concept', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/tasks/knowledge-graph-reasoning.md': {'page_type': 'task', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/scenarios/知识图谱推理问答.md': {'page_type': 'scenario', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/benchmarks/WebQSP.md': {'page_type': 'benchmark', 'expected_frontmatter': {}, 'required_edges': []},
    'intermediate/papers/PathMind.sections.md': {'page_type': 'evidence', 'expected_frontmatter': {}, 'required_edges': []},
}
```
```

- [ ] **Step 3: Add page-type discovery and migration-state-aware validation helpers**

Insert these helpers below the existing parsing helpers:

```python
def classify_serving_page(rel: str) -> str | None:
    if rel.startswith('wiki/papers/'):
        return 'paper'
    if rel.startswith('wiki/methods/'):
        return 'method'
    if rel.startswith('wiki/concepts/'):
        return 'concept'
    if rel.startswith('wiki/tasks/'):
        return 'task'
    if rel.startswith('wiki/scenarios/'):
        return 'scenario'
    if rel.startswith('wiki/benchmarks/'):
        return 'benchmark'
    if rel.startswith('intermediate/papers/'):
        return 'evidence'
    return None


def validate_serving_structure(rel: str, text: str, page_type: str) -> list[str]:
    rules = SERVING_TYPE_RULES[page_type]
    page_errors: list[str] = []
    for heading in rules['required_headings']:
        if heading not in text:
            page_errors.append(f'missing serving heading {heading} in {rel}')
    return page_errors


def validate_sample_projection(rel: str, rules: dict[str, object]) -> list[str]:
    text = read_text(rel)
    frontmatter, _body = split_frontmatter(text)
    page_errors: list[str] = []
    for key, expected in rules['expected_frontmatter'].items():
        actual = frontmatter.get(key)
        if actual != expected:
            page_errors.append(f'frontmatter mismatch for {key} in {rel}: expected {expected!r}, got {actual!r}')
    actual_edges = set(extract_formal_relations(text))
    for edge in rules['required_edges']:
        if edge not in actual_edges:
            page_errors.append(f'missing formal relation {edge} in {rel}')
    return page_errors
```
```

- [ ] **Step 4: Replace the current serving-page loop with full-type structure checks plus sample completeness checks**

Replace the current `for rel, rules in SERVING_PAGES.items():` loop with:

```python
for path in (ROOT / 'wiki').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type is None:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))

for path in (ROOT / 'intermediate/papers').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type != 'evidence':
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))

for rel, rules in SERVING_READY_SAMPLES.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing serving-ready sample page: {rel}')
        continue
    text = read_text(rel)
    errors.extend(validate_serving_structure(rel, text, rules['page_type']))
    errors.extend(validate_sample_projection(rel, rules))
```
```

- [ ] **Step 5: Run the parser smoke test again to prove the representative Concept page is now migrated**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('wiki/concepts/路径优先化.md').read_text(encoding='utf-8')
assert '## Formal relations' in text
assert '### Outgoing' in text
assert '### Incoming' in text
PY
```

Expected: no output

- [ ] **Step 6: Run full lint and verify the refactored validator passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 7: Commit the lint refactor**

```bash
git add scripts/lint_graph.py
git commit -m "feat: generalize serving-layer lint validation"
```

---

### Task 6: Migrate the representative Concept page

**Files:**
- Modify: `wiki/concepts/路径优先化.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-friendly evidence and formal relation sections to `wiki/concepts/路径优先化.md`**

Replace the tail of the page starting at `## 与其他概念的关系` with:

```markdown
## 与其他概念的关系
- [[重要推理路径]]：路径优先化的直接输出对象。
- [[knowledge-graph-reasoning]]：在该任务中用于压缩候选路径搜索空间。

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
- `[[路径优先化]] --supports--> [[重要推理路径]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]

### Incoming
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --uses_concept--> [[路径优先化]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```
```

- [ ] **Step 2: Run lint and verify the Concept page passes serving checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Concept migration**

```bash
git add wiki/concepts/路径优先化.md
git commit -m "docs: migrate concept page to serving layer"
```

---

### Task 7: Migrate the representative Task page

**Files:**
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add benchmark/evidence/formal relation sections to `wiki/tasks/knowledge-graph-reasoning.md`**

Replace the tail beginning at `## 相关方法` with:

```markdown
## 相关方法
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[EPERM]]
- [[ToG]]

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
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[GCR]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[EPERM]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[重要推理路径]] --supports--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```
```

- [ ] **Step 2: Run lint and verify the Task page passes serving checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Task migration**

```bash
git add wiki/tasks/knowledge-graph-reasoning.md
git commit -m "docs: migrate task page to serving layer"
```

---

### Task 8: Migrate the representative Scenario page

**Files:**
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add benchmark/evidence/formal relation sections to `wiki/scenarios/知识图谱推理问答.md`**

Replace the tail beginning at `## 使用的主要方法` with:

```markdown
## 使用的主要方法 / 概念
- [[PathMind]] — 通过路径优先化识别重要推理路径，再引导 LLM 完成推理。
- [[RoG]] — 通过显式关系路径生成支持图上的忠实推理。
- [[GCR]] — 通过图约束路径增强 grounded reasoning。
- [[路径优先化]] — 用于压缩候选路径空间并突出高价值证据。

## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

## 相关论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]

## 相关 benchmark
- [[WebQSP]]
- [[CWQ]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/PathMind.sections|PathMind.sections]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- 无

### Incoming
- `[[PathMind]] --applies_to--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```
```

- [ ] **Step 2: Run lint and verify the Scenario page passes serving checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Scenario migration**

```bash
git add wiki/scenarios/知识图谱推理问答.md
git commit -m "docs: migrate scenario page to serving layer"
```

---

### Task 9: Migrate the representative Benchmark page

**Files:**
- Modify: `wiki/benchmarks/WebQSP.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-friendly benchmark sections and `Formal relations` to `wiki/benchmarks/WebQSP.md`**

Replace the tail beginning at `## 相关任务` with:

```markdown
## 相关任务
- [[kgqa]]
- [[multi-hop-qa]]
- [[knowledge-graph-reasoning]]

## 被哪些方法 / 论文使用
- 方法：[[PathMind]]、[[RoG]]、[[GCR]]、[[EPERM]]
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
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
```
```

- [ ] **Step 2: Run lint and verify the Benchmark page passes serving checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Benchmark migration**

```bash
git add wiki/benchmarks/WebQSP.md
git commit -m "docs: migrate benchmark page to serving layer"
```

---

### Task 10: Migrate the representative Evidence page

**Files:**
- Modify: `intermediate/papers/PathMind.sections.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-oriented evidence summary sections near the end of `intermediate/papers/PathMind.sections.md`**

Append the following content to the file:

```markdown
## 本节支撑什么
- 支撑 [[PathMind]] 的总体方法定义、[[路径优先化]] 与 [[重要推理路径]] 的核心概念定位，以及 [[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]] 与 [[知识图谱推理问答]] 上的问题场景描述。

## 来源说明
- 来源 PDF：[[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]
- provenance 账本：[[provenance_links]]

## Formal relations
### Outgoing
- `[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```
```

- [ ] **Step 2: Run lint and verify the Evidence page passes serving checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the Evidence migration**

```bash
git add intermediate/papers/PathMind.sections.md
git commit -m "docs: migrate evidence page to serving layer"
```

---

### Task 11: Run serving-governance verification on the representative migration batch

**Files:**
- Modify: none
- Test: manual skill invocation checklist

- [ ] **Step 1: Review the migrated representative set against the new serving-governance criteria**

Review this exact set:
- `wiki/concepts/路径优先化.md`
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/benchmarks/WebQSP.md`
- `intermediate/papers/PathMind.sections.md`

Check for:
- `## Formal relations` presence
- `### Outgoing` / `### Incoming` presence
- human-readable section alignment with formal projections
- sufficient QA traversability without default ledger fallback

Expected result: classify each page as `pass`, `needs_fixes`, or `blocked`

- [ ] **Step 2: Record the representative migration as serving-ready only if all pages pass**

If all five pages pass, record that this representative batch is serving-ready in the PR/commit notes or follow-up docs. If any page does not pass, keep the batch in partial status and fix the pages before moving to broader migration.

- [ ] **Step 3: Re-run lint after any serving-governance-driven content changes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 12: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full governance check from the final migrated state**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Verify the final scope is limited to the planned framework and representative pages**

Run:

```bash
git diff -- \
  CLAUDE.md \
  wiki/ontology/index.md \
  wiki/ontology/graph-standard.md \
  .claude/skills/serving-governance-review/SKILL.md \
  scripts/lint_graph.py \
  wiki/concepts/路径优先化.md \
  wiki/tasks/knowledge-graph-reasoning.md \
  wiki/scenarios/知识图谱推理问答.md \
  wiki/benchmarks/WebQSP.md \
  intermediate/papers/PathMind.sections.md
```

Expected: diff is limited to the framework files and the five representative pages

- [ ] **Step 3: Commit any final verification-only fixes if needed**

Run:

```bash
git status --short
```

Expected: only planned files remain changed. If verification uncovered issues and you fixed them, commit with:

```bash
git add CLAUDE.md wiki/ontology/index.md wiki/ontology/graph-standard.md .claude/skills/serving-governance-review/SKILL.md scripts/lint_graph.py wiki/concepts/路径优先化.md wiki/tasks/knowledge-graph-reasoning.md wiki/scenarios/知识图谱推理问答.md wiki/benchmarks/WebQSP.md intermediate/papers/PathMind.sections.md
git commit -m "chore: finalize full serving-layer framework rollout"
```

If no verification-only fixes were needed, do not create an extra commit.
