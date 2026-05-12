# Paper Stub and Method Anchor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode Formal Paper vs Paper Stub semantics, enforce `references_method` → `cites` anchoring, and keep partial Method materialization valid without promoting cited placeholder papers into default serving.

**Architecture:** Update the ontology contract first in `ontology/graph-standard.md`, then align pipeline skills so reconciliation, projection, index sync, and serving governance all treat placeholder cited papers as non-serving paper stubs. Extend lint and regression tests so the new rules are executable: `references_method` edges with paper provenance must be backed by matching `cites`, partial Methods must have a paper anchor, and paper indexes must continue to keep stubs out of default serving entries.

**Tech Stack:** Markdown ontology specs, Claude skill contracts, JSON eval fixtures, Python lint script, Python unittest regression suite, Bash, git

---

## File Structure

- Modify: `ontology/graph-standard.md`
  - Add the Formal Paper vs Paper Stub / Anchor split.
  - Define the minimum paper-anchor rule for formal / partial Methods.
  - Define the hard requirement that `references_method` with `source_paper_path` and `target_paper_path` must be backed by a matching `cites` edge.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Require reconciliation to preserve paper stubs, enforce `references_method` → `cites` backing, and distinguish stub creation from Formal Paper promotion.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Keep placeholder paper pages synced as formal-bearing stubs without treating them as new paper neighbors or Formal Papers.
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Clarify that placeholder cited papers are Paper Stubs / Anchors and must stay in non-serving blocks.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Clarify that Paper Stubs / Anchors are legal phase-1 neighbors and should not be upgraded to default paper serving surfaces.
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Add quality checks for paper-stub preservation and `references_method` / `cites` anchoring.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Replace the outdated `target_paper` expectation with the current path-metadata projection rule and add a paper-stub check.
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Add or refine regression samples for placeholder target pages remaining non-serving paper stubs.
- Modify: `scripts/lint_graph.py`
  - Add direct validation that `references_method` edges with paper paths have a matching `cites` edge.
  - Add validation that partial / formal Methods have at least one paper anchor.
  - Keep placeholder papers legal as non-serving anchors rather than treating them as malformed Formal Papers.
- Modify: `scripts/test_method_relation_pipeline.py`
  - Add contract-level and lint-level regression tests for paper stubs, method anchors, and `references_method` / `cites` consistency.
- Verify only: `ontology/entities/papers/index.md`
  - Confirm the current non-serving placeholder block already matches the new paper-stub semantics before deciding whether any wording updates are needed later.

No new runtime modules. No new relation types. No object-page path migrations.

### Task 1: Lock the ontology contract in docs and tests

**Files:**
- Modify: `scripts/test_method_relation_pipeline.py`
- Verify: `docs/superpowers/specs/2026-05-12-paper-stub-and-method-anchor-design.md`
- Verify: `ontology/graph-standard.md`
- Verify: `.claude/skills/relation-reconciliation/SKILL.md`
- Verify: `.claude/skills/page-projection-sync/SKILL.md`
- Verify: `.claude/skills/index-sync/SKILL.md`
- Verify: `.claude/skills/serving-governance-review/SKILL.md`
- Verify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Verify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Verify: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Write the failing regression test**

Add this test method near the end of `scripts/test_method_relation_pipeline.py`, above the `if __name__ == '__main__':` block:

```python
    def test_paper_stub_and_method_anchor_contract_is_documented(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        reconciliation = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        index_sync = (ROOT / '.claude/skills/index-sync/SKILL.md').read_text(encoding='utf-8')
        serving = (ROOT / '.claude/skills/serving-governance-review/SKILL.md').read_text(encoding='utf-8')
        reconciliation_samples = (ROOT / '.claude/skills/relation-reconciliation/evals/regression-samples.json').read_text(encoding='utf-8')
        projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
        projection_samples = (ROOT / '.claude/skills/page-projection-sync/evals/regression-samples.json').read_text(encoding='utf-8')

        self.assertIn('Formal Paper 与 Paper Stub / Anchor', graph_standard)
        self.assertIn('每个 formal / partial `Method` 都必须至少能回挂到一个 paper anchor', graph_standard)
        self.assertIn('若一条 `references_method` 实例边同时声明 `source_paper_path` 与 `target_paper_path`，则 formal ledger 中必须存在对应 `cites`', graph_standard)
        self.assertIn('placeholder cited paper target 应保留为 Paper Stub / Anchor，而不是自动升级为 Formal Paper', reconciliation)
        self.assertIn('不得把 `source_paper_path` / `target_paper_path` 投影成新的 paper 邻接', projection)
        self.assertIn('`placeholder` Paper 只进入 non-serving block，并作为 Paper Stub / Anchor 理解', index_sync)
        self.assertIn('Paper Stub / Anchor 属于可合法遍历但非 default paper serving surface 的 phase-1 中间态', serving)
        self.assertIn('must preserve placeholder cited papers as Paper Stub / Anchor targets', reconciliation_samples)
        self.assertIn('must reject references_method provenance when the matching cites edge is missing', reconciliation_samples)
        self.assertIn('must keep placeholder cited-paper targets non-serving paper stubs', projection_samples)
        self.assertIn('Paper Stub / Anchor pages may bear formal relations without becoming Formal Paper entries', projection_checklist)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_paper_stub_and_method_anchor_contract_is_documented -v
```

Expected: FAIL because the new contract strings do not exist yet.

- [ ] **Step 3: Commit the failing-test scaffold**

```bash
git add scripts/test_method_relation_pipeline.py
git commit -m "test: add paper stub anchor regressions"
```

- [ ] **Step 4: Verify the commit landed**

Run:

```bash
git log --oneline -1
```

Expected: latest commit message is `test: add paper stub anchor regressions`.

### Task 2: Update the ontology and skill contracts

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Add the graph-standard contract text**

Insert these exact bullets into the Paper / Method / relation-contract sections of `ontology/graph-standard.md`:

```markdown
- Paper 分成两种层级：`Formal Paper` 与 `Paper Stub / Anchor`。
- `Formal Paper` 只有在该 paper 自身产出至少一种稳定 ontology payload 时才成立；仅有 citation target 身份不足以进入正式 Paper 对象层。
- `Paper Stub / Anchor` 仅承担 relation target、paper-level provenance 与 future ingest 升级落点职责；它不进入默认 paper serving surface。
- 每个 formal / partial `Method` 都必须至少能回挂到一个 paper anchor；允许的锚点包括 incoming `proposes`、`references_method` 中的 `source_paper_path` / `target_paper_path`，以及其他稳定 coverage provenance。
- 若一条 `references_method` 实例边同时声明 `source_paper_path` 与 `target_paper_path`，则 formal ledger 中必须存在对应 `[[source_paper]] --cites--> [[target_paper]]`；否则该边不得视为 fully valid formal edge。
- `cites` 与 `references_method` 不要求一一对应；`cites` 不新增镜像 `references_method_path` 字段。
```

- [ ] **Step 2: Add the reconciliation skill contract text**

Under the reconciliation rules in `.claude/skills/relation-reconciliation/SKILL.md`, add this exact block:

```markdown
- 对于 `references_method`：若实例边声明了 `source_paper_path` 与 `target_paper_path`，则必须同时验证 `ontology/relations/cites.md` 中存在对应 `Paper --cites--> Paper` 实例；否则归入 `needs_human_review`，不得直接落为 fully valid formal edge。
- `references_method` 的 target paper 若当前仅由 citation / provenance 需要支撑，应保留或创建为 `Paper Stub / Anchor`，而不是自动升级为 Formal Paper。
- partial `Method` 可以依赖 target paper stub 作为弱锚点；不得因为 target paper 尚未成为 Formal Paper 就回退已稳定的方法 identity。
- 仅有普通 related-work mention 时，可保留在 `cites` 并按需创建 paper stub，但不得自动 materialize 为 partial `Method`。
```

- [ ] **Step 3: Add the projection, index, and serving contract text**

Add this exact block to `.claude/skills/page-projection-sync/SKILL.md` near the `references_method` projection rules:

```markdown
- `references_method` 的 `source_paper_path` / `target_paper_path` 只作为 path metadata 投影；不得把它们升级成新的可点击 paper 邻接。
- placeholder cited-paper target 若承接 formal relation，应继续作为 non-serving `Paper Stub / Anchor` 投影，而不是按 Formal Paper 模板推升为默认 paper 入口。
```

Add this exact block to `.claude/skills/index-sync/SKILL.md` under 收录规则:

```markdown
- `placeholder` Paper 只进入 non-serving block，并作为 `Paper Stub / Anchor` 理解；它承担 relation / provenance 锚点职责，但不自动进入默认 paper serving 入口。
- cited-work placeholder paper 被后续正式 ingest 之前，应保持原路径并原地升级，而不是新建第二个 Formal Paper 页面。
```

Add this exact block to `.claude/skills/serving-governance-review/SKILL.md` under 问答可遍历性 or 输出状态:

```markdown
- `Paper Stub / Anchor` 属于可合法遍历但非 default paper serving surface 的 phase-1 中间态。
- 若某 Method / Evidence / Paper 页的关键 formal 邻居是 Paper Stub / Anchor，只要遍历链完整、状态暴露正确且未被错误提升为默认入口，不应仅因其不是 Formal Paper 就判为 serving 失败。
```

- [ ] **Step 4: Update the eval fixtures**

Append these exact checklist items to `.claude/skills/page-projection-sync/evals/quality-checklist.md`:

```markdown
- [ ] `references_method` paper-path metadata stays metadata and does not become new paper neighbors.
- [ ] Paper Stub / Anchor pages may bear formal relations without becoming Formal Paper entries.
```

Replace the outdated line:

```markdown
- [ ] `references_method` 若存在 `target_paper_path`，对象页投影必须提供 `target_paper`。
```

with:

```markdown
- [ ] `references_method` 若存在 `source_paper_path` / `target_paper_path`，对象页投影必须保留 path metadata，但不得把它们升级为新的 paper 邻接。
```

Replace `.claude/skills/relation-reconciliation/evals/regression-samples.json` with:

```json
[
  {
    "name": "PathMind-method-paper",
    "input_assumption": "paper-ingest has emitted relation_candidates for a standard empirical method paper",
    "must_reconcile": [
      "proposes",
      "targets_task",
      "evaluated_on",
      "uses_concept",
      "supported_by",
      "cites",
      "sourced_from"
    ],
    "quality_checks": [
      "must classify existing ledger edges as already_present",
      "must add missing formal edges to the correct ledger file",
      "must preserve explicit relation exemptions",
      "must output affected_pages for page-projection-sync",
      "must include both source and target object pages in affected_pages when both page files exist",
      "must reject or surface for review any Paper --supported_by--> Evidence candidate",
      "must render relation pages as 关系语义说明区 + 实例边账本区",
      "must write references_method ledger child fields in canonical order: source_path, target_path, source_paper_path, target_paper_path, edge_semantics, evidence, evidence_link, evidence_path",
      "must keep wikilinks limited to main-line source/target and evidence_link",
      "must fall back to path-based wikilinks when basename is not unique",
      "must not require RawSource file targets to enter object-page affected_pages coverage",
      "must preserve placeholder cited papers as Paper Stub / Anchor targets",
      "must reject references_method provenance when the matching cites edge is missing"
    ]
  }
]
```

Replace `.claude/skills/page-projection-sync/evals/regression-samples.json` with:

```json
[
  {
    "name": "method-page-sync",
    "input_assumption": "relation-reconciliation has added or confirmed method evolution, task, benchmark, and proposes edges",
    "must_sync": [
      "Formal relations",
      "strong-consistency frontmatter",
      "templated human relation blocks"
    ],
    "quality_checks": [
      "must update parent_methods and child_methods when affected",
      "must emit semi-expanded projection lines with explicit document paths",
      "must include fixed role sentences after Outgoing and Incoming headings",
      "must project edge_semantics and evidence for every relation instance",
      "must keep repeated neighbor relations separate when edge_semantics or evidence differ",
      "must keep interpretive prose untouched",
      "must report manual followups if prose still needs human review"
    ]
  },
  {
    "name": "cited-placeholder-target-sync",
    "input_assumption": "relation-reconciliation has confirmed a Paper --cites--> Placeholder Paper edge and both page files exist",
    "must_sync": [
      "source outgoing cites projection",
      "target incoming cites projection",
      "placeholder target Formal relations block"
    ],
    "quality_checks": [
      "must keep placeholder cited-paper targets non-serving paper stubs",
      "must include Outgoing and Incoming headings on the placeholder target page",
      "must keep body wikilinks inside the projected neighbor set"
    ]
  },
  {
    "name": "rawsource-target-exemption",
    "input_assumption": "relation-reconciliation has confirmed an Evidence --sourced_from--> RawSource PDF edge",
    "must_sync": [
      "source outgoing sourced_from projection"
    ],
    "quality_checks": [
      "must not require a RawSource file target to gain object-page Incoming projection",
      "must preserve the RawSource provenance path in the relation ledger and source Evidence page"
    ]
  }
]
```

- [ ] **Step 5: Run the contract regression and lint-adjacent test suite**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected: the new contract test passes; existing tests that still encode the old projection checklist wording may fail until Task 3 updates the implementation and assertions.

- [ ] **Step 6: Commit the contract updates**

```bash
git add ontology/graph-standard.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md .claude/skills/serving-governance-review/SKILL.md .claude/skills/relation-reconciliation/evals/regression-samples.json .claude/skills/page-projection-sync/evals/quality-checklist.md .claude/skills/page-projection-sync/evals/regression-samples.json scripts/test_method_relation_pipeline.py
git commit -m "feat: define paper stub anchor contract"
```

### Task 3: Enforce paper-anchor and cites-backing rules in lint and regression tests

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `scripts/test_method_relation_pipeline.py`
- Verify: `ontology/relations/references_method.md`
- Verify: `ontology/relations/cites.md`
- Verify: `ontology/entities/methods/PathMind.md`
- Verify: `ontology/entities/methods/GNN-RAG.md`
- Verify: `ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`

- [ ] **Step 1: Add a failing lint regression for missing cites backing**

Add this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_lint_rejects_references_method_without_matching_cites_edge(self):
        references_method_path = ROOT / 'ontology/relations/references_method.md'
        cites_path = ROOT / 'ontology/relations/cites.md'
        original_references = references_method_path.read_text(encoding='utf-8')
        original_cites = cites_path.read_text(encoding='utf-8')

        references_method_path.write_text(
            original_references
            + "\n- [[Synthetic Source Method]] --references_method--> [[Synthetic Target Method]]\n"
            + "  - source_path: ontology/entities/methods/Synthetic Source Method.md\n"
            + "  - target_path: ontology/entities/methods/Synthetic Target Method.md\n"
            + "  - source_paper_path: ontology/entities/papers/Synthetic Source Paper.md\n"
            + "  - target_paper_path: ontology/entities/papers/Synthetic Target Paper.md\n"
            + "  - edge_semantics: synthetic missing cites backing.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            references_method_path.write_text(original_references, encoding='utf-8')
            cites_path.write_text(original_cites, encoding='utf-8')

        self.assertIn(
            'references_method paper provenance must be backed by cites: ontology/entities/papers/Synthetic Source Paper.md -> ontology/entities/papers/Synthetic Target Paper.md',
            result.stdout + result.stderr,
        )
```

- [ ] **Step 2: Add a failing lint regression for missing paper anchor on partial Method**

Add this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_lint_rejects_partial_method_without_any_paper_anchor(self):
        method_path = ROOT / 'ontology/entities/methods/Synthetic Anchorless Method.md'
        original_exists = method_path.exists()
        original_text = method_path.read_text(encoding='utf-8') if original_exists else None

        method_path.write_text(
            """---
 title: Synthetic Anchorless Method
 type: 基础方法
 parent_methods: []
 child_methods: []
 problem: [reasoning]
 method_family: [hybrid]
 scenario: []
 research_task: [knowledge-graph-reasoning]
 industry: [general]
 research_role: [foundational]
 status: partial
 ---
 
 # Synthetic Anchorless Method
 
 ## Object semantics
 - 一个故意缺少 paper anchor 的测试方法。
 
 ## 当前定位
 - 测试 partial Method 锚点校验。
 
 ## 与知识库现有内容的关系
 - 无。
 
 ## 最小定义/角色
 - 无。
 
 ## 待补充
 - 无。
 
 ## Formal relations
 ### Outgoing
 当前对象作为 source；以下列出当前对象指向的 relation 实例。
 - 无
 
 ### Incoming
 当前对象作为 target；以下列出指向当前对象的 relation 实例。
 - 无
 """,
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            if original_exists and original_text is not None:
                method_path.write_text(original_text, encoding='utf-8')
            else:
                method_path.unlink()

        self.assertIn(
            'formal/partial Method must resolve to at least one paper anchor: ontology/entities/methods/Synthetic Anchorless Method.md',
            result.stdout + result.stderr,
        )
```

- [ ] **Step 3: Implement the minimal lint helpers**

Add these helpers to `scripts/lint_graph.py` near the other projection / ledger parsing helpers:

```python
def extract_relation_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if match := FORMAL_RELATION_RE.match(line.strip()):
            current = {
                'source': match.group('src').strip(),
                'relation_type': match.group('rel').strip(),
                'target': match.group('dst').strip(),
            }
            records.append(current)
            continue
        if current and line.startswith('  - '):
            key, _, value = line[4:].partition(':')
            if _:
                current[key.strip()] = value.strip()
        elif line.strip() and not line.startswith('  - '):
            current = None
    return records


def load_relation_records(rel_path: str) -> list[dict[str, str]]:
    return extract_relation_records(read_text(rel_path))
```

Then add this validator near the other ledger contract checks:

```python
def check_references_method_cites_backing(errors: list[str]) -> None:
    cites_records = load_relation_records('ontology/relations/cites.md')
    cites_pairs = {
        (record.get('source_path', ''), record.get('target_path', ''))
        for record in cites_records
        if record.get('relation_type') == 'cites'
    }
    for record in load_relation_records('ontology/relations/references_method.md'):
        source_paper_path = record.get('source_paper_path', '')
        target_paper_path = record.get('target_paper_path', '')
        if not source_paper_path or not target_paper_path:
            continue
        if (source_paper_path, target_paper_path) not in cites_pairs:
            errors.append(
                'references_method paper provenance must be backed by cites: '
                f'{source_paper_path} -> {target_paper_path}'
            )
```

And add this validator for method anchors:

```python
def check_method_paper_anchors(errors: list[str]) -> None:
    anchor_map: dict[str, set[str]] = {}

    for record in load_relation_records('ontology/relations/proposes.md'):
        target_path = record.get('target_path', '')
        source_path = record.get('source_path', '')
        if target_path.startswith('ontology/entities/methods/') and source_path.startswith('ontology/entities/papers/'):
            anchor_map.setdefault(target_path, set()).add(source_path)

    for record in load_relation_records('ontology/relations/references_method.md'):
        for method_key, paper_key in (('source_path', 'source_paper_path'), ('target_path', 'target_paper_path')):
            method_path = record.get(method_key, '')
            paper_path = record.get(paper_key, '')
            if method_path.startswith('ontology/entities/methods/') and paper_path.startswith('ontology/entities/papers/'):
                anchor_map.setdefault(method_path, set()).add(paper_path)

    for method_path in sorted((ROOT / 'ontology/entities/methods').glob('*.md')):
        rel_path = str(method_path.relative_to(ROOT))
        frontmatter, _ = split_frontmatter(method_path.read_text(encoding='utf-8', errors='ignore'))
        status = frontmatter.get('status')
        if status not in {'partial', 'processed'}:
            continue
        if not anchor_map.get(rel_path):
            errors.append(f'formal/partial Method must resolve to at least one paper anchor: {rel_path}')
```

Finally, call both validators from `main()` after the existing relation-ledger checks:

```python
    check_references_method_cites_backing(errors)
    check_method_paper_anchors(errors)
```

- [ ] **Step 4: Update the existing regression assertions to the new paper-stub semantics**

In `scripts/test_method_relation_pipeline.py`, update these assertions:

```python
        self.assertIn('`placeholder` Paper 只进入 non-serving block，并作为 `Paper Stub / Anchor` 理解', index_sync)
```

```python
        self.assertIn('`references_method` 若存在 `source_paper_path` / `target_paper_path`，对象页投影必须保留 path metadata，但不得把它们升级为新的 paper 邻接。', projection_checklist)
```

```python
        self.assertIn('must preserve placeholder cited papers as Paper Stub / Anchor targets', reconciliation_samples)
        self.assertIn('must reject references_method provenance when the matching cites edge is missing', reconciliation_samples)
```

```python
        self.assertIn('must keep placeholder cited-paper targets non-serving paper stubs', projection_samples)
```

- [ ] **Step 5: Run the full regression suite**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected: PASS. The output should not contain either of these strings:

```text
references_method paper provenance must be backed by cites
formal/partial Method must resolve to at least one paper anchor
```

- [ ] **Step 6: Commit the lint and regression work**

```bash
git add scripts/lint_graph.py scripts/test_method_relation_pipeline.py
git commit -m "feat: enforce paper stub method anchor rules"
```

### Task 4: Reconfirm live serving/index semantics for cited placeholder papers

**Files:**
- Verify: `ontology/entities/papers/index.md`
- Verify: `ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
- Verify: `ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
- Verify: `ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`
- Verify: `ontology/entities/methods/GNN-RAG.md`
- Verify: `ontology/entities/methods/RoG.md`
- Verify: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Verify the existing papers index still matches the new stub semantics**

Read `ontology/entities/papers/index.md` and confirm the non-serving block still contains cited placeholder entries like:

```markdown
- Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs 入口（文档：`ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`）：[[ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
  - object_semantics: 被 PathMind 引用的上游论文占位节点，待后续正式 ingest。
  - status: placeholder
```

Expected: the file already reflects non-serving cited-paper behavior; no edit needed unless the wording actively contradicts `Paper Stub / Anchor`.

- [ ] **Step 2: Verify cited placeholder pages remain formal-bearing stubs**

Read the cited paper pages and confirm each still has:

```markdown
## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `cites`：...
```

Expected: PASS for the PathMind cited-paper stubs.

- [ ] **Step 3: Verify partial Methods still rely on stub-backed anchors**

Read `ontology/entities/methods/GNN-RAG.md` and `ontology/entities/methods/RoG.md` and confirm they still contain incoming `references_method` and paper-path metadata on the source PathMind page rather than direct paper neighbors.

Expected snippet on `ontology/entities/methods/PathMind.md`:

```markdown
- `references_method`：GNN-RAG（文档：`ontology/entities/methods/GNN-RAG.md`）：[[../methods/GNN-RAG]]
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md
  - evidence: [[../evidence/PathMind.refs]]
```

- [ ] **Step 4: Run lint as final verification**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: no output and exit code 0.

- [ ] **Step 5: Commit the verification-only checkpoint if any wording changed**

If you had to edit `ontology/entities/papers/index.md` or any live placeholder page wording to align with Paper Stub semantics:

```bash
git add ontology/entities/papers/index.md ontology/entities/papers/*.md
git commit -m "docs: align cited paper stubs with serving semantics"
```

If no file changed, skip this commit.

## Self-Review

- Spec coverage: the plan covers the four spec pillars — Paper split, Method anchor minimum, `references_method` / `cites` hard backing, and serving/index treatment of stubs. The only live-content edits deferred are optional wording touch-ups if current placeholder pages contradict the new semantics.
- Placeholder scan: no `TODO`, `TBD`, “similar to above”, or unbound “write tests” steps remain. Each code-changing step includes concrete code or exact replacement text.
- Type consistency: all names match the current repo terms: `Formal Paper`, `Paper Stub / Anchor`, `source_paper_path`, `target_paper_path`, `references_method`, `cites`, `needs_human_review`, `affected_pages`.
