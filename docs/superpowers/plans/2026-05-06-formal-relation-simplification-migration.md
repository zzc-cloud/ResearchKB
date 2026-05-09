# Formal Relation Simplification Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate ResearchKB from the 12-relation formal ledger model to the reduced 8-relation model, carrying forward truth into `based_on` / `uses_concept` / page prose, then update lint and skills so the retired relations stop being produced or expected.

**Architecture:** First lock the reduced relation contract in tests so the migration has an executable boundary. Then update `scripts/lint_graph.py` and the live relation ledgers/pages to remove `improves_on`, `depends_on`, `applies_to`, and `supports` as formal graph truth while preserving their meaning in `reason`, frontmatter, and human-readable sections. Finally, rewrite the ingest / reconciliation / projection / review skills and eval fixtures so the daily pipeline only emits and validates the reduced formal relation set.

**Tech Stack:** Markdown knowledge pages under `ontology/` and `intermediate/`, Claude skill contracts under `.claude/skills/`, Python 3 unittest and repository linting in `scripts/lint_graph.py`, Obsidian wikilinks, grep-based verification.

---

## File map

### Tests and lint runtime
  - Replace 12-ledger expectations with the reduced 8-ledger set.
  - Add regression checks that `scripts/lint_graph.py` no longer expects retired relation types.
- Modify: `scripts/lint_graph.py`
  - Remove retired ledgers from `REQUIRED_FILES`.
  - Remove retired relation edges from `SERVING_READY_SAMPLES`.
  - Update any hard-coded relation-name assertions so they match the reduced model.

### Formal relation truth
- Modify: `ontology/relations/based_on.md`
  - Keep only `based_on` edges; merge former improvement semantics into `reason`.
- Modify: `ontology/relations/uses_concept.md`
  - Keep only `uses_concept` edges; merge former prerequisite semantics into `reason`.
- Modify: `ontology/relations/proposes.md`
- Modify: `ontology/relations/cites.md`
- Modify: `ontology/relations/targets_task.md`
- Modify: `ontology/relations/evaluated_on.md`
- Modify: `ontology/relations/supported_by.md`
- Modify: `ontology/relations/sourced_from.md`
- Delete: `ontology/relations/improves_on.md`
- Delete: `ontology/relations/depends_on.md`
- Delete: `ontology/relations/applies_to.md`
- Delete: `ontology/relations/supports.md`

### Serving pages affected by retired formal edges
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/methods/RoG.md`
- Modify: `ontology/entities/methods/GCR.md`
- Modify: `ontology/entities/methods/EPERM.md`
- Modify: `ontology/entities/methods/ToG.md`
- Modify: `ontology/entities/concepts/路径优先化.md`
- Modify: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/concepts/LLM增强知识图谱.md`
- Modify: `ontology/entities/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/tasks/engineering-design-knowledge-management.md`
- Modify: `ontology/entities/scenarios/知识图谱推理问答.md`
- Modify: `ontology/entities/scenarios/复杂产品设计.md`
  - Remove references to retired formal relations from `## Formal relations` and surrounding human-readable sections.
  - Preserve scenario and support semantics in prose / frontmatter rather than ledger edges.

### Skill and eval contracts
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/ontology-semantic-review/evals/evals.json`
  - Remove retired relation outputs and examples.
  - Reword rules so retired semantics are reviewed as `reason` / prose quality rather than formal edge placement.

---

### Task 1: Lock the reduced relation contract in tests

**Files:**

- [ ] **Step 1: Replace the expected formal ledger list with the reduced set**

Update `test_lint_graph_requires_new_relation_type_ledgers` so `expected` is exactly:

```python
        expected = [
            'ontology/relations/cites.md',
            'ontology/relations/proposes.md',
            'ontology/relations/based_on.md',
            'ontology/relations/targets_task.md',
            'ontology/relations/uses_concept.md',
            'ontology/relations/evaluated_on.md',
            'ontology/relations/supported_by.md',
            'ontology/relations/sourced_from.md',
        ]
```

- [ ] **Step 2: Add a failing regression test for retired relation names**

Add this method below `test_lint_graph_requires_new_relation_type_ledgers`:

```python
    def test_lint_graph_does_not_expect_retired_relation_types(self):
        retired = [
            'ontology/relations/improves_on.md',
            'ontology/relations/depends_on.md',
            'ontology/relations/applies_to.md',
            'ontology/relations/supports.md',
            "('PathMind', 'improves_on', '路径导向知识图谱推理')",
            "('PathMind', 'applies_to', '知识图谱推理问答')",
            "('RoG', 'improves_on', '路径导向知识图谱推理')",
        ]

        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        for needle in retired:
            self.assertNotIn(needle, text)
```

- [ ] **Step 3: Run the new regression tests and verify they fail for the right reason**

Run:

```bash
```

Expected:
- `FAIL`
- Failures mention lingering retired ledger names or retired sample edges in `scripts/lint_graph.py`
- No syntax or import errors

---

### Task 2: Update lint runtime to the 8-relation model

**Files:**
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Reduce the required ledger file list**

In `scripts/lint_graph.py`, replace the 12-item `REQUIRED_FILES` relation block with this 8-item block:

```python
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/based_on.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/uses_concept.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
```

- [ ] **Step 2: Remove retired formal edges from serving samples**

In `SERVING_READY_SAMPLES`, edit the `required_edges` lists so they no longer expect retired relations. Use these exact replacements:

```python
    'ontology/entities/methods/PathMind.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('PathMind', 'based_on', '路径导向知识图谱推理'),
            ('PathMind', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind', 'targets_task', 'kgqa'),
            ('PathMind', 'targets_task', 'multi-hop-qa'),
            ('PathMind', 'uses_concept', '路径优先化'),
            ('PathMind', 'uses_concept', '重要推理路径'),
            ('PathMind', 'evaluated_on', 'WebQSP'),
            ('PathMind', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
        ],
    },
```

```python
    'ontology/entities/methods/RoG.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('RoG', 'based_on', '路径导向知识图谱推理'),
            ('RoG', 'targets_task', 'knowledge-graph-reasoning'),
            ('RoG', 'targets_task', 'kgqa'),
            ('RoG', 'targets_task', 'multi-hop-qa'),
        ],
    },
```

Do the same cleanup anywhere else `SERVING_READY_SAMPLES` still expects `improves_on`, `depends_on`, `applies_to`, or `supports`.

- [ ] **Step 3: Run the targeted unittest set again**

Run:

```bash
```

Expected:
- `OK`
- Both tests pass

- [ ] **Step 4: Run the repository lint script to expose downstream breakage before ledger migration**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- This may still fail
- Any remaining failure should now be about live ledger/page content, not about the retired relation names still being wired into the lint runtime

---

### Task 3: Migrate formal relation truth and serving pages

**Files:**
- Modify: `ontology/relations/based_on.md`
- Modify: `ontology/relations/uses_concept.md`
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/methods/RoG.md`
- Modify: `ontology/entities/methods/GCR.md`
- Modify: `ontology/entities/methods/EPERM.md`
- Modify: `ontology/entities/methods/ToG.md`
- Modify: `ontology/entities/concepts/路径优先化.md`
- Modify: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/concepts/LLM增强知识图谱.md`
- Modify: `ontology/entities/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/tasks/engineering-design-knowledge-management.md`
- Modify: `ontology/entities/scenarios/知识图谱推理问答.md`
- Modify: `ontology/entities/scenarios/复杂产品设计.md`
- Delete: `ontology/relations/improves_on.md`
- Delete: `ontology/relations/depends_on.md`
- Delete: `ontology/relations/applies_to.md`
- Delete: `ontology/relations/supports.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Merge former improvement semantics into `based_on.md` reasons**

Rewrite the affected `based_on` reasons so the improvement detail is preserved in prose. At minimum, the following edges should read like this:

```md
- `[[RoG]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: RoG 采用显式关系推理路径作为核心机制，并推进了路径导向路线的显式推理表达。
  - evidence: [[PathMind.refs|PathMind.refs]] §2–4
```

```md
- `[[GCR]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: GCR 采用 grounded reasoning path 路线，并通过 grounded 约束提升路径可靠性。
  - evidence: [[PathMind.refs|PathMind.refs]] §2–4
```

```md
- `[[EPERM]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: EPERM 采用 evidence path 增强路径推理，并通过证据路径增强改进路径导向推理。
  - evidence: [[PathMind.refs|PathMind.refs]] §2–4
```

```md
- `[[PathMind]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: PathMind 属于路径导向知识图谱推理路线，并通过路径优先化与对齐训练提升推理质量。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4
```

```md
- `[[ToG]] --based_on--> [[协同增强式知识图谱推理]]`
  - reason: ToG 属于协同增强式知识图谱推理路线，并通过多轮 LLM 交互与迭代搜索推进该路线。
  - evidence: [[PathMind.refs|PathMind.refs]] §4
```

- [ ] **Step 2: Merge former prerequisite semantics into `uses_concept.md` reasons**

Add / rewrite the prerequisite-style concept edge like this:

```md
- `[[重要推理路径]] --uses_concept--> [[路径优先化]]`
  - reason: 重要推理路径的识别以路径优先化作为成立前提。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4
```

Keep the existing `PathMind` and paper-level `uses_concept` edges, but ensure none of their reasons imply a separate formal `depends_on` ledger is still required.

- [ ] **Step 3: Remove retired formal edges from serving pages and preserve the meaning in prose/frontmatter**

Update the affected pages so `## Formal relations` only mentions the reduced relation set. Use these exact transformations as the model:

```md
## 应用场景
- 该方法面向知识图谱推理问答场景落地，并在 KGQA 与多跳问答任务上验证有效性。
```

```md
## 与其他概念的关系
- 路径优先化为重要推理路径的识别与筛选提供关键机制支撑。
```

```md
## 相关框架 / 概念
- 复杂产品设计中的 LLM-KG 协同框架以 LLM 增强知识图谱为核心知识组织基础。
```

Specifically:
- Remove `improves_on`, `depends_on`, `applies_to`, and `supports` bullets from `## Formal relations`
- Keep scenario meaning in `scenario:` frontmatter and the human-readable sections
- Keep support/prerequisite meaning in the human-readable concept/task/scenario sections

- [ ] **Step 4: Delete the retired ledger files after all references are migrated**

Delete these files:

```text
ontology/relations/improves_on.md
ontology/relations/depends_on.md
ontology/relations/applies_to.md
ontology/relations/supports.md
```

- [ ] **Step 5: Run lint and verify the relation directory matches the reduced set**

Run:

```bash
ls ontology/relations
python3 scripts/lint_graph.py
```

Expected:
- `ls ontology/relations` lists only the 8 active ledger files
- `python3 scripts/lint_graph.py` either passes or fails only on pipeline contracts that still mention the retired relations

---

### Task 4: Rewrite pipeline skills and eval fixtures to stop producing retired relations

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/ontology-semantic-review/evals/evals.json`
- Test: grep plus `python3 scripts/lint_graph.py`

- [ ] **Step 1: Reduce `paper-ingest` to the 8 formal relation outputs**

In `.claude/skills/paper-ingest/SKILL.md`, replace the formal ledger enumeration in Step 5 with:

```md
   - `ontology/relations/cites.md`
   - `ontology/relations/proposes.md`
   - `ontology/relations/based_on.md`
   - `ontology/relations/targets_task.md`
   - `ontology/relations/uses_concept.md`
   - `ontology/relations/evaluated_on.md`
   - `ontology/relations/supported_by.md`
   - `ontology/relations/sourced_from.md`
```

Replace the candidate summary block with:

```md
- `proposes`
- `targets_task`
- `evaluated_on`
- `uses_concept`
- `supported_by`
- `cites`
- `based_on`
- `sourced_from`
```

Replace the output schema with:

```yaml
relation_candidates:
  proposes: []
  targets_task: []
  evaluated_on: []
  uses_concept: []
  supported_by: []
  cites: []
  based_on: []
  sourced_from: []
```

Also add one explicit sentence after the schema:

```md
- 改进、前提依赖、应用场景与概念性支撑语义默认写入 `reason`、frontmatter 或对象页正文，而不再单独输出为 formal relation candidate。
```

- [ ] **Step 2: Update `relation-reconciliation` and `page-projection-sync` routing rules**

In `.claude/skills/relation-reconciliation/SKILL.md`, replace the routing block with:

```md
## Ledger routing
- `cites` → `ontology/relations/cites.md`
- `proposes` → `ontology/relations/proposes.md`
- `based_on` → `ontology/relations/based_on.md`
- `targets_task` → `ontology/relations/targets_task.md`
- `uses_concept` → `ontology/relations/uses_concept.md`
- `evaluated_on` → `ontology/relations/evaluated_on.md`
- `supported_by` → `ontology/relations/supported_by.md`
- `sourced_from` → `ontology/relations/sourced_from.md`
```

In `.claude/skills/page-projection-sync/SKILL.md`, replace the variant rules with:

```md
## 变体识别规则
- survey 论文页：优先同步 `proposes`、`uses_concept`、`targets_task`、`cites`、`supported_by`，并保留 `evaluated_on` 豁免信息。
- framework 型 Concept 页：优先同步 incoming `proposes`、outgoing `uses_concept`、`supported_by`。
- survey / framework 主线的 Scenario 页：默认不再单独同步场景适配型 formal edge，重排人类区块为“主要框架 / 概念 / 方法”优先。
- survey / framework 主线的 Task 页：优先同步 incoming `targets_task`，并重排人类区块为“相关框架 / 概念 / 场景 / 论文”优先。
```

- [ ] **Step 3: Rewrite ontology semantic review rules to the reduced model**

In `.claude/skills/ontology-semantic-review/SKILL.md`, reduce the “先阅读” ledger list to the active 8 files only.

In `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`, replace the retired-relation checks with:

```md
- 概念 → 论文支撑关系被错误写进 `uses_concept.md`
- 文献支撑关系被错误写进 `based_on.md`
- 本应下沉到 `reason` / frontmatter / 正文的改进、前提依赖、场景适配或概念性支撑语义，被错误升格为新的 formal relation
```

Replace the heuristics block tail with:

```md
- 如果一条关系表达的是“这篇论文支撑 / 梳理 / 解释了这个概念”，优先放在概念页证据区或 `supported_by.md`，而不是误写进 `uses_concept.md`。
- 如果一条关系表达的是文献借鉴或引用支撑，而不是严格的技术演化谱系，优先放在 `cites.md`，而不是 `based_on.md`。
- 如果一条语义只是说明改进、前提依赖、场景适配或概念性支撑，优先下沉到 `reason`、frontmatter 或对象页正文，而不是新增 formal relation。
```

In `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`, replace the special checks with:

```md
- 如果 `uses_concept.md` 中出现“概念 → 论文支撑”关系，必须指出，并建议迁移到概念页证据区或 `supported_by.md`。
- 如果 `based_on.md` 中出现文献支撑关系而不是实际技术谱系，必须指出。
- 如果改进、前提依赖、场景适配或概念性支撑语义被单独升格为 formal relation，必须指出，并建议下沉到 `reason`、frontmatter 或对象页正文。
```

- [ ] **Step 4: Update eval fixtures so they stop expecting retired relations**

In `.claude/skills/paper-ingest/evals/regression-samples.json`:
- Remove `ontology/relations/improves_on.md` from `PathMind.must_create`
- Remove any expectation of retired relation ledgers from all samples
- Keep `relation_candidates` coverage to: `proposes`, `targets_task`, `evaluated_on`, `uses_concept`, `supported_by`, `cites`, `based_on`, `sourced_from`

In `.claude/skills/ontology-semantic-review/evals/evals.json`, rewrite any prompt that currently says:

```text
uses_concept / supports / depends_on / applies_to 与 based_on / improves_on 的关系边界
```

to instead say:

```text
uses_concept 与 based_on 的 formal relation 边界，以及改进、前提依赖、场景适配、概念性支撑语义是否被正确下沉到 reason / frontmatter / 正文。
```

- [ ] **Step 5: Run focused grep verification for pipeline contracts**

Run:

```bash
```

Expected:
- Remaining matches are either historical plan/spec documents outside the execution surface or benign English words unrelated to relation types
- No active skill, lint, or test contract still routes or expects the retired formal relations

---

### Task 5: Final verification and cleanup

**Files:**
- Modify: any file still failing the checks above
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full lint regression suite**

Run:

```bash
```

Expected:
- `OK`
- No test still expects the retired relation ledgers

- [ ] **Step 2: Run graph lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- `PASS` or repo-specific success output
- No complaints about missing `improves_on.md`, `depends_on.md`, `applies_to.md`, or `supports.md`

- [ ] **Step 3: Run one repository-wide grep to catch active-surface stragglers**

Run:

```bash
grep -R -nE "ontology/relations/(improves_on|depends_on|applies_to|supports)\.md|--(improves_on|depends_on|applies_to|supports)-->" \
  CLAUDE.md ontology scripts .claude/skills intermediate/papers
```

Expected:
- No matches in active runtime surfaces
- If there are matches, they should be genuine leftover migration bugs and must be fixed before claiming completion

- [ ] **Step 4: Do not create a git commit unless the user explicitly asks for one**

Use this rule for execution:

```text
Leave the working tree uncommitted unless the user explicitly requests a commit.
```

---

## Self-review checklist
- Spec coverage: This plan covers the remaining migration layers after the normative rewrite already completed in `CLAUDE.md` and `ontology/graph-standard.md`: live ledgers, serving pages, lint runtime, skills, evals, and verification.
- Placeholder scan: No `TODO` / `TBD` markers remain; each task names concrete files, exact snippets, and exact commands.
- Type consistency: The plan consistently treats the active formal relation set as `proposes`, `cites`, `based_on`, `uses_concept`, `targets_task`, `evaluated_on`, `supported_by`, and `sourced_from`.
