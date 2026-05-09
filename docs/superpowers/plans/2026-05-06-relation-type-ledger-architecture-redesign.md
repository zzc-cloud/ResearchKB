# Relation-Type Ledger Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current mixed relation-ledger system with a one-relation-type-per-file formal ledger architecture, migrate all formal relation truth into the new files, and update every runtime contract to read, write, project, and lint against the new ledger layout.

**Architecture:** First rewrite the normative and cognitive layers so the repository explicitly defines a one-relation-type-per-file relation system. Then create the new ledger files and migrate all existing relation instances into them, making the new files the only formal truth source. After the truth source migration, update runtime skills, page projection behavior, and lint rules to target the new relation-type files, then rewrite object/evidence references and remove the retired clustered ledgers.

**Tech Stack:** Markdown knowledge pages under `ontology/`, Claude skill contracts under `.claude/skills/`, Python 3 linting in `scripts/lint_graph.py`, Obsidian wikilinks, grep-based verification, unittest for script regression coverage.

---

## File map

### Normative and cognitive layers
- Modify: `ontology/graph-standard.md`
  - Replace clustered relation-file assignment rules with one-file-per-relation-type rules.
  - Update method-evolution, concept-network, service-layer, and projection language so it points at the new files.
- Modify: `CLAUDE.md`
  - Replace the relation entry list and relation-to-ledger mapping so AI can route directly from relation semantics to same-name ledgers.

### New relation-type formal ledgers to create
- Create: `ontology/relations/cites.md`
- Create: `ontology/relations/proposes.md`
- Create: `ontology/relations/based_on.md`
- Create: `ontology/relations/improves_on.md`
- Create: `ontology/relations/targets_task.md`
- Create: `ontology/relations/uses_concept.md`
- Create: `ontology/relations/depends_on.md`
- Create: `ontology/relations/supports.md`
- Create: `ontology/relations/applies_to.md`
- Create: `ontology/relations/evaluated_on.md`
- Create: `ontology/relations/supported_by.md`
- Create: `ontology/relations/sourced_from.md`

### Existing clustered or inconsistently named ledgers to retire
- Delete after migration: `ontology/relations/citation_graph.md`
- Delete after migration: `ontology/relations/method_evolution.md`
- Delete after migration: `ontology/relations/task_method_map.md`
- Delete after migration: `ontology/relations/concept_links.md`
- Delete after migration: `ontology/relations/paper_method_links.md`
- Delete after migration: `ontology/relations/benchmark_links.md`
- Delete after migration: `ontology/relations/evidence_index.md`
- Delete after migration: `ontology/relations/provenance_links.md`

### Runtime skills that route relations today
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md` (only if examples or wording name old ledgers)
- Modify: `.claude/skills/serving-governance-review/SKILL.md` (only if examples or wording name old ledgers)

### Object, evidence, and relation references
- Modify: `ontology/entities/**`
- Modify: `intermediate/papers/**`
- Modify: `ontology/relations/*.md` page headers and cross-links

### Lint and regression coverage
- Modify: `scripts/lint_graph.py`

---

### Task 1: Rewrite the normative and cognitive definition of relation ledgers

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Write the failing regression test for old clustered ledger names in lint contracts**

```python
    def test_lint_graph_uses_relation_type_ledger_names(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        combined_output = result.stdout + result.stderr
        self.assertNotIn('ontology/relations/citation_graph.md', combined_output)
        self.assertNotIn('ontology/relations/method_evolution.md', combined_output)
        self.assertNotIn('ontology/relations/concept_links.md', combined_output)
        self.assertNotIn('ontology/relations/task_method_map.md', combined_output)
        self.assertNotIn('ontology/relations/paper_method_links.md', combined_output)
        self.assertNotIn('ontology/relations/benchmark_links.md', combined_output)
        self.assertNotIn('ontology/relations/evidence_index.md', combined_output)
        self.assertNotIn('ontology/relations/provenance_links.md', combined_output)
```

- [ ] **Step 2: Run the new regression test and watch it fail for the expected reason**

Run:

```bash
```

Expected:
- FAIL
- Failure output still includes one or more old clustered ledger file names
- Failure must be about lingering old ledger names, not syntax or import errors

- [ ] **Step 3: Rewrite `ontology/graph-standard.md` relation-file ownership and projection wording**

Make these exact textual replacements in `ontology/graph-standard.md`:

1. In `### 4.3 关系文件分工`, replace the current clustered list with this block:

```md
### 4.3 关系文件分工
- 每个正式 relation type 都有且只有一个正式 ledger 文件，文件名直接等于 relation type：
  - `ontology/relations/cites.md`：维护 `cites`
  - `ontology/relations/proposes.md`：维护 `proposes`
  - `ontology/relations/based_on.md`：维护 `based_on`
  - `ontology/relations/improves_on.md`：维护 `improves_on`
  - `ontology/relations/targets_task.md`：维护 `targets_task`
  - `ontology/relations/uses_concept.md`：维护 `uses_concept`
  - `ontology/relations/depends_on.md`：维护 `depends_on`
  - `ontology/relations/supports.md`：维护 `supports`
  - `ontology/relations/applies_to.md`：维护 `applies_to`
  - `ontology/relations/evaluated_on.md`：维护 `evaluated_on`
  - `ontology/relations/supported_by.md`：维护 `supported_by`
  - `ontology/relations/sourced_from.md`：维护 `sourced_from`
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 边；若出现正式知识页到 RawSource 的临时占位关系，需显式标注 `status: placeholder` 并尽快补齐对应 Evidence 缓存。
- 新增关系类型或未归属关系类型，必须先在本节明确“归属文件 + 维护范围”，再进入正式实例边维护。
```

2. In `### 4.4 概念网络补充边标签`, replace the current block with:

```md
### 4.4 概念网络补充边标签
- `supports`、`depends_on`、`applies_to` 的语义见前文“关系类型”。
- 这些标签各自拥有独立 ledger 文件；若要新增新的概念网络补充边标签，必须先在 `### 4.3 关系文件分工` 中登记其独立归属文件。
```

3. In `### 5.2 全类型服务层投影规则`, replace the Method strong-field bullet with:

```md
- Method 的 `parent_methods` / `child_methods` 继续作为首批强一致派生字段，必须与 `ontology/relations/based_on.md`、`ontology/relations/improves_on.md` 中的正式方法演化边保持一致。
```

- [ ] **Step 4: Rewrite `CLAUDE.md` relation entry and mapping language**

Make these exact textual edits in `CLAUDE.md`:

1. In `#### 3.2 正式关系入口`, replace the current list and note with:

```md
#### 3.2 正式关系入口
- [[cites]]
- [[proposes]]
- [[based_on]]
- [[improves_on]]
- [[targets_task]]
- [[uses_concept]]
- [[depends_on]]
- [[supports]]
- [[applies_to]]
- [[evaluated_on]]
- [[supported_by]]
- [[sourced_from]]
- 用于 formal relation truth、治理、修复、审计与关系级核对；读取某种关系时，默认进入与 relation type 同名的 ledger 文件。
```

2. Immediately below `#### 3.2 正式关系入口`, insert this new subsection:

```md
#### 3.2.1 relation type → ledger file 映射
- `cites` → `ontology/relations/cites.md`
- `proposes` → `ontology/relations/proposes.md`
- `based_on` → `ontology/relations/based_on.md`
- `improves_on` → `ontology/relations/improves_on.md`
- `targets_task` → `ontology/relations/targets_task.md`
- `uses_concept` → `ontology/relations/uses_concept.md`
- `depends_on` → `ontology/relations/depends_on.md`
- `supports` → `ontology/relations/supports.md`
- `applies_to` → `ontology/relations/applies_to.md`
- `evaluated_on` → `ontology/relations/evaluated_on.md`
- `supported_by` → `ontology/relations/supported_by.md`
- `sourced_from` → `ontology/relations/sourced_from.md`
```

- [ ] **Step 5: Run the regression test again and verify it now passes**

Run:

```bash
```

Expected:
- PASS
- No old clustered ledger names appear in test output

---

### Task 2: Create all new relation-type ledger files with a unified template

**Files:**
- Create: `ontology/relations/cites.md`
- Create: `ontology/relations/proposes.md`
- Create: `ontology/relations/based_on.md`
- Create: `ontology/relations/improves_on.md`
- Create: `ontology/relations/targets_task.md`
- Create: `ontology/relations/uses_concept.md`
- Create: `ontology/relations/depends_on.md`
- Create: `ontology/relations/supports.md`
- Create: `ontology/relations/applies_to.md`
- Create: `ontology/relations/evaluated_on.md`
- Create: `ontology/relations/supported_by.md`
- Create: `ontology/relations/sourced_from.md`

- [ ] **Step 1: Create `ontology/relations/proposes.md` as the reference template**

Create this file:

```md
> 本页是正式关系账本：维护 `proposes` 实例边。默认问答优先读取对象页；只有在治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../entities/papers/index|papers/index]]、[[../entities/methods/index|methods/index]]、[[../entities/concepts/index|concepts/index]]
> 相关证据入口：[[supported_by]]、[[sourced_from]]

## `proposes` 实例边
- `proposes` 表示论文提出了某个正式知识产物。
- 常见 source：`Paper`
- 常见 target：`Method`、`Concept`
- 若 framework / taxonomy 的主语义是知识组织或解释框架，target 通常是 `Concept`；若主语义是方法流程或演化路线，target 通常是 `Method`。

## 实例边
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - reason: 论文提出了 PathMind 作为核心方法。
  - evidence: [[PathMind.sections|PathMind.sections]] §1、§7
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`
  - reason: survey 论文提出了复杂产品设计中的 LLM-KG 协同框架作为核心知识产物。
  - evidence: [[LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] §6–10
```

- [ ] **Step 2: Create the remaining 11 relation-type files by following the same structure**

Create each file with:
- the same three-part structure (`页头说明` → `关系语义说明` → `实例边`)
- relation-type-specific source/target guidance
- migrated sample edges from the current ledgers

Use these minimum required sample edges:

```md
# cites.md
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - reason: PathMind 将 RoG 作为相关上游工作引用。
  - evidence: [[PathMind.refs|PathMind.refs]] §2–4

# based_on.md
- `[[PathMind]] --based_on--> [[RoG]]`
  - reason: PathMind 沿用了 RoG 的路径推理主线作为上游基础。
  - evidence: [[PathMind.refs|PathMind.refs]] §2–4

# improves_on.md
- `[[PathMind]] --improves_on--> [[RoG]]`
  - reason: PathMind 在路径优先化与检索-推理协同上相对 RoG 形成改进。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4

# targets_task.md
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - reason: PathMind 直接面向知识图谱推理任务。
  - evidence: [[PathMind.sections|PathMind.sections]] §1、§7

# uses_concept.md
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
  - reason: PathMind 的核心机制之一是路径优先化。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4

# depends_on.md
- `[[重要推理路径]] --depends_on--> [[路径优先化]]`
  - reason: 重要推理路径的识别与筛选依赖路径优先化机制。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4

# supports.md
- `[[路径优先化]] --supports--> [[知识图谱推理问答]]`
  - reason: 路径优先化通过突出高价值证据路径支撑知识图谱推理问答场景中的答案推断。
  - evidence: [[PathMind.sections|PathMind.sections]] §1、§7

# applies_to.md
- `[[PathMind]] --applies_to--> [[知识图谱推理问答]]`
  - reason: PathMind 方法面向知识图谱推理问答场景落地。
  - evidence: [[PathMind.sections|PathMind.sections]] §1、§7

# evaluated_on.md
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
  - reason: PathMind 在 WebQSP 上进行了评估。
  - evidence: [[PathMind.experiments|PathMind.experiments]] §主要结果

# supported_by.md
- `[[PathMind]] --supported_by--> [[PathMind.sections|PathMind.sections]]`
  - reason: PathMind 的核心机制由 sections 证据页支撑。
  - evidence: [[PathMind.sections|PathMind.sections]] §7.1–7.4

# sourced_from.md
- `[[PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: sections 证据缓存直接来源于原始 PDF。
  - evidence: [[PathMind.sections|PathMind.sections]] §来源说明
```

- [ ] **Step 3: Verify all 12 new files exist before migrating runtime contracts**

Run:

```bash
for f in cites proposes based_on improves_on targets_task uses_concept depends_on supports applies_to evaluated_on supported_by sourced_from; do test -f "ontology/relations/${f}.md" || exit 1; done
```

Expected:
- Shell exits successfully
- All 12 new relation-type files exist

---

### Task 3: Migrate formal relation instances from the old ledgers into the new files

**Files:**
- Modify: all newly created `ontology/relations/*.md`
- Modify then later delete: old clustered ledgers

- [ ] **Step 1: Split `method_evolution.md` into `based_on.md` and `improves_on.md`**

Move every canonical edge from `ontology/relations/method_evolution.md` into exactly one of:
- `ontology/relations/based_on.md`
- `ontology/relations/improves_on.md`

Use this rule:
- inheritance / upstream borrowing → `based_on.md`
- explicit improvement / stronger later method → `improves_on.md`

Keep the original `reason` and `evidence` lines unchanged.

- [ ] **Step 2: Split `concept_links.md` into four files**

Move every edge from `ontology/relations/concept_links.md` into exactly one of:
- `ontology/relations/uses_concept.md`
- `ontology/relations/depends_on.md`
- `ontology/relations/supports.md`
- `ontology/relations/applies_to.md`

Examples that must land in the right targets:
- `[[PathMind]] --uses_concept--> [[路径优先化]]` → `uses_concept.md`
- `[[路径优先化]] --supports--> [[知识图谱推理问答]]` → `supports.md`
- `[[PathMind]] --applies_to--> [[知识图谱推理问答]]` → `applies_to.md`

- [ ] **Step 3: Rename one-to-one ledgers by migrating their full edge payloads**

Move the complete edge sets:
- `citation_graph.md` → `cites.md`
- `task_method_map.md` → `targets_task.md`
- `benchmark_links.md` → `evaluated_on.md`
- `evidence_index.md` → `supported_by.md`
- `paper_method_links.md` → `proposes.md`
- `provenance_links.md` → `sourced_from.md`

Preserve every canonical triple, `reason`, `evidence`, `status`, and `note` line.

- [ ] **Step 4: Leave the old files as temporary migration shells, not formal ledgers**

Replace the body of each old ledger file with a temporary one-line migration notice such as:

```md
> 本页已退出正式关系真源体系；对应实例边已迁移到同名 relation type ledger 文件。
```

Do not leave canonical edge bodies in the old files.

- [ ] **Step 5: Verify there are no canonical triples left in old clustered ledgers**

Run:

```bash
grep -R -n -- "--[a-z_][a-z_]*-->" ontology/relations/citation_graph.md ontology/relations/method_evolution.md ontology/relations/task_method_map.md ontology/relations/concept_links.md ontology/relations/paper_method_links.md ontology/relations/benchmark_links.md ontology/relations/evidence_index.md ontology/relations/provenance_links.md
```

Expected:
- No matches
- Old files contain only migration-shell prose

---

### Task 4: Update runtime skills to route by relation type

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md` (if old ledger names appear)
- Modify: `.claude/skills/serving-governance-review/SKILL.md` (if old ledger names appear)

- [ ] **Step 1: Rewrite the explicit ledger target list in `paper-ingest`**

In `.claude/skills/paper-ingest/SKILL.md`, replace the old ledger list under Step 5 with this exact list:

```md
   - `ontology/relations/cites.md`
   - `ontology/relations/proposes.md`
   - `ontology/relations/based_on.md`
   - `ontology/relations/improves_on.md`
   - `ontology/relations/targets_task.md`
   - `ontology/relations/uses_concept.md`
   - `ontology/relations/depends_on.md`
   - `ontology/relations/supports.md`
   - `ontology/relations/applies_to.md`
   - `ontology/relations/evaluated_on.md`
   - `ontology/relations/supported_by.md`
   - `ontology/relations/sourced_from.md`
```

- [ ] **Step 2: Rewrite `relation-reconciliation` ledger routing to one-file-per-relation-type**

Replace the current `## Ledger routing` block in `.claude/skills/relation-reconciliation/SKILL.md` with:

```md
## Ledger routing
- `cites` → `ontology/relations/cites.md`
- `proposes` → `ontology/relations/proposes.md`
- `based_on` → `ontology/relations/based_on.md`
- `improves_on` → `ontology/relations/improves_on.md`
- `targets_task` → `ontology/relations/targets_task.md`
- `uses_concept` → `ontology/relations/uses_concept.md`
- `depends_on` → `ontology/relations/depends_on.md`
- `supports` → `ontology/relations/supports.md`
- `applies_to` → `ontology/relations/applies_to.md`
- `evaluated_on` → `ontology/relations/evaluated_on.md`
- `supported_by` → `ontology/relations/supported_by.md`
- `sourced_from` → `ontology/relations/sourced_from.md`
```

Also update the output example so `added_relations.file` points at a new relation-type file, for example `ontology/relations/targets_task.md`.

- [ ] **Step 3: Rewrite any old ledger file references in `page-projection-sync` and other skills**

Search and replace old relation ledger file names in:
- `.claude/skills/page-projection-sync/SKILL.md`
- `.claude/skills/index-sync/SKILL.md`
- `.claude/skills/serving-governance-review/SKILL.md`

Use the direct same-name replacements:
- `citation_graph.md` → `cites.md`
- `method_evolution.md` → `based_on.md` / `improves_on.md` as appropriate in prose
- `task_method_map.md` → `targets_task.md`
- `concept_links.md` → `uses_concept.md` / `depends_on.md` / `supports.md` / `applies_to.md` as appropriate in prose
- `paper_method_links.md` → `proposes.md`
- `benchmark_links.md` → `evaluated_on.md`
- `evidence_index.md` → `supported_by.md`
- `provenance_links.md` → `sourced_from.md`

- [ ] **Step 4: Verify no runtime skill still references retired clustered ledgers**

Run:

```bash
! grep -R -n "citation_graph\.md\|method_evolution\.md\|task_method_map\.md\|concept_links\.md\|paper_method_links\.md\|benchmark_links\.md\|evidence_index\.md\|provenance_links\.md" .claude/skills --exclude-dir=.git
```

Expected:
- No matches
- Shell exits successfully

---

### Task 5: Update object pages, evidence pages, and CLAUDE relation entries to the new file names

**Files:**
- Modify: `CLAUDE.md`
- Modify: `ontology/entities/**`
- Modify: `intermediate/papers/**`

- [ ] **Step 1: Update `CLAUDE.md` formal relation entry section and mapping to the new files**

Ensure `CLAUDE.md` uses the exact new file names listed in Task 1 Step 4 and contains no old clustered ledger names.

- [ ] **Step 2: Rewrite direct object/evidence links to old relation-ledger filenames**

Search all runtime knowledge files and replace direct links:

```bash
grep -R -n "citation_graph\|method_evolution\|task_method_map\|concept_links\|paper_method_links\|benchmark_links\|evidence_index\|provenance_links" ontology/entities intermediate/papers
```

For each match, replace the old ledger name with the new relation-type file that matches the actual relation semantics at that location.

- [ ] **Step 3: Verify runtime knowledge pages no longer link to retired clustered ledgers**

Run:

```bash
! grep -R -n "citation_graph\|method_evolution\|task_method_map\|concept_links\|paper_method_links\|benchmark_links\|evidence_index\|provenance_links" ontology/entities intermediate/papers CLAUDE.md
```

Expected:
- No matches
- Shell exits successfully

---

### Task 6: Rewrite lint_graph.py for the new relation-type ledger architecture

**Files:**
- Modify: `scripts/lint_graph.py`

- [ ] **Step 1: Replace all old relation-ledger file-name constants and required-file checks**

Update `scripts/lint_graph.py` so every old relation-ledger file name in:
- `REQUIRED_FILES`
- `GRAPH_STANDARD_NEEDLES`
- `RELATION_LEDGER_NEEDLES`
- `SERVING_READY_SAMPLES`
- any direct string comparisons

is replaced with the new relation-type file names.

- [ ] **Step 2: Update method projection and concept-network assumptions in lint rules**

Adjust any logic that assumes:
- method evolution is stored in one file
- concept network lives in one file

so it now accepts:
- `based_on.md` and `improves_on.md` as the method-evolution truth sources
- `uses_concept.md`, `depends_on.md`, `supports.md`, and `applies_to.md` as the split concept-network truth sources

Add this test method:

```python
    def test_lint_graph_requires_new_relation_type_ledgers(self):
        expected = [
            'ontology/relations/cites.md',
            'ontology/relations/proposes.md',
            'ontology/relations/based_on.md',
            'ontology/relations/improves_on.md',
            'ontology/relations/targets_task.md',
            'ontology/relations/uses_concept.md',
            'ontology/relations/depends_on.md',
            'ontology/relations/supports.md',
            'ontology/relations/applies_to.md',
            'ontology/relations/evaluated_on.md',
            'ontology/relations/supported_by.md',
            'ontology/relations/sourced_from.md',
        ]

        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        for needle in expected:
            self.assertIn(needle, text)
```

- [ ] **Step 4: Run the focused unittest file and verify green**

Run:

```bash
```

Expected:
- PASS

---

### Task 7: Remove retired clustered ledgers and run full verification

**Files:**
- Delete: `ontology/relations/citation_graph.md`
- Delete: `ontology/relations/method_evolution.md`
- Delete: `ontology/relations/task_method_map.md`
- Delete: `ontology/relations/concept_links.md`
- Delete: `ontology/relations/paper_method_links.md`
- Delete: `ontology/relations/benchmark_links.md`
- Delete: `ontology/relations/evidence_index.md`
- Delete: `ontology/relations/provenance_links.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Delete the retired clustered ledger files**

Run:

```bash
rm ontology/relations/citation_graph.md ontology/relations/method_evolution.md ontology/relations/task_method_map.md ontology/relations/concept_links.md ontology/relations/paper_method_links.md ontology/relations/benchmark_links.md ontology/relations/evidence_index.md ontology/relations/provenance_links.md
```

Expected:
- The eight retired clustered ledger files are removed from the working tree

- [ ] **Step 2: Verify no runtime file still references the retired ledger names**

Run:

```bash
! grep -R -n "citation_graph\.md\|method_evolution\.md\|task_method_map\.md\|concept_links\.md\|paper_method_links\.md\|benchmark_links\.md\|evidence_index\.md\|provenance_links\.md" CLAUDE.md ontology scripts .claude/skills --exclude-dir=.git
```

Expected:
- No matches
- Shell exits successfully

- [ ] **Step 3: Run full graph lint after the ledger migration**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- PASS
- If it fails, every failure must be fixed before claiming the redesign is complete

- [ ] **Step 4: Inspect the final change surface**

Run:

```bash
git diff --stat
git status --short
```

Expected:
- The diff covers only the files implicated by the relation-ledger architecture redesign
- Working tree status matches the intended set of created, modified, and deleted files

---

## Self-review checklist

- Spec coverage:
  - one-file-per-relation-type normative definition: Task 1
  - new ledger files created: Task 2
  - formal truth migrated from old ledgers: Task 3
  - skills updated to route by relation type: Task 4
  - object/evidence references updated: Task 5
  - lint and regression coverage updated: Task 6
  - retired clustered ledgers deleted and full verification run: Task 7
- Placeholder scan:
  - No `TODO`, `TBD`, or vague migration steps remain
  - Every task has exact files, exact commands, or exact replacement content
- Consistency check:
  - Every relation type in the spec maps to exactly one file in the plan
  - Old clustered ledgers are treated only as temporary shells before deletion
  - Runtime contracts, page projection, and lint all converge on the same new file names
