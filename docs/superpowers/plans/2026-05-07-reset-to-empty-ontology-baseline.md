# Reset to Empty Ontology Baseline Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a skill that restores `ontology/` to the current strict empty baseline snapshot, matches the new navigation-index structure, and verifies the restored state with lint while blocking unsafe overwrites.

**Architecture:** Add a dedicated skill directory containing a checked-in `baseline/ontology/` snapshot plus a small Python restore script. The baseline snapshot will reflect the current `navigation-entries` / `non-serving-placeholders` index model and empty relation ledgers; the restore script will validate git state, replace the live `ontology/` tree with the snapshot, and run `python3 scripts/lint_graph.py` before reporting success.

---

## File structure

- Create: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
  - User-facing skill contract and restore workflow.
- Create: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
  - Restores `baseline/ontology/` over the live `ontology/` tree and runs lint.
- Create: `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/`
  - Checked-in strict empty ontology snapshot that matches current index block conventions.
  - Add regression tests for reset-baseline behavior and snapshot validity.

---

### Task 1: Add failing reset-baseline tests

**Files:**

- [ ] **Step 1: Write the failing existence tests**

```python
    def test_restore_baseline_script_exists(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        self.assertTrue(script_path.exists())

    def test_empty_baseline_snapshot_exists(self):
        baseline_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'baseline' / 'ontology'
        self.assertTrue(baseline_path.exists())
```

- [ ] **Step 2: Run the two tests to verify they fail**

Expected: FAIL because the skill directory, restore script, and baseline snapshot do not exist yet.

- [ ] **Step 3: Write the failing dirty-ontology guard test**

Add this test method:

```python
    def test_restore_baseline_script_blocks_dirty_ontology_without_force(self):
        ontology_marker = ROOT / 'ontology' / 'dirty-reset-baseline-marker.md'
        ontology_marker.write_text('temporary\n', encoding='utf-8')
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'),
                    '--check-only',
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            if ontology_marker.exists():
                ontology_marker.unlink()
        self.assertIn('blocked', result.stdout + result.stderr)
```

- [ ] **Step 4: Run the dirty-ontology guard test to verify it fails**

Expected: FAIL because the restore script does not exist yet.

- [ ] **Step 5: Commit**

```bash
git commit -m "test: add reset-baseline regression coverage"
```

### Task 2: Create the checked-in empty ontology baseline snapshot

**Files:**
- Create: `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/**`

- [ ] **Step 1: Create the baseline directory structure**

Create these directories exactly:

```text
.claude/skills/reset-to-empty-ontology-baseline/
.claude/skills/reset-to-empty-ontology-baseline/baseline/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/papers/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/methods/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/concepts/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/tasks/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/scenarios/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/benchmarks/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/evidence/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/raw-sources/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/raw-sources/files/
.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/relations/
```

- [ ] **Step 2: Populate the snapshot from the current strict-empty semantics**

Copy only baseline files from the live `ontology/` tree into the matching paths under `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/`:

```text
ontology/graph-standard.md
ontology/log.md
ontology/entities/papers/index.md
ontology/entities/methods/index.md
ontology/entities/concepts/index.md
ontology/entities/tasks/index.md
ontology/entities/scenarios/index.md
ontology/entities/benchmarks/index.md
ontology/entities/evidence/index.md
ontology/entities/raw-sources/index.md
ontology/relations/cites.md
ontology/relations/proposes.md
ontology/relations/based_on.md
ontology/relations/targets_task.md
ontology/relations/uses_concept.md
ontology/relations/evaluated_on.md
ontology/relations/supported_by.md
ontology/relations/sourced_from.md
```

Do not copy any instance pages under `papers/`, `methods/`, `concepts/`, `tasks/`, `scenarios/`, `benchmarks/`, or `evidence/`.

- [ ] **Step 3: Rewrite the baseline indexes to true empty-state content**

Ensure the baseline copies use the current block model and are empty where required:

- `entities/papers/index.md` must contain:
  - `<!-- BEGIN MANAGED BLOCK:navigation-entries -->` with no entries
  - `<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->` with no entries
- `entities/methods/index.md`, `concepts/index.md`, `tasks/index.md`, `scenarios/index.md`, `benchmarks/index.md`, `evidence/index.md` must do the same
- `entities/raw-sources/index.md` must retain the current raw PDF `navigation-entries` block and no placeholder block

- [ ] **Step 4: Run the two existence tests again**

Expected: the baseline snapshot test PASSES, the restore-script test still FAILS.

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: add empty ontology baseline snapshot"
```

### Task 3: Implement the baseline restore script

**Files:**
- Create: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`

- [ ] **Step 1: Run the dirty-ontology guard test again to confirm RED**

Expected: FAIL because the restore script still does not exist.

- [ ] **Step 2: Write the minimal restore script**

Create `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py` with this code:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASELINE = Path(__file__).resolve().parent / 'baseline' / 'ontology'
ONTOLOGY = ROOT / 'ontology'

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    return parser.parse_args()

def ontology_is_dirty() -> bool:
    result = subprocess.run(
        ['git', 'status', '--short', '--', 'ontology'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())

def run_lint() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

def main() -> int:
    args = parse_args()

    if not BASELINE.exists():
        print('failed: baseline snapshot missing')
        return 1

    if ontology_is_dirty() and not args.force:
        print('blocked: ontology has uncommitted changes; rerun with --force to overwrite')
        return 2

    if args.check_only:
        print('success: baseline snapshot available and overwrite preconditions satisfied')
        return 0

    if ONTOLOGY.exists():
        shutil.rmtree(ONTOLOGY)
    shutil.copytree(BASELINE, ONTOLOGY)

    lint = run_lint()
    sys.stdout.write(lint.stdout)
    sys.stderr.write(lint.stderr)
    if lint.returncode != 0:
        print('failed: restored baseline did not pass lint')
        return 1

    print('success: ontology restored to empty baseline')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
```

- [ ] **Step 3: Run the dirty-ontology guard test to verify GREEN**

Expected: PASS

- [ ] **Step 4: Run the restore-script existence test**

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: add reset-baseline restore script"
```

### Task 4: Add the end-to-end restore integration test

**Files:**

- [ ] **Step 1: Write the failing integration test**

Add this test method:

```python
    def test_restore_baseline_script_restores_ontology_and_passes_lint(self):
        restore_script = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        marker = ROOT / 'ontology' / 'log.md'
        original = marker.read_text(encoding='utf-8')
        marker.write_text(original + '\nTEMP-RESET-BASELINE-MARKER\n', encoding='utf-8')
        try:
            result = subprocess.run(
                [sys.executable, str(restore_script), '--force'],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            pass
        self.assertIn('success: ontology restored to empty baseline', result.stdout + result.stderr)
```
```

- [ ] **Step 2: Run the integration test to verify it fails**

Expected: FAIL until the baseline snapshot is fully aligned with current lint expectations.

- [ ] **Step 3: Complete the integration assertions**

Expand the test so it also asserts:

```python
        combined_output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, combined_output)
        self.assertIn('PASS: graph lint succeeded', combined_output)
        self.assertNotIn('TEMP-RESET-BASELINE-MARKER', marker.read_text(encoding='utf-8'))
```

- [ ] **Step 4: Run the integration test to verify it passes**

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git commit -m "test: verify reset-baseline restore end-to-end"
```

### Task 5: Add the skill contract and run final verification

**Files:**
- Create: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- Test: full test suite + lint + check-only restore

- [ ] **Step 1: Write the skill contract**

Create `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md` with this content:

```md
---
name: reset-to-empty-ontology-baseline
description: 恢复 ResearchKB 的 ontology 到严格空骨架基线，用于 cold-start ingest / relation / projection / governance 回归测试。Whenever 用户要求恢复空骨架、回到 baseline、清空 ontology 但保留骨架、或为单篇论文测试重置图谱时，都应使用此 skill。
---

# Reset to Empty Ontology Baseline

## Purpose
把 `ontology/` 恢复到 skill 自带的严格空骨架基线，然后立即运行 `python3 scripts/lint_graph.py` 验证恢复结果。

## Safety
- 默认先检查 `git status --short -- ontology`
- 若 `ontology/` 下存在未提交改动，则默认中止
- 只有用户明确允许覆盖时，才可带 `--force` 执行恢复

## Execution
1. 运行 `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
2. 如用户已确认覆盖当前 ontology，则附加 `--force`
3. 成功后回报 lint 结果

## Output
```yaml
status: success | blocked | failed
lint: pass | fail
warnings: []
```
```

- [ ] **Step 2: Run the restore script in check-only mode**

Run: `python3 .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py --check-only`
Expected: `success: baseline snapshot available and overwrite preconditions satisfied`

- [ ] **Step 3: Run the full lint test suite**

Expected: all tests PASS

- [ ] **Step 4: Run graph lint**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: add reset-baseline skill"
```

---

## Self-review

### Spec coverage
- Matches the current index model: `navigation-entries` and `non-serving-placeholders`.
- Preserves raw-source navigation while resetting all ontology instance pages.
- Adds git-safety gating, checked-in baseline snapshot, restore script, skill contract, and end-to-end verification.

### Placeholder scan
- No TODO / TBD placeholders remain.
- Each task contains explicit files, code, and commands.
- No task depends on old `core-entry / grouped-navigation / canonical-list` assumptions.

### Type consistency
- The skill root is consistently `.claude/skills/reset-to-empty-ontology-baseline/`.
- The baseline snapshot root is consistently `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/`.
- The restore script CLI is consistently `--force` / `--check-only`.
