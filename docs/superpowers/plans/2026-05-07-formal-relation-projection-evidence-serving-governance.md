# Formal Relation Projection and Evidence Serving Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update ResearchKB so relation ledgers remain the only formal instance-edge truth source while object pages and Evidence pages use the new semi-expanded serving projection format, `Paper` is removed from `supported_by`, and the full ingest → reconciliation → projection → governance pipeline automatically enforces the new contract.

**Architecture:** First lock the new contract in executable checks by extending `scripts/test_lint_graph.py` and `scripts/lint_graph.py` to understand semi-expanded projections, body-wikilink restrictions, and the contracted `supported_by` semantics. Then update the normative docs and pipeline skills (`CLAUDE.md`, `ontology/graph-standard.md`, `ontology/relations/supported_by.md`, `paper-ingest`, `relation-reconciliation`, `page-projection-sync`, governance skills/evals) so writers and reviewers agree on the same model. Finally, migrate the live PathMind serving pages and Evidence pages, run lint/tests, and confirm the pipeline now preserves the new representation automatically.

**Tech Stack:** Obsidian-flavored Markdown under `ontology/` and `docs/`, Claude skill contracts under `.claude/skills/`, Python 3 `unittest` and repository linting in `scripts/lint_graph.py`, relation ledgers under `ontology/relations/`, serving pages under `ontology/entities/`.

---

## File map

### Normative docs and relation semantics
- Modify: `CLAUDE.md`
  - Remove `Paper` from the conceptual `supported_by` definition and add object-page/Evidence serving constraints to the global workflow description.
- Modify: `ontology/graph-standard.md`
  - Replace the old `supported_by` source contract, define the semi-expanded projection format, forbid Paper↔Evidence formal linkage, and add body-wikilink / pipeline invariants.
- Modify: `ontology/relations/supported_by.md`
  - Remove `Paper` from the allowed source description and delete the three PathMind Paper→Evidence sample edges.

### Lint runtime and tests
- Modify: `scripts/lint_graph.py`
  - Parse semi-expanded projections, validate role sentences, validate body-wikilink subsets, reject Evidence→Paper body links, and reject `Paper` as `supported_by` source.
- Modify: `scripts/test_lint_graph.py`
  - Add regression tests that pin the new projection format, body-link rule, and contracted `supported_by` model.

### Pipeline skill contracts and review gates
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Stop instructing writers to produce Paper→Evidence `supported_by`, add body-link constraints, and hand off the new projection expectations.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Enforce triple identity, forbid `Paper` as `supported_by` source, and describe Evidence/Paper non-linking.
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - Add checks for rejecting Paper→Evidence and preserving affected-page handoff.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Define the semi-expanded projection format, required role sentences, body-link normalization, and Evidence body-link restrictions.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Add checks for path-explicit projection lines and body-wikilink subset enforcement.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Add semantic review focus for contracted `supported_by`, Evidence/Paper non-linking, and overlinked bodies.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Add review heuristics for the new projection and Evidence rules.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Add serving checks for path-explicit projections, role sentences, and click-graph alignment.

### Live serving pages and evidence pages
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/scenarios/知识图谱推理问答.md`
- Modify: `ontology/entities/concepts/路径优先化.md`
- Modify: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/benchmarks/WebQSP.md`
- Modify: `ontology/entities/benchmarks/CWQ.md`
  - Replace legacy full-edge `Formal relations` blocks with the semi-expanded format and keep body wikilinks aligned.
- Modify: `ontology/entities/evidence/PathMind.sections.md`
- Modify: `ontology/entities/evidence/PathMind.refs.md`
- Modify: `ontology/entities/evidence/PathMind.experiments.md`
  - Remove body links to the Paper page, keep `source_file`, and replace legacy full-edge projections with the new serving format.

### Existing design artifacts consulted
- Reference only: `docs/superpowers/specs/2026-05-07-formal-relation-projection-evidence-serving-governance-design.md`
- Reference only: `docs/superpowers/plans/2026-05-03-knowledge-compile-pipeline.md`
- Reference only: `docs/superpowers/plans/2026-05-06-formal-relation-simplification-migration.md`

### Verification surface
- Test: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_paper_supported_by_edges scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_semi_expanded_projection_format scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_evidence_body_links_to_paper scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_body_wikilinks_to_be_projected -v`
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Lock the new serving and `supported_by` contract in tests

**Files:**
- Modify: `scripts/test_lint_graph.py`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Add a regression test that forbids `Paper` as a `supported_by` source**

Append this method near the bottom of `scripts/test_lint_graph.py`, above `if __name__ == '__main__':`:

```python
    def test_lint_graph_rejects_paper_supported_by_edges(self):
        supported_by_path = ROOT / 'ontology' / 'relations' / 'supported_by.md'
        original = supported_by_path.read_text(encoding='utf-8')

        supported_by_path.write_text(
            original
            + "\n- `[[Synthetic Paper]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`\n"
            + "  - reason: test fixture\n"
            + "  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]\n",
            encoding='utf-8',
        )

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
        self.assertIn('Paper may not appear as supported_by source: Synthetic Paper', combined_output)
```

- [ ] **Step 2: Add a regression test that requires the semi-expanded projection format on object pages**

Append this method below the prior one:

```python
    def test_lint_graph_requires_semi_expanded_projection_format(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        broken = original.replace(
            '- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]',
            '- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`',
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
        self.assertIn('legacy full-edge projection found in ontology/entities/methods/PathMind.md', combined_output)
```

- [ ] **Step 3: Add a regression test that forbids Evidence body links to a Paper page**

Append this method below the prior one:

```python
    def test_lint_graph_rejects_evidence_body_links_to_paper(self):
        evidence_path = ROOT / 'ontology' / 'entities' / 'evidence' / 'PathMind.sections.md'
        original = evidence_path.read_text(encoding='utf-8')

        broken = original.replace(
            'PathMind 的问题设定、三模块框架与总体方法定位。',
            'PathMind 的问题设定、三模块框架与总体方法定位，见 [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]。',
        )
        evidence_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            evidence_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('Evidence body may not link to Paper: ontology/entities/evidence/PathMind.sections.md', combined_output)
```

- [ ] **Step 4: Add a regression test that requires every body wikilink to also appear in `Formal relations`**

Append this method below the prior one:

```python
    def test_lint_graph_requires_body_wikilinks_to_be_projected(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        broken = original.replace(
            '相较纯 retrieval-augmented 方法，它更强调路径重要性建模；相较 synergy-augmented 方法，它减少了大搜索空间下的多轮交互成本。',
            '相较纯 retrieval-augmented 方法，它更强调路径重要性建模；也可参考 [[../concepts/LLM增强知识图谱|LLM增强知识图谱]]。',
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
        self.assertIn('body wikilink missing from Formal relations in ontology/entities/methods/PathMind.md: ../concepts/LLM增强知识图谱|LLM增强知识图谱', combined_output)
```

- [ ] **Step 5: Run the four new tests to verify they fail for the current implementation**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_paper_supported_by_edges \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_semi_expanded_projection_format \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_evidence_body_links_to_paper \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_body_wikilinks_to_be_projected -v
```

Expected:
- `FAIL`
- Failures show that `scripts/lint_graph.py` does not yet enforce the new contract
- No syntax or import errors

---

### Task 2: Teach `scripts/lint_graph.py` the semi-expanded projection format and new serving invariants

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Add regex helpers for the semi-expanded projection format and body-link parsing**

In `scripts/lint_graph.py`, directly below `FORMAL_RELATION_RE`, add these definitions:

```python
SEMI_EXPANDED_RELATION_RE = re.compile(
    r"- `(?P<rel>[^`]+)`：(?P<label>[^（]+)（文档：`(?P<doc>[^`]+)`）：\[\[(?P<link_target>[^\]|]+)(?:\|(?P<link_label>[^\]]+))?\]\]"
)
BODY_WIKILINK_RE = re.compile(r"\[\[(?P<link>[^\]]+)\]\]")
ROLE_SENTENCE_BY_HEADING = {
    '### Outgoing': '当前对象作为 source；以下列出当前对象指向的邻接对象。',
    '### Incoming': '当前对象作为 target；以下列出指向当前对象的邻接对象。',
}
SUPPORTED_BY_ALLOWED_SOURCES = {'Method', 'Concept', 'Task', 'Scenario', 'Benchmark'}
ENTITY_TITLE_TO_TYPE = {
    'PathMind': 'Method',
    '路径优先化': 'Concept',
    '重要推理路径': 'Concept',
    'knowledge-graph-reasoning': 'Task',
    'kgqa': 'Task',
    'multi-hop-qa': 'Task',
    '知识图谱推理问答': 'Scenario',
    'WebQSP': 'Benchmark',
    'CWQ': 'Benchmark',
    'PathMind.sections': 'Evidence',
    'PathMind.refs': 'Evidence',
    'PathMind.experiments': 'Evidence',
    'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models': 'Paper',
}
```

- [ ] **Step 2: Replace the old object-page projection parser with a semi-expanded parser**

Replace the existing `extract_formal_relations` function with this pair of helpers:

```python
def extract_legacy_full_edge_lines(text: str) -> list[str]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    return [line.strip() for line in formal_block.splitlines() if FORMAL_RELATION_RE.match(line.strip())]


def extract_projected_links(text: str) -> dict[str, set[str]]:
    if '## Formal relations' not in text:
        return {'Outgoing': set(), 'Incoming': set()}
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    result = {'Outgoing': set(), 'Incoming': set()}
    current = None
    for raw_line in formal_block.splitlines():
        line = raw_line.strip()
        if line == '### Outgoing':
            current = 'Outgoing'
            continue
        if line == '### Incoming':
            current = 'Incoming'
            continue
        if current and (match := SEMI_EXPANDED_RELATION_RE.match(line)):
            result[current].add(match.group('link_target'))
    return result
```

- [ ] **Step 3: Add validators for role sentences, legacy full-edge lines, body-wikilink subset, and Evidence→Paper links**

Insert these helpers below `validate_serving_structure`:

```python
def extract_body_before_formal_relations(text: str) -> str:
    if '## Formal relations' not in text:
        return text
    return text.split('## Formal relations', 1)[0]


def validate_projection_contract(rel: str, text: str) -> list[str]:
    page_errors: list[str] = []
    if '## Formal relations' not in text:
        return page_errors

    formal_block = text.split('## Formal relations', 1)[1]
    for heading, sentence in ROLE_SENTENCE_BY_HEADING.items():
        if heading in formal_block and sentence not in formal_block:
            page_errors.append(f'missing role sentence {heading} in {rel}')

    if extract_legacy_full_edge_lines(text):
        page_errors.append(f'legacy full-edge projection found in {rel}')

    projected = extract_projected_links(text)
    allowed_links = projected['Outgoing'] | projected['Incoming']
    body = extract_body_before_formal_relations(text)
    for match in BODY_WIKILINK_RE.finditer(body):
        link = match.group('link')
        if link.startswith('#'):
            continue
        if '|' in link:
            target = link
        else:
            target = link
        if target not in allowed_links:
            page_errors.append(f'body wikilink missing from Formal relations in {rel}: {target}')

    if rel.startswith('ontology/entities/evidence/'):
        for match in BODY_WIKILINK_RE.finditer(body):
            target = match.group('link')
            if target.startswith('../papers/') or target.startswith('ontology/entities/papers/'):
                page_errors.append(f'Evidence body may not link to Paper: {rel}')
                break

    return page_errors
```

- [ ] **Step 4: Add a `supported_by` source-type validator against the contracted source set**

Insert this helper below `validate_cited_paper_targets`:

```python
def validate_supported_by_contract(errors: list[str]) -> None:
    text = read_text('ontology/relations/supported_by.md')
    for src, rel, _dst in extract_ledger_edges(text):
        if rel != 'supported_by':
            continue
        source_name = src.split('|', 1)[0]
        source_type = ENTITY_TITLE_TO_TYPE.get(source_name)
        if source_type == 'Paper':
            errors.append(f'Paper may not appear as supported_by source: {source_name}')
        elif source_type not in SUPPORTED_BY_ALLOWED_SOURCES:
            errors.append(f'unsupported supported_by source type for {source_name}: {source_type}')
```

- [ ] **Step 5: Wire the new validators into the main lint loop**

In the main lint loop near the existing serving-page checks, make these exact changes:

```python
validate_supported_by_contract(errors)
```

Place that line after `validate_cited_paper_targets(errors)`.

Then, in the `for path in (ROOT / 'ontology').rglob('*.md'):` loop, immediately after `errors.extend(validate_serving_structure(rel, text, page_type))`, add:

```python
        errors.extend(validate_projection_contract(rel, text))
```

- [ ] **Step 6: Run the four new targeted tests again**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_paper_supported_by_edges \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_semi_expanded_projection_format \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_evidence_body_links_to_paper \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_body_wikilinks_to_be_projected -v
```

Expected:
- `OK`
- All four tests pass

- [ ] **Step 7: Run the repository lint to expose the remaining live-page migration failures**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `FAIL`
- Remaining failures are about current docs/skills/pages still using the old contract, not about the new lint code itself

---

### Task 3: Update normative docs to the contracted `supported_by` and serving model

**Files:**
- Modify: `CLAUDE.md`
- Modify: `ontology/graph-standard.md`
- Modify: `ontology/relations/supported_by.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Update the high-level `supported_by` definition in `CLAUDE.md`**

In `CLAUDE.md`, replace:

```markdown
- 支撑关系：`supported_by`
  - 表示对象被某个 Evidence 页面所支撑。
```

with:

```markdown
- 支撑关系：`supported_by`
  - 表示 Method、Concept、Task、Scenario 或 Benchmark 这类正式知识对象被某个 Evidence 页面所支撑。
  - `Paper` 不再作为 `supported_by` 的 source；Evidence 与 Paper 之间也不建立单独 formal relation。
```

- [ ] **Step 2: Add the serving projection and body-link constraints to `CLAUDE.md` query guidance**

In the `### 查询与分析` section of `CLAUDE.md`, replace step 4:

```markdown
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展
```

with:

```markdown
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展；对象页正文中的所有可跳转 wikilink 必须已在 `Formal relations` 中出现，不应通过正文额外暴露 formal graph 之外的对象邻接。
```

Then replace step 5:

```markdown
5. 如涉及机制、实验、引用、基线、统计分析或 provenance 核验，优先读取对应 Evidence 对象页与 `ontology/entities/evidence/`
```

with:

```markdown
5. 如涉及机制、实验、引用、基线、统计分析或 provenance 核验，优先读取对应 Evidence 对象页与 `ontology/entities/evidence/`；Evidence 页保留 `source_file` provenance 锚点，但不通过正文或 formal relation 直接链接回 Paper。
```

- [ ] **Step 3: Replace the `supported_by` relation contract in `ontology/graph-standard.md`**

In `ontology/graph-standard.md`, replace this line:

```markdown
- `supported_by`：`[[Paper|Method|Concept|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`；表示正式知识页由 Evidence 对象页支撑。
```

with:

```markdown
- `supported_by`：`[[Method|Concept|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`；表示正式知识对象页由 Evidence 对象页支撑。`Paper` 不再作为 `supported_by` 的 source；Evidence 与 Paper 之间也不单独建立 formal relation。
```

- [ ] **Step 4: Add the semi-expanded projection format and body-link contract to `ontology/graph-standard.md`**

Immediately after the existing canonical edge-format block in section `4.2 实例边记录格式`, insert:

```markdown
对象页与 Evidence 页中的 `## Formal relations` 不复用上述完整边写法作为 serving projection 默认格式。投影同步后的页面必须使用半展开格式：

```markdown
### Outgoing
当前对象作为 source；以下列出当前对象指向的邻接对象。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]

### Incoming
当前对象作为 target；以下列出指向当前对象的邻接对象。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
```

约束：
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在该页 `Formal relations` 中出现。
- 不允许通过正文额外暴露 formal graph 之外的对象邻接。
- Evidence 页正文不允许直接链接回 Paper；Paper provenance 仅通过 `source_file` 与 `sourced_from` 体系表达。
```

- [ ] **Step 5: Remove `Paper` from the supporting-ledger description and examples**

In `ontology/relations/supported_by.md`, replace:

```markdown
- 常见 source：`Paper`、`Method`、`Concept`、`Task`、`Scenario`、`Benchmark`
```

with:

```markdown
- 常见 source：`Method`、`Concept`、`Task`、`Scenario`、`Benchmark`
```

Then delete these three sample edges entirely:

```markdown
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[../entities/evidence/PathMind.sections|PathMind.sections]]`
  - reason: 论文的方法定位与总体机制由 sections 证据页支撑。
  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[../entities/evidence/PathMind.refs|PathMind.refs]]`
  - reason: 论文的相关工作与引用 grounding 由 refs 证据页支撑。
  - evidence: [[../entities/evidence/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[../entities/evidence/PathMind.experiments|PathMind.experiments]]`
  - reason: 论文的实验结果由 experiments 证据页支撑。
  - evidence: [[../entities/evidence/PathMind.experiments|PathMind.experiments]]
```

- [ ] **Step 6: Run repository lint after the doc updates**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Likely still `FAIL`
- Failures should now mostly point at skill contracts and live pages rather than these three normative docs

---

### Task 4: Update ingest, reconciliation, and projection skill contracts

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Remove Paper→Evidence expectations from `paper-ingest`**

In `.claude/skills/paper-ingest/SKILL.md`, after the `### Step 6: 汇总候选正式关系` heading, add this rule block:

```markdown
补充约束：
- `supported_by` 候选只允许从 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 指向 `Evidence`。
- 不生成 `Paper --supported_by--> Evidence`。
- Evidence 页保留 `source_file` provenance 锚点，但不通过正文或单独 formal relation 直接链接回 Paper。
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在各自的 `Formal relations` 中出现。
```

- [ ] **Step 2: Tighten `relation-reconciliation` around the contracted `supported_by` model**

In `.claude/skills/relation-reconciliation/SKILL.md`, directly below `## Normalize`, add:

```markdown
补充约束：
- 正式 relation 实例唯一按 `relation_type + source + target` 识别。
- `reason`、`evidence`、`status`、`note` 仅作为该实例属性，不构成新实例。
- `supported_by` 只允许 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 作为 source。
- 若候选关系试图把 `Paper` 作为 `supported_by` source，必须归入 `needs_human_review` 或直接判为非法，不得落账。
- 不得新增 Evidence 与 Paper 之间的 formal relation。
```

- [ ] **Step 3: Rewrite `page-projection-sync` to describe the semi-expanded serving format**

In `.claude/skills/page-projection-sync/SKILL.md`, replace the current `## 自动同步内容` list item `1. `## Formal relations`` with:

```markdown
1. `## Formal relations`（使用半展开 serving projection 格式，而不是完整边字符串）
```

Then insert this new section below `## 输入`:

```markdown
## `Formal relations` 投影格式
- 页面必须保留 `### Outgoing` 与 `### Incoming`。
- `### Outgoing` 后必须写：`当前对象作为 source；以下列出当前对象指向的邻接对象。`
- `### Incoming` 后必须写：`当前对象作为 target；以下列出指向当前对象的邻接对象。`
- 每条投影边必须写成：
  - `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
- 不再使用 ``[[Source]] --relation--> [[Target]]`` 作为对象页或 Evidence 页的默认 serving projection 格式。
- 正文中的所有 wikilink 必须是 `Formal relations` 已出现对象链接的子集。
- Evidence 页正文不允许直接链接回 Paper。
```

- [ ] **Step 4: Update the relation-reconciliation eval checklist and sample**

Append these checklist bullets to `.claude/skills/relation-reconciliation/evals/quality-checklist.md`:

```markdown
- [ ] 不会把 `Paper` 作为 `supported_by` source 落入正式 ledger。
- [ ] 识别 formal relation 实例时以 `relation_type + source + target` 为唯一实例身份。
- [ ] 不会引入 Evidence 与 Paper 之间的新 formal relation。
```

Then append this `quality_checks` item in `.claude/skills/relation-reconciliation/evals/regression-samples.json`:

```json
"must reject or surface for review any Paper --supported_by--> Evidence candidate"
```

- [ ] **Step 5: Update the page-projection-sync eval checklist and sample**

Append these checklist bullets to `.claude/skills/page-projection-sync/evals/quality-checklist.md`:

```markdown
- [ ] `### Outgoing` 与 `### Incoming` 后都必须包含固定角色语义句。
- [ ] 每条投影边必须使用 `relation_type` + 语义标签 + 文档路径 + wikilink 的半展开格式。
- [ ] 正文中的 wikilink 不得超出 `Formal relations` 已投影邻接。
- [ ] Evidence 页正文不允许直接链接回 Paper。
```

Then replace the sample `quality_checks` array in `.claude/skills/page-projection-sync/evals/regression-samples.json` with:

```json
[
  "must update parent_methods and child_methods when affected",
  "must emit semi-expanded projection lines with explicit document paths",
  "must include fixed role sentences after Outgoing and Incoming headings",
  "must keep interpretive prose untouched",
  "must report manual followups if prose still needs human review"
]
```

- [ ] **Step 6: Run repository lint to verify the skill contracts now mention the new rules**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Likely still `FAIL`
- Remaining failures should now concentrate on ontology semantic review, serving review, and live content migration

---

### Task 5: Update ontology-semantic-review and serving-governance-review to enforce the new quality gate

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Expand ontology semantic review scope for contracted `supported_by` and overlinked pages**

In `.claude/skills/ontology-semantic-review/SKILL.md`, replace:

```markdown
## 审查重点
检查：
- 实体分类是否正确
- 关系放置是否正确
- 本体位置是否正确
- 是否与现有图谱保持一致
- 是否存在重复 / 冲突 / 伪关系
- 是否存在关系方向错误或粒度不匹配
```

with:

```markdown
## 审查重点
检查：
- 实体分类是否正确
- 关系放置是否正确
- 本体位置是否正确
- 是否与现有图谱保持一致
- 是否存在重复 / 冲突 / 伪关系
- 是否存在关系方向错误或粒度不匹配
- `supported_by` 是否被错误用于 `Paper`
- Evidence 是否通过正文或 formal relation 直接连接回 Paper
- 对象页 / Evidence 页正文中的 wikilink 是否超出 formal relation 已投影邻接
```

- [ ] **Step 2: Add the same review rules to `review-scope-rules.md`**

Append this section to `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`:

```markdown
## Formal projection and Evidence serving rules
- `supported_by` 只允许 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 作为 source；`Paper` 不得作为 source。
- Evidence 与 Paper 之间不建立 formal relation。
- Evidence 页正文不允许直接链接回 Paper。
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在该页 `Formal relations` 中出现。
```

- [ ] **Step 3: Add projection-specific review prompts to `diff-review-playbook.md`**

Append this section to `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`:

```markdown
## Projection-format review prompts
- 若 diff 修改了对象页 `Formal relations`，检查是否仍在使用完整边字符串而不是半展开格式。
- 若 diff 修改了 Evidence 页，检查是否新增了指向 Paper 的正文链接。
- 若 diff 修改了对象页正文，检查新增 wikilink 是否已经在 `Formal relations` 中投影。
- 若 diff 修改了 `supported_by` ledger，检查是否把 `Paper` 放入 source。
```

- [ ] **Step 4: Update the serving review skill to check the new serving-surface contract**

In `.claude/skills/serving-governance-review/SKILL.md`, under `## What to check`, replace the first and third numbered blocks with:

```markdown
1. **Serving completeness**
   - Does every migrated page have `## Formal relations`, `### Outgoing`, and `### Incoming`?
   - Do `### Outgoing` and `### Incoming` each include the fixed role sentence for the current page role?
   - Are projected entries written in the semi-expanded format with relation type, semantic label, document path, and clickable wikilink?
   - Are the required one-hop relations present for the node type?
   - Are evidence links present and useful for drill-down?
```

```markdown
3. **QA traversability**
   - Can an LLM identify the next-hop nodes and relation types directly from the page?
   - Does each projected neighbor expose its document path explicitly?
   - Do page-body wikilinks stay within the projected formal neighbor set?
   - Are there missing key neighbors that would force runtime fallback to `ontology/relations/`?
```

- [ ] **Step 5: Run repository lint after the review-contract updates**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Likely still `FAIL`
- Remaining failures should now be predominantly live ontology pages that still need migration

---

### Task 6: Migrate the live object pages and Evidence pages to the new projection format

**Files:**
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/scenarios/知识图谱推理问答.md`
- Modify: `ontology/entities/concepts/路径优先化.md`
- Modify: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/benchmarks/WebQSP.md`
- Modify: `ontology/entities/benchmarks/CWQ.md`
- Modify: `ontology/entities/evidence/PathMind.sections.md`
- Modify: `ontology/entities/evidence/PathMind.refs.md`
- Modify: `ontology/entities/evidence/PathMind.experiments.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Rewrite `PathMind.md` `Formal relations` into the semi-expanded format**

Replace the entire `## Formal relations` block in `ontology/entities/methods/PathMind.md` with:

```markdown
## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的邻接对象。
- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
- `targets_task`：任务目标（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa|multi-hop-qa]]
- `uses_concept`：采用概念（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化|路径优先化]]
- `uses_concept`：采用概念（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径|重要推理路径]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/WebQSP.md`）：[[../benchmarks/WebQSP|WebQSP]]
- `evaluated_on`：评测基准（文档：`ontology/entities/benchmarks/CWQ.md`）：[[../benchmarks/CWQ|CWQ]]
- `supported_by`：章节与机制证据（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections|PathMind.sections]]
- `supported_by`：实验结果证据（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments|PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的邻接对象。
- `proposes`：由论文提出（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
```

- [ ] **Step 2: Rewrite the four neighbor object pages to the same semi-expanded format**

For each file below, replace the `## Formal relations` block so it uses the same structure: fixed role sentence after each heading, and one line per neighbor in the semi-expanded format.

Files and required links:

- `ontology/entities/tasks/knowledge-graph-reasoning.md`
  - Outgoing: `supported_by` → `../evidence/PathMind.sections`
  - Incoming: `targets_task` ← `../methods/PathMind`, `../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models`
- `ontology/entities/tasks/kgqa.md`
  - Outgoing: `supported_by` → `../evidence/PathMind.sections`
  - Incoming: `targets_task` ← `../methods/PathMind`, `../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models`
- `ontology/entities/tasks/multi-hop-qa.md`
  - Outgoing: `supported_by` → `../evidence/PathMind.sections`
  - Incoming: `targets_task` ← `../methods/PathMind`, `../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models`
- `ontology/entities/scenarios/知识图谱推理问答.md`
  - Outgoing: `supported_by` → `../evidence/PathMind.sections`
  - Incoming: no change in relation types; keep only projected formal neighbors that already exist in ledgers

Use this exact line template for every entry:

```markdown
- `relation_type`：关系语义标签（文档：`ontology/entities/.../<file>.md`）：[[../.../<file>|Display Name]]
```

- [ ] **Step 3: Rewrite concept and benchmark pages to the semi-expanded format**

Apply the same `## Formal relations` replacement pattern to these files:

- `ontology/entities/concepts/路径优先化.md`
- `ontology/entities/concepts/重要推理路径.md`
- `ontology/entities/benchmarks/WebQSP.md`
- `ontology/entities/benchmarks/CWQ.md`

Constraints:
- Keep only links already backed by ledgers.
- Use explicit `ontology/entities/.../<file>.md` document paths in the prose label.
- Keep body wikilinks untouched unless they point to objects not listed in the new projection.

- [ ] **Step 4: Remove Paper links from the three Evidence pages and rewrite their `Formal relations` blocks**

For each of these files:

- `ontology/entities/evidence/PathMind.sections.md`
- `ontology/entities/evidence/PathMind.refs.md`
- `ontology/entities/evidence/PathMind.experiments.md`

make these exact changes:

1. In `## 对应正式知识节点`, delete the Paper bullet:

```markdown
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
```

2. Replace the `## Formal relations` block with the semi-expanded format.

For `PathMind.sections.md`, use:

```markdown
## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的邻接对象。
- `sourced_from`：原始来源（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[../raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf|A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]

### Incoming
当前对象作为 target；以下列出指向当前对象的邻接对象。
- `supported_by`：支撑方法定义（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind|PathMind]]
- `supported_by`：支撑概念定义（文档：`ontology/entities/concepts/路径优先化.md`）：[[../concepts/路径优先化|路径优先化]]
- `supported_by`：支撑概念定义（文档：`ontology/entities/concepts/重要推理路径.md`）：[[../concepts/重要推理路径|重要推理路径]]
- `supported_by`：支撑任务定位（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
- `supported_by`：支撑任务定位（文档：`ontology/entities/tasks/kgqa.md`）：[[../tasks/kgqa|kgqa]]
- `supported_by`：支撑任务定位（文档：`ontology/entities/tasks/multi-hop-qa.md`）：[[../tasks/multi-hop-qa|multi-hop-qa]]
- `supported_by`：支撑场景定位（文档：`ontology/entities/scenarios/知识图谱推理问答.md`）：[[../scenarios/知识图谱推理问答|知识图谱推理问答]]
```

For `PathMind.refs.md`, keep only `sourced_from` in Outgoing and no Paper link in either body or incoming lines.

For `PathMind.experiments.md`, use incoming `supported_by` entries only for `PathMind`, `WebQSP`, and `CWQ`, plus the same `sourced_from` outgoing line.

- [ ] **Step 5: Run the full lint after all page migrations**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`
- If it still fails, remaining errors should be precise migration misses in the touched pages, not systemic contract gaps

---

### Task 7: Run the targeted unittest suite and full verification

**Files:**
- Test: `scripts/test_lint_graph.py`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the targeted new lint-contract tests**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_paper_supported_by_edges \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_semi_expanded_projection_format \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_evidence_body_links_to_paper \
  scripts.test_lint_graph.LintGraphTests.test_lint_graph_requires_body_wikilinks_to_be_projected -v
```

Expected:
- `OK`
- All four tests pass

- [ ] **Step 2: Run the full unittest file**

Run:

```bash
python3 -m unittest scripts.test_lint_graph -v
```

Expected:
- `OK`
- No regressions in pre-existing lint tests

- [ ] **Step 3: Run the repository lint one final time**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`
- Output includes an ontology page count dictionary

- [ ] **Step 4: Commit the completed migration in one focused commit**

```bash
git add \
  CLAUDE.md \
  ontology/graph-standard.md \
  ontology/relations/supported_by.md \
  scripts/lint_graph.py \
  scripts/test_lint_graph.py \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/relation-reconciliation/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  .claude/skills/page-projection-sync/evals/regression-samples.json \
  .claude/skills/ontology-semantic-review/SKILL.md \
  .claude/skills/ontology-semantic-review/references/review-scope-rules.md \
  .claude/skills/ontology-semantic-review/references/diff-review-playbook.md \
  .claude/skills/serving-governance-review/SKILL.md \
  ontology/entities/methods/PathMind.md \
  ontology/entities/tasks/knowledge-graph-reasoning.md \
  ontology/entities/tasks/kgqa.md \
  ontology/entities/tasks/multi-hop-qa.md \
  ontology/entities/scenarios/知识图谱推理问答.md \
  ontology/entities/concepts/路径优先化.md \
  ontology/entities/concepts/重要推理路径.md \
  ontology/entities/benchmarks/WebQSP.md \
  ontology/entities/benchmarks/CWQ.md \
  ontology/entities/evidence/PathMind.sections.md \
  ontology/entities/evidence/PathMind.refs.md \
  ontology/entities/evidence/PathMind.experiments.md

git commit -m "feat: align serving projections with formal relation contract"
```

---

## Spec coverage self-check

- Canonical truth layer preserved by Tasks 3-5 and live projections only being rewritten in Task 6.
- Triple identity and `supported_by` contraction implemented in Tasks 2 and 4.
- Evidence/Paper non-linking implemented in Tasks 3, 4, and 6.
- Body-wikilink subset rule implemented in Tasks 1, 2, and 6.
- Semi-expanded projection format implemented in Tasks 2, 4, and 6.
- Pipeline automation and governance alignment implemented in Tasks 3-5.
- Existing-page migration order implemented in Task 6 and verified in Task 7.

No uncovered spec requirement remains.
