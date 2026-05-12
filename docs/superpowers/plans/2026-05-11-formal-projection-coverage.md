# Formal Projection Coverage Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce that every formal relation ledger edge is projected onto every existing source/target object page, while explicitly exempting RawSource file targets from object-page incoming projection.

**Architecture:** Tighten the contract in three layers. First codify the source+target projection rule in `ontology/graph-standard.md`, the reconciliation/projection skills, and their eval fixtures. Then teach `scripts/lint_graph.py` to reconcile canonical ledger records against object-page `Formal relations` blocks, including a dedicated error for formal-bearing placeholder pages that still lack projection structure. Finally, backfill the currently broken cited placeholder paper pages from `ontology/relations/cites.md` so the stricter lint can pass on the live repo.

**Tech Stack:** Markdown ontology spec, Claude skill contracts, JSON eval fixtures, Python lint script, Python unittest regression suite, Bash, git

---

## File Structure

- Modify: `scripts/test_method_relation_pipeline.py`
  - Add contract-level regression tests for the new source+target projection rule.
  - Add lint regression tests for missing source projection, missing target projection, placeholder formal-bearing pages, and RawSource target exemption.
- Modify: `ontology/graph-standard.md`
  - Add the formal-bearing placeholder contract and the RawSource exemption language.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Require `affected_pages` to include both source and target object pages for every reconciled formal relation instance whose page file exists.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Require any existing formal-bearing object page, including placeholder/partial pages, to receive `## Formal relations`, `### Outgoing`, and `### Incoming`.
  - Document the RawSource target exemption for `sourced_from`.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Add explicit checklist items for source+target coverage, formal-bearing placeholder pages, and RawSource exemption.
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Add quality checks for dual-sided `affected_pages` coverage and RawSource-safe routing.
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Add regression samples for cited placeholder target projection and RawSource exemption.
- Modify: `scripts/lint_graph.py`
  - Add ledger-to-object-page projection coverage validation.
  - Add a specific failure for formal-bearing placeholder pages with no formal relations block.
  - Exempt non-object-page RawSource targets from target-side incoming projection requirements.
- Modify live placeholder paper pages to satisfy the new contract:
  - `ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
  - `ontology/entities/papers/Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models.md`
  - `ontology/entities/papers/Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering.md`
  - `ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
  - `ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
  - `ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`
  - `ontology/entities/papers/LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph.md`
  - `ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
  - `ontology/entities/papers/Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation.md`
  - `ontology/entities/papers/Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph.md`
  - `ontology/entities/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`

No new runtime scripts. No relation-ledger format changes. No index-sync redesign.

### Task 1: Add contract regressions for the new projection-coverage rule

**Files:**
- Modify: `scripts/test_method_relation_pipeline.py`
- Verify: `ontology/graph-standard.md`
- Verify: `.claude/skills/relation-reconciliation/SKILL.md`
- Verify: `.claude/skills/page-projection-sync/SKILL.md`
- Verify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Verify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Verify: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Write the failing regression test**

Add this test method near the end of `scripts/test_method_relation_pipeline.py`, above the `if __name__ == '__main__':` block:

```python
    def test_formal_projection_coverage_contract_is_documented(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        reconciliation = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
        reconciliation_samples = (ROOT / '.claude/skills/relation-reconciliation/evals/regression-samples.json').read_text(encoding='utf-8')
        projection_samples = (ROOT / '.claude/skills/page-projection-sync/evals/regression-samples.json').read_text(encoding='utf-8')

        self.assertIn('若该页已经承接 formal relation instance，则必须具备 formal projection 合同', graph_standard)
        self.assertIn('RawSource 文件是 provenance target，不进入普通对象页双侧 projection 合同', graph_standard)
        self.assertIn('`affected_pages` must include both source and target object pages for every reconciled formal relation instance whose corresponding page file exists.', reconciliation)
        self.assertIn('只要对象页存在，且它在 current formal ledger 中作为任一 instance edge 的 source 或 target 出现，就必须生成 formal projection。', projection)
        self.assertIn('RawSource targets are exempt from object-page incoming projection', projection_checklist)
        self.assertIn('must include both source and target object pages in affected_pages when both page files exist', reconciliation_samples)
        self.assertIn('cited-placeholder-target-sync', projection_samples)
        self.assertIn('rawsource-target-exemption', projection_samples)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected: FAIL in `test_formal_projection_coverage_contract_is_documented` because the new contract strings do not exist yet.

- [ ] **Step 3: Commit the failing-test scaffold**

```bash
git add scripts/test_method_relation_pipeline.py
git commit -m "test: add projection coverage contract regressions"
```

- [ ] **Step 4: Verify the commit landed**

Run:

```bash
git log --oneline -1
```

Expected: latest commit message is `test: add projection coverage contract regressions`.

### Task 2: Update the graph standard, skill contracts, and eval fixtures

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Add the graph-standard contract block**

Insert these exact bullets into the semantic-stub / projection contract area of `ontology/graph-standard.md`:

```markdown
- `status: placeholder` 仅表示对象尚非 default serving-ready entry；若该页已经承接 formal relation instance，则必须具备 formal projection 合同。
- formal projection 合同至少包括：`## Formal relations`、`### Outgoing`、`### Incoming`，且空侧显式写 `- 无`。
- formal relation 投影义务由“页面是否存在 + 是否承接 formal relation”决定，而不是由页面状态决定。
- RawSource 文件是 provenance target，不进入普通对象页双侧 projection 合同；但 source Evidence 页仍必须维护 outgoing `sourced_from`。
```

- [ ] **Step 2: Add the reconciliation skill contract text**

In `.claude/skills/relation-reconciliation/SKILL.md`, add this exact sentence under the `affected_pages` / handoff section:

```markdown
- `affected_pages` must include both source and target object pages for every reconciled formal relation instance whose corresponding page file exists.
- 若某对象页已承接 formal relation 且同时出现在 `affected_stub_pages` 中，它仍必须同时出现在 `affected_pages` 中；`affected_stub_pages` 只做辅助分类，不替代对象页同步清单。
- 对于 `cites` 指向的 placeholder paper target，创建占位页后不得停在“仅可解析”状态，必须继续进入 `page-projection-sync`。
```

- [ ] **Step 3: Add the projection skill contract text**

In `.claude/skills/page-projection-sync/SKILL.md`, add this exact block to the formal-projection rules:

```markdown
- 只要对象页存在，且它在 current formal ledger 中作为任一 instance edge 的 source 或 target 出现，就必须生成 formal projection。
- 该规则对 `processed`、`partial`、`placeholder` 一视同仁。
- `status: placeholder` 仅表示该页尚非 default serving-ready 页面；若它已承接 formal relation，则必须具备 `## Formal relations`、`### Outgoing`、`### Incoming`。
- `RawSource` 文件路径只作为 provenance target；对 `sourced_from`，source Evidence 页必须投影 outgoing，但 target 不要求对象页式 `Incoming`。
```

- [ ] **Step 4: Update the eval fixtures**

Append these exact checklist items to `.claude/skills/page-projection-sync/evals/quality-checklist.md`:

```markdown
- [ ] placeholder pages that bear formal relations must still receive `Formal relations` projection.
- [ ] RawSource targets are exempt from object-page incoming projection.
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
      "must write ledger child fields in canonical order: source_path, target_path, edge_semantics, evidence, evidence_link, evidence_path",
      "must keep wikilinks limited to main-line source/target and evidence_link",
      "must fall back to path-based wikilinks when basename is not unique",
      "must not require RawSource file targets to enter object-page affected_pages coverage"
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
      "must keep the placeholder target non-serving while still projecting incoming cites",
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

- [ ] **Step 5: Re-run the regression test**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected: `test_formal_projection_coverage_contract_is_documented` passes.

- [ ] **Step 6: Commit the contract-file updates**

```bash
git add \
  ontology/graph-standard.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/evals/regression-samples.json
git commit -m "docs: define formal projection coverage contract"
```

### Task 3: Add lint regressions for source/target coverage and RawSource exemption

**Files:**
- Modify: `scripts/test_method_relation_pipeline.py`
- Verify: `scripts/lint_graph.py`

- [ ] **Step 1: Write the failing regression tests**

Append these exact test methods to `scripts/test_method_relation_pipeline.py`, below the contract test from Task 1:

```python
    def test_lint_rejects_ledger_edge_when_source_page_lacks_formal_relations(self):
        cites_path = ROOT / 'ontology/relations/cites.md'
        source_path = ROOT / 'ontology/entities/papers/Synthetic Source Paper.md'
        target_path = ROOT / 'ontology/entities/papers/Synthetic Target Paper.md'
        original_cites = cites_path.read_text(encoding='utf-8')
        original_source_exists = source_path.exists()
        original_target_exists = target_path.exists()
        original_source = source_path.read_text(encoding='utf-8') if original_source_exists else None
        original_target = target_path.read_text(encoding='utf-8') if original_target_exists else None

        source_path.write_text(
            """---
title: Synthetic Source Paper
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Source Paper

## 当前定位
- 当前作为 [[Synthetic Target Paper]] 的测试 source 页。

## 与知识库现有内容的关系
- 无。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        target_path.write_text(
            """---
title: Synthetic Target Paper
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Target Paper

## 当前定位
- 当前作为 [[Synthetic Source Paper]] 的测试 target 页。

## 与知识库现有内容的关系
- 被引用于：[[Synthetic Source Paper]]。

## 待补充
- 无。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `cites`：Synthetic Source Paper（文档：`ontology/entities/papers/Synthetic Source Paper.md`）：[[Synthetic Source Paper]]
  - edge_semantics: synthetic source coverage check.
  - evidence: [[../evidence/PathMind.refs]]
""",
            encoding='utf-8',
        )

        cites_path.write_text(
            original_cites
            + "\n- [[Synthetic Source Paper]] --cites--> [[Synthetic Target Paper]]\n"
            + "  - source_path: ontology/entities/papers/Synthetic Source Paper.md\n"
            + "  - target_path: ontology/entities/papers/Synthetic Target Paper.md\n"
            + "  - edge_semantics: synthetic source coverage check.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            cites_path.write_text(original_cites, encoding='utf-8')
            if original_source_exists and original_source is not None:
                source_path.write_text(original_source, encoding='utf-8')
            else:
                source_path.unlink()
            if original_target_exists and original_target is not None:
                target_path.write_text(original_target, encoding='utf-8')
            else:
                target_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'missing Formal relations on source page for ledger edge: ontology/entities/papers/Synthetic Source Paper.md --cites--> ontology/entities/papers/Synthetic Target Paper.md',
            combined_output,
        )

    def test_lint_rejects_formal_bearing_placeholder_target_without_formal_relations(self):
        cites_path = ROOT / 'ontology/relations/cites.md'
        target_path = ROOT / 'ontology/entities/papers/Synthetic Placeholder Target.md'
        original_cites = cites_path.read_text(encoding='utf-8')
        original_target_exists = target_path.exists()
        original_target = target_path.read_text(encoding='utf-8') if original_target_exists else None

        target_path.write_text(
            """---
title: Synthetic Placeholder Target
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Placeholder Target

## 当前定位
- 当前作为 [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] 的测试 target 页。

## 与知识库现有内容的关系
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        cites_path.write_text(
            original_cites
            + "\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Synthetic Placeholder Target]]\n"
            + "  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md\n"
            + "  - target_path: ontology/entities/papers/Synthetic Placeholder Target.md\n"
            + "  - edge_semantics: synthetic placeholder coverage check.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            cites_path.write_text(original_cites, encoding='utf-8')
            if original_target_exists and original_target is not None:
                target_path.write_text(original_target, encoding='utf-8')
            else:
                target_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'formal-bearing placeholder page missing formal relations contract: ontology/entities/papers/Synthetic Placeholder Target.md',
            combined_output,
        )
        self.assertIn(
            'missing Formal relations on target page for ledger edge: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md --cites--> ontology/entities/papers/Synthetic Placeholder Target.md',
            combined_output,
        )

    def test_lint_exempts_rawsource_targets_from_incoming_projection_requirement(self):
        sourced_from_path = ROOT / 'ontology/relations/sourced_from.md'
        evidence_path = ROOT / 'ontology/entities/evidence/SyntheticProjection.sections.md'
        raw_path = ROOT / 'ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf'
        original_ledger = sourced_from_path.read_text(encoding='utf-8')
        original_evidence_exists = evidence_path.exists()
        original_evidence = evidence_path.read_text(encoding='utf-8') if original_evidence_exists else None
        original_raw_exists = raw_path.exists()

        evidence_path.write_text(
            """---
title: SyntheticProjection.sections
short_name: SyntheticProjection
source_file: ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf
cache_type: sections
status: processed
year: 2026
venue: synthetic
---

# SyntheticProjection.sections

## Object semantics
- Synthetic projection coverage evidence page.

## 对应正式知识节点
- [[../tasks/knowledge-graph-reasoning]]

## 本节支撑什么
- Synthetic projection coverage fixture.

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Synthetic projection coverage fixture.

## 来源说明
- Synthetic projection coverage fixture.

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：Synthetic Projection Coverage.pdf（文档：`ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf`）：[[../raw-sources/files/Synthetic Projection Coverage.pdf]]
  - edge_semantics: synthetic rawsource exemption fixture.
  - evidence: [[../evidence/SyntheticProjection.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
""",
            encoding='utf-8',
        )

        if not original_raw_exists:
            raw_path.write_bytes(b'%PDF-1.4\n%synthetic\n')

        sourced_from_path.write_text(
            original_ledger
            + "\n- [[SyntheticProjection.sections]] --sourced_from--> [[ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf]]\n"
            + "  - source_path: ontology/entities/evidence/SyntheticProjection.sections.md\n"
            + "  - target_path: ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf\n"
            + "  - edge_semantics: synthetic rawsource exemption fixture.\n"
            + "  - evidence: SyntheticProjection.sections\n"
            + "  - evidence_link: [[SyntheticProjection.sections]]\n"
            + "  - evidence_path: ontology/entities/evidence/SyntheticProjection.sections.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            sourced_from_path.write_text(original_ledger, encoding='utf-8')
            if original_evidence_exists and original_evidence is not None:
                evidence_path.write_text(original_evidence, encoding='utf-8')
            else:
                evidence_path.unlink()
            if not original_raw_exists and raw_path.exists():
                raw_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing Formal relations on target page for ledger edge: ontology/entities/evidence/SyntheticProjection.sections.md --sourced_from--> ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf', combined_output)
        self.assertNotIn('missing incoming projection for ledger edge: ontology/entities/evidence/SyntheticProjection.sections.md --sourced_from--> ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf', combined_output)
```

- [ ] **Step 2: Run the tests to verify the new source/target coverage tests fail**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected:
- `test_lint_rejects_ledger_edge_when_source_page_lacks_formal_relations` FAILS because `lint_graph.py` does not yet compare ledger records against source-page projections.
- `test_lint_rejects_formal_bearing_placeholder_target_without_formal_relations` FAILS because placeholder target pages are not yet validated as formal-bearing pages.
- `test_lint_exempts_rawsource_targets_from_incoming_projection_requirement` may already PASS; keep it as a guard while the other two fail.

- [ ] **Step 3: Commit the failing lint regressions**

```bash
git add scripts/test_method_relation_pipeline.py
git commit -m "test: add ledger projection coverage lint regressions"
```

- [ ] **Step 4: Verify the commit landed**

Run:

```bash
git log --oneline -1
```

Expected: latest commit message is `test: add ledger projection coverage lint regressions`.

### Task 4: Implement ledger-to-object-page coverage validation in `lint_graph.py`

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Add helper functions for object-page path classification and projected relation keys**

Add these exact helpers below `extract_projected_links` in `scripts/lint_graph.py`:

```python
def extract_projected_relation_keys(text: str) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for item in parse_projected_relation_items(text):
        main_line = item['main_line']
        match = SEMI_EXPANDED_RELATION_RE.match(main_line)
        if not match:
            continue
        heading = item['heading']
        relation_type = match.group('rel').strip()
        document_path = match.group('doc').strip()
        keys.add((heading, relation_type, document_path))
    return keys


def is_object_page_relpath(rel_path: str) -> bool:
    return rel_path.startswith('ontology/entities/papers/') or rel_path.startswith('ontology/entities/methods/') or rel_path.startswith('ontology/entities/tasks/') or rel_path.startswith('ontology/entities/scenarios/') or rel_path.startswith('ontology/entities/benchmarks/') or rel_path.startswith('ontology/entities/evidence/')


def is_rawsource_relpath(rel_path: str) -> bool:
    return rel_path.startswith('ontology/entities/raw-sources/files/')
```

- [ ] **Step 2: Add the ledger coverage validator**

Insert this exact validator below `validate_cited_paper_targets`:

```python
def validate_ledger_projection_coverage(errors: list[str]) -> None:
    for rel_file in RELATION_LEDGER_FILES:
        text = read_text(rel_file)
        for record in parse_relation_instance_records(text):
            field_map = dict(record['fields'])
            source_path = field_map['source_path']
            target_path = field_map['target_path']
            relation_type = record['rel']
            edge_label = f'{source_path} --{relation_type}--> {target_path}'

            if is_object_page_relpath(source_path):
                source_file = ROOT / source_path
                if source_file.exists():
                    source_text = source_file.read_text(encoding='utf-8', errors='ignore')
                    source_frontmatter, _ = split_frontmatter(source_text)
                    if '## Formal relations' not in source_text:
                        errors.append(f'missing Formal relations on source page for ledger edge: {edge_label}')
                    else:
                        source_keys = extract_projected_relation_keys(source_text)
                        expected_source_key = ('Outgoing', relation_type, target_path)
                        if expected_source_key not in source_keys:
                            errors.append(f'missing outgoing projection for ledger edge: {edge_label}')
                    if source_frontmatter.get('status') == 'placeholder' and '## Formal relations' not in source_text:
                        errors.append(f'formal-bearing placeholder page missing formal relations contract: {source_path}')

            if is_object_page_relpath(target_path):
                target_file = ROOT / target_path
                if target_file.exists():
                    target_text = target_file.read_text(encoding='utf-8', errors='ignore')
                    target_frontmatter, _ = split_frontmatter(target_text)
                    if '## Formal relations' not in target_text:
                        errors.append(f'missing Formal relations on target page for ledger edge: {edge_label}')
                    else:
                        target_keys = extract_projected_relation_keys(target_text)
                        expected_target_key = ('Incoming', relation_type, source_path)
                        if expected_target_key not in target_keys:
                            errors.append(f'missing incoming projection for ledger edge: {edge_label}')
                    if target_frontmatter.get('status') == 'placeholder' and '## Formal relations' not in target_text:
                        errors.append(f'formal-bearing placeholder page missing formal relations contract: {target_path}')
            elif is_rawsource_relpath(target_path):
                continue
```

- [ ] **Step 3: Wire the new validator into the lint flow**

Add this exact call after `validate_method_status_contract(errors)` in the main execution section:

```python
validate_ledger_projection_coverage(errors)
```

- [ ] **Step 4: Re-run the regression tests**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected:
- the new source/target coverage tests PASS;
- the RawSource exemption test PASSes;
- existing projection/lint tests remain green except for the known live cited-placeholder pages, which will be fixed in Task 5.

- [ ] **Step 5: Commit the lint implementation**

```bash
git add scripts/lint_graph.py scripts/test_method_relation_pipeline.py
git commit -m "feat: enforce ledger projection coverage in lint"
```

- [ ] **Step 6: Verify the commit landed**

Run:

```bash
git log --oneline -1
```

Expected: latest commit message is `feat: enforce ledger projection coverage in lint`.

### Task 5: Backfill the current cited placeholder paper targets from `cites.md`

**Files:**
- Modify:
  - `ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
  - `ontology/entities/papers/Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models.md`
  - `ontology/entities/papers/Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering.md`
  - `ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
  - `ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
  - `ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`
  - `ontology/entities/papers/LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph.md`
  - `ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
  - `ontology/entities/papers/Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation.md`
  - `ontology/entities/papers/Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph.md`
  - `ontology/entities/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`
- Source truth: `ontology/relations/cites.md`

- [ ] **Step 1: Write the backfill one-off script**

Run this exact one-off migration from the repo root:

```bash
python3 - <<'PY'
from pathlib import Path
import re

ROOT = Path.cwd()
ledger_path = ROOT / 'ontology/relations/cites.md'
ledger = ledger_path.read_text(encoding='utf-8')

record_re = re.compile(
    r'- \[\[(?P<src>[^\]]+)\]\] --cites--> \[\[(?P<dst>[^\]]+)\]\]\n'
    r'  - source_path: (?P<source_path>[^\n]+)\n'
    r'  - target_path: (?P<target_path>[^\n]+)\n'
    r'  - edge_semantics: (?P<edge_semantics>[^\n]+)\n'
    r'  - evidence: (?P<evidence>[^\n]+)\n'
    r'  - evidence_link: \[\[(?P<evidence_link>[^\]]+)\]\]\n'
    r'  - evidence_path: (?P<evidence_path>[^\n]+)',
    re.MULTILINE,
)

for match in record_re.finditer(ledger):
    target_rel = match.group('target_path').strip()
    target_file = ROOT / target_rel
    text = target_file.read_text(encoding='utf-8')
    if '## Formal relations' in text:
        continue

    source_rel = match.group('source_path').strip()
    source_link = Path(source_rel).stem
    evidence_rel = match.group('evidence_path').strip()
    evidence_link = '../' + str(Path(evidence_rel).relative_to('ontology/entities')).replace('.md', '')

    formal_block = (
        '## Formal relations\n'
        '### Outgoing\n'
        '当前对象作为 source；以下列出当前对象指向的 relation 实例。\n'
        '- 无\n\n'
        '### Incoming\n'
        '当前对象作为 target；以下列出指向当前对象的 relation 实例。\n'
        f'- `cites`：{match.group("src")}（文档：`{source_rel}`）：[[{source_link}]]\n'
        f'  - edge_semantics: {match.group("edge_semantics").strip()}\n'
        f'  - evidence: [[{evidence_link}]]\n'
    )

    target_file.write_text(text.rstrip() + '\n\n' + formal_block + '\n', encoding='utf-8')
PY
```

- [ ] **Step 2: Inspect one patched page and one edge source page**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for rel in [
    'ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md',
    'ontology/entities/papers/Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph.md',
    'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md',
]:
    path = Path(rel)
    print(f'===== {rel} =====')
    print(path.read_text(encoding='utf-8'))
PY
```

Expected:
- the cited placeholder target pages now contain `## Formal relations`, `### Outgoing`, `### Incoming`, and an incoming `cites` projection;
- the PathMind source page remains unchanged.

- [ ] **Step 3: Run the full lint to verify the backfill closes the live repo gap**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: the previous cited-placeholder coverage errors disappear. If any remaining error appears, it should be a genuinely unrelated repo issue that predates this plan.

- [ ] **Step 4: Commit the backfilled placeholder pages**

```bash
git add \
  "ontology/entities/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md" \
  "ontology/entities/papers/Chatkbqa - A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models.md" \
  "ontology/entities/papers/Flexkbqa - A flexible llm-powered framework for few-shot knowledge base question answering.md" \
  "ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md" \
  "ontology/entities/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md" \
  "ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md" \
  "ontology/entities/papers/LightPROF - A Lightweight Reasoning Framework for Large Language Model on Knowledge Graph.md" \
  "ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md" \
  "ontology/entities/papers/Simple is effective - The roles of graphs and large language models in knowledge-graph-based retrieval-augmented generation.md" \
  "ontology/entities/papers/Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph.md" \
  "ontology/entities/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md"
git commit -m "fix: backfill cited placeholder paper projections"
```

- [ ] **Step 5: Verify the commit landed**

Run:

```bash
git log --oneline -1
```

Expected: latest commit message is `fix: backfill cited placeholder paper projections`.

### Task 6: Run the full verification suite and finalize

**Files:**
- Verify all files changed in Tasks 1-5

- [ ] **Step 1: Run the regression suite**

Run:

```bash
python3 -m unittest discover -s scripts -p 'test_method_relation_pipeline.py' -v
```

Expected: PASS for the new contract test, the new lint coverage tests, and the pre-existing projection/lint regressions.

- [ ] **Step 2: Run the graph lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded`.

- [ ] **Step 3: Review the final diff**

Run:

```bash
git diff --stat HEAD~5..HEAD
git status --short
```

Expected:
- the diff shows only the spec/skill/eval/lint/test/placeholder-page files listed in this plan;
- `git status --short` is empty.

- [ ] **Step 4: Create the final integration commit if verification required a final touch-up**

If Steps 1-3 required any last edit, commit it with:

```bash
git add \
  scripts/test_method_relation_pipeline.py \
  ontology/graph-standard.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/evals/regression-samples.json \
  scripts/lint_graph.py \
  ontology/entities/papers/*.md
git commit -m "feat: enforce formal projection coverage"
```

If no final touch-up was needed, skip this step.
