# Ontology Navigation Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate ResearchKB navigation so `wiki/ontology/index.md` becomes the only navigation entry, `wiki/ontology/graph-standard.md` remains the only ontology standard, and `wiki/index.md` is removed cleanly.

**Architecture:** Keep ontology navigation and ontology rules as two separate documents with different responsibilities. Rewrite `wiki/ontology/index.md` into a task-oriented portal, update every operational entry point that still depends on `wiki/index.md`, then delete `wiki/index.md` and repair backlinks so the repo has a single navigation center.

**Tech Stack:** Markdown, Obsidian wikilinks, Claude Code skills, Python 3 lint script, git

---

## File map

### Existing files to modify
- Modify: `wiki/ontology/index.md`
- Modify: `CLAUDE.md`
- Modify: `wiki/log.md`
- Modify: `wiki/synthesis/researchkb-core-architecture.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `docs/superpowers/specs/2026-05-03-ontology-navigation-consolidation-design.md`

### Existing files to delete
- Delete: `wiki/index.md`

### Existing files to verify for stale references
- Verify references only: `docs/superpowers/specs/2026-05-02-remove-ontology-index-design.md`
- Verify references only: `docs/superpowers/specs/2026-05-02-relation-ledger-completion-design.md`
- Verify references only: `docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md`

### Existing files to reference and preserve as authority
- Reuse: `wiki/ontology/graph-standard.md`
- Reuse: `wiki/relations/citation_graph.md`
- Reuse: `wiki/relations/method_evolution.md`
- Reuse: `wiki/relations/concept_links.md`
- Reuse: `wiki/relations/task_method_map.md`
- Reuse: `wiki/relations/evidence_index.md`
- Reuse: `wiki/relations/paper_method_links.md`
- Reuse: `wiki/relations/benchmark_links.md`
- Reuse: `wiki/relations/provenance_links.md`
- Reuse: `wiki/synthesis/researchkb-core-architecture.md`
- Reuse: `scripts/lint_graph.py`

---

### Task 1: Rewrite `wiki/ontology/index.md` into the only navigation portal

**Files:**
- Modify: `wiki/ontology/index.md`
- Test: `wiki/ontology/index.md`

- [ ] **Step 1: Write the failing structure check**

Run:

```bash
grep -n "按任务进入\|推荐阅读路径\|唯一导航入口" wiki/ontology/index.md
```

Expected before implementation: no matches, because the current ontology index is still a thin list rather than the final portal structure.

- [ ] **Step 2: Replace `wiki/ontology/index.md` with the new portal content**

Write this exact content:

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

## 3. 正式知识对象入口
- Papers：`wiki/papers/`
- Methods：`wiki/methods/`
- Concepts：`wiki/concepts/`
- Tasks：`wiki/tasks/`
- Scenarios：`wiki/scenarios/`
- Benchmarks：`wiki/benchmarks/`
- Synthesis：`wiki/synthesis/`

## 4. 按任务进入
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式知识结论 → 对应 `wiki/` 对象页
- 想看正式关系账本 → `wiki/relations/`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `wiki/synthesis/`

## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → `wiki/relations/` → 具体对象页 → `intermediate/papers/`

### 回答知识问题
对象页 / 关系账本 → `intermediate/papers/` → 必要时 `raw/`

### 治理知识变更
[[graph-standard]] → `wiki/relations/` → 变更对象页 → `intermediate/papers/`

## 6. 说明
- 本页负责导航，不负责规范定义。
- 若导航与规范存在差异，以 [[graph-standard]] 为准。
```

- [ ] **Step 3: Run the portal structure check to verify GREEN**

Run:

```bash
grep -n "按任务进入\|推荐阅读路径\|唯一导航入口" wiki/ontology/index.md
```

Expected: matching lines for all three headings/phrases.

- [ ] **Step 4: Commit**

```bash
git add wiki/ontology/index.md
git commit -m "docs: rewrite ontology index as navigation portal"
```

---

### Task 2: Repoint CLAUDE and core docs from `wiki/index.md` to `wiki/ontology/index.md`

**Files:**
- Modify: `CLAUDE.md`
- Modify: `wiki/log.md`
- Modify: `wiki/synthesis/researchkb-core-architecture.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `CLAUDE.md`

- [ ] **Step 1: Write the failing old-entry check**

Run:

```bash
grep -n "wiki/index.md\|\[\[index\]\]" CLAUDE.md wiki/log.md wiki/synthesis/researchkb-core-architecture.md .claude/skills/paper-ingest/SKILL.md
```

Expected before implementation: matches still exist.

- [ ] **Step 2: Update the navigation entry references in `CLAUDE.md`**

Make these exact substitutions:

1. In the “需要哪些信息层” list, replace:

```markdown
- `wiki/index.md` 定位
```

with:

```markdown
- `wiki/ontology/index.md` 定位导航入口
```

2. In “本体初步探查”, replace:

```markdown
- `wiki/index.md`
```

with:

```markdown
- `wiki/ontology/index.md`
```

3. In “查询与分析默认顺序”, replace:

```markdown
1. 读取 `wiki/index.md` 定位
```

with:

```markdown
1. 读取 `wiki/ontology/index.md` 定位导航入口
```

- [ ] **Step 3: Repair backlinks in `wiki/log.md` and `wiki/synthesis/researchkb-core-architecture.md`**

Make these exact changes:

1. In `wiki/log.md`, replace:

```markdown
- 关联索引：[[index]]
```

with:

```markdown
- 导航入口：[[ontology/index|ontology-index]]
```

2. In `wiki/synthesis/researchkb-core-architecture.md`, replace:

```markdown
- [[index]]
```

with:

```markdown
- [[ontology/index|ontology-index]]
```

- [ ] **Step 4: Update `paper-ingest` skill guidance**

In `.claude/skills/paper-ingest/SKILL.md`, inside the list of pages to update, replace:

```markdown
   - `wiki/index.md`
```

with:

```markdown
   - `wiki/ontology/index.md`
```

- [ ] **Step 5: Verify GREEN**

Run:

```bash
grep -n "wiki/index.md\|\[\[index\]\]" CLAUDE.md wiki/log.md wiki/synthesis/researchkb-core-architecture.md .claude/skills/paper-ingest/SKILL.md
```

Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md wiki/log.md wiki/synthesis/researchkb-core-architecture.md .claude/skills/paper-ingest/SKILL.md
git commit -m "docs: repoint navigation to ontology index"
```

---

### Task 3: Delete `wiki/index.md` and record the direct-removal decision

**Files:**
- Delete: `wiki/index.md`
- Modify: `docs/superpowers/specs/2026-05-03-ontology-navigation-consolidation-design.md`
- Test: `wiki/index.md`

- [ ] **Step 1: Write the failing existence check**

Run:

```bash
ls wiki/index.md
```

Expected before deletion: file exists.

- [ ] **Step 2: Delete `wiki/index.md`**

Run:

```bash
rm wiki/index.md
```

Expected: command succeeds with no output.

- [ ] **Step 3: Add one implementation note to the design doc**

Append this section to `docs/superpowers/specs/2026-05-03-ontology-navigation-consolidation-design.md`:

```markdown
## 9. 实施说明
- 本次实现直接删除 `wiki/index.md`，不保留过渡跳转页。
- 所有默认入口统一改为 `wiki/ontology/index.md`。
- `wiki/ontology/graph-standard.md` 保持为唯一规范页，不承担导航首页职责。
```

- [ ] **Step 4: Verify GREEN**

Run:

```bash
ls wiki/index.md
```

Expected: shell failure with `No such file or directory`.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-05-03-ontology-navigation-consolidation-design.md
git add -u wiki/index.md
git commit -m "docs: remove legacy wiki index entrypoint"
```

---

### Task 4: Verify that operational navigation still works after consolidation

**Files:**
- Verify only: `wiki/ontology/index.md`
- Verify only: `CLAUDE.md`
- Verify only: `wiki/ontology/graph-standard.md`
- Verify only: `wiki/log.md`
- Verify only: `wiki/synthesis/researchkb-core-architecture.md`
- Verify only: `.claude/skills/paper-ingest/SKILL.md`
- Verify only: `scripts/lint_graph.py`

- [ ] **Step 1: Verify no stale runtime references remain in operational files**

Run:

```bash
grep -R -n "wiki/index.md\|\[\[index\]\]" CLAUDE.md wiki .claude/skills/paper-ingest 2>/dev/null
```

Expected: no output.

- [ ] **Step 2: Run graph lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:

```text
PASS: graph lint succeeded
```

- [ ] **Step 3: Verify the ontology portal points to the standard and ledgers**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('wiki/ontology/index.md').read_text(encoding='utf-8')
needles = [
    '[[graph-standard]]',
    '[[citation_graph]]',
    '[[method_evolution]]',
    '[[concept_links]]',
    '[[task_method_map]]',
    '[[evidence_index]]',
    '[[paper_method_links]]',
    '[[benchmark_links]]',
    '[[provenance_links]]',
]
for needle in needles:
    assert needle in text, f'missing {needle}'
print('PASS: ontology portal links to standard and ledgers')
PY
```

Expected: `PASS: ontology portal links to standard and ledgers`.

- [ ] **Step 4: Commit verification-safe cleanup if needed**

If no files changed during verification, skip commit for this step. If you had to make any small verification-driven fixes, commit them with:

```bash
git add <fixed-files>
git commit -m "docs: finalize ontology navigation consolidation"
```

---

## Self-review

### Spec coverage
- Unique navigation entrypoint: covered by Task 1.
- Keep `graph-standard.md` as unique rules page: preserved by Task 1 and verified in Task 4.
- Delete `wiki/index.md` directly: covered by Task 3.
- Update all default entry references in `CLAUDE.md`: covered by Task 2.
- Repair direct backlinks that still point to `[[index]]`: covered by Task 2 and Task 4.
- Keep scope limited to navigation and entrypoint consolidation: preserved across all tasks.

### Placeholder scan
- No `TODO`, `TBD`, or deferred implementation placeholders remain.
- Every edit step names exact files and exact replacement content.
- Every verification step includes exact commands and expected output.
- Commits stage exact files.

### Type consistency
- `wiki/ontology/index.md` is consistently treated as the only navigation page.
- `wiki/ontology/graph-standard.md` is consistently treated as the only rules page.
- `wiki/index.md` is consistently treated as deleted, not redirected.
- `[[ontology/index|ontology-index]]` is used consistently as the replacement backlink label where a wiki link is still needed.
