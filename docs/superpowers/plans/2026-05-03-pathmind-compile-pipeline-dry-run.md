# PathMind Compile Pipeline Dry-Run Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the new three-skill compile pipeline end-to-end on the existing PathMind paper/PDF slice and determine whether the full chain is operational in the real repository.

**Architecture:** Treat PathMind as an integration-test paper, not a greenfield ingest. First snapshot the current PathMind-related state and define the bounded write set. Then run `paper-ingest`, capture and inspect its structured outputs, run `relation-reconciliation` against those outputs and the current ledgers, run `page-projection-sync` on the affected pages, and finally pass the resulting state through lint, ontology-semantic-review, and serving-governance-review. The dry-run succeeds only if each stage emits outputs directly consumable by the next stage.

**Tech Stack:** Markdown skills under `.claude/skills/`, PathMind PDF in `raw/`, existing PathMind `wiki/` and `intermediate/papers/` assets, relation ledgers under `wiki/relations/`, Python 3 lint script, governance review skills.

---

## File map

### Input / baseline assets
- Read/compare: `raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`
- Read/compare: `intermediate/papers/PathMind.sections.md`
- Read/compare: `intermediate/papers/PathMind.refs.md`
- Read/compare: `intermediate/papers/PathMind.experiments.md`
- Read/compare: `intermediate/papers/PathMind.full.md`
- Read/compare: `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Read/compare: `wiki/methods/PathMind.md`
- Read/compare: `wiki/concepts/路径优先化.md`
- Read/compare: `wiki/concepts/重要推理路径.md`
- Read/compare: `wiki/tasks/knowledge-graph-reasoning.md`
- Read/compare: `wiki/tasks/kgqa.md`
- Read/compare: `wiki/tasks/multi-hop-qa.md`
- Read/compare: `wiki/scenarios/知识图谱推理问答.md`
- Read/compare: `wiki/benchmarks/WebQSP.md`
- Read/compare: `wiki/benchmarks/CWQ.md`
- Read/compare: `wiki/relations/citation_graph.md`
- Read/compare: `wiki/relations/method_evolution.md`
- Read/compare: `wiki/relations/concept_links.md`
- Read/compare: `wiki/relations/task_method_map.md`
- Read/compare: `wiki/relations/benchmark_links.md`
- Read/compare: `wiki/relations/evidence_index.md`
- Read/compare: `wiki/relations/paper_method_links.md`
- Read/compare: `wiki/relations/provenance_links.md`

### Skills under test
- Read/use: `.claude/skills/paper-ingest/SKILL.md`
- Read/use: `.claude/skills/relation-reconciliation/SKILL.md`
- Read/use: `.claude/skills/page-projection-sync/SKILL.md`
- Read/use: `.claude/skills/ontology-semantic-review/SKILL.md`
- Read/use: `.claude/skills/serving-governance-review/SKILL.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: governance review outputs from `ontology-semantic-review`
- Test: governance review outputs from `serving-governance-review`

---

### Task 1: Snapshot the current PathMind slice and bounded write scope

**Files:**
- Modify: none
- Test: `git diff -- <pathmind-scope>`

- [ ] **Step 1: Capture the current PathMind-related file set for comparison**

Run:

```bash
git diff -- \
  "intermediate/papers/PathMind.sections.md" \
  "intermediate/papers/PathMind.refs.md" \
  "intermediate/papers/PathMind.experiments.md" \
  "intermediate/papers/PathMind.full.md" \
  "wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" \
  "wiki/methods/PathMind.md" \
  "wiki/concepts/路径优先化.md" \
  "wiki/concepts/重要推理路径.md" \
  "wiki/tasks/knowledge-graph-reasoning.md" \
  "wiki/tasks/kgqa.md" \
  "wiki/tasks/multi-hop-qa.md" \
  "wiki/scenarios/知识图谱推理问答.md" \
  "wiki/benchmarks/WebQSP.md" \
  "wiki/benchmarks/CWQ.md" \
  "wiki/relations/citation_graph.md" \
  "wiki/relations/method_evolution.md" \
  "wiki/relations/concept_links.md" \
  "wiki/relations/task_method_map.md" \
  "wiki/relations/benchmark_links.md" \
  "wiki/relations/evidence_index.md" \
  "wiki/relations/paper_method_links.md" \
  "wiki/relations/provenance_links.md"
```

Expected: a readable baseline of any already-pending changes in the PathMind slice.

- [ ] **Step 2: Verify the dry-run is constrained to the PathMind slice**

Run:

```bash
git status --short | rg "PathMind|路径优先化|重要推理路径|knowledge-graph-reasoning|kgqa|multi-hop-qa|知识图谱推理问答|WebQSP|CWQ|citation_graph|method_evolution|concept_links|task_method_map|benchmark_links|evidence_index|paper_method_links|provenance_links"
```

Expected: only PathMind-adjacent files appear in the dry-run scope.

- [ ] **Step 3: Record the bounded write contract before running skills**

Write this note into your working notes for the run (do not create a file; keep it in session context):

```text
Allowed writes: PathMind-adjacent relation ledgers, PathMind object-page Formal relations, strong-consistency frontmatter, and templated relation blocks only. No unrelated topic-line updates.
```

---

### Task 2: Execute `paper-ingest` and inspect its structured outputs

**Files:**
- Modify: PathMind-adjacent files only, if the skill writes them
- Test: inspect final structured summary and changed file set

- [ ] **Step 1: Run `paper-ingest` on the PathMind PDF**

Invoke `paper-ingest` with the exact input:

```text
处理论文：/Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf，重点看方法演化、formal relations 候选与 serving-ready 邻接
```

Expected: the skill runs against the existing PathMind assets instead of treating the paper as a blank ingest.

- [ ] **Step 2: Verify the final `paper-ingest` output includes the new contract fields**

Inspect the final structured summary and confirm it explicitly contains:

```text
relation_candidates
relation_exemptions
updated_pages
warnings
```

Expected: all four appear in the final structured output.

- [ ] **Step 3: Confirm that `relation_candidates` is meaningfully populated**

Check that the output contains non-empty or intentionally empty arrays for at least:

```text
proposes
targets_task
evaluated_on
uses_concept
supported_by
cites
sourced_from
```

Expected: the run does not silently omit the relation-candidate contract.

- [ ] **Step 4: If `paper-ingest` mutates files, run lint immediately**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 3: Execute `relation-reconciliation` on the real PathMind run outputs

**Files:**
- Modify: PathMind-adjacent `wiki/relations/*.md` files if reconciliation decides edges are missing
- Test: inspect reconciliation output; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run `relation-reconciliation` using the `paper-ingest` outputs from Task 2**

Invoke `relation-reconciliation` with instructions equivalent to:

```text
Use the current PathMind ingest run outputs as input. Reconcile relation_candidates, PathMind object pages, PathMind evidence caches, and the current PathMind-adjacent relation ledgers. Only update PathMind-adjacent formal ledgers. Produce structured output with already_present, added_relations, exemptions, needs_human_review, and affected_pages.
```

Expected: the skill produces a structured reconciliation summary, not just prose.

- [ ] **Step 2: Verify the reconciliation output contains all contract sections**

Confirm the output explicitly includes:

```text
already_present
added_relations
exemptions
needs_human_review
affected_pages
```

Expected: all sections are present, even if some are empty.

- [ ] **Step 3: Re-run lint after reconciliation writes formal ledgers**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 4: Execute `page-projection-sync` on the affected PathMind pages

**Files:**
- Modify: PathMind-adjacent object pages only
- Test: inspect sync output; `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run `page-projection-sync` using the reconciliation output**

Invoke `page-projection-sync` with instructions equivalent to:

```text
Use the updated PathMind-adjacent formal ledgers and the current relation-reconciliation output. Sync only the affected PathMind pages. Update Formal relations, strong-consistency frontmatter if needed, and templated human-readable relation blocks. Do not rewrite interpretive prose.
```

Expected: the skill updates only the declared sync surfaces.

- [ ] **Step 2: Verify the sync output contains the expected contract sections**

Confirm the output explicitly includes:

```text
synced_pages
updated_sections
manual_followups
```

Expected: the stage reports what it touched rather than silently editing pages.

- [ ] **Step 3: Re-run lint after projection sync**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 5: Run ontology-semantic-review on the resulting PathMind state

**Files:**
- Modify: none unless review reveals necessary fixes
- Test: review output + `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run `ontology-semantic-review` on the post-sync PathMind slice**

Review this exact set:
- `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- `wiki/methods/PathMind.md`
- `wiki/concepts/路径优先化.md`
- `wiki/concepts/重要推理路径.md`
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/benchmarks/WebQSP.md`
- `wiki/benchmarks/CWQ.md`
- PathMind-adjacent relation ledgers that changed in Tasks 2–4

Expected: a structured semantic review report that can assess the compile chain results without reinterpreting the whole pipeline by hand.

- [ ] **Step 2: Apply only minimal fixes if the review reports concrete ontology-semantic issues**

If the review returns `revise-then-accept` or similar, fix only the smallest PathMind-adjacent semantic issue it identifies.

Expected: no unrelated refactoring.

- [ ] **Step 3: Re-run lint after any ontology-semantic fix**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 6: Run serving-governance-review on the resulting PathMind state

**Files:**
- Modify: none unless review reveals necessary fixes
- Test: review output + `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run `serving-governance-review` on the same PathMind slice**

Expected review focus:
- serving completeness
- readability alignment
- QA traversability
- release readiness

Expected: a page-by-page verdict plus overall batch verdict.

- [ ] **Step 2: Apply only minimal serving fixes if the review reports concrete serving gaps**

If the review returns `needs_fixes`, patch only the smallest missing formal or templated-projection issues within the PathMind slice.

Expected: no broad content expansion.

- [ ] **Step 3: Re-run lint after any serving fix**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 7: Decide whether the dry-run truly “ran end-to-end”

**Files:**
- Modify: none
- Test: reasoning against captured outputs

- [ ] **Step 1: Check the minimum success criteria**

Confirm all are true:

```text
- paper-ingest executed
- relation-reconciliation executed
- page-projection-sync executed
- each stage emitted explicit output
- lint passed after the chain
```

- [ ] **Step 2: Check the real success criteria**

Confirm all are true:

```text
- each stage’s output was directly usable by the next stage
- governance layers could evaluate the result without ad hoc reinterpretation
- only bounded PathMind-adjacent files were touched
- no large manual patching was required between stages
```

If any of these fail, record exactly which stage contract broke.

- [ ] **Step 3: Produce an explicit verdict for the dry-run**

Use one of:
- `pipeline-ran-end-to-end`
- `pipeline-ran-with-manual-bridges`
- `pipeline-did-not-run-cleanly`

Expected: one explicit verdict, not a vague summary.

---

### Task 8: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the final full lint check**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Show the final PathMind-scope diff**

Run:

```bash
git diff -- \
  "intermediate/papers/PathMind.sections.md" \
  "intermediate/papers/PathMind.refs.md" \
  "intermediate/papers/PathMind.experiments.md" \
  "intermediate/papers/PathMind.full.md" \
  "wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" \
  "wiki/methods/PathMind.md" \
  "wiki/concepts/路径优先化.md" \
  "wiki/concepts/重要推理路径.md" \
  "wiki/tasks/knowledge-graph-reasoning.md" \
  "wiki/tasks/kgqa.md" \
  "wiki/tasks/multi-hop-qa.md" \
  "wiki/scenarios/知识图谱推理问答.md" \
  "wiki/benchmarks/WebQSP.md" \
  "wiki/benchmarks/CWQ.md" \
  "wiki/relations/citation_graph.md" \
  "wiki/relations/method_evolution.md" \
  "wiki/relations/concept_links.md" \
  "wiki/relations/task_method_map.md" \
  "wiki/relations/benchmark_links.md" \
  "wiki/relations/evidence_index.md" \
  "wiki/relations/paper_method_links.md" \
  "wiki/relations/provenance_links.md"
```

Expected: all touched files remain within the declared PathMind-adjacent scope.

- [ ] **Step 3: Do not create a commit automatically**

Run:

```bash
git status --short
```

Expected: working tree remains available for user review, because this dry-run is for architecture validation rather than automatic integration.
