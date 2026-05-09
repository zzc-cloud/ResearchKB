# Reset-to-Empty Ontology Baseline Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old snapshot-copy reset skill with a live-derived reset flow that preserves current live index/raw-source structure, deletes object instance pages, clears relation ledgers to the current empty-ledger form, rewrites `ontology/log.md` to an empty baseline, and verifies the result with lint.

**Tech Stack:** Python 3 standard library (`argparse`, `os`, `pathlib`, `subprocess`, `sys`, `tempfile`, `importlib.util`), git CLI, unittest, Obsidian Markdown files under `ontology/`, ResearchKB lint (`scripts/lint_graph.py`).

---

## File map

- Modify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
  - Replace baseline-copy logic with live-derived reset helpers and a test-only root override.
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
  - Rewrite the skill contract so it describes live-derived reset semantics instead of copying from `baseline/ontology/`.
  - Remove outdated baseline-snapshot assumptions and add behavior tests for relation clearing, entity cleanup, log reset, dirty-worktree blocking, and force-reset integration.

---

### Task 1: Replace outdated reset-baseline tests with live-derived failing tests

**Files:**

- [ ] **Step 1: Add helper imports and loader utilities for the reset script**

```python
import importlib.util
import os
import tempfile
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load_reset_baseline_module():
    script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
    spec = importlib.util.spec_from_file_location('reset_to_empty_ontology_baseline', script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
```

- [ ] **Step 2: Replace the old snapshot-centric reset tests with new RED behavior tests**

Delete these outdated tests if they still exist:
- `test_empty_baseline_snapshot_exists`
- `test_restore_baseline_script_requires_baseline_consistency_check`
- any assertion that still expects `baseline snapshot is out of date`

Then add these new tests inside `LintGraphTests`:

```python
    def test_clear_relation_ledger_text_keeps_semantics_and_empties_instances(self):
        module = load_reset_baseline_module()
        original = (
            "## 关系语义说明\n"
            "- `based_on` 表示某方法以另一方法作为上游基础。\n\n"
            "## 实例边\n"
            "- [[Child]] --based_on--> [[Parent]]\n"
            "  - source_path: ontology/entities/methods/Child.md\n"
            "  - target_path: ontology/entities/methods/Parent.md\n"
            "  - edge_semantics: fixture\n"
            "  - evidence: Fixture.sections\n"
            "  - evidence_link: [[Fixture.sections]]\n"
            "  - evidence_path: ontology/entities/evidence/Fixture.sections.md\n"
        )

        updated = module.clear_relation_ledger_text(original)

        self.assertIn('## 关系语义说明', updated)
        self.assertIn('`based_on` 表示某方法以另一方法作为上游基础。', updated)
        self.assertIn('## 实例边\n- 无\n', updated)
        self.assertNotIn('[[Child]] --based_on--> [[Parent]]', updated)

    def test_clear_relation_ledger_text_requires_instance_heading(self):
        module = load_reset_baseline_module()
        with self.assertRaisesRegex(ValueError, 'missing ## 实例边 heading'):
            module.clear_relation_ledger_text('## 关系语义说明\n- only semantics\n')

    def test_remove_entity_instance_pages_preserves_indexes_and_raw_pdfs(self):
        module = load_reset_baseline_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            entities = root / 'ontology' / 'entities'
            write_file(entities / 'papers' / 'index.md', '# Papers Index\n')
            write_file(entities / 'papers' / 'Fixture Paper.md', '# Fixture Paper\n')
            write_file(entities / 'methods' / 'index.md', '# Methods Index\n')
            write_file(entities / 'methods' / 'Fixture Method.md', '# Fixture Method\n')
            write_file(entities / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            raw_pdf = entities / 'raw-sources' / 'files' / 'fixture.pdf'
            raw_pdf.parent.mkdir(parents=True, exist_ok=True)
            raw_pdf.write_bytes(b'%PDF-1.4 fixture')

            module.clear_entity_instance_pages(entities)

            self.assertTrue((entities / 'papers' / 'index.md').exists())
            self.assertFalse((entities / 'papers' / 'Fixture Paper.md').exists())
            self.assertTrue((entities / 'methods' / 'index.md').exists())
            self.assertFalse((entities / 'methods' / 'Fixture Method.md').exists())
            self.assertTrue((entities / 'raw-sources' / 'index.md').exists())
            self.assertTrue(raw_pdf.exists())

    def test_write_empty_log_rewrites_history(self):
        module = load_reset_baseline_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / 'ontology' / 'log.md'
            write_file(log_path, '# 操作日志\n\n## 2026-05-08 ingest | fixture\n')

            module.write_empty_log(log_path)

            self.assertEqual(
                log_path.read_text(encoding='utf-8'),
                '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n',
            )

    def test_restore_script_blocks_dirty_ontology_without_force_in_temp_repo(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subprocess.run(['git', 'init'], cwd=root, capture_output=True, text=True, check=True)
            write_file(root / 'ontology' / 'graph-standard.md', '# graph standard\n')
            write_file(root / 'ontology' / 'log.md', '# 操作日志\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'index.md', '# Papers Index\n')
            write_file(root / 'ontology' / 'entities' / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            write_file(root / 'ontology' / 'relations' / 'based_on.md', '## 关系语义说明\n- fixture\n\n## 实例边\n- 无\n')
            write_file(
                root / 'scripts' / 'lint_graph.py',
                'print("PASS: graph lint succeeded")\n',
            )
            write_file(root / 'ontology' / 'dirty-marker.md', 'dirty\n')

            env = os.environ | {'RESEARCHKB_RESET_ROOT': str(root)}
            result = subprocess.run(
                [sys.executable, str(script_path), '--check-only'],
                cwd=root,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertIn('blocked: ontology has uncommitted changes', result.stdout + result.stderr)

    def test_restore_script_force_resets_temp_repo_and_runs_lint(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subprocess.run(['git', 'init'], cwd=root, capture_output=True, text=True, check=True)
            write_file(root / 'ontology' / 'graph-standard.md', '# graph standard\n')
            write_file(root / 'ontology' / 'log.md', '# 操作日志\n\n## 2026-05-08 ingest | fixture\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'index.md', '# Papers Index\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'Fixture Paper.md', '# Fixture Paper\n')
            write_file(root / 'ontology' / 'entities' / 'methods' / 'index.md', '# Methods Index\n')
            write_file(root / 'ontology' / 'entities' / 'methods' / 'Fixture Method.md', '# Fixture Method\n')
            write_file(root / 'ontology' / 'entities' / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            raw_pdf = root / 'ontology' / 'entities' / 'raw-sources' / 'files' / 'fixture.pdf'
            raw_pdf.parent.mkdir(parents=True, exist_ok=True)
            raw_pdf.write_bytes(b'%PDF-1.4 fixture')
            write_file(
                root / 'ontology' / 'relations' / 'based_on.md',
                '## 关系语义说明\n- fixture\n\n## 实例边\n- [[Child]] --based_on--> [[Parent]]\n',
            )
            write_file(
                root / 'scripts' / 'lint_graph.py',
                'print("PASS: graph lint succeeded")\n',
            )

            env = os.environ | {'RESEARCHKB_RESET_ROOT': str(root)}
            result = subprocess.run(
                [sys.executable, str(script_path), '--force'],
                cwd=root,
                capture_output=True,
                text=True,
                env=env,
            )

            combined = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, combined)
            self.assertIn('PASS: graph lint succeeded', combined)
            self.assertEqual(
                (root / 'ontology' / 'relations' / 'based_on.md').read_text(encoding='utf-8'),
                '## 关系语义说明\n- fixture\n\n## 实例边\n- 无\n',
            )
            self.assertFalse((root / 'ontology' / 'entities' / 'papers' / 'Fixture Paper.md').exists())
            self.assertFalse((root / 'ontology' / 'entities' / 'methods' / 'Fixture Method.md').exists())
            self.assertTrue((root / 'ontology' / 'entities' / 'papers' / 'index.md').exists())
            self.assertTrue(raw_pdf.exists())
            self.assertEqual(
                (root / 'ontology' / 'log.md').read_text(encoding='utf-8'),
                '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n',
            )
            self.assertEqual((root / 'ontology' / 'graph-standard.md').read_text(encoding='utf-8'), '# graph standard\n')
```

- [ ] **Step 3: Run the targeted RED tests and confirm they fail for the right reasons**

Run:

```bash
python3 -m unittest \
  -v
```

Expected: FAIL. The current script does not expose `clear_relation_ledger_text`, `clear_entity_instance_pages`, or `write_empty_log`; it also lacks the test-only root override and still copies from `baseline/ontology/`.

- [ ] **Step 4: Commit the failing tests**

```bash
git commit -m "test: cover live-derived ontology reset"
```

### Task 2: Refactor the restore script to perform live-derived reset

**Files:**
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`

- [ ] **Step 1: Re-run the RED tests for the script behavior**

Run:

```bash
python3 -m unittest \
  -v
```

Expected: still FAIL before implementation.

- [ ] **Step 2: Replace the old baseline-copy script with the live-derived implementation**

Rewrite `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py` to this structure:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
ROOT = Path(os.environ.get('RESEARCHKB_RESET_ROOT', DEFAULT_ROOT)).resolve()
ONTOLOGY = ROOT / 'ontology'
ENTITIES = ONTOLOGY / 'entities'
RELATIONS = ONTOLOGY / 'relations'
LOG_FILE = ONTOLOGY / 'log.md'
RESET_ENTITY_DIRS = [
    'papers',
    'methods',
    'concepts',
    'tasks',
    'scenarios',
    'benchmarks',
    'evidence',
]
EMPTY_LOG = '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n'

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

def clear_relation_ledger_text(text: str) -> str:
    marker = '## 实例边'
    if marker not in text:
        raise ValueError('missing ## 实例边 heading in relation ledger')
    prefix = text.split(marker, 1)[0].rstrip()
    return f"{prefix}\n\n{marker}\n- 无\n"

def clear_relation_ledgers(relations_dir: Path) -> None:
    for path in sorted(relations_dir.glob('*.md')):
        path.write_text(clear_relation_ledger_text(path.read_text(encoding='utf-8')), encoding='utf-8')

def clear_entity_instance_pages(entities_dir: Path) -> None:
    for dirname in RESET_ENTITY_DIRS:
        entity_dir = entities_dir / dirname
        entity_dir.mkdir(parents=True, exist_ok=True)
        for path in entity_dir.glob('*.md'):
            if path.name != 'index.md':
                path.unlink()

def write_empty_log(log_path: Path) -> None:
    log_path.write_text(EMPTY_LOG, encoding='utf-8')

def ensure_required_paths() -> None:
    if not ONTOLOGY.exists():
        raise FileNotFoundError(f'missing ontology directory: {ONTOLOGY}')
    if not ENTITIES.exists():
        raise FileNotFoundError(f'missing entities directory: {ENTITIES}')
    if not RELATIONS.exists():
        raise FileNotFoundError(f'missing relations directory: {RELATIONS}')

def reset_live_ontology() -> None:
    ensure_required_paths()
    clear_entity_instance_pages(ENTITIES)
    clear_relation_ledgers(RELATIONS)
    write_empty_log(LOG_FILE)

def main() -> int:
    args = parse_args()

    try:
        ensure_required_paths()
    except FileNotFoundError as exc:
        print(f'failed: {exc}')
        return 1

    if ontology_is_dirty() and not args.force:
        print('blocked: ontology has uncommitted changes; rerun with --force to overwrite')
        return 2

    if args.check_only:
        print('success: live-derived reset preconditions satisfied')
        return 0

    try:
        reset_live_ontology()
    except ValueError as exc:
        print(f'failed: {exc}')
        return 1

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

- [ ] **Step 3: Run the focused GREEN tests for the restore script**

Run:

```bash
python3 -m unittest \
  -v
```

Expected: PASS.

- [ ] **Step 4: Commit the script refactor**

```bash
git commit -m "feat: derive empty ontology reset from live structure"
```

### Task 3: Update the skill contract to match the new reset semantics

**Files:**
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- Test: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`

- [ ] **Step 1: Rewrite the skill description so it no longer claims baseline-copy behavior**

Replace the current frontmatter + body with:

```md
---
name: reset-to-empty-ontology-baseline
description: 把 ResearchKB 的 ontology 重置到当前 live 结构下的空图状态，用于 cold-start ingest / relation / projection / governance 回归测试。Whenever 用户要求恢复空骨架、清空 ontology 但保留当前导航骨架与 raw PDFs、或为单篇论文测试重置图谱时，都应使用此 skill。
---

# Reset to Empty Ontology Baseline

## Purpose
把 `ontology/` 重置到当前 live 结构下的空图状态：
- 保留当前各对象域 `index.md`
- 保留 `ontology/entities/raw-sources/index.md`
- 保留 `ontology/entities/raw-sources/files/*.pdf`
- 删除对象实例页
- 将 `ontology/relations/*.md` 清空为当前格式的空账本
- 将 `ontology/log.md` 重写为空日志基线
- 立即运行 `python3 scripts/lint_graph.py` 验证结果

## Safety
- 默认先检查 `git status --short -- ontology`
- 若 `ontology/` 下存在未提交改动，则默认中止
- 只有用户明确允许覆盖时，才可带 `--force` 执行恢复

## Execution
1. 运行 `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
2. 如用户已确认覆盖当前 ontology，则附加 `--force`
3. 成功后回报 lint 结果与保留项（indexes / raw PDFs）

## Output
```yaml
status: success | blocked | failed
lint: pass | fail
warnings: []
manual_followups: []
```
```

- [ ] **Step 2: Sanity-check the skill text for stale phrases**

Run:

```bash
grep -n "skill 自带的严格空骨架基线\|baseline/ontology\|baseline snapshot" \
  .claude/skills/reset-to-empty-ontology-baseline/SKILL.md
```

Expected: no output.

- [ ] **Step 3: Commit the skill-doc update**

```bash
git add .claude/skills/reset-to-empty-ontology-baseline/SKILL.md
git commit -m "docs: update reset skill for live-derived behavior"
```

### Task 4: Run full verification and capture the live safety behavior

**Files:**
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the complete reset-related unittest coverage**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 2: Run the live repo lint without performing a destructive reset**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: PASS: `PASS: graph lint succeeded`.

- [ ] **Step 3: Verify the live repo still blocks accidental overwrite**

Run:

```bash
python3 .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py --check-only
```

Expected in the current dirty working tree: `blocked: ontology has uncommitted changes; rerun with --force to overwrite`.

- [ ] **Step 4: Commit the final verified redesign**

```bash
  .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py \
  .claude/skills/reset-to-empty-ontology-baseline/SKILL.md
git commit -m "feat: redesign empty ontology reset workflow"
```

---

## Self-review checklist

- Spec coverage:
  - live-derived relation clearing: covered in Task 1 tests + Task 2 implementation
  - object-instance deletion while keeping indexes/raw PDFs: covered in Task 1 tests + Task 2 implementation
  - empty log rewrite: covered in Task 1 tests + Task 2 implementation
  - skill contract rewrite: covered in Task 3
  - lint verification and live safety behavior: covered in Task 4
- Placeholder scan: no placeholder markers remain
- Type consistency:
  - helper names used consistently: `clear_relation_ledger_text`, `clear_relation_ledgers`, `clear_entity_instance_pages`, `write_empty_log`, `reset_live_ontology`
  - env override name used consistently: `RESEARCHKB_RESET_ROOT`
