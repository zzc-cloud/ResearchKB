# Ontology Semantic Review Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an `ontology-semantic-review` skill that reviews post-ingest git diffs against the ResearchKB ontology and knowledge graph, catching semantic misclassification and bad relations that structure lint cannot detect.

**Architecture:** Add a new dedicated skill under `.claude/skills/ontology-semantic-review/` with a focused SKILL.md, a reusable review prompt resource, and a small eval set. The skill will consume git diff plus ontology/relations context, output a structured semantic review report, and integrate after `paper-ingest` + `lint_graph.py` as the semantic governance layer.

**Tech Stack:** Markdown skill files, JSON eval files, ResearchKB ontology docs, git diff, Claude Code skills

---

## File map

### New skill files
- Create: `.claude/skills/ontology-semantic-review/SKILL.md`
- Create: `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- Create: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Create: `.claude/skills/ontology-semantic-review/evals/evals.json`
- Create: `.claude/skills/ontology-semantic-review/evals/quality-checklist.md`

### Existing project files to update
- Modify: `CLAUDE.md`
- Modify: `docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`

### Existing files to reference and reuse
- Reuse: `wiki/ontology/graph-standard.md`
- Reuse: `wiki/relations/citation_graph.md`
- Reuse: `wiki/relations/method_evolution.md`
- Reuse: `wiki/relations/concept_links.md`
- Reuse: `wiki/relations/task_method_map.md`
- Reuse: `wiki/relations/evidence_index.md`
- Reuse: `scripts/lint_graph.py`
- Reuse samples: PathMind and CPD Survey pages/caches already in the repo

---

### Task 1: Create the new skill skeleton and trigger contract

**Files:**
- Create: `.claude/skills/ontology-semantic-review/SKILL.md`
- Create: `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- Create: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`

- [ ] **Step 1: Write the failing trigger/structure test concept**

Use this manual failing check as the first red step:

```bash
ls .claude/skills/ontology-semantic-review/SKILL.md
```

Expected before implementation: `No such file or directory`

- [ ] **Step 2: Run the missing-file check to verify RED**

Run:

```bash
ls .claude/skills/ontology-semantic-review/SKILL.md
```

Expected: shell failure because the skill does not yet exist.

- [ ] **Step 3: Write minimal `SKILL.md`**

Create this file content:

```md
---
name: ontology-semantic-review
description: Review newly ingested or recently modified ResearchKB knowledge-graph content for semantic correctness after paper-ingest and after scripts/lint_graph.py passes. Use this whenever the user asks to review whether newly added papers, concepts, frameworks, tasks, scenarios, or relations are placed correctly in the ontology, whether a git diff introduced bad entity classifications or bad relation placement, or whether an ingest result is semantically reasonable even though the structure is valid. This skill is for post-ingest ontology/knowledge-graph governance, not for PDF extraction or basic linting.
---

# Ontology Semantic Review

## Purpose
Use this skill after `paper-ingest` and after `python3 scripts/lint_graph.py` passes. Your job is to review semantic correctness, not structural existence.

## Read first
- `wiki/ontology/graph-standard.md`
- `wiki/relations/citation_graph.md`
- `wiki/relations/method_evolution.md`
- `wiki/relations/concept_links.md`
- `wiki/relations/task_method_map.md`
- `wiki/relations/evidence_index.md`
- `references/review-output-template.md`
- `references/review-scope-rules.md`

## Inputs
Review using:
1. the current git diff or modified file list
2. the ontology and relation files above
3. the specific changed wiki/intermediate pages

## Review focus
Check:
- entity classification correctness
- relation placement correctness
- ontology position correctness
- consistency with existing graph
- duplicate / conflicting / pseudo-relations

Do not rewrite the ontology yourself. Output a structured review report with the exact template in `references/review-output-template.md`.
```

- [ ] **Step 4: Write the output template reference**

Create `.claude/skills/ontology-semantic-review/references/review-output-template.md`:

```md
# Semantic Review Report

## Overall verdict
- pass / pass-with-issues / fail

## High-priority issues
- ...

## Medium-priority issues
- ...

## Low-priority issues
- ...

## Suggested fixes
- point to concrete files and minimal changes

## Good decisions in this change
- ...

## Final recommendation
- accept / revise-then-accept / reject
```

- [ ] **Step 5: Write the scope rules reference**

Create `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`:

```md
## Scope rules
- Review only nodes and relations touched by the current change.
- Do not restate the whole ontology.
- Structural validity is assumed to be checked by `scripts/lint_graph.py` first.
- Focus on semantic errors such as:
  - survey as task
  - framework as method
  - concept-to-paper relation placed inside concept graph
  - citation relation placed in method evolution
  - duplicate or conflicting node identity

## Classification guidance
- Paper: a publication artifact
- Method: a reusable technical approach
- Concept: a stable semantic unit
- Framework: a layered or role-based organizing structure
- Task: a problem to solve, not a paper type
- Scenario: a domain or application context
- Benchmark: a dataset/evaluation target
- Evidence: a support cache, not a domain node
```

- [ ] **Step 6: Verify GREEN**

Run:

```bash
ls .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/review-output-template.md .claude/skills/ontology-semantic-review/references/review-scope-rules.md
```

Expected: all three files listed successfully.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/review-output-template.md .claude/skills/ontology-semantic-review/references/review-scope-rules.md
git commit -m "feat: add ontology semantic review skill skeleton"
```

---

### Task 2: Integrate the skill into the documented workflow

**Files:**
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md`

- [ ] **Step 1: Write the failing workflow-presence check**

Run:

```bash
grep -n "ontology-semantic-review" CLAUDE.md .claude/skills/paper-ingest/SKILL.md docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md
```

Expected before implementation: no matches or incomplete matches.

- [ ] **Step 2: Add workflow hook to `CLAUDE.md`**

Add this guidance under the single-paper processing workflow after graph lint and before git submission:

```md
**Step 8 — 语义审查（新增）**
- 在 `python3 scripts/lint_graph.py` 通过后，调用 `ontology-semantic-review` skill。
- 它负责审查本次 ingest 的实体分类、关系放置与全局本体位置是否合理。
- 若审查结论为 `revise-then-accept` 或 `reject`，先修正再提交 git。
```

- [ ] **Step 3: Add invocation guidance to `paper-ingest` skill**

Add a short section near the end of `.claude/skills/paper-ingest/SKILL.md`:

```md
## Ingest 完成后的治理建议
当本次摄入已经完成缓存、wiki 页面与关系更新后：
1. 先运行 `python3 scripts/lint_graph.py`
2. 若通过，再调用 `ontology-semantic-review` skill 审查语义合理性
3. 只有结构与语义都合理时，才建议接受本次变更并进入 git 提交
```

- [ ] **Step 4: Add one implementation note to the design doc**

Append a short note to the spec saying the implementation will integrate the skill after `paper-ingest` and after `lint_graph.py` in the normal workflow.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
grep -n "ontology-semantic-review" CLAUDE.md .claude/skills/paper-ingest/SKILL.md docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md
```

Expected: all three files show matching lines.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md .claude/skills/paper-ingest/SKILL.md docs/superpowers/specs/2026-05-01-ontology-semantic-review-design.md
git commit -m "docs: wire semantic review into ingest workflow"
```

---

### Task 3: Create the first eval set for the new skill

**Files:**
- Create: `.claude/skills/ontology-semantic-review/evals/evals.json`
- Create: `.claude/skills/ontology-semantic-review/evals/quality-checklist.md`

- [ ] **Step 1: Write the failing eval-file existence check**

Run:

```bash
ls .claude/skills/ontology-semantic-review/evals/evals.json .claude/skills/ontology-semantic-review/evals/quality-checklist.md
```

Expected before implementation: missing file failure.

- [ ] **Step 2: Create the eval set**

Write `.claude/skills/ontology-semantic-review/evals/evals.json` with these three prompts:

```json
{
  "skill_name": "ontology-semantic-review",
  "evals": [
    {
      "id": 1,
      "prompt": "请审查本次 PathMind ingest 的 git diff，判断新增的概念、关系和方法演化位置是否合理，尤其看 concept_links 和 method_evolution 的关系边界。",
      "expected_output": "输出结构化语义审查报告，指出 PathMind 主线中的关系是否放对位置，并给出 accept / revise-then-accept / reject。",
      "files": []
    },
    {
      "id": 2,
      "prompt": "请审查这次 complex product design survey ingest 的改动，重点判断 survey 是否被误当作 task、framework 是否被放对位置、analysis.md 的使用是否合理。",
      "expected_output": "输出结构化语义审查报告，能识别 survey/task 混淆与 framework 落点合理性。",
      "files": []
    },
    {
      "id": 3,
      "prompt": "请根据当前 git diff 检查新增的概念关系是否有概念→论文这类不该放进 concept_links 的关系，并指出最小修正方案。",
      "expected_output": "输出结构化语义审查报告，明确指出 concept_links 中不合理的概念→论文关系并建议迁移位置。",
      "files": []
    }
  ]
}
```

- [ ] **Step 3: Create the quality checklist**

Write `.claude/skills/ontology-semantic-review/evals/quality-checklist.md`:

```md
# Ontology Semantic Review Quality Checklist

## Core expectations
- Reports only on changed nodes/relations
- Distinguishes structural issues from semantic issues
- Identifies misclassified nodes
- Identifies wrong relation-file placement
- Gives minimal concrete fixes
- Produces a final recommendation

## Key failure patterns
- survey treated as task
- framework treated as method
- concept-to-paper support relation inside concept graph
- citation support relation inside method evolution
- duplicate semantic identity across multiple node types
```

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import json
base = Path('.claude/skills/ontology-semantic-review/evals')
obj = json.loads((base / 'evals.json').read_text())
assert obj['skill_name'] == 'ontology-semantic-review'
assert len(obj['evals']) == 3
text = (base / 'quality-checklist.md').read_text()
assert 'survey treated as task' in text
print('PASS: ontology-semantic-review eval assets valid')
PY
```

Expected: `PASS: ontology-semantic-review eval assets valid`

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/ontology-semantic-review/evals/evals.json .claude/skills/ontology-semantic-review/evals/quality-checklist.md
git commit -m "test: add semantic review eval set"
```

---

### Task 4: Add a reusable review runner prompt for diff-based checks

**Files:**
- Create: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

- [ ] **Step 1: Write the failing existence check**

Run:

```bash
ls .claude/skills/ontology-semantic-review/references/diff-review-playbook.md
```

Expected before implementation: missing file failure.

- [ ] **Step 2: Create the playbook**

Write this file:

```md
## Diff review playbook
1. Read the current git diff or changed file list.
2. Read `wiki/ontology/graph-standard.md` and the relation hub files.
3. Classify every changed node touched by the diff.
4. For every changed relation, ask:
   - Is this relation real?
   - Is it in the correct relation file?
   - Is it local evidence support rather than ontology-level structure?
5. Produce the standard review report.

## Special checks
- If a survey is represented as a task, flag it.
- If a framework is represented as a method, flag it.
- If concept_links contains concept→paper support edges, flag and suggest moving to concept page or evidence index.
- If method_evolution contains literature support rather than actual lineage, flag it.
```

- [ ] **Step 3: Update `SKILL.md` to reference the playbook**

Add one line under the “Read first” list:

```md
- `references/diff-review-playbook.md`
```

- [ ] **Step 4: Verify GREEN**

Run:

```bash
grep -n "diff-review-playbook" .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/diff-review-playbook.md
```

Expected: matches in both files.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/diff-review-playbook.md
git commit -m "docs: add diff review playbook for semantic review skill"
```

---

### Task 5: Run a first manual verification loop for the skill definition

**Files:**
- Review only; no new files required beyond those above

- [ ] **Step 1: Sanity-check the skill bundle exists**

Run:

```bash
find .claude/skills/ontology-semantic-review -maxdepth 3 -type f | sort
```

Expected files include:
- `SKILL.md`
- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`
- `evals/evals.json`
- `evals/quality-checklist.md`

- [ ] **Step 2: Re-run graph lint to ensure no collateral breakage**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Review the new skill for line-of-duty coherence**

Manually verify:
- trigger description matches actual use
- inputs are diff + ontology files, not PDF
- output is report-only, not auto-editing
- PathMind and CPD Survey are explicitly supported in evals

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/ontology-semantic-review
git commit -m "feat: add ontology semantic review governance skill"
```

---

## Self-review

### Spec coverage
- New skill identity and trigger behavior: covered in Task 1
- Structured report format: covered in Task 1
- Integration after `paper-ingest` and `lint_graph.py`: covered in Task 2
- Test prompts using PathMind and CPD Survey: covered in Task 3
- Diff-scoped semantic review playbook: covered in Task 4

### Placeholder scan
- No TODO/TBD placeholders remain.
- Every created/modified file path is explicit.
- Commands and expected outcomes are concrete.

### Type consistency
- Skill name is consistently `ontology-semantic-review`
- Output artifact names and reference filenames are consistent across tasks
- PathMind and CPD Survey are consistently used as validation examples

---

Plan complete and saved to `docs/superpowers/plans/2026-05-01-ontology-semantic-review-implementation.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
