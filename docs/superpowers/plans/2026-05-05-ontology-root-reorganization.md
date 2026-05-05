# Ontology Root Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-root ResearchKB from `wiki/` to `ontology/`, promote the ontology entrypoints to the new root, move all serving-ready object domains under `ontology/entities/`, keep relation ledgers under `ontology/relations/`, and retarget workflow docs and graph lint so the new structure is the only canonical knowledge layout.

**Architecture:** Make the filesystem match the approved information architecture first, then update workflow-critical path assumptions, then clean human-facing path text, and finally run graph-governance verification. To avoid leaving a dangling `wiki/` root behind, also move the operational ingest log from `wiki/log.md` to `ontology/log.md` even though it is not part of the six entity domains.

**Tech Stack:** Markdown knowledge pages under `ontology/`, workflow skills under `.claude/skills/`, Python 3 lint script `scripts/lint_graph.py`, Git file moves via `git mv`, shell verification via `find`, `grep`, and inline `python3` scripts.

---

## File map

### Root entrypoints and operational log
- Move: `wiki/ontology/index.md` → `ontology/index.md`
- Move: `wiki/ontology/graph-standard.md` → `ontology/graph-standard.md`
- Move: `wiki/log.md` → `ontology/log.md`

### Entity directories to move under `ontology/entities/`
- Move: `wiki/papers/` → `ontology/entities/papers/`
- Move: `wiki/methods/` → `ontology/entities/methods/`
- Move: `wiki/concepts/` → `ontology/entities/concepts/`
- Move: `wiki/tasks/` → `ontology/entities/tasks/`
- Move: `wiki/scenarios/` → `ontology/entities/scenarios/`
- Move: `wiki/benchmarks/` → `ontology/entities/benchmarks/`

### Relation ledgers
- Move: `wiki/relations/` → `ontology/relations/`

### Workflow and governance docs to modify
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`

### Lint and structure enforcement
- Modify: `scripts/lint_graph.py`

### Moved knowledge pages whose displayed paths must be rewritten
- Modify after move: `ontology/index.md`
- Modify after move: `ontology/graph-standard.md`
- Modify after move: `ontology/log.md`
- Modify after move: all `*.md` files under:
  - `ontology/entities/papers/`
  - `ontology/entities/methods/`
  - `ontology/entities/concepts/`
  - `ontology/entities/tasks/`
  - `ontology/entities/scenarios/`
  - `ontology/entities/benchmarks/`
  - `ontology/relations/`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `grep -RIn "wiki/ontology\|wiki/papers\|wiki/methods\|wiki/concepts\|wiki/tasks\|wiki/scenarios\|wiki/benchmarks\|wiki/relations\|wiki/log.md" CLAUDE.md .claude/skills scripts ontology`
- Test: `find ontology -maxdepth 3 \( -type d -o -type f \) | sort`
- Test: targeted manual navigation checks through `ontology/index.md`, one entity-domain index, one entity page, one relation ledger, and one evidence cache

---

### Task 1: Move the knowledge root into the approved `ontology/` structure

**Files:**
- Move: `wiki/ontology/index.md` → `ontology/index.md`
- Move: `wiki/ontology/graph-standard.md` → `ontology/graph-standard.md`
- Move: `wiki/log.md` → `ontology/log.md`
- Move: `wiki/papers/` → `ontology/entities/papers/`
- Move: `wiki/methods/` → `ontology/entities/methods/`
- Move: `wiki/concepts/` → `ontology/entities/concepts/`
- Move: `wiki/tasks/` → `ontology/entities/tasks/`
- Move: `wiki/scenarios/` → `ontology/entities/scenarios/`
- Move: `wiki/benchmarks/` → `ontology/entities/benchmarks/`
- Move: `wiki/relations/` → `ontology/relations/`
- Test: inline filesystem assertions

- [ ] **Step 1: Capture the pre-move baseline so you know exactly what exists**

Run:

```bash
find wiki -maxdepth 2 \( -type d -o -type f \) | sort
```

Expected: output includes `wiki/ontology/index.md`, `wiki/ontology/graph-standard.md`, the six object-domain directories, `wiki/relations/`, and `wiki/log.md`.

- [ ] **Step 2: Create the target directories and move every canonical knowledge path with `git mv`**

Run:

```bash
mkdir -p ontology/entities ontology/relations && \
  git mv wiki/ontology/index.md ontology/index.md && \
  git mv wiki/ontology/graph-standard.md ontology/graph-standard.md && \
  git mv wiki/log.md ontology/log.md && \
  git mv wiki/papers ontology/entities/papers && \
  git mv wiki/methods ontology/entities/methods && \
  git mv wiki/concepts ontology/entities/concepts && \
  git mv wiki/tasks ontology/entities/tasks && \
  git mv wiki/scenarios ontology/entities/scenarios && \
  git mv wiki/benchmarks ontology/entities/benchmarks && \
  git mv wiki/relations ontology/relations
```

Expected: Git stages pure renames/moves for all canonical knowledge files.

- [ ] **Step 3: Remove the now-empty legacy directories if they remain**

Run:

```bash
rmdir wiki/ontology 2>/dev/null || true && \
  rmdir wiki 2>/dev/null || true
```

Expected: no `wiki/` directory remains, or the command is a harmless no-op if Git already removed it.

- [ ] **Step 4: Verify the filesystem now matches the approved root structure**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
required = [
    Path('ontology/index.md'),
    Path('ontology/graph-standard.md'),
    Path('ontology/log.md'),
    Path('ontology/entities/papers'),
    Path('ontology/entities/methods'),
    Path('ontology/entities/concepts'),
    Path('ontology/entities/tasks'),
    Path('ontology/entities/scenarios'),
    Path('ontology/entities/benchmarks'),
    Path('ontology/relations'),
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, missing
assert not Path('wiki').exists(), 'legacy wiki/ directory still exists'
print('ontology root structure ok')
PY
```

Expected: prints `ontology root structure ok`.

- [ ] **Step 5: Commit the filesystem re-rooting**

```bash
git add ontology && \
  git commit -m "refactor: move knowledge root under ontology"
```

---

### Task 2: Retarget `CLAUDE.md` and workflow skills to the new ontology paths

**Files:**
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Test: targeted grep on those files

- [ ] **Step 1: Run a targeted rewrite script for all deterministic path replacements in workflow-facing files**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
files = [
    Path('CLAUDE.md'),
    Path('.claude/skills/paper-ingest/SKILL.md'),
    Path('.claude/skills/relation-reconciliation/SKILL.md'),
    Path('.claude/skills/page-projection-sync/SKILL.md'),
    Path('.claude/skills/ontology-semantic-review/SKILL.md'),
    Path('.claude/skills/ontology-semantic-review/references/diff-review-playbook.md'),
    Path('.claude/skills/serving-governance-review/SKILL.md'),
    Path('.claude/skills/relation-reconciliation/evals/quality-checklist.md'),
    Path('.claude/skills/paper-ingest/evals/regression-samples.json'),
]
replacements = [
    ('wiki/ontology/graph-standard.md', 'ontology/graph-standard.md'),
    ('wiki/ontology/index.md', 'ontology/index.md'),
    ('wiki/papers/', 'ontology/entities/papers/'),
    ('wiki/methods/', 'ontology/entities/methods/'),
    ('wiki/concepts/', 'ontology/entities/concepts/'),
    ('wiki/tasks/', 'ontology/entities/tasks/'),
    ('wiki/scenarios/', 'ontology/entities/scenarios/'),
    ('wiki/benchmarks/', 'ontology/entities/benchmarks/'),
    ('wiki/relations/', 'ontology/relations/'),
    ('wiki/log.md', 'ontology/log.md'),
    ('`wiki/<对象域>/index.md`', '`ontology/entities/<对象域>/index.md`'),
    ('`wiki/`', '`ontology/`'),
]
for path in files:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
PY
```

Expected: the selected files now use `ontology/` and `ontology/entities/` / `ontology/relations/` paths instead of `wiki/...`.

- [ ] **Step 2: Manually fix the non-mechanical wording in `CLAUDE.md` and skill docs so the new layers are described correctly**

Make these edits exactly where the wording appears:

```md
- 你负责维护所有 `ontology/` 内容，`raw/` 目录只读
- `ontology/index.md` 负责系统级导航
- `ontology/entities/<对象域>/index.md` 负责对象域内导航
- `ontology/relations/*.md` 负责正式关系治理导航
- 本体实例编译层：`intermediate/papers/`、`ontology/relations/`、`ontology/entities/` 对象页
- 汇总 `ontology/entities/papers/`、`ontology/entities/methods/`、`ontology/entities/concepts/`、`ontology/entities/tasks/`、`ontology/entities/benchmarks/`、`ontology/entities/scenarios/`、`ontology/relations/`
```

Also make these exact workflow corrections:

```md
# .claude/skills/paper-ingest/SKILL.md
- formal page candidates live under `ontology/entities/...`
- relation ledgers live under `ontology/relations/...`
- update `ontology/index.md`
- update `ontology/log.md`

# .claude/skills/serving-governance-review/SKILL.md
- Are there missing key neighbors that would force runtime fallback to `ontology/relations/`?

# .claude/skills/relation-reconciliation/evals/quality-checklist.md
- [ ] Routes each relation type to the correct `ontology/relations/*.md` file.
```

- [ ] **Step 3: Verify that the workflow-critical files no longer contain stale `wiki/...` paths**

Run:

```bash
grep -RIn "wiki/ontology\|wiki/papers\|wiki/methods\|wiki/concepts\|wiki/tasks\|wiki/scenarios\|wiki/benchmarks\|wiki/relations\|wiki/log.md" \
  CLAUDE.md \
  .claude/skills/paper-ingest \
  .claude/skills/relation-reconciliation \
  .claude/skills/page-projection-sync \
  .claude/skills/ontology-semantic-review \
  .claude/skills/serving-governance-review
```

Expected: no output.

- [ ] **Step 4: Commit the workflow-path retargeting**

```bash
git add CLAUDE.md .claude/skills && \
  git commit -m "docs: retarget workflows to ontology root"
```

---

### Task 3: Rewrite displayed paths inside moved ontology pages

**Files:**
- Modify: `ontology/index.md`
- Modify: `ontology/graph-standard.md`
- Modify: `ontology/log.md`
- Modify: all moved markdown files under `ontology/entities/` and `ontology/relations/`
- Test: grep on `ontology/`

- [ ] **Step 1: Run a bulk markdown rewrite under `ontology/` for deterministic displayed path strings**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
replacements = [
    ('wiki/ontology/graph-standard.md', 'ontology/graph-standard.md'),
    ('wiki/ontology/index.md', 'ontology/index.md'),
    ('wiki/papers/', 'ontology/entities/papers/'),
    ('wiki/methods/', 'ontology/entities/methods/'),
    ('wiki/concepts/', 'ontology/entities/concepts/'),
    ('wiki/tasks/', 'ontology/entities/tasks/'),
    ('wiki/scenarios/', 'ontology/entities/scenarios/'),
    ('wiki/benchmarks/', 'ontology/entities/benchmarks/'),
    ('wiki/relations/', 'ontology/relations/'),
    ('`wiki/<对象域>/index.md`', '`ontology/entities/<对象域>/index.md`'),
    ('`wiki/`', '`ontology/`'),
]
for path in Path('ontology').rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
PY
```

Expected: the moved content tree no longer displays old `wiki/...` paths.

- [ ] **Step 2: Manually fix the router and specification pages so the object layer is explicitly `entities/`**

Ensure these exact lines exist in the moved pages:

```md
# ontology/index.md
- Papers：[[entities/papers/index|ontology/entities/papers/index.md]]
- Methods：[[entities/methods/index|ontology/entities/methods/index.md]]
- Concepts：[[entities/concepts/index|ontology/entities/concepts/index.md]]
- Tasks：[[entities/tasks/index|ontology/entities/tasks/index.md]]
- Scenarios：[[entities/scenarios/index|ontology/entities/scenarios/index.md]]
- Benchmarks：[[entities/benchmarks/index|ontology/entities/benchmarks/index.md]]
- 想做受约束知识问答 → 先进入对应 `ontology/entities/<对象域>/index.md`

# ontology/graph-standard.md
- `ontology/relations/` 是正式维护实例边账本的唯一治理真源。
- `ontology/entities/papers/`、`ontology/entities/methods/`、`ontology/entities/concepts/`、`ontology/entities/tasks/`、`ontology/entities/scenarios/`、`ontology/entities/benchmarks/` 与 `intermediate/papers/` 中的 Evidence 页，在治理通过后，作为受约束知识问答的默认服务层。
```

Also update `ontology/log.md` so its top links still point to the new root pages:

```md
- 导航入口：[[ontology/index|ontology-index]]
- 图谱规范：[[graph-standard]]
```

- [ ] **Step 3: Verify the ontology content tree no longer contains stale root-path text**

Run:

```bash
grep -RIn "wiki/ontology\|wiki/papers\|wiki/methods\|wiki/concepts\|wiki/tasks\|wiki/scenarios\|wiki/benchmarks\|wiki/relations\|wiki/log.md" ontology
```

Expected: no output.

- [ ] **Step 4: Commit the content-layer path rewrite**

```bash
git add ontology && \
  git commit -m "docs: rewrite ontology content paths"
```

---

### Task 4: Retarget `scripts/lint_graph.py` to the ontology root model

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`
- Test: targeted grep on `scripts/lint_graph.py`

- [ ] **Step 1: Rewrite the root path constants so the lint script expects the new directory layout**

In `scripts/lint_graph.py`, replace the current directory and file constant blocks with:

```python
REQUIRED_DIRECTORIES = [
    'ontology/entities/tasks',
    'ontology/entities/benchmarks',
    'ontology/entities/papers',
    'ontology/entities/methods',
    'ontology/entities/concepts',
    'ontology/entities/scenarios',
    'ontology/relations',
    'intermediate/papers',
    'scripts',
]

REQUIRED_FILES = [
    'ontology/index.md',
    'ontology/graph-standard.md',
    'ontology/log.md',
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

CLAUDE_NEEDLES = [
    'ontology/entities/tasks/',
    'ontology/entities/benchmarks/',
    'ontology/index.md',
    'ontology/graph-standard.md',
    'ontology/relations/',
    'python3 scripts/lint_graph.py',
]

NAVIGATION_ENTRY_PATH = 'ontology/index.md'
```

- [ ] **Step 2: Replace every serving-page path prefix and scan root with the ontology equivalents**

Update `classify_serving_page` to:

```python
def classify_serving_page(rel: str) -> str | None:
    if rel.startswith('ontology/entities/papers/'):
        return 'paper'
    if rel.startswith('ontology/entities/methods/'):
        return 'method'
    if rel.startswith('ontology/entities/concepts/'):
        return 'concept'
    if rel.startswith('ontology/entities/tasks/'):
        return 'task'
    if rel.startswith('ontology/entities/scenarios/'):
        return 'scenario'
    if rel.startswith('ontology/entities/benchmarks/'):
        return 'benchmark'
    if rel.startswith('intermediate/papers/'):
        return 'evidence'
    return None
```

Update the scan loops and summary block to:

```python
for path in (ROOT / 'ontology').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type is None:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))

knowledge_pages = []
with_wikilinks = 0
for path in (ROOT / 'ontology').rglob('*.md'):
    knowledge_pages.append(path)
    text = path.read_text(encoding='utf-8', errors='ignore')
    if WIKILINK_RE.search(text):
        with_wikilinks += 1
    else:
        errors.append(f'ontology page has no wikilinks: {path.relative_to(ROOT)}')

print('PASS: graph lint succeeded')
print({'ontology_pages': len(knowledge_pages), 'with_wikilinks': with_wikilinks})
```

- [ ] **Step 3: Run a mechanical path rewrite inside the lint fixtures and rule tables, then manually fix any leftovers**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('scripts/lint_graph.py')
text = path.read_text(encoding='utf-8')
replacements = [
    ('wiki/ontology/graph-standard.md', 'ontology/graph-standard.md'),
    ('wiki/ontology/index.md', 'ontology/index.md'),
    ("'wiki/papers/", "'ontology/entities/papers/"),
    ("'wiki/methods/", "'ontology/entities/methods/"),
    ("'wiki/concepts/", "'ontology/entities/concepts/"),
    ("'wiki/tasks/", "'ontology/entities/tasks/"),
    ("'wiki/scenarios/", "'ontology/entities/scenarios/"),
    ("'wiki/benchmarks/", "'ontology/entities/benchmarks/"),
    ('wiki/relations/', 'ontology/relations/'),
]
for old, new in replacements:
    text = text.replace(old, new)
path.write_text(text, encoding='utf-8')
PY
```

Then manually confirm that these calls now point at ontology paths:

```python
graph_standard_text = read_text('ontology/graph-standard.md')
if '## `sourced_from` 实例边' in read_text('ontology/relations/evidence_index.md'):
    errors.append('sourced_from must live in ontology/relations/provenance_links.md, not ontology/relations/evidence_index.md')
```

- [ ] **Step 4: Verify there are no stale `wiki/...` path assumptions left inside the lint script**

Run:

```bash
grep -n "wiki/ontology\|wiki/papers\|wiki/methods\|wiki/concepts\|wiki/tasks\|wiki/scenarios\|wiki/benchmarks\|wiki/relations\|wiki/log.md" scripts/lint_graph.py
```

Expected: no output.

- [ ] **Step 5: Run the full lint and fix any path-related failures until it passes**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded`.

If it fails, only make the smallest path-model corrections needed in `scripts/lint_graph.py`, `ontology/index.md`, `ontology/graph-standard.md`, or the moved pages, then rerun until it passes.

- [ ] **Step 6: Commit the lint-model retargeting**

```bash
git add scripts/lint_graph.py ontology && \
  git commit -m "fix: retarget graph lint to ontology structure"
```

---

### Task 5: Run regression cleanup and final verification for the new ontology root

**Files:**
- Modify if needed after verification: `CLAUDE.md`
- Modify if needed after verification: `.claude/skills/...`
- Modify if needed after verification: `ontology/...`
- Modify if needed after verification: `scripts/lint_graph.py`
- Test: repo-wide targeted grep, lint, manual navigation, diff review

- [ ] **Step 1: Run the final stale-path sweep over the active knowledge surfaces**

Run:

```bash
grep -RIn "wiki/ontology\|wiki/papers\|wiki/methods\|wiki/concepts\|wiki/tasks\|wiki/scenarios\|wiki/benchmarks\|wiki/relations\|wiki/log.md" \
  CLAUDE.md \
  .claude/skills \
  scripts \
  ontology
```

Expected: no output.

- [ ] **Step 2: Re-run graph lint as the gate for structural and path consistency**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded`.

- [ ] **Step 3: Manually verify the two representative navigation paths**

Read these files in order and confirm every hop exists and still makes sense:

```text
Path A:
ontology/index.md
→ ontology/entities/papers/index.md
→ ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
→ ontology/relations/paper_method_links.md
→ intermediate/papers/PathMind.sections.md

Path B:
ontology/index.md
→ ontology/entities/concepts/index.md
→ ontology/entities/concepts/复杂产品设计中的LLM-KG协同框架.md
→ ontology/relations/concept_links.md
→ intermediate/papers/LLM-KG-CPD-Survey.analysis.md
```

Expected: every file opens, displayed paths mention `ontology/...`, and the path order still reflects the approved serving-vs-governance split.

- [ ] **Step 4: Inspect the final diff footprint before the closing commit**

Run:

```bash
git diff --stat && \
  git status --short
```

Expected: only the planned root-reorganization moves and path-retargeting edits are present.

- [ ] **Step 5: Commit the final verified reorganization state**

```bash
git add CLAUDE.md .claude/skills scripts ontology && \
  git commit -m "refactor: land ontology root reorganization"
```

---

## Spec coverage check

- **Replace `wiki/` as the formal knowledge root with `ontology/`** → Task 1, Task 4, Task 5
- **Promote navigation and specification entrypoints to `ontology/index.md` and `ontology/graph-standard.md`** → Task 1, Task 3, Task 4
- **Add explicit `entities/` layer for all six object domains** → Task 1, Task 3, Task 4
- **Preserve `relations/` as the formal relation-ledger source of truth** → Task 1, Task 2, Task 3, Task 4
- **Allow staged migration with transition period** → entire task order, especially Task 2 before Task 5
- **Retarget workflow docs and lint to the new structure** → Task 2, Task 4
- **Clean human-facing path wording** → Task 3, Task 5
- **Keep the specification authority singular** → Task 2 and Task 3 preserve `ontology/graph-standard.md` as the only authority
- **Avoid new extra layers besides `entities/`** → Task 1 creates only `ontology/entities/` and `ontology/relations/`

## Placeholder scan

No `TODO`, `TBD`, or “implement later” placeholders remain. Every task contains concrete files, concrete commands, and concrete expected outcomes.

## Type and naming consistency check

Consistent names used throughout:
- knowledge root: `ontology/`
- navigation entrypoint: `ontology/index.md`
- specification authority: `ontology/graph-standard.md`
- entity layer: `ontology/entities/...`
- relation layer: `ontology/relations/...`
- operational log: `ontology/log.md`

The only planned addition not explicitly listed in the approved structure summary is `ontology/log.md`; it is included because current ingest workflows actively update `wiki/log.md`, and moving it is the smallest change that fully retires the legacy `wiki/` root.
