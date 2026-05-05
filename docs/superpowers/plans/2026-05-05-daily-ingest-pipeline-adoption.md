# Daily Ingest Pipeline Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the six-stage compile/governance chain the default interpretation of daily single-paper ingest, using only the six control-surface files that define workflow, skill handoff, normative expectations, and lint contract checks.

**Architecture:** Update the human-facing workflow source of truth (`CLAUDE.md`) so `paper-ingest` is no longer treated as the whole operation. Then update the three skill docs so each stage explicitly hands off to the next. Add a short normative compile-chain section to `wiki/ontology/graph-standard.md`, and add minimal contract checks in `scripts/lint_graph.py` so future regressions are caught. This is a workflow-adoption change, not a content migration.

**Tech Stack:** Markdown workflow/spec files, three skill docs under `.claude/skills/`, Python 3 lint script (`scripts/lint_graph.py`).

---

## File map

### Workflow / instructions
- Modify: `CLAUDE.md`
  - Make the six-stage chain the default meaning of “处理论文” and “批量处理论文”.

### Skill docs
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Make `paper-ingest` explicitly end at handoff to `relation-reconciliation`.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Make it explicitly the required next stage after ingest and hand off `affected_pages` to `page-projection-sync`.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Make it explicitly the third stage and direct the workflow into the three governance gates.

### Normative process source
- Modify: `wiki/ontology/graph-standard.md`
  - Add a short single-paper compile-chain section to the standard.

### Lint contract protection
- Modify: `scripts/lint_graph.py`
  - Add or adjust contract checks for the three-skill chain markers.

### Verification surface
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Update `CLAUDE.md` so “处理论文” means the full six-stage chain

**Files:**
- Modify: `CLAUDE.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the single-paper workflow bullets**

In `CLAUDE.md`, replace the current `### 处理单篇论文` block:

```markdown
### 处理单篇论文
当我说 **“处理论文：[文件路径或论文标题]”** 时：
- 默认使用 `paper-ingest` skill
- `CLAUDE.md` 负责认知方式与约束，不重复维护具体摄入步骤
- 如与 `wiki/ontology/graph-standard.md` 冲突，以后者为准
```

with:

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
- 如与 `wiki/ontology/graph-standard.md` 冲突，以后者为准
```

- [ ] **Step 2: Replace the batch-paper workflow bullets**

Replace the current `### 批量处理论文` block:

```markdown
### 批量处理论文
当我说 **“批量处理 raw/ 目录下的所有论文”** 时：
- 仍以 `paper-ingest` 作为单篇摄入执行器
- 先列出候选论文并按主题 / 年份分组，与我确认顺序
- 逐篇汇报进度，避免无确认的大规模落库
```

with:

```markdown
### 批量处理论文
当我说 **“批量处理 raw/ 目录下的所有论文”** 时：
- 仍以单篇论文编译链为基本执行单元：`paper-ingest` → `relation-reconciliation` → `page-projection-sync` → 三层治理
- 先列出候选论文并按主题 / 年份分组，与我确认顺序
- 逐篇汇报进度，避免无确认的大规模落库
- 不允许只批量跑 `paper-ingest` 而跳过后续 relation / projection / 治理阶段
```

- [ ] **Step 3: Add explicit stop conditions for the daily chain**

Insert this new section directly after `### 批量处理论文`:

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

- [ ] **Step 4: Run lint to verify `CLAUDE.md` still satisfies repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 2: Update `paper-ingest` so it is explicitly an entrypoint, not the whole workflow

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a one-line explicit handoff note to the architecture block**

In `.claude/skills/paper-ingest/SKILL.md`, append this sentence to the architecture block after the existing last sentence:

```markdown
在日常处理论文流程中，本 skill 默认只负责编译入口；完成后必须显式进入 `relation-reconciliation`，而不是把 ingest 结果直接当作正式入图结果。
```

- [ ] **Step 2: Strengthen the end-of-skill handoff language**

In the `## Ingest 完成后的后续治理要求` section, replace:

```markdown
1. 必须先交给 `relation-reconciliation` 补齐 formal relation ledger
2. relation ledger 更新后，必须交给 `page-projection-sync` 回写对象页投影
3. 然后运行 `python3 scripts/lint_graph.py`
4. lint 通过后，必须调用 `ontology-semantic-review` skill 审查语义合理性
5. 如本次改动涉及 serving-ready 页面，还必须调用 `serving-governance-review`
6. 只有结构、语义与 serving 都合理时，才建议接受本次变更并进入 git 提交
```

with:

```markdown
1. 在日常 ingest 流程中，`paper-ingest` 结束后默认进入 `relation-reconciliation`
2. `relation-reconciliation` 完成后，必须进入 `page-projection-sync`
3. `page-projection-sync` 完成后，必须运行 `python3 scripts/lint_graph.py`
4. lint 通过后，必须调用 `ontology-semantic-review` skill 审查语义合理性
5. 如本次改动涉及 serving-ready 页面，还必须调用 `serving-governance-review`
6. 只有结构、语义与 serving 都合理时，才建议接受本次变更并进入 git 提交
```

- [ ] **Step 3: Run lint after the `paper-ingest` wording update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 3: Update `relation-reconciliation` to be the required next stage after ingest

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add an explicit stage-position section near the top**

Insert this block after the first paragraph of the skill body:

```markdown
## 链路位置
本 skill 是单篇论文日常编译链的第二阶段，默认前置为 `paper-ingest`。
本 skill 不应独立替代 ingest，也不应跳过后续 `page-projection-sync`。
```

- [ ] **Step 2: Strengthen the downstream handoff requirement**

Append this block near the end of the file:

```markdown
## 完成后的默认后继阶段
当本 skill 完成 formal relation ledger 的补齐与对齐后：
- 必须把 `affected_pages` 交给 `page-projection-sync`
- 不应停留在“ledger 已更新但对象页尚未同步”的状态
- 对象页同步完成后，才进入 lint 与后续治理
```

- [ ] **Step 3: Run lint after the `relation-reconciliation` wording update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 4: Update `page-projection-sync` to be the required third stage before governance

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add an explicit stage-position section near the top**

Insert this block after the opening paragraph:

```markdown
## 链路位置
本 skill 是单篇论文日常编译链的第三阶段，默认前置为 `relation-reconciliation`。
本 skill 完成后不视为流程结束，而应继续进入三层治理出口。
```

- [ ] **Step 2: Add an explicit governance handoff section**

Append this block near the end of the skill:

```markdown
## 完成后的默认后继阶段
当本 skill 完成对象页投影同步后，默认进入以下三层治理：
1. `python3 scripts/lint_graph.py`
2. `ontology-semantic-review`
3. `serving-governance-review`

若其中任一阶段失败，则本次论文处理流程不得视为正式入图完成。
```

- [ ] **Step 3: Run lint after the `page-projection-sync` wording update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 5: Add a normative single-paper compile-chain section to `graph-standard.md`

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Insert a compact compile-chain section before `## 三层治理出口`**

Insert this block into `wiki/ontology/graph-standard.md` immediately before `## 三层治理出口`:

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
```

- [ ] **Step 2: Run lint after the standard update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 6: Strengthen lint so pipeline-contract regressions are caught

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a small daily-ingest contract needle set**

After the existing `PAPER_INGEST_NEEDLES`, add:

```python
DAILY_INGEST_CHAIN_NEEDLES = [
    'relation-reconciliation',
    'page-projection-sync',
    'ontology-semantic-review',
    'serving-governance-review',
]
```

- [ ] **Step 2: Validate the new default-chain language in `CLAUDE.md` and both downstream skills**

Insert this block before the final `if errors:` section:

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

- [ ] **Step 3: Run lint after the contract-check update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 7: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the final full lint check**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Verify scope is limited to the six agreed control-surface files**

Run:

```bash
git diff -- \
  CLAUDE.md \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/page-projection-sync/SKILL.md \
  wiki/ontology/graph-standard.md \
  scripts/lint_graph.py
```

Expected: the diff is limited to the six control-surface files.

- [ ] **Step 3: Do not auto-commit unless separately requested**

Run:

```bash
git status --short
```

Expected: the working tree remains available for user review.
