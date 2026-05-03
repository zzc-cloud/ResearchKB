# Knowledge Compile Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce a three-skill knowledge compile pipeline in which `paper-ingest` emits structured relation candidates, `relation-reconciliation` closes formal relation ledgers, and `page-projection-sync` realigns object pages before structural, ontology-semantic, and serving governance.

**Architecture:** First update the `paper-ingest` contract so it emits structured `relation_candidates` and `relation_exemptions` without trying to own full graph closure. Then add two new skills — `relation-reconciliation` for formal-ledger completion and `page-projection-sync` for object-page projection sync. Finally, extend the existing `paper-ingest` eval materials and `scripts/lint_graph.py` so the new pipeline can be trialed on one standard method-paper path and handed cleanly to the existing three governance gates.

**Tech Stack:** Markdown skill definitions under `.claude/skills/`, Python 3 lint script (`scripts/lint_graph.py`), JSON regression samples, ResearchKB relation ledgers and serving-page conventions.

---

## File map

### Skill definitions
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Extend the output contract with relation candidate and exemption blocks, plus explicit handoff to reconciliation.
- Create: `.claude/skills/relation-reconciliation/SKILL.md`
  - Define normalize → diff → reconcile workflow for formal relation ledgers.
- Create: `.claude/skills/page-projection-sync/SKILL.md`
  - Define ledger-to-page sync for `Formal relations`, strong-consistency frontmatter, and templated human-readable relation sections.

### Skill eval and reference assets
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
  - Add checks for emitting structured relation candidates rather than only writing relation files.
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
  - Extend regression expectations to include `relation_candidates` and exemptions in final output.
- Create: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
  - Define what a correct reconciliation pass must prove.
- Create: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Seed 1-2 reconciliation eval fixtures tied to PathMind-style method papers.
- Create: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Define projection-sync expectations.
- Create: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Seed projection-sync eval fixtures.

### Governance / lint integration
- Modify: `scripts/lint_graph.py`
  - Add a small number of compile-pipeline contract checks, without turning lint into a skill runner.

### Planning artifact
- Create: `docs/superpowers/plans/2026-05-03-knowledge-compile-pipeline.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: manual readback of each new skill file

---

### Task 1: Extend `paper-ingest` output contract with structured relation candidates

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: inspect resulting markdown; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Update the architecture positioning language so `paper-ingest` no longer claims to finish graph closure**

In `.claude/skills/paper-ingest/SKILL.md`, replace this block:

```markdown
## 架构定位
本 skill 属于 ResearchKB 的**本体实例编译层**。
它的职责是把原始论文编译成候选知识变更，包括：
- `intermediate/papers/` 证据缓存
- `wiki/` 正式节点页变更
- `wiki/relations/` 正式关系账本变更

它不直接裁决语义合法性；生成结果后必须交给本体治理层继续审查。
```

with:

```markdown
## 架构定位
本 skill 属于 ResearchKB 的**本体实例编译入口**。
它的职责是把原始论文编译成候选知识变更，包括：
- `intermediate/papers/` 证据缓存
- `wiki/` 正式节点页候选变更
- formal relation candidates（供后续 relation reconciliation 使用）

它不直接完成全图 formal relation 闭环，也不裁决语义合法性；生成结果后应先交给 relation reconciliation，再进入本体治理层继续审查。
```

- [ ] **Step 2: Insert a new step after page creation to emit structured candidate relations**

Immediately after `### Step 5: 创建/更新知识库页面`, insert:

```markdown
### Step 5.5: 汇总候选正式关系
在完成页面与缓存候选更新后，必须显式整理本次论文直接支撑的 formal relation candidates，而不是只把关系散落写进正文或关系账本。

输出时至少按以下关系类型归类：
- `proposes`
- `targets_task`
- `evaluated_on`
- `uses_concept`
- `supported_by`
- `cites`
- `applies_to`
- `based_on`
- `improves_on`
- `sourced_from`

并且必须区分三类：
1. direct relations：证据明确、可直接落账
2. high-confidence candidate relations：强支持但仍需 graph-level reconciliation
3. needs-human-review relations：存在方向、粒度或本体归属歧义
```

- [ ] **Step 3: Extend the final YAML summary template with `relation_candidates` and `relation_exemptions`**

In the `## 最终输出格式` section, replace the existing YAML template with:

```yaml
status: success | partial | needs-skill-update
paper_type_guess: method | application | survey | benchmark | dataset | taxonomy | framework | mixed
generated_caches:
  - intermediate/papers/<short_name>.sections.md
  - intermediate/papers/<short_name>.refs.md
  - intermediate/papers/<short_name>.experiments.md | intermediate/papers/<short_name>.analysis.md
  - intermediate/papers/<short_name>.full.md (optional, generated when deep cross-section tracing is needed)
updated_pages:
  - wiki/papers/...
  - wiki/methods/...
  - wiki/concepts/...
  - wiki/scenarios/...
  - wiki/relations/...
relation_candidates:
  proposes: []
  targets_task: []
  evaluated_on: []
  uses_concept: []
  supported_by: []
  cites: []
  applies_to: []
  based_on: []
  improves_on: []
  sourced_from: []
relation_exemptions:
  - relation_type: evaluated_on
    reason: no unified benchmark; exempt by graph-standard
warnings:
  - ...
skill_update_signals:
  - ...
```

- [ ] **Step 4: Add explicit post-ingest handoff steps to reconciliation and governance**

Replace the existing `## Ingest 完成后的治理要求` block with:

```markdown
## Ingest 完成后的后续治理要求
当本次摄入已经完成缓存、wiki 页面与候选关系输出后：
1. 必须先交给 `relation-reconciliation` 补齐 formal relation ledger
2. relation ledger 更新后，必须交给 `page-projection-sync` 回写对象页投影
3. 然后运行 `python3 scripts/lint_graph.py`
4. lint 通过后，必须调用 `ontology-semantic-review` skill 审查语义合理性
5. 如本次改动涉及 serving-ready 页面，还必须调用 `serving-governance-review`
6. 只有结构、语义与 serving 都合理时，才建议接受本次变更并进入 git 提交
```

- [ ] **Step 5: Run lint to ensure the skill-doc changes did not break repository structure expectations**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the `paper-ingest` contract update**

```bash
git add .claude/skills/paper-ingest/SKILL.md
git commit -m "docs: extend paper ingest relation contract"
```

---

### Task 2: Update `paper-ingest` evals to reflect the new output contract

**Files:**
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Test: inspect files in editor

- [ ] **Step 1: Add relation-candidate expectations to the quality checklist**

Append these bullets to `.claude/skills/paper-ingest/evals/quality-checklist.md` under `## Relation autowrite checks`:

```markdown
- [ ] 最终结构化输出必须显式包含 `relation_candidates`，而不是只在正文或关系账本中隐含关系。
- [ ] `relation_candidates` 至少应覆盖：`proposes`、`targets_task`、`evaluated_on`、`uses_concept`、`supported_by`、`cites`、`sourced_from`。
- [ ] 若某类关系按规范豁免，最终结构化输出必须显式包含 `relation_exemptions`。
- [ ] 若存在方向、粒度或本体归属歧义，最终结构化输出必须将对应关系放入 `needs-human-review` 语义，而不是静默忽略。
```

- [ ] **Step 2: Extend the PathMind regression sample with the new contract expectations**

In `.claude/skills/paper-ingest/evals/regression-samples.json`, append these `quality_checks` to the `PathMind` sample:

```json
"必须在最终输出中显式列出 relation_candidates",
"relation_candidates 必须至少覆盖 proposes、targets_task、evaluated_on、uses_concept、supported_by、cites、sourced_from",
"若无关系豁免，则 relation_exemptions 应为空数组而不是缺失"
```

- [ ] **Step 3: Extend the survey regression sample with exemption expectations**

In the `LLM-KG-CPD-Survey` sample, append these `quality_checks`:

```json
"最终输出必须显式包含 relation_candidates",
"最终输出必须显式包含 relation_exemptions",
"evaluated_on 的豁免必须在 relation_exemptions 中说明，而不是仅写在 warnings 里"
```

- [ ] **Step 4: Commit the eval contract update**

```bash
git add .claude/skills/paper-ingest/evals/quality-checklist.md .claude/skills/paper-ingest/evals/regression-samples.json
git commit -m "test: extend paper ingest eval contract"
```

---

### Task 3: Create the `relation-reconciliation` skill

**Files:**
- Create: `.claude/skills/relation-reconciliation/SKILL.md`
- Create: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Create: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Test: inspect files; `ls .claude/skills/relation-reconciliation`

- [ ] **Step 1: Create the main skill file**

Write `.claude/skills/relation-reconciliation/SKILL.md` with this content:

```markdown
---
name: relation-reconciliation
description: 在 `paper-ingest` 完成后，对照 relation_candidates、Evidence 缓存、对象页与当前 `wiki/relations/*.md` 正式账本，补齐 formal relation ledger，并输出 added/already_present/exempt/needs-human-review 结果。Whenever 单篇论文 ingest 完成后需要补齐 formal relations、比较 evidence 与 ledger 差异、检查哪些关系已存在/缺失/应豁免、或要把候选关系正确分发到各关系账本时，都应使用本 skill。
---

# Relation Reconciliation

你是 ResearchKB 的 formal relation reconciliation stage。你的任务不是重新解析论文，而是在 `paper-ingest` 之后，把候选关系、对象页暗示关系、Evidence 支撑关系与当前 formal ledger 对齐并补齐。

## 核心职责
1. 读取 `paper-ingest` 输出中的 `relation_candidates` 与 `relation_exemptions`
2. 读取本次改动涉及的对象页与 Evidence 缓存
3. 读取当前 `wiki/relations/*.md` 正式账本
4. 进行 normalize → diff → reconcile
5. 将缺失正式边写入正确的关系文件
6. 输出结构化 reconciliation 摘要，并指出受影响对象页供 `page-projection-sync` 使用

## 不负责
- 不重新做 PDF 解析
- 不改写解释性正文
- 不做最终 ontology verdict
- 不做 serving-ready 最终发布裁决

## Normalize
把所有候选关系统一规范成：
- source
- relation_type
- target
- evidence
- source_of_claim（ingest / page / evidence / ledger）

## Diff
对比：
- candidate edges
- page-implied edges
- evidence-backed edges
- current formal ledger edges
- explicit exemptions

## Reconcile 输出分类
- `already_present`
- `add_now`
- `exempt`
- `needs_human_review`

## Ledger routing
- `proposes` → `wiki/relations/paper_method_links.md`
- `targets_task` → `wiki/relations/task_method_map.md`
- `evaluated_on` → `wiki/relations/benchmark_links.md`
- `uses_concept` / `supports` / `depends_on` / `applies_to` → `wiki/relations/concept_links.md`
- `based_on` / `improves_on` → `wiki/relations/method_evolution.md`
- `cites` → `wiki/relations/citation_graph.md`
- `supported_by` → `wiki/relations/evidence_index.md`
- `sourced_from` → `wiki/relations/provenance_links.md`

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
already_present: []
added_relations:
  - file: wiki/relations/task_method_map.md
    edge: "[[Paper]] --targets_task--> [[Task]]"
    evidence: "[[intermediate/papers/foo.sections|foo.sections]] §x"
exemptions: []
needs_human_review: []
affected_pages: []
```
```

- [ ] **Step 2: Create the skill quality checklist**

Write `.claude/skills/relation-reconciliation/evals/quality-checklist.md` with:

```markdown
# Relation Reconciliation Quality Checklist

## Input handling
- [ ] Reads `relation_candidates` and `relation_exemptions` from ingest output.
- [ ] Reads affected object pages, evidence caches, and current relation ledgers.

## Reconciliation logic
- [ ] Distinguishes `already_present`, `add_now`, `exempt`, and `needs_human_review`.
- [ ] Routes each relation type to the correct `wiki/relations/*.md` file.
- [ ] Detects prose-ledger drift when a page implies a relation that is missing from the formal ledger.

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists affected pages for downstream page-projection sync.
- [ ] Does not silently drop ambiguous edges.
```

- [ ] **Step 3: Create one regression sample file for a standard method-paper case**

Write `.claude/skills/relation-reconciliation/evals/regression-samples.json` with:

```json
[
  {
    "name": "PathMind-method-paper",
    "input_assumption": "paper-ingest has emitted relation_candidates for a standard empirical method paper",
    "must_reconcile": [
      "proposes",
      "targets_task",
      "evaluated_on",
      "uses_concept",
      "supported_by",
      "cites",
      "sourced_from"
    ],
    "quality_checks": [
      "must classify existing ledger edges as already_present",
      "must add missing formal edges to the correct ledger file",
      "must preserve explicit relation exemptions",
      "must output affected_pages for page-projection-sync"
    ]
  }
]
```

- [ ] **Step 4: Verify the new skill directory exists**

Run: `find .claude/skills/relation-reconciliation -maxdepth 2 -type f`
Expected: `SKILL.md`, `evals/quality-checklist.md`, and `evals/regression-samples.json`

- [ ] **Step 5: Commit the new reconciliation skill**

```bash
git add .claude/skills/relation-reconciliation
git commit -m "feat: add relation reconciliation skill"
```

---

### Task 4: Create the `page-projection-sync` skill

**Files:**
- Create: `.claude/skills/page-projection-sync/SKILL.md`
- Create: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Create: `.claude/skills/page-projection-sync/evals/regression-samples.json`
- Test: inspect files; `ls .claude/skills/page-projection-sync`

- [ ] **Step 1: Create the main sync skill file**

Write `.claude/skills/page-projection-sync/SKILL.md` with:

```markdown
---
name: page-projection-sync
description: 在 formal relation ledger 更新后，把最新 ledger 投影同步回对象页：更新 `Formal relations`、强一致 frontmatter 和模板化人类关系区块。Whenever relation-reconciliation 已补齐 formal ledger，需要让对象页重新与账本对齐、更新 serving-ready 页面投影、同步 `parent_methods` / `child_methods` 等强一致字段，或批量刷新页面中的关系区块时，都应使用本 skill。
---

# Page Projection Sync

你是 ResearchKB 的 page projection synchronization stage。你的任务是在 relation ledger 已更新后，把 formal graph truth 同步回对象页。

## 自动同步内容
1. `## Formal relations`
2. 强一致 frontmatter（当前包括 `parent_methods` / `child_methods`）
3. 模板化人类友好关系区块（相关方法、相关任务、相关概念、相关 benchmark、代表论文、证据来源等）

## 不自动同步
- 方法解释性正文
- 核心问题分析
- 优势与局限
- 关键结论
- 批注与综述判断

## 输入
- 更新后的 formal ledgers
- `relation-reconciliation` 输出
- 受影响对象页列表

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_pages:
  - path: wiki/methods/Foo.md
    updated_sections:
      - formal_relations
      - frontmatter
      - human_relation_blocks
manual_followups:
  - path: wiki/papers/Bar.md
    reason: interpretive prose not auto-synced
```
```

- [ ] **Step 2: Create the sync skill quality checklist**

Write `.claude/skills/page-projection-sync/evals/quality-checklist.md` with:

```markdown
# Page Projection Sync Quality Checklist

## Inputs
- [ ] Reads updated formal ledgers.
- [ ] Reads relation-reconciliation output including `affected_pages`.

## Sync behavior
- [ ] Updates `## Formal relations` consistently.
- [ ] Updates strong-consistency frontmatter fields.
- [ ] Updates templated human-readable relation blocks.
- [ ] Does not rewrite interpretive prose.

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists any manual followups that still require human editing.
```

- [ ] **Step 3: Create one regression sample file for a serving-page sync case**

Write `.claude/skills/page-projection-sync/evals/regression-samples.json` with:

```json
[
  {
    "name": "method-page-sync",
    "input_assumption": "relation-reconciliation has added or confirmed method evolution, task, benchmark, and proposes edges",
    "must_sync": [
      "Formal relations",
      "strong-consistency frontmatter",
      "templated human relation blocks"
    ],
    "quality_checks": [
      "must update parent_methods and child_methods when affected",
      "must keep interpretive prose untouched",
      "must report manual followups if prose still needs human review"
    ]
  }
]
```

- [ ] **Step 4: Verify the new skill directory exists**

Run: `find .claude/skills/page-projection-sync -maxdepth 2 -type f`
Expected: `SKILL.md`, `evals/quality-checklist.md`, and `evals/regression-samples.json`

- [ ] **Step 5: Commit the new page sync skill**

```bash
git add .claude/skills/page-projection-sync
git commit -m "feat: add page projection sync skill"
```

---

### Task 5: Add minimal pipeline contract checks to `scripts/lint_graph.py`

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add new lint needles for the compile-pipeline documentation contract**

After `CLAUDE_NEEDLES`, add:

```python
PIPELINE_SKILL_FILES = [
    '.claude/skills/relation-reconciliation/SKILL.md',
    '.claude/skills/page-projection-sync/SKILL.md',
]

PAPER_INGEST_NEEDLES = [
    'relation_candidates',
    'relation_exemptions',
    'relation-reconciliation',
    'page-projection-sync',
]
```

- [ ] **Step 2: Add validation loops for the new skill files and ingest contract markers**

Insert this before the final `if errors:` block:

```python
paper_ingest_text = read_text('.claude/skills/paper-ingest/SKILL.md')
for needle in PAPER_INGEST_NEEDLES:
    if needle not in paper_ingest_text:
        errors.append(f'missing {needle} in .claude/skills/paper-ingest/SKILL.md')

for rel in PIPELINE_SKILL_FILES:
    if not (ROOT / rel).exists():
        errors.append(f'missing pipeline skill file: {rel}')
```

- [ ] **Step 3: Run lint to verify the compile-pipeline contract passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit the lint contract update**

```bash
git add scripts/lint_graph.py
git commit -m "test: validate knowledge compile pipeline contract"
```

---

### Task 6: Document a minimal rollout path inside the new skills

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: inspect both files in editor

- [ ] **Step 1: Add a rollout note to `relation-reconciliation`**

Append this block to `.claude/skills/relation-reconciliation/SKILL.md`:

```markdown
## 最小 rollout 建议
- 先在标准 empirical 方法论文上试跑（如 PathMind 类论文）。
- 再扩到 survey / framework 论文。
- 每次 reconciliation 完成后，都应将 `affected_pages` 交给 `page-projection-sync`，而不是停留在 ledger 已更新但页面未同步的状态。
```

- [ ] **Step 2: Add a rollout note to `page-projection-sync`**

Append this block to `.claude/skills/page-projection-sync/SKILL.md`:

```markdown
## 最小 rollout 建议
- 先在已具备 serving-ready 基础模板的 Method / Paper 页试跑。
- 然后扩到 Concept / Task / Scenario / Benchmark / Evidence。
- 同步完成后，必须再交给 lint、ontology-semantic-review 与 serving-governance-review。
```

- [ ] **Step 3: Commit the rollout-note update**

```bash
git add .claude/skills/relation-reconciliation/SKILL.md .claude/skills/page-projection-sync/SKILL.md
git commit -m "docs: add compile pipeline rollout guidance"
```

---

### Task 7: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full lint check for the compile pipeline design implementation**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Verify the final diff is limited to pipeline-contract files**

Run:

```bash
git diff -- \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/paper-ingest/evals/quality-checklist.md \
  .claude/skills/paper-ingest/evals/regression-samples.json \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/relation-reconciliation/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  .claude/skills/page-projection-sync/evals/regression-samples.json \
  scripts/lint_graph.py
```

Expected: diff limited to the ingest contract, new skills, eval files, and lint contract checks.

- [ ] **Step 3: Commit any verification-only fixes if needed**

Run:

```bash
git status --short
```

Expected: only planned files remain changed. If verification uncovered issues and you fixed them, commit with:

```bash
git add .claude/skills/paper-ingest/SKILL.md .claude/skills/paper-ingest/evals/quality-checklist.md .claude/skills/paper-ingest/evals/regression-samples.json .claude/skills/relation-reconciliation .claude/skills/page-projection-sync scripts/lint_graph.py
git commit -m "chore: finalize knowledge compile pipeline contract"
```

If no verification-only fixes were needed, do not create an extra commit.
