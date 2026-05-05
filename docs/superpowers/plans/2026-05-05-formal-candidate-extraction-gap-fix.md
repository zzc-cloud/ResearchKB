# Formal Candidate Extraction Gap Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce future missing formal relations by teaching `paper-ingest` and `relation-reconciliation` to upgrade strong semantic statements into candidate formal edges before those gaps leak into downstream audits.

**Architecture:** First tighten the candidate-upgrade rules in `paper-ingest` so strong semantic statements like method primary scenarios, paper core concepts, and paper core tasks are emitted into `relation_candidates`. Then extend `relation-reconciliation` so it re-audits those same strong semantic patterns from updated pages even if ingest missed them. Finally, verify on current migrated slices that the stricter upstream contract still passes lint and does not over-promote context-only links.

**Tech Stack:** Markdown skill definitions under `.claude/skills/`, existing relation ledgers and migrated pages under `wiki/`, Python 3 lint script (`scripts/lint_graph.py`).

---

## File map

### Skill definitions
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Add explicit candidate-upgrade rules for strong semantic statements.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Add strong-semantic re-audit rules and clarify `add_now` vs `needs_human_review` logic.

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: readback of current migrated pages as examples only (no page edits in this pass)

---

### Task 1: Extend `paper-ingest` with strong-semantic candidate promotion rules

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Insert a new subsection under `### Step 5.5: 汇总候选正式关系`**

In `.claude/skills/paper-ingest/SKILL.md`, after the existing three candidate classes, insert:

```markdown
### Step 5.5.1: 强语义表述的候选关系升级
除直接从论文正文抽取的 formal relation 外，还必须检查将要更新的对象页候选中是否出现以下“强语义表述”：
- 方法页中的“主要场景：[[Scenario]]”
- 论文页中的“核心概念：[[Concept]]”
- 论文页中的“核心任务 / 相关任务：[[Task]]”
- framework 型 Concept 页中的“场景：[[Scenario]]”或“面向：[[Scenario]]”

若同时满足以下条件：
1. 本体中存在合法 relation type
2. 当前 caches 中有足够证据支撑
3. 该关系不是纯背景/对比/延伸阅读

则必须把该关系升级写入 `relation_candidates`，而不是只停留在人类友好关系区块中。
```

- [ ] **Step 2: Add explicit semantic-pattern → relation-type mappings**

Immediately after the new subsection, insert:

```markdown
### Step 5.5.2: 强语义模式的默认映射
- 方法页“主要场景” → `applies_to`
- 论文页“核心概念” → `uses_concept`
- 论文页“核心任务 / 相关任务” → `targets_task`
- framework 型 Concept 页“场景 / 面向” → `applies_to`

若命中上述模式但仍存在明显歧义，不应静默忽略；应进入 `needs-human-review`。
```

- [ ] **Step 3: Add a negative rule for context-only links**

Append this block directly after the mapping section:

```markdown
### Step 5.5.3: 不自动升级的链接
以下链接默认仅视为 context-only，不应自动进入 `relation_candidates`：
- broad “相关方法 / 路线” 列表
- 对比对象
- 背景路线
- 延伸阅读
- benchmark 页中 task / scenario 的阅读辅助链接（除非本体后续新增正式 relation type）
```

- [ ] **Step 4: Run lint after updating `paper-ingest`**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 2: Extend `relation-reconciliation` with a strong-semantic re-audit layer

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a new subsection after `## Diff`**

Insert this block into `.claude/skills/relation-reconciliation/SKILL.md` after the existing Diff bullets:

```markdown
## 强语义表述复核
除显式 `relation_candidates` 外，还必须复核已更新对象页中的强语义表述，重点包括：
- 方法页中的“主要场景”
- 论文页中的“核心概念”
- 论文页中的“核心任务 / 相关任务”
- framework 型 Concept 页中的“场景 / 面向”

若这些表述满足：
1. ontology 存在合法 relation type
2. 当前 evidence 足以支撑
3. formal ledger 中缺失对应边

则必须继续判断是否应补为 formal relation，而不是因 ingest 未显式列出就跳过。
```

- [ ] **Step 2: Add explicit reconciliation behavior for missed candidates**

Immediately after that block, insert:

```markdown
### 复核后的判定规则
- 若 relation type 清晰、evidence 明确，则归入 `add_now`
- 若 relation type 合法但粒度或方向仍存在歧义，则归入 `needs_human_review`
- 不得因为该关系最初未出现在 `relation_candidates` 中就直接忽略
```

- [ ] **Step 3: Add a warning against over-promoting broad context links**

Append this block near the end of the file:

```markdown
## Context-only 护栏
即使某页人类区块中出现大量 `[[wikilink]]`，也不得机械全部升级。 broad “相关方法 / 路线”、对比对象、背景路线、延伸阅读仍默认按 context-only 处理，除非存在单独明确的 formal relation 语义与证据支撑。
```

- [ ] **Step 4: Run lint after updating `relation-reconciliation`**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 3: Verify the new upstream rules against known migrated examples

**Files:**
- Modify: none
- Test: manual verification against existing migrated pages + `python3 scripts/lint_graph.py`

- [ ] **Step 1: Check one method-page scenario example against the new rule**

Use this page as the concrete example:
- `wiki/methods/ToG.md`

Verify that the human-friendly statement:
- `主要场景：[[知识图谱推理问答]]`

would now be treated as a candidate `applies_to` trigger by the new `paper-ingest` / `relation-reconciliation` rules.

Expected: yes.

- [ ] **Step 2: Check one survey-paper concept/task example against the new rule**

Use this page as the concrete example:
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`

Verify that the human-friendly statements:
- `核心概念：[[LLM增强知识图谱]]`
- `相关任务：[[engineering-design-knowledge-management]]`

would now be treated as candidate triggers for `uses_concept` and `targets_task`.

Expected: yes.

- [ ] **Step 3: Check one context-only example against the new negative rule**

Use this page as the concrete example:
- `wiki/concepts/LLM增强知识图谱.md`

Verify that the block:
- `相关方法 / 路线：PathMind / RoG / GCR / ToG`

should remain context-only rather than being promoted into new formal relations.

Expected: yes.

- [ ] **Step 4: Run lint after the contract update verification**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 4: Final verification

**Files:**
- Modify: none
- Test: `git diff --`, `git status --short`

- [ ] **Step 1: Verify the final scope is limited to the two agreed skill files**

Run:

```bash
git diff -- \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/relation-reconciliation/SKILL.md
```

Expected: diff is limited to the candidate-upgrade and re-audit rule additions.

- [ ] **Step 2: Run the final lint check**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Do not auto-commit unless separately requested**

Run:

```bash
git status --short
```

Expected: working tree remains available for user review.
