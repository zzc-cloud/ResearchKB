# CLAUDE.md Git History Hard-Block Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a ResearchKB-wide hard rule to `CLAUDE.md` that forbids using git history and deleted ontology objects as default content references.

**Architecture:** This is a single-file policy change in `CLAUDE.md`. The implementation inserts one new execution principle and one new avoidable-error bullet so the rule is visible both as a positive operating constraint and as a failure mode to avoid.

**Tech Stack:** Markdown, project instruction file (`CLAUDE.md`)

---

### Task 1: Add the project-wide rule to CLAUDE.md

**Files:**
- Modify: `CLAUDE.md:177-189`
- Test: manual diff review in `CLAUDE.md`

- [ ] **Step 1: Read the target section before editing**

Read the `## 执行原则` and `## 你应避免的常见错误` section in `CLAUDE.md` so the new rule matches the surrounding wording and numbering.

Run:
```bash
python3 - <<'PY'
from pathlib import Path
p = Path('CLAUDE.md')
for i, line in enumerate(p.read_text().splitlines(), start=1):
    if 177 <= i <= 189:
        print(f"{i}: {line}")
PY
```

Expected: output showing principles 1-4 and the two existing error bullets.

- [ ] **Step 2: Insert the new execution principle**

Update the numbered list under `## 执行原则` to add a new rule after current principle 4:

```md
5. **当前工作区优先于仓库历史**：在 ResearchKB 中，默认只以当前工作区与当前规范文件作为内容真源，不得把 git 历史、已删除对象、旧提交内容或旧分支内容当作建模、写作、修复或摄入参考；如确需查看历史，必须先获得用户对当次任务、当次用途的明确授权，且该授权不自动延续到后续任务。
```

This wording must preserve the hard-block scope, the default allowed truth sources, and the single-task authorization rule from the approved spec.

- [ ] **Step 3: Add a matching avoidable-error bullet**

Append one new bullet under `## 你应避免的常见错误`:

```md
- 把 git 历史、已删除对象或旧版本页面当作当前任务的默认参考，而不是先以当前工作区与现行规范重新判断
```

This keeps the rule visible in both the “do” and “avoid” sections.

- [ ] **Step 4: Review the edited text in place**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
p = Path('CLAUDE.md')
for i, line in enumerate(p.read_text().splitlines(), start=1):
    if 177 <= i <= 191:
        print(f"{i}: {line}")
PY
```

Expected: principle 5 appears under `## 执行原则`, and the new git-history error bullet appears under `## 你应避免的常见错误`.

- [ ] **Step 5: Verify the exact diff**

Run:
```bash
git diff -- CLAUDE.md
```

Expected: the diff shows only the newly added principle and the newly added error bullet in `CLAUDE.md`.

- [ ] **Step 6: Commit the change**

```bash
git add CLAUDE.md
git commit -m "docs: forbid git history as default ResearchKB reference"
```

This commit should contain only the `CLAUDE.md` policy update if no unrelated files are staged.

---

## Self-Review

- Spec coverage: the plan adds the project-wide rule, forbids deleted-object reuse, restricts history access to explicit single-task authorization, and writes the rule only in `CLAUDE.md`.
- Placeholder scan: no TBD/TODO markers remain.
- Type consistency: the exact wording target and file path stay consistent across all steps.
