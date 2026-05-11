# Remove Concept from Phase-1 Ontology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `Concept` and `uses_concept` from the phase-1 ResearchKB ontology so the live system behaves as a pure method graph.

**Architecture:** Apply the contraction in four layers: ontology truth source, live entity/ledger surfaces, ingest-and-governance skills, then verification and serving cleanup. The implementation removes the Concept domain entirely, rewrites all surviving pages to keep concept-like terminology in prose only, and updates every phase-1 workflow assumption so no tool emits or expects `Concept` or `uses_concept`.

**Tech Stack:** Obsidian Markdown knowledge base, relation ledgers under `ontology/relations/`, managed object pages under `ontology/entities/`, Claude Code skills under `.claude/skills/`, Python lint entrypoint `scripts/lint_graph.py`

---

## File structure

### Ontology truth source
- Modify: `ontology/graph-standard.md`
  - Remove `Concept` from node types.
  - Remove `uses_concept` from relation types.
  - Rewrite framework / taxonomy handling for phase 1.
  - Remove Concept-specific object-page contract and any Concept mentions from serving/minimum-link rules.
- Modify: `ontology/relations/proposes.md`
  - Narrow target legality from `Method|Concept` to `Method` only.
- Modify: `ontology/relations/supported_by.md`
  - Remove `Concept` from legal source list.
- Delete: `ontology/relations/uses_concept.md`

### Entity domains and live pages
- Delete: `ontology/entities/concepts/index.md`
- Delete: `ontology/entities/concepts/路径优先化.md`
- Delete: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/methods/PathMind.md`
  - Remove Concept wikilinks and `uses_concept` projections; preserve mechanism wording in prose.
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
  - Remove concept-domain dependencies and keep mechanism language as prose.
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
  - Remove concept-domain wikilinks and phrase related-mechanism mentions as prose.
- Modify: `ontology/entities/scenarios/企业知识图谱问答.md`
  - Remove concept-domain references.
- Modify: `ontology/entities/evidence/PathMind.sections.md`
- Modify: `ontology/entities/evidence/PathMind.refs.md`
- Modify: `ontology/entities/evidence/PathMind.experiments.md`
  - Remove concept-page links and concept-supported_by projections; keep terminology only as evidence prose if needed.
- Modify: `ontology/entities/methods/index.md`
  - Ensure method entry semantics do not rely on concept-domain links.

### Workflow and governance skills
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Remove Concept page creation, `uses_concept`, and `Paper -> Concept` expectations.
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
  - Remove Concept / `uses_concept` requirements.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Remove `uses_concept` routing and Concept assumptions.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Remove Concept-specific projection rules and serving-domain expectations.
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Remove `uses_concept` / Concept prereads and review rules.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
  - Remove Concept classification and relation checks; tighten Method/Task/Scenario/Benchmark rules.
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Remove `uses_concept` checks and Concept-specific review prompts.
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
  - Remove Concept from serving-layer page-type assumptions.

### Verification
- Run: `python3 scripts/lint_graph.py`
- Run: targeted `rg` commands proving there is no surviving `entities/concepts`, `uses_concept`, or live phase-1 Concept assumption in ontology or skills.

---

### Task 1: Remove Concept and uses_concept from the ontology contract

**Files:**
- Modify: `ontology/graph-standard.md`
- Modify: `ontology/relations/proposes.md`
- Modify: `ontology/relations/supported_by.md`
- Delete: `ontology/relations/uses_concept.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing contract checks**

Run:
```bash
rg -n 'Concept|uses_concept|\[\[Paper\]\] --proposes--> \[\[Method\|Concept\]\]|Method\|Concept\|Task\|Scenario\|Benchmark' ontology/graph-standard.md ontology/relations/proposes.md ontology/relations/supported_by.md ontology/relations/uses_concept.md
```
Expected: PASS showing current Concept and `uses_concept` references that must be removed.

- [ ] **Step 2: Rewrite the ontology node and relation definitions in `ontology/graph-standard.md`**

Edit the file so section `2.1 节点类型` becomes:
```markdown
### 2.1 节点类型
- Paper：论文实例节点
- Method：方法节点
- Task：研究任务节点
- Scenario：应用场景节点
- Benchmark：数据集或评测基准节点
- Evidence：`ontology/entities/evidence/` 下的结构化证据对象页
- RawSource：`ontology/entities/raw-sources/files/` 下的受管原始来源文件集合，由 `ontology/entities/raw-sources/index.md` 提供导航；主要用于 provenance 追踪与最终回查，不承担主图谱组织职责
```
Rewrite section `2.2 survey / framework 建模公理` to:
```markdown
### 2.2 survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task，也不在 phase 1 单独抽象为独立概念层对象。
- Framework / taxonomy 若主要承担可执行方法流程、明确实验对比或方法演化语义，则应按 Method 处理。
- Framework / taxonomy 若主要承担知识组织、分类、分层或解释框架语义，但不构成可复用方法，则 phase 1 保留在 Paper、Method 或 Evidence prose 中，不单独实体化。
- 当论文的核心贡献是可复用技术流程或方法框架时，应登记 `[[Paper]] --proposes--> [[Method]]`。
```
Rewrite section `2.3 关系类型` to remove `uses_concept` and make `proposes` Method-only:
```markdown
- `proposes`：`[[Paper]] --proposes--> [[Method]]`；表示论文首次提出或正式定义某方法或可执行方法框架。Survey 保持为 Paper 层节点；phase 1 不再为 framework / taxonomy / terminology 单独生成 Concept 实体。
- `targets_task`：`[[Method]] --targets_task--> [[Task]]`；表示方法主要面向的研究任务。若论文描述了任务定位，应通过 Method 层 formal relation 承接；Paper 页中的任务信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- `applied_in`：`[[Method]] --applied_in--> [[Scenario]]`；表示方法被明确应用、部署、验证或定位在某个应用场景中。该关系只允许 Method 作为 source、Scenario 作为 target；Paper 页中的场景信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Scenario` formal edge。
- `based_on`：`[[Method]] --based_on--> [[Method]]`
- `references_method`：`[[Method]] --references_method--> [[Method]]`
- `evaluated_on`：`[[Method]] --evaluated_on--> [[Benchmark]]`
- `supported_by`：`[[Method|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`
- `cites`：`[[Paper]] --cites--> [[Paper]]`
- `sourced_from`：`[[Evidence]] --sourced_from--> [[RawSource]]`
```
Also rewrite the final consolidation sentence so there is no mention of concept semantics:
```markdown
- Formal relation 只保留对 ingest 稳定、治理边界清晰、且对检索 / 问答有明显增益的关系类型；应用场景语义若已稳定到方法层，可通过 `applied_in` 表达；尚不足以形成正式方法-场景边时，仍可下沉到 frontmatter `scenario`、对象页正文与索引导航表达；改进强度与前提依赖等语义默认继续下沉到 `edge_semantics` 与对象页正文。
```

- [ ] **Step 3: Remove the entire Concept object-page contract from `ontology/graph-standard.md`**

Delete the full `### 3.5 Concept` section and renumber or shift the remaining sections so `Task` follows `Method` directly. While editing, also replace these affected lines:
```markdown
- Method 页状态分层规则
- `status: processed` 的 Method 页必须满足完整 serving 合同：`## 证据来源`、`## Formal relations`、`### Outgoing`、`### Incoming`。
```
```markdown
- survey / framework-taxonomy 论文的 Paper 页投影补充规则：
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架、相关任务、应用场景、关键结论、综述证据来源。
- 与任务、场景相关的论文级信息优先保留在人类区块、frontmatter 与 Evidence 支撑中；若需要 formal relation，应由对应 Method 层的 `targets_task`、`applied_in` 承接。
```
```markdown
- 场景页主要由 framework / survey 节点供给时，人类区块应优先突出：使用的主要方法、相关任务、相关论文、证据来源。
```
Remove Concept mentions from minimum-link and serving requirements, for example:
```markdown
- Method 页通常至少链接：1 篇代表论文、1 个父方法或上游方法、1 个子方法或对比方法、1 个任务或场景；若上下游节点尚未正式落库，可先保留明确占位说明。
- Task / Benchmark 页至少链接：2 个论文或方法节点、1 个场景；若当前只有单条主线，可先围绕主线节点建立最小可视网络。
```
And in serving rules:
```markdown
- Paper、Method、Task、Scenario、Benchmark、Evidence 页必须同时包含：frontmatter、面向人类的关系区块、`## Formal relations` 规范化关系区块。
```

- [ ] **Step 4: Rewrite relation-ledger legality files and delete `uses_concept.md`**

Change `ontology/relations/proposes.md` top section to:
```markdown
## 关系语义说明
- `proposes` 表示论文首次提出或正式定义某方法或可执行方法框架。
- 合法 source：`Paper`。
- 合法 target：`Method`。
- phase 1 不再为 framework / taxonomy / terminology 单独生成 Concept 实体；若论文只提供组织性解释而不形成可复用方法，应保留在 prose / Evidence 中。
```
Change `ontology/relations/supported_by.md` top section to:
```markdown
## 关系语义说明
- `supported_by` 表示正式知识对象页由 Evidence 对象页支撑。
- 合法 source：`Method`、`Task`、`Scenario`、`Benchmark`。
- 合法 target：`Evidence`。
- `Paper` 不再作为 `supported_by` 的 source；Evidence 与 Paper 之间也不单独建立 formal relation。
```
Then delete the file:
```bash
rm "ontology/relations/uses_concept.md"
```

- [ ] **Step 5: Run lint and contract grep verification**

Run:
```bash
python3 scripts/lint_graph.py && rg -n 'Concept|uses_concept' ontology/graph-standard.md ontology/relations
```
Expected: lint PASS; no `uses_concept` file content remains; any remaining `Concept` hits indicate missed contract cleanup and must be fixed before moving on.

### Task 2: Remove the Concept entity domain and repair live pages

**Files:**
- Delete: `ontology/entities/concepts/index.md`
- Delete: `ontology/entities/concepts/路径优先化.md`
- Delete: `ontology/entities/concepts/重要推理路径.md`
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Modify: `ontology/entities/tasks/knowledge-graph-reasoning.md`
- Modify: `ontology/entities/tasks/kgqa.md`
- Modify: `ontology/entities/tasks/multi-hop-qa.md`
- Modify: `ontology/entities/scenarios/企业知识图谱问答.md`
- Modify: `ontology/entities/evidence/PathMind.sections.md`
- Modify: `ontology/entities/evidence/PathMind.refs.md`
- Modify: `ontology/entities/evidence/PathMind.experiments.md`
- Modify: `ontology/entities/methods/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing entity-domain check**

Run:
```bash
rg -n 'concepts/|uses_concept|路径优先化|重要推理路径' ontology/entities/methods/PathMind.md ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md ontology/entities/tasks/*.md ontology/entities/scenarios/企业知识图谱问答.md ontology/entities/evidence/PathMind.*.md ontology/entities/concepts/index.md ontology/entities/concepts/*.md
```
Expected: PASS with many hits showing the live dependency on the Concept domain.

- [ ] **Step 2: Delete the Concept domain files**

Run:
```bash
rm "ontology/entities/concepts/index.md" "ontology/entities/concepts/路径优先化.md" "ontology/entities/concepts/重要推理路径.md"
```
Expected: shell exits successfully.

- [ ] **Step 3: Rewrite `ontology/entities/methods/PathMind.md` without Concept links or `uses_concept`**

Make these exact content changes:
```markdown
## 技术原理
- 方法由子图检索、路径优先排序和知识推理三部分组成。
- 它通过路径优先排序识别高价值推理路径，再用这些路径引导 LLM 完成回答。
```
```markdown
## 相关机制
- 路径优先排序
- 高价值推理路径筛选
```
Replace the old `## 相关概念` section with `## 相关机制`.
In `## Formal relations`, delete both `uses_concept` entries entirely so the outgoing relation set contains only:
- `based_on`
- `references_method`
- `targets_task`
- `applied_in`
- `evaluated_on`
- `supported_by`
No `uses_concept` entries may remain.
```

- [ ] **Step 4: Rewrite the PathMind paper page to prose-only mechanism language**

In `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`, replace:
```markdown
- 论文提出 [[../methods/PathMind]] 方法，并显式使用路径优先化与重要推理路径两个核心概念。
```
with:
```markdown
- 论文提出 [[../methods/PathMind]] 方法，并以路径优先排序和高价值推理路径筛选作为核心机制。
```
Replace:
```markdown
- 该论文为 [[../methods/PathMind]] 提供提出关系与方法语义真源，并为路径优先化、重要推理路径与知识图谱推理任务提供证据支撑。
```
with:
```markdown
- 该论文为 [[../methods/PathMind]] 提供提出关系与方法语义真源，并为知识图谱推理任务与企业知识图谱问答场景中的关键机制提供证据支撑。
```
Do not introduce any Concept wikilinks.

- [ ] **Step 5: Rewrite Task and Scenario pages to remove Concept links**

Apply these exact replacements:
In `ontology/entities/tasks/knowledge-graph-reasoning.md` replace
```markdown
## 相关概念
- 路径优先化
- 重要推理路径
```
with:
```markdown
## 相关机制
- 路径优先排序
- 高价值推理路径筛选
```
In `ontology/entities/tasks/kgqa.md` replace
```markdown
## 相关概念
- 重要推理路径
```
with:
```markdown
## 相关机制
- 高价值推理路径筛选
```
In `ontology/entities/tasks/multi-hop-qa.md` replace
```markdown
## 相关概念
- 重要推理路径
```
with:
```markdown
## 相关机制
- 高价值推理路径筛选
```
In `ontology/entities/scenarios/企业知识图谱问答.md` replace
```markdown
## 使用的主要方法 / 概念
- [[../methods/PathMind]]
- 路径优先化
- 重要推理路径
```
with:
```markdown
## 使用的主要方法 / 机制
- [[../methods/PathMind]]
- 路径优先排序
- 高价值推理路径筛选
```

- [ ] **Step 6: Rewrite evidence pages to remove Concept-supported_by projections**

In `ontology/entities/evidence/PathMind.sections.md`, remove any `supported_by` projection entries that target deleted concept pages. Also replace the explanatory prose:
```markdown
- 该证据页主要支撑 PathMind 方法、PathMind 论文、路径优先化、重要推理路径，以及知识图谱推理相关任务与场景页的最小正式语义。
```
with:
```markdown
- 该证据页主要支撑 PathMind 方法、PathMind 论文，以及知识图谱推理相关任务与场景页的最小正式语义，并保留关键机制说明。
```
Keep mechanism wording like “路径优先化” only as prose if needed, but remove all concept-page wikilinks and all `supported_by` edges for deleted Concept nodes. Re-read `PathMind.refs.md` and `PathMind.experiments.md`; if they contain concept-page wikilinks, replace them with plain text mechanism wording.

- [ ] **Step 7: Run lint and domain-removal grep verification**

Run:
```bash
python3 scripts/lint_graph.py && rg -n 'concepts/|uses_concept' ontology/entities ontology/relations
```
Expected: lint PASS and no remaining live ontology references to `concepts/` or `uses_concept`.

### Task 3: Remove Concept assumptions from phase-1 skills

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Modify: `.claude/skills/serving-governance-review/SKILL.md`
- Test: `rg -n "Concept|uses_concept|concepts/" .claude/skills`

- [ ] **Step 1: Write the failing workflow grep check**

Run:
```bash
rg -n 'Concept|uses_concept|concepts/' .claude/skills/paper-ingest .claude/skills/relation-reconciliation .claude/skills/page-projection-sync .claude/skills/ontology-semantic-review .claude/skills/serving-governance-review
```
Expected: PASS showing many remaining phase-1 Concept assumptions.

- [ ] **Step 2: Rewrite `paper-ingest` to remove Concept and uses_concept**

Make these exact edits in `.claude/skills/paper-ingest/SKILL.md`:
- Delete the line that says a concept page should be created under `ontology/entities/concepts/`.
- Remove `ontology/relations/uses_concept.md` from preread/reference lists.
- Change
```markdown
- `supported_by` 候选只允许从 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 指向 `Evidence`。
```
to
```markdown
- `supported_by` 候选只允许从 `Method`、`Task`、`Scenario`、`Benchmark` 指向 `Evidence`。
```
- Remove `uses_concept` from required relation-type output lists and templates.
- Replace framework/taxonomy rules with:
```markdown
- 若论文核心贡献是可复用方法框架，应登记 `[[Paper]] --proposes--> [[Method]]`。
- 若论文主要提供 taxonomy、术语组织或解释框架而不形成可复用方法，phase 1 保留在 Paper / Evidence prose 中，不单独实体化。
```

- [ ] **Step 3: Rewrite `paper-ingest/evals/quality-checklist.md`**

Replace any checklist items requiring `Paper -> Concept` or `uses_concept` with:
```markdown
- [ ] 如果论文核心贡献是可复用方法框架，输出与落库结果必须包含 `Paper -> Method` 的 `proposes` 关系。
- [ ] 若论文只提供 taxonomy、术语组织或解释框架而不形成可复用方法，不得在 phase 1 强行创建独立实体。
- [ ] `relation_candidates` 至少应覆盖：`proposes`、`targets_task`、`evaluated_on`、`applied_in`、`supported_by`、`cites`、`sourced_from`。
```

- [ ] **Step 4: Rewrite reconciliation, projection, review, and serving skills**

Apply these exact transformations:
- In `.claude/skills/relation-reconciliation/SKILL.md`
  - remove `uses_concept` routing
  - remove any mention of `Concept` as a supported_by source
  - remove any framework-Concept page assumptions
- In `.claude/skills/page-projection-sync/SKILL.md`
  - remove the `framework 型 Concept 页` bullet
  - remove any mention that phase 1 expands to the Concept domain
  - rewrite survey-paper guidance so it only references Paper / Method / Task / Scenario / Benchmark / Evidence
- In `.claude/skills/ontology-semantic-review/SKILL.md`
  - remove `ontology/relations/uses_concept.md` from preread
  - remove the bullet `uses_concept 是否被错误用于 Paper`
  - replace any review language involving Concept with Method/Task/Scenario legality checks
- In `review-scope-rules.md`
  - remove `Concept` from classification guidance
  - remove `uses_concept` legality rules
  - rewrite source-allowed list for `supported_by` without Concept
- In `diff-review-playbook.md`
  - remove `uses_concept.md` checks
  - replace with checks for invalid phase-1 attempts to recreate Concept entities or concept-domain pages
- In `.claude/skills/serving-governance-review/SKILL.md`
  - remove `Concept` from the list of serving-layer page types the skill expects to review

- [ ] **Step 5: Run the skill cleanup grep check**

Run:
```bash
rg -n 'Concept|uses_concept|concepts/' .claude/skills
```
Expected: only incidental non-ontology uses such as generic English words may remain; no phase-1 ontology skills should still instruct creation, routing, serving, or review of a Concept entity domain.

### Task 4: Final verification and scope check

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full ontology verification**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

- [ ] **Step 2: Prove the phase-1 ontology no longer contains the Concept domain**

Run:
```bash
find ontology/entities -maxdepth 1 -type d | sort && rg -n 'Concept|uses_concept|concepts/' ontology .claude/skills
```
Expected: no `ontology/entities/concepts` directory and no phase-1 ontology contract or workflow instruction that still depends on `Concept` / `uses_concept`.

- [ ] **Step 3: Inspect diff scope**

Run:
```bash
git diff --name-only
```
Expected: only the planned ontology contract files, relation ledgers, live pages, deleted concept domain files, and relevant skills are in scope.

## Spec coverage self-check
- Remove `Concept` as a phase-1 entity → covered by Tasks 1 and 2.
- Remove `uses_concept` as a formal relation → covered by Tasks 1 and 3.
- Update ontology contract, entity domains, relation ledgers, live pages, indexes, and relevant skills → covered by Tasks 1 through 3.
- Do not design or introduce any phase-2 concept layer → enforced by scope and by replacing Concept logic with prose-only handling instead of new entities.

## Placeholder scan
- No `TODO`, `TBD`, or vague placeholders remain.
- Every edit step contains exact target files and replacement text.
- Verification commands are explicit and fresh.

## Type consistency check
- Phase 1 entity set is consistently Paper / Method / Task / Scenario / Benchmark / Evidence / RawSource throughout the plan.
- `uses_concept` is removed everywhere in the plan.
- `proposes` is consistently rewritten as `Paper -> Method` only.
- Framework / taxonomy handling is consistently prose-only unless it forms a reusable Method.
