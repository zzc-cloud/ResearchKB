# Live-Derived Empty Ontology Reset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `/reset-to-empty-ontology-baseline` reset ResearchKB to a lint-clean empty graph state by deleting instance pages, clearing relation/log state, and emptying managed index blocks without relying on a static baseline snapshot.

**Architecture:** Keep the reset workflow live-derived inside `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`. Add one focused helper to clear managed blocks in object-domain index files, reuse the existing relation-clearing flow, and remove the stale `baseline/` snapshot so the skill follows the live ontology schema instead of a duplicated template.

**Tech Stack:** Python 3, filesystem operations via `pathlib`, existing `scripts/lint_graph.py`, Obsidian Markdown files in `ontology/`.

---

### Task 1: Update the skill contract to match live-derived reset

**Files:**
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- Test: `python3 .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py --check-only`

- [ ] **Step 1: Write the failing documentation expectation**

Add the following acceptance checklist to your scratchpad before editing so the doc change is concrete:

```text
The skill description must say:
- index.md files are kept but their managed navigation blocks are cleared
- raw-sources index and PDFs are preserved
- reset is live-derived, not baseline-driven
- reset still runs lint immediately
```

- [ ] **Step 2: Read the current skill text and verify it is missing the new contract**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('.claude/skills/reset-to-empty-ontology-baseline/SKILL.md').read_text(encoding='utf-8')
needles = [
    '清理对象域 index.md 中的受管入口块',
    'live-derived',
    '不依赖静态 baseline',
]
for needle in needles:
    print(f'{needle}:', needle in text)
PY`

Expected: at least one line prints `False`

- [ ] **Step 3: Update the skill description and execution steps**

Replace the purpose/safety/execution language with content equivalent to:

```md
## Purpose
把 `ontology/` 重置到当前 live 结构下的空图状态：
- 保留对象域 `index.md` 文件本身，但清理其受管导航区块
- 保留 `ontology/entities/raw-sources/index.md`
- 保留 `ontology/entities/raw-sources/files/*.pdf`
- 删除对象实例页
- 将 `ontology/relations/*.md` 清空为当前 live 格式的空账本
- 将 `ontology/log.md` 重写为空日志基线
- 立即运行 `python3 scripts/lint_graph.py` 验证结果

## Execution
1. 运行 `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
2. 如用户已确认覆盖当前 ontology，则附加 `--force`
3. 成功后回报 lint 结果与保留项（indexes / raw PDFs）
```

Keep the frontmatter `name` unchanged.

- [ ] **Step 4: Run the precondition command and verify the skill text is internally consistent**

Run: `python3 .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py --check-only`

Expected: `success: live-derived reset preconditions satisfied`

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/reset-to-empty-ontology-baseline/SKILL.md
git commit -m "docs: align reset skill with live-derived contract"
```

### Task 2: Add a failing regression test for managed index clearing

**Files:**
- Create: `scripts/test_reset_to_empty_ontology_baseline.py`
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- Test: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

- [ ] **Step 1: Write the failing test**

Create `scripts/test_reset_to_empty_ontology_baseline.py` with this exact test harness:

```python
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path('.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py').resolve()


def git(command: list[str], cwd: Path) -> None:
    subprocess.run(['git', *command], cwd=cwd, check=True, capture_output=True, text=True)


def main() -> int:
    repo_root = Path.cwd().resolve()
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp) / 'repo'
        shutil.copytree(repo_root, sandbox, ignore=shutil.ignore_patterns('.git', '__pycache__', '.DS_Store', '.smart-env'))
        git(['init'], sandbox)
        git(['config', 'user.name', 'Test User'], sandbox)
        git(['config', 'user.email', 'test@example.com'], sandbox)
        git(['add', '.'], sandbox)
        git(['commit', '-m', 'sandbox snapshot'], sandbox)

        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=sandbox,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, 'RESEARCHKB_RESET_ROOT': str(sandbox)},
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError('reset should succeed in sandbox')

        methods_index = (sandbox / 'ontology/entities/methods/index.md').read_text(encoding='utf-8')
        papers_index = (sandbox / 'ontology/entities/papers/index.md').read_text(encoding='utf-8')
        raw_index = (sandbox / 'ontology/entities/raw-sources/index.md').read_text(encoding='utf-8')

        assert '[[ontology/entities/methods/PathMind]]' not in methods_index
        assert '[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]' not in papers_index
        assert '[[ontology/entities/raw-sources/files/' in raw_index
        assert '- 无' in (sandbox / 'ontology/relations/references_method.md').read_text(encoding='utf-8')
        assert '2026-04-30 init' not in (sandbox / 'ontology/log.md').read_text(encoding='utf-8')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

- [ ] **Step 2: Run the test to verify it fails for the current bug**

Run: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

Expected: `AssertionError` because managed index blocks still contain deleted instance links

- [ ] **Step 3: Confirm the failure points to the missing behavior, not test setup**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py').read_text(encoding='utf-8')
print('clear_entity_instance_pages' in text)
print('clear_relation_ledgers' in text)
print('clear_index' in text or 'managed block' in text)
PY`

Expected:
- first line `True`
- second line `True`
- third line `False`

- [ ] **Step 4: Commit the failing test**

```bash
git add scripts/test_reset_to_empty_ontology_baseline.py
git commit -m "test: capture reset index-clearing regression"
```

### Task 3: Implement managed index clearing in the reset script

**Files:**
- Modify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- Test: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

- [ ] **Step 1: Write the minimal implementation helpers**

Add these constants and helpers near the top-level definitions:

```python
INDEX_MANAGED_BLOCK_NAMES = {
    'papers': ['navigation-entries', 'non-serving-placeholders'],
    'methods': ['navigation-entries', 'non-serving-placeholders'],
    'concepts': ['navigation-entries', 'non-serving-placeholders'],
    'tasks': ['navigation-entries', 'non-serving-placeholders'],
    'scenarios': ['navigation-entries', 'non-serving-placeholders'],
    'benchmarks': ['navigation-entries', 'non-serving-placeholders'],
    'evidence': ['navigation-entries', 'non-serving-placeholders'],
}


def clear_managed_block(text: str, block_name: str) -> str:
    begin = f'<!-- BEGIN MANAGED BLOCK:{block_name} -->'
    end = f'<!-- END MANAGED BLOCK:{block_name} -->'
    if begin not in text or end not in text:
        raise ValueError(f'missing managed block markers for {block_name}')
    before, remainder = text.split(begin, 1)
    middle, after = remainder.split(end, 1)
    return f'{before}{begin}\n{end}{after}'


def clear_index_managed_blocks(entities_dir: Path) -> None:
    for dirname, block_names in INDEX_MANAGED_BLOCK_NAMES.items():
        index_path = entities_dir / dirname / 'index.md'
        text = index_path.read_text(encoding='utf-8')
        for block_name in block_names:
            text = clear_managed_block(text, block_name)
        index_path.write_text(text, encoding='utf-8')
```

Do not include `raw-sources` in `INDEX_MANAGED_BLOCK_NAMES`.

- [ ] **Step 2: Call the new helper from the reset flow**

Update `reset_live_ontology()` to:

```python
def reset_live_ontology() -> None:
    ensure_required_paths()
    clear_entity_instance_pages(ENTITIES)
    clear_relation_ledgers(RELATIONS)
    write_empty_log(LOG_FILE)
    clear_index_managed_blocks(ENTITIES)
```

- [ ] **Step 3: Run the regression test to verify it passes**

Run: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

Expected: exit code 0 with no assertion output

- [ ] **Step 4: Re-run the script-level precondition and main verification**

Run: `python3 .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py --check-only`

Expected: `success: live-derived reset preconditions satisfied`

Run: `python3 scripts/lint_graph.py`

Expected: `PASS: graph lint succeeded`

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py scripts/test_reset_to_empty_ontology_baseline.py
git commit -m "feat: clear managed index blocks during ontology reset"
```

### Task 4: Remove the stale baseline snapshot and cache artifacts

**Files:**
- Delete: `.claude/skills/reset-to-empty-ontology-baseline/baseline/`
- Delete: `.claude/skills/reset-to-empty-ontology-baseline/__pycache__/`
- Test: `git diff --name-status -- .claude/skills/reset-to-empty-ontology-baseline`

- [ ] **Step 1: Verify the snapshot directory still exists before deletion**

Run: `find .claude/skills/reset-to-empty-ontology-baseline -maxdepth 2 \( -name baseline -o -name __pycache__ \) | sort`

Expected: both `baseline` and `__pycache__` appear

- [ ] **Step 2: Delete the directories**

Run: `rm -rf .claude/skills/reset-to-empty-ontology-baseline/baseline .claude/skills/reset-to-empty-ontology-baseline/__pycache__`

Expected: command exits 0

- [ ] **Step 3: Verify only the intended skill files remain**

Run: `find .claude/skills/reset-to-empty-ontology-baseline -maxdepth 2 -print | sort`

Expected output contains only:
- `.claude/skills/reset-to-empty-ontology-baseline`
- `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/reset-to-empty-ontology-baseline
git commit -m "chore: remove reset baseline snapshot files"
```

### Task 5: Verify the full reset workflow in a sandbox repository

**Files:**
- Modify: `scripts/test_reset_to_empty_ontology_baseline.py`
- Test: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

- [ ] **Step 1: Extend the regression test to verify deleted instance pages and preserved PDFs**

Update the assertions section in `scripts/test_reset_to_empty_ontology_baseline.py` to include:

```python
        assert not (sandbox / 'ontology/entities/methods/PathMind.md').exists()
        assert not (sandbox / 'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md').exists()
        assert (sandbox / 'ontology/entities/raw-sources/files').exists()
        assert list((sandbox / 'ontology/entities/raw-sources/files').glob('*.pdf'))
```

Keep the earlier assertions unchanged.

- [ ] **Step 2: Run the test to verify the full reset contract passes**

Run: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

Expected: exit code 0 with no output

- [ ] **Step 3: Run the standalone lint command as independent verification**

Run: `python3 scripts/lint_graph.py`

Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit**

```bash
git add scripts/test_reset_to_empty_ontology_baseline.py
git commit -m "test: verify full live-derived reset contract"
```

### Task 6: Final verification and branch hygiene

**Files:**
- Verify: `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- Verify: `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- Verify: `scripts/test_reset_to_empty_ontology_baseline.py`

- [ ] **Step 1: Run the targeted regression test**

Run: `python3 scripts/test_reset_to_empty_ontology_baseline.py`

Expected: exit code 0

- [ ] **Step 2: Run the repo lint command**

Run: `python3 scripts/lint_graph.py`

Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Inspect the working tree for unrelated ontology mutations**

Run: `git status --short`

Expected: only the planned skill/script/doc changes remain

- [ ] **Step 4: Create the final commit**

```bash
git add .claude/skills/reset-to-empty-ontology-baseline/SKILL.md \
        .claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py \
        scripts/test_reset_to_empty_ontology_baseline.py \
        docs/superpowers/specs/2026-05-10-live-derived-empty-ontology-reset-design.md \
        docs/superpowers/plans/2026-05-10-live-derived-empty-ontology-reset.md
git commit -m "fix: make ontology reset live-derived and lint-clean"
```
