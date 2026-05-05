# Intermediate Evidence Cache Minimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce a hard-minimum `intermediate/papers/` Evidence cache model by paper type, remove `full`, update ontology/process/lint contracts, migrate provenance and object-page references, and delete the legacy full cache files.

**Architecture:** First update the normative sources (`wiki/ontology/graph-standard.md`, `CLAUDE.md`, and ingest-related skill docs) so the repository defines the minimized Evidence model consistently. Then update `scripts/lint_graph.py` to forbid `full`, enforce cache-set expectations, and reject lingering references. Finally, clean up provenance and serving pages, remove the two legacy `*.full.md` files, and run lint to verify that standards, skills, content, and governance now agree.

**Tech Stack:** Markdown knowledge pages and skill docs, Python 3 lint script (`scripts/lint_graph.py`), git.

---

## File map

### Normative ontology and workflow files
- Modify: `wiki/ontology/graph-standard.md`
  - Remove `full` from formal Evidence cache types, define paper-type-to-cache-set rules, define `sections` / `analysis` boundaries, and add a redundancy retirement rule.
- Modify: `CLAUDE.md`
  - Reframe `intermediate/papers/` as the minimal Evidence cache layer instead of a broad working-draft space.

### Compile / ingest skill docs
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Remove `full` from default/optional outputs and make the cache split hard by paper type.
- Review only: `.claude/skills/relation-reconciliation/SKILL.md`
  - Confirm no wording change is required because it already routes retained Evidence caches generically.
- Review only: `.claude/skills/page-projection-sync/SKILL.md`
  - Confirm no wording change is required because it already treats Evidence links generically.

### Lint contract and sample expectations
- Modify: `scripts/lint_graph.py`
  - Remove `full` from sample cache inventories, sample expected links, and evidence guidance checks.
  - Add checks for forbidden `cache_type: full`, forbidden `*.full` references, and undeclared cache types.

### Provenance ledger and serving pages
- Modify: `wiki/relations/provenance_links.md`
  - Remove the two `full --sourced_from--> raw` edges.
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
  - Remove “高保真工作底稿” references.
- Modify: `wiki/concepts/LLM增强知识图谱.md`
  - Remove the `LLM-KG-CPD-Survey.full` evidence link.
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
  - Remove the `LLM-KG-CPD-Survey.full` evidence link.

### Legacy files to delete
- Delete: `intermediate/papers/PathMind.full.md`
- Delete: `intermediate/papers/LLM-KG-CPD-Survey.full.md`

### Verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: `git grep -n "\.full\|cache_type: full\|高保真工作底稿" wiki intermediate .claude/skills scripts CLAUDE.md`

---

### Task 1: Update `graph-standard.md` to define the minimized Evidence cache model

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Remove `full` from the allowed `cache_type` list**

In `wiki/ontology/graph-standard.md`, replace:

```markdown
- `cache_type` 使用 `sections` / `refs` / `experiments` / `analysis` / `full`
```

with:

```markdown
- `cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`
```

- [ ] **Step 2: Add hard-minimum cache-set rules to the Evidence section**

Directly after the `cache_type` bullet in the `### Evidence` section, insert:

```markdown
- 按论文类型执行最小缓存集合：
  - empirical / method / application 论文：`sections` + `refs` + `experiments`
  - survey / framework / taxonomy / benchmark-landscape 论文：`sections` + `refs` + `analysis`
  - theoretical / position 论文：`sections` + `refs`
- 不允许在未更新本规范前新增其他正式 cache 类型。
```

- [ ] **Step 3: Add `sections` and `analysis` responsibility boundaries**

Directly after the `正文标准结构` list in the `### Evidence` section, insert:

```markdown
- `sections` 用于章节结构、核心机制与足以支撑 formal relation 审计的章节级摘要；不得扩张为接近整篇论文的重写稿，或与正式论文页形成大段叙述重复。
- `analysis` 仅用于 survey / framework / taxonomy / benchmark-landscape 类论文的统计、landscape、阶段分析、框架拆解或非统一实验型证据；不得作为 empirical 论文的常规第三缓存，也不得充当泛化“额外总结页”。
- 若新增 `sections` 内容不能提升 formal relation 可审计性或章节级复用性，则不应写入。
```

- [ ] **Step 4: Add a cache-retirement rule to governance guidance**

Insert this new subsection immediately before `## 证据要求`:

```markdown
## 冗余 cache 判废规则
- 若某 cache 类型不承载独立证据职责，且相对现有 cache 类型不提供不可替代的结构化审计价值，则不得作为正式 cache 类型保留。
- 新增 cache 类型前，必须先在本规范中声明其证据职责、适用论文类型与 relation / provenance 作用范围。
```

- [ ] **Step 5: Replace the old mechanism-evidence guidance that still mentions `full`**

In `## 证据要求`, replace:

```markdown
- 方法机制优先绑定 `sections.md` 或 `full.md`。
```

with:

```markdown
- 方法机制优先绑定 `sections.md`。
```

- [ ] **Step 6: Strengthen provenance wording so retained caches are first-class anchors**

In the `sourced_from` bullet, append this sentence to the end of the paragraph:

```markdown
保留的 `sections`、`refs`、`experiments`、`analysis` 均可直接承担 `sourced_from` provenance 锚点，不依赖额外全文型 cache。
```

- [ ] **Step 7: Run lint to confirm the ontology file still parses and passes repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 2: Update `CLAUDE.md` and `paper-ingest` to remove `full` from the default compile contract

**Files:**
- Modify: `CLAUDE.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Tighten the `CLAUDE.md` description of the Evidence layer**

In `CLAUDE.md`, replace:

```markdown
- `intermediate/papers/` 是机制、实验、引用、基线与 provenance 的默认证据层
```

with:

```markdown
- `intermediate/papers/` 是最小化的正式 Evidence 缓存层，用于机制、实验、引用、基线与 provenance 核验
```

- [ ] **Step 2: Remove the `full.md` recommendation from the ingest core principles**

In `.claude/skills/paper-ingest/SKILL.md`, replace this three-item block:

```markdown
2. 默认生成 3 份基础缓存：
   - `[short_name].sections.md`
   - `[short_name].refs.md`
   - 第三缓存按论文类型分流（`experiments.md` 或 `analysis.md`）
3. `full.md` 属于高复用工作底稿，按需生成；若论文需要跨章节深挖、长篇比较、框架抽象或高保真叙事保留时，默认建议生成
```

with:

```markdown
2. 默认按论文类型生成最小缓存集合：
   - empirical / method / application 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].experiments.md`
   - survey / framework / taxonomy / benchmark-landscape 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].analysis.md`
   - theoretical / position 论文：`[short_name].sections.md`、`[short_name].refs.md`
3. 不生成 `full.md`；若未来需要新增 cache 类型，必须先更新本体规范与 skill 合约，而不是临时加文件
```

- [ ] **Step 3: Rewrite the cache-generation step to remove the optional `full` path**

In the `### Step 3: 生成 intermediate 缓存` section of `.claude/skills/paper-ingest/SKILL.md`, replace the whole block starting at:

```markdown
在 `intermediate/papers/` 下默认生成以下 3 份基础缓存：
```

through the `生成要求` bullets with:

```markdown
在 `intermediate/papers/` 下按论文类型生成最小缓存集合：

1. 所有论文默认生成：
   - `[short_name].sections.md`
   - `[short_name].refs.md`
2. 第三缓存按论文类型分流：
   - empirical / method / application 论文：`[short_name].experiments.md`
   - survey / framework / benchmark / taxonomy / dataset / benchmark-landscape 论文：`[short_name].analysis.md`
3. theoretical / position 论文不生成第三缓存，除非本体规范后续明确扩展

生成要求：
- `sections.md` 是默认分析入口，承担章节结构、核心机制与 formal relation 审计所需的最小章节级摘要
- `refs.md` 服务引用关系、方法演化与上游基线 grounding
- `experiments.md` 仅用于实验、消融、效率、泛化与 benchmark 结果证据
- `analysis.md` 仅用于综述统计、landscape、阶段分析、software-gap 分析、framework 支撑证据或 benchmark 设计分析
- 不生成 `full.md`，也不以长篇高保真重写稿替代 `sections.md`
```

- [ ] **Step 4: Remove `full` from `sourced_from` and output-format guidance**

Make these exact edits in `.claude/skills/paper-ingest/SKILL.md`:

1. Replace:

```markdown
- 只要本次生成了 `sections.md`、`refs.md`、`experiments.md`、`analysis.md`、`full.md` 任一 Evidence 缓存，就必须同步登记 `[[Evidence]] --sourced_from--> [[RawSource]]`
```

with:

```markdown
- 只要本次生成了 `sections.md`、`refs.md`、`experiments.md`、`analysis.md` 任一 Evidence 缓存，就必须同步登记 `[[Evidence]] --sourced_from--> [[RawSource]]`
```

2. In the final YAML example, replace:

```markdown
  - intermediate/papers/<short_name>.experiments.md | intermediate/papers/<short_name>.analysis.md
  - intermediate/papers/<short_name>.full.md (optional, generated when deep cross-section tracing is needed)
```

with:

```markdown
  - intermediate/papers/<short_name>.experiments.md | intermediate/papers/<short_name>.analysis.md
```

3. Replace:

```markdown
- `success`：基础缓存、正式页面与应有关系账本更新都已完成，且结构适配良好；如生成了 `full.md`，它作为高复用增强缓存计入 `generated_caches`。
```

with:

```markdown
- `success`：基础缓存、正式页面与应有关系账本更新都已完成，且结构适配良好。
```

- [ ] **Step 5: Update the example that still claims four caches for a standard method paper**

Near the end of `.claude/skills/paper-ingest/SKILL.md`, replace:

```markdown
预期：
- 生成 4 个缓存
```

with:

```markdown
预期：
- 生成 3 个缓存（`sections`、`refs`、`experiments`）
```

- [ ] **Step 6: Run lint after the workflow-contract edits**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

---

### Task 3: Update `scripts/lint_graph.py` to ban `full` and enforce the minimized cache contract

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`
- Test: `git grep -n "\.full\|cache_type: full\|高保真工作底稿" wiki intermediate .claude/skills scripts CLAUDE.md`

- [ ] **Step 1: Remove `full` from phase-one sample expectations**

In `scripts/lint_graph.py`, make these exact replacements:

1. In `PHASE_ONE_CORE_PAGES['wiki/concepts/复杂产品设计中的LLM-KG协同框架.md']['links']`, replace:

```python
            '[[intermediate/papers/LLM-KG-CPD-Survey.full',
```

with:

```python
            '[[intermediate/papers/LLM-KG-CPD-Survey.sections',
```

2. Replace the `PHASE_ONE_EVIDENCE_CACHES` constant:

```python
PHASE_ONE_EVIDENCE_CACHES = {
    'method': [
        'intermediate/papers/PathMind.sections.md',
        'intermediate/papers/PathMind.refs.md',
        'intermediate/papers/PathMind.experiments.md',
        'intermediate/papers/PathMind.full.md',
    ],
    'survey': [
        'intermediate/papers/LLM-KG-CPD-Survey.sections.md',
        'intermediate/papers/LLM-KG-CPD-Survey.refs.md',
        'intermediate/papers/LLM-KG-CPD-Survey.analysis.md',
        'intermediate/papers/LLM-KG-CPD-Survey.full.md',
    ],
}
```

with:

```python
PHASE_ONE_EVIDENCE_CACHES = {
    'method': [
        'intermediate/papers/PathMind.sections.md',
        'intermediate/papers/PathMind.refs.md',
        'intermediate/papers/PathMind.experiments.md',
    ],
    'survey': [
        'intermediate/papers/LLM-KG-CPD-Survey.sections.md',
        'intermediate/papers/LLM-KG-CPD-Survey.refs.md',
        'intermediate/papers/LLM-KG-CPD-Survey.analysis.md',
    ],
}
```

- [ ] **Step 2: Update the old evidence guidance needle that still mentions `full`**

Replace:

```python
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
```

with:

```python
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    '`cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`',
```

Then add this string to the same list:

```python
    '方法机制优先绑定 `sections.md`。',
```

- [ ] **Step 3: Add an explicit ban on `full` caches and references**

Insert this block after the existing constant declarations and before the first function definition:

```python
ALLOWED_EVIDENCE_CACHE_TYPES = {'sections', 'refs', 'experiments', 'analysis'}
FORBIDDEN_FULL_REFERENCE_NEEDLES = (
    '.full|',
    '.full]]',
    'cache_type: full',
    '高保真工作底稿',
)
FULL_REFERENCE_SCAN_PATHS = [
    ROOT / 'wiki',
    ROOT / 'intermediate' / 'papers',
    ROOT / '.claude' / 'skills',
    ROOT / 'scripts',
    ROOT / 'CLAUDE.md',
]
```

- [ ] **Step 4: Add a helper that validates Evidence cache types in frontmatter**

Insert this function before the main `lint()` function:

```python
def check_evidence_cache_types(errors):
    for path in sorted((ROOT / 'intermediate' / 'papers').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        match = re.search(r'^cache_type:\s*([^\n]+)$', text, re.MULTILINE)
        if not match:
            errors.append(f"Missing cache_type in evidence cache: {path.relative_to(ROOT)}")
            continue
        cache_type = match.group(1).strip()
        if cache_type not in ALLOWED_EVIDENCE_CACHE_TYPES:
            errors.append(
                f"Forbidden or undeclared cache_type '{cache_type}' in {path.relative_to(ROOT)}"
            )
```

- [ ] **Step 5: Add a helper that scans for forbidden full references**

Insert this function directly after `check_evidence_cache_types`:

```python
def check_forbidden_full_references(errors):
    for scan_path in FULL_REFERENCE_SCAN_PATHS:
        paths = [scan_path] if scan_path.is_file() else sorted(p for p in scan_path.rglob('*.md'))
        if scan_path == ROOT / 'scripts':
            paths = sorted(p for p in scan_path.rglob('*.py'))
        for path in paths:
            text = path.read_text(encoding='utf-8')
            for needle in FORBIDDEN_FULL_REFERENCE_NEEDLES:
                if needle in text:
                    errors.append(f"Forbidden full-cache reference '{needle}' found in {path.relative_to(ROOT)}")
```

- [ ] **Step 6: Wire the new checks into the lint entrypoint**

Inside the main lint flow, add these calls alongside the existing structural checks:

```python
    check_evidence_cache_types(errors)
    check_forbidden_full_references(errors)
```

Use the same indentation level as the other `check_*` calls already present in the file.

- [ ] **Step 7: Run lint and then verify the forbidden strings are gone**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

Then run: `git grep -n "\.full\|cache_type: full\|高保真工作底稿" wiki intermediate .claude/skills scripts CLAUDE.md`
Expected: no matches

---

### Task 4: Clean up provenance and serving-page references, then delete the legacy `full` files

**Files:**
- Modify: `wiki/relations/provenance_links.md`
- Modify: `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- Modify: `wiki/concepts/LLM增强知识图谱.md`
- Modify: `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`
- Delete: `intermediate/papers/PathMind.full.md`
- Delete: `intermediate/papers/LLM-KG-CPD-Survey.full.md`
- Test: `python3 scripts/lint_graph.py`
- Test: `git grep -n "\.full\|cache_type: full\|高保真工作底稿" wiki intermediate .claude/skills scripts CLAUDE.md`

- [ ] **Step 1: Remove the two `full` provenance edges**

In `wiki/relations/provenance_links.md`, delete exactly these four lines:

```markdown
- `[[intermediate/papers/PathMind.full|PathMind.full]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: full 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.full|PathMind.full]] frontmatter `source_pdf`
```

and

```markdown
- `[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: full 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]] frontmatter `source_pdf`
```

- [ ] **Step 2: Remove `full` references from the survey Paper page**

In `wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`, delete these two lines:

```markdown
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]
```

One appears under `## 综述证据来源`, and one appears under `## 证据来源`.

- [ ] **Step 3: Remove `full` references from the two concept pages**

In `wiki/concepts/LLM增强知识图谱.md`, delete:

```markdown
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]
```

In `wiki/concepts/复杂产品设计中的LLM-KG协同框架.md`, delete:

```markdown
- 高保真工作底稿：[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]]
```

- [ ] **Step 4: Delete the two obsolete full-cache files**

Run:

```bash
rm "intermediate/papers/PathMind.full.md" "intermediate/papers/LLM-KG-CPD-Survey.full.md"
```

Expected: command exits with status 0 and both files disappear from `git status` as deletions.

- [ ] **Step 5: Run lint and then prove no `full` references remain**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

Then run: `git grep -n "\.full\|cache_type: full\|高保真工作底稿" wiki intermediate .claude/skills scripts CLAUDE.md`
Expected: no matches

- [ ] **Step 6: Commit the minimized Evidence cache migration**

Run:

```bash
git add wiki/ontology/graph-standard.md CLAUDE.md .claude/skills/paper-ingest/SKILL.md scripts/lint_graph.py wiki/relations/provenance_links.md "wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md" "wiki/concepts/LLM增强知识图谱.md" "wiki/concepts/复杂产品设计中的LLM-KG协同框架.md" intermediate/papers/PathMind.full.md intermediate/papers/LLM-KG-CPD-Survey.full.md
git commit -m "refactor: minimize intermediate evidence caches"
```

Expected: commit succeeds and `git status --short` no longer shows these paths as modified.

---

## Self-review

### Spec coverage
- Hard-minimum cache sets by paper type: covered in Task 1 and Task 2.
- Remove `full` from the formal model: covered in Tasks 1, 2, 3, and 4.
- Provenance migration off `full`: covered in Task 1 Step 6 and Task 4 Step 1.
- Lint enforcement for forbidden `full` and undeclared cache types: covered in Task 3.
- Cleanup of existing `full` references and legacy files: covered in Task 4.

No spec requirement is left without a concrete task.

### Placeholder scan
- No `TODO`, `TBD`, or “similar to” placeholders remain.
- All commands, file paths, and text replacements are explicit.

### Type consistency
- Allowed cache types are consistently `sections`, `refs`, `experiments`, `analysis`.
- `full` is consistently treated as forbidden legacy state.
- Provenance remains `[[Evidence]] --sourced_from--> [[RawSource]]` throughout the plan.
