# Paper/Method Human-Friendly Prose Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich the human-friendly prose on ResearchKB Paper and Method entity pages, with Paper pages first and Method pages second, without relocating graph truth away from Evidence pages and formal relation ledgers.

**Architecture:** First update the ontology contract and pipeline skill boundaries so Paper/Method human-friendly prose is a first-class object-page concern rather than ad hoc manual prose. Then extend `paper-ingest` to emit richer Paper/Method semantic payloads, extend `page-projection-sync` to project only the prose sections that are safe to auto-sync, and finally tighten lint plus a focused regression checklist so richer prose becomes part of the normal single-paper pipeline. Paper processed pages are upgraded first, then processed Method pages, while partial Method pages keep their lighter contract.

**Tech Stack:** Obsidian Markdown ontology pages, ResearchKB skill contracts in `.claude/skills/*/SKILL.md`, Python graph lint script, managed entity pages under `ontology/entities/*`, regression checklist under `docs/superpowers/checks/`

---

## File map

### Modify
- `ontology/graph-standard.md` — codify the richer Paper and Method human-friendly section contracts and clarify processed vs partial Method prose expectations
- `.claude/skills/paper-ingest/SKILL.md` — require richer Paper-first and Method-following human-facing semantic extraction payloads
- `.claude/skills/page-projection-sync/SKILL.md` — allow safe projection/synchronization of selected human-friendly prose sections, while preserving existing no-freeform boundaries
- `scripts/lint_graph.py` — require the new processed Paper/Method headings so richer prose is structurally enforced
- `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md` — one-off rollout checklist for this implementation

### Reuse for verification
- `docs/superpowers/specs/2026-05-13-paper-method-human-friendly-prose-design.md`
- `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- `ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md`
- `ontology/entities/methods/PathMind.md`
- `ontology/entities/methods/LLM-KG collaboration framework for advanced complex product design.md`
- `ontology/entities/methods/ASKG.md`
- `ontology/entities/evidence/PathMind.sections.md`
- `ontology/entities/evidence/LLM-KG-CPD.sections.md`

### Do not modify in this plan
- `ontology/entities/papers/*.md` and `ontology/entities/methods/*.md` content pages themselves — those should be refreshed later by the updated pipeline, not manually bulk-rewritten in this plan
- `.claude/skills/relation-reconciliation/SKILL.md` — relation truth remains its own concern
- `.claude/skills/index-sync/SKILL.md` — navigation logic should not become prose-authoring logic in this feature
- `.claude/skills/ontology-semantic-review/SKILL.md` and `.claude/skills/serving-governance-review/SKILL.md` — this plan relies on existing downstream review stages rather than redefining their contracts

---

### Task 1: Update the ontology contract for richer Paper/Method prose

**Files:**
- Modify: `ontology/graph-standard.md`
- Create: `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`
- Test: `ontology/graph-standard.md`

- [ ] **Step 1: Write the failing rollout checklist**

```markdown
# Paper/Method human-friendly prose smoke check

## Expected missing rules before implementation
- processed Paper human-friendly section contract
- processed Method human-friendly section contract
- partial Method remains lighter semantic-stub contract
- Paper-first / Method-following rollout note
```

- [ ] **Step 2: Verify the new rule phrases are absent or incomplete**

Run:
```bash
grep -n "Paper-first\|Method-following\|关键判断\|与知识库现有内容的关系\|当前抽取边界与不确定性\|当前知识状态" ontology/graph-standard.md || true
```
Expected: no hits for the exact new contract phrases

- [ ] **Step 3: Add the processed Paper human-friendly section contract**

Insert this exact block into the `### 3.3 Paper` section after the existing standard structure list:

```markdown
Paper 页的人类友好正文增强合同：
- processed `Paper` 页除 `Formal relations` 外，还应形成稳定的人类阅读入口。
- 这些区块的目标不是复述全文，而是帮助人快速判断：论文解决什么问题、主要贡献是什么、最值得记住什么、与知识库现有内容如何相连、当前抽取边界在哪里。
- 推荐以以下区块承载：`## 核心问题`、`## 主要贡献`、`## 关键结论`、`## 与知识库其他内容的关联`、`## 我的批注`。
- 当论文页属于 survey / framework / taxonomy 主线时，可保留 `## 核心方法`、`## 相关任务`、`## 应用场景`、`## 相关基准` 作为 Paper 级人类解释层，但不得把这些 prose 升格为新的 formal relation truth。
- 这些区块可以总结 Evidence 与 formal relation 的主语义面，但不得复制大段 Evidence cache，也不得绕过 `Formal relations` 暴露未受控对象邻接。
```

- [ ] **Step 4: Add the processed Method human-friendly section contract while preserving partial Method lightness**

Insert this exact block into the `### 3.4 Method` section after the existing standard structure list:

```markdown
Method 页的人类友好正文增强合同：
- `status: processed` 的 Method 页除最小 serving 合同外，还应形成稳定的方法身份解释层。
- 这些区块的目标是帮助人快速判断：该方法是什么、解决什么核心问题、核心机制是什么、与相邻方法如何区分、当前优势与局限是什么。
- 推荐以以下区块承载：`## 方法定义`、`## 解决的核心问题`、`## 技术原理`、`## 方法演化与参照关系`、`## 应用场景`、`## 代表论文`、`## 相关机制`、`## 优势与局限`、`## 与其他方法的对比`。
- `status: partial` 的 Method 页仍以 semantic-stub 合同为主，不要求立即具备完整 processed Method 正文；只有在后续证据成熟并升级为 processed 后，才强制满足完整方法解释层。
- Method 页的人类友好正文用于解释方法身份，不替代 `based_on`、`references_method`、`targets_task`、`applied_in`、`evaluated_on` 等 formal relation truth。
```

- [ ] **Step 5: Add a rollout note clarifying Paper-first, Method-following**

Insert this exact block near the end of the object-page contract section:

```markdown
Rollout 顺序说明：
- 若新的正文增强合同尚未一次性覆盖所有对象类型，应优先保证 Paper 页先满足 richer human-friendly prose 合同，再扩展到 processed Method 页。
- partial Method、Task、Scenario、Benchmark、Evidence 不因本轮 Paper-first rollout 而自动获得新的长篇解释性正文义务。
```

- [ ] **Step 6: Verify the new ontology contract text is present**

Run:
```bash
grep -n "Paper 页的人类友好正文增强合同\|Method 页的人类友好正文增强合同\|Paper-first\|Method-following\|partial Method 页仍以 semantic-stub 合同为主" ontology/graph-standard.md
```
Expected: hits for all inserted phrases

- [ ] **Step 7: Commit**

```bash
git add docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md ontology/graph-standard.md
git commit -m "spec: codify paper and method prose contracts"
```

### Task 2: Extend `paper-ingest` to emit richer Paper-first and Method-following prose payloads

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `.claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Record the failing ingest expectations in the checklist**

Append this to `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`:

```markdown
## Expected paper-ingest additions
- richer Paper-first object semantics payload
- Method identity/mechanism payload for processed Method candidates
- explicit uncertainty notes for Paper and Method prose
- projection-ready human-friendly section cues
```

- [ ] **Step 2: Verify the current skill lacks the new payload phrases**

Run:
```bash
grep -n "关键判断\|关系到知识库现有内容\|抽取边界\|方法身份\|核心机制 summary\|projection-ready" .claude/skills/paper-ingest/SKILL.md || true
```
Expected: no hits for the exact new payload contract terms

- [ ] **Step 3: Add the Paper-first human-facing extraction contract**

Insert this exact block into the object-level semantic requirements area of `.claude/skills/paper-ingest/SKILL.md` after the existing `object_semantics` bullets:

```markdown
对于 `Paper` 候选，除最小 `object_semantics` 外，还必须额外整理可投影到人类友好正文的语义载荷，至少覆盖：
- `core_problem_framing`
- `core_contribution_framing`
- `key_judgments`（3-5 条）
- `kb_relationship_framing`
- `extraction_boundary_notes`

这些字段的目标不是复述论文全文，而是为后续 Paper 页的人类阅读入口提供高密度判断材料。
```

- [ ] **Step 4: Add the Method-following human-facing extraction contract**

Insert this exact block nearby in the same section:

```markdown
对于 `Method` 候选，若当前论文已足以支撑 processed Method 级别的对象页，还必须额外整理可投影到方法解释层的语义载荷，至少覆盖：
- `method_identity_framing`
- `core_mechanism_summary`
- `task_scenario_positioning_notes`
- `neighbor_method_distinctions`
- `current_knowledge_state_notes`

若当前仅能支撑 `status: partial` 的 Method，则继续以 semantic-stub 最小语义骨架为主，不强制生成完整方法解释层。
```

- [ ] **Step 5: Add an explicit uncertainty-and-boundary rule for human-friendly prose payloads**

Insert this exact block into the prose/output boundary guidance:

```markdown
人类友好正文载荷的抽取边界：
- 必须显式暴露不确定性，不得把弱证据推断伪装成确定结论。
- 不得把 Evidence cache 大段复制为对象页 prose。
- 不得把这些载荷当作第二套 relation ledger；formal relation truth 仍由 relation candidates 与后续 ledger / projection 阶段承接。
- 当当前论文只足以支持 Paper 层解释，而不足以支持完整 Method 身份解释时，优先保证 Paper-first 输出完整，而不是勉强生成低质量 Method prose。
```

- [ ] **Step 6: Extend the final output summary schema with human-friendly payload buckets**

Insert this exact block into the final output format section near `relation_candidates` / `relation_exemptions`:

```markdown
新增对象页人类友好正文载荷输出：
- `paper_human_friendly_payloads`
- `method_human_friendly_payloads`

其中：
- `paper_human_friendly_payloads` 至少应包含 `core_problem_framing`、`core_contribution_framing`、`key_judgments`、`kb_relationship_framing`、`extraction_boundary_notes`
- `method_human_friendly_payloads` 至少应包含 `method_identity_framing`、`core_mechanism_summary`、`task_scenario_positioning_notes`、`neighbor_method_distinctions`、`current_knowledge_state_notes`
```

- [ ] **Step 7: Verify the new ingest contract is present**

Run:
```bash
grep -n "paper_human_friendly_payloads\|method_human_friendly_payloads\|core_problem_framing\|method_identity_framing\|Paper-first" .claude/skills/paper-ingest/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/paper-ingest/SKILL.md docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md
git commit -m "feat: enrich ingest prose payload contracts"
```

### Task 3: Extend `page-projection-sync` to project safe human-friendly prose sections

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Test: `.claude/skills/page-projection-sync/SKILL.md`

- [ ] **Step 1: Record the failing projection expectations in the checklist**

Append this to `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`:

```markdown
## Expected page-projection-sync additions
- safe syncing of selected Paper prose sections
- safe syncing of selected processed Method prose sections
- explicit prohibition on syncing partial Method long-form prose
- manual_followups when payload exists but projection should stay manual
```

- [ ] **Step 2: Verify the current skill still blocks these new sync phrases**

Run:
```bash
grep -n "核心问题\|主要贡献\|方法定义\|技术原理\|current_knowledge_state_notes\|partial Method long-form" .claude/skills/page-projection-sync/SKILL.md || true
```
Expected: no hits for the exact new sync contract phrases

- [ ] **Step 3: Replace the blanket no-sync boundary with a narrower authoring boundary**

In `.claude/skills/page-projection-sync/SKILL.md`, replace this exact block:

```markdown
## 不自动同步
- 方法解释性正文
- 核心问题分析
- 优势与局限
- 关键结论
- 批注与综述判断
```

with this exact block:

```markdown
## 不自动同步
- 自由发挥的长篇解释性正文
- 无 evidence / ingest payload 支撑的批注性判断
- “开放问题”“我的批注”这类明确属于人工研究笔记的区块
- 对 partial Method 的完整长篇方法解释层

## 可在严格载荷约束下同步
- processed Paper 页的：`## 核心问题`、`## 主要贡献`、`## 关键结论`、`## 与知识库其他内容的关联`
- processed Method 页的：`## 方法定义`、`## 解决的核心问题`、`## 技术原理`、`## 应用场景`、`## 相关机制`、`## 优势与局限`、`## 与其他方法的对比`

前提是：
- 这些内容来自 `paper-ingest` 明确产出的对象级人类友好正文载荷
- formal relation truth 已经完成 reconciliation
- 不会引入 formal adjacency 之外的新对象链接
```

- [ ] **Step 4: Add a projection rule for payload-to-section mapping**

Insert this exact block into the `正文摘要覆盖合同` area:

```markdown
对象页人类友好正文投影合同：
- 当 `paper-ingest` 已提供 `paper_human_friendly_payloads` 时，`page-projection-sync` 应优先把这些载荷同步到 processed Paper 页对应区块，而不是仅输出 `manual_followups`。
- 当 `paper-ingest` 已提供 `method_human_friendly_payloads`，且目标 Method 页已满足 processed Method 条件时，`page-projection-sync` 应把这些载荷同步到对应方法解释层区块。
- 若目标 Method 页仍为 `status: partial`，则不得强制投影完整方法解释层；此时应保留 semantic-stub 骨架，并按需输出 `manual_followups`。
- 若载荷存在但当前页面缺少安全投影前提（例如 formal relation 未对齐、页面状态仍 partial、或 prose 会造成越界对象邻接），则输出 `manual_followups`，而不是强行写入长篇 prose。
```

- [ ] **Step 5: Add a Paper-first rollout note to the rollout section**

Insert this exact block near the rollout guidance:

```markdown
Paper-first rollout 建议：
- 先在 processed Paper 页试跑 richer human-friendly prose 同步。
- 再扩展到 processed Method 页。
- partial Method 页在本轮默认继续保持轻量 semantic-stub 合同，不因 Paper-first rollout 被自动补成长篇解释性正文。
```

- [ ] **Step 6: Verify the new projection contract is present**

Run:
```bash
grep -n "可在严格载荷约束下同步\|paper_human_friendly_payloads\|method_human_friendly_payloads\|Paper-first rollout\|partial Method" .claude/skills/page-projection-sync/SKILL.md
```
Expected: hits for all inserted phrases

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/page-projection-sync/SKILL.md docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md
git commit -m "feat: sync safe paper and method prose sections"
```

### Task 4: Tighten `lint_graph.py` to require richer processed Paper/Method headings

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `scripts/lint_graph.py`

- [ ] **Step 1: Record the failing lint expectations in the checklist**

Append this to `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`:

```markdown
## Expected lint additions
- processed Paper pages require richer human-friendly headings
- processed Method pages require richer human-friendly headings
- partial Method pages keep lighter required headings
```

- [ ] **Step 2: Verify the current serving rules are still too thin**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
text = Path('scripts/lint_graph.py').read_text(encoding='utf-8')
print("paper_core_problem", '## 核心问题' in text)
print("paper_main_contribution", '## 主要贡献' in text)
print("method_definition", '## 方法定义' in text)
print("method_mechanism", '## 技术原理' in text)
PY
```
Expected:
```text
paper_core_problem False
paper_main_contribution False
method_definition False
method_mechanism False
```

- [ ] **Step 3: Expand processed Paper required headings**

In `scripts/lint_graph.py`, replace the current `paper` rule:

```python
    'paper': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {},
    },
```

with this exact block:

```python
    'paper': {
        'required_headings': [
            '## 核心问题',
            '## 主要贡献',
            '## 关键结论',
            '## 与知识库其他内容的关联',
            '## 证据来源',
            '## Formal relations',
            '### Outgoing',
            '### Incoming',
        ],
        'strong_frontmatter_fields': {},
    },
```

- [ ] **Step 4: Expand processed Method required headings while leaving partial Method alone**

In `scripts/lint_graph.py`, replace the current `method_processed` rule:

```python
    'method_processed': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
```

with this exact block:

```python
    'method_processed': {
        'required_headings': [
            '## 方法定义',
            '## 解决的核心问题',
            '## 技术原理',
            '## 方法演化与参照关系',
            '## 应用场景',
            '## 代表论文',
            '## 相关机制',
            '## 证据来源',
            '## Formal relations',
            '### Outgoing',
            '### Incoming',
            '## 优势与局限',
            '## 与其他方法的对比',
        ],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
```

- [ ] **Step 5: Run the focused lint-rule verification snippet**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
text = Path('scripts/lint_graph.py').read_text(encoding='utf-8')
checks = {
    'paper_core_problem': '## 核心问题' in text,
    'paper_main_contribution': '## 主要贡献' in text,
    'method_definition': '## 方法定义' in text,
    'method_mechanism': '## 技术原理' in text,
    'partial_still_stub': "'method_partial'" in text and '## 最小定义/角色' in text,
}
for key, value in checks.items():
    print(f"{key} {value}")
PY
```
Expected:
```text
paper_core_problem True
paper_main_contribution True
method_definition True
method_mechanism True
partial_still_stub True
```

- [ ] **Step 6: Run the full graph lint to catch unexpected regressions**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: pass, or only failures directly explained by content pages not yet refreshed by the upgraded pipeline

- [ ] **Step 7: Commit**

```bash
git add scripts/lint_graph.py docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md
git commit -m "feat: require richer paper and method headings"
```

### Task 5: Run a focused pipeline verification against representative Paper and Method pages

**Files:**
- Modify: `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`
- Test: `docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md`

- [ ] **Step 1: Append the final verification matrix to the checklist**

Append this exact block:

```markdown
## Final verification matrix
- PathMind paper still satisfies processed Paper contract
- LLM-KG-CPD survey paper still satisfies processed Paper contract
- PathMind method still satisfies processed Method contract
- survey-derived partial Method pages remain on semantic-stub contract only
- projection sync contract now allows safe Paper/processed-Method prose sync without turning prose into a second ledger
```

- [ ] **Step 2: Verify representative Paper pages still contain the required richer headings**

Run:
```bash
for f in \
  "ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" \
  "ontology/entities/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md"; do
  echo "CHECK $f"
  grep -n "## 核心问题\|## 主要贡献\|## 关键结论\|## 与知识库其他内容的关联\|## 证据来源\|## Formal relations" "$f"
done
```
Expected: both files print all six headings

- [ ] **Step 3: Verify a processed Method page and a partial Method page each satisfy the intended split contract**

Run:
```bash
echo "CHECK processed method"
grep -n "## 方法定义\|## 解决的核心问题\|## 技术原理\|## 方法演化与参照关系\|## 证据来源\|## 优势与局限\|## 与其他方法的对比" "ontology/entities/methods/PathMind.md"
echo "CHECK partial method"
grep -n "## Object semantics\|## 当前定位\|## 与知识库现有内容的关系\|## 最小定义/角色\|## 待补充\|## Formal relations" "ontology/entities/methods/ASKG.md"
```
Expected: `PathMind.md` prints all processed-method headings; `ASKG.md` prints only the semantic-stub headings plus `Formal relations`

- [ ] **Step 4: Re-run full graph lint and capture result in the checklist**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: pass, or only known content-refresh failures that must be addressed before rollout is considered complete

- [ ] **Step 5: Record verification outcome in the checklist**

Append this exact block after you run the checks, filling in the observed result:

```markdown
## Verification result
- `python3 scripts/lint_graph.py`: PASS
- representative processed Paper pages: PASS
- representative processed Method page: PASS
- representative partial Method page: PASS
```

If lint does not pass yet, replace the first line with the real failure summary instead of `PASS`.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/checks/2026-05-13-paper-method-human-friendly-prose-smoke.md
git commit -m "test: add paper and method prose rollout checks"
```

---

## Self-review

### Spec coverage
- Problem and goal are covered by Tasks 1–4: ontology contract, ingest payload contract, projection boundary, and lint enforcement.
- Paper-first / Method-following priority is covered by Task 1 rollout rules, Task 2 ingest boundary, and Task 3 projection rollout note.
- Paper-page richer prose sections are covered by Task 1 processed Paper contract, Task 2 Paper payload extraction, and Task 4 Paper lint headings.
- Method-page richer prose sections are covered by Task 1 processed Method contract, Task 2 Method payload extraction, and Task 4 Method lint headings.
- The boundary that Evidence and formal relations remain the truth layers is covered by Tasks 1–3.
- The requirement that partial Methods keep the lighter semantic-stub contract is covered by Tasks 1, 3, 4, and 5.
- The implementation-order requirement for `paper-ingest`, `page-projection-sync`, and validation is covered by the task order itself.

### Placeholder scan
- No `TODO`, `TBD`, or deferred placeholders remain.
- Every code-editing step includes exact text to insert or replace.
- Every verification step includes exact commands and expected outputs.
- All commit steps specify exact files and commit messages.

### Type consistency
- `paper_human_friendly_payloads` and `method_human_friendly_payloads` are introduced once in Task 2 and reused consistently in Task 3.
- Processed-vs-partial Method distinction is consistent across ontology contract, projection contract, lint rules, and verification.
- Paper headings use `## 核心问题`, `## 主要贡献`, `## 关键结论`, `## 与知识库其他内容的关联` consistently across tasks.
- Processed Method headings use `## 方法定义`, `## 解决的核心问题`, `## 技术原理`, `## 方法演化与参照关系`, `## 应用场景`, `## 代表论文`, `## 相关机制`, `## 优势与局限`, `## 与其他方法的对比` consistently across tasks.
