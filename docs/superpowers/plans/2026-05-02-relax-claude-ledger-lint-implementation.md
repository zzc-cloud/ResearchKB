# Relax CLAUDE Relation-Ledger Lint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `scripts/lint_graph.py` so `CLAUDE.md` is validated only as a workflow-level entry surface, while `wiki/ontology/graph-standard.md` remains the authoritative registry of relation-ledger ownership.

**Architecture:** This is a narrow lint-boundary change inside one Python script. The implementation rewrites the `CLAUDE.md` needle list to enforce ontology and relation entry guidance instead of concrete ledger filenames, then verifies that the repository still passes lint without relaxing any graph-standard, relation-ledger, or instance-edge checks.

**Tech Stack:** Python 3, Markdown, grep, git

---

## File structure

- `scripts/lint_graph.py` — repository lint script; adjust the `CLAUDE.md` invariants only
- `CLAUDE.md` — workflow guide used as a verification target only; do not edit
- `wiki/ontology/graph-standard.md` — authoritative registry for relation-ledger ownership; verify unchanged lint coverage only

### Task 1: Rewrite the `CLAUDE.md` lint boundary

**Files:**
- Modify: `scripts/lint_graph.py:201-208`
- Modify: `scripts/lint_graph.py:308-311`

- [ ] **Step 1: Replace the current `CLAUDE_NEEDLES` list**

Replace this block:

```python
CLAUDE_NEEDLES = [
    'tasks/',
    'benchmarks/',
    'wiki/ontology/',
    'task_method_map.md',
    'evidence_index.md',
    'python3 scripts/lint_graph.py',
]
```

with this block:

```python
CLAUDE_NEEDLES = [
    'tasks/',
    'benchmarks/',
    'wiki/ontology/',
    'wiki/relations/',
    'python3 scripts/lint_graph.py',
]
```

- [ ] **Step 2: Keep the `CLAUDE.md` enforcement loop unchanged**

After Step 1, confirm this block still exists exactly as:

```python
claude_text = read_text('CLAUDE.md')
for needle in CLAUDE_NEEDLES:
    if needle not in claude_text:
        errors.append(f'missing {needle} in CLAUDE.md')
```

This preserves the existing enforcement mechanism while changing only what it asks `CLAUDE.md` to prove.

- [ ] **Step 3: Verify the planned change in the diff**

Run:

```bash
git diff -- scripts/lint_graph.py
```

Expected:
- The diff removes `task_method_map.md` and `evidence_index.md` from `CLAUDE_NEEDLES`
- The diff adds `wiki/relations/` to `CLAUDE_NEEDLES`
- No other part of the file changes yet

- [ ] **Step 4: Commit the lint-boundary change**

Run:

```bash
git add scripts/lint_graph.py
git commit -m "refactor: relax CLAUDE relation ledger lint"
```

Expected:
- A new commit is created containing only `scripts/lint_graph.py`

### Task 2: Verify that graph-standard remains the authority

**Files:**
- Verify: `scripts/lint_graph.py:209-219`
- Verify: `wiki/ontology/graph-standard.md`

- [ ] **Step 1: Re-check the `GRAPH_STANDARD_NEEDLES` block**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('scripts/lint_graph.py').read_text()
start = text.index('GRAPH_STANDARD_NEEDLES = [')
end = text.index('INDEX_NEEDLES = [')
print(text[start:end])
assert '`wiki/relations/paper_method_links.md`：维护 `proposes`' in text
assert '`wiki/relations/benchmark_links.md`：维护 `evaluated_on`' in text
assert '`wiki/relations/evidence_index.md`：维护 `supported_by`' in text
assert '`wiki/relations/provenance_links.md`：维护 `sourced_from`' in text
PY
```

Expected:
- The `GRAPH_STANDARD_NEEDLES` block prints to stdout
- All assertions pass

- [ ] **Step 2: Verify relation-ledger content checks remain intact**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('scripts/lint_graph.py').read_text()
for needle in [
    "RELATION_LEDGER_NEEDLES = {",
    "wiki/relations/paper_method_links.md",
    "wiki/relations/benchmark_links.md",
    "wiki/relations/provenance_links.md",
    "sourced_from must live in wiki/relations/provenance_links.md, not wiki/relations/evidence_index.md",
]:
    assert needle in text, needle
print('PASS: relation-ledger validation remains intact')
PY
```

Expected:
- `PASS: relation-ledger validation remains intact`

- [ ] **Step 3: Review the script diff again**

Run:

```bash
git diff HEAD~1..HEAD -- scripts/lint_graph.py
```

Expected:
- The committed diff changes only the `CLAUDE_NEEDLES` list
- The committed diff does not touch `GRAPH_STANDARD_NEEDLES`, `RELATION_LEDGER_NEEDLES`, or the sourced-from placement check

### Task 3: Run end-to-end lint verification

**Files:**
- Verify: `scripts/lint_graph.py`
- Verify: `CLAUDE.md`
- Verify: `wiki/ontology/graph-standard.md`

- [ ] **Step 1: Run the repository lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Output begins with `PASS: graph lint succeeded`

- [ ] **Step 2: Prove the new boundary semantically**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
script = Path('scripts/lint_graph.py').read_text()
claude = Path('CLAUDE.md').read_text()
assert 'task_method_map.md' not in script.split('CLAUDE_NEEDLES = [', 1)[1].split(']', 1)[0]
assert 'evidence_index.md' not in script.split('CLAUDE_NEEDLES = [', 1)[1].split(']', 1)[0]
for needle in ['wiki/ontology/', 'wiki/relations/', 'python3 scripts/lint_graph.py']:
    assert needle in claude, needle
print('PASS: CLAUDE lint now checks workflow-level entry guidance only')
PY
```

Expected:
- `PASS: CLAUDE lint now checks workflow-level entry guidance only`

- [ ] **Step 3: Review final status**

Run:

```bash
git status --short
```

Expected:
- No new changes from this task beyond any pre-existing unrelated working-tree modifications
- `scripts/lint_graph.py` is clean because it is already committed

- [ ] **Step 4: Do not create a follow-up commit unless verification requires a fix**

If all prior steps pass, stop here.

If verification exposes a small issue in `scripts/lint_graph.py`, fix it and run:

```bash
git add scripts/lint_graph.py
git commit -m "fix: tighten CLAUDE lint boundary"
```

Expected:
- No extra commit if verification passes cleanly
- Otherwise, one small follow-up commit containing only the fix
