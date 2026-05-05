# Obsidian Graph Inflation Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce Obsidian graph inflation by cleanly separating formal-neighbor links from context links, so migrated pages preserve reading value while the graph view more closely reflects `Formal relations`.

**Architecture:** First update the formal rules in `wiki/ontology/graph-standard.md` and the sync behavior in `page-projection-sync` so the two-link model is explicit. Then add lint protection in `scripts/lint_graph.py` to stop non-formal wikilinks from creeping back into context-only blocks. Finally, clean the highest-value migrated pages in the PathMind/high-frequency and survey/framework mainlines by converting context-only wikilinks into plain text while keeping true formal-neighbor links as wikilinks.

**Tech Stack:** Markdown page templates in `wiki/`, skill documentation in `.claude/skills/`, Python 3 lint script (`scripts/lint_graph.py`).

---

## File map

### Rules and sync behavior
- Modify: `wiki/ontology/graph-standard.md`
  - Add the formal-neighbor vs context-link rule.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Make sync emit formal-neighbor links as wikilinks and context links as plain text.
- Modify: `scripts/lint_graph.py`
  - Add protection against wikilinks appearing in context-only blocks.

### PathMind / high-frequency mainline pages
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Modify: `wiki/benchmarks/WebQSP.md`
- Modify: `wiki/benchmarks/CWQ.md`
- Modify: `wiki/methods/PathMind.md`
- Modify: `wiki/methods/RoG.md`
- Modify: `wiki/methods/GCR.md`
- Modify: `wiki/methods/EPERM.md`
- Modify: `wiki/methods/ToG.md`

### Survey / framework mainline pages
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `serving-governance-review`

---

### Task 1: Add the two-link rule to `graph-standard.md`

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Insert a new rule block after `## Formal relations 区块规范`**

Add this block immediately after the current `Formal relations` rules:

```markdown
## 人类友好关系区块的链接分层
- 人类友好关系区块中的链接分为两类：formal-neighbor links 与 context links。
- formal-neighbor links：仅指已经在当前页 `Formal relations` 中出现、且与正式关系账本一致的一跳正式邻居；允许使用 `[[wikilink]]`。
- context links：仅用于背景路线、对比对象、延伸阅读、同主题导航或阅读辅助；不保证存在 formal edge，默认不得使用 `[[wikilink]]`。
- 若某链接不属于 formal-neighbor links，就不应因为阅读方便而直接写成 `[[wikilink]]`，否则会污染 Obsidian 图谱层。
```

- [ ] **Step 2: Run lint after the rule addition**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 2: Teach `page-projection-sync` the two-link model

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a formal-neighbor vs context-link section to the skill**

Insert this block after `## 自动同步内容`:

```markdown
## 两层链接模型
- formal-neighbor links：仅限已存在于当前页 `Formal relations` 且与正式关系账本一致的一跳邻居；保留 `[[wikilink]]`。
- context links：背景路线、对比方法、延伸阅读、同主题导航等阅读辅助信息；输出为纯文本，不使用 `[[wikilink]]`。
```

- [ ] **Step 2: Add explicit sync behavior for context links**

Append this block after `## 不自动同步`:

```markdown
## 上下文链接同步规则
- 当人类友好区块中的信息只属于 context link 时，保留信息但改写为纯文本。
- 不得因为页面可读性需求把 context link 自动输出为 `[[wikilink]]`。
- formal-neighbor block 与 context block 必须分开组织，避免单一区块混用两类链接。
```

- [ ] **Step 3: Run lint after the sync-skill update**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 3: Add lint protection against context-only wikilinks in migrated pages

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add a small list of context-only headings that should not contain wikilinks**

After the existing constants near the top of `scripts/lint_graph.py`, add:

```python
CONTEXT_ONLY_HEADINGS = {
    '## 相关方法 / 路线',
    '## 背景路线',
    '## 延伸阅读',
}
```

- [ ] **Step 2: Add a helper that checks context-only headings for wikilinks**

Insert this helper near the parsing helpers:

```python
def find_heading_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith('## '):
            current = line
            blocks.setdefault(current, [])
            continue
        if current is not None:
            blocks[current].append(line)
    return {k: '\n'.join(v) for k, v in blocks.items()}
```

- [ ] **Step 3: Add a validation loop for migrated pages only**

Insert this block before the final `if errors:`:

```python
for rel in PHASE_ONE_CORE_PAGES:
    text = read_text(rel)
    blocks = find_heading_blocks(text)
    for heading in CONTEXT_ONLY_HEADINGS:
        if heading in blocks and WIKILINK_RE.search(blocks[heading]):
            errors.append(f'context-only heading {heading} contains wikilinks in {rel}')
```

- [ ] **Step 4: Run lint; expect it to fail before page cleanup if any context-only blocks still use wikilinks**

Run: `python3 scripts/lint_graph.py`
Expected: either PASS immediately or FAIL specifically on context-only headings that still contain wikilinks.

---

### Task 4: Clean the PathMind / high-frequency mainline pages

**Files:**
- Modify: `wiki/concepts/路径优先化.md`
- Modify: `wiki/concepts/重要推理路径.md`
- Modify: `wiki/tasks/knowledge-graph-reasoning.md`
- Modify: `wiki/tasks/kgqa.md`
- Modify: `wiki/tasks/multi-hop-qa.md`
- Modify: `wiki/scenarios/知识图谱推理问答.md`
- Modify: `wiki/benchmarks/WebQSP.md`
- Modify: `wiki/benchmarks/CWQ.md`
- Modify: `wiki/methods/PathMind.md`
- Modify: `wiki/methods/RoG.md`
- Modify: `wiki/methods/GCR.md`
- Modify: `wiki/methods/EPERM.md`
- Modify: `wiki/methods/ToG.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Convert broad concept-page route blocks to context-only plain text**

In `wiki/concepts/LLM增强知识图谱.md`-style patterns and any concept pages with `## 相关方法 / 路线`, remove wikilink syntax from entries that are only background routes and not one-hop formal neighbors.

Expected transformation pattern:

```markdown
## 相关方法 / 路线
- PathMind
- RoG
- GCR
- ToG
```

instead of `[[PathMind]]`, `[[RoG]]`, etc.

- [ ] **Step 2: Convert method-page comparison blocks to context-only plain text where needed**

For `## 与其他方法的对比` blocks in migrated method pages, keep the comparison information but replace context-only wikilinks with plain text unless the compared method is also a one-hop formal neighbor.

- [ ] **Step 3: Convert benchmark-page contextual task/scenario links to plain text if they are not formal neighbors**

In `WebQSP.md` and `CWQ.md`, keep human-readable task/scenario context, but use plain text for non-formal contextual links if they are not represented in `Formal relations`.

- [ ] **Step 4: Run lint after the PathMind/high-frequency cleanup**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 5: Clean the survey / framework mainline pages

**Files:**
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Modify: `wiki/scenarios/复杂产品设计.md`
- Modify: `wiki/tasks/engineering-design-knowledge-management.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Keep only true formal neighbors as wikilinks in the survey paper’s related-object blocks**

In the survey paper page, leave links that correspond to explicit `Formal relations` as wikilinks, but turn purely contextual references into plain text.

- [ ] **Step 2: Convert concept-page related-method/route navigation into context-only text**

On `wiki/concepts/LLM增强知识图谱.md`, convert broad route-navigation links like PathMind / RoG / GCR / ToG into plain text, while keeping formal neighbors like the survey paper and framework concept as wikilinks.

- [ ] **Step 3: Keep scenario/task pages aligned with formal-neighbor-only wikilinks**

On `wiki/scenarios/复杂产品设计.md` and `wiki/tasks/engineering-design-knowledge-management.md`, leave only links that correspond to actual `Formal relations` as wikilinks. Any broader background references should become plain text.

- [ ] **Step 4: Run lint after the survey/framework cleanup**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 6: Re-run serving-governance after cleanup

**Files:**
- Modify: none unless the review identifies a minimal corrective fix
- Test: `serving-governance-review`, `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run `serving-governance-review` on the cleaned migrated pages**

Review this exact set:
- `wiki/concepts/路径优先化.md`
- `wiki/concepts/重要推理路径.md`
- `wiki/tasks/knowledge-graph-reasoning.md`
- `wiki/tasks/kgqa.md`
- `wiki/tasks/multi-hop-qa.md`
- `wiki/scenarios/知识图谱推理问答.md`
- `wiki/benchmarks/WebQSP.md`
- `wiki/benchmarks/CWQ.md`
- `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `wiki/concepts/LLM增强知识图谱.md`
- `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- `wiki/scenarios/复杂产品设计.md`
- `wiki/tasks/engineering-design-knowledge-management.md`

Expected: serving completeness remains intact while context-only link inflation is reduced.

- [ ] **Step 2: If the review finds a minimal issue, apply only that issue’s smallest fix and rerun lint**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 7: Final verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`, `git status --short`

- [ ] **Step 1: Run the final lint check**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Verify the cleanup did not touch relation ledgers**

Run:

```bash
git diff -- \
  wiki/relations/citation_graph.md \
  wiki/relations/method_evolution.md \
  wiki/relations/concept_links.md \
  wiki/relations/task_method_map.md \
  wiki/relations/benchmark_links.md \
  wiki/relations/evidence_index.md \
  wiki/relations/paper_method_links.md \
  wiki/relations/provenance_links.md
```

Expected: no new changes introduced by this cleanup pass.

- [ ] **Step 3: Do not auto-commit unless separately requested**

Run: `git status --short`
Expected: the working tree remains available for review.
