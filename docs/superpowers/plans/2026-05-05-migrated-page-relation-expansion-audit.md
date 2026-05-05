# Migrated Page Relation Expansion Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit all migrated markdown pages under `wiki/` (excluding `wiki/relations/`) and classify every human-friendly wikilink as `already-formalized`, `should-be-formalized`, or `context-only`, then summarize the results both page-by-page and by relation type.

**Architecture:** Treat this as an audit/reporting pass, not a content-editing pass. First enumerate all relevant `wiki/**/*.md` pages except `wiki/relations/`. Then, for each page, compare human-friendly relation blocks, the page’s `Formal relations` block if present, and the current formal ledgers. Classify links by the agreed rules and write one consolidated audit report that contains both per-page audit cards and a relation-type summary. No object pages or ledgers should be modified in this pass.

**Tech Stack:** Markdown pages in `wiki/`, formal relation ledgers in `wiki/relations/`, Python 3 lint script for structural sanity only, markdown audit report output under `docs/`.

---

## File map

### Audit inputs
- Read: every `wiki/**/*.md` file except `wiki/relations/*.md`
- Read: all `wiki/relations/*.md` files as the formal graph truth source
- Read: `wiki/ontology/graph-standard.md`

### Audit output
- Create: `docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`

---

### Task 1: Enumerate the audit scope and freeze the classification rules

**Files:**
- Modify: none
- Test: shell listing only

- [ ] **Step 1: List every markdown page under `wiki/` excluding `wiki/relations/`**

Run:

```bash
find "/Users/yyzz/Desktop/MyClaudeCode/ResearchKB/wiki" \
  -path "/Users/yyzz/Desktop/MyClaudeCode/ResearchKB/wiki/relations" -prune -o \
  -type f -name "*.md" -print | sort
```

Expected: a full ordered list of all audit target pages.

- [ ] **Step 2: Freeze the three classification rules in working notes before auditing**

Use exactly these rules for every `[[wikilink]]` found in human-friendly relation blocks:

```text
already-formalized:
- the page's Formal relations contains the matching one-hop neighbor
- the formal relation ledger contains the corresponding formal edge
- the relation type is clear

should-be-formalized:
- the human-friendly block expresses a relationship that the ontology can legally model
- current evidence is sufficient
- the edge is missing from Formal relations and/or the formal ledger

context-only:
- primarily background, comparison, route context, or further reading
- or no appropriate formal relation type exists
- or evidence is insufficient
- or it should not be treated as a one-hop formal neighbor
```

- [ ] **Step 3: Run a sanity lint before beginning the audit**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 2: Audit benchmark, concept, and method pages

**Files:**
- Create: `docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md`
- Test: no code execution beyond file write

- [ ] **Step 1: Create the audit report skeleton**

Create `docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md` starting with:

```markdown
# Migrated Page Relation Expansion Audit

Date: 2026-05-05

## Scope
All `wiki/**/*.md` pages excluding `wiki/relations/`.

## Classification rules
### already-formalized
- the page's `Formal relations` contains the matching one-hop neighbor
- the formal relation ledger contains the corresponding formal edge
- the relation type is clear

### should-be-formalized
- the human-friendly block expresses a relationship that the ontology can legally model
- current evidence is sufficient
- the edge is missing from `Formal relations` and/or the formal ledger

### context-only
- primarily background, comparison, route context, or further reading
- or no appropriate formal relation type exists
- or evidence is insufficient
- or it should not be treated as a one-hop formal neighbor

## Page-by-page audit cards
```

- [ ] **Step 2: Add audit cards for benchmark pages**

Add audit cards for:
- `wiki/benchmarks/WebQSP.md`
- `wiki/benchmarks/CWQ.md`

Each card must use this exact structure:

```markdown
### [page path]
**Human-friendly links examined**
- ...

**already-formalized**
- ...

**should-be-formalized**
- ...

**context-only**
- ...

**Conclusion**
- ...
```

For benchmark pages, specifically inspect links under:
- `## 相关任务`
- `## 被哪些方法 / 论文使用`
- `## 相关场景`

- [ ] **Step 3: Add audit cards for concept pages**

Add audit cards for:
- `wiki/concepts/路径优先化.md`
- `wiki/concepts/重要推理路径.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`

Specifically inspect links under:
- `## 与其他概念的关系`
- `## 相关方法` / `## 相关方法 / 路线`
- `## 相关论文`
- `## 相关任务 / 场景`
- `## 相关场景与任务`

- [ ] **Step 4: Add audit cards for method pages**

Add audit cards for:
- `wiki/methods/PathMind.md`
- `wiki/methods/RoG.md`
- `wiki/methods/GCR.md`
- `wiki/methods/EPERM.md`
- `wiki/methods/ToG.md`
- `wiki/methods/协同增强式知识图谱推理.md`
- `wiki/methods/检索增强式知识图谱推理.md`
- `wiki/methods/路径导向知识图谱推理.md`

Specifically inspect links under:
- `## 方法演化位置`
- `## 应用场景`
- `## 代表论文`
- `## 相关概念`
- `## 与其他方法的对比`

---

### Task 3: Audit paper, scenario, and task pages

**Files:**
- Modify: `docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md`
- Test: no code execution beyond file write

- [ ] **Step 1: Add audit cards for paper pages**

Add audit cards for:
- `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md`
- `wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md`
- `wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md`
- `wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`
- `wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`
- `wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md`

Specifically inspect links under:
- `## 核心方法` / `## 核心方法 / 框架`
- `## 相关任务`
- `## 应用场景`
- `## 相关基准`
- `## 与知识库其他内容的关联`
- `## 引用了哪些重要工作`

- [ ] **Step 2: Add audit cards for scenario pages**

Add audit cards for:
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/scenarios/复杂产品设计.md`

Specifically inspect links under:
- `## 使用的主要方法 / 概念`
- `## 使用的主要方法 / 框架 / 概念`
- `## 相关任务`
- `## 相关论文`
- `## 相关 benchmark`

- [ ] **Step 3: Add audit cards for task pages**

Add audit cards for:
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/tasks/engineering-design-knowledge-management.md`

Specifically inspect links under:
- `## 相关方法`
- `## 相关框架 / 概念`
- `## 相关概念`
- `## 相关场景`
- `## 相关 benchmark`
- `## 相关论文`

---

### Task 4: Add relation-type summary and recommendations

**Files:**
- Modify: `docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a `## Relation-type summary` section**

Append this section structure to the end of the audit report:

```markdown
## Relation-type summary

### already-formalized by relation type
- `proposes`:
- `targets_task`:
- `evaluated_on`:
- `uses_concept`:
- `applies_to`:
- `supports`:
- `cites`:
- `supported_by`:

### should-be-formalized by relation type
- `proposes`:
- `targets_task`:
- `evaluated_on`:
- `uses_concept`:
- `applies_to`:
- `supports`:
- `cites`:
- `supported_by`:

### context-only patterns
- ...
```

- [ ] **Step 2: Add a short decision section at the end**

Append:

```markdown
## Decision recommendations
- Which relation types appear too narrow in the current formal graph?
- Which recurring human-friendly links should be downgraded to plain-text context links?
- Which pages should be prioritized for a follow-up formal-relation expansion pass?
```

- [ ] **Step 3: Run lint after writing the audit report**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 5: Final verification

**Files:**
- Modify: none
- Test: `git diff`, `git status --short`

- [ ] **Step 1: Verify the audit did not modify any wiki content or relation ledger files**

Run:

```bash
git diff -- \
  docs/relation-expansion-audits/2026-05-05-migrated-page-relation-expansion-audit.md
```

Expected: only the new audit report shows as changed for this pass.

- [ ] **Step 2: Show the current working tree status**

Run:

```bash
git status --short
```

Expected: this audit contributes only the new report file; any other changes shown belong to previously in-progress work.

- [ ] **Step 3: Do not auto-commit unless separately requested**

Expected: leave the audit report available for user review.
