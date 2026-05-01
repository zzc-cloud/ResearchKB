# Remove Ontology Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `wiki/ontology/index.md`, consolidate ontology navigation into `wiki/ontology/graph-standard.md`, and keep the main wiki index pointing directly at the ontology authority page.

**Architecture:** This is a narrow documentation-structure cleanup. The implementation removes the shallow ontology landing page, rewires `wiki/index.md` to point directly to `graph-standard`, and adds a small navigation block at the top of `graph-standard` so it can serve as both authority page and ontology entry point.

**Tech Stack:** Markdown, Obsidian wikilinks, Python 3, grep, git

---

## File structure

- `wiki/ontology/index.md` — current shallow ontology landing page; delete it
- `wiki/index.md` — main wiki navigation; replace all `[[ontology/index|ontology]]` links with `[[graph-standard|ontology]]`
- `wiki/ontology/graph-standard.md` — ontology authority page; add a short navigation block near the top linking the formal relation ledgers
- `scripts/lint_graph.py` — existing verifier; run it unchanged to confirm the documentation graph still passes

### Task 1: Update ontology entry points

**Files:**
- Modify: `wiki/index.md:12-13`
- Modify: `wiki/index.md:22-23`
- Modify: `wiki/index.md:132-133`
- Modify: `wiki/ontology/graph-standard.md:1-10`

- [ ] **Step 1: Replace the top-level ontology link in `wiki/index.md`**

Replace this block:

```markdown
- [[ontology/index|ontology]]
- [[graph-standard]]
```

with this block:

```markdown
- [[graph-standard|ontology]]
- [[graph-standard]]
```

- [ ] **Step 2: Replace the ontology/modeling section link in `wiki/index.md`**

Replace this block:

```markdown
### 本体 / 模式建模
- [[ontology/index|ontology]]
- [[graph-standard]]
- [[复杂产品设计中的LLM-KG协同框架]]
```

with this block:

```markdown
### 本体 / 模式建模
- [[graph-standard|ontology]]
- [[graph-standard]]
- [[复杂产品设计中的LLM-KG协同框架]]
```

- [ ] **Step 3: Replace the ontology object-section link in `wiki/index.md`**

Replace this block:

```markdown
### 本体
- [[ontology/index|ontology]]
- [[graph-standard]]
```

with this block:

```markdown
### 本体
- [[graph-standard|ontology]]
- [[graph-standard]]
```

- [ ] **Step 4: Add a short navigation block near the top of `wiki/ontology/graph-standard.md`**

Insert this block immediately below the `# Graph Standard` heading:

```markdown
## 相关关系账本
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
```

The top of the file should become:

```markdown
# Graph Standard

## 相关关系账本
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]

## 节点类型
- Paper：论文实例节点
- Method：方法节点
```

- [ ] **Step 5: Review the edited files before deletion**

Run:

```bash
grep -n "ontology/index\|graph-standard|ontology" wiki/index.md wiki/ontology/graph-standard.md
```

Expected:
- `wiki/index.md` shows `[[graph-standard|ontology]]` in the three ontology entry locations
- `wiki/ontology/graph-standard.md` shows the new `## 相关关系账本` block
- No `[[ontology/index|ontology]]` remains in those two files

- [ ] **Step 6: Commit the navigation rewiring**

Run:

```bash
git add wiki/index.md wiki/ontology/graph-standard.md
git commit -m "docs: consolidate ontology navigation into graph standard"
```

Expected:
- A new commit is created containing only the two modified Markdown files

### Task 2: Remove the obsolete ontology landing page

**Files:**
- Delete: `wiki/ontology/index.md`

- [ ] **Step 1: Confirm the current file contents before deleting**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('wiki/ontology/index.md')
text = path.read_text()
print(text)
assert '# Ontology Index' in text
assert '[[graph-standard]]' in text
PY
```

Expected:
- The file prints to stdout
- The assertions pass, proving the deletion target is the shallow landing page rather than a repurposed document

- [ ] **Step 2: Delete `wiki/ontology/index.md`**

Run:

```bash
rm wiki/ontology/index.md
```

Expected:
- The file is removed from the working tree

- [ ] **Step 3: Verify there are no remaining runtime wiki references to the deleted page**

Run:

```bash
grep -R -n "\[\[ontology/index\|wiki/ontology/index.md" wiki CLAUDE.md
```

Expected:
- No matches

Notes:
- Matches in historical plan/spec documents under `docs/` are acceptable for this task
- Only runtime knowledge-base surfaces (`wiki/` and `CLAUDE.md`) must be clean

- [ ] **Step 4: Review git status before final verification**

Run:

```bash
git status --short
```

Expected:
- `D wiki/ontology/index.md`
- No unexpected wiki file changes beyond the edits from Task 1

- [ ] **Step 5: Commit the page removal**

Run:

```bash
git add wiki/ontology/index.md
git commit -m "docs: remove ontology landing page"
```

Expected:
- A new commit is created removing only `wiki/ontology/index.md`

### Task 3: Verify the documentation graph still works

**Files:**
- Verify: `wiki/index.md`
- Verify: `wiki/ontology/graph-standard.md`
- Verify: `wiki/ontology/index.md` (deleted)
- Verify: `scripts/lint_graph.py`

- [ ] **Step 1: Search the whole repository for live references to the deleted ontology index page**

Run:

```bash
grep -R -n "\[\[ontology/index\|wiki/ontology/index.md" .
```

Expected:
- Matches may remain in `docs/superpowers/specs/` or `docs/superpowers/plans/` as historical design records
- No matches under `wiki/` or `CLAUDE.md`

- [ ] **Step 2: Run the graph lint script**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Output begins with `PASS: graph lint succeeded`

- [ ] **Step 3: Inspect the final ontology entry points**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
index_text = Path('wiki/index.md').read_text()
graph_text = Path('wiki/ontology/graph-standard.md').read_text()
assert '[[ontology/index|ontology]]' not in index_text
assert index_text.count('[[graph-standard|ontology]]') == 3
assert '## 相关关系账本' in graph_text
for link in ['[[task_method_map]]', '[[evidence_index]]', '[[citation_graph]]', '[[method_evolution]]', '[[concept_links]]']:
    assert link in graph_text, link
print('PASS: ontology entry points consolidated into graph-standard')
PY
```

Expected:
- `PASS: ontology entry points consolidated into graph-standard`

- [ ] **Step 4: Review the final diff**

Run:

```bash
git diff HEAD~2..HEAD -- wiki/index.md wiki/ontology/graph-standard.md wiki/ontology/index.md
```

Expected:
- The diff shows three link replacements in `wiki/index.md`
- The diff shows a short relation-ledger block added near the top of `wiki/ontology/graph-standard.md`
- The diff shows deletion of `wiki/ontology/index.md`

- [ ] **Step 5: Commit any final verification-only adjustments if needed**

If Steps 1-4 require no further edits, do not create another commit.

If a small follow-up edit is required, run:

```bash
git add wiki/index.md wiki/ontology/graph-standard.md
git commit -m "docs: fix ontology navigation cleanup"
```

Expected:
- No commit if verification passes without changes
- Otherwise, one small follow-up commit containing only the correction
