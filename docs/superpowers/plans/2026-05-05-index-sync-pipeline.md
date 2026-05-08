# Index Sync Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicit `index-sync` stage to the ResearchKB paper compile pipeline, give it a dedicated skill contract, mark index pages with managed blocks, and teach lint + serving governance to treat indexes as first-class navigation/QA surfaces.

**Architecture:** Implement this as a contract-first Phase 1 rollout. First, tighten pipeline-contract lint so `index-sync` becomes a required stage and create/update the workflow + skill docs to satisfy that contract. Second, add navigation-governance norms and a dedicated `index-sync` skill. Third, wrap `ontology/index.md` and all entity index pages in explicit managed blocks, create the missing benchmarks index, and extend `scripts/lint_graph.py` to validate index completeness and managed-block integrity.

**Tech Stack:** Markdown workflow/spec files, Claude skill docs under `.claude/skills/`, Python 3 lint script (`scripts/lint_graph.py`), entity index pages under `ontology/entities/*/index.md`.

---

## File map

### Workflow / skill contracts
- Modify: `CLAUDE.md`
  - Insert `index-sync` into the default single-paper and batch compile chains; add an interruption rule for `index-sync` failures.
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Remove ambiguous index-maintenance ownership from ingest; hand off to `relation-reconciliation` → `page-projection-sync` → `index-sync`.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - End object-page projection at `index-sync`, not directly at governance.
- Create: `.claude/skills/index-sync/SKILL.md`
  - Define the new fourth-stage skill contract.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Expand review scope from object pages to index/navigation surfaces.

### Normative ontology guidance
- Modify: `ontology/graph-standard.md`
  - Add an `Index 导航投影层` section and update the normative compile chain to include `index-sync`.

### Navigation surfaces
- Modify: `ontology/index.md`
  - Add a managed block around object-domain navigation.
- Modify: `ontology/entities/papers/index.md`
  - Add managed blocks for core entry, grouped navigation, and canonical list.
- Modify: `ontology/entities/methods/index.md`
  - Add managed blocks for core entry, grouped navigation, and canonical list.
- Modify: `ontology/entities/concepts/index.md`
  - Add managed blocks for core entry, grouped navigation, and canonical list.
- Modify: `ontology/entities/tasks/index.md`
  - Add managed blocks for core entry, grouped navigation, and canonical list.
- Modify: `ontology/entities/scenarios/index.md`
  - Add managed blocks for core entry, grouped navigation, and canonical list.
- Create: `ontology/entities/benchmarks/index.md`
  - Create the missing domain index with Phase 1 managed blocks and empty-state placeholders.

### Lint / verification
- Modify: `scripts/lint_graph.py`
  - Add pipeline-contract needles for `index-sync`, require the new skill file and benchmarks index, and validate managed blocks + canonical-list coverage.
- Test: `python3 scripts/lint_graph.py`
  - This repository has no dedicated test directory right now; `scripts/lint_graph.py` is the executable verification surface for this feature.

---

### Task 1: Make `index-sync` a required pipeline stage

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Create: `.claude/skills/index-sync/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing lint contract for the new stage**

In `scripts/lint_graph.py`, replace the existing pipeline constants block:

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

DAILY_INGEST_CHAIN_NEEDLES = [
    'relation-reconciliation',
    'page-projection-sync',
    'ontology-semantic-review',
    'serving-governance-review',
]
```

with:

```python
PIPELINE_SKILL_FILES = [
    '.claude/skills/relation-reconciliation/SKILL.md',
    '.claude/skills/page-projection-sync/SKILL.md',
    '.claude/skills/index-sync/SKILL.md',
]

PAPER_INGEST_NEEDLES = [
    'relation_candidates',
    'relation_exemptions',
    'relation-reconciliation',
    'page-projection-sync',
    'index-sync',
]

DAILY_INGEST_CHAIN_NEEDLES = [
    'relation-reconciliation',
    'page-projection-sync',
    'index-sync',
    'ontology-semantic-review',
    'serving-governance-review',
]

INDEX_SYNC_NEEDLES = [
    '# Index Sync',
    '受管区块',
    'synced_indexes',
    'skipped_pages',
    'manual_followups',
]
```

Then replace the existing pipeline-handoff checks:

```python
for needle in DAILY_INGEST_CHAIN_NEEDLES:
    if needle not in read_text('CLAUDE.md'):
        errors.append(f'missing {needle} in CLAUDE.md daily ingest chain')
    if needle in ['ontology-semantic-review', 'serving-governance-review']:
        if needle not in read_text('.claude/skills/page-projection-sync/SKILL.md'):
            errors.append(f'missing {needle} in page-projection-sync handoff')

if 'page-projection-sync' not in read_text('.claude/skills/relation-reconciliation/SKILL.md'):
    errors.append('missing page-projection-sync in relation-reconciliation handoff')
```

with:

```python
for needle in DAILY_INGEST_CHAIN_NEEDLES:
    if needle not in read_text('CLAUDE.md'):
        errors.append(f'missing {needle} in CLAUDE.md daily ingest chain')

page_projection_text = read_text('.claude/skills/page-projection-sync/SKILL.md')
for needle in ['index-sync', 'ontology-semantic-review', 'serving-governance-review']:
    if needle not in page_projection_text:
        errors.append(f'missing {needle} in page-projection-sync handoff')

if 'page-projection-sync' not in read_text('.claude/skills/relation-reconciliation/SKILL.md'):
    errors.append('missing page-projection-sync in relation-reconciliation handoff')

index_sync_path = ROOT / '.claude/skills/index-sync/SKILL.md'
if index_sync_path.exists():
    index_sync_text = read_text('.claude/skills/index-sync/SKILL.md')
    for needle in INDEX_SYNC_NEEDLES:
        if needle not in index_sync_text:
            errors.append(f'missing {needle} in .claude/skills/index-sync/SKILL.md')
```

- [ ] **Step 2: Run lint to verify the contract fails before the docs exist**

Run: `python3 scripts/lint_graph.py`
Expected: `FAIL` with errors including missing `.claude/skills/index-sync/SKILL.md` and missing `index-sync` in pipeline handoff text.

- [ ] **Step 3: Update `CLAUDE.md` to include the new stage and stop condition**

In `CLAUDE.md`, replace the existing single-paper block:

```markdown
### 处理单篇论文
当我说 **“处理论文：[文件路径或论文标题]”** 时，默认走完整单篇论文编译链：
1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

其中：
- `paper-ingest` 是编译入口，不代表正式入图完成
- `relation-reconciliation` 负责补齐 formal relation ledger
- `page-projection-sync` 负责把 formal graph truth 同步回对象页
- 只有三层治理都通过后，才算可进入正式图谱
- 如与 `ontology/graph-standard.md` 冲突，以后者为准
```

with:

```markdown
### 处理单篇论文
当我说 **“处理论文：[文件路径或论文标题]”** 时，默认走完整单篇论文编译链：
1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

其中：
- `paper-ingest` 是编译入口，不代表正式入图完成
- `relation-reconciliation` 负责补齐 formal relation ledger
- `page-projection-sync` 负责把 formal graph truth 同步回对象页
- `index-sync` 负责把对象页与关系页的稳定结构同步到导航 index
- 只有三层治理都通过后，才算可进入正式图谱
- 如与 `ontology/graph-standard.md` 冲突，以后者为准
```

Then replace the batch block:

```markdown
### 批量处理论文
当我说 **“批量处理 raw/ 目录下的所有论文”** 时：
- 仍以单篇论文编译链为基本执行单元：`paper-ingest` → `relation-reconciliation` → `page-projection-sync` → 三层治理
- 先列出候选论文并按主题 / 年份分组，与我确认顺序
- 逐篇汇报进度，避免无确认的大规模落库
- 不允许只批量跑 `paper-ingest` 而跳过后续 relation / projection / 治理阶段
```

with:

```markdown
### 批量处理论文
当我说 **“批量处理 raw/ 目录下的所有论文”** 时：
- 仍以单篇论文编译链为基本执行单元：`paper-ingest` → `relation-reconciliation` → `page-projection-sync` → `index-sync` → 三层治理
- 先列出候选论文并按主题 / 年份分组，与我确认顺序
- 逐篇汇报进度，避免无确认的大规模落库
- 不允许只批量跑 `paper-ingest` 而跳过后续 relation / projection / index sync / 治理阶段
```

Then replace the interruption block:

```markdown
### 单篇论文编译链的中断条件
以下情况允许或要求中断默认编译链：
- `paper-ingest` 输出 `needs-skill-update`
- `relation-reconciliation` 输出大量 `needs_human_review`
- `page-projection-sync` 输出大量 `manual_followups`
- 任一治理 gate 失败

中断时必须明确说明：
- 当前停在哪一阶段
- 已经完成了什么
- 下一阶段为什么不能安全继续
```

with:

```markdown
### 单篇论文编译链的中断条件
以下情况允许或要求中断默认编译链：
- `paper-ingest` 输出 `needs-skill-update`
- `relation-reconciliation` 输出大量 `needs_human_review`
- `page-projection-sync` 输出大量 `manual_followups`
- `index-sync` 输出大量 `manual_followups` 或 `needs-human-review`
- 任一治理 gate 失败

中断时必须明确说明：
- 当前停在哪一阶段
- 已经完成了什么
- 下一阶段为什么不能安全继续
```

- [ ] **Step 4: Update `paper-ingest` and `page-projection-sync` handoff text**

In `.claude/skills/paper-ingest/SKILL.md`, replace the existing post-ingest governance section:

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

with:

```markdown
## Ingest 完成后的后续治理要求
当本次摄入已经完成缓存、wiki 页面与候选关系输出后：
1. 在日常 ingest 流程中，`paper-ingest` 结束后默认进入 `relation-reconciliation`
2. `relation-reconciliation` 完成后，必须进入 `page-projection-sync`
3. `page-projection-sync` 完成后，必须进入 `index-sync`
4. `index-sync` 完成后，必须运行 `python3 scripts/lint_graph.py`
5. lint 通过后，必须调用 `ontology-semantic-review` skill 审查语义合理性
6. 如本次改动涉及 serving-ready 页面，还必须调用 `serving-governance-review`
7. 只有结构、语义与 serving 都合理时，才建议接受本次变更并进入 git 提交
```

In `.claude/skills/page-projection-sync/SKILL.md`, replace the existing stage-position and successor text:

```markdown
## 链路位置
本 skill 是单篇论文日常编译链的第三阶段，默认前置为 `relation-reconciliation`。
本 skill 完成后不视为流程结束，而应继续进入三层治理出口。
```

with:

```markdown
## 链路位置
本 skill 是单篇论文日常编译链的第三阶段，默认前置为 `relation-reconciliation`。
本 skill 完成后不视为流程结束，而应继续进入 `index-sync` 与后续三层治理出口。
```

Then replace the existing successor section:

```markdown
## 完成后的默认后继阶段
当本 skill 完成对象页投影同步后，默认进入以下三层治理：
1. `python3 scripts/lint_graph.py`
2. `ontology-semantic-review`
3. `serving-governance-review`

若其中任一阶段失败，则本次论文处理流程不得视为正式入图完成。
```

with:

```markdown
## 完成后的默认后继阶段
当本 skill 完成对象页投影同步后，默认进入以下后继阶段：
1. `index-sync`
2. `python3 scripts/lint_graph.py`
3. `ontology-semantic-review`
4. `serving-governance-review`

若其中任一阶段失败，则本次论文处理流程不得视为正式入图完成。
```

- [ ] **Step 5: Create the new `index-sync` skill contract**

Create `.claude/skills/index-sync/SKILL.md` with exactly this content:

```markdown
---
name: index-sync
description: 在 `page-projection-sync` 完成后，把对象页与导航页之间的投影补齐到 index 层：更新 `ontology/index.md`、`ontology/entities/*/index.md` 的受管区块，并输出 `synced_indexes`、`skipped_pages` 与 `manual_followups`。Whenever 对象页 formal projection 已完成且需要刷新系统入口、对象域 index、或判断哪些页面可被索引但暂不应 default serve 时，都应使用本 skill。
---

# Index Sync

你是 ResearchKB 的 navigation index synchronization stage。你的任务是在对象页真相已经同步后，把可安全收录的页面投影到导航面。

## 链路位置
本 skill 是单篇论文日常编译链的第四阶段，默认前置为 `page-projection-sync`。
本 skill 完成后不视为流程结束，而应继续进入结构治理、本体语义治理与 serving 治理。

## 自动同步内容
1. `ontology/index.md` 中的对象域导航受管区块
2. `ontology/entities/*/index.md` 中的 `core-entry`、`grouped-navigation` 与 `canonical-list` 受管区块
3. 后续 phase 2 才纳入的 relation-ledger 导航受管区块

## 不自动同步
- 对象页解释性正文
- relation ledger 实例边正文
- index 页的人类导读、综述判断与非受管备注

## 输入
- `page-projection-sync` 输出的 `synced_pages` / `manual_followups`
- 当前对象页集合
- 当前 index 页内容
- 受控 frontmatter 与 `## Formal relations` 结构

## 真源
- 页面存在性
- 节点类型所需 frontmatter
- 足以判断导航归属的稳定结构

## 收录规则
- 页面可被 index 收录，不等于页面可作为默认 serving 入口
- 若页面缺少安全收录所需结构，应跳过并记录 followup
- 不得通过猜测补齐分组或伪造入口状态

## 受管区块
- 只允许更新 `<!-- BEGIN MANAGED BLOCK:... -->` 与 `<!-- END MANAGED BLOCK:... -->` 之间的内容
- 不得重写区块外 prose
- Phase 1 先覆盖 `ontology/index.md` 与 `ontology/entities/*/index.md`

## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_indexes:
  - path: ontology/index.md
    updated_blocks:
      - object-domain-navigation
skipped_pages: []
manual_followups: []
```

## 完成后的默认后继阶段
1. `python3 scripts/lint_graph.py`
2. `ontology-semantic-review`
3. `serving-governance-review`
```

- [ ] **Step 6: Run lint to verify the new pipeline contract passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 7: Commit the pipeline-stage contract changes**

Run:

```bash
git add CLAUDE.md .claude/skills/paper-ingest/SKILL.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md scripts/lint_graph.py
git commit -m "docs: add index-sync pipeline stage"
```

Expected: a new commit containing only the stage-contract and lint-needle changes above.

---

### Task 2: Add index-governance norms and serving-review coverage

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `ontology/graph-standard.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing lint needles for index governance text**

In `scripts/lint_graph.py`, replace the existing `GRAPH_STANDARD_NEEDLES` block:

```python
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    '`cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`',
    '方法机制优先绑定 `sections.md`。',
    'paper_method_links.md',
    'benchmark_links.md',
    'provenance_links.md',
    '`ontology/relations/paper_method_links.md`：维护 `proposes`',
    '`ontology/relations/benchmark_links.md`：维护 `evaluated_on`',
    '`ontology/relations/evidence_index.md`：维护 `supported_by`',
    '`ontology/relations/provenance_links.md`：维护 `sourced_from`',
]
```

with:

```python
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    '`cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`',
    '方法机制优先绑定 `sections.md`。',
    'paper_method_links.md',
    'benchmark_links.md',
    'provenance_links.md',
    '`ontology/relations/paper_method_links.md`：维护 `proposes`',
    '`ontology/relations/benchmark_links.md`：维护 `evaluated_on`',
    '`ontology/relations/evidence_index.md`：维护 `supported_by`',
    '`ontology/relations/provenance_links.md`：维护 `sourced_from`',
    '## Index 导航投影层',
    '`index-sync`',
    '可被 index 收录',
    '默认 serving 入口',
]
```

Then add a new serving-review needle block immediately after `INDEX_NEEDLES`:

```python
SERVING_GOVERNANCE_NEEDLES = [
    'index pages',
    'default navigation/QA entry surfaces',
    'indexed but not default-serving',
]
```

and add this check immediately after the existing `INDEX_NEEDLES` loop:

```python
serving_review_text = read_text('.claude/skills/serving-governance-review/SKILL.md')
for needle in SERVING_GOVERNANCE_NEEDLES:
    if needle not in serving_review_text:
        errors.append(f'missing {needle} in .claude/skills/serving-governance-review/SKILL.md')
```

- [ ] **Step 2: Run lint to verify the new governance contract fails first**

Run: `python3 scripts/lint_graph.py`
Expected: `FAIL` with missing `## Index 导航投影层` and missing index-governance phrases in `.claude/skills/serving-governance-review/SKILL.md`.

- [ ] **Step 3: Update `ontology/graph-standard.md` and `serving-governance-review` to satisfy the contract**

In `ontology/graph-standard.md`, insert this new section immediately before `## 服务层治理校验要求`:

```markdown
## Index 导航投影层
- `ontology/index.md` 与 `ontology/entities/*/index.md` 是导航投影层，不是 formal relation truth source。
- index 页中的受管区块由 `index-sync` 维护；区块外 prose 可保留人工导读与解释。
- 页面“可被 index 收录”和“可作为默认 serving 入口暴露”是两个不同状态。
- index 结构完整性由 `python3 scripts/lint_graph.py` 负责；index 的默认入口质量由 `serving-governance-review` 负责。
```

Then replace the existing single-paper chain block:

```markdown
## 单篇论文编译链
单篇论文进入正式图谱时，默认按以下顺序完成：
1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `python3 scripts/lint_graph.py`
5. `ontology-semantic-review`
6. `serving-governance-review`

其中：
- `paper-ingest` 负责抽取与候选输出
- `relation-reconciliation` 负责 formal relation ledger 补齐
- `page-projection-sync` 负责把 formal graph truth 同步回对象页
- 只有三层治理通过后，才视为可进入正式图谱

其中 serving 治理是独立发布门槛，不等同于结构 lint，也不等同于本体语义审查。
```

with:

```markdown
## 单篇论文编译链
单篇论文进入正式图谱时，默认按以下顺序完成：
1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

其中：
- `paper-ingest` 负责抽取与候选输出
- `relation-reconciliation` 负责 formal relation ledger 补齐
- `page-projection-sync` 负责把 formal graph truth 同步回对象页
- `index-sync` 负责把对象页与导航页之间的稳定结构投影到 index 层
- 只有三层治理通过后，才视为可进入正式图谱

其中 serving 治理是独立发布门槛，不等同于结构 lint，也不等同于本体语义审查。
```

In `.claude/skills/serving-governance-review/SKILL.md`, replace the entire file with exactly this content:

```markdown
# Serving Governance Review

Review migrated knowledge pages and index pages to decide whether they are ready to serve as default constrained-QA entry surfaces and default navigation/QA entry surfaces.

## Use this when
- A batch of Paper / Method / Concept / Task / Scenario / Benchmark / Evidence pages has been migrated to the serving-layer model.
- `ontology/index.md` or `ontology/entities/*/index.md` changed and you need to decide whether the index surfaces are safe as default navigation/QA entry surfaces.
- You need to decide whether pages or indexes are `serving-ready`, `partial`, or `legacy`.
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
   - Are there missing key neighbors that would force runtime fallback to `ontology/relations/`?

4. **Index navigation quality**
   - Do `ontology/index.md` and `ontology/entities/*/index.md` expose the right default entry layer?
   - Are stub / placeholder / structurally incomplete pages incorrectly promoted as default entries?
   - Do index grouping and labels match actual page state?
   - Can a reader or LLM traverse from index → object page → Formal relations → adjacent object / Evidence pages without hidden fallback?
   - If a page is only indexed but not ready to be a default surface, is it distinguished rather than mixed into the default-serving layer?

5. **Release readiness**
   - Is this page or batch safe to promote as the default QA serving surface?
   - Are index pages safe to promote as default navigation/QA entry surfaces?

## Output states
- `pass`: serving-ready
- `needs_fixes`: structurally or semantically usable, but not ready as default serving surface
- `blocked`: should not be promoted to serving-ready

## Constraints
- Do not redo structure lint.
- Do not redo ontology-semantic-review.
- Focus only on the distinct serving-surface quality gate.
- Treat “indexed but not default-serving” as a valid intermediate state when the page is discoverable but not yet safe to expose as a default QA surface.
```

- [ ] **Step 4: Run lint to verify the index-governance contract passes**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit the governance-contract changes**

Run:

```bash
git add ontology/graph-standard.md .claude/skills/serving-governance-review/SKILL.md scripts/lint_graph.py
git commit -m "docs: define index governance contract"
```

Expected: a new commit containing only the graph-standard + serving-review + lint-needle updates above.

---

### Task 3: Add managed blocks to index pages and validate them with lint

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `ontology/index.md`
- Modify: `ontology/entities/papers/index.md`
- Modify: `ontology/entities/methods/index.md`
- Modify: `ontology/entities/concepts/index.md`
- Modify: `ontology/entities/tasks/index.md`
- Modify: `ontology/entities/scenarios/index.md`
- Create: `ontology/entities/benchmarks/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing managed-block and domain-index lint checks**

In `scripts/lint_graph.py`, add `ontology/entities/benchmarks/index.md` to `REQUIRED_FILES`:

```python
REQUIRED_FILES = [
    'ontology/index.md',
    'ontology/graph-standard.md',
    'ontology/log.md',
    'ontology/entities/benchmarks/index.md',
    'ontology/relations/citation_graph.md',
    'ontology/relations/method_evolution.md',
    'ontology/relations/concept_links.md',
    'ontology/relations/task_method_map.md',
    'ontology/relations/evidence_index.md',
    'ontology/relations/paper_method_links.md',
    'ontology/relations/benchmark_links.md',
    'ontology/relations/provenance_links.md',
    'scripts/lint_graph.py',
]
```

Then insert these constants immediately after `NAVIGATION_ENTRY_PATH = 'ontology/index.md'`:

```python
DOMAIN_INDEX_FILES = [
    'ontology/entities/papers/index.md',
    'ontology/entities/methods/index.md',
    'ontology/entities/concepts/index.md',
    'ontology/entities/tasks/index.md',
    'ontology/entities/scenarios/index.md',
    'ontology/entities/benchmarks/index.md',
]

INDEX_MANAGED_BLOCKS = {
    'ontology/index.md': ['object-domain-navigation'],
    'ontology/entities/papers/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
    'ontology/entities/methods/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
    'ontology/entities/concepts/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
    'ontology/entities/tasks/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
    'ontology/entities/scenarios/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
    'ontology/entities/benchmarks/index.md': ['core-entry', 'grouped-navigation', 'canonical-list'],
}

ROOT_INDEX_DOMAIN_LINKS = [
    '[[entities/papers/index|ontology/entities/papers/index.md]]',
    '[[entities/methods/index|ontology/entities/methods/index.md]]',
    '[[entities/concepts/index|ontology/entities/concepts/index.md]]',
    '[[entities/tasks/index|ontology/entities/tasks/index.md]]',
    '[[entities/scenarios/index|ontology/entities/scenarios/index.md]]',
    '[[entities/benchmarks/index|ontology/entities/benchmarks/index.md]]',
]
```

Then insert these helper functions immediately after `validate_sample_projection`:

```python
def extract_managed_block(text: str, name: str) -> str | None:
    start = f'<!-- BEGIN MANAGED BLOCK:{name} -->'
    end = f'<!-- END MANAGED BLOCK:{name} -->'
    if start not in text or end not in text:
        return None
    return text.split(start, 1)[1].split(end, 1)[0]


def validate_index_pages(errors: list[str]) -> None:
    root_text = read_text('ontology/index.md')
    root_block = extract_managed_block(root_text, 'object-domain-navigation')
    if root_block is None:
        errors.append('missing managed block object-domain-navigation in ontology/index.md')
    else:
        for needle in ROOT_INDEX_DOMAIN_LINKS:
            if needle not in root_block:
                errors.append(f'missing domain navigation link {needle} in ontology/index.md')

    for rel in DOMAIN_INDEX_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f'missing domain index file: {rel}')
            continue
        text = read_text(rel)
        for block_name in INDEX_MANAGED_BLOCKS[rel]:
            block = extract_managed_block(text, block_name)
            if block is None:
                errors.append(f'missing managed block {block_name} in {rel}')
        canonical_block = extract_managed_block(text, 'canonical-list')
        if canonical_block is None:
            continue
        domain_dir = path.parent
        for page in sorted(domain_dir.glob('*.md')):
            if page.name == 'index.md':
                continue
            stem_link = f'[[{page.stem}]]'
            if stem_link not in canonical_block:
                errors.append(f'missing canonical index entry {stem_link} in {rel}')
```

Finally, insert this call immediately before `check_evidence_cache_types(errors)`:

```python
validate_index_pages(errors)
```

- [ ] **Step 2: Run lint to verify the new index checks fail before the index pages are updated**

Run: `python3 scripts/lint_graph.py`
Expected: `FAIL` with errors including missing `ontology/entities/benchmarks/index.md` and missing managed blocks in the existing index pages.

- [ ] **Step 3: Add managed blocks to the root and entity index pages**

Replace `ontology/index.md` with exactly this content:

```markdown
# Ontology Index

> 本页是 ResearchKB 的唯一导航入口。先导航，再判定，再下钻。

## 1. 规范与判定入口
- 唯一规范页：[[graph-standard]]
- 所有节点、关系、字段、证据与豁免规则，一律以 [[graph-standard]] 为准。

## 2. 正式关系入口
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[paper_method_links]]
- [[benchmark_links]]
- [[provenance_links]]

## 3. 正式知识对象域入口
<!-- BEGIN MANAGED BLOCK:object-domain-navigation -->
- Papers：[[entities/papers/index|ontology/entities/papers/index.md]]
- Methods：[[entities/methods/index|ontology/entities/methods/index.md]]
- Concepts：[[entities/concepts/index|ontology/entities/concepts/index.md]]
- Tasks：[[entities/tasks/index|ontology/entities/tasks/index.md]]
- Scenarios：[[entities/scenarios/index|ontology/entities/scenarios/index.md]]
- Benchmarks：[[entities/benchmarks/index|ontology/entities/benchmarks/index.md]]
<!-- END MANAGED BLOCK:object-domain-navigation -->

## 4. 按任务进入
- 想做受约束知识问答 → 先进入对应 `ontology/entities/<对象域>/index.md` 锁定正式对象，再读取 serving-ready 对象页，并按 `Formal relations` 扩展；需要证据细节时再下钻对应 Evidence 页
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式对象知识 → 对应对象域 index → 对象页
- 想看治理用正式关系账本 → 对应 `ontology/relations/*.md`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `docs/`

## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → 本页 → 对应对象域 index → 代表对象页 → 必要时 Evidence / relation ledger

### 回答知识问题
对象域 index → serving-ready 对象页 → `Formal relations` → 邻接对象页 / Evidence 页 → 必要时 relation ledger

### 治理知识变更
[[graph-standard]] → relation ledger → 变更对象页 / Evidence 页 → 必要时对象域 index 回链

## 6. 说明
- 本页负责导航，不负责规范定义。
- 若导航与规范存在差异，以 [[graph-standard]] 为准。
```

Replace `ontology/entities/papers/index.md` with:

```markdown
# Papers Index

> 本页负责 Paper 对象域导航：先定位论文实例，再进入论文页；如需正式关系真源，再转到相关 relation ledger。

## 1. 对象域说明
- 本域收录正式 Paper 节点。
- 默认先从论文页读取核心问题、贡献、关系与证据入口，再按需要扩展到方法、概念、任务、场景与 benchmark。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
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
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/citation_graph|citation_graph]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/evidence_index|evidence_index]]
```

Replace `ontology/entities/methods/index.md` with:

```markdown
# Methods Index

> 本页负责 Method 对象域导航：先定位方法实例，再进入方法页；formal 演化边与任务/概念/benchmark 真源在相关 relation ledger。

## 1. 对象域说明
- 本域收录正式 Method 节点。
- 默认从方法页读取方法定义、演化位置、相关任务、相关概念与证据来源。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- [[PathMind]]
- [[RoG]]
- [[GCR]]
- [[ToG]]
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
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
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- [[EPERM]]
- [[GCR]]
- [[PathMind]]
- [[RoG]]
- [[ToG]]
- [[协同增强式知识图谱推理]]
- [[检索增强式知识图谱推理]]
- [[路径导向知识图谱推理]]
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/method_evolution|method_evolution]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/evidence_index|evidence_index]]
```

Replace `ontology/entities/concepts/index.md` with:

```markdown
# Concepts Index

> 本页负责 Concept 对象域导航：先定位概念实例，再进入概念页；formal 概念网络真源在 `concept_links`。

## 1. 对象域说明
- 本域收录正式 Concept 节点，包括一般概念与 framework 型概念。
- 默认从概念页读取概念定义、相关方法、相关论文、相关任务 / 场景与证据入口。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- [[路径优先化]]
- [[重要推理路径]]
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
### 路径推理核心概念
- [[路径优先化]]
- [[重要推理路径]]

### LLM-KG / framework 主线
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- [[LLM增强知识图谱]]
- [[复杂产品设计中的LLM-KG协同框架]]
- [[路径优先化]]
- [[重要推理路径]]
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/concept_links|concept_links]]
- [[../relations/paper_method_links|paper_method_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

Replace `ontology/entities/tasks/index.md` with:

```markdown
# Tasks Index

> 本页负责 Task 对象域导航：先定位任务实例，再进入任务页；formal 方法映射真源在 `task_method_map`。

## 1. 对象域说明
- 本域收录正式 Task 节点。
- 默认从任务页读取任务定义、核心挑战、相关方法、相关概念、相关 benchmark 与证据入口。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]
- [[engineering-design-knowledge-management]]
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
### KG 推理 / 问答任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]
- [[multi-hop-qa]]

### 设计知识管理任务
- [[engineering-design-knowledge-management]]
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- [[engineering-design-knowledge-management]]
- [[kgqa]]
- [[knowledge-graph-reasoning]]
- [[multi-hop-qa]]
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/task_method_map|task_method_map]]
- [[../relations/concept_links|concept_links]]
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/evidence_index|evidence_index]]
```

Replace `ontology/entities/scenarios/index.md` with:

```markdown
# Scenarios Index

> 本页负责 Scenario 对象域导航：先定位场景实例，再进入场景页；formal 场景相关边目前主要分散锚定在对象页与 `concept_links` / `task_method_map` 中。

## 1. 对象域说明
- 本域收录正式 Scenario 节点。
- 默认从场景页读取场景描述、核心挑战、主要方法 / 概念、相关任务与证据入口。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- [[知识图谱推理问答]]
- [[复杂产品设计]]
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
### 知识图谱推理场景
- [[知识图谱推理问答]]

### 复杂产品设计场景
- [[复杂产品设计]]
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- [[复杂产品设计]]
- [[知识图谱推理问答]]
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/concept_links|concept_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

Create `ontology/entities/benchmarks/index.md` with:

```markdown
# Benchmarks Index

> 本页负责 Benchmark 对象域导航：先定位 benchmark 实例，再进入 benchmark 页；formal benchmark 评测关系真源在 `benchmark_links`。

## 1. 对象域说明
- 本域收录正式 Benchmark 节点。
- 当 benchmark 正式页面补齐后，默认从 benchmark 页读取相关任务、相关方法与证据入口。

## 2. 核心入口
<!-- BEGIN MANAGED BLOCK:core-entry -->
- 无
<!-- END MANAGED BLOCK:core-entry -->

## 3. 按主题分组
<!-- BEGIN MANAGED BLOCK:grouped-navigation -->
- 无
<!-- END MANAGED BLOCK:grouped-navigation -->

## 4. 完整实例清单
<!-- BEGIN MANAGED BLOCK:canonical-list -->
- 无
<!-- END MANAGED BLOCK:canonical-list -->

## 5. 相关关系账本
- [[../relations/benchmark_links|benchmark_links]]
- [[../relations/task_method_map|task_method_map]]
- [[../relations/evidence_index|evidence_index]]
```

- [ ] **Step 4: Run lint to verify the managed-block and benchmarks-index checks pass**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit the index-surface changes**

Run:

```bash
git add ontology/index.md ontology/entities/papers/index.md ontology/entities/methods/index.md ontology/entities/concepts/index.md ontology/entities/tasks/index.md ontology/entities/scenarios/index.md ontology/entities/benchmarks/index.md scripts/lint_graph.py
git commit -m "docs: add managed index blocks"
```

Expected: a new commit containing only the managed-block index updates and the associated lint checks.

---

## Plan self-review

### Spec coverage
- **New pipeline stage** → Task 1 updates `CLAUDE.md`, `paper-ingest`, `page-projection-sync`, and creates `.claude/skills/index-sync/SKILL.md`.
- **Index governance split** → Task 2 updates `ontology/graph-standard.md` and `.claude/skills/serving-governance-review/SKILL.md`.
- **Managed-block strategy** → Task 3 wraps `ontology/index.md` and all entity index pages with explicit managed blocks.
- **Benchmarks index gap** → Task 3 creates `ontology/entities/benchmarks/index.md`.
- **Lint completeness checks** → Tasks 1–3 extend `scripts/lint_graph.py` in stages so each contract addition fails first, then passes.
- **Phase 1 only / Phase 2 deferred** → Task 1’s `index-sync` skill explicitly scopes immediate automation to `ontology/index.md` + entity index pages and reserves relation-ledger navigation blocks for Phase 2.

### Placeholder scan
- No `TODO`, `TBD`, or “similar to previous task” language remains.
- Every modified file path is concrete.
- Every command is concrete and has an expected pass/fail outcome.
- Every new code/doc block is included inline.

### Type / name consistency
- Stage names are consistent everywhere: `paper-ingest` → `relation-reconciliation` → `page-projection-sync` → `index-sync` → `python3 scripts/lint_graph.py` → `ontology-semantic-review` → `serving-governance-review`.
- Managed-block names are consistent everywhere: `object-domain-navigation`, `core-entry`, `grouped-navigation`, `canonical-list`.
- The lint helper and skill outputs consistently use `synced_indexes`, `skipped_pages`, and `manual_followups`.

---
