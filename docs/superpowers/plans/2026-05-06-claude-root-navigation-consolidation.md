# CLAUDE Root Navigation Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `CLAUDE.md` the only system-level ontology navigation entry, update the dependent skills and runtime docs to match, and remove `ontology/index.md` without leaving live workflow references behind.

**Architecture:** First rewire `CLAUDE.md` so system-level routing no longer depends on `ontology/index.md` and the normative role of `ontology/graph-standard.md` is narrowed to “唯一规范裁决依据”. Then update the two affected skills so their contracts no longer assume a root ontology index exists. Finally clean up the remaining runtime references, delete `ontology/index.md`, and run targeted grep plus graph lint to confirm the navigation contract is closed.

**Tech Stack:** Markdown docs, Claude skills under `.claude/skills/`, Obsidian-style wikilinks, `grep`, `git`, Python 3, `scripts/lint_graph.py`.

---

## File map

### System-level navigation policy
- Modify: `CLAUDE.md`
  - Add the layered ontology navigation model to `## 本体认知`
  - Replace the old `ontology/index.md`-first query flow
  - Update the `index-sync` pipeline wording so it no longer implies a root navigation page

### Skills whose contract currently depends on the root ontology index
- Modify: `.claude/skills/index-sync/SKILL.md`
  - Remove `ontology/index.md` from the skill description, automatic sync targets, managed-block scope, and sample output
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Change the review surface from “system root index + domain indexes” to “domain indexes + explicitly managed serving/navigation indexes”

### Remaining runtime references that must be cleaned before deletion
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Remove the stale claim that `paper-ingest` updates `ontology/index.md`
- Modify: `ontology/log.md`
  - Replace the root ontology index navigation pointer with a system-level navigation pointer that matches the new architecture
- Modify: `ontology/graph-standard.md`
  - Update the `## Index 导航投影层` section so it no longer names `ontology/index.md`
- Delete: `ontology/index.md`
  - Remove the obsolete root ontology index page after the contract migration is complete

### Verification surface
- Test: `grep` across `CLAUDE.md`, `.claude/skills/`, and `ontology/`
- Test: `python3 scripts/lint_graph.py`
- Test: `git diff --stat`
- Test: `git status --short`

---

### Task 1: Rewire `CLAUDE.md` as the only system-level navigation entry

**Files:**
- Modify: `CLAUDE.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Capture the current failing state in `CLAUDE.md`**

Run:

```bash
grep -n "ontology/index\.md\|index-sync 负责把对象页与关系页的稳定结构同步到导航 index" CLAUDE.md
```

Expected:
- One match in `## 查询与分析` for `读取 \`ontology/index.md\` 定位系统级导航入口`
- One match in the single-paper compile pipeline for the old `index-sync` wording

- [ ] **Step 2: Replace the minimal `## 本体认知` section with the layered navigation model**

Replace the current `## 本体认知` block with this exact content:

```md
## 本体认知
- 本体认知是全局认知的核心认知底座
- 系统级本体导航由 `CLAUDE.md` 负责，默认采用“先分层判定，再进入对象，再按需下钻”的方式。
- 规范层：`ontology/graph-standard.md`
  - 它是唯一规范裁决依据。
  - 凡涉及节点归类、关系合法性、frontmatter 受控字段、证据义务与豁免规则的描述，若与 `CLAUDE.md` 或其他导航 / 流程说明不一致，以它为准。
- 对象层：`ontology/entities/*/index.md` 与 serving-ready 对象页
  - 对象域 index 用于锁定正式实例。
  - 对象页是默认问答入口，并以 `Formal relations` 作为受约束拓扑扩展面。
- 关系层：`ontology/relations/*.md`
  - 用于 formal relation ledger、治理、修复、审计与 formal graph truth 核对。
  - 不作为通用知识问答默认起点。
- 证据层：`intermediate/papers/`
  - 用于机制、实验、引用、baseline、provenance 核验。
- 原始来源层：`raw/`
  - 仅在上述层次不足以支持判断时回查，不进入默认导航主链。
```

- [ ] **Step 3: Replace the query flow so it no longer starts from `ontology/index.md`**

Inside `### 查询与分析`, replace the current ordered list with this exact list:

```md
1. 先依据 `CLAUDE.md` 的本体分层导航判断当前问题应进入规范层、对象层、关系层、证据层还是原始来源层
2. 若为正式知识问答，进入对应对象域 `ontology/entities/<对象域>/index.md` 锁定候选正式实例
3. 读取对应 serving-ready 对象页，作为默认问答入口
4. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展
5. 如涉及机制、实验、引用、基线、统计分析或 provenance 核验，优先读取对应 Evidence 页与 `intermediate/papers/`
6. 如处于治理、修复、审计场景，或需核对 formal graph truth，再读取 `ontology/relations/*.md`
7. 只有在上述层都不足时，才回看 `raw/`
8. 回答时区分：正式知识结论 / 证据缓存结论 / 治理账本结论（仅在实际查询 relation ledger 时） / 待核验推断
```

- [ ] **Step 4: Tighten the compile-pipeline description of `index-sync`**

In the single-paper compile pipeline section, replace this bullet:

```md
- `index-sync` 负责把对象页与关系页的稳定结构同步到导航 index
```

with this exact bullet:

```md
- `index-sync` 负责把对象页投影同步到各对象域 index，并维护仍然存在的受管导航页
```

- [ ] **Step 5: Verify the new routing language is present and the old root-index language is gone**

Run:

```bash
grep -n "唯一规范裁决依据\|先依据 `CLAUDE.md` 的本体分层导航\|对象页投影同步到各对象域 index" CLAUDE.md && ! grep -n "读取 `ontology/index.md`" CLAUDE.md
```

Expected:
- Three positive matches for the new wording
- No match for `读取 \`ontology/index.md\``
- Shell exits successfully

- [ ] **Step 6: Commit the `CLAUDE.md` rewrite**

Run:

```bash
git add CLAUDE.md
git commit -m "docs: consolidate root navigation into claude"
```

Expected:
- A new commit containing only the `CLAUDE.md` navigation-policy rewrite

---

### Task 2: Update `index-sync` so it no longer assumes a root ontology index

**Files:**
- Modify: `.claude/skills/index-sync/SKILL.md`

- [ ] **Step 1: Capture the current root-index coupling in the skill**

Run:

```bash
grep -n "ontology/index\.md\|刷新系统入口\|Phase 1 先覆盖" .claude/skills/index-sync/SKILL.md
```

Expected:
- Matches in the frontmatter description
- A match in `## 自动同步内容`
- A match in `## 受管区块`
- A match in the sample output block

- [ ] **Step 2: Replace the frontmatter description with the new contract**

Replace the frontmatter block at the top of `.claude/skills/index-sync/SKILL.md` with this exact content:

```md
---
name: index-sync
description: 在 `page-projection-sync` 完成后，把对象页与 index 层之间的投影补齐到对象域导航与受管导航页：更新 `ontology/entities/*/index.md` 与其他显式受管导航页的受管区块，并输出 `synced_indexes`、`skipped_pages` 与 `manual_followups`。Whenever 对象页 formal projection 已完成且需要刷新对象域 index、关系域受管导航页、或判断哪些页面可被索引但暂不应 default serve 时，都应使用本 skill。
---
```

- [ ] **Step 3: Replace the sync-scope sections so `ontology/index.md` disappears from the skill body**

Use these exact replacements in `.claude/skills/index-sync/SKILL.md`:

Replace `## 自动同步内容` with:

```md
## 自动同步内容
1. `ontology/entities/*/index.md` 中的 `core-entry`、`grouped-navigation` 与 `canonical-list` 受管区块
2. relation-ledger 导航受管区块
3. 其他被显式声明为受管的域级 / 关系级导航页
```

Replace the `## 受管区块` section with:

```md
## 受管区块
- 只允许更新 `<!-- BEGIN MANAGED BLOCK:... -->` 与 `<!-- END MANAGED BLOCK:... -->` 之间的内容
- 不得重写区块外 prose
- Phase 1 先覆盖 `ontology/entities/*/index.md` 与其他显式受管导航页
```

Replace the sample under `## 结构化输出模板` with:

```md
## 结构化输出模板
```yaml
status: success | partial | needs-human-review
synced_indexes:
  - path: ontology/entities/papers/index.md
    updated_blocks:
      - core-entry
skipped_pages: []
manual_followups: []
```
```

- [ ] **Step 4: Verify the skill contract no longer names the root ontology index**

Run:

```bash
! grep -n "ontology/index\.md\|刷新系统入口" .claude/skills/index-sync/SKILL.md && grep -n "对象域导航与受管导航页\|其他被显式声明为受管的域级 / 关系级导航页\|ontology/entities/papers/index.md" .claude/skills/index-sync/SKILL.md
```

Expected:
- No matches for `ontology/index.md` or `刷新系统入口`
- Positive matches for the new object-domain/managed-navigation wording
- Shell exits successfully

- [ ] **Step 5: Commit the `index-sync` contract update**

Run:

```bash
git add .claude/skills/index-sync/SKILL.md
git commit -m "docs: narrow index sync navigation scope"
```

Expected:
- A new commit containing only the `index-sync` skill contract change

---

### Task 3: Update `serving-governance-review` to audit domain indexes instead of a root index

**Files:**
- Modify: `.claude/skills/serving-governance-review/SKILL.md`

- [ ] **Step 1: Capture the current root-index dependency in the serving review skill**

Run:

```bash
grep -n "ontology/index\.md\|index surfaces\|default navigation/QA entry surfaces" .claude/skills/serving-governance-review/SKILL.md
```

Expected:
- Matches in the intro sentence
- A match in `## Use this when`
- Matches inside `## What to check` item 4

- [ ] **Step 2: Replace the intro and `## Use this when` section with domain-index language**

Replace the opening paragraphs of `.claude/skills/serving-governance-review/SKILL.md` with this exact content:

```md
# Serving Governance Review

Review migrated knowledge pages and domain index pages to decide whether they are ready to serve as default constrained-QA entry surfaces and domain-level navigation/QA entry surfaces.

## Use this when
- A batch of Paper / Method / Concept / Task / Scenario / Benchmark / Evidence pages has been migrated to the serving-layer model.
- `ontology/entities/*/index.md` or other explicitly managed serving / navigation index pages changed and you need to decide whether those surfaces are safe as default navigation/QA entry surfaces.
- You need to decide whether pages or indexes are `serving-ready`, `partial`, or `legacy`.
- Structural lint and ontology semantic review have already been run or are available.
```

- [ ] **Step 3: Replace the `Index navigation quality` and `Release readiness` bullets with the narrowed scope**

In `.claude/skills/serving-governance-review/SKILL.md`, replace item 4 and item 5 under `## What to check` with this exact content:

```md
4. **Index navigation quality**
   - Do `ontology/entities/*/index.md` and any explicitly managed serving / navigation index pages expose the right default entry layer?
   - Are stub / placeholder / structurally incomplete pages incorrectly promoted as default entries?
   - Do index grouping and labels match actual page state?
   - Can a reader or LLM traverse from domain index → object page → Formal relations → adjacent object / Evidence pages without hidden fallback?
   - If a page is only indexed but not ready to be a default surface, is it distinguished rather than mixed into the default-serving layer?

5. **Release readiness**
   - Is this page or batch safe to promote as the default QA serving surface?
   - Are domain index pages or other explicitly managed navigation surfaces safe to promote as default navigation/QA entry surfaces?
```

- [ ] **Step 4: Verify the root-index wording is gone and the narrowed scope is present**

Run:

```bash
! grep -n "ontology/index\.md" .claude/skills/serving-governance-review/SKILL.md && grep -n "domain index pages\|explicitly managed serving / navigation index pages\|domain index → object page" .claude/skills/serving-governance-review/SKILL.md
```

Expected:
- No match for `ontology/index.md`
- Positive matches for the new domain-index wording
- Shell exits successfully

- [ ] **Step 5: Commit the serving-governance skill update**

Run:

```bash
git add .claude/skills/serving-governance-review/SKILL.md
git commit -m "docs: narrow serving governance index scope"
```

Expected:
- A new commit containing only the `serving-governance-review` contract change

---

### Task 4: Clean the remaining runtime references and delete `ontology/index.md`

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `ontology/log.md`
- Modify: `ontology/graph-standard.md`
- Delete: `ontology/index.md`

- [ ] **Step 1: Capture the remaining live references before cleanup**

Run:

```bash
grep -RIn "ontology/index\.md\|ontology/index" CLAUDE.md .claude/skills ontology --exclude-dir=.git
```

Expected:
- No matches in `CLAUDE.md`, `.claude/skills/index-sync/SKILL.md`, or `.claude/skills/serving-governance-review/SKILL.md` if Tasks 1–3 are complete
- Remaining matches in:
  - `.claude/skills/paper-ingest/SKILL.md`
  - `ontology/log.md`
  - `ontology/graph-standard.md`
  - `ontology/index.md`

- [ ] **Step 2: Remove the stale runtime references from the remaining files**

Apply these exact edits:

In `.claude/skills/paper-ingest/SKILL.md`, replace the frontmatter description with:

```md
---
name: paper-ingest
description: 完整摄入单篇学术论文并落库到 ResearchKB。Whenever the user says 处理论文、摄入论文、解析论文、落库论文、为某篇 paper 建缓存/摘要/方法页/关系页，或给出 PDF 路径希望完整提取并写入知识库时，都应使用此 skill，即使用户只明确提到其中一步。它会解析论文、生成全部 intermediate 缓存、按用户当前关注方向强化提取、更新 `ontology/log.md`，并产出供后续 `relation-reconciliation`、`page-projection-sync` 与 `index-sync` 消费的对象页候选与关系候选；在遇到异常结构论文时输出 `needs-skill-update` 告警。
---
```

In `ontology/log.md`, replace the two-line navigation header with:

```md
- 系统级导航：`CLAUDE.md`
- 图谱规范：[[graph-standard]]
```

In `ontology/graph-standard.md`, replace the `## Index 导航投影层` section with:

```md
## Index 导航投影层
- `CLAUDE.md` 负责系统级导航；`ontology/entities/*/index.md` 与其他显式受管导航页是导航投影层，不是 formal relation truth source。
- index 页中的受管区块由 `index-sync` 维护；区块外 prose 可保留人工导读与解释。
- 页面“可被 index 收录”和“可作为默认 serving 入口暴露”是两个不同状态。
- index 结构完整性由 `python3 scripts/lint_graph.py` 负责；index 的默认入口质量由 `serving-governance-review` 负责。
```

- [ ] **Step 3: Delete the obsolete root ontology index file**

Run:

```bash
rm ontology/index.md
```

Expected:
- `ontology/index.md` is removed from the working tree

- [ ] **Step 4: Verify there are no live runtime references to the deleted page**

Run:

```bash
! grep -RIn "ontology/index\.md\|ontology/index" CLAUDE.md .claude/skills ontology --exclude-dir=.git
```

Expected:
- No matches
- Shell exits successfully

- [ ] **Step 5: Commit the runtime cleanup and page removal**

Run:

```bash
git add .claude/skills/paper-ingest/SKILL.md ontology/log.md ontology/graph-standard.md ontology/index.md
git commit -m "docs: remove ontology root index"
```

Expected:
- A new commit containing the last runtime-reference cleanup plus the file deletion

---

### Task 5: Run final verification on the new navigation contract

**Files:**
- Verify: `CLAUDE.md`
- Verify: `.claude/skills/index-sync/SKILL.md`
- Verify: `.claude/skills/serving-governance-review/SKILL.md`
- Verify: `.claude/skills/paper-ingest/SKILL.md`
- Verify: `ontology/graph-standard.md`
- Verify: `ontology/log.md`
- Verify: `ontology/index.md` (deleted)
- Verify: `scripts/lint_graph.py`

- [ ] **Step 1: Re-run the scoped grep across runtime surfaces**

Run:

```bash
! grep -RIn "ontology/index\.md\|ontology/index\|刷新系统入口\|读取 `ontology/index.md`" CLAUDE.md .claude/skills ontology --exclude-dir=.git
```

Expected:
- No matches
- Shell exits successfully

- [ ] **Step 2: Run graph lint after the navigation-contract migration**

Run:

```bash
python3 scripts/lint_graph.py
```

Expected:
- PASS
- If it fails, the failure must be investigated before any further commit or merge work

- [ ] **Step 3: Inspect the change surface**

Run:

```bash
git diff --stat HEAD~4..HEAD
git status --short
```

Expected:
- `git diff --stat` shows only the intended documentation and skill files
- `git status --short` is empty if all four commits were created successfully

- [ ] **Step 4: Manually spot-check the new reading order in the edited files**

Run:

```bash
grep -n "唯一规范裁决依据\|先依据 `CLAUDE.md` 的本体分层导航\|对象域导航与受管导航页\|domain index pages\|系统级导航：`CLAUDE.md`" CLAUDE.md .claude/skills/index-sync/SKILL.md .claude/skills/serving-governance-review/SKILL.md ontology/log.md
```

Expected:
- `CLAUDE.md` exposes the new layered routing language
- `index-sync` exposes the object-domain/managed-navigation contract
- `serving-governance-review` exposes the narrowed domain-index review surface
- `ontology/log.md` points system-level navigation at `CLAUDE.md`

---

## Self-review checklist

- Spec coverage:
  - `CLAUDE.md` takes over system-level navigation: Task 1
  - `ontology/graph-standard.md` is reframed as normative authority, not system entry: Tasks 1 and 4
  - `index-sync` and `serving-governance-review` contracts are updated: Tasks 2 and 3
  - Remaining runtime references are cleaned and `ontology/index.md` is deleted: Task 4
  - Repo-level verification runs after deletion: Task 5
- Placeholder scan:
  - No `TODO`, `TBD`, or “similar to above” language remains
  - Every edit step includes exact replacement content or exact shell commands
- Consistency check:
  - All tasks use `CLAUDE.md` as the system-level navigation surface
  - All tasks use `ontology/entities/*/index.md` as the domain-index layer
  - All tasks treat `ontology/relations/*.md` as governance/truth surfaces rather than default entry pages
