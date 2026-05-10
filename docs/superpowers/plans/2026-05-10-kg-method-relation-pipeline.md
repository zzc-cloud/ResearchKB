# KG Method Relation Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the ResearchKB single-paper compile pipeline so `references_method` and `based_on` are first-class method-neighbor relations, `evaluated_on` becomes Method-only, missing upstream methods materialize as navigable partial Method pages, and generated object-page links default to simplified Obsidian jump format.

**Architecture:** Update the normative ontology contract first, then teach lint to enforce the new graph rules, then align `paper-ingest`, `relation-reconciliation`, `page-projection-sync`, and `index-sync` around the new method-neighbor workflow. Validate the redesign with a PathMind regression pass that proves references, partial Method materialization, Method-only benchmark edges, and simplified page links all work together.

**Tech Stack:** Obsidian-flavored Markdown under `ontology/` and `docs/`, Claude skill contracts under `.claude/skills/`, Python 3 repository linting in `scripts/lint_graph.py`, and Python `unittest` regression coverage in `scripts/test_method_relation_pipeline.py`.

---

## File map

### Normative ontology and relation contracts
- Modify: `ontology/graph-standard.md`
  - Narrow `evaluated_on` to `Method -> Benchmark`, remove Method placeholder state, replace `方法演化位置` with the new Method evolution/reference section contract, and codify simplified object-page link generation.
- Modify: `ontology/relations/evaluated_on.md`
  - Rewrite source/target contract to Method-only and adjust explanation prose accordingly.
- Modify: `ontology/relations/references_method.md`
  - Elevate this relation as a core method-neighbor relation and clarify the difference from `based_on`.
- Modify: `ontology/entities/methods/index.md`
  - Update object-domain explanation prose so partial Method pages in `navigation-entries` are explicitly valid.

### Runtime lint and regression coverage
- Modify: `scripts/lint_graph.py`
  - Reject `Paper` as `evaluated_on` source, remove Method placeholder assumptions, require simplified generated object-page links, and validate partial Method navigation treatment.
- Create: `scripts/test_method_relation_pipeline.py`
  - Add targeted regression tests for Method-only `evaluated_on`, partial Method contract, and simplified link-format enforcement.

### Pipeline skill contracts
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Require `references_method` extraction, forbid `Paper -> Benchmark` `evaluated_on`, and require direct partial Method materialization candidates for stable missing upstream methods.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Add based_on vs references_method routing rules, direct partial Method materialization handoff, and Method-only benchmark-edge enforcement.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Add the new Method “方法演化与参照关系” section contract and simplified link-format rules.
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Change partial Method indexing semantics so partial Method pages may enter `navigation-entries`.

### PathMind regression surface
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
  - Remove formal paper-level benchmark edges and simplify generated page links where needed.
- Modify: `ontology/entities/methods/PathMind.md`
  - Replace the old evolution section with the new dual based_on/references_method presentation and simplified links.
- Modify: `ontology/entities/benchmarks/WebQSP.md`
- Modify: `ontology/entities/benchmarks/CWQ.md`
  - Remove incoming paper-level `evaluated_on` projections, keep only Method-sourced benchmark relations, and simplify links.
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/references_method.md`
- Modify: `ontology/relations/based_on.md`
  - Ensure PathMind regression truth uses the correct relation split.
- Modify: `ontology/entities/methods/index.md`
  - Confirm partial Method navigation entries are valid in live content.

### New live partial Method pages for regression
- Create: `ontology/entities/methods/RoG.md`
- Create: `ontology/entities/methods/GCR.md`
- Create: `ontology/entities/methods/EPERM.md`
- Create: `ontology/entities/methods/ToG.md`
- Create: `ontology/entities/methods/KnowPath.md`
  - Materialize these only because PathMind already gives stable method identity and relation semantics for them.

### Verification surface
- Test: `python3 scripts/test_method_relation_pipeline.py -v`
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Lock the new normative ontology contract

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/references_method.md`
- Modify: `ontology/entities/methods/index.md`

- [ ] **Step 1: Write the failing test that captures the new normative rules**

Create `scripts/test_method_relation_pipeline.py` with this initial content:

```python
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class MethodRelationPipelineTests(unittest.TestCase):
    def run_lint(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def replace_file(self, rel: str, old: str, new: str) -> None:
        path = ROOT / rel
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding='utf-8')

    def test_docs_still_describe_paper_evaluated_on_and_method_placeholder_before_fix(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        self.assertIn('`[[Paper|Method]] --evaluated_on--> [[Benchmark]]`', graph_standard)
        self.assertIn('`status: placeholder` 的 Method 页按最小占位合同校验', graph_standard)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test to verify the old contract is still present**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: PASS with one test proving the repo still reflects the pre-change contract.

- [ ] **Step 3: Rewrite the global relation-type contract in `ontology/graph-standard.md`**

Replace the relation bullets with this exact block:

```markdown
- `targets_task`：`[[Paper|Method]] --targets_task--> [[Task]]`；表示论文或方法主要面向的研究任务。
- `evaluated_on`：`[[Method]] --evaluated_on--> [[Benchmark]]`；表示方法在某个正式 benchmark 上进行了评测。该关系不再用于 `Paper -> Benchmark`；论文页中的 benchmark 信息只保留在 prose、frontmatter、Evidence 与 Method 邻接投影中。
- `based_on`：`[[Method]] --based_on--> [[Method]]`；表示方法建立在某个上游方法之上，只用于方法演化谱系，不指向概念、框架或场景。若需要表达改进、增强或优化等增量语义，默认写入 `edge_semantics`，而不额外拆分 formal relation。
- `references_method`：`[[Method]] --references_method--> [[Method]]`；表示方法将另一方法作为关键比较对象、借鉴路线或方法参照。该关系与 `based_on` 一起构成方法图谱的核心邻接关系：前者表达参照，后者表达谱系；`references_method` 不驱动 `parent_methods` / `child_methods`。
```

- [ ] **Step 4: Remove Method placeholder from the Method state contract**

Replace the current Method-state block with this exact text:

```markdown
#### Method 页状态分层规则
- `status: processed` 的 Method 页必须满足完整 serving 合同：`## 相关概念`、`## 证据来源`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- `status: partial` 的 Method 页按 semantic-stub 合同校验，至少应具有：`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- Method 不再使用 `status: placeholder` 作为正式中间状态；只要方法身份与 formal relation 已稳定成立，就应直接 materialize 为 `status: partial` 的 Method 页。
```

- [ ] **Step 5: Rename the Method body-structure section and add the explanation prose**

Make these two exact changes in `ontology/graph-standard.md`:

```markdown
- 方法演化与参照关系
```

and then append this paragraph after the Method body bullet list:

```markdown
Method 页中的“方法演化与参照关系”用于面向人类区分两类核心方法邻接：
- `based_on`：上游演化方法 / 严格方法谱系来源
- `references_method`：关键参照方法 / 比较对象 / 借鉴路线

其中 `parent_methods` / `child_methods` 只由 `based_on` 派生；`references_method` 不进入父子方法链。
```

- [ ] **Step 6: Rewrite `ontology/relations/evaluated_on.md` to Method-only**

Replace the whole file body with:

```markdown
## 关系语义说明
- `evaluated_on` 表示某个正式 Method 在某个正式 benchmark 上进行了评测。
- 合法 source：`Method`。
- 合法 target：`Benchmark`。
- 该关系不再用于 `Paper -> Benchmark`；论文页中的 benchmark 讨论应保留在 prose、Evidence 与 Method 的 formal relation 投影中。

## 实例边
- 无
```

- [ ] **Step 7: Rewrite the explanation block in `ontology/relations/references_method.md`**

Replace the explanation block with:

```markdown
## 关系语义说明
- `references_method` 表示某方法将另一方法作为关键比较对象、借鉴路线或方法参照。
- 合法 source：`Method`。
- 合法 target：`Method`。
- 该关系与 `based_on` 一起构成方法图谱的核心邻接关系：`based_on` 表达严格谱系，`references_method` 表达参照与比较。
- `references_method` 不表示方法谱系继承，因此不驱动 `parent_methods` / `child_methods`。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，应保留在 `cites`，不得升格为 `references_method`。

## 实例边
- 无
```

- [ ] **Step 8: Update the method-domain index explanation prose**

Replace the object-domain explanation block in `ontology/entities/methods/index.md` with:

```markdown
## 1. 对象域说明
- 本域收录 Method 节点。
- `status: processed` 与 `status: partial` 的 Method 均可进入“导航入口”。
- Paper placeholder 不承担方法域导航；若方法身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页。
```

- [ ] **Step 9: Update the test so it expects the new normative contract**

Replace the test method from Step 1 with this exact code:

```python
    def test_docs_describe_method_only_evaluated_on_and_no_method_placeholder(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        evaluated_on = (ROOT / 'ontology/relations/evaluated_on.md').read_text(encoding='utf-8')
        references_method = (ROOT / 'ontology/relations/references_method.md').read_text(encoding='utf-8')
        methods_index = (ROOT / 'ontology/entities/methods/index.md').read_text(encoding='utf-8')

        self.assertIn('`[[Method]] --evaluated_on--> [[Benchmark]]`', graph_standard)
        self.assertNotIn('`[[Paper|Method]] --evaluated_on--> [[Benchmark]]`', graph_standard)
        self.assertIn('Method 不再使用 `status: placeholder` 作为正式中间状态', graph_standard)
        self.assertIn('方法演化与参照关系', graph_standard)
        self.assertIn('该关系与 `based_on` 一起构成方法图谱的核心邻接关系', references_method)
        self.assertIn('合法 source：`Method`。', evaluated_on)
        self.assertNotIn('合法 source：`Paper`、`Method`。', evaluated_on)
        self.assertIn('`status: processed` 与 `status: partial` 的 Method 均可进入“导航入口”', methods_index)
```

- [ ] **Step 10: Run the test and lint after the doc changes**

Run: `python3 scripts/test_method_relation_pipeline.py -v && python3 scripts/lint_graph.py`
Expected: the unittest passes; lint may still fail because runtime code and live pages have not yet been updated, but there should be no failures caused by malformed doc edits.

- [ ] **Step 11: Commit the normative contract update**

```bash
git add scripts/test_method_relation_pipeline.py ontology/graph-standard.md ontology/relations/evaluated_on.md ontology/relations/references_method.md ontology/entities/methods/index.md
git commit -m "docs: revise method relation ontology contract"
```

---

### Task 2: Teach lint the new Method-only and partial-Method rules

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Add a failing regression test for rejecting `Paper -> Benchmark`**

Append this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_lint_rejects_paper_evaluated_on_edges(self):
        evaluated_on_path = ROOT / 'ontology/relations/evaluated_on.md'
        original = evaluated_on_path.read_text(encoding='utf-8')

        evaluated_on_path.write_text(
            original
            + "\n- [[Synthetic Paper]] --evaluated_on--> [[Synthetic Benchmark]]\n"
            + "  - source_path: ontology/entities/papers/Synthetic Paper.md\n"
            + "  - target_path: ontology/entities/benchmarks/Synthetic Benchmark.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: SyntheticEvidence\n"
            + "  - evidence_link: [[SyntheticEvidence]]\n"
            + "  - evidence_path: ontology/entities/evidence/SyntheticEvidence.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            evaluated_on_path.write_text(original, encoding='utf-8')

        self.assertIn('Paper may not appear as evaluated_on source: Synthetic Paper', result.stdout + result.stderr)
```

- [ ] **Step 2: Add a failing regression test for rejecting Method placeholder pages**

Append this test method below the prior one:

```python
    def test_lint_rejects_method_placeholder_status(self):
        method_path = ROOT / 'ontology/entities/methods/Synthetic Method.md'
        original_exists = method_path.exists()
        original = method_path.read_text(encoding='utf-8') if original_exists else None

        method_path.write_text(
            """---
title: Synthetic Method
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning]
method_family: [hybrid]
scenario: [enterprise-qa]
research_task: []
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Method

## 当前定位
- 仅用于测试。

## 与知识库现有内容的关系
- 无。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            if original_exists and original is not None:
                method_path.write_text(original, encoding='utf-8')
            else:
                method_path.unlink()

        self.assertIn('Method placeholder status is no longer allowed: ontology/entities/methods/Synthetic Method.md', result.stdout + result.stderr)
```

- [ ] **Step 3: Add a failing regression test for simplified object-page links**

Append this test method below the prior one:

```python
    def test_lint_rejects_generated_display_text_links_on_object_pages(self):
        result = self.run_lint()
        self.assertIn(
            'generated object-page link must omit display alias in ontology/entities/methods/PathMind.md: ../methods/RoG|RoG',
            result.stdout + result.stderr,
        )
```

- [ ] **Step 4: Add new lint helpers for `evaluated_on` source validation and Method placeholder rejection**

In `scripts/lint_graph.py`, directly below `SUPPORTED_BY_ALLOWED_SOURCES`, add:

```python
EVALUATED_ON_ALLOWED_SOURCES = {'Method'}
```

Then add this helper below `validate_supported_by_contract`:

```python
def validate_evaluated_on_contract(errors: list[str]) -> None:
    text = read_text('ontology/relations/evaluated_on.md')
    for src, rel, _dst in extract_ledger_edges(text):
        if rel != 'evaluated_on':
            continue
        source_name = src.split('|', 1)[0]
        source_type = infer_entity_type_from_name(source_name)
        if source_type == 'Paper':
            errors.append(f'Paper may not appear as evaluated_on source: {source_name}')
        elif source_type is None:
            errors.append(f'unknown evaluated_on source type for {source_name}')
        elif source_type not in EVALUATED_ON_ALLOWED_SOURCES:
            errors.append(f'unsupported evaluated_on source type for {source_name}: {source_type}')
```

- [ ] **Step 5: Remove Method placeholder runtime branches and add direct rejection**

Make these exact edits in `scripts/lint_graph.py`:

1. Replace the `method` branch inside `validate_serving_structure` with:

```python
    if page_type == 'method':
        status = frontmatter.get('status')
        if status == 'placeholder':
            page_errors.append(f'Method placeholder status is no longer allowed: {rel}')
            status = 'partial'
        if status == 'partial':
            rules = SERVING_TYPE_RULES['method_partial']
        else:
            rules = SERVING_TYPE_RULES['method_processed']
```

2. Delete this old block entirely:

```python
    if page_type == 'method' and frontmatter.get('status') == 'placeholder' and 'references_method' in text:
        for heading in ['## Formal relations', '### Outgoing', '### Incoming']:
            if heading not in text:
                page_errors.append(f'missing serving heading {heading} in {rel}')
```

- [ ] **Step 6: Enforce simplified generated links on object pages**

Add this helper below `extract_non_formal_relations_text`:

```python
def validate_no_generated_display_aliases(rel: str, text: str) -> list[str]:
    page_errors: list[str] = []
    if not rel.startswith('ontology/entities/'):
        return page_errors
    for match in BODY_WIKILINK_RE.finditer(text):
        link = match.group('link')
        if not link.startswith('../'):
            continue
        if '|' in link:
            page_errors.append(f'generated object-page link must omit display alias in {rel}: {link}')
    return page_errors
```

Then call it in both serving-page loops right after `validate_projection_contract(rel, text)`.

- [ ] **Step 7: Wire the new `evaluated_on` validator into the main error pipeline**

In the main execution block of `scripts/lint_graph.py`, immediately after `validate_supported_by_contract(errors)`, add:

```python
validate_evaluated_on_contract(errors)
```

- [ ] **Step 8: Run the tests to verify they fail before the lint implementation is complete, then rerun after edits**

Run first: `python3 scripts/test_method_relation_pipeline.py -v`
Expected before finishing the lint edits: at least one FAIL showing the new behavior is not yet enforced.

Run again after all edits: `python3 scripts/test_method_relation_pipeline.py -v && python3 scripts/lint_graph.py`
Expected after finishing: unittest PASS; lint may still fail only because pipeline skills/live pages are not yet aligned.

- [ ] **Step 9: Commit the lint-rule update**

```bash
git add scripts/lint_graph.py scripts/test_method_relation_pipeline.py
git commit -m "fix: enforce method relation pipeline lint rules"
```

---

### Task 3: Update `paper-ingest` for references extraction and partial Method candidates
git commit -m "fix: enforce method relation pipeline lint rules"
```

---

### Task 3: Update `paper-ingest` for references extraction and partial Method candidates

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Write the failing contract test in the existing test file**

Append this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_paper_ingest_contract_mentions_references_method_and_method_only_evaluated_on(self):
        skill = (ROOT / '.claude/skills/paper-ingest/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('`references_method` 使用规则：', skill)
        self.assertIn('若仅存在论文级引用事实而缺少稳定方法对象语义，不得从 `cites` 升格为 `references_method`。', skill)
        self.assertNotIn('必须登记 `[[Paper]] --evaluated_on--> [[Benchmark]]`', skill)
        self.assertIn('只要存在明确 benchmark，应登记 `[[Method]] --evaluated_on--> [[Benchmark]]`', skill)
```

- [ ] **Step 2: Run the test to verify the current ingest contract still contains the old evaluated_on rule**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: FAIL because the current skill still mandates paper-level `evaluated_on`.

- [ ] **Step 3: Rewrite the `evaluated_on` rule in `paper-ingest/SKILL.md`**

Replace the current `evaluated_on` bullet block with this exact content:

```markdown
- `evaluated_on`：
  - empirical / method / application 论文只要存在明确 benchmark，必须登记 `[[Method]] --evaluated_on--> [[Benchmark]]`
  - 论文页中的 benchmark 信息保留在 prose、frontmatter 与 Evidence 支撑中，不再生成 `[[Paper]] --evaluated_on--> [[Benchmark]]`
  - survey / framework / taxonomy / dataset / benchmark 类型论文若无统一 benchmark，不生成 `evaluated_on`，并在最终输出中显式写明“按规范豁免”
```

- [ ] **Step 4: Strengthen the missing-upstream Method materialization contract**

In the semantic stub section, replace the existing “最小语义骨架” language with this exact block:

```markdown
对于被 `based_on`、`references_method` 或 `proposes`（target 为 Method）稳定指向、但当前库中尚不存在的上游方法对象：
- 若当前论文已经稳定提供其 Method 身份、正常 `object_semantics` 与至少一条正式方法关系，则必须直接产出 `status: partial` 的 Method 候选，而不是 Method placeholder。
- Method placeholder 不再作为正式中间状态保留；只保留 cited paper placeholder 用于 `cites` target 解析。
```

- [ ] **Step 5: Promote `references_method` to a required relation-candidate family**

In the relation-candidate output list, add `references_method` immediately after `based_on`, and update the required relation coverage sentence to this exact text:

```markdown
`relation_candidates` 必须至少覆盖 `proposes`、`targets_task`、`evaluated_on`、`uses_concept`、`supported_by`、`cites`、`based_on`、`references_method`、`sourced_from`
```

- [ ] **Step 6: Add the based_on vs references_method routing rule to the Method extraction section**

Insert this exact paragraph under `### 方法页`:

```markdown
当上游方法关系表达严格方法谱系、继承来源或明确建立在某方法之上时，优先产出 `based_on`；当表达关键比较对象、借鉴路线或方法参照但不构成谱系继承时，优先产出 `references_method`。
```

- [ ] **Step 7: Re-run the test to verify the ingest contract now matches the new pipeline design**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: the new ingest-contract test passes.

- [ ] **Step 8: Commit the ingest-contract update**

```bash
git add .claude/skills/paper-ingest/SKILL.md scripts/test_method_relation_pipeline.py
git commit -m "docs: update paper-ingest method relation contract"
```

---

### Task 4: Update `relation-reconciliation` to route core method-neighbor relations

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`

- [ ] **Step 1: Write the failing contract test for reconciliation routing**

Append this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_relation_reconciliation_contract_mentions_partial_method_materialization_and_method_only_evaluated_on(self):
        skill = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('若缺失 target Method 页但其 Method 身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页', skill)
        self.assertIn('`evaluated_on` 只接收 `Method -> Benchmark`', skill)
        self.assertIn('严格谱系才进 `based_on`', skill)
        self.assertIn('比较/借鉴/路线参照进 `references_method`', skill)
```

- [ ] **Step 2: Run the test to verify the current contract is missing the new routing language**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: FAIL because the current reconciliation skill does not yet contain all four required statements.

- [ ] **Step 3: Add the Method-only benchmark-edge rule to `relation-reconciliation/SKILL.md`**

Insert this exact bullet under `补充约束`:

```markdown
- `evaluated_on` 只接收 `Method -> Benchmark`；若候选关系试图把 `Paper` 作为 `evaluated_on` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
```

- [ ] **Step 4: Add the explicit partial Method materialization rule**

Insert this exact paragraph below `## Diff`:

```markdown
若缺失 target Method 页但其 Method 身份已稳定，并且当前论文已提供正常 `object_semantics`、至少一条正式方法关系与至少一个有效 Evidence anchor，则应直接 materialize 为 `status: partial` 的 Method 页，而不是生成 Method placeholder。
```

- [ ] **Step 5: Replace the routing prose with the exact based_on vs references_method split**

Insert this exact block under `## Ledger routing`:

```markdown
方法邻接分流规则：
- 严格谱系才进 `based_on`
- 比较 / 借鉴 / 路线参照进 `references_method`
- 若仅存在论文级引用事实且 Method 身份不稳定，则保留在 `cites`
```

- [ ] **Step 6: Extend the output template to track materialized partial Methods**

Replace the output-template tail with this exact block:

```yaml
affected_pages: []
affected_stub_pages: []
materialized_partial_methods: []
serving_status_recommendations:
  - path: ontology/entities/methods/RoG.md
    recommended_status: partial
    reason: stable Method identity and formal relation exist, but explanatory coverage remains incomplete
```

- [ ] **Step 7: Re-run the test to verify the reconciliation contract now matches the new design**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: the reconciliation-contract test passes.

- [ ] **Step 8: Commit the reconciliation-contract update**

```bash
git add .claude/skills/relation-reconciliation/SKILL.md scripts/test_method_relation_pipeline.py
git commit -m "docs: update relation reconciliation method routing"
```

---

### Task 5: Update projection and index contracts for dual Method relations and simplified links

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md`

- [ ] **Step 1: Write the failing contract test for projection and index behavior**

Append this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_projection_and_index_contracts_cover_dual_method_sections_and_partial_navigation(self):
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        index_sync = (ROOT / '.claude/skills/index-sync/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('## 方法演化与参照关系', projection)
        self.assertIn('上游演化方法', projection)
        self.assertIn('关键参照方法', projection)
        self.assertIn('默认生成 `[[../x]]` 而不是 `[[../x|Name]]`', projection)
        self.assertIn('`partial`：Method 页可进入默认导航入口', index_sync)
```

- [ ] **Step 2: Run the test to verify the current contracts are missing the new behavior**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: FAIL because the current projection/index skill contracts still reflect the old rules.

- [ ] **Step 3: Add the new Method human-readable section contract**

Insert this exact paragraph into `.claude/skills/page-projection-sync/SKILL.md` under `## 自动同步内容`:

```markdown
Method 页中的“方法演化位置”应重构为“方法演化与参照关系”，并分成两个模板化子区块：
- 上游演化方法：解释 `based_on`
- 关键参照方法：解释 `references_method`
```

- [ ] **Step 4: Add the simplified object-link generation rule**

Insert this exact bullet under `## Formal relations 投影格式` in `.claude/skills/page-projection-sync/SKILL.md`:

```markdown
- 对象页与 Evidence 页默认生成 `[[../x]]` 形式的相对 wikilink，不再默认生成 `[[../x|Name]]`；文档路径信息继续保留在 `（文档：
`...`）` 提示中。
```

- [ ] **Step 5: Change partial Method indexing semantics in `.claude/skills/index-sync/SKILL.md`**

Replace the current status bullets with this exact block:

```markdown
- `placeholder`：只进入 non-serving block
- `partial`：Method 页可进入默认导航入口；其他类型仍可被 index 收录但不自动等同 serving-ready
- `serving-ready`：进入默认导航入口
```

- [ ] **Step 6: Add the exact partial Method navigation note under 收录规则**

Append this exact sentence immediately after the status bullets:

```markdown
- 对于 Method 类型，`status: partial` 一旦被 index 收录，即视为可导航对象页，不再额外降级到 placeholder 区块。
```

- [ ] **Step 7: Re-run the test to verify both contracts now reflect the approved design**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: the projection/index contract test passes.

- [ ] **Step 8: Commit the projection/index contract update**

```bash
git add .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md scripts/test_method_relation_pipeline.py
git commit -m "docs: align projection and index method contracts"
```

---

### Task 6: Apply the new live regression shape to PathMind and upstream Methods

**Files:**
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/benchmarks/WebQSP.md`
- Modify: `ontology/entities/benchmarks/CWQ.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/references_method.md`
- Modify: `ontology/relations/based_on.md`
- Modify: `ontology/entities/methods/index.md`
- Create: `ontology/entities/methods/RoG.md`
- Create: `ontology/entities/methods/GCR.md`
- Create: `ontology/entities/methods/EPERM.md`
- Create: `ontology/entities/methods/ToG.md`
- Create: `ontology/entities/methods/KnowPath.md`

- [ ] **Step 1: Write the failing regression test for the live PathMind surface**

Append this test method to `scripts/test_method_relation_pipeline.py`:

```python
    def test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods(self):
        pathmind_paper = (ROOT / 'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md').read_text(encoding='utf-8')
        pathmind_method = (ROOT / 'ontology/entities/methods/PathMind.md').read_text(encoding='utf-8')
        evaluated_on = (ROOT / 'ontology/relations/evaluated_on.md').read_text(encoding='utf-8')
        references_method = (ROOT / 'ontology/relations/references_method.md').read_text(encoding='utf-8')

        self.assertNotIn('`evaluated_on`：WebQSP', pathmind_paper)
        self.assertIn('## 方法演化与参照关系', pathmind_method)
        self.assertIn('关键参照方法', pathmind_method)
        self.assertIn('[[PathMind]] --references_method--> [[GCR]]', references_method)
        self.assertIn('[[PathMind]] --evaluated_on--> [[WebQSP]]', evaluated_on)
        self.assertNotIn('[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]', evaluated_on)
        for name in ['RoG', 'GCR', 'EPERM', 'ToG', 'KnowPath']:
            text = (ROOT / 'ontology/entities/methods' / f'{name}.md').read_text(encoding='utf-8')
            self.assertIn('status: partial', text)
            self.assertIn('## Object semantics', text)
            self.assertIn('## Formal relations', text)
```

- [ ] **Step 2: Run the regression test to verify the current live content still reflects the old behavior**

Run: `python3 scripts/test_method_relation_pipeline.py -v`
Expected: FAIL because PathMind still has paper-level benchmark edges, no `references_method` ledger entries, and no upstream partial Method pages.

- [ ] **Step 3: Rewrite the PathMind Method evolution section**

In `ontology/entities/methods/PathMind.md`, replace this exact block:

```markdown
## 方法演化位置
- 相较 [[../methods/RoG|RoG]] 一类显式路径推理路线，PathMind 更强调路径重要性建模与偏好对齐训练。
```

with:

```markdown
## 方法演化与参照关系
### 上游演化方法
- [[../methods/RoG]]：PathMind 延续显式推理路径路线，并在其上加入路径优先化与偏好对齐机制。

### 关键参照方法
- [[../methods/GCR]]：作为 grounded reasoning path 代表方法，用于对照 PathMind 的路径选择设计。
- [[../methods/EPERM]]：作为 evidence path 增强代表方法，用于对照 PathMind 的路径重要性建模。
- [[../methods/ToG]]：作为 synergy-augmented 代表方法，用于对照多轮交互式推理路线。
- [[../methods/KnowPath]]：作为生成推理路径方向代表方法，用于对照 LLM 生成式路径方案。
```

- [ ] **Step 4: Remove paper-level benchmark formal relations from the PathMind paper page**

In `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`, delete these two exact blocks:

```markdown
- `evaluated_on`：WebQSP（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]
  - edge_semantics: 论文在 WebQSP 上评测 PathMind 的复杂问答效果。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
- `evaluated_on`：CWQ（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ|CWQ]]
  - edge_semantics: 论文在 CWQ 上评测 PathMind 的多跳推理效果。
  - evidence: [[../evidence/PathMind.experiments|PathMind.experiments]]
```

Then simplify the remaining page links by replacing:

```markdown
[[../methods/PathMind|PathMind]]
[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
[[../tasks/kgqa|kgqa]]
[[../tasks/multi-hop-qa|multi-hop-qa]]
[[../concepts/路径优先化|路径优先化]]
[[../concepts/重要推理路径|重要推理路径]]
```

with:

```markdown
[[../methods/PathMind]]
[[../tasks/knowledge-graph-reasoning]]
[[../tasks/kgqa]]
[[../tasks/multi-hop-qa]]
[[../concepts/路径优先化]]
[[../concepts/重要推理路径]]
```

- [ ] **Step 5: Split PathMind’s live method-neighbor ledgers correctly**

Make these exact ledger changes:

1. Keep this one edge in `ontology/relations/based_on.md`:

```markdown
- [[PathMind]] --based_on--> [[RoG]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/RoG.md
  - edge_semantics: PathMind 延续显式推理路径路线，并在其上加入路径优先化与偏好对齐机制。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
```

2. Add these four edges to `ontology/relations/references_method.md`:

```markdown
- [[PathMind]] --references_method--> [[GCR]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/GCR.md
  - edge_semantics: PathMind 将 GCR 作为 grounded reasoning path 代表方法进行路线参照。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind]] --references_method--> [[EPERM]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/EPERM.md
  - edge_semantics: PathMind 将 EPERM 作为 evidence path 增强代表方法进行参照与比较。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind]] --references_method--> [[ToG]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/ToG.md
  - edge_semantics: PathMind 将 ToG 作为 synergy-augmented 代表方法进行路线比较。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
- [[PathMind]] --references_method--> [[KnowPath]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/KnowPath.md
  - edge_semantics: PathMind 将 KnowPath 作为 LLM 生成推理路径方向代表方法进行参照。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
```

3. In `ontology/relations/evaluated_on.md`, keep only the Method-sourced PathMind edges:

```markdown
- [[PathMind]] --evaluated_on--> [[WebQSP]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/benchmarks/WebQSP.md
  - edge_semantics: 方法在 WebQSP 上取得最优结果。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
- [[PathMind]] --evaluated_on--> [[CWQ]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/benchmarks/CWQ.md
  - edge_semantics: 方法在 CWQ 上取得最优结果。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
```

- [ ] **Step 6: Create the five upstream partial Method pages**

Create `ontology/entities/methods/RoG.md` with this exact content:

```markdown
---
title: RoG
type: 基础方法
parent_methods: []
child_methods: [PathMind]
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# RoG

## Object semantics
- 一种显式推理路径导向的知识图谱推理方法，代表 retrieval-augmented 路线中的关系路径推理方案。

## 当前定位
- 当前作为 PathMind 的严格上游演化方法。

## 与知识库现有内容的关系
- 被 [[PathMind]] 作为 `based_on` 上游方法引用。

## 最小定义/角色
- 代表显式路径推理路线，为 PathMind 的路径优先化扩展提供上游方法基础。

## 待补充
- 正式方法定义、独立 evidence 与更多邻接方法页。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `based_on`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 延续显式推理路径路线，并在其上加入路径优先化与偏好对齐机制。
  - evidence: [[../evidence/PathMind.refs]]
```

Create `ontology/entities/methods/GCR.md` with this exact content:

```markdown
---
title: GCR
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# GCR

## Object semantics
- 一种 grounded reasoning path 知识图谱推理方法，代表 grounded 路线的参考方法。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[PathMind]] 作为 `references_method` 代表方法引用。

## 最小定义/角色
- 代表 grounded reasoning path 设计，用于对照 PathMind 的路径选择与解释性方案。

## 待补充
- 正式方法定义、独立 evidence 与更多上下游邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 GCR 作为 grounded reasoning path 代表方法进行路线参照。
  - evidence: [[../evidence/PathMind.refs]]
```

Create `ontology/entities/methods/EPERM.md` with this exact content:

```markdown
---
title: EPERM
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa]
industry: [general]
research_role: [foundational]
status: partial
---

# EPERM

## Object semantics
- 一种 evidence path enhanced 知识图谱问答方法，代表 evidence-path 增强路线。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[PathMind]] 作为 `references_method` 代表方法引用。

## 最小定义/角色
- 代表 evidence-path 增强设计，用于对照 PathMind 的路径重要性建模与结构化推理方案。

## 待补充
- 正式方法定义、独立 evidence 与更多任务邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 EPERM 作为 evidence path 增强代表方法进行参照与比较。
  - evidence: [[../evidence/PathMind.refs]]
```

Create `ontology/entities/methods/ToG.md` with this exact content:

```markdown
---
title: ToG
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# ToG

## Object semantics
- 一种通过 LLM 与知识图谱多轮交互进行路径搜索的 synergy-augmented 知识图谱推理方法。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[PathMind]] 作为 `references_method` 的协同增强路线代表方法引用。

## 最小定义/角色
- 代表多轮交互式推理路线，用于对照 PathMind 对低交互成本结构化推理的设计。

## 待补充
- 正式方法定义、独立 evidence 与完整 benchmark 邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 ToG 作为 synergy-augmented 代表方法进行路线比较。
  - evidence: [[../evidence/PathMind.refs]]
```

Create `ontology/entities/methods/KnowPath.md` with this exact content:

```markdown
---
title: KnowPath
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, multi-hop-qa]
industry: [general]
research_role: [foundational]
status: partial
---

# KnowPath

## Object semantics
- 一种利用 LLM 生成推理路径的知识图谱推理方法，代表生成式 inference-path 路线。

## 当前定位
- 当前作为 PathMind 的关键参照方法。

## 与知识库现有内容的关系
- 被 [[PathMind]] 作为 `references_method` 的生成式路径代表方法引用。

## 最小定义/角色
- 代表生成式推理路径方法，用于对照 PathMind 的显式路径优先化设计。

## 待补充
- 正式方法定义、独立 evidence 与更多方法邻接。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 KnowPath 作为 LLM 生成推理路径方向代表方法进行参照。
  - evidence: [[../evidence/PathMind.refs]]
```

- [ ] **Step 7: Remove paper-level benchmark projections from benchmark pages and simplify links**

In both `ontology/entities/benchmarks/WebQSP.md` and `ontology/entities/benchmarks/CWQ.md`, delete the incoming `evaluated_on` item whose source is the PathMind paper, and simplify object links so they use `[[../methods/PathMind]]` and not `[[../methods/PathMind|PathMind]]`.

- [ ] **Step 8: Add the new partial Methods to the live method-domain index**

Replace the managed block in `ontology/entities/methods/index.md` with this exact content:

```markdown
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- PathMind 入口（文档：`ontology/entities/methods/PathMind.md`）：[[ontology/entities/methods/PathMind]]
  - object_semantics: 一种面向知识图谱推理的 retrieve-prioritize-reason 集成方法，通过路径优先化与路径偏好对齐引导 LLM 使用高价值推理路径。
  - status: serving-ready
- RoG 入口（文档：`ontology/entities/methods/RoG.md`）：[[ontology/entities/methods/RoG]]
  - object_semantics: 一种显式推理路径导向的知识图谱推理方法，代表 retrieval-augmented 路线中的关系路径推理方案。
  - status: partial
- GCR 入口（文档：`ontology/entities/methods/GCR.md`）：[[ontology/entities/methods/GCR]]
  - object_semantics: 一种 grounded reasoning path 知识图谱推理方法，代表 grounded 路线的参考方法。
  - status: partial
- EPERM 入口（文档：`ontology/entities/methods/EPERM.md`）：[[ontology/entities/methods/EPERM]]
  - object_semantics: 一种 evidence path enhanced 知识图谱问答方法，代表 evidence-path 增强路线。
  - status: partial
- ToG 入口（文档：`ontology/entities/methods/ToG.md`）：[[ontology/entities/methods/ToG]]
  - object_semantics: 一种通过 LLM 与知识图谱多轮交互进行路径搜索的 synergy-augmented 知识图谱推理方法。
  - status: partial
- KnowPath 入口（文档：`ontology/entities/methods/KnowPath.md`）：[[ontology/entities/methods/KnowPath]]
  - object_semantics: 一种利用 LLM 生成推理路径的知识图谱推理方法，代表生成式 inference-path 路线。
  - status: partial
<!-- END MANAGED BLOCK:navigation-entries -->
```

- [ ] **Step 9: Run the live regression and lint**

Run: `python3 scripts/test_method_relation_pipeline.py -v && python3 scripts/lint_graph.py`
Expected: PASS on both commands.

- [ ] **Step 10: Commit the live PathMind regression update**

```bash
git add ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md ontology/entities/methods/PathMind.md ontology/entities/benchmarks/WebQSP.md ontology/entities/benchmarks/CWQ.md ontology/entities/methods/index.md ontology/entities/methods/RoG.md ontology/entities/methods/GCR.md ontology/entities/methods/EPERM.md ontology/entities/methods/ToG.md ontology/entities/methods/KnowPath.md ontology/relations/evaluated_on.md ontology/relations/references_method.md ontology/relations/based_on.md scripts/test_method_relation_pipeline.py
git commit -m "feat: materialize core method relation workflow"
```

---

### Task 7: Final verification and governance handoff

**Files:**
- Verify: `ontology/graph-standard.md`
- Verify: `ontology/relations/evaluated_on.md`
- Verify: `ontology/relations/references_method.md`
- Verify: `.claude/skills/paper-ingest/SKILL.md`
- Verify: `.claude/skills/relation-reconciliation/SKILL.md`
- Verify: `.claude/skills/page-projection-sync/SKILL.md`
- Verify: `.claude/skills/index-sync/SKILL.md`
- Verify: `scripts/lint_graph.py`
- Verify: `scripts/test_method_relation_pipeline.py`
- Verify: PathMind regression pages and ledgers

- [ ] **Step 1: Run the full verification commands**

Run:

```bash
python3 scripts/test_method_relation_pipeline.py -v && python3 scripts/lint_graph.py
```

Expected:
- unittest output ends with `OK`
- lint output is exactly `PASS: graph lint succeeded`

- [ ] **Step 2: Run ontology semantic review on the changed files**

Run the normal workflow entry that reviews the changed ontology files for:
- `based_on` vs `references_method` correctness
- absence of `Paper -> Benchmark`
- correct use of partial Method pages

Expected: no high-priority semantic issues.

- [ ] **Step 3: Run serving-governance review on the changed serving pages and method index**

Review at least these pages:
- `ontology/entities/methods/PathMind.md`
- `ontology/entities/methods/RoG.md`
- `ontology/entities/methods/GCR.md`
- `ontology/entities/methods/EPERM.md`
- `ontology/entities/methods/ToG.md`
- `ontology/entities/methods/KnowPath.md`
- `ontology/entities/methods/index.md`
- `ontology/entities/benchmarks/WebQSP.md`
- `ontology/entities/benchmarks/CWQ.md`

Expected: pages are structurally navigable, Method partials are indexable, and benchmark pages no longer expose paper-level benchmark edges.

- [ ] **Step 4: Create the final integration commit**

```bash
git add ontology .claude/skills scripts
git commit -m "feat: optimize method relation compile pipeline"
```

---

## Spec coverage check

This plan covers every approved requirement from `docs/superpowers/specs/2026-05-10-kg-method-relation-pipeline-design.md`:
- `evaluated_on` global contraction → Task 1, Task 2, Task 6
- `references_method` as pipeline-core relation → Task 1, Task 3, Task 4, Task 6
- partial Method + Paper placeholder only → Task 1, Task 2, Task 3, Task 4, Task 6
- partial Method enters method navigation → Task 1, Task 5, Task 6
- Method evolution/reference section redesign → Task 1, Task 5, Task 6
- simplified `[[../x]]` links → Task 2, Task 5, Task 6
- PathMind regression proof → Task 6, Task 7

## Self-review

- Placeholder scan: no `TODO`, `TBD`, or “similar to above” placeholders remain.
- Internal consistency: all tasks use the same decisions — Method-only `evaluated_on`, no Method placeholder, partial Method in method navigation, and simplified `[[../x]]` object-page links.
- Scope check: the plan stays within one coherent subsystem — the single-paper method-relation compile pipeline.

Plan complete and saved to `docs/superpowers/plans/2026-05-10-kg-method-relation-pipeline.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
