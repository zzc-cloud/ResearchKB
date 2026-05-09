# Relation Instance and Object/Index Semantics Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign ResearchKB so relation ledgers use `edge_semantics` + `evidence`, object pages project full relation instances into incoming/outgoing items, and entity-domain index entries project governed `object_semantics` instead of free-form hook prose.

**Architecture:** First lock the new representation in structural tests so the migration has an executable boundary: relation ledger child-field order, `edge_semantics` naming, object-page projection items carrying `edge_semantics` + `evidence`, and index entries carrying controlled `object_semantics`. Then update the normative docs plus the generation/sync skills (`paper-ingest`, `relation-reconciliation`, `page-projection-sync`, `index-sync`) so formal truth and serving truth use the same semantic field names and projection contract. Finally, update lint, governance skills, eval fixtures, and the live PathMind sample pages/indexes so the full compile pipeline preserves the redesigned model end to end.

**Tech Stack:** Obsidian-flavored Markdown under `ontology/` and `.claude/skills/`, Python 3 `unittest` and repository linting in `scripts/lint_graph.py`, managed index blocks, relation-ledger markdown records, and serving-page projections under `ontology/entities/**`.

---

## File map

### Normative ontology and cognition docs
- Modify: `CLAUDE.md`
  - Update global cognition so object-page `Formal relations` are relation-instance projections and index entries project object-level semantics.
- Modify: `ontology/graph-standard.md`
  - Replace `reason` with `edge_semantics`, define relation-instance projection rules, define `object_semantics` truth source, and redefine index entry semantics as governed projections.

### Formal relation truth layer
- Modify: `ontology/relations/cites.md`
- Modify: `ontology/relations/proposes.md`
- Modify: `ontology/relations/based_on.md`
- Modify: `ontology/relations/targets_task.md`
- Modify: `ontology/relations/uses_concept.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/supported_by.md`
- Modify: `ontology/relations/sourced_from.md`
  - Rename `reason` → `edge_semantics`.
  - Keep canonical child-field order aligned to the new field set.

### Object-page and index serving projections
- Modify: representative serving pages under `ontology/entities/**`
  - At minimum the current PathMind sample set:
    - `ontology/entities/methods/PathMind.md`
    - `ontology/entities/tasks/knowledge-graph-reasoning.md`
    - `ontology/entities/tasks/kgqa.md`
    - `ontology/entities/tasks/multi-hop-qa.md`
    - `ontology/entities/concepts/路径优先化.md`
    - `ontology/entities/concepts/重要推理路径.md`
    - `ontology/entities/benchmarks/WebQSP.md`
    - `ontology/entities/benchmarks/CWQ.md`
    - `ontology/entities/scenarios/知识图谱推理问答.md`
    - `ontology/entities/evidence/PathMind.sections.md`
    - `ontology/entities/evidence/PathMind.refs.md`
    - `ontology/entities/evidence/PathMind.experiments.md`
  - Each projected relation item must include neighbor, `edge_semantics`, and `evidence`.
- Modify: `ontology/entities/papers/index.md`
- Modify: other `ontology/entities/*/index.md` files as needed
  - Replace free trailing hook prose with governed `object_semantics` projection layout.

### Compile-pipeline skills
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Require relation candidates to emit `edge_semantics`, normalized evidence metadata, and object-page `object_semantics` sources.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Reconcile candidate fields into canonical ledgers using `edge_semantics`.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Project one ledger instance to one object-page item including `edge_semantics` + `evidence`.
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Project `object_semantics` from object pages into index managed blocks.

### Governance and lint
- Modify: `scripts/lint_graph.py`
  - Enforce `edge_semantics` field usage, object-page per-instance projection shape, and index `object_semantics` projection shape.
  - Add failing tests first for the new field names and projection requirements.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Update semantic review expectations from `reason` to `edge_semantics` and from free hooks to `object_semantics`.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Update serving review to check instance-semantic projections and index-level `object_semantics` readability.

### Eval / checklist fixtures
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Replace `reason` references with `edge_semantics` and encode the new projection contract.

### Verification surface
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Lock the new semantic field names and projection contract in tests

**Files:**

- [ ] **Step 1: Add a failing test that relation ledgers must use `edge_semantics` instead of `reason`**

```python
    def test_lint_graph_requires_edge_semantics_in_relation_ledgers(self):
        relation_path = ROOT / 'ontology' / 'relations' / 'targets_task.md'
        original = relation_path.read_text(encoding='utf-8')

        broken = original.replace('  - edge_semantics:', '  - reason:', 1)
        relation_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            relation_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('invalid relation child-field order in ontology/relations/targets_task.md', combined_output)
```

- [ ] **Step 2: Add a failing test that object-page projection items must carry both `edge_semantics` and `evidence`**

Insert this method directly below the previous one:

```python
    def test_lint_graph_requires_edge_semantics_and_evidence_in_object_page_projections(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        broken = original.replace(
            '  - edge_semantics: 该方法被明确定位为知识图谱问答任务求解方法。\n  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]',
            '  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]',
            1,
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
        self.assertIn('missing edge_semantics field in projected relation item: ontology/entities/methods/PathMind.md', combined_output)
```

- [ ] **Step 3: Add a failing test that index entries must use projected `object_semantics` fields rather than trailing hook prose**

Insert this method directly below the previous one:

```python
    def test_lint_graph_requires_index_entries_to_use_object_semantics_projection(self):
        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        original = index_path.read_text(encoding='utf-8')

        broken = original.replace(
            '- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] — 提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa，状态=serving-ready',
            '- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]',
            1,
        )
        index_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            index_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('missing object_semantics projection in ontology/entities/papers/index.md', combined_output)
```

- [ ] **Step 4: Run the three new tests and verify they fail for the expected reason**

Run:

```bash
python3 -m unittest \
```

Expected:
- `FAIL`
- Failures show that `scripts/lint_graph.py` does not yet enforce the new representation.
- No syntax or import errors.

---

### Task 2: Update normative docs to the unified semantics model

**Files:**
- Modify: `CLAUDE.md`
- Modify: `ontology/graph-standard.md`
- Test: inspect changed markdown; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Update `CLAUDE.md` query guidance from neighbor projection to relation-instance projection**

In `CLAUDE.md`, replace:

```markdown
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展；对象页正文中的所有可跳转 wikilink 必须已在 `Formal relations` 中出现，不应通过正文额外暴露 formal graph 之外的对象邻接。
```

with:

```markdown
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展；该区块逐条投影 relation ledger 实例边，必须同时保留 relation type、邻接对象、`edge_semantics` 与 `evidence`。对象页正文中的所有可跳转 wikilink 必须已在 `Formal relations` 中出现，不应通过正文额外暴露 formal graph 之外的对象邻接。
```

- [ ] **Step 2: Replace `reason` with `edge_semantics` in the canonical relation record definition**

In `ontology/graph-standard.md`, replace the canonical block under `### 4.2 实例边记录格式` with:

```markdown
```markdown
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - edge_semantics: 关系成立语义
  - evidence: [[证据页]]
```
```

Then replace this explanatory bullet:

```markdown
- `reason` 必须给出最小可审计语义，不可仅写“相关”或“见正文”。
```

with:

```markdown
- `edge_semantics` 必须给出最小可审计语义，不可仅写“相关”或“见正文”。
```

- [ ] **Step 3: Redefine object-page and index-page serving projections in `ontology/graph-standard.md`**

Immediately below the existing semi-expanded projection example in `ontology/graph-standard.md`, insert:

```markdown
对象页中的 `## Formal relations` 不再被视为对象邻接摘要，而是 formal relation instance 的 serving projection。每条投影项必须同时包含：
- relation type
- 邻接对象文档路径与 wikilink
- `edge_semantics`
- `evidence`

推荐格式：

```markdown
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]
```

若同一邻接对象存在多条 formal relation instance，且 `edge_semantics` 或 `evidence` 不同，不得合并，必须逐条投影。

对象域 index 不再使用自由 trailing hook prose；每个对象入口项必须投影对象页真源 `object_semantics`。
```

- [ ] **Step 4: Add an object-level semantic truth-source requirement**

Under the object-page contract section in `ontology/graph-standard.md`, add:

```markdown
- 每个正式对象页必须提供对象级语义真源 `object_semantics`，用于向对象域 `index.md` 投影入口语义；推荐以 `## Object semantics` 区块承载，而不是使用自由 prose hook。
```

- [ ] **Step 5: Run repository lint after the normative doc updates**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Likely still `FAIL`
- Failures should now point to missing implementation in ledgers, pages, index projection, and lint rules rather than outdated docs.

---

### Task 3: Migrate relation-ledger truth from `reason` to `edge_semantics`

**Files:**
- Modify: `ontology/relations/cites.md`
- Modify: `ontology/relations/proposes.md`
- Modify: `ontology/relations/based_on.md`
- Modify: `ontology/relations/targets_task.md`
- Modify: `ontology/relations/uses_concept.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/supported_by.md`
- Modify: `ontology/relations/sourced_from.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Rename every ledger child field from `reason` to `edge_semantics`**

In each of the eight relation ledgers above, replace every line of the form:

```md
  - reason: ...
```

with:

```md
  - edge_semantics: ...
```

Do not change the actual semantic text yet; only rename the field key.

- [ ] **Step 2: Preserve canonical child-field order after the rename**

Ensure each ledger instance block follows the order already expected by the repo’s relation-page lint model, with `edge_semantics` occupying the semantic slot formerly used by `reason`.

If the current canonical order is:

```md
  - source_path: ...
  - target_path: ...
  - reason: ...
  - evidence: ...
  - evidence_link: ...
  - evidence_path: ...
```

then update it to:

```md
  - source_path: ...
  - target_path: ...
  - edge_semantics: ...
  - evidence: ...
  - evidence_link: ...
  - evidence_path: ...
```

- [ ] **Step 3: Run lint to expose the still-missing object/index projection checks**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `FAIL` is acceptable at this stage
- Remaining failures should move from ledger field naming toward object-page and index-page projection requirements

---

### Task 4: Teach lint to enforce `edge_semantics` and projected-instance structure

**Files:**
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Update relation-ledger field-order enforcement to require `edge_semantics`**

In `scripts/lint_graph.py`, update the relation-ledger child-field order constant so it uses `edge_semantics` instead of `reason`.

Use this exact sequence:

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

- [ ] **Step 2: Add parsing for projected relation-instance child fields on object pages**

Below the existing semi-expanded relation regex helpers, add logic that can parse an object-page projected item plus its child fields:

```python
def parse_projected_relation_items(text: str) -> list[dict[str, object]]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    items: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_heading = None
    for raw_line in formal_block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped == '### Outgoing':
            current_heading = 'Outgoing'
            continue
        if stripped == '### Incoming':
            current_heading = 'Incoming'
            continue
        if stripped.startswith('- `') and '（文档：`' in stripped and '）：[[' in stripped:
            current = {'heading': current_heading, 'main_line': stripped, 'fields': []}
            items.append(current)
            continue
        if current is not None and stripped.startswith('- '):
            field_line = stripped[2:]
            if ': ' not in field_line:
                continue
            key, value = field_line.split(': ', 1)
            current['fields'].append((key, value))
    return items
```

- [ ] **Step 3: Enforce `edge_semantics` + `evidence` on every projected relation item**

In `validate_projection_contract`, after the existing body-wikilink checks, add:

```python
    for item in parse_projected_relation_items(text):
        field_map = dict(item['fields'])
        if 'edge_semantics' not in field_map:
            page_errors.append(f'missing edge_semantics field in projected relation item: {rel}')
        if 'evidence' not in field_map:
            page_errors.append(f'missing evidence field in projected relation item: {rel}')
```

- [ ] **Step 4: Add index-entry enforcement for governed `object_semantics`**

In `validate_index_pages`, after the existing document-path checks, add checks that each entry line is followed by a child line starting with `- object_semantics:` and a child line starting with `- status:`.

Use this exact helper:

```python
def validate_index_entry_projection(block: str, rel: str, errors: list[str]) -> None:
    lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith('- '):
            i += 1
            continue
        child_lines = []
        j = i + 1
        while j < len(lines) and lines[j].startswith('  - '):
            child_lines.append(lines[j].strip())
            j += 1
        if not any(cl.startswith('- object_semantics: ') for cl in child_lines):
            errors.append(f'missing object_semantics projection in {rel}')
        if not any(cl.startswith('- status: ') for cl in child_lines):
            errors.append(f'missing status projection in {rel}')
        i = j
```

Call it on both `navigation_block` and `placeholder_block` after format validation.

- [ ] **Step 5: Run the three targeted tests again**

Run:

```bash
python3 -m unittest \
```

Expected:
- `OK`

---

### Task 5: Align generation and projection skills with the new semantic fields

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md`
- Test: inspect files; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Require `edge_semantics` and object-level semantic source in `paper-ingest`**

In `.claude/skills/paper-ingest/SKILL.md`, replace the normalized relation candidate field list under `### Step 6: 汇总候选正式关系` from:

```markdown
- `reason`
```

to:

```markdown
- `edge_semantics`
```

Then append this bullet block immediately below the field list:

```markdown
对象级语义要求：
- 每个正式对象页候选必须同时产出对象级语义真源 `object_semantics`，供后续 `index-sync` 投影到对象域入口项。
- `object_semantics` 用于表达“该对象实例是什么”，不替代 relation candidate 的 `edge_semantics`。
```

- [ ] **Step 2: Update `relation-reconciliation` from `reason` to `edge_semantics`**

In `.claude/skills/relation-reconciliation/SKILL.md`, replace the Normalize bullet list so it uses:

```markdown
- edge_semantics
```

instead of `reason`, and replace any later mentions of “reason” as the instance-semantic field with `edge_semantics`.

- [ ] **Step 3: Upgrade `page-projection-sync` to project full relation instances**

In `.claude/skills/page-projection-sync/SKILL.md`, replace the current example under `## Formal relations 投影格式` with the four-field projection contract:

```markdown
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]
```

Then append:

```markdown
- 每条 relation ledger 实例边必须逐条投影到对象页；即使同一邻接对象重复，若 `edge_semantics` 或 `evidence` 不同，也不得合并。
```

- [ ] **Step 4: Redesign `index-sync` around `object_semantics` projection**

In `.claude/skills/index-sync/SKILL.md`, replace the current managed-block description with one that explicitly says index entries project:

- 文档路径
- wikilink
- `object_semantics`
- `status`

Append this block under `## 自动同步内容`:

```markdown
对象域入口项不再使用自由 trailing hook prose。每个对象入口项必须从对象页真源投影：
- object_path
- object_wikilink
- object_semantics
- status
```

- [ ] **Step 5: Run repository lint after the generation-skill updates**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- Likely still `FAIL`
- Remaining failures should now point at live pages/indexes and governance docs rather than outdated skill contracts.

---

### Task 6: Align governance docs and eval fixtures

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/evals/regression-samples.json`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify: `.claude/skills/page-projection-sync/evals/regression-samples.json`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Rename semantic-review expectations from `reason` to `edge_semantics`**

In `.claude/skills/ontology-semantic-review/SKILL.md`, append to `## 审查重点`:

```markdown
- relation 实例的 `edge_semantics` 是否准确表达边成立语义
- index 入口项投影的 `object_semantics` 是否准确表达对象实例身份
```

- [ ] **Step 2: Update semantic review reference docs**

Append to `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`:

```markdown
- relation ledger 的实例语义字段统一为 `edge_semantics`，不得继续使用 `reason` 作为正式实例字段名。
- 对象页 `Formal relations` 必须逐条投影 relation instance 的 `edge_semantics` 与 `evidence`。
- 对象域 index 的入口语义必须来自对象页真源 `object_semantics`，不得回退为自由 prose hook。
```

Append to `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`:

```markdown
- 若 diff 修改了 relation ledger，检查 `reason` 是否已统一迁为 `edge_semantics`。
- 若 diff 修改了对象页 `Formal relations`，检查每条实例投影是否同时保留 `edge_semantics` 与 `evidence`。
- 若 diff 修改了对象域 index，检查入口项是否投影 `object_semantics` 而不是自由 trailing prose。
```

- [ ] **Step 3: Update serving governance to review full instance projections and object semantics**

In `.claude/skills/serving-governance-review/SKILL.md`, add these bullets:

Under `1. **Serving completeness**`:

```markdown
   - Does every projected relation item include both `edge_semantics` and `evidence`?
```

Under `2. **Serving readability alignment**`:

```markdown
   - Do projected `edge_semantics` lines preserve the formal relation-instance meaning without collapsing distinct instances?
   - Do index entry `object_semantics` lines accurately summarize object identity without drifting into free prose?
```

- [ ] **Step 4: Update reconciliation and projection eval assets**

Append these bullets to `.claude/skills/relation-reconciliation/evals/quality-checklist.md`:

```markdown
- [ ] 正式 relation instance 语义字段统一为 `edge_semantics`，不得继续输出 `reason`。
- [ ] 输出的 evidence 仍必须保留，并与 `edge_semantics` 共同构成可投影的实例语义。
```

In `.claude/skills/relation-reconciliation/evals/regression-samples.json`, replace the old field-order expectation string:

```json
"must write ledger child fields in canonical order: source_path, target_path, reason, evidence, evidence_link, evidence_path"
```

with:

```json
"must write ledger child fields in canonical order: source_path, target_path, edge_semantics, evidence, evidence_link, evidence_path"
```

Append these bullets to `.claude/skills/page-projection-sync/evals/quality-checklist.md`:

```markdown
- [ ] 每条对象页投影项都必须包含 `edge_semantics` 与 `evidence`。
- [ ] 同邻接对象的多条 relation instance 不得被静默合并。
```

Replace the `quality_checks` array in `.claude/skills/page-projection-sync/evals/regression-samples.json` with:

```json
[
  "must update parent_methods and child_methods when affected",
  "must emit semi-expanded projection lines with explicit document paths",
  "must include fixed role sentences after Outgoing and Incoming headings",
  "must project edge_semantics and evidence for every relation instance",
  "must keep repeated neighbor relations separate when edge_semantics or evidence differ",
  "must keep interpretive prose untouched",
  "must report manual followups if prose still needs human review"
]
```

- [ ] **Step 5: Run lint after governance/eval alignment**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `FAIL` is acceptable here if live PathMind sample pages/indexes have not yet been migrated.
- Failures should now point primarily at live content migration gaps.

---

### Task 7: Migrate the live PathMind sample content to the new model

**Files:**
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/concepts/路径优先化.md`
- Modify: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/benchmarks/WebQSP.md`
- Modify: `ontology/entities/benchmarks/CWQ.md`
- Modify: `ontology/entities/scenarios/知识图谱推理问答.md`
- Modify: `ontology/entities/evidence/PathMind.sections.md`
- Modify: `ontology/entities/evidence/PathMind.refs.md`
- Modify: `ontology/entities/evidence/PathMind.experiments.md`
- Modify: `ontology/entities/papers/index.md`
- Modify: other entity-domain indexes as needed
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add `## Object semantics` to the representative object pages**

For each of these files:

- `ontology/entities/methods/PathMind.md`
- `ontology/entities/tasks/knowledge-graph-reasoning.md`
- `ontology/entities/tasks/kgqa.md`
- `ontology/entities/tasks/multi-hop-qa.md`
- `ontology/entities/concepts/路径优先化.md`
- `ontology/entities/concepts/重要推理路径.md`
- `ontology/entities/benchmarks/WebQSP.md`
- `ontology/entities/benchmarks/CWQ.md`
- `ontology/entities/scenarios/知识图谱推理问答.md`

insert a new section near the top:

```md
## Object semantics
<one controlled paragraph describing what this object instance is>
```

Write the paragraph from the page’s existing semantic content; do not invent new ontology claims.

- [ ] **Step 2: Replace projected child field name `reason` with `edge_semantics` in every object-page relation item**

Where object-page `Formal relations` already contain child semantic fields, rename every:

```md
  - reason: ...
```

into:

```md
  - edge_semantics: ...
```

and ensure every projected item also has:

```md
  - evidence: [[...]]
```

- [ ] **Step 3: Expand any PathMind sample page whose projected items still lack `edge_semantics` or `evidence`**

For every projected incoming/outgoing item in the representative sample pages, make sure it includes both lines:

```md
  - edge_semantics: ...
  - evidence: [[...]]
```

If the semantic wording can be copied from the canonical relation ledger, do that exactly rather than paraphrasing loosely.

- [ ] **Step 4: Redesign `ontology/entities/papers/index.md` to use projected `object_semantics` child lines**

Replace entries such as:

```md
- KnowPath 入口（文档：`...`）：[[...]] — PathMind 引用的生成推理路径上游论文，占位节点，状态=placeholder
```

with the projected form:

```md
- KnowPath 入口（文档：`...`）：[[...]]
  - object_semantics: 生成推理路径方向的上游论文，占位节点。
  - status: placeholder
```

Apply the same pattern to the `PathMind` entry and the other placeholder entries in the file.

- [ ] **Step 5: Apply the same index-entry structure to other entity-domain indexes as required by lint**

For any other `ontology/entities/*/index.md` file that still uses free trailing prose hooks, migrate entries to:

```md
- <Entry>
  - object_semantics: ...
  - status: ...
```

Only touch indexes that lint reports as nonconforming.

- [ ] **Step 6: Run repository lint after the live-content migration**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS: graph lint succeeded`

---

### Task 8: Final verification and focused commit

**Files:**
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Run the targeted redesign tests**

Run:

```bash
python3 -m unittest \
```

Expected:
- `OK`

- [ ] **Step 2: Run the full lint unittest suite**

Run:

```bash
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

- [ ] **Step 4: Commit only the files relevant to the redesign**

```bash
git add \
  CLAUDE.md \
  ontology/graph-standard.md \
  ontology/relations/cites.md \
  ontology/relations/proposes.md \
  ontology/relations/based_on.md \
  ontology/relations/targets_task.md \
  ontology/relations/uses_concept.md \
  ontology/relations/evaluated_on.md \
  ontology/relations/supported_by.md \
  ontology/relations/sourced_from.md \
  ontology/entities/methods/PathMind.md \
  ontology/entities/tasks/knowledge-graph-reasoning.md \
  ontology/entities/tasks/kgqa.md \
  ontology/entities/tasks/multi-hop-qa.md \
  ontology/entities/concepts/路径优先化.md \
  ontology/entities/concepts/重要推理路径.md \
  ontology/entities/benchmarks/WebQSP.md \
  ontology/entities/benchmarks/CWQ.md \
  ontology/entities/scenarios/知识图谱推理问答.md \
  ontology/entities/evidence/PathMind.sections.md \
  ontology/entities/evidence/PathMind.refs.md \
  ontology/entities/evidence/PathMind.experiments.md \
  ontology/entities/papers/index.md \
  .claude/skills/paper-ingest/SKILL.md \
  .claude/skills/relation-reconciliation/SKILL.md \
  .claude/skills/page-projection-sync/SKILL.md \
  .claude/skills/index-sync/SKILL.md \
  .claude/skills/ontology-semantic-review/SKILL.md \
  .claude/skills/ontology-semantic-review/references/review-scope-rules.md \
  .claude/skills/ontology-semantic-review/references/diff-review-playbook.md \
  .claude/skills/serving-governance-review/SKILL.md \
  .claude/skills/relation-reconciliation/evals/quality-checklist.md \
  .claude/skills/relation-reconciliation/evals/regression-samples.json \
  .claude/skills/page-projection-sync/evals/quality-checklist.md \
  .claude/skills/page-projection-sync/evals/regression-samples.json \
  scripts/lint_graph.py \

git commit -m "refactor: unify relation and object semantics projections"
```

---

## Spec coverage self-check

- Relation ledger field rename from `reason` to `edge_semantics`: Tasks 1-4
- Object-page incoming/outgoing now project `edge_semantics` + `evidence`: Tasks 1, 4, 5, 7
- Index pages project governed `object_semantics`: Tasks 1, 4, 5, 7
- Full compile-pipeline alignment (`paper-ingest`, `relation-reconciliation`, `page-projection-sync`, `index-sync`): Tasks 2 and 5
- Structural governance alignment: Tasks 1 and 4
- Ontology semantic governance alignment: Task 6
- Serving governance alignment: Task 6
- Representative live content migration: Task 7
- Verification and focused delivery: Task 8

No uncovered spec requirement remains.
