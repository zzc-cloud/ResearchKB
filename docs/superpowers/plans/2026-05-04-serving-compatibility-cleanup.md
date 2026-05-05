# Serving Compatibility Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove compatibility-only duplicate sections from serving-migrated pages by updating lint expectations to the new canonical serving headings and then cleaning the affected pages.

**Architecture:** First update `scripts/lint_graph.py` so it validates the new canonical serving headings instead of legacy transitional headings. Then remove only the duplicate compatibility residue from the affected PathMind/high-frequency and survey-mainline pages, preserving formal relations and substantive content. Finally, rerun lint plus governance checks to confirm cleanup did not regress serving behavior.

**Tech Stack:** Markdown page templates in `wiki/`, Python 3 lint script (`scripts/lint_graph.py`), existing ontology-semantic-review and serving-governance-review gates.

---

## File map

### Lint contract
- Modify: `scripts/lint_graph.py`
  - Replace legacy section expectations with canonical serving headings.

### PathMind / high-frequency cleanup pages
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Modify: `wiki/benchmarks/WebQSP.md`
- Modify: `wiki/benchmarks/CWQ.md`

### Survey mainline cleanup pages
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `ontology-semantic-review`
- Test: `serving-governance-review`

---

### Task 1: Update lint expectations to canonical serving headings

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] Replace the legacy transitional `sections` expectations in `PHASE_ONE_CORE_PAGES` with canonical headings:
  - `wiki/concepts/路径优先化.md`: `['## 与其他概念的关系', '## 证据来源']`
  - `wiki/concepts/重要推理路径.md`: `['## 与其他概念的关系', '## 证据来源']`
  - `wiki/scenarios/知识图谱推理问答.md`: `['## 相关任务', '## 证据来源']`
  - `wiki/tasks/knowledge-graph-reasoning.md`: `['## 相关方法', '## 证据来源 / 关系索引']`
  - `wiki/tasks/kgqa.md`: `['## 相关方法', '## 证据来源 / 关系索引']`
  - `wiki/tasks/multi-hop-qa.md`: `['## 相关方法', '## 证据来源 / 关系索引']`
  - `wiki/benchmarks/WebQSP.md`: `['## 相关任务', '## 证据来源']`
  - `wiki/benchmarks/CWQ.md`: `['## 相关任务', '## 证据来源']`
  - `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`: `['## 核心方法 / 框架', '## 证据来源']`
  - `wiki/scenarios/复杂产品设计.md`: `['## 使用的主要方法 / 框架 / 概念', '## 证据来源']`
  - `wiki/concepts/LLM增强知识图谱.md`: `['## 与其他概念的关系', '## 证据来源']`
  - `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`: `['## 与其他概念的关系', '## 证据来源']`
  - `wiki/tasks/engineering-design-knowledge-management.md`: `['## 相关框架 / 概念', '## 证据来源 / 关系索引']`

- [ ] Run: `python3 scripts/lint_graph.py`
Expected: it may fail initially on pages that still contain only compatibility shapes.

### Task 2: Remove duplicate compatibility sections from PathMind/high-frequency pages

**Files:**
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Modify: `wiki/benchmarks/WebQSP.md`
- Modify: `wiki/benchmarks/CWQ.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] Remove compatibility-only duplicate blocks:
  - delete `## 关系索引与证据` from the two concept pages, keep `## 证据来源`
  - delete `## 关系索引` from the three task pages, keep `## 证据来源 / 关系索引`
  - delete `## 关联任务` from `wiki/scenarios/知识图谱推理问答.md`, keep `## 相关任务`
  - delete `## 证据索引` from both benchmark pages, keep `## 证据来源`

- [ ] Run: `python3 scripts/lint_graph.py`
Expected: PASS or only survey-mainline failures remain.

### Task 3: Remove duplicate compatibility sections from survey mainline pages

**Files:**
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] Remove compatibility-only duplicate blocks:
  - delete `## 实验证据 / 综述证据` from the survey paper, keep `## 综述证据来源` + `## 证据来源` only if still needed by canonical lint
  - delete `## 关系索引与证据` from `LLM增强知识图谱.md`, keep `## 证据来源`
  - delete one of the duplicated task/scenario mixed blocks in `复杂产品设计中的LLM-KG协同框架.md`, keep canonical `## 相关任务 / 场景`
  - delete the second `## 证据来源` from `复杂产品设计.md`, keep one canonical block
  - delete `## 相关方法 / 框架` and `## 关系索引` from `engineering-design-knowledge-management.md`, keep `## 相关框架 / 概念` and `## 证据来源 / 关系索引`

- [ ] Run: `python3 scripts/lint_graph.py`
Expected: PASS

### Task 4: Re-run governance checks after cleanup

**Files:**
- Modify: none unless a minimal fix is required
- Test: `python3 scripts/lint_graph.py`, `ontology-semantic-review`, `serving-governance-review`

- [ ] Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] Run `ontology-semantic-review` on the survey mainline representative pages plus related ledgers.
Expected: semantics remain unchanged and valid.

- [ ] Run `serving-governance-review` on the survey mainline representative pages.
Expected: pages remain serving-ready after compatibility cleanup.

### Task 5: Final verification

**Files:**
- Modify: none
- Test: `git diff -- <cleanup-scope>` and `git status --short`

- [ ] Verify diff scope is limited to `scripts/lint_graph.py` and the cleanup pages.
- [ ] Verify no formal relation content was removed accidentally.
- [ ] Keep the working tree available for review; do not auto-commit unless separately requested.
