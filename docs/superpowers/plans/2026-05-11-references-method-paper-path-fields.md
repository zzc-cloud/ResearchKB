# references_method Paper Path Fields Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `source_paper_path` and `target_paper_path` to `references_method` ledger instances, and synchronize the schema truth across the relation ledger, graph standard, skill contracts, lint rules, and regression tests.

**Architecture:** Treat `ontology/relations/references_method.md` and `ontology/graph-standard.md` as schema truth, then update the relation-reconciliation skill contract and checklists to match that truth. Finally, extend `scripts/lint_graph.py` to enforce the new child-field contract and update regression tests to lock the new format in place.

**Tech Stack:** Obsidian Markdown, Python (`unittest`, `pathlib`, `re`), ResearchKB skill docs and JSON eval fixtures

---

## File map and responsibilities

### Schema truth
- Modify: `ontology/relations/references_method.md`
  - Canonical `references_method` relation examples and live ledger instances.
- Modify: `ontology/graph-standard.md`
  - Normative contract for what `references_method` ledger instances must contain.

### Skill-contract synchronization
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Canonical child-field rendering rules for relation ledger output.
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Regression contract asserting canonical child-field order.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Checklist wording if it explicitly enumerates canonical ledger child fields.
- Inspect only unless needed: `.claude/skills/page-projection-sync/SKILL.md`
  - Confirm no direct consumption changes are required.

### Enforcement and regression coverage
- Modify: `scripts/lint_graph.py`
  - Child-field order constant and `references_method`-specific paper-path validation.
- Modify: `scripts/test_method_relation_pipeline.py`
  - Regression checks for docs, skill contract, and live PathMind examples.

### Design and plan references
- Reference: `docs/superpowers/specs/2026-05-11-references-method-paper-path-fields-design.md`
- This plan: `docs/superpowers/plans/2026-05-11-references-method-paper-path-fields.md`

## Implementation order

1. Update schema truth in the relation ledger and graph standard.
2. Synchronize skill contracts and regression samples to that schema.
3. Update lint enforcement to require the new child fields only for `references_method`.
4. Update Python regression tests to cover schema truth, skill truth, and the live examples.
5. Run targeted tests and lint.

This order keeps every downstream contract aligned to the normative source before enforcement is tightened.

## Key validation points

- `references_method` child-field order becomes:
  1. `source_path`
  2. `target_path`
  3. `source_paper_path`
  4. `target_paper_path`
  5. `edge_semantics`
  6. `evidence`
  7. `evidence_link`
  8. `evidence_path`
- `source_paper_path` and `target_paper_path` must be plain paths, not wikilinks.
- Both paper paths must point to existing files under `ontology/entities/papers/` and end in `.md`.
- Only `references_method` should gain these paper-path requirements in this change.
- `page-projection-sync` should not be forced to consume or display these new fields; only checklist wording changes if it explicitly enumerates ledger child fields.

## Task 1: Update the references_method ledger truth

**Files:**
- Modify: `ontology/relations/references_method.md`
- Reference: `docs/superpowers/specs/2026-05-11-references-method-paper-path-fields-design.md`

- [ ] **Step 1: Read the current references_method ledger and identify every live instance that needs the two new paper paths**

Confirm that every existing `[[PathMind]] --references_method--> [[...]]` entry will need:

```md
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
```

and a target-specific paper path such as:

```md
  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md
```

Expected: all live `references_method` entries have the same source paper path and distinct target paper paths.

- [ ] **Step 2: Update the example block and all live instances in `ontology/relations/references_method.md`**

Insert the two new lines between `target_path` and `edge_semantics` for every instance.

Target shape:

```md
- [[PathMind]] --references_method--> [[GNN-RAG]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/GNN-RAG.md
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
```

Repeat the same structural insertion for `RoG`, `GCR`, `EPERM`, and `ToG` with their correct paper paths.

- [ ] **Step 3: Verify the ledger is internally consistent before touching any downstream contract**

Manual checklist:
- No new wikilinks appear in `source_paper_path` or `target_paper_path`
- Every instance uses the same child-field order
- No relation main lines change

Expected: `ontology/relations/references_method.md` is the new schema example and live truth.

- [ ] **Step 4: Commit the schema-ledger update**

```bash
git add ontology/relations/references_method.md
git commit -m "feat: add paper paths to references_method ledger"
```

## Task 2: Update the normative graph standard

**Files:**
- Modify: `ontology/graph-standard.md`
- Reference: `ontology/relations/references_method.md`

- [ ] **Step 1: Add the `references_method` paper-path contract to the graph standard**

Update the `references_method` relation description so the normative text explicitly says the ledger instance must include:

```md
- `source_paper_path`：该 `references_method` 实例边所抽取自的 source paper 路径
- `target_paper_path`：该 `references_method` 的 target method 所对应的代表 / 参考论文路径
```

Also state that these are provenance anchors and do not change the ontology type from `Method -> Method`.

- [ ] **Step 2: Keep the wording scoped to references_method only**

Do **not** generalize this into a rule for all relation ledgers. The text should remain specific so `based_on`, `evaluated_on`, and other ledgers are unaffected.

Expected: the standard documents this as a `references_method`-specific contract extension.

- [ ] **Step 3: Review the surrounding section for contradictions**

Check that the updated standard still agrees with:
- `references_method` as weak method adjacency
- no impact on `parent_methods` / `child_methods`
- ledger truth vs projection truth separation

Expected: no accidental widening of semantics.

- [ ] **Step 4: Commit the graph-standard update**

```bash
git add ontology/graph-standard.md
git commit -m "docs: define references_method paper path contract"
```

## Task 3: Synchronize skill contracts and eval fixtures

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify if needed: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Inspect: `.claude/skills/page-projection-sync/SKILL.md`

- [ ] **Step 1: Update relation-reconciliation’s canonical child-field order**

In `.claude/skills/relation-reconciliation/SKILL.md`, replace the current canonical child-field list:

```md
- `source_path: ...`
- `target_path: ...`
- `edge_semantics: ...`
- `evidence: ...`
- `evidence_link: [[...]]`
- `evidence_path: ...`
```

with the `references_method`-aware contract:

```md
- `source_path: ...`
- `target_path: ...`
- `source_paper_path: ...`（仅 `references_method` 必填）
- `target_paper_path: ...`（仅 `references_method` 必填）
- `edge_semantics: ...`
- `evidence: ...`
- `evidence_link: [[...]]`
- `evidence_path: ...`
```

Make the wording explicit that the paper-path fields are specific to `references_method`, not global to every relation type.

- [ ] **Step 2: Update the regression sample contract**

In `.claude/skills/relation-reconciliation/evals/regression-samples.json`, change the quality check string that currently expects:

```json
"must write ledger child fields in canonical order: source_path, target_path, edge_semantics, evidence, evidence_link, evidence_path"
```

to a `references_method`-specific expectation such as:

```json
"must write references_method ledger child fields in canonical order: source_path, target_path, source_paper_path, target_paper_path, edge_semantics, evidence, evidence_link, evidence_path"
```

Preserve the other quality checks unchanged.

- [ ] **Step 3: Update the page-projection checklist only if it names the old canonical child set**

If `.claude/skills/page-projection-sync/evals/quality-checklist.md` still says the ledger contains only:

```md
source_path / target_path / evidence / evidence_link / evidence_path
```

expand that wording so it no longer contradicts the new `references_method` contract. Keep the statement scoped to “can read canonical ledger records, including relation-specific child fields such as `source_paper_path` / `target_paper_path` for `references_method`”.

Do **not** add a requirement for projection to display those fields.

- [ ] **Step 4: Confirm page-projection-sync skill text itself needs no behavioral change**

Review `.claude/skills/page-projection-sync/SKILL.md` and leave it unchanged unless it explicitly hardcodes the old child-field set. Since it consumes formal truth rather than rendering paper-path provenance, the expected outcome is likely **no file change** here.

Expected: skill behavior stays the same; only contracts/checklists stop contradicting the ledger truth.

- [ ] **Step 5: Commit the skill-contract sync**

```bash
git add .claude/skills/relation-reconciliation/SKILL.md .claude/skills/relation-reconciliation/evals/regression-samples.json .claude/skills/page-projection-sync/evals/quality-checklist.md
git commit -m "docs: sync skill contracts for references_method paper paths"
```

If the checklist file is unchanged, omit it from `git add`.

## Task 4: Tighten lint enforcement for references_method paper paths

**Files:**
- Modify: `scripts/lint_graph.py`
- Reference: `ontology/relations/references_method.md`

- [ ] **Step 1: Update the canonical field-order constant**

Change `RELATION_CHILD_FIELD_ORDER` from:

```python
RELATION_CHILD_FIELD_ORDER = [
    'source_path',
    'target_path',
    'edge_semantics',
    'evidence',
    'evidence_link',
    'evidence_path',
]
```

to a base-plus-variant structure so only `references_method` requires the two new fields. For example:

```python
BASE_RELATION_CHILD_FIELD_ORDER = [
    'source_path',
    'target_path',
    'edge_semantics',
    'evidence',
    'evidence_link',
    'evidence_path',
]

REFERENCES_METHOD_CHILD_FIELD_ORDER = [
    'source_path',
    'target_path',
    'source_paper_path',
    'target_paper_path',
    'edge_semantics',
    'evidence',
    'evidence_link',
    'evidence_path',
]
```

This avoids unintentionally forcing all relation ledgers to adopt the paper-path fields.

- [ ] **Step 2: Update `validate_relation_ledger()` to choose the expected order by relation type**

Inside `validate_relation_ledger()`, derive the expected field list from `record['rel']`:

```python
expected_field_order = (
    REFERENCES_METHOD_CHILD_FIELD_ORDER
    if record['rel'] == 'references_method'
    else BASE_RELATION_CHILD_FIELD_ORDER
)
```

Then compare:

```python
if field_names != expected_field_order:
    errors.append(f'invalid relation child-field order in {rel}')
    continue
```

- [ ] **Step 3: Keep wikilink rejection correct for the new path fields**

Extend the forbidden-wikilink list for `references_method` path fields so these values remain plain paths:

```python
for forbidden_field in forbidden_fields:
    if WIKILINK_RE.search(field_map[forbidden_field]):
        errors.append(...)
```

For `references_method`, `forbidden_fields` must include:

```python
['source_path', 'target_path', 'source_paper_path', 'target_paper_path', 'edge_semantics', 'evidence', 'evidence_path']
```

Keep `evidence_link` as the only allowed child-field wikilink.

- [ ] **Step 4: Add references_method-specific paper-path validation**

In `validate_relation_ledger()`, after building `field_map`, add minimal structural checks for `references_method`:

```python
if record['rel'] == 'references_method':
    for paper_field in ['source_paper_path', 'target_paper_path']:
        value = field_map[paper_field]
        if not value.startswith('ontology/entities/papers/') or not value.endswith('.md'):
            errors.append(f'invalid references_method paper path in {rel}: {value}')
            continue
        if not (ROOT / value).exists():
            errors.append(f'missing references_method paper path target in {rel}: {value}')
```

Do not add semantic checks about whether the paper proposes the method; only verify shape and existence.

- [ ] **Step 5: Re-run the lint logic mentally against non-references ledgers**

Confirm that:
- `cites`, `proposes`, `based_on`, `targets_task`, `evaluated_on`, `supported_by`, and `sourced_from` still use the old six-field contract
- only `references_method` opts into the eight-field contract

Expected: the lint change is additive and scoped.

- [ ] **Step 6: Commit the lint update**

```bash
git add scripts/lint_graph.py
git commit -m "feat: lint references_method paper path fields"
```

## Task 5: Update regression tests

**Files:**
- Modify: `scripts/test_method_relation_pipeline.py`
- Test: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Add failing assertions for the new schema truth**

Extend the existing tests that read:
- `ontology/relations/references_method.md`
- `ontology/graph-standard.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/relation-reconciliation/evals/regression-samples.json`

Add concrete assertions such as:

```python
self.assertIn('source_paper_path', references_method)
self.assertIn('target_paper_path', references_method)
self.assertIn('source_paper_path', graph_standard)
self.assertIn('target_paper_path', graph_standard)
self.assertIn('source_paper_path', skill)
self.assertIn('target_paper_path', skill)
self.assertIn('must write references_method ledger child fields in canonical order', reconciliation_samples)
```

- [ ] **Step 2: Add a live-example regression around PathMind**

In the existing PathMind regression test, assert that at least one live entry contains the two new fields in the correct area, for example:

```python
self.assertIn(
    '  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md',
    references_method,
)
self.assertIn(
    '  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md',
    references_method,
)
```

- [ ] **Step 3: Add a regression for the checklist wording if that file changed**

If `.claude/skills/page-projection-sync/evals/quality-checklist.md` is updated, add an assertion matching its new wording, for example:

```python
projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
self.assertIn('source_paper_path', projection_checklist)
self.assertIn('target_paper_path', projection_checklist)
```

If the file is intentionally unchanged, do not add this assertion.

- [ ] **Step 4: Run the targeted test suite and verify failures are resolved**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline -v
```

Expected: all tests in `MethodRelationPipelineTests` pass.

- [ ] **Step 5: Commit the regression coverage**

```bash
git add scripts/test_method_relation_pipeline.py
git commit -m "test: cover references_method paper path contract"
```

## Task 6: Run final validation

**Files:**
- Validate modified files only

- [ ] **Step 1: Run graph lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: no errors.

- [ ] **Step 2: Re-run the targeted regression suite**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline -v
```

Expected: PASS for all `MethodRelationPipelineTests`.

- [ ] **Step 3: Inspect git diff for accidental spillover**

Run:

```bash
git diff -- ontology/relations/references_method.md ontology/graph-standard.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/relation-reconciliation/evals/regression-samples.json .claude/skills/page-projection-sync/evals/quality-checklist.md scripts/lint_graph.py scripts/test_method_relation_pipeline.py
```

Expected: only the planned schema, skill-contract, lint, and regression updates appear.

- [ ] **Step 4: Commit the final validation state if needed**

If validation required any final fixups, commit them with a message such as:

```bash
git add ontology/relations/references_method.md ontology/graph-standard.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/relation-reconciliation/evals/regression-samples.json .claude/skills/page-projection-sync/evals/quality-checklist.md scripts/lint_graph.py scripts/test_method_relation_pipeline.py
git commit -m "chore: finalize references_method paper path validation"
```

If no fixups were needed because prior task commits already cover the exact final state, skip this commit.

## Spec coverage check

- Schema truth in the relation ledger: covered by Task 1.
- Normative graph-standard update: covered by Task 2.
- relation-reconciliation skill contract and regression sample sync: covered by Task 3.
- page-projection checklist wording sync if needed: covered by Task 3.
- Lint order and `references_method` paper-path validation: covered by Task 4.
- Python regression coverage: covered by Task 5.
- Final verification commands: covered by Task 6.

## Notes for the implementer

- Treat `ontology/relations/references_method.md` and `ontology/graph-standard.md` as the schema truth. Skill docs and tests must conform to those files, not the other way around.
- Do not expand the paper-path requirement to other relation ledgers in this change.
- Do not make projection display changes for the new fields unless a contradiction in the checklist wording forces a documentation-only sync.
- Keep commits small and aligned to the task boundaries above.
