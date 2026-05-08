# Entity Domain Index Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign `ontology/entities/*/index.md` so each index only serves object-domain navigation, separates serving-ready entries from non-serving placeholders, and stays correct through the automated ingest → reconciliation → projection → index-sync → governance pipeline.

**Architecture:** Replace the old `core-entry` / `grouped-navigation` / `canonical-list` model with two object-navigation managed blocks: `navigation-entries` and `non-serving-placeholders`. Teach index generation and linting to derive domain-specific semantic descriptions from object pages and to enforce that placeholder pages never appear in default navigation entries.

**Tech Stack:** Python (`scripts/lint_graph.py`, `scripts/test_lint_graph.py`), Obsidian Markdown knowledge pages, ResearchKB skill contracts in `.claude/skills/index-sync/SKILL.md` and `.claude/skills/paper-ingest/SKILL.md`

---

## File structure

- Modify: `ontology/entities/papers/index.md`
  - Establish the new target structure for paper-domain navigation.
- Modify: `ontology/entities/methods/index.md`
- Modify: `ontology/entities/concepts/index.md`
- Modify: `ontology/entities/tasks/index.md`
- Modify: `ontology/entities/scenarios/index.md`
- Modify: `ontology/entities/benchmarks/index.md`
- Modify: `ontology/entities/evidence/index.md`
- Modify: `ontology/entities/raw-sources/index.md`
  - Convert each index to object-domain-only navigation.
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Update the managed-block contract and generation responsibilities.
- Modify: `scripts/lint_graph.py`
  - Enforce the new index structure and semantic-entry rules.
- Modify: `scripts/test_lint_graph.py`
  - Add regression tests for new managed blocks, semantic descriptions, and placeholder placement.

---

### Task 1: Lock the new index contract in tests and the index-sync skill

**Files:**
- Modify: `scripts/test_lint_graph.py`
- Modify: `.claude/skills/index-sync/SKILL.md`

- [ ] **Step 1: Write the failing test for new index block names**

Add this test method to `scripts/test_lint_graph.py`:

```python
    def test_lint_graph_uses_new_index_managed_block_names(self):
        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        self.assertIn('navigation-entries', text)
        self.assertIn('non-serving-placeholders', text)
        self.assertNotIn("'core-entry'", text)
        self.assertNotIn("'grouped-navigation'", text)
        self.assertNotIn("'canonical-list'", text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_uses_new_index_managed_block_names -v`
Expected: FAIL because `scripts/lint_graph.py` still references the old block names.

- [ ] **Step 3: Update the index-sync skill contract**

In `.claude/skills/index-sync/SKILL.md`, replace the old managed-block wording with the new contract:

```md
1. `ontology/entities/*/index.md` 中的 `navigation-entries` 与 `non-serving-placeholders` 受管区块
2. 只做对象域导航，不负责 relation 层入口投影
3. 默认 serving-ready 页面进入 `navigation-entries`
4. `status: placeholder` 或其他不可默认 serving 的实例进入 `non-serving-placeholders`
5. 每条实例必须带对象域定制语义说明，而不是裸 `[[wikilink]]`
```

- [ ] **Step 4: Run the targeted test again**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_uses_new_index_managed_block_names -v`
Expected: Still FAIL, because lint has not been updated yet.

- [ ] **Step 5: Commit**

```bash
git add scripts/test_lint_graph.py .claude/skills/index-sync/SKILL.md
git commit -m "docs: define object-domain index block contract"
```

### Task 2: Convert `papers/index.md` into the new object-domain-only structure

**Files:**
- Modify: `ontology/entities/papers/index.md`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Write the failing structure test**

Add this test method:

```python
    def test_papers_index_uses_object_navigation_only_structure(self):
        text = (ROOT / 'ontology' / 'entities' / 'papers' / 'index.md').read_text(encoding='utf-8')
        self.assertIn('<!-- BEGIN MANAGED BLOCK:navigation-entries -->', text)
        self.assertIn('<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->', text)
        self.assertNotIn('## 5. 相关关系账本', text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_papers_index_uses_object_navigation_only_structure -v`
Expected: FAIL because `papers/index.md` still uses the old sections and contains relation-entry content.

- [ ] **Step 3: Rewrite `ontology/entities/papers/index.md` minimally**

Replace the current body with this structure:

```md
# Papers Index

> 本页负责 Paper 对象域导航：先定位正式论文实例，再进入具体论文页；placeholder 论文仅用于引用解析与图谱连通，不作为默认入口。

## 1. 对象域说明
- 本域收录正式 Paper 节点。
- 默认 serving-ready 的正式论文进入“导航入口”。
- `status: placeholder` 的占位论文进入“其他实例（不可导航）”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]：提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]：PathMind 引用的 retrieval-augmented 上游论文，占位节点，状态=placeholder
- [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]：PathMind 引用的 grounded reasoning 上游论文，占位节点，状态=placeholder
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]：PathMind 引用的 evidence-path 上游论文，占位节点，状态=placeholder
- [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]：PathMind 引用的图检索增强上游论文，占位节点，状态=placeholder
- [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]：PathMind 引用的 synergy-augmented 上游论文，占位节点，状态=placeholder
- [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]：PathMind 引用的生成推理路径上游论文，占位节点，状态=placeholder
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_papers_index_uses_object_navigation_only_structure -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ontology/entities/papers/index.md scripts/test_lint_graph.py
git commit -m "refactor: redesign papers index as object navigation"
```

### Task 3: Convert the remaining entity indexes to the new block structure

**Files:**
- Modify: `ontology/entities/methods/index.md`
- Modify: `ontology/entities/concepts/index.md`
- Modify: `ontology/entities/tasks/index.md`
- Modify: `ontology/entities/scenarios/index.md`
- Modify: `ontology/entities/benchmarks/index.md`
- Modify: `ontology/entities/evidence/index.md`
- Modify: `ontology/entities/raw-sources/index.md`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Write the failing lint-structure test**

Add this test:

```python
    def test_all_entity_indexes_use_navigation_and_placeholder_blocks(self):
        expected = {
            'ontology/entities/papers/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/methods/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/concepts/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/tasks/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/scenarios/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/benchmarks/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/evidence/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/raw-sources/index.md': ['navigation-entries'],
        }
        for rel, blocks in expected.items():
            text = (ROOT / rel).read_text(encoding='utf-8')
            for block in blocks:
                self.assertIn(f'<!-- BEGIN MANAGED BLOCK:{block} -->', text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_all_entity_indexes_use_navigation_and_placeholder_blocks -v`
Expected: FAIL because the remaining indexes still use the old structure.

- [ ] **Step 3: Rewrite the indexes with domain-specific semantics**

Use these exact replacements:

```md
# Methods Index

> 本页负责 Method 对象域导航：先定位正式方法实例，再进入具体方法页；placeholder 方法仅用于图谱解析，不作为默认入口。

## 1. 对象域说明
- 本域收录 Method 节点。
- 默认 serving-ready 的方法进入“导航入口”。
- placeholder 方法进入“其他实例（不可导航）”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[PathMind]]：集成方法，强调路径优先化与重要推理路径引导，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Concepts Index

> 本页负责 Concept 对象域导航：先定位正式概念实例，再进入具体概念页。

## 1. 对象域说明
- 本域收录 Concept 节点。
- 默认 serving-ready 概念进入“导航入口”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[路径优先化]]：用于识别高价值 reasoning path 的核心概念，状态=serving-ready
- [[重要推理路径]]：面向答案生成的高价值推理路径概念，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Tasks Index

> 本页负责 Task 对象域导航：先定位正式任务实例，再进入具体任务页。

## 1. 对象域说明
- 本域收录 Task 节点。
- 默认 serving-ready 任务进入“导航入口”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[knowledge-graph-reasoning]]：知识图谱推理总任务，关注结构化多步推理，状态=serving-ready
- [[kgqa]]：知识图谱问答任务，关注自然语言问题到图结构推理映射，状态=serving-ready
- [[multi-hop-qa]]：复杂多跳问答任务，关注长推理链与噪声控制，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Scenarios Index

> 本页负责 Scenario 对象域导航：先定位正式场景实例，再进入具体场景页。

## 1. 对象域说明
- 本域收录 Scenario 节点。
- 默认 serving-ready 场景进入“导航入口”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[知识图谱推理问答]]：知识图谱上的复杂问答应用场景，强调多跳推理与噪声控制，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Benchmarks Index

> 本页负责 Benchmark 对象域导航：先定位正式 benchmark 实例，再进入具体 benchmark 页。

## 1. 对象域说明
- 本域收录 Benchmark 节点。
- 默认 serving-ready benchmark 进入“导航入口”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[WebQSP]]：KGQA benchmark，评测知识图谱问答表现，状态=serving-ready
- [[CWQ]]：复杂多跳 KGQA benchmark，评测复杂组合推理能力，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Evidence Index

> 本页负责 Evidence 对象域导航：先定位正式证据实例，再进入具体证据页。

## 1. 对象域说明
- 本域收录 Evidence 节点。
- 默认 serving-ready 证据页进入“导航入口”。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[PathMind.sections]]：章节与方法机制证据，服务 PathMind 主体知识抽取，状态=serving-ready
- [[PathMind.refs]]：引用与上游工作证据，服务 cites grounding，状态=serving-ready
- [[PathMind.experiments]]：实验与 benchmark 结果证据，服务 evaluated_on 与 supported_by，状态=serving-ready
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

```md
# Raw Sources Index

> 本页负责 RawSource 受管原始文件导航：先定位原始 PDF，再在需要时直接打开文件进行最终回查。

## 1. 对象域说明
- 本域收录受管原始 PDF 文件。
- 默认从本页进入 provenance 回查原件。

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
- [[files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]：PathMind 原始 PDF，用于 provenance 回查
- [[files/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]：survey 原始 PDF，用于 provenance 回查
<!-- END MANAGED BLOCK:navigation-entries -->
```

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_all_entity_indexes_use_navigation_and_placeholder_blocks -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ontology/entities/methods/index.md ontology/entities/concepts/index.md ontology/entities/tasks/index.md ontology/entities/scenarios/index.md ontology/entities/benchmarks/index.md ontology/entities/evidence/index.md ontology/entities/raw-sources/index.md scripts/test_lint_graph.py
git commit -m "refactor: convert entity indexes to navigation blocks"
```

### Task 4: Update lint to enforce the new index model

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Write the failing lint-behavior test**

Add this test:

```python
    def test_lint_graph_rejects_placeholder_in_navigation_entries(self):
        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        self.assertIn('non-serving-placeholders', text)
        self.assertIn('navigation-entries', text)
        self.assertIn('placeholder', text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_placeholder_in_navigation_entries -v`
Expected: FAIL because lint still enforces the old block names and old canonical-list behavior.

- [ ] **Step 3: Replace the old index validation logic minimally**

In `scripts/lint_graph.py`:

1. Replace `INDEX_MANAGED_BLOCKS` with:

```python
INDEX_MANAGED_BLOCKS = {
    'ontology/entities/papers/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/methods/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/concepts/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/tasks/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/scenarios/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/benchmarks/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/evidence/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/raw-sources/index.md': ['navigation-entries'],
}
```

2. Replace the old `canonical-list` check in `validate_index_pages` with block-aware checks:

```python
def validate_index_pages(errors: list[str]) -> None:
    for rel in DOMAIN_INDEX_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f'missing domain index file: {rel}')
            continue
        text = read_text(rel)
        for block_name in INDEX_MANAGED_BLOCKS[rel]:
            block = extract_managed_block(text, block_name)
            if block is None:
                errors.append(f'missing managed block {block_name} in {rel}')

        if '## 5. 相关关系账本' in text:
            errors.append(f'legacy relation-entry section must be removed from {rel}')

        navigation_block = extract_managed_block(text, 'navigation-entries') or ''
        placeholder_block = extract_managed_block(text, 'non-serving-placeholders') or ''

        for line in [ln.strip() for ln in navigation_block.splitlines() if ln.strip().startswith('- [[')]:
            if '：' not in line:
                errors.append(f'missing semantic description in navigation entry {line} in {rel}')
            if 'placeholder' in line:
                errors.append(f'placeholder promoted into navigation entries in {rel}: {line}')

        for line in [ln.strip() for ln in placeholder_block.splitlines() if ln.strip().startswith('- [[')]:
            if '：' not in line:
                errors.append(f'missing semantic description in placeholder entry {line} in {rel}')
            if 'status=placeholder' not in line:
                errors.append(f'non-serving placeholder missing status marker in {rel}: {line}')
```

3. Remove the old `canonical-list` page-existence requirement entirely.

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_lint_graph_rejects_placeholder_in_navigation_entries -v`
Expected: PASS

- [ ] **Step 5: Run the full lint suite**

Run: `python3 -m unittest scripts.test_lint_graph -v`
Expected: all tests PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/lint_graph.py scripts/test_lint_graph.py
git commit -m "test: enforce object-domain index navigation rules"
```

### Task 5: Reconcile placeholder materialization with the new paper-index structure

**Files:**
- Modify: `.claude/skills/paper-ingest/materialize_cited_paper_placeholders.py`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `scripts/test_lint_graph.py`

- [ ] **Step 1: Write the failing behavior test**

Add this test:

```python
    def test_materializer_puts_cited_placeholders_only_in_non_serving_block(self):
        text = (ROOT / '.claude' / 'skills' / 'paper-ingest' / 'materialize_cited_paper_placeholders.py').read_text(encoding='utf-8')
        self.assertIn('non-serving-placeholders', text)
        self.assertNotIn('core-entry', text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_lint_graph.LintGraphTests.test_materializer_puts_cited_placeholders_only_in_non_serving_block -v`
Expected: FAIL because the materializer still knows the old block model.

- [ ] **Step 3: Update the materializer minimally**

In `.claude/skills/paper-ingest/materialize_cited_paper_placeholders.py`:

1. Replace `add_to_index` with:

```python
def add_to_non_serving_placeholder_block(index_path: Path, title: str, source_page_stem: str) -> None:
    text = index_path.read_text(encoding='utf-8')
    line = f'- [[{title}]]：{source_page_stem} 引用的上游论文，占位节点，状态=placeholder'
    start = '<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->'
    end = '<!-- END MANAGED BLOCK:non-serving-placeholders -->'
    if start not in text or end not in text:
        return
    block = text.split(start, 1)[1].split(end, 1)[0]
    if line in block:
        return
    insertion = block.rstrip('\n') + ('\n' if block.strip() else '') + line + '\n'
    text = text.replace(f'{start}{block}{end}', f'{start}{insertion}{end}')
    index_path.write_text(text, encoding='utf-8')
```

2. Call it only for placeholder pages:

```python
        if index_path.exists():
            add_to_non_serving_placeholder_block(index_path, target, source_page_stem)
```

3. Remove the old behavior that writes placeholders into all managed blocks.

4. Update `.claude/skills/paper-ingest/SKILL.md` with one explicit sentence:

```md
- 自动生成的 cited paper placeholder 只允许进入对象域 index 的“其他实例（不可导航）”区块，不得提升到默认导航入口。
```

- [ ] **Step 4: Run the targeted tests to verify they pass**

Run:

```bash
python3 -m unittest \
  scripts.test_lint_graph.LintGraphTests.test_materialize_cited_paper_placeholders_creates_missing_pages \
  scripts.test_lint_graph.LintGraphTests.test_materializer_puts_cited_placeholders_only_in_non_serving_block -v
```

Expected: both PASS

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/paper-ingest/materialize_cited_paper_placeholders.py .claude/skills/paper-ingest/SKILL.md scripts/test_lint_graph.py
git commit -m "feat: keep cited placeholders out of default navigation"
```

### Task 6: Verify the redesigned index model on the current PathMind batch

**Files:**
- Modify: generated index pages and paper placeholders as needed
- Test: lint + governance chain

- [ ] **Step 1: Regenerate the cited placeholders using the updated materializer**

Run:

```bash
python3 .claude/skills/paper-ingest/materialize_cited_paper_placeholders.py \
  --cites-ledger ontology/relations/cites.md \
  --papers-dir ontology/entities/papers \
  --source-page "ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" \
  --paper-index ontology/entities/papers/index.md
```

Expected: placeholders exist and are added only to the non-serving block.

- [ ] **Step 2: Run the full lint suite**

Run: `python3 -m unittest scripts.test_lint_graph -v`
Expected: all tests PASS

- [ ] **Step 3: Run graph lint**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Re-run ontology semantic review and serving governance review**

Run the existing governance flow for the current PathMind batch.
Expected:
- semantic review: no issue that entity indexes mix relation-layer entrances
- serving review: placeholder papers are indexed as non-serving, not promoted as default paper entry surfaces

- [ ] **Step 5: Commit**

```bash
git status
```

Expected: clean working tree, or only intentional review artifacts.

---

## Self-review

### Spec coverage
- Covers the new object-domain-only index responsibility.
- Covers domain-specific semantic descriptions.
- Covers automated placeholder placement and pipeline consistency.
- Covers lint and governance enforcement.

### Placeholder scan
- No TBD / TODO placeholders remain.
- Every code-changing step includes concrete content.
- No cross-task shorthand is used.

### Type consistency
- Managed block names are consistently `navigation-entries` and `non-serving-placeholders`.
- Placeholder state is consistently represented as `status=placeholder` in index entries and `status: placeholder` in placeholder pages.
