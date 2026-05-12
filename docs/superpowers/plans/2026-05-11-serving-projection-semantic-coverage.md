# Serving Projection Semantic Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade ResearchKB’s serving contract so object-page `Formal relations` carry all serving-necessary relation attributes and human-readable page sections provide summary coverage that is not weaker than those formal projections.

**Architecture:** Treat [ontology/graph-standard.md](ontology/graph-standard.md) as the schema truth for serving contracts, then update [page-projection-sync/SKILL.md](.claude/skills/page-projection-sync/SKILL.md) and its checklists to implement that truth. Finally, lock the contract with focused regressions that verify both relation-specific projection fields like `target_paper` and stronger Method/Paper summary coverage expectations.

**Tech Stack:** Obsidian Markdown, Python `unittest`, existing ResearchKB skill contracts, serving checklists, and page-projection templates

---

## File map and responsibilities

### Schema truth
- Modify: `ontology/graph-standard.md`
  - Defines the normative object-page serving contract, including `Formal relations` coverage and human-readable summary coverage requirements.

### Projection implementation contract
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Describes what formal truth the projection stage consumes and what must appear in object-page projections and summary sections.
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
  - Checklist for serving-complete projection behavior.
- Modify if needed: `.claude/skills/page-projection-sync/evals/regression-samples.json`
  - Regression fixture wording if current samples hardcode weaker assumptions.
- Modify if needed: `.claude/skills/serving-governance-review/SKILL.md`
  - Only if its contract text explicitly contradicts the new summary-coverage standard.

### Page-template examples and serving exemplars
- Modify: `ontology/entities/methods/PathMind.md`
  - First concrete Method-page exemplar for `target_paper` projection and stronger summary coverage.
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
  - First concrete Paper-page exemplar for stronger `cites` summary coverage.

### Regression coverage
- Modify: `scripts/test_method_relation_pipeline.py`
  - Verifies projection contract, checklist language, and exemplar page behavior.

### References
- Spec: `docs/superpowers/specs/2026-05-11-serving-projection-semantic-coverage-design.md`
- Plan: `docs/superpowers/plans/2026-05-11-serving-projection-semantic-coverage.md`

## Implementation order

1. Tighten schema truth in `ontology/graph-standard.md`.
2. Update `page-projection-sync` skill contract and checklist language to match the schema truth.
3. Update PathMind Method/Paper pages as the first concrete serving exemplars.
4. Add failing regression assertions for the new projection and summary-coverage requirements.
5. Make the minimal remaining content/contract fixes until tests pass.
6. Run targeted regression and graph lint.

This order keeps the normative contract ahead of the implementation examples and keeps the examples ahead of test lock-in.

## Key validation points

- `Formal relations` on object pages must cover all **serving-necessary attributes**, not only `edge_semantics` and `evidence`.
- `references_method` projections must expose `target_paper` as an object-page-friendly projection of ledger `target_paper_path`.
- `source_paper_path` remains ledger truth and is **not** required to surface as a separate object-page field.
- Human-readable Method/Paper sections must provide thematic summary coverage of the formal relations and may not collapse away key distinctions.
- Summary coverage means “readable and not weaker than formal projection,” **not** instance-by-instance duplication.

## Task 1: Update the normative serving contract

**Files:**
- Modify: `ontology/graph-standard.md`
- Reference: `docs/superpowers/specs/2026-05-11-serving-projection-semantic-coverage-design.md`

- [ ] **Step 1: Write the failing test for the new serving contract language**

Add a new regression in `scripts/test_method_relation_pipeline.py` that expects `graph-standard.md` to contain these phrases:

```python
self.assertIn('serving-necessary attributes', graph_standard)
self.assertIn('target_paper_path → `target_paper`', graph_standard)
self.assertIn('正文必须对 `Formal relations` 做主题化摘要覆盖', graph_standard)
```

Pick exact assertions that match the final wording you intend to add.

- [ ] **Step 2: Run the targeted test to verify it fails**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_formal_projection_coverage_contract_is_documented -v
```

Expected: FAIL because the current graph standard still describes weaker projection behavior.

- [ ] **Step 3: Update `ontology/graph-standard.md` with the new contract**

In the sections around object-page projection and `Formal relations`, add explicit normative text that:

```md
- 对象页 `Formal relations` 必须覆盖 formal relation instance 的全部 serving-necessary attributes。
- relation-specific 必要属性允许以对象页友好别名投影，而不是原样 child-field 名称。
- 例如：`references_method` ledger 的 `target_paper_path` 在对象页投影为 `target_paper`。
- 正文模板化关系区块必须对 `Formal relations` 做主题化摘要覆盖，且语义不弱于 formal projection。
```

Keep the wording clear that the ledger remains the most complete truth source.

- [ ] **Step 4: Re-run the targeted test to verify it passes**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_formal_projection_coverage_contract_is_documented -v
```

Expected: PASS for the graph-standard assertions.

- [ ] **Step 5: Commit the schema-truth update**

```bash
git add ontology/graph-standard.md scripts/test_method_relation_pipeline.py
git commit -m "docs: define serving projection semantic coverage"
```

## Task 2: Update page-projection-sync’s contract and checklist

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/evals/quality-checklist.md`
- Modify if needed: `.claude/skills/page-projection-sync/evals/regression-samples.json`

- [ ] **Step 1: Write the failing test for skill-contract coverage**

Extend `test_projection_and_index_contracts_cover_dual_method_sections_and_partial_navigation` or add a new focused test that expects:

```python
self.assertIn('serving-necessary attributes', projection)
self.assertIn('`target_paper_path` 必须投影为对象页友好 `target_paper`', projection)
self.assertIn('正文模板区块未覆盖其主题语义，应输出 `manual_followups`', projection)
self.assertIn('摘要覆盖', projection_checklist)
```

Use exact strings you intend to add.

- [ ] **Step 2: Run the targeted test to verify it fails**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_projection_and_index_contracts_cover_dual_method_sections_and_partial_navigation -v
```

Expected: FAIL because the current skill still describes minimal formal truth projection.

- [ ] **Step 3: Update `page-projection-sync/SKILL.md` input and projection contract**

Revise the skill so it no longer says it only consumes:

```md
source、target、relation、edge_semantics、evidence truth
```

Replace it with wording like:

```md
它消费 canonical relation ledger record 中的 serving-necessary attributes，并把这些 formal relation truth 投影回对象页。
```

Also update the projection examples to show relation-specific projection fields, including:

```md
- `references_method`：...
  - edge_semantics: ...
  - target_paper: ...
  - evidence: ...
```

- [ ] **Step 4: Update the human-readable summary-sync contract**

Add explicit rules that:

```md
- 模板化人类区块必须对 `Formal relations` 做主题化摘要覆盖。
- 若 formal relation 已投影但正文未覆盖其主语义面，应输出 `manual_followups`。
- Method 页的 `## 方法演化与参照关系` 与 Paper 页的 `## 引用了哪些重要工作` 不得只剩对象列表。
```

- [ ] **Step 5: Update the checklist language**

In `.claude/skills/page-projection-sync/evals/quality-checklist.md`, add checklist items such as:

```md
- [ ] `Formal relations` 覆盖 relation-specific serving-necessary attributes。
- [ ] `references_method` 若存在 `target_paper_path`，对象页投影必须提供 `target_paper`。
- [ ] 正文模板区块必须对 formal projection 做摘要覆盖，而不是只给对象列表。
```

- [ ] **Step 6: Update regression samples only if they currently encode weaker assumptions**

If `.claude/skills/page-projection-sync/evals/regression-samples.json` contains wording that conflicts with the new contract, update those strings so they describe the stronger projection behavior without adding unrelated scenarios.

- [ ] **Step 7: Re-run the targeted skill-contract test to verify it passes**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_projection_and_index_contracts_cover_dual_method_sections_and_partial_navigation -v
```

Expected: PASS.

- [ ] **Step 8: Commit the skill-contract sync**

```bash
git add .claude/skills/page-projection-sync/SKILL.md .claude/skills/page-projection-sync/evals/quality-checklist.md .claude/skills/page-projection-sync/evals/regression-samples.json scripts/test_method_relation_pipeline.py
git commit -m "docs: strengthen serving projection sync contract"
```

If `regression-samples.json` is unchanged, omit it from `git add`.

## Task 3: Upgrade the PathMind Method page exemplar

**Files:**
- Modify: `ontology/entities/methods/PathMind.md`
- Test: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Write the failing test for Method-page `target_paper` projection**

Add a regression that expects the PathMind Method page to include a `target_paper` line under at least one `references_method` projection, for example:

```python
self.assertIn('  - target_paper: Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs', pathmind_method)
```

Also assert that the human-readable `## 方法演化与参照关系` section mentions the representative-paper angle, for example by checking for a phrase such as:

```python
self.assertIn('对应代表论文', pathmind_method)
```

Choose the exact phrase you will actually add.

- [ ] **Step 2: Run the targeted test to verify it fails**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods -v
```

Expected: FAIL because the current Method page has no `target_paper` projection and the summary section is too thin.

- [ ] **Step 3: Update `PathMind.md` formal projections**

For each outgoing `references_method` item, add a `target_paper` sub-line after `edge_semantics`, for example:

```md
- `references_method`：GNN-RAG（文档：`ontology/entities/methods/GNN-RAG.md`）：[[../methods/GNN-RAG]]
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - target_paper: Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs（文档：`ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`）：[[../papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
  - evidence: [[../evidence/PathMind.refs]]
```

Repeat for `RoG`, `GCR`, `EPERM`, and `ToG`.

- [ ] **Step 4: Strengthen the human-readable summary section**

Revise `## 方法演化与参照关系` so it no longer reads as a bare object list. Make it summarize why each referenced method matters and, where relevant, which representative paper anchors that route. For example:

```md
### 关键参照方法
- [[../methods/GNN-RAG]]：retrieval-augmented 图检索代表方法，对应代表论文为 [[../papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]；PathMind 以其作为图检索增强路线的核心比较对象。
```

Do the same style upgrade for the other referenced methods.

- [ ] **Step 5: Re-run the targeted Method-page regression**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods -v
```

Expected: PASS.

- [ ] **Step 6: Commit the Method-page exemplar update**

```bash
git add ontology/entities/methods/PathMind.md scripts/test_method_relation_pipeline.py
git commit -m "feat: enrich method serving projections for references_method"
```

## Task 4: Upgrade the PathMind Paper page summary coverage

**Files:**
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Test: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Write the failing test for Paper-page summary coverage**

Add a regression that expects the `## 引用了哪些重要工作` section to include route-level summaries, not just titles. For example:

```python
self.assertIn('显式 relational path reasoning 代表工作', pathmind_paper)
self.assertIn('retrieval-augmented 图检索代表方法', pathmind_paper)
self.assertIn('evidence-path enhanced 代表工作', pathmind_paper)
```

These should match exact phrases you plan to write.

- [ ] **Step 2: Run the targeted test to verify it fails**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods -v
```

Expected: FAIL because the current Paper-page section is still a title-only list.

- [ ] **Step 3: Update the `## 引用了哪些重要工作` section**

Convert the current title-only list into semantic summary bullets such as:

```md
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]：显式 relational path reasoning 的代表工作。
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]：retrieval-augmented 图检索代表方法。
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]：evidence-path enhanced 路线代表工作。
```

Keep the links, but add route/role semantics so the section actually summarizes the formal `cites` projection.

- [ ] **Step 4: Strengthen `## 与知识库其他内容的关联` if needed**

If this section still reads too vaguely after Step 3, expand it minimally so it mentions the key outgoing `proposes` relation and the major task/benchmark/evidence anchors in a way a reader can understand without returning to `Formal relations`.

- [ ] **Step 5: Re-run the targeted Paper-page regression**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline.MethodRelationPipelineTests.test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods -v
```

Expected: PASS.

- [ ] **Step 6: Commit the Paper-page exemplar update**

```bash
git add "ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" scripts/test_method_relation_pipeline.py
git commit -m "docs: strengthen paper serving summary coverage"
```

## Task 5: Finalize regression coverage

**Files:**
- Modify: `scripts/test_method_relation_pipeline.py`
- Test: `scripts/test_method_relation_pipeline.py`

- [ ] **Step 1: Consolidate the new assertions into stable regression tests**

Make sure the regression suite now explicitly covers:

```python
# graph standard
self.assertIn('serving-necessary attributes', graph_standard)

# page-projection-sync contract
self.assertIn('target_paper', projection)
self.assertIn('摘要覆盖', projection)

# Method page exemplar
self.assertIn('  - target_paper: Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs', pathmind_method)
self.assertIn('对应代表论文', pathmind_method)

# Paper page exemplar
self.assertIn('显式 relational path reasoning 的代表工作', pathmind_paper)
self.assertIn('retrieval-augmented 图检索代表方法', pathmind_paper)
```

Adjust exact strings to match the final content, but keep them specific enough to catch regressions.

- [ ] **Step 2: Run the full targeted regression suite**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline -v
```

Expected: all tests in `MethodRelationPipelineTests` pass.

- [ ] **Step 3: Commit the finalized test coverage**

```bash
git add scripts/test_method_relation_pipeline.py
git commit -m "test: cover serving projection semantic coverage"
```

## Task 6: Run final validation

**Files:**
- Validate all modified files in this change set

- [ ] **Step 1: Run graph lint**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Re-run the full targeted regression suite**

Run:

```bash
python3 -m unittest scripts.test_method_relation_pipeline -v
```

Expected: full PASS.

- [ ] **Step 3: Inspect the diff for scope control**

Run:

```bash
git diff -- ontology/graph-standard.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/page-projection-sync/evals/quality-checklist.md .claude/skills/page-projection-sync/evals/regression-samples.json "ontology/entities/methods/PathMind.md" "ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" scripts/test_method_relation_pipeline.py
```

Expected: only schema-truth, projection-contract, exemplar-page, and regression-test changes appear.

- [ ] **Step 4: Commit any final fixups if validation requires them**

If you had to make final cleanup edits after validation, commit them with:

```bash
git add ontology/graph-standard.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/page-projection-sync/evals/quality-checklist.md .claude/skills/page-projection-sync/evals/regression-samples.json "ontology/entities/methods/PathMind.md" "ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" scripts/test_method_relation_pipeline.py
git commit -m "chore: finalize serving projection semantic coverage"
```

If validation passes cleanly with the earlier commits, skip this extra commit.

## Spec coverage check

- Graph-standard serving contract update: covered by Task 1.
- `page-projection-sync` contract for serving-necessary attributes and summary coverage: covered by Task 2.
- Checklist / eval contract sync: covered by Task 2.
- Method-page `references_method -> target_paper` projection exemplar: covered by Task 3.
- Paper-page summary coverage stronger than title-only lists: covered by Task 4.
- Regression coverage for both projection and summary contracts: covered by Task 5.
- Lint and targeted verification: covered by Task 6.

## Notes for the implementer

- Treat `ontology/graph-standard.md` as the schema truth. The skill contract and page exemplars must conform to it.
- Preserve the distinction between ledger truth and object-page serving truth. Do not turn object pages into raw path-field dumps.
- Keep summary coverage thematic and human-readable. The point is “not weaker than formal projection,” not “duplicate every instance.”
- Start with PathMind as the first exemplar. Do not broaden to unrelated pages in this change.