# Placeholder and Partial Method Lint Layering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `scripts/lint_graph.py` validate Method pages by status tier (`processed`, `partial`, `placeholder`) instead of forcing every Method page through the full serving-ready contract.

**Architecture:** Keep the change tightly scoped to Method-page lint layering. First codify the status-tier rules in `ontology/graph-standard.md`, then teach `scripts/lint_graph.py` to branch Method-page required headings by frontmatter status, then add focused regression tests and revalidate the GCR/EPERM placeholder-with-formal-relations case.

**Tech Stack:** Markdown ontology spec, Python lint script, Python unittest regression suite, Bash, git

---

## File Structure

- Modify: `ontology/graph-standard.md`
  - Add the explicit Method-page status-tier contract for `processed`, `partial`, and `placeholder`.
- Modify: `scripts/lint_graph.py`
  - Implement Method-page status-sensitive heading validation.
  - Add regression tests for processed/partial/placeholder Method pages and the PathMind → GCR/EPERM placeholder case.
- Verify against existing files:
  - `ontology/entities/methods/GCR.md`
  - `ontology/entities/methods/EPERM.md`
  - `ontology/entities/methods/PathMind.md`

No new skill docs. No change to non-Method page linting in this plan.

### Task 1: Define Method-page status tiers in the graph standard

**Files:**
- Modify: `ontology/graph-standard.md`

- [ ] **Step 1: Write the failing regression test**

```python
    def test_graph_standard_defines_method_status_tiers(self):
        text = (ROOT / 'ontology' / 'graph-standard.md').read_text(encoding='utf-8')
        self.assertIn('`status: processed` 的 Method 页', text)
        self.assertIn('`status: partial` 的 Method 页', text)
        self.assertIn('`status: placeholder` 的 Method 页', text)
        self.assertIn('## 最小定义/角色', text)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
```

Expected: FAIL because the Method-page status tiers are not yet explicitly defined in `ontology/graph-standard.md`.

- [ ] **Step 3: Update `ontology/graph-standard.md` with Method-page layering rules**

Under the Method-page contract or serving contract section, add this exact rule block:

```markdown
#### Method 页状态分层规则
- `status: processed` 的 Method 页必须满足完整 serving 合同：`## 相关概念`、`## 证据来源`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- `status: partial` 的 Method 页按 semantic-stub 合同校验，至少应具有：`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- `status: placeholder` 的 Method 页按最小占位合同校验，至少应具有：`## 当前定位`、`## 与知识库现有内容的关系`、`## 待补充`；若该页已承接 formal relation，则还必须具有 `## Formal relations`、`### Outgoing`、`### Incoming`。
```

- [ ] **Step 4: Re-run the regression test**

Run:

```bash
```

Expected: PASS.

- [ ] **Step 5: Commit the graph-standard change**

```bash
git commit -m "feat: define method page lint status tiers"
```

### Task 2: Make `lint_graph.py` branch Method heading rules by status

**Files:**
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Write the failing regression tests**

```python
    def test_processed_method_still_requires_full_serving_headings(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')
        broken = original.replace('## 相关概念\n', '', 1)
        method_path.write_text(broken, encoding='utf-8')
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')
        combined_output = result.stdout + result.stderr
        self.assertIn('missing serving heading ## 相关概念 in ontology/entities/methods/PathMind.md', combined_output)

    def test_partial_method_can_pass_without_full_method_serving_sections(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'GCR.md'
        original = method_path.read_text(encoding='utf-8')
        partial_page = (
            '---\n'
            'title: GCR\n'
            'type: [基础方法]\n'
            'problem: [reasoning]\n'
            'industry: [general]\n'
            'research_role: [foundational]\n'
            'status: partial\n'
            'tags: [partial, cited-work]\n'
            '---\n\n'
            '# GCR\n\n'
            '## Object semantics\n'
            '- GCR 是图约束推理路线中的 partial 方法页。\n\n'
            '## 当前定位\n'
            '- 当前作为 [[PathMind]] 的关键比较或借鉴路线方法。\n\n'
            '## 与知识库现有内容的关系\n'
            '- 当前被 [[PathMind]] 通过 formal relation 指向。\n\n'
            '## 最小定义/角色\n'
            '- 在当前论文语境中承担图约束推理参照方法角色。\n\n'
            '## 待补充\n'
            '- 正式方法定义、代表论文、技术细节与证据页。\n\n'
            '## Formal relations\n'
            '### Outgoing\n'
            '当前对象作为 source；以下列出当前对象指向的 relation 实例。\n'
            '- 无\n'
            '### Incoming\n'
            '当前对象作为 target；以下列出指向当前对象的 relation 实例。\n'
            '- `references_method`：引用该方法的方法（文档：`ontology/entities/methods/PathMind.md`）：[[PathMind]]\n'
            '  - edge_semantics: PathMind 将当前方法作为关键比较、借鉴或路线参照对象。\n'
            '  - evidence: [[../evidence/PathMind.refs|PathMind.refs]]\n'
        )
        method_path.write_text(partial_page, encoding='utf-8')
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')
        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing serving heading ## 相关概念 in ontology/entities/methods/GCR.md', combined_output)
        self.assertNotIn('missing serving heading ## 证据来源 in ontology/entities/methods/GCR.md', combined_output)

    def test_placeholder_method_with_formal_relations_requires_formal_relation_headings(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'EPERM.md'
        original = method_path.read_text(encoding='utf-8')
        broken = (
            '---\n'
            'title: EPERM\n'
            'type: [基础方法]\n'
            'problem: [reasoning]\n'
            'industry: [general]\n'
            'research_role: [foundational]\n'
            'status: placeholder\n'
            'tags: [placeholder, cited-work]\n'
            '---\n\n'
            '# EPERM\n\n'
            '## 当前定位\n'
            '- 当前作为 [[PathMind]] 的关键上游方法占位节点。\n\n'
            '## 与知识库现有内容的关系\n'
            '- 当前被 [[PathMind]] 作为关键比较、借鉴或路线参照方法引用。\n\n'
            '## 待补充\n'
            '- 正式方法定义、代表论文、技术细节与证据页。\n'
        )
        method_path.write_text(broken, encoding='utf-8')
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')
        combined_output = result.stdout + result.stderr
        self.assertIn('missing serving heading ## Formal relations in ontology/entities/methods/EPERM.md', combined_output)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest \
```

Expected: the `processed` test passes already, but the `partial` and/or `placeholder` tests fail because `lint_graph.py` still applies one uniform Method contract.

- [ ] **Step 3: Update `scripts/lint_graph.py` Method-page serving rules**

Replace the current Method entry in `SERVING_TYPE_RULES` with three explicit rule sets keyed by status. The resulting logic should support:

```python
SERVING_TYPE_RULES = {
    'method_processed': {
        'required_headings': ['## 相关概念', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
    'method_partial': {
        'required_headings': ['## Object semantics', '## 当前定位', '## 与知识库现有内容的关系', '## 最小定义/角色', '## 待补充', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'method_placeholder': {
        'required_headings': ['## 当前定位', '## 与知识库现有内容的关系', '## 待补充'],
        'strong_frontmatter_fields': set(),
    },
    ...
}
```

Then branch in the Method-page validation path using frontmatter `status`:

```python
if page_type == 'method':
    status = frontmatter.get('status')
    if status == 'processed':
        method_rules = SERVING_TYPE_RULES['method_processed']
    elif status == 'partial':
        method_rules = SERVING_TYPE_RULES['method_partial']
    elif status == 'placeholder':
        method_rules = SERVING_TYPE_RULES['method_placeholder']
    else:
        method_rules = SERVING_TYPE_RULES['method_processed']
```

And add one extra placeholder rule:

```python
if page_type == 'method' and frontmatter.get('status') == 'placeholder' and '## Formal relations' in text:
    for heading in ['### Outgoing', '### Incoming']:
        if heading not in text:
            page_errors.append(f'missing serving heading {heading} in {rel}')
```

- [ ] **Step 4: Re-run the regression tests**

Run:

```bash
python3 -m unittest \
```

Expected: all three tests pass.

- [ ] **Step 5: Commit the lint-layering change**

```bash
git commit -m "feat: layer method lint rules by page status"
```

### Task 3: Revalidate the GCR/EPERM placeholder-with-formal-relations case

**Files:**
- Verify: `ontology/entities/methods/GCR.md`
- Verify: `ontology/entities/methods/EPERM.md`

- [ ] **Step 1: Write the concrete validation test for current files**

```python
    def test_current_gcr_and_eperm_placeholder_pages_pass_lint_contract(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing serving heading ## 相关概念 in ontology/entities/methods/GCR.md', combined_output)
        self.assertNotIn('missing serving heading ## 证据来源 in ontology/entities/methods/GCR.md', combined_output)
        self.assertNotIn('missing serving heading ## 相关概念 in ontology/entities/methods/EPERM.md', combined_output)
        self.assertNotIn('missing serving heading ## 证据来源 in ontology/entities/methods/EPERM.md', combined_output)
```

- [ ] **Step 2: Run the validation test**

Run:

```bash
```

Expected: PASS after the lint layering logic is in place.

- [ ] **Step 3: Run the full unittest suite**

Run:

```bash
```

Expected: all tests pass.

- [ ] **Step 4: Run graph lint end-to-end**

Run:

```bash
python3 ./scripts/lint_graph.py
```

Expected:

```text
PASS: graph lint succeeded
```

- [ ] **Step 5: Commit the validation checkpoint**

```bash
git commit -m "test: cover placeholder method lint layering"
```

## Spec Coverage Check

- Update `graph-standard.md` so Method pages are validated by status tier: covered by Task 1.
- Update lint logic to branch on `processed` / `partial` / `placeholder`: covered by Task 2.
- Revalidate the GCR/EPERM placeholder-with-formal-relations case: covered by Task 3.
- Keep scope limited to Method-page lint layering only: enforced by File Structure and task boundaries.

## Placeholder Scan

- No `TODO`, `TBD`, or “similar to above” markers remain.
- Every changed file path is explicit.
- Every verification step includes an exact command and expected result.

## Type / Name Consistency Check

- Status values are consistently `processed`, `partial`, and `placeholder`.
- The Method-page structural tiers match the approved spec in every task.
- The concrete validation case consistently uses `GCR.md` and `EPERM.md` as placeholder-with-formal-relations examples.
