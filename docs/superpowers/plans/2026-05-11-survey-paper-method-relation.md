# Survey-to-Method Relation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `surveys_method` formal relation so survey papers can formally cover methods without overloading `proposes` or collapsing into plain `cites`.

**Architecture:** Extend the phase-1 method graph with one new relation family only: `Paper -> Method` for structured survey coverage. Update the ontology contract first, then add a dedicated ledger, then align survey-paper serving guidance and candidate-generation/reconciliation/review skills so they can generate and govern `surveys_method` with a higher evidence threshold than ordinary mention or citation.

**Tech Stack:** Obsidian Markdown knowledge base, relation ledgers under `ontology/relations/`, managed object pages under `ontology/entities/`, Claude Code skills under `.claude/skills/`, Python lint entrypoint `scripts/lint_graph.py`

---

## File structure

### Ontology truth source
- Modify: `ontology/graph-standard.md`
  - Add `surveys_method` to the formal relation list.
  - Define legal source/target types and evidence threshold.
  - Update survey-paper serving guidance so survey Paper pages can formally cover methods without polluting `proposes`.
- Create: `ontology/relations/surveys_method.md`
  - New canonical ledger file for `Paper -> Method` survey coverage.

### Workflow and governance guidance
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Teach candidate generation for `surveys_method` when a survey structurally covers methods.
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
  - Add survey-method coverage checks and distinguish them from `proposes` and `cites`.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Add routing and review rules for `surveys_method`.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Add survey-paper projection guidance for outgoing `surveys_method`.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Add survey-method relation review focus.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
  - Add legality and distinction rules for `surveys_method` vs `proposes` / `cites`.
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Add diff-review checks for incorrect survey-method relation placement.
- Modify: `scripts/lint_graph.py`
  - Add `ontology/relations/surveys_method.md` to required files and ledger scans.

### Verification
- Run: `python3 scripts/lint_graph.py`
- Run: targeted `rg` checks over ontology and skills for `surveys_method`
- Run: targeted `rg` checks to ensure `proposes` was not broadened and `surveys_method` is distinct from `cites`

---

### Task 1: Add the new ontology contract and ledger

**Files:**
- Modify: `ontology/graph-standard.md`
- Create: `ontology/relations/surveys_method.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing contract check**

Run:
```bash
rg -n 'surveys_method|Formal relations.*proposes.*cites|systematic survey coverage' ontology/graph-standard.md ontology/relations
```
Expected: FAIL to find `surveys_method`, proving the new relation does not exist yet.

- [ ] **Step 2: Add `surveys_method` to `ontology/graph-standard.md`**

Insert this relation definition into section `2.3 关系类型`, after `proposes` and before `targets_task`:
```markdown
- `surveys_method`：`[[Paper]] --surveys_method--> [[Method]]`；表示综述论文、landscape 论文、taxonomy 论文或其他 survey-role 论文将某方法纳入其系统梳理、分类、比较或 coverage 范围。该关系只允许 `Paper` 作为 source、`Method` 作为 target；它不表示方法被首次提出，也不等同于普通论文引用事实。
```
Also add this constraint sentence nearby:
```markdown
- `surveys_method` 只在论文对方法形成结构化综述覆盖时成立；仅有背景提及、普通 related work 引用或零散 mention，不足以生成该 formal relation。
```

- [ ] **Step 3: Update survey-paper guidance in `ontology/graph-standard.md`**

Replace the survey Paper supplement block so it reads:
```markdown
survey / framework-taxonomy 论文的 Paper 页投影补充规则：
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架、相关任务、应用场景、关键结论、综述证据来源。
- 这类 Paper 的 `Formal relations` 重点为：`proposes`、`surveys_method`、`cites`。
- 与任务、场景相关的论文级信息优先保留在人类区块、frontmatter 与 Evidence 支撑中；若需要 formal relation，应由对应 Method 层的 `targets_task`、`applied_in` 承接。
- 若无统一 benchmark，必须显式以 `relation_exemptions` 说明 `evaluated_on` 按规范豁免，而不是伪造 benchmark formal edge。
```

- [ ] **Step 4: Create `ontology/relations/surveys_method.md`**

Create the file with this exact content:
```markdown
## 关系语义说明
- `surveys_method` 表示综述论文、landscape 论文、taxonomy 论文或其他 survey-role 论文将某方法纳入其系统梳理、分类、比较或 coverage 范围。
- 合法 source：`Paper`。
- 合法 target：`Method`。
- 该关系不表示方法被首次提出；若论文首次提出或正式定义该方法，应使用 `proposes`。
- 该关系也不等同于普通 `cites`；仅有引用事实、背景 mention 或零散 related-work 提及，不足以生成 `surveys_method`。
- 证据应优先来自 `analysis.md` 或 survey-oriented `sections.md` 中的结构化 coverage 内容，而不是默认从 `refs.md` 升格。

## 实例边
- 暂无
```

- [ ] **Step 5: Run lint to verify the new ledger is structurally valid**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

### Task 2: Align survey-paper candidate generation and reconciliation

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Test: `rg -n "surveys_method|proposes|cites" .claude/skills/paper-ingest .claude/skills/relation-reconciliation`

- [ ] **Step 1: Write the failing workflow grep check**

Run:
```bash
rg -n 'surveys_method|Paper -> Method|ordinary citation|analysis.md' .claude/skills/paper-ingest .claude/skills/relation-reconciliation
```
Expected: FAIL to find `surveys_method` guidance before implementation.

- [ ] **Step 2: Update `.claude/skills/paper-ingest/SKILL.md` relation output list**

Add `surveys_method` to the required relation-type list:
```markdown
- `proposes`
- `surveys_method`
- `targets_task`
- `evaluated_on`
- `applied_in`
- `supported_by`
- `cites`
- `based_on`
- `references_method`
- `sourced_from`
```
And add it to the structured output template:
```yaml
relation_candidates:
  proposes: []
  surveys_method: []
  targets_task: []
  evaluated_on: []
  applied_in: []
  supported_by: []
  cites: []
  based_on: []
  references_method: []
  sourced_from: []
```

- [ ] **Step 3: Add candidate-generation rules to `.claude/skills/paper-ingest/SKILL.md`**

Insert this exact block under `### 关系文件` after the `proposes` rules:
```markdown
- `surveys_method`：
  - 只在综述论文、landscape 论文、taxonomy 论文或其他 survey-role 论文对方法形成结构化 coverage 时生成 `[[Paper]] --surveys_method--> [[Method]]`
  - 强证据包括：方法出现在综述表格、方法分类、coverage 列表、比较章节或系统梳理结构中
  - 普通背景提及、单纯引用事实或 related work 顺带一提，不生成 `surveys_method`
  - 证据优先来自 `analysis.md` 或 survey-oriented `sections.md`，不默认从 `refs.md` 升格
```

- [ ] **Step 4: Update `.claude/skills/paper-ingest/evals/quality-checklist.md`**

Add these checklist items under `## Relation autowrite checks`:
```markdown
- [ ] 如果论文是 survey / landscape / taxonomy 角色，并且系统梳理了既有方法，则输出与落库结果必须包含 `surveys_method`，而不是只保留 `cites`。
- [ ] `surveys_method` 不得替代 `proposes`；只有首次提出或正式定义的方法才使用 `proposes`。
- [ ] 普通相关工作提及或单条引用事实，不得被误升格为 `surveys_method`。
```

- [ ] **Step 5: Update `.claude/skills/relation-reconciliation/SKILL.md` routing and review logic**

Add routing:
```markdown
- `surveys_method` → `ontology/relations/surveys_method.md`
```
And under the strong-semantic review or routing guidance, add:
```markdown
- survey 论文中的方法 coverage 若属于系统梳理、分类、比较或 landscape 结构，应优先判断是否补为 `surveys_method`，而不是停留在 `cites`。
- `surveys_method` 不得用于首次提出方法；若论文对方法的关系是“首次提出/正式定义”，应落为 `proposes`。
```

- [ ] **Step 6: Run the workflow grep verification**

Run:
```bash
rg -n 'surveys_method|proposes|ordinary citation|analysis.md|coverage' .claude/skills/paper-ingest .claude/skills/relation-reconciliation
```
Expected: PASS with explicit `surveys_method` guidance and separation from `proposes` / `cites`.

### Task 3: Align projection and semantic-review guidance

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Test: `rg -n "surveys_method|proposes|cites" .claude/skills/page-projection-sync .claude/skills/ontology-semantic-review`

- [ ] **Step 1: Write the failing review/projection grep check**

Run:
```bash
rg -n 'surveys_method|survey coverage|proposes.*cites' .claude/skills/page-projection-sync .claude/skills/ontology-semantic-review
```
Expected: FAIL to find `surveys_method` before implementation.

- [ ] **Step 2: Update `.claude/skills/page-projection-sync/SKILL.md`**

Replace the survey-paper bullet with:
```markdown
- survey 论文页：优先同步 `proposes`、`surveys_method`、`cites`，并保留任务、场景的人类区块与豁免信息；不得把 survey-paper 对既有方法的 coverage 误投影为 `proposes`。
```

- [ ] **Step 3: Update `.claude/skills/ontology-semantic-review/SKILL.md` review focus**

Add this bullet under `## 审查重点`:
```markdown
- `surveys_method` 是否被正确用于综述论文对方法的系统覆盖，而不是误用 `proposes` 或退化为普通 `cites`
```
And add `ontology/relations/surveys_method.md` to the preread list.

- [ ] **Step 4: Update `review-scope-rules.md` and `diff-review-playbook.md`**

Add these rules to `review-scope-rules.md`:
```markdown
- `surveys_method` 只允许 `Paper -> Method`，且 source 应承担综述/landscape/taxonomy 的 survey-role。
- 如果论文只是引用某方法来源论文，而没有形成结构化 coverage，不应生成 `surveys_method`。
- 如果论文首次提出或正式定义某方法，应使用 `proposes`，而不是 `surveys_method`。
```
Add these checks to `diff-review-playbook.md`:
```markdown
- 如果 survey 论文对方法的系统梳理只落在 `cites` 而未形成 formal coverage，必须指出，并评估是否应补为 `surveys_method`。
- 如果 `surveys_method` 被错误用于非综述论文，必须指出。
- 如果 `surveys_method` 实际表达的是首次提出方法，必须指出，并迁回 `proposes`。
```

- [ ] **Step 5: Run the projection/review verification grep**

Run:
```bash
rg -n 'surveys_method|systematic coverage|误投影为 `proposes`|只允许 `Paper -> Method`' .claude/skills/page-projection-sync .claude/skills/ontology-semantic-review
```
Expected: PASS with survey-method-specific projection and semantic-review rules.

### Task 4: Update lint coverage for the new relation family

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing lint-script check**

Run:
```bash
rg -n 'surveys_method' scripts/lint_graph.py
```
Expected: FAIL to find any lint awareness of the new relation.

- [ ] **Step 2: Add `surveys_method` to required relation files and scans**

Update `scripts/lint_graph.py` so these blocks include the new ledger:
```python
REQUIRED_FILES = [
    'ontology/graph-standard.md',
    'ontology/log.md',
    'ontology/entities/benchmarks/index.md',
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/surveys_method.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
    'scripts/lint_graph.py',
]
```
```python
RELATION_LEDGER_FILES = [
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/surveys_method.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/applied_in.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
]
```

- [ ] **Step 3: Run lint to verify the new relation integrates cleanly**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

### Task 5: Final scope and contract verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Re-run full lint**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

- [ ] **Step 2: Verify the new relation exists and stays in its lane**

Run:
```bash
rg -n 'surveys_method|proposes|cites' ontology/graph-standard.md ontology/relations/surveys_method.md .claude/skills/paper-ingest .claude/skills/relation-reconciliation .claude/skills/page-projection-sync .claude/skills/ontology-semantic-review scripts/lint_graph.py
```
Expected: PASS with hits for `surveys_method`, plus explicit wording that distinguishes it from `proposes` and `cites`.

- [ ] **Step 3: Inspect diff scope**

Run:
```bash
git diff --name-only
```
Expected: only the planned ontology contract, new ledger, skill guidance, and lint-script files are included.

## Spec coverage self-check
- Add `surveys_method` as `Paper -> Method` → covered by Tasks 1, 2, 3, 4, 5.
- Keep it distinct from `proposes` / `cites` / `references_method` → covered by Tasks 1, 2, 3, 5.
- Use stronger evidence threshold than mention or citation → covered by Tasks 1, 2, 3.
- Do not add survey-specific relations for tasks/scenarios/benchmarks → enforced by scope and verification.

## Placeholder scan
- No `TODO`, `TBD`, or vague implementation placeholders remain.
- All code/text changes are explicit.
- Verification commands are concrete and fresh.

## Type consistency check
- `surveys_method` is consistently `Paper -> Method`.
- `proposes` remains `Paper -> Method` for actual method introduction only.
- `cites` remains paper-to-paper citation only.
- No survey-specific task/scenario/benchmark relations are introduced anywhere in the plan.
