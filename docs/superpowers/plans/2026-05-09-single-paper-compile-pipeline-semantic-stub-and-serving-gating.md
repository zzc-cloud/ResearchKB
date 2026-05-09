# Single-Paper Compile Pipeline Semantic Stub and Serving Gating Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing 7-step single-paper compile pipeline so it can emit semantic stub candidates, project them into partial semantic pages, and prevent those pages from being mis-promoted to default serving surfaces.

**Architecture:** Keep the current pipeline stages unchanged, but strengthen the contracts between them. `paper-ingest` will emit semantic stub candidates, `relation-reconciliation` will carry forward stub/page serving status recommendations, `page-projection-sync` and `index-sync` will materialize and classify `placeholder` / `partial` / `serving-ready`, and `serving-governance-review` will gate on those states rather than treating all formal neighbors as equally serveable.

**Tech Stack:** Markdown skill docs, Python lint/tests, ResearchKB ontology pages, Bash, git

---

## File Structure

- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Extend the ingest contract to emit `semantic_stub_candidates` with the approved fields.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Add `affected_stub_pages` and `serving_status_recommendations` to the reconcile outputs and inputs.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Define how semantic stub metadata becomes minimal semantic skeletons and `status: partial` / `status: placeholder` projections.
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Define the three-state index rules for `placeholder`, `partial`, and `serving-ready`.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Change serving verdict rules to gate on partial neighbors.
- Modify: `ontology/graph-standard.md`
  - Add the normative status distinction and semantic-stub serving rules so the skill contracts align with the spec.
- Modify: `scripts/lint_graph.py`
  - Teach lint to recognize `partial` as a legitimate projection/index state where appropriate.
  - Add regression tests for `partial` state, semantic-stub index treatment, and serving-gating assumptions.

No new pipeline stage. No broad ontology page migration in this plan.

### Task 1: Define semantic stub contract in `paper-ingest`

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Write the failing regression test for semantic stub contract text**

```python
def test_paper_ingest_contract_defines_semantic_stub_candidates(self):
    text = (ROOT / '.claude' / 'skills' / 'paper-ingest' / 'SKILL.md').read_text(encoding='utf-8')
    self.assertIn('semantic_stub_candidates', text)
    self.assertIn('object_name', text)
    self.assertIn('object_type', text)
    self.assertIn('source_evidence', text)
    self.assertIn('object_semantics', text)
    self.assertIn('serving_readiness_hint', text)
```

- [ ] **Step 2: Run the new test to verify it fails first**

Run:

```bash
```

Expected: FAIL because `semantic_stub_candidates` is not yet documented in `paper-ingest`.

- [ ] **Step 3: Update `paper-ingest` to emit semantic stub candidates**

Add a new contract block under the existing structured-output section in `.claude/skills/paper-ingest/SKILL.md` with content equivalent to:

```markdown
semantic_stub_candidates:
  - object_name: RoG
    object_type: Method
    source_evidence: PathMind.refs
    object_semantics: retrieval-augmented 显式路径推理上游方法。
    minimal_sections:
      当前定位: 当前作为 PathMind 的关键上游方法或比较路线。
      与知识库现有内容的关系: 被当前论文引用，并可能被 formal relation 指向。
      最小定义/角色: 在当前论文语境中承担上游方法或代表路线角色。
      待补充: 正式方法定义、代表论文、技术细节与证据页。
    serving_readiness_hint: partial
```

Also add short explanatory bullets that:
- semantic stubs are for objects with stable minimal semantics but insufficient evidence for full serving-ready promotion
- they do not replace full ingest
- they are intended for downstream projection and serving gating

- [ ] **Step 4: Update the graph standard to recognize semantic stub / partial state**

Add a short normative rule block to `ontology/graph-standard.md` covering:

```markdown
- 当单篇论文已稳定提供某个邻接对象的最小对象语义，但证据仍不足以支持完整 serving-ready 页面时，可生成 semantic stub。
- semantic stub 页至少应具有：`status: partial` 或 `status: placeholder`、`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`。
- `partial` 表示对象可被正式链接、可被 index 收录、可参与 formal graph 遍历，但不得自动提升为默认 serving 入口。
```

- [ ] **Step 5: Run the regression test again to verify it passes**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 6: Commit the semantic stub contract change**

```bash
git commit -m "feat: define semantic stub ingest contract"
```

### Task 2: Carry stub status through `relation-reconciliation`

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`

- [ ] **Step 1: Write the failing regression test for reconcile outputs**

Add a test like:

```python
def test_relation_reconciliation_contract_mentions_stub_handoff(self):
    text = (ROOT / '.claude' / 'skills' / 'relation-reconciliation' / 'SKILL.md').read_text(encoding='utf-8')
    self.assertIn('affected_stub_pages', text)
    self.assertIn('serving_status_recommendations', text)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
```

Expected: FAIL because these output names are not yet documented.

- [ ] **Step 3: Update the reconciliation skill output contract**

Extend the output template in `.claude/skills/relation-reconciliation/SKILL.md` to include:

```yaml
affected_pages: []
affected_stub_pages: []
serving_status_recommendations:
  - path: ontology/entities/methods/RoG.md
    recommended_status: partial
    reason: stable minimal semantics exist, but default serving evidence is still insufficient
```

Also add a short note in the responsibility section that reconciliation must propagate semantic-stub state to downstream projection.

- [ ] **Step 4: Run the regression test again**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 5: Commit the reconciliation handoff change**

```bash
git commit -m "feat: add stub serving handoff to reconciliation"
```

### Task 3: Project semantic stubs into partial pages

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Write the failing regression test for partial semantic skeleton requirements**

Add a test like:

```python
def test_graph_standard_defines_partial_semantic_stub_sections(self):
    text = (ROOT / 'ontology' / 'graph-standard.md').read_text(encoding='utf-8')
    self.assertIn('## 最小定义/角色', text)
    self.assertIn('`partial` 表示对象可被正式链接', text)
```
```

And a page-projection contract test like:

```python
def test_page_projection_sync_mentions_semantic_stub_projection(self):
    text = (ROOT / '.claude' / 'skills' / 'page-projection-sync' / 'SKILL.md').read_text(encoding='utf-8')
    self.assertIn('semantic_stub_candidates', text)
    self.assertIn('## 最小定义/角色', text)
    self.assertIn('status: partial', text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
```

Expected: FAIL.

- [ ] **Step 3: Update `page-projection-sync` to project semantic stub skeletons**

Document in `.claude/skills/page-projection-sync/SKILL.md` that when a page is classified as a semantic stub, the projection stage writes:

```markdown
## Object semantics
- ...

## 当前定位
- ...

## 与知识库现有内容的关系
- ...

## 最小定义/角色
- ...

## 待补充
- ...
```

And that the page may be marked `status: partial` while retaining formal relation truth.

- [ ] **Step 4: Re-run the regression tests**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 5: Commit the projection contract change**

```bash
git commit -m "feat: project semantic stubs as partial pages"
```

### Task 4: Teach `index-sync` and lint about `partial`

**Files:**
- Modify: `.claude/skills/index-sync/SKILL.md`
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Write the failing regression test for partial index handling**

Add a test like:

```python
def test_index_sync_contract_distinguishes_partial_from_serving_ready(self):
    text = (ROOT / '.claude' / 'skills' / 'index-sync' / 'SKILL.md').read_text(encoding='utf-8')
    self.assertIn('partial', text)
    self.assertIn('placeholder', text)
    self.assertIn('serving-ready', text)
```

And a lint-oriented test like:

```python
def test_lint_graph_accepts_partial_status_projection(self):
    text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
    self.assertIn('partial', text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
```

Expected: FAIL.

- [ ] **Step 3: Update `index-sync` status rules**

Document in `.claude/skills/index-sync/SKILL.md` that:

```markdown
- `placeholder`：只进入 non-serving block
- `partial`：可被 index 收录，但不得进入 default entry
- `serving-ready`：进入默认导航入口
```

- [ ] **Step 4: Update lint to recognize `partial` as a valid projected/index state**

Adjust `scripts/lint_graph.py` so index projection and related status validation accept:

```python
{'placeholder', 'partial', 'serving-ready'}
```

where status values are checked for projected/index entries.

- [ ] **Step 5: Re-run the tests to verify they pass**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 6: Commit the index/lint state-model change**

```bash
git commit -m "feat: add partial serving state to index sync"
```

### Task 5: Gate serving on partial-vs-serving-ready neighbors

**Files:**
- Modify: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Write the failing regression test for serving-gating language**

Add a test like:

```python
def test_serving_governance_review_mentions_partial_neighbor_gating(self):
    text = (ROOT / '.claude' / 'skills' / 'serving-governance-review' / 'SKILL.md').read_text(encoding='utf-8')
    self.assertIn('partial', text)
    self.assertIn('formal neighbor 是否仍然停留在合格的默认 serving surface 上', text)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
```

Expected: FAIL.

- [ ] **Step 3: Update serving-governance-review verdict rules**

Add or revise the skill text so it explicitly states:

```markdown
- 即使页面已能基于 `Formal relations` 做受约束拓扑扩展，只要关键拓扑下一跳仍主要落在 `partial` 对象页上，也不得直接判为 `serving-ready`。
- `partial`：当前页结构完整、formal relation 完整、邻居可解析，但关键邻居仍主要是 semantic stub / partial 页。
```

- [ ] **Step 4: Re-run the regression test**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 5: Run the full lint regression suite**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 6: Run graph lint to verify the repository contract still holds**

Run:

```bash
python3 ./scripts/lint_graph.py
```

Expected:

```python
PASS: graph lint succeeded
```

- [ ] **Step 7: Commit the serving-gating change**

```bash
git commit -m "feat: gate serving readiness on partial neighbors"
```

## Spec Coverage Check

- `paper-ingest` emits `semantic_stub_candidates`: covered by Task 1.
- `relation-reconciliation` forwards stub/page serving status recommendations: covered by Task 2.
- `page-projection-sync` writes minimal semantic skeletons and `partial` status: covered by Task 3.
- `index-sync` distinguishes `placeholder` / `partial` / `serving-ready`: covered by Task 4.
- `serving-governance-review` uses partial-vs-serving-ready gating: covered by Task 5.
- No new pipeline stage introduced: preserved in File Structure and all tasks.

## Placeholder Scan

- No `TODO`, `TBD`, or “implement later” markers remain.
- Every changed file path is explicit.
- Every verification step includes an exact command and expected result.

## Type / Name Consistency Check

- State names are consistently `placeholder`, `partial`, and `serving-ready`.
- The same `semantic_stub_candidates`, `affected_stub_pages`, and `serving_status_recommendations` names are used throughout.
- All tasks modify only the approved pipeline skills, graph standard, and lint/test files.
