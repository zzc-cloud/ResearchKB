# Supported By Evidence Exception Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `supported_by` a strict relation-type exception so its ledger entries never include `- evidence:`, while all other formal relation types still require explicit `- evidence:` and the full compile/governance pipeline stays aligned.

**Architecture:** First lock the new rule in `scripts/test_lint_graph.py` with regression tests proving that `supported_by` must omit `- evidence:` and non-`supported_by` ledgers still require it. Then update the normative rule in `ontology/graph-standard.md`, rewrite the live `supported_by` ledger examples, and align the skill contracts (`paper-ingest`, `relation-reconciliation`, `page-projection-sync`, governance skills/evals) so generation and review use the same exception. Finally, add the structural lint checks that enforce the exception and run full verification.

**Tech Stack:** Obsidian-flavored Markdown under `ontology/` and `.claude/skills/`, Python 3 `unittest` and repository linting in `scripts/lint_graph.py`, relation ledgers in `ontology/relations/`, skill eval checklists and regression JSON fixtures.

---

## File map

### Normative rule surface
- Modify: `ontology/graph-standard.md`
  - Change the generic formal-edge evidence rule so `supported_by` becomes the only no-`evidence` exception.
- Modify: `ontology/relations/supported_by.md`
  - Remove duplicated `- evidence:` lines from all `supported_by` examples.

### Generation-stage skill contracts
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - State that `supported_by` candidates do not carry a repeated `evidence` field because the target Evidence object is the support anchor.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Enforce `supported_by`: `reason` required, `evidence` forbidden; everything else still requires `evidence`.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - State that `supported_by` ledger entries are consumed from source, target, and reason only.

### Governance and review contracts
- Modify: `scripts/lint_graph.py`
  - Add ledger-level validation: `supported_by` entries must not contain `- evidence:`; other relation ledgers still require it.
- Modify: `scripts/test_lint_graph.py`
  - Add failing tests first for the new ledger exception and preserve the existing index/projection regressions.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Add review guidance that missing `evidence` on `supported_by` is correct, but duplicated `evidence` is outdated formatting.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Add prompts to flag duplicated `evidence` on `supported_by` and missing `evidence` on non-`supported_by` ledgers.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - State that the new `supported_by` truth surface is expected and not a serving defect.

### Supporting eval/checklist assets
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Add checks that `supported_by` output omits `evidence` while other relations retain it.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Clarify that `supported_by` projections rely on target Evidence and reason, not a ledger `evidence` field.

### Verification surface
- Test: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_supported_by_evidence_lines scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_evidence_on_non_supported_by_ledgers -v`
- Test: `python3 -m unittest scripts.test_lint_graph -v`
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Lock the `supported_by` exception in tests

**Files:**
- Modify: `scripts/test_lint_graph.py`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Add a failing regression test that forbids `- evidence:` inside `supported_by.md`**

Insert this method above `test_lint_graph_requires_index_entry_target_files_to_exist` in `scripts/test_lint_graph.py`:

```python
    def test_lint_graph_rejects_supported_by_evidence_lines(self):
        supported_by_path = ROOT / 'ontology' / 'relations' / 'supported_by.md'
        original = supported_by_path.read_text(encoding='utf-8')

        broken = original.replace(
            '- `[[PathMind]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`\n  - reason: PathMind 方法定义与总体机制由 sections 证据页支撑。',
            '- `[[PathMind]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`\n  - reason: PathMind 方法定义与总体机制由 sections 证据页支撑。\n  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]',
            1,
        )
        supported_by_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            supported_by_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('supported_by entries must not include evidence field: ontology/relations/supported_by.md', combined_output)
```

- [ ] **Step 2: Add a failing regression test that preserves `- evidence:` requirements for other ledgers**

Insert this method directly below the previous one:

```python
    def test_lint_graph_requires_evidence_on_non_supported_by_ledgers(self):
        cites_path = ROOT / 'ontology' / 'relations' / 'cites.md'
        original = cites_path.read_text(encoding='utf-8')

        broken = original.replace(
            '  - evidence: [[../entities/evidence/PathMind.refs|PathMind.refs]]',
            '',
            1,
        )
        cites_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            cites_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('missing evidence field for relation entry in ontology/relations/cites.md', combined_output)
```

- [ ] **Step 3: Run the two new tests and verify they fail for the expected reason**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_supported_by_evidence_lines \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_evidence_on_non_supported_by_ledgers -v
```

Expected:
- `FAIL`
- The output shows that `scripts/lint_graph.py` does not yet distinguish `supported_by` from other ledgers for `evidence` enforcement.
- No syntax or import errors.

---

### Task 2: Update the normative rule and live `supported_by` ledger examples

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `ontology/relations/supported_by.md`
- Test: inspect changed markdown; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the generic evidence rule in `ontology/graph-standard.md` with the strict exception wording**

In `ontology/graph-standard.md`, replace this line under `### 4.5 实例边维护规则`:

```markdown
- 证据优先：每条正式实例边必须至少附带一个 `evidence`，无证据仅可用 `status: placeholder` 暂存。
```

with:

```markdown
- 证据优先：默认情况下，每条正式实例边必须至少附带一个 `evidence`；无证据仅可用 `status: placeholder` 暂存。
- `supported_by` 属于例外关系：其 target 必须为 Evidence 对象，且不再允许重复书写 `- evidence:`；该关系的支撑语义由 source、target Evidence 与 `reason` 三者共同构成。
```

- [ ] **Step 2: Update the serving-layer `Formal relations` wording so it no longer claims every relation line has `- evidence:`**

In `ontology/graph-standard.md`, replace this line under `### 5.3 Formal relations 区块规范`:

```markdown
- 每条关系至少附带一个 `- evidence: [[证据页]]` 行；必要时可补 `- note:`，但应避免 prose 污染区块。
```

with:

```markdown
- 默认情况下，每条关系至少附带一个 `- evidence: [[证据页]]` 行；`supported_by` 为例外，不再重复附带 `- evidence:`。必要时可补 `- note:`，但应避免 prose 污染区块。
```

- [ ] **Step 3: Remove duplicated `- evidence:` lines from every `supported_by` sample**

In `ontology/relations/supported_by.md`, delete every `- evidence:` line so the file uses this shape throughout:

```md
- `[[PathMind]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`
  - reason: PathMind 方法定义与总体机制由 sections 证据页支撑。
```

Specifically, remove the `- evidence:` line from all ten existing entries in the file.

- [ ] **Step 4: Run repository lint to expose only the missing structural enforcement next**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS` is possible if nothing else is broken, but the new TDD tests from Task 1 should still fail until lint enforcement is added.

---

### Task 3: Teach structural lint to enforce the `supported_by` exception

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Add a helper that validates ledger evidence-field rules by relation type**

Insert this helper below `validate_supported_by_contract` in `scripts/lint_graph.py`:

```python
def validate_relation_ledger_evidence_rules(errors: list[str]) -> None:
    for rel_path in [
        'ontology/relations/cites.md',
        'ontology/relations/proposes.md',
        'ontology/relations/based_on.md',
        'ontology/relations/targets_task.md',
        'ontology/relations/uses_concept.md',
        'ontology/relations/evaluated_on.md',
        'ontology/relations/supported_by.md',
        'ontology/relations/sourced_from.md',
    ]:
        text = read_text(rel_path)
        lines = text.splitlines()
        current_rel = None
        has_evidence = False
        for line in lines + ['- `[[SENTINEL]] --end--> [[SENTINEL]]`']:
            if match := FORMAL_RELATION_RE.match(line.strip()):
                if current_rel is not None:
                    if current_rel == 'supported_by' and has_evidence:
                        errors.append(f'supported_by entries must not include evidence field: {rel_path}')
                    if current_rel != 'supported_by' and not has_evidence:
                        errors.append(f'missing evidence field for relation entry in {rel_path}')
                current_rel = match.group('rel')
                has_evidence = False
                continue
            if current_rel is not None and line.strip().startswith('- evidence:'):
                has_evidence = True
```

- [ ] **Step 2: Wire the helper into the main lint run**

In `scripts/lint_graph.py`, directly after:

```python
validate_supported_by_contract(errors)
```

add:

```python
validate_relation_ledger_evidence_rules(errors)
```

- [ ] **Step 3: Re-run the two targeted regression tests**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_supported_by_evidence_lines \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_evidence_on_non_supported_by_ledgers -v
```

Expected:
- `OK`
- Both tests pass.

- [ ] **Step 4: Run the full unittest file and repository lint**

Run:

```bash
python3 -m unittest scripts.test_lint_graph -v
python3 scripts/lint_graph.py
```

Expected:
- unittest: `OK`
- lint: `PASS: graph lint succeeded`

---

### Task 4: Align generation-stage skills to the new `supported_by` truth model

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: inspect files; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Update `paper-ingest` so `supported_by` no longer implies a repeated evidence field**

In `.claude/skills/paper-ingest/SKILL.md`, append this bullet under the existing `补充约束：` block in `### Step 6: 汇总候选正式关系`:

```markdown
- `supported_by` 的支撑锚点已由 target Evidence 对象承担；不要为该关系再重复生成独立 `evidence` 字段描述。
```

- [ ] **Step 2: Make `relation-reconciliation` explicitly enforce the exception**

In `.claude/skills/relation-reconciliation/SKILL.md`, replace the current `supported_by` bullet block inside `补充约束：` with:

```markdown
- `supported_by` 只允许 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 作为 source。
- `supported_by` 的 target 必须是 Evidence 对象。
- `supported_by` 必须保留 `reason`，但不得重复写 `evidence`。
- 若候选关系试图把 `Paper` 作为 `supported_by` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
```

- [ ] **Step 3: Tell `page-projection-sync` not to depend on `supported_by` ledger `evidence` lines**

In `.claude/skills/page-projection-sync/SKILL.md`, append this bullet under `## Formal relations 投影格式`:

```markdown
- `supported_by` 投影只依赖 source、target Evidence 与 `reason`；不得假设 ledger 中存在重复的 `- evidence:` 行。
```

- [ ] **Step 4: Run lint after the generation-contract updates**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`

---

### Task 5: Align governance/review skills and eval checklists

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Expand ontology-semantic-review to treat duplicated `supported_by` evidence as outdated**

In `.claude/skills/ontology-semantic-review/SKILL.md`, add this bullet to `## 审查重点`:

```markdown
- `supported_by` 是否错误重复携带了 `evidence` 字段，或其他 relation 是否错误缺失 `evidence`
```

- [ ] **Step 2: Update semantic review reference rules**

Append this section to `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`:

```markdown
- `supported_by` 为 relation 实例格式例外：必须保留 `reason`，不得重复书写 `evidence`。
- 除 `supported_by` 外，其他正式 relation 实例仍必须显式保留 `evidence`。
```

Append this section to `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`:

```markdown
- 若 diff 修改了 `supported_by.md`，检查是否还保留重复的 `- evidence:` 行。
- 若 diff 修改了其他 relation ledger，检查是否误删了必需的 `- evidence:` 行。
```

- [ ] **Step 3: Update serving review to accept the new truth surface**

In `.claude/skills/serving-governance-review/SKILL.md`, append this bullet under `2. **Serving readability alignment**`:

```markdown
   - Do `supported_by`-driven pages remain readable without duplicated ledger `evidence` fields, relying instead on target Evidence objects and projected links?
```

- [ ] **Step 4: Update reconciliation and projection eval checklists**

Append these bullets to `.claude/skills/relation-reconciliation/evals/quality-checklist.md`:

```markdown
- [ ] `supported_by` 输出必须保留 `reason`，但不得重复写 `evidence`。
- [ ] 除 `supported_by` 外，其余 formal relation 输出仍必须显式包含 `evidence`。
```

Replace the `quality_checks` array in `.claude/skills/relation-reconciliation/evals/regression-samples.json` with:

```json
[
  "must classify existing ledger edges as already_present",
  "must add missing formal edges to the correct ledger file",
  "must preserve explicit relation exemptions",
  "must output affected_pages for page-projection-sync",
  "must reject or surface for review any Paper --supported_by--> Evidence candidate",
  "must omit evidence field on supported_by outputs while preserving reason"
]
```

Append this bullet to `.claude/skills/page-projection-sync/evals/quality-checklist.md`:

```markdown
- [ ] 不得假设 `supported_by` ledger 项包含 `evidence` 行；投影应仅依赖 target Evidence 与 reason。
```

- [ ] **Step 5: Run lint one final time**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`

---

### Task 6: Final verification and focused commit

**Files:**
- Test: `scripts/test_lint_graph.py`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the targeted `supported_by` exception tests**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_supported_by_evidence_lines \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_evidence_on_non_supported_by_ledgers -v
```

Expected:
- `OK`

- [ ] **Step 2: Run the full lint unittest suite**

Run:

```bash
python3 -m unittest scripts.test_lint_graph -v
```

Expected:
- `OK`

- [ ] **Step 3: Run repository lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`

- [ ] **Step 4: Commit only the files relevant to the `supported_by` evidence exception**

```bash
git add \
  ontology/graph-standard.md \
  ontology/relations/supported_by.md \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/ontology-semantic-review/SKILL.md \
  .claude/skills/ontology-semantic-review/references/review-scope-rules.md \
  .claude/skills/ontology-semantic-review/references/diff-review-playbook.md \
  .claude/skills/serving-governance-review/SKILL.md \
  .claude/skills/relation-reconciliation/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  scripts/lint_graph.py \
  scripts/test_lint_graph.py

git commit -m "refactor: remove redundant evidence from supported_by"
```

---

## Spec coverage self-check

- Core rule (`supported_by` no `evidence`, others still require it): Tasks 1-3
- Normative rule wording: Task 2
- Compile pipeline alignment (`paper-ingest`, `relation-reconciliation`, `page-projection-sync`): Task 4
- Structural governance hardening: Task 3
- Ontology semantic governance alignment: Task 5
- Serving governance alignment: Task 5
- Eval/checklist updates: Task 5
- Verification and focused delivery: Task 6

No uncovered spec requirement remains.
