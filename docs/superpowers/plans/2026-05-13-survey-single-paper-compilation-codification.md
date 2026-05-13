# Survey Single-Paper Compilation Codification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Codify survey-paper single-paper compilation so the default ResearchKB pipeline can automatically reach the repaired LLM-KG-CPD-style outcome when a survey has stable structured method coverage.

**Architecture:** First update the normative ontology contract in `ontology/graph-standard.md`, then align each pipeline stage to a three-tier survey coverage model: Tier A direct admission, Tier B reconciliation-only, Tier C review-only. Finally, extend lint and governance expectations so survey-derived `surveys_method`, partial Methods, representative paper stubs, and `cites` form one validated end-to-end path.

**Tech Stack:** Obsidian Markdown ontology/spec/skill files, Python lint script, ResearchKB relation ledgers, Claude Code pipeline skills

---

## File map

### Modify
- `ontology/graph-standard.md` — add survey coverage thresholds, survey-derived Method admission contract, representative paper stub / `cites` provenance rules, and minimum link clarifications
- `.claude/skills/paper-ingest/SKILL.md` — add Tier A/B/C survey coverage detection and output contracts
- `.claude/skills/relation-reconciliation/SKILL.md` — add survey-derived `surveys_method` / paper stub / `cites` reconciliation rules and outputs
- `.claude/skills/page-projection-sync/SKILL.md` — add projection requirements for representative paper stubs, Evidence incoming `supported_by`, and Method `## 代表论文`
- `.claude/skills/index-sync/SKILL.md` — add default routing for survey-derived partial Methods and non-serving representative paper stubs
- `.claude/skills/ontology-semantic-review/SKILL.md` — add three valid survey states and survey-derived provenance review expectations
- `.claude/skills/serving-governance-review/SKILL.md` — add survey-derived serving path expectations
- `scripts/lint_graph.py` — validate survey-derived Method admission, representative paper anchors, paper stubs, `cites`, and Evidence incoming projection closure
- `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md` — one-off regression checklist for this implementation

### Reuse for verification
- `docs/superpowers/specs/2026-05-13-survey-single-paper-compilation-codification-design.md`
- `ontology/relations/surveys_method.md`
- `ontology/relations/cites.md`
- `ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `ontology/entities/methods/BEAR.md`
- `ontology/entities/evidence/LLM-KG-CPD.refs.md`

---

### Task 1: Update the normative ontology contract in `graph-standard.md`

**Files:**
- Modify: `ontology/graph-standard.md`
- Create: `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md`
- Test: `ontology/graph-standard.md`

- [ ] **Step 1: Write the failing checklist expectations**

```markdown
# Survey pipeline codification smoke check

## Expected missing graph-standard rules before implementation
- survey coverage tiering rule
- survey-derived partial Method representative paper rule
- survey-derived paper stub and cites provenance rule
- survey-derived minimum link clarification
```

- [ ] **Step 2: Verify those rules are absent or incomplete**

Run:
```bash
grep -n "Tier A\|Tier B\|Tier C\|representative paper stub\|wide detection\|survey-derived partial Method" ontology/graph-standard.md || true
```
Expected: no hits for the new rule phrases

- [ ] **Step 3: Add `surveys_method` threshold clarification near relation semantics**

Insert this exact block after the existing `surveys_method` rules in `ontology/graph-standard.md`:

```markdown
- survey 论文不天然产生 `surveys_method`；只有当论文对方法形成结构化 coverage 时，才允许默认直接生成该 formal relation。
- 结构化 coverage 的典型证据包括：方法分组表、taxonomy / grouping section、comparison matrix、coverage list、role-based method table。
- 当 survey 论文只提供 related-work 背景、趋势总结、高体量 citation list 或零散方法 mention 时，不得直接默认生成 `surveys_method` formal relation。
- 当前单篇 survey 编译默认采用三档 coverage 判定：Tier A（direct admission）、Tier B（reconciliation review required）、Tier C（needs-human-review only）。宽松检测不等于宽松落账。
```

- [ ] **Step 4: Add survey-derived Method admission and representative paper rules in Method contract area**

Insert this exact block near the Method contract and paper-anchor rules:

```markdown
- 对于通过 `surveys_method` 稳定覆盖并 materialize 的 `Method`，允许以 `status: partial` 进入正式图谱。
- 这类 survey-derived partial `Method` 必须同时具备：formal survey paper anchor（例如 incoming `surveys_method`）、人类可读 `## 代表论文` 锚点，以及最小 `Formal relations` 合同。
- 若 representative paper 身份稳定可识别，则应优先为其生成 `Paper Stub / Anchor` 作为 future ingest 升级落点；该 stub 不自动升级为 Formal Paper。
- survey-derived partial `Method` 的“1 篇代表论文”最小链接义务，可先由 `## 代表论文` prose anchor 加 representative paper stub / anchor 共同满足，而不要求立即生成 Formal Paper。
```

- [ ] **Step 5: Add representative paper stub and `cites` provenance rule in Paper/Paper Stub area**

Insert this exact block in the Paper layering area:

```markdown
- 当 survey-derived partial `Method` 具备稳定 representative paper 时，可默认生成对应 `Paper Stub / Anchor`，并允许 source survey paper 同步生成指向该 stub 的 `cites`。
- 该 `cites` 用于补齐 survey-derived method admission 的 paper-level provenance 闭环，不表示该 representative paper 已升级为 Formal Paper。
- representative paper stub 默认只进入 papers index 的 non-serving block，不得自动提升为默认 paper serving 入口。
```

- [ ] **Step 6: Verify the new graph-standard rules are present**

Run:
```bash
grep -n "Tier A（direct admission）\|representative paper stub\|宽松检测不等于宽松落账\|survey-derived partial `Method`" ontology/graph-standard.md
```
Expected: hits for all inserted rule phrases

- [ ] **Step 7: Commit**

```bash
git add docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md ontology/graph-standard.md
git commit -m "spec: codify survey-derived method admission rules"
```

### Task 2: Extend `paper-ingest` to output Tier A/B/C survey coverage results

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `.claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Write the failing contract expectations into the checklist**

Append this to `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md`:

```markdown
## Expected paper-ingest additions
- Tier A / Tier B / Tier C survey coverage outputs
- representative_paper_candidates
- paper_stub_candidates
- cites candidates for Tier A
- stale-prose replacement guidance for survey refs caches
```

- [ ] **Step 2: Verify the current skill lacks the new output terms**

Run:
```bash
grep -n "Tier A\|Tier B\|Tier C\|representative_paper_candidates\|paper_stub_candidates\|宽松检测不等于宽松落账" .claude/skills/paper-ingest/SKILL.md || true
```
Expected: no hits

- [ ] **Step 3: Add survey coverage tiering and output contract**

Insert this exact block into the survey-handling area of `.claude/skills/paper-ingest/SKILL.md`:

```markdown
### survey coverage tiering
对于 survey / landscape / taxonomy / framework 论文，必须主动检测 method coverage，并将候选对象分为三档：
- Tier A（direct survey-covered method candidates）：稳定方法名 + 结构化 coverage + 可写最小 `object_semantics` + representative paper 稳定可识别；默认直接进入 formal admission 链。
- Tier B（high-confidence survey method candidates）：方法身份较稳定，但结构化 coverage 或 representative paper 仍略弱；默认输出为高置信候选并强制交给 `relation-reconciliation` 复核，不在 ingest 阶段直接落 formal ledger。
- Tier C（needs-human-review survey candidates）：仅有 related-work mention、对象身份不稳、或更像系统/场景/benchmark/概念；只进入 review 输出，不自动 materialize。

宽松检测不等于宽松落账：survey 论文应积极发现方法候选，但只有 Tier A 默认自动落入 `surveys_method`。
```

- [ ] **Step 4: Extend the final output schema for Tier A metadata**

Insert this exact block into the output contract of `.claude/skills/paper-ingest/SKILL.md` near `relation_candidates` / candidate metadata:

```markdown
对于 Tier A survey-covered methods，除 `surveys_method` / `supported_by` / `cites` relation candidates 外，还必须额外输出：
- `representative_paper_candidates`
- `paper_stub_candidates`
- `survey_method_tier: TierA`

对于 Tier B survey candidates，必须输出：
- `survey_method_tier: TierB`
- `high_confidence_survey_method_candidates`
- 可选 `representative_paper_candidates`

对于 Tier C survey candidates，必须输出：
- `survey_method_tier: TierC`
- `needs-human-review survey candidates`
```

- [ ] **Step 5: Add stale-prose replacement rule for refs/analysis caches**

Insert this exact block near survey cache guidance:

```markdown
当 survey 论文已经对 Tier A 方法完成 direct admission 时，相关 Evidence 缓存不得继续保留“当前 ingest 不把高体量 survey 引文批量升格为 `surveys_method`”这类 blanket prose。必须改写为：
- 哪些方法已被当前批次直接 materialize
- 哪些候选仍处于 Tier B / Tier C
- 为什么剩余候选被延后
```

- [ ] **Step 6: Verify the new ingest contract text is present**

Run:
```bash
grep -n "Tier A（direct survey-covered method candidates）\|representative_paper_candidates\|paper_stub_candidates\|宽松检测不等于宽松落账" .claude/skills/paper-ingest/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/paper-ingest/SKILL.md docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md
git commit -m "feat: tier survey coverage in paper-ingest"
```

### Task 3: Extend `relation-reconciliation` for survey-derived methods, stubs, and cites

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Test: `.claude/skills/relation-reconciliation/SKILL.md`

- [ ] **Step 1: Write the failing reconciliation expectations into the checklist**

Append this to `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md`:

```markdown
## Expected relation-reconciliation additions
- Tier A survey candidates must not pass with empty surveys_method
- materialized_paper_stubs output
- deferred_survey_candidates output
- survey-derived cites closure requirement
```

- [ ] **Step 2: Verify the current skill lacks the new phrases**

Run:
```bash
grep -n "materialized_paper_stubs\|deferred_survey_candidates\|Tier A survey candidates\|survey-derived cites" .claude/skills/relation-reconciliation/SKILL.md || true
```
Expected: no hits

- [ ] **Step 3: Add Tier A/Tier B survey reconciliation rules**

Insert this exact block in the survey coverage review area:

```markdown
- 若 survey 论文在 ingest 输出中已声明 Tier A survey-covered method candidates，则 `relation-reconciliation` 不得接受“空的 `surveys_method` ledger”直接过关。
- 对于 Tier A candidates，必须默认补齐：`surveys_method`、必要的 `supported_by`、representative paper stub / anchor，以及与 representative paper 对应的 `cites`。
- 对于 Tier B candidates，必须显式判定 `add_now` 或 `needs-human-review`；不得因 ingest 未直接 formalize 而静默跳过。
- 对于 Tier C candidates，允许停留在 review 输出，不自动 materialize。
```

- [ ] **Step 4: Extend the output contract with stub/deferred fields**

Insert this exact block into the structured output section:

```markdown
新增输出字段：
- `materialized_paper_stubs`: []
- `deferred_survey_candidates`: []

当 Tier A survey-derived partial Methods 已 materialize 时：
- `affected_pages` 必须包含 source survey Paper、new partial Method pages、supporting Evidence pages、以及 newly created representative paper stub pages。
```

- [ ] **Step 5: Add survey-derived `cites` closure rule**

Insert this exact block in the ledger routing / provenance rules section:

```markdown
- 当 survey-derived partial `Method` 默认生成 representative paper stub / anchor 时，source survey Paper 应同步生成指向该 representative paper 的 `cites`。
- 若 Tier A survey-derived `Method` 已落为 formal partial Method，但 representative paper stub 已生成且 `cites` 缺失，则该 provenance 闭环不完整，至少应进入 `needs-human-review`。
```

- [ ] **Step 6: Verify the new reconciliation contract is present**

Run:
```bash
grep -n "materialized_paper_stubs\|deferred_survey_candidates\|Tier A survey-covered method candidates\|representative paper stub / anchor" .claude/skills/relation-reconciliation/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/relation-reconciliation/SKILL.md docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md
git commit -m "feat: reconcile survey-derived methods and paper stubs"
```

### Task 4: Extend projection and index sync contracts for survey-derived outputs

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/index-sync/SKILL.md`
- Test: `.claude/skills/page-projection-sync/SKILL.md`
- Test: `.claude/skills/index-sync/SKILL.md`

- [ ] **Step 1: Write the failing projection/index expectations into the checklist**

Append this to `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md`:

```markdown
## Expected projection and index additions
- representative paper stub projection rule
- Evidence incoming supported_by projection requirement
- Method `## 代表论文` projection rule
- papers index non-serving routing for representative paper stubs
```

- [ ] **Step 2: Verify the current skill files lack the new phrases**

Run:
```bash
grep -n "representative paper stub\|Method `## 代表论文`\|Evidence incoming `supported_by`\|papers index non-serving" .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md || true
```
Expected: no hits

- [ ] **Step 3: Add page-projection-sync rules**

Insert this exact block into `.claude/skills/page-projection-sync/SKILL.md`:

```markdown
- 对于 survey-derived Tier A admissions，`page-projection-sync` 必须同步 source survey Paper、new partial Method pages、supporting Evidence pages，以及 representative paper stub / anchor pages。
- 当 survey-derived `supported_by` ledger 已存在时，Evidence 页 incoming projection 也是默认合同的一部分；不得只同步 Method outgoing 而遗漏 Evidence incoming。
- 当 survey-derived partial `Method` 已拥有稳定 representative paper anchor 时，应同步或保留 `## 代表论文` 人类区块，而不是仅依赖 formal relation ledger。
- representative paper stub 若承接 formal relation，应继续作为 non-serving `Paper Stub / Anchor` 投影，不得自动提升为 Formal Paper 页面模板。
```

- [ ] **Step 4: Add index-sync routing rules**

Insert this exact block into `.claude/skills/index-sync/SKILL.md`:

```markdown
- survey-derived `status: partial` Method 默认进入 Methods index 的默认导航入口。
- survey-derived representative paper stubs 默认进入 Papers index 的 non-serving block。
- 仅因其承担 survey-derived method provenance 而创建的 paper stub，不得自动提升为 papers index 默认入口。
```

- [ ] **Step 5: Verify the new projection/index rules are present**

Run:
```bash
grep -n "representative paper stub / anchor\|Evidence 页 incoming projection\|`## 代表论文`\|non-serving block" .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md
git commit -m "feat: project survey-derived methods and paper stubs"
```

### Task 5: Extend lint and governance expectations

**Files:**
- Modify: `scripts/lint_graph.py`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Test: `scripts/lint_graph.py`
- Test: `.claude/skills/ontology-semantic-review/SKILL.md`
- Test: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Write the failing lint/governance expectations into the checklist**

Append this to `docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md`:

```markdown
## Expected lint and governance additions
- survey-derived representative paper anchor validation
- survey-derived cites closure validation
- ontology-semantic-review survey state triage
- serving-governance-review survey-derived serving path rule
```

- [ ] **Step 2: Verify the current files lack the new phrases**

Run:
```bash
grep -n "representative paper anchor\|survey-derived cites\|three valid survey states\|survey-derived serving path" scripts/lint_graph.py .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/serving-governance-review/SKILL.md || true
```
Expected: no hits

- [ ] **Step 3: Extend `scripts/lint_graph.py` with representative paper and cites checks**

Insert this exact Python helper near the survey/lint validation helpers:

```python
def check_survey_method_representative_anchors(errors: list[str]) -> None:
    for method_path in sorted((ROOT / 'ontology/entities/methods').glob('*.md')):
        rel_path = str(method_path.relative_to(ROOT))
        text = method_path.read_text(encoding='utf-8', errors='ignore')
        if '`surveys_method`' not in text:
            continue
        if '## 代表论文' not in text:
            errors.append(f'survey-derived partial Method missing representative paper section: {rel_path}')
```
```

And add this exact call near the existing validation calls:

```python
check_survey_method_representative_anchors(errors)
```

- [ ] **Step 4: Add semantic-review survey-state triage rules**

Insert this exact block into `.claude/skills/ontology-semantic-review/SKILL.md`:

```markdown
- 必须区分三种合法 survey 状态：
  1. 无结构化 method coverage，因此不要求 `surveys_method`
  2. 存在 Tier A 结构化 coverage，因此应存在 `surveys_method`
  3. 仅有 Tier B / Tier C 候选，因此允许停留在 reconciliation / review 路径
- 若某 survey 已明显存在 Tier A 结构化 coverage，却没有 `surveys_method`，必须指出。
- 若某 survey-derived partial `Method` 已 materialize，却缺少 representative paper provenance，也必须指出。
```

- [ ] **Step 5: Add serving-governance survey-derived path rules**

Insert this exact block into `.claude/skills/serving-governance-review/SKILL.md`:

```markdown
- 必须识别 survey-derived serving path：source survey Paper → partial Method → Evidence，以及 source survey Paper → representative paper stub / anchor。
- 若该链路的 formal/evidence 遍历完整、paper stub 状态暴露正确且未被误升为默认入口，则应判为合法 serving path，而不是自动降级。
- 若 survey-derived partial `Method` 已被 default expose，但缺少 representative paper human-readable anchor 或关键 Evidence next-hop，则应至少判为 `needs_fixes`。
```

- [ ] **Step 6: Verify the new lint and governance text is present**

Run:
```bash
grep -n "survey-derived partial Method missing representative paper section\|三种合法 survey 状态\|survey-derived serving path" scripts/lint_graph.py .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/serving-governance-review/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 7: Run end-to-end smoke verification on the codified contract**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: `PASS: graph lint succeeded`

Run:
```bash
grep -n "Tier A（direct survey-covered method candidates）\|materialized_paper_stubs\|representative paper stub / anchor\|三种合法 survey 状态\|survey-derived serving path" ontology/graph-standard.md .claude/skills/paper-ingest/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/index-sync/SKILL.md .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/serving-governance-review/SKILL.md
```
Expected: hits across all seven pipeline components plus `graph-standard.md`

- [ ] **Step 8: Commit**

```bash
git add scripts/lint_graph.py \
  .claude/skills/ontology-semantic-review/SKILL.md \
  .claude/skills/serving-governance-review/SKILL.md \
  docs/superpowers/checks/2026-05-13-survey-pipeline-codification-smoke.md
git commit -m "feat: validate survey-derived single-paper compilation"
```
