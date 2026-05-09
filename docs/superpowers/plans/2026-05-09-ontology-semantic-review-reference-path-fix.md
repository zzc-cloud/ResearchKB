# Ontology Semantic Review Reference Path Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `ontology-semantic-review` so it reads its reference documents from `.claude/skills/ontology-semantic-review/references/...` instead of nonexistent root-level `references/...`, then verify the skill no longer breaks on those reads.

**Architecture:** Keep the fix strictly local to the skill contract in `.claude/skills/ontology-semantic-review/SKILL.md`. Correct the three reference paths in the “先阅读” block and the two downstream output-format mentions, then verify by searching for stale root paths and checking that all referenced local files exist.

**Tech Stack:** Markdown skill docs, ripgrep, Bash, git

---

## File Structure

- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Owns the contract for the ontology semantic review skill, including required reading inputs and output-format instructions.
- Verify against existing files:
  - `.claude/skills/ontology-semantic-review/references/review-output-template.md`
  - `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
  - `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

No new files. No changes to ontology pages, lint scripts, or other skills.

### Task 1: Correct the skill’s reference paths

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md:14-26`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md:51-57`

- [ ] **Step 1: Confirm the current broken root-path references exist in the skill doc**

Run:

```bash
rg -n 'references/(review-output-template|review-scope-rules|diff-review-playbook)\.md' \
  ".claude/skills/ontology-semantic-review/SKILL.md"
```

Expected: 5 matches — 3 in the “先阅读” list and 2 in the output/verdict instructions.

- [ ] **Step 2: Update the “先阅读” block to point at the real local files**

Replace the old block entries with this exact content:

```markdown
## 先阅读
- `ontology/graph-standard.md`
- `ontology/relations/cites.md`
- `ontology/relations/proposes.md`
- `ontology/relations/based_on.md`
- `ontology/relations/targets_task.md`
- `ontology/relations/uses_concept.md`
- `ontology/relations/evaluated_on.md`
- `ontology/relations/supported_by.md`
- `ontology/relations/sourced_from.md`
- `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
```

- [ ] **Step 3: Update the output-format instructions to use the same local path**

Replace the old wording with this exact content:

```markdown
## 判断原则
- 优先给出能恢复本体一致性的最小修正方案。
- 区分“论文支撑关系”和“本体层概念关系”。
- 必须使用 `.claude/skills/ontology-semantic-review/references/review-output-template.md` 中的报告格式与 verdict 语义，不要临时发明自己的 verdict 规则。

## 输出
不要直接改写本体。必须使用 `.claude/skills/ontology-semantic-review/references/review-output-template.md` 的固定结构输出一份语义审查报告。
```

- [ ] **Step 4: Re-run the search to confirm the stale root-level paths are gone**

Run:

```bash
rg -n 'references/(review-output-template|review-scope-rules|diff-review-playbook)\.md' \
  ".claude/skills/ontology-semantic-review/SKILL.md"
```

Expected: 0 matches.

- [ ] **Step 5: Commit the doc-only fix**

Run:

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md
git commit -m "fix: point ontology semantic review to local references"
```

Expected: 1 file changed in the commit.

### Task 2: Verify the skill contract is now executable

**Files:**
- Verify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Verify: `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- Verify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Verify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

- [ ] **Step 1: Verify all three local reference files exist on disk**

Run:

```bash
test -f ".claude/skills/ontology-semantic-review/references/review-output-template.md" && \
test -f ".claude/skills/ontology-semantic-review/references/review-scope-rules.md" && \
test -f ".claude/skills/ontology-semantic-review/references/diff-review-playbook.md"
```

Expected: exit code 0 and no output.

- [ ] **Step 2: Verify the skill doc now points at the local files explicitly**

Run:

```bash
rg -n '\.claude/skills/ontology-semantic-review/references/' \
  ".claude/skills/ontology-semantic-review/SKILL.md"
```

Expected: 5 matches — the 3 “先阅读” entries and the 2 output/verdict references.

- [ ] **Step 3: Verify the exact local paths referenced in the skill all exist**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re
skill = Path('.claude/skills/ontology-semantic-review/SKILL.md').read_text(encoding='utf-8')
paths = re.findall(r'`(\.claude/skills/ontology-semantic-review/references/[^`]+)`', skill)
missing = [p for p in paths if not Path(p).exists()]
print({'paths': paths, 'missing': missing})
assert len(paths) == 5, f'expected 5 local path mentions, got {len(paths)}'
assert not missing, f'missing referenced files: {missing}'
PY
```

Expected:

```python
{'paths': ['.claude/skills/ontology-semantic-review/references/review-output-template.md', '.claude/skills/ontology-semantic-review/references/review-scope-rules.md', '.claude/skills/ontology-semantic-review/references/diff-review-playbook.md', '.claude/skills/ontology-semantic-review/references/review-output-template.md', '.claude/skills/ontology-semantic-review/references/review-output-template.md'], 'missing': []}
```

- [ ] **Step 4: Re-run the ontology semantic review handoff from the paper pipeline**

Run the skill on the current PathMind ingest context using the normal pipeline entrypoint that previously failed.

Expected: it proceeds past the reference-reading phase without “file does not exist” errors for:
- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`

- [ ] **Step 5: Commit the verification result if Task 2 required any follow-up edit**

If Task 2 required no edits, skip this step.

If Task 2 required a tiny follow-up edit, run:

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md
git commit -m "fix: align ontology semantic review path references"
```

Expected: either no commit because verification passed cleanly, or a small single-file follow-up commit.

## Spec Coverage Check

- Fix wrong root-level `references/...` paths in `ontology-semantic-review`: covered by Task 1 Steps 2-3.
- Keep scope tightly limited to the approved spec: enforced by File Structure and task scope.
- Verify no stale root-level references remain: covered by Task 1 Step 4.
- Verify the skill no longer breaks on those reads: covered by Task 2 Steps 1-4.

## Placeholder Scan

- No `TODO` / `TBD` placeholders remain.
- All file paths are explicit.
- All verification commands are concrete.

## Type / Name Consistency Check

- The only modified file is `.claude/skills/ontology-semantic-review/SKILL.md` throughout the plan.
- All reference paths use the same `.claude/skills/ontology-semantic-review/references/...` prefix.
- Verification expects exactly 5 local path mentions because the approved design changes 3 input references and 2 output-format references.
