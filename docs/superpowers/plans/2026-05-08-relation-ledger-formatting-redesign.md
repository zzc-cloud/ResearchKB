# Relation Ledger Formatting Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the new canonical relation-ledger format the managed output of the full ResearchKB compile chain, from candidate extraction through reconciliation, projection sync, structural governance, ontology semantic governance, and serving governance.

**Architecture:** Keep relation truth ownership in `relation-reconciliation`, not in ingest or projection. `paper-ingest` emits richer normalized candidate metadata, `relation-reconciliation` renders the canonical ledger markdown and migrates existing ledgers, `page-projection-sync` consumes the normalized truth without owning ledger presentation, and governance stages enforce the new contract so the format cannot drift back.

**Tech Stack:** Obsidian Markdown, Claude skills (`paper-ingest`, `relation-reconciliation`, `page-projection-sync`, `ontology-semantic-review`, `serving-governance-review`), Python (`scripts/lint_graph.py`), managed ontology markdown in `ontology/`.

---

## File map

### Normative spec / ontology contract
- Modify: `ontology/graph-standard.md`
  - Replace the current canonical relation-ledger record contract in section 4.2.
  - Add the new allowed-wikilink rule, fixed child-field order, `文档路径：` requirement, and compile-stage responsibility boundaries.

### Managed relation ledgers
- Modify:
  - `ontology/relations/cites.md`
  - `ontology/relations/proposes.md`
  - `ontology/relations/based_on.md`
  - `ontology/relations/targets_task.md`
  - `ontology/relations/uses_concept.md`
  - `ontology/relations/evaluated_on.md`
  - `ontology/relations/supported_by.md`
  - `ontology/relations/sourced_from.md`
  - Rewrite top sections from navigation-oriented blocks into relation-semantic explanation sections.
  - Rewrite all instance-edge records into canonical field order and path-rich format.

### Compile-chain skill contracts
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Require normalized path-rich candidate metadata.
  - Remove or weaken any instruction that implies ingest owns final relation-ledger presentation.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Make reconciliation the canonical ledger formatter.
  - Define canonical record rendering, uniqueness fallback, allowed jump surfaces, and page-level section structure.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Update assumptions so it reads the new ledger shape and only projects truth.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Expand review scope to relation-semantic explanation quality and new ledger semantics.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Add checks for the separation between governance ledgers and serving pages.

### Governance code
- Modify: `scripts/lint_graph.py`
  - Replace old full-edge ledger assumptions with the new canonical relation-ledger parser and checks.

### Eval / checklist fixtures
- Modify:
  - `.claude/skills/paper-ingest/evals/regression-samples.json`
  - `.claude/skills/paper-ingest/evals/trigger-evals.json`
  - `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
  - `.claude/skills/relation-reconciliation/evals/regression-samples.json`
  - `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - `.claude/skills/ontology-semantic-review/evals/evals.json`
  - Any semantic / serving reference docs that encode old relation-ledger assumptions.

### Tests / verification
- Modify: `scripts/test_lint_graph.py`
  - Add coverage for canonical relation-ledger validation.

---

### Task 1: Update the normative ontology contract

**Files:**
- Modify: `ontology/graph-standard.md`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Read the current relation-ledger contract section and identify the exact replacement range**

Read and target the current block beginning at the `## 4. 关系账本与证据契约` section, especially the old canonical example under section 4.2 that currently says:

```md
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: 关系成立原因
  - evidence: [[证据页]]
```

Expected: You identify the existing canonical record description and the serving-projection section that still assumes old full-edge display.

- [ ] **Step 2: Write the failing lint expectation mentally before editing**

The new contract must require:

```md
- formal relation ledger 页面固定由“关系语义说明区”和“实例边账本区”构成。
- relation 页中的 Obsidian 跳转仅允许出现在实例边主行的 source、target，以及子项中的 `evidence_link`。
- 每条正式实例边必须按固定顺序显式提供：`source_path`、`target_path`、`reason`、`evidence`、`evidence_link`、`evidence_path`。
- `source_path`、`target_path`、`evidence_path` 必须使用 `文档路径：` 前缀。
- `source`、`target`、`evidence_link` 默认使用短 wikilink；若 basename 不唯一，则退化为带路径的 wikilink。
```

Expected: After this step, you know exactly which normative needles `scripts/lint_graph.py` must later enforce.

- [ ] **Step 3: Replace the old canonical relation-record contract with the new one**

Insert a canonical example like:

```md
## 4.2 实例边记录格式
规范格式（canonical）：

```markdown
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: 文档路径：ontology/entities/methods/PathMind.md
  - target_path: 文档路径：ontology/entities/tasks/kgqa.md
  - reason: PathMind 在知识图谱问答任务上验证有效性。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: 文档路径：ontology/entities/evidence/PathMind.sections.md
```

约束：
- relation 页固定由“关系语义说明区”和“实例边账本区”构成。
- relation 页顶部不再保留对象域导航、证据入口导航及其他非必要跳转。
- 仅允许主行 source、主行 target、以及 `evidence_link` 使用 Obsidian wikilink。
- 子项顺序固定为：`source_path`、`target_path`、`reason`、`evidence`、`evidence_link`、`evidence_path`。
- 三个 path 字段必须显式使用 `文档路径：` 前缀。
```

- [ ] **Step 4: Add compile-stage responsibility wording**

Add wording like:

```md
- `paper-ingest` 负责产出可渲染的规范化 relation candidate 元数据，不直接定义 relation ledger 最终 markdown 表示。
- `relation-reconciliation` 是 relation ledger 的最终格式写盘阶段，负责唯一性判断、短 wikilink / 带路径 wikilink 退化与 canonical record 渲染。
- `page-projection-sync` 只消费 formal relation truth，不定义 relation 页表示层。
```

- [ ] **Step 5: Run lint to capture expected failures before downstream fixes**

Run: `python3 scripts/lint_graph.py`

Expected: FAIL, likely because ledgers, skill docs, and lint rules still reflect the old format.

- [ ] **Step 6: Commit the contract change**

```bash
git add ontology/graph-standard.md
git commit -m "docs: define canonical relation ledger format"
```

### Task 2: Update paper-ingest to emit path-rich relation candidates

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Test: `.claude/skills/paper-ingest/evals/trigger-evals.json`

- [ ] **Step 1: Write the failing contract example into the ingest eval fixture**

Add or update a regression sample so the expected candidate payload includes fields like:

```yaml
relation_candidates:
  - relation: targets_task
    source_name: PathMind
    source_type: Method
    source_path: ontology/entities/methods/PathMind.md
    target_name: kgqa
    target_type: Task
    target_path: ontology/entities/tasks/kgqa.md
    reason: PathMind 在知识图谱问答任务上验证有效性。
    evidence_name: PathMind.sections
    evidence_path: ontology/entities/evidence/PathMind.sections.md
```

Expected: The eval now fails against the current skill contract because those fields are not yet required.

- [ ] **Step 2: Update the skill contract to require normalized candidate metadata**

In `.claude/skills/paper-ingest/SKILL.md`, replace generic candidate wording with explicit required fields:

```md
每条 relation candidate 至少包含：
- `relation`
- `source_name`
- `source_type`
- `source_path`
- `target_name`
- `target_type`
- `target_path`
- `reason`
- `evidence_name`
- `evidence_path`
```

- [ ] **Step 3: Remove presentation ownership from ingest**

Add wording like:

```md
`paper-ingest` 不直接生成 relation ledger 最终 markdown，不在此阶段决定短 wikilink 还是带路径 wikilink；这些表示层决策由 `relation-reconciliation` 完成。
```

- [ ] **Step 4: Run the ingest evals**

Run: `python3 -m json.tool .claude/skills/paper-ingest/evals/regression-samples.json >/dev/null && python3 -m json.tool .claude/skills/paper-ingest/evals/trigger-evals.json >/dev/null`

Expected: PASS for JSON validity.

- [ ] **Step 5: Commit the ingest contract update**

```bash
git add .claude/skills/paper-ingest/SKILL.md .claude/skills/paper-ingest/evals/regression-samples.json .claude/skills/paper-ingest/evals/trigger-evals.json
git commit -m "docs: enrich ingest relation candidate contract"
```

### Task 3: Make relation-reconciliation the canonical ledger formatter

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Test: `.claude/skills/relation-reconciliation/evals/quality-checklist.md`
- Test: `.claude/skills/relation-reconciliation/evals/regression-samples.json`

- [ ] **Step 1: Add failing checklist expectations for canonical formatting**

Extend the checklist with items like:

```md
- [ ] relation 页固定包含“关系语义说明区”和“实例边账本区”。
- [ ] 实例边子项固定为 `source_path` → `target_path` → `reason` → `evidence` → `evidence_link` → `evidence_path`。
- [ ] relation 页除主行 source/target 与 `evidence_link` 外，不出现其他 wikilink。
- [ ] basename 不唯一时，source/target/evidence_link 自动退化为带路径的 wikilink。
```

- [ ] **Step 2: Rewrite the skill’s normalization target**

Update the `Normalize` section so it no longer normalizes only to:

```md
- source
- relation_type
- target
- evidence
- source_of_claim
```

and instead normalizes to a richer structure such as:

```md
- source_name
- source_type
- source_path
- relation_type
- target_name
- target_type
- target_path
- reason
- evidence_name
- evidence_path
- source_of_claim
```

- [ ] **Step 3: Add canonical rendering rules to the skill**

Add explicit rendering instructions like:

```md
relation-reconciliation 是 relation ledger 的 canonical formatter。
每条实例边必须渲染为：
- 主行：`[[source]] --relation_type--> [[target]]`
- 子项顺序固定：
  - `source_path: 文档路径：...`
  - `target_path: 文档路径：...`
  - `reason: ...`
  - `evidence: ...`
  - `evidence_link: [[...]]`
  - `evidence_path: 文档路径：...`
```

- [ ] **Step 4: Add uniqueness fallback rules**

Add wording like:

```md
`source`、`target`、`evidence_link` 默认使用短 wikilink；若 basename 在 vault 中不唯一，则必须退化为带路径的 wikilink并保留原显示名。
```

- [ ] **Step 5: Add page-level structure rules**

Add wording like:

```md
relation 页顶部的对象域导航和证据入口导航必须移除。
relation 页固定由两部分组成：
1. 关系语义说明区
2. 实例边账本区
```

- [ ] **Step 6: Run JSON validity check on regression fixtures**

Run: `python3 -m json.tool .claude/skills/relation-reconciliation/evals/regression-samples.json >/dev/null`

Expected: PASS for JSON validity.

- [ ] **Step 7: Commit the reconciliation contract update**

```bash
git add .claude/skills/relation-reconciliation/SKILL.md .claude/skills/relation-reconciliation/evals/quality-checklist.md .claude/skills/relation-reconciliation/evals/regression-samples.json
git commit -m "docs: define canonical relation ledger rendering"
```

### Task 4: Migrate the managed relation ledger pages

**Files:**
- Modify: `ontology/relations/cites.md`
- Modify: `ontology/relations/proposes.md`
- Modify: `ontology/relations/based_on.md`
- Modify: `ontology/relations/targets_task.md`
- Modify: `ontology/relations/uses_concept.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/supported_by.md`
- Modify: `ontology/relations/sourced_from.md`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Rewrite one ledger first as the pattern file**

Start with `ontology/relations/targets_task.md` and convert it from the current form:

```md
> 本页是正式关系账本...
> 相关对象域：[[...]]
> 相关证据入口：[[supported_by]]

## `targets_task` 实例边
- ...

## 实例边
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - reason: ...
  - evidence: [[../entities/evidence/PathMind.sections|PathMind.sections]]
```

into the new form:

```md
# targets_task

## 关系语义说明
- `targets_task` 表示方法或论文明确面向某个研究任务。
- 合法 source：`Method`、`Paper`。
- 合法 target：`Task`。
- 与场景相关的落地语义默认写入对象页 `scenario`、正文或 `reason`，不再单独拆分 formal relation。

## 实例边
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: 文档路径：ontology/entities/methods/PathMind.md
  - target_path: 文档路径：ontology/entities/tasks/kgqa.md
  - reason: PathMind 在知识图谱问答任务上验证有效性。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: 文档路径：ontology/entities/evidence/PathMind.sections.md
```

- [ ] **Step 2: Apply the same page shape to the remaining ledgers**

For each relation file, ensure:

```md
# <relation_name>
## 关系语义说明
...
## 实例边
...
```

and remove all navigation-only wikilinks from the explanation area.

- [ ] **Step 3: Apply the fixed field order to every edge record**

Every instance must follow exactly:

```md
- source_path
- target_path
- reason
- evidence
- evidence_link
- evidence_path
```

Expected: No ledger keeps the old `reason + evidence` only shape.

- [ ] **Step 4: Use short wikilinks where basename is unique**

Prefer forms like:

```md
[[PathMind]]
[[kgqa]]
[[PathMind.sections]]
```

Fallback only where names are ambiguous.

- [ ] **Step 5: Run lint after ledger migration**

Run: `python3 scripts/lint_graph.py`

Expected: FAIL or partial progress until lint code and downstream docs are updated, but old top-nav link errors and old edge-shape mismatches should be on the path to removal.

- [ ] **Step 6: Commit the ledger migration**

```bash
git add ontology/relations/cites.md ontology/relations/proposes.md ontology/relations/based_on.md ontology/relations/targets_task.md ontology/relations/uses_concept.md ontology/relations/evaluated_on.md ontology/relations/supported_by.md ontology/relations/sourced_from.md
git commit -m "docs: migrate relation ledgers to canonical format"
```

### Task 5: Update page-projection-sync to consume the new ledger shape

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Test: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Add failing checklist expectations for the new input shape**

Add checklist items like:

```md
- [ ] 能从包含 `source_path` / `target_path` / `evidence` / `evidence_link` / `evidence_path` 的 canonical ledger 记录中读取 formal truth。
- [ ] 不依赖 relation 页顶部导航说明或旧的 `reason + evidence` 简化记录形态。
```

- [ ] **Step 2: Update the skill contract to consume normalized ledger truth**

Add wording like:

```md
`page-projection-sync` 读取 canonical relation ledger record，但不定义 relation 页 markdown 表示；它只消费 source、target、relation、reason、evidence truth，并把它们投影回对象页。
```

- [ ] **Step 3: Preserve the existing serving projection contract explicitly**

Retain or restate the semi-expanded object-page output:

```md
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
```

Expected: This makes it clear that relation-ledger canonical format and object-page serving projection remain different.

- [ ] **Step 4: Run JSON validity check on projection fixtures**

Run: `python3 -m json.tool .claude/skills/page-projection-sync/evals/regression-samples.json >/dev/null`

Expected: PASS for JSON validity.

- [ ] **Step 5: Commit the projection-sync contract update**

```bash
git add .claude/skills/page-projection-sync/SKILL.md .claude/skills/page-projection-sync/evals/quality-checklist.md .claude/skills/page-projection-sync/evals/regression-samples.json
git commit -m "docs: align page projection with canonical ledgers"
```

### Task 6: Teach structural governance the new ledger rules

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `scripts/test_lint_graph.py`

- [ ] **Step 1: Write failing tests for canonical relation-ledger validation**

Add tests shaped like:

```python
from pathlib import Path
from scripts import lint_graph


def test_extract_ledger_edge_requires_main_line_shape():
    text = """
## 实例边
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: 文档路径：ontology/entities/methods/PathMind.md
  - target_path: 文档路径：ontology/entities/tasks/kgqa.md
  - reason: demo
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: 文档路径：ontology/entities/evidence/PathMind.sections.md
"""
    assert "targets_task" in text
```

and

```python
def test_rejects_wikilinks_outside_allowed_relation_positions():
    text = """
## 关系语义说明
- 相关对象域：[[../entities/tasks/index|tasks/index]]
"""
    assert "[[../entities/tasks/index|tasks/index]]" in text
```

These tests should initially fail because the script does not yet validate the new contract.

- [ ] **Step 2: Add dedicated relation-ledger parsing helpers**

Add helpers with signatures like:

```python
def extract_relation_ledger_blocks(text: str) -> tuple[str, str]:
    ...


def parse_relation_instance_records(text: str) -> list[dict[str, str]]:
    ...


def collect_relation_page_wikilinks(text: str) -> list[str]:
    ...
```

- [ ] **Step 3: Add canonical ledger validation rules**

Implement checks for:

```python
- page contains "## 关系语义说明"
- page contains "## 实例边"
- no top navigation block remains
- every edge has source_path / target_path / reason / evidence / evidence_link / evidence_path
- child-field order is fixed
- every path field starts with "文档路径："
- only main-line source/target and evidence_link may contain wikilinks
```

- [ ] **Step 4: Preserve existing serving-page validation without collapsing contracts**

Do not change the object-page projection validation to the relation-ledger format. Keep these separate:

```python
FORMAL_RELATION_RE           # for relation-ledger main line parsing
SEMI_EXPANDED_RELATION_RE    # for object/evidence page serving projections
```

- [ ] **Step 5: Run the lint tests**

Run: `python3 -m pytest scripts/test_lint_graph.py -q`

Expected: PASS.

- [ ] **Step 6: Run the structural lint script**

Run: `python3 scripts/lint_graph.py`

Expected: PASS once all preceding markdown and contract updates are in place.

- [ ] **Step 7: Commit the lint upgrade**

```bash
git add scripts/lint_graph.py scripts/test_lint_graph.py
git commit -m "feat: enforce canonical relation ledger format"
```

### Task 7: Expand ontology-semantic-review for the new ledger semantics

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/ontology-semantic-review/evals/evals.json`

- [ ] **Step 1: Add a failing semantic-review eval scenario**

Add a scenario where a relation page has correct edge triples but incorrect explanation semantics, such as a `targets_task` ledger that describes scenario placement instead of task placement.

Expected: The eval captures that semantic review must now reject bad explanation framing, not just bad edge placement.

- [ ] **Step 2: Update the skill’s review scope**

Add wording like:

```md
除关系实例边本身外，还要审查 relation 页“关系语义说明区”是否与 `ontology/graph-standard.md` 一致，是否足以帮助判断 source/target 合法性与边归属，且不得重新引入导航型噪声。
```

- [ ] **Step 3: Update the scope-rules reference**

Add bullets like:

```md
- relation semantic explanation must match the relation’s formal ontology contract
- explanation prose may not introduce object-domain navigation expectations
- semantics that belong in `reason` must not be promoted into extra formal-edge interpretations
```

- [ ] **Step 4: Update the diff-review playbook**

Add review prompts like:

```md
- Does the relation page explanation still describe legal source and target types?
- Does it explain the boundary between formal relation truth and context-only semantics?
- Does it avoid extra wikilink-based navigation surfaces?
```

- [ ] **Step 5: Validate the eval JSON**

Run: `python3 -m json.tool .claude/skills/ontology-semantic-review/evals/evals.json >/dev/null`

Expected: PASS for JSON validity.

- [ ] **Step 6: Commit the semantic-review contract update**

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/review-scope-rules.md .claude/skills/ontology-semantic-review/references/diff-review-playbook.md .claude/skills/ontology-semantic-review/evals/evals.json
git commit -m "docs: expand semantic review for relation ledgers"
```

### Task 8: Expand serving-governance-review for the new separation of concerns

**Files:**
- Modify: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Add the failing serving expectation into the skill text**

Add a serving-governance concern that would currently be missed:

```md
- relation 页可以更机器友好，但对象页 serving 投影不得被 relation ledger 的 path-rich子项污染。
```

Expected: Before the edit, the skill has no explicit rule about this separation.

- [ ] **Step 2: Update the serving review scope**

Add wording like:

```md
- relation pages should remain governance-oriented truth surfaces, not default serving entry pages
- object pages should remain the primary human-facing serving surfaces
- relation-ledger machine fields must not bleed into object-page serving readability
```

- [ ] **Step 3: Commit the serving-governance update**

```bash
git add .claude/skills/serving-governance-review/SKILL.md
git commit -m "docs: clarify serving boundary for relation ledgers"
```

### Task 9: Run end-to-end verification on the compile-chain contract

**Files:**
- Verify: `ontology/graph-standard.md`
- Verify: `ontology/relations/*.md`
- Verify: `.claude/skills/paper-ingest/SKILL.md`
- Verify: `.claude/skills/relation-reconciliation/SKILL.md`
- Verify: `.claude/skills/page-projection-sync/SKILL.md`
- Verify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Verify: `.claude/skills/serving-governance-review/SKILL.md`
- Verify: `scripts/lint_graph.py`
- Verify: `scripts/test_lint_graph.py`

- [ ] **Step 1: Run unit-style lint tests**

Run: `python3 -m pytest scripts/test_lint_graph.py -q`

Expected: PASS.

- [ ] **Step 2: Run structural governance**

Run: `python3 scripts/lint_graph.py`

Expected: PASS.

- [ ] **Step 3: Run JSON validity checks for updated eval fixtures**

Run: `python3 -m json.tool .claude/skills/paper-ingest/evals/regression-samples.json >/dev/null && python3 -m json.tool .claude/skills/paper-ingest/evals/trigger-evals.json >/dev/null && python3 -m json.tool .claude/skills/relation-reconciliation/evals/regression-samples.json >/dev/null && python3 -m json.tool .claude/skills/page-projection-sync/evals/regression-samples.json >/dev/null && python3 -m json.tool .claude/skills/ontology-semantic-review/evals/evals.json >/dev/null`

Expected: PASS.

- [ ] **Step 4: Manually spot-check one migrated ledger and one serving page**

Check:
- `ontology/relations/targets_task.md`
- `ontology/entities/scenarios/知识图谱推理问答.md`

Verify:
- the ledger uses canonical canonical relation-edge formatting
- the serving page still uses semi-expanded serving projection formatting
- the two layers are structurally different on purpose

- [ ] **Step 5: Commit the verification pass if any final fixups were needed**

```bash
git add ontology/graph-standard.md ontology/relations .claude/skills scripts
git commit -m "test: verify relation ledger formatting pipeline"
```

## Self-review against spec

### Spec coverage
- Relation page structure (`关系语义说明区` + `实例边账本区`): covered in Tasks 1, 3, 4, and 6.
- Allowed wikilink surfaces: covered in Tasks 1, 3, 4, and 6.
- Fixed child-field order: covered in Tasks 1, 3, 4, and 6.
- `文档路径：` path-field requirement: covered in Tasks 1, 3, 4, and 6.
- Short-link uniqueness fallback: covered in Tasks 3 and 4.
- Full compile-chain integration: covered in Tasks 2 through 9.
- Structural governance updates: covered in Task 6.
- Ontology semantic governance updates: covered in Task 7.
- Serving governance updates: covered in Task 8.

### Placeholder scan
- No `TODO` / `TBD` placeholders remain.
- Every code-changing task names exact files.
- Every verification step includes an exact command.
- All relation child-field names match the spec: `source_path`, `target_path`, `reason`, `evidence`, `evidence_link`, `evidence_path`.

### Type consistency
- Ingest candidate fields consistently use `source_name`, `source_type`, `source_path`, `target_name`, `target_type`, `target_path`, `evidence_name`, `evidence_path`.
- Ledger-rendered fields consistently use `source_path`, `target_path`, `reason`, `evidence`, `evidence_link`, `evidence_path`.
- Serving projection remains explicitly separate from ledger formatting.
