# Method Weak-Reference Relation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new formal relation type `references_method` for weak Method → Method comparison / borrowing / route-reference semantics while keeping `based_on` reserved for strong lineage semantics.

**Architecture:** Introduce `references_method` as a sibling of `based_on`, not its parent. The change lands in three layers: ontology norms (`ontology/graph-standard.md` and `CLAUDE.md`), formal truth storage (`ontology/relations/references_method.md` plus lint awareness), and pipeline/governance skill contracts (candidate extraction, reconciliation, projection, semantic review, serving review). Use PathMind → GCR / EPERM as the first concrete validation case.

**Tech Stack:** Markdown ontology docs, Claude skill docs, Python lint script, Python unittest regression suite, Bash, git

---

## File Structure

- Modify: `ontology/graph-standard.md`
  - Add the canonical definition and usage boundary for `references_method`.
- Modify: `CLAUDE.md`
  - Keep the repo’s top-level ontology cognition and formal relation entry list aligned with the new relation type.
- Create: `ontology/relations/references_method.md`
  - New formal ledger for Method → Method weak-reference edges.
- Modify: `scripts/lint_graph.py`
  - Treat `references_method.md` as a required relation ledger and enforce its presence in the pipeline contract.
  - Add regression tests for the new relation type, skill-contract mentions, and the PathMind validation case.
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Allow `references_method` in relation candidate output.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Route `references_method` candidates to the new ledger.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Project `references_method` into Method pages without touching `parent_methods` / `child_methods`.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Review `references_method` as a distinct semantic choice from `based_on` and `cites`.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Treat `references_method` as traversable formal adjacency without lineage implications.
- Modify: `ontology/entities/methods/PathMind.md`
  - Add projected `references_method` edges to GCR and EPERM while keeping `parent_methods: [RoG]`.
- Modify: `ontology/entities/methods/GCR.md`
  - Reflect the incoming weak-reference relation from PathMind.
- Modify: `ontology/entities/methods/EPERM.md`
  - Reflect the incoming weak-reference relation from PathMind.
- Modify: `ontology/relations/based_on.md`
  - Keep the strong-lineage case limited to PathMind → RoG.

No new pipeline stage. No change to `parent_methods` / `child_methods` derivation source.

### Task 1: Define `references_method` in the ontology norm layer

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Write the failing regression tests**

```python
    def test_graph_standard_defines_references_method_relation(self):
        text = (ROOT / 'ontology' / 'graph-standard.md').read_text(encoding='utf-8')
        self.assertIn('`references_method`：`[[Method]] --references_method--> [[Method]]`', text)
        self.assertIn('用于方法级比较、借鉴、路线参照', text)
        self.assertIn('不驱动 `parent_methods` / `child_methods`', text)

    def test_claude_md_lists_references_method_as_formal_relation(self):
        text = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('`references_method`', text)
        self.assertIn('方法级比较、借鉴与路线参照', text)
        self.assertIn('ontology/relations/references_method.md', text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
```

Expected: FAIL because neither `ontology/graph-standard.md` nor `CLAUDE.md` mention `references_method` yet.

- [ ] **Step 3: Update `ontology/graph-standard.md`**

In the relation-type section, add this exact bullet immediately after `based_on`:

```markdown
- `references_method`：`[[Method]] --references_method--> [[Method]]`；表示方法将另一方法作为关键比较对象、借鉴路线或方法参照。该关系不表示方法谱系继承，不驱动 `parent_methods` / `child_methods`；若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。
```

- [ ] **Step 4: Update `CLAUDE.md` ontology relation descriptions and entry list**

Add a new relation bullet in the “关系语义” section:

```markdown
- 方法弱关联关系：`references_method`
  - 表示方法级比较、借鉴与路线参照。
  - 它强于纯论文引用，弱于 `based_on` 的谱系继承语义。
  - 不驱动 `parent_methods` / `child_methods`。
```

And add a new formal relation entry line in the formal relation entry list:

```markdown
- references_method 入口（文档：`ontology/relations/references_method.md`）：[[ontology/relations/references_method]]
```

- [ ] **Step 5: Re-run the regression tests**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 6: Commit the norm-layer change**

```bash
git commit -m "feat: define references_method ontology relation"
```

### Task 2: Add the new formal ledger and teach lint about it

**Files:**
- Create: `ontology/relations/references_method.md`
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Write the failing regression tests**

```python
    def test_lint_graph_requires_references_method_ledger(self):
        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        self.assertIn('ontology/relations/references_method.md', text)

    def test_references_method_ledger_exists_with_expected_heading(self):
        path = ROOT / 'ontology' / 'relations' / 'references_method.md'
        self.assertTrue(path.exists(), 'references_method ledger should exist')
        text = path.read_text(encoding='utf-8')
        self.assertIn('## 关系语义说明', text)
        self.assertIn('## 实例边', text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
```

Expected: FAIL because the ledger file does not exist yet and lint does not require it.

- [ ] **Step 3: Create `ontology/relations/references_method.md`**

Write this exact file:

```markdown
## 关系语义说明
- `references_method` 表示某方法将另一方法作为关键比较对象、借鉴路线或方法参照。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系不表示方法谱系继承，因此不驱动 `parent_methods` / `child_methods`。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。

## 实例边
- 无
```

- [ ] **Step 4: Update `scripts/lint_graph.py` to require the new ledger**

Add `ontology/relations/references_method.md` everywhere the existing relation ledgers are enumerated:

```python
REQUIRED_FILES = [
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/uses_concept.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
]
```

and:

```python
RELATION_LEDGER_FILES = [
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/uses_concept.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
]
```

- [ ] **Step 5: Re-run the regression tests**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 6: Commit the ledger/lint change**

```bash
git commit -m "feat: add references_method formal ledger"
```

### Task 3: Update pipeline and governance skill contracts

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Write the failing regression tests**

```python
    def test_paper_ingest_contract_mentions_references_method_candidates(self):
        text = (ROOT / '.claude' / 'skills' / 'paper-ingest' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references_method', text)

    def test_relation_reconciliation_contract_routes_references_method(self):
        text = (ROOT / '.claude' / 'skills' / 'relation-reconciliation' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('ontology/relations/references_method.md', text)

    def test_page_projection_sync_mentions_references_method_without_parent_derivation(self):
        text = (ROOT / '.claude' / 'skills' / 'page-projection-sync' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references_method', text)
        self.assertIn('formal relation only', text)
        self.assertIn('parent_methods', text)

    def test_ontology_semantic_review_reads_references_method_ledger(self):
        text = (ROOT / '.claude' / 'skills' / 'ontology-semantic-review' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('ontology/relations/references_method.md', text)

    def test_serving_governance_review_treats_references_method_as_formal_neighbor(self):
        text = (ROOT / '.claude' / 'skills' / 'serving-governance-review' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references_method', text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
```

Expected: FAIL because the skills do not all mention the new relation yet.

- [ ] **Step 3: Update `paper-ingest` relation candidate examples**

In the structured relation output example, add `references_method` as a supported candidate bucket:

```yaml
relation_candidates:
  proposes: []
  based_on: []
  references_method: []
  uses_concept: []
  targets_task: []
  evaluated_on: []
  supported_by: []
  cites: []
  sourced_from: []
```

- [ ] **Step 4: Update `relation-reconciliation` routing instructions**

Add an explicit routing note:

```markdown
- `references_method` 候选必须写入 `ontology/relations/references_method.md`
- 若某方法间关系属于比较、借鉴、路线参照而非谱系继承，应优先落为 `references_method`，而不是 `based_on`
```

- [ ] **Step 5: Update `page-projection-sync` instructions**

Add an explicit rule:

```markdown
- `based_on` → formal relation + `parent_methods` / `child_methods` 强一致派生
- `references_method` → formal relation only，不写入 `parent_methods` / `child_methods`
```

- [ ] **Step 6: Update `ontology-semantic-review` required reading and decision guidance**

Add the new ledger to the “先阅读” list:

```markdown
- `ontology/relations/references_method.md`
```

And add this decision guidance:

```markdown
- 若方法间关系表达的是比较、借鉴或路线参照，而非严格谱系继承，应优先审查其是否应落为 `references_method`。
```

- [ ] **Step 7: Update `serving-governance-review` neighbor guidance**

Add a sentence in the traversal/neighbor section:

```markdown
- `references_method` 属于正式可遍历邻接，但不应被解释为谱系继承或父方法链。
```

- [ ] **Step 8: Re-run the regression tests**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 9: Commit the skill-contract change**

```bash
git commit -m "feat: route references_method through pipeline skills"
```

### Task 4: Apply the first validation case to PathMind / GCR / EPERM

**Files:**
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/methods/GCR.md`
- Modify: `ontology/entities/methods/EPERM.md`
- Modify: `ontology/relations/references_method.md`
- Modify: `ontology/relations/based_on.md`

- [ ] **Step 1: Write the failing regression test for the PathMind case**

```python
    def test_pathmind_uses_references_method_for_gcr_and_eperm(self):
        pathmind = (ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md').read_text(encoding='utf-8')
        refs_ledger = (ROOT / 'ontology' / 'relations' / 'references_method.md').read_text(encoding='utf-8')
        based_on_ledger = (ROOT / 'ontology' / 'relations' / 'based_on.md').read_text(encoding='utf-8')
        self.assertIn('`references_method`', pathmind)
        self.assertIn('[[PathMind]] --references_method--> [[GCR]]', refs_ledger)
        self.assertIn('[[PathMind]] --references_method--> [[EPERM]]', refs_ledger)
        self.assertNotIn('[[PathMind]] --based_on--> [[GCR]]', based_on_ledger)
        self.assertNotIn('[[PathMind]] --based_on--> [[EPERM]]', based_on_ledger)
        self.assertIn('parent_methods: [RoG]', pathmind)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
```

Expected: FAIL because PathMind does not yet use the new relation.

- [ ] **Step 3: Update `ontology/relations/references_method.md` with the first two edges**

Append these exact entries under `## 实例边`:

```markdown
- [[PathMind]] --references_method--> [[GCR]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/GCR.md
  - edge_semantics: PathMind 将 GCR 作为可靠路径生成路线的重要比较与借鉴对象。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind]] --references_method--> [[EPERM]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/EPERM.md
  - edge_semantics: PathMind 将 EPERM 作为 evidence-path 增强路线的重要比较与借鉴对象。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
```

- [ ] **Step 4: Update `ontology/entities/methods/PathMind.md`**

Add these projected outgoing relation items in `## Formal relations` after the RoG `based_on` item:

```markdown
- `references_method`：比较 / 借鉴方法（文档：`ontology/entities/methods/GCR.md`）：[[GCR]]
  - edge_semantics: PathMind 将 GCR 作为可靠路径生成路线的重要比较与借鉴对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
- `references_method`：比较 / 借鉴方法（文档：`ontology/entities/methods/EPERM.md`）：[[EPERM]]
  - edge_semantics: PathMind 将 EPERM 作为 evidence-path 增强路线的重要比较与借鉴对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
```

Do **not** change:

```yaml
parent_methods: [RoG]
```

- [ ] **Step 5: Update `ontology/entities/methods/GCR.md` and `EPERM.md`**

In each file, change the “与知识库现有内容的关系” line to this pattern:

```markdown
- 当前被 [[PathMind]] 作为关键比较、借鉴或路线参照方法引用。
```

And add an incoming projected relation item for PathMind in each file’s `## Formal relations` block:

```markdown
- `references_method`：引用该方法的方法（文档：`ontology/entities/methods/PathMind.md`）：[[PathMind]]
  - edge_semantics: PathMind 将当前方法作为关键比较、借鉴或路线参照对象。
  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 6: Keep `based_on` limited to RoG**

Ensure `ontology/relations/based_on.md` still contains only:

```markdown
- [[PathMind]] --based_on--> [[RoG]]
```

for the PathMind case, with no GCR / EPERM entries.

- [ ] **Step 7: Re-run the PathMind regression test**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 8: Commit the validation-case change**

```bash
git commit -m "feat: model weak method references for PathMind"
```

### Task 5: Run full verification

**Files:**
- Verify: `scripts/lint_graph.py`
- Verify: all files changed in Tasks 1-4

- [ ] **Step 1: Run the full unittest regression suite**

Run:

```bash
```

Expected: all tests pass.

- [ ] **Step 2: Run graph lint**

Run:

```bash
python3 ./scripts/lint_graph.py
```

Expected:

```text
PASS: graph lint succeeded
```

- [ ] **Step 3: Review the final diff for only the intended files**

Run:

```bash
```

Expected: only the relation-modeling changes described in this plan.

- [ ] **Step 4: Commit the final verification checkpoint**

```bash
git commit -m "feat: add references_method relation type"
```

## Spec Coverage Check

- Add a new formal relation type `references_method`: covered by Tasks 1-2.
- Keep `based_on` as strong lineage only: covered by Tasks 1 and 4.
- Add a new relation ledger: covered by Task 2.
- Update graph-standard and relevant pipeline/governance skills: covered by Tasks 1 and 3.
- Use PathMind / GCR / EPERM as the first validation case: covered by Task 4.
- Keep the change focused on relation modeling only: enforced by File Structure and Task 5 diff review.

## Placeholder Scan

- No `TODO`, `TBD`, or “similar to above” markers remain.
- Every changed file path is explicit.
- Every verification step includes the exact command and expected result.

## Type / Name Consistency Check

- The new relation name is consistently `references_method` everywhere.
- `based_on` remains the sole source for `parent_methods` / `child_methods` derivation in every task.
- PathMind / GCR / EPERM are used consistently as the first validation case across ledger, object pages, and tests.
