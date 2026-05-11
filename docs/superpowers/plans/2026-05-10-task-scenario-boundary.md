# Task/Scenario Boundary and Method-Only Relation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `Method -> Scenario` formal relation `applied_in`, narrow `uses_concept` and `targets_task` to Method-only sources, and update the live ontology plus skill prompts so future paper-processing follows the new contract.

**Architecture:** The change is centered on ontology truth sources first, then on the single known live example, then on workflow guidance. Update `ontology/graph-standard.md` and relation ledgers to redefine legal source/target types, project the new relation into the affected Method and Scenario surfaces, remove now-invalid paper-level formal edges, and then align the ingest/reconciliation/projection/review skills to the same contract.

**Tech Stack:** Obsidian Markdown knowledge base, relation ledgers under `ontology/relations/`, managed object pages under `ontology/entities/`, Claude Code skills under `.claude/skills/`, Python lint entrypoint `scripts/lint_graph.py`

---

## File structure

### Ontology truth sources
- Modify: `ontology/graph-standard.md`
  - Redefine `uses_concept` and `targets_task` as Method-only source relations.
  - Add the new `applied_in` relation contract and Task-vs-Scenario classification rules.
- Modify: `ontology/relations/uses_concept.md`
  - Remove paper-level instances and update semantic explanation to Method-only legality.
- Modify: `ontology/relations/targets_task.md`
  - Remove paper-level instances and update semantic explanation to Method-only legality.
- Create: `ontology/relations/applied_in.md`
  - New ledger for `[[Method]] --applied_in--> [[Scenario]]`.

### Live ontology pages
- Modify or rename: `ontology/entities/scenarios/知识图谱推理问答.md`
  - Converge the mixed example into a real application-context Scenario page.
- Modify: `ontology/entities/scenarios/index.md`
  - Update the managed navigation entry to match the corrected Scenario node.
- Modify: `ontology/entities/methods/PathMind.md`
  - Add outgoing `applied_in`, keep Method-only `uses_concept` and `targets_task`.
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
  - Remove now-invalid paper-level `uses_concept` and `targets_task` projections while preserving prose and `proposes` / `cites`.

### Workflow and governance guidance
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
  - Teach the new Method-only legality and `applied_in` relation.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
  - Add Task-vs-Scenario classification heuristics and forbid paper-level `uses_concept` / `targets_task` / `applied_in`.
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Add checks for `applied_in` and invalid paper-level formal edges.
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
  - Update projection assumptions for Scenario pages and Method-only relation families.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Add routing for `applied_in` and remove paper-level edge examples for `targets_task`.
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Update relation candidate expectations so `uses_concept` / `targets_task` / `applied_in` are Method-centered.

### Verification
- Run: `python3 scripts/lint_graph.py`
- Run: targeted `rg` commands over `ontology/` and `.claude/skills/` to ensure no stale paper-level `uses_concept` / `targets_task` or missing `applied_in` references remain.

---

### Task 1: Redefine ontology relation contracts

**Files:**
- Modify: `ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Read the exact graph-standard sections to edit**

Run:
```bash
rg -n "uses_concept|targets_task|supported_by|Scenario|survey / framework|关系文件分工|下沉语义" ontology/graph-standard.md
```
Expected: line hits for relation definitions, Scenario section, and relation-ledger governance sections.

- [ ] **Step 2: Write the failing expectation as a grep check**

Run:
```bash
rg -n '\[\[Paper\|Method\]\] --uses_concept-->|\[\[Paper\|Method\]\] --targets_task-->|应用场景语义默认通过 frontmatter `scenario`、对象页正文与索引导航表达，不再单独拆分 formal relation。' ontology/graph-standard.md
```
Expected: PASS showing the old mixed legality and old Scenario-downstream-only wording that must change.

- [ ] **Step 3: Rewrite the relation contract text in `ontology/graph-standard.md`**

Replace the relation block so it includes this content:
```markdown
- `uses_concept`：`[[Method]] --uses_concept--> [[Concept]]`；表示方法显式采用某概念作为定义、建模、机制设计或实现的一部分。若论文讨论了相关概念，应通过 Method 层 formal relation 承接；Paper 页中的概念信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Concept` formal edge。若需要表达“以前提方式依赖该概念”，默认写入 `edge_semantics`，而不额外拆分 formal relation。
- `targets_task`：`[[Method]] --targets_task--> [[Task]]`；表示方法主要面向的研究任务。若论文描述了任务定位，应通过 Method 层 formal relation 承接；Paper 页中的任务信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- `applied_in`：`[[Method]] --applied_in--> [[Scenario]]`；表示方法被明确应用、部署、验证或定位在某个应用场景中。该关系只允许 Method 作为 source、Scenario 作为 target；Paper 页中的场景信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Scenario` formal edge。
```
And add this boundary rule near the Scenario guidance:
```markdown
- `Task` 回答“要解决什么研究问题 / 推理范式 / 问答目标”；`Scenario` 回答“方法在什么应用语境 / 业务环境 / 部署上下文中使用”。
- 若候选项同时像 Task 又像 Scenario，优先判断其是否命名研究目标；若是 KGQA、多跳问答、推理、对齐、补全等研究目标，落为 `Task`；若是企业问答、金融风控、合规审查、投研辅助等应用语境，落为 `Scenario`。
- 若仍存在歧义，默认先判 `Task`，除非存在明确应用上下文证据支撑 `Scenario` 身份。
```

- [ ] **Step 4: Add `applied_in` to relation-file ownership and serving rules**

Make sure `graph-standard.md` also contains these updates:
```markdown
- `ontology/relations/applied_in.md`：维护 `applied_in`
```
and:
```markdown
- 应用场景语义若已稳定到方法层，可通过 `applied_in` 表达；尚不足以形成正式方法-场景边时，仍可下沉到 frontmatter `scenario`、对象页正文与索引导航表达。
```

- [ ] **Step 5: Run lint to verify the edited standard stays structurally valid**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS with no new structural errors.

- [ ] **Step 6: Commit the ontology-contract change**

```bash
git add ontology/graph-standard.md
git commit -m "docs: tighten method-only relation contracts"
```

### Task 2: Update relation ledgers to the new legality

**Files:**
- Modify: `ontology/relations/uses_concept.md`
- Modify: `ontology/relations/targets_task.md`
- Create: `ontology/relations/applied_in.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing legality check for stale paper-level edges**

Run:
```bash
rg -n '^- \[\[PathMind - .*\]\] --(uses_concept|targets_task)-->' ontology/relations/uses_concept.md ontology/relations/targets_task.md
```
Expected: PASS showing the stale paper-level ledger entries that must be removed.

- [ ] **Step 2: Rewrite `ontology/relations/uses_concept.md` to Method-only legality**

Make the top of the file read:
```markdown
## 关系语义说明
- `uses_concept` 表示方法显式采用某概念作为定义、建模、机制设计或实现的一部分。
- 合法 source：`Method`。
- 合法 target：`Concept`。
- Paper 页中的概念语义保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Concept` formal edge。
- 若需要表达“以前提方式依赖该概念”，默认写入 `edge_semantics`，而不额外拆分 formal relation。
```
And keep only these instance edges:
```markdown
- [[PathMind]] --uses_concept--> [[路径优先化]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/concepts/路径优先化.md
  - edge_semantics: 方法使用路径优先化机制评估候选路径的重要性。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --uses_concept--> [[重要推理路径]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/concepts/重要推理路径.md
  - edge_semantics: 方法围绕重要推理路径进行路径选择与答案生成。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
```

- [ ] **Step 3: Rewrite `ontology/relations/targets_task.md` to Method-only legality**

Make the top of the file read:
```markdown
## 关系语义说明
- `targets_task` 表示方法明确面向某个研究任务。
- 合法 source：`Method`。
- 合法 target：`Task`。
- Paper 页中的任务定位保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- 与应用场景相关的落地语义，若已稳定到方法层则应使用 `applied_in`；否则可写入对象页 `scenario`、正文或 `edge_semantics`。
```
And keep only these instance edges:
```markdown
- [[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/knowledge-graph-reasoning.md
  - edge_semantics: 方法以知识图谱推理为总体任务定位。
  - evidence: PathMind.sections
  - evidence_link: [[PathMind.sections]]
  - evidence_path: ontology/entities/evidence/PathMind.sections.md
- [[PathMind]] --targets_task--> [[kgqa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/kgqa.md
  - edge_semantics: 方法在知识图谱问答任务中被验证。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
- [[PathMind]] --targets_task--> [[multi-hop-qa]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/tasks/multi-hop-qa.md
  - edge_semantics: 方法重点处理复杂多跳问答中的路径筛选与推理。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
```

- [ ] **Step 4: Create the new `ontology/relations/applied_in.md` ledger**

Create the file with this content:
```markdown
## 关系语义说明
- `applied_in` 表示方法被明确应用、部署、验证或定位在某个应用场景中。
- 合法 source：`Method`。
- 合法 target：`Scenario`。
- 该关系用于表达应用语境归属，而不是研究任务归属；研究任务应继续使用 `targets_task`。
- Paper 页中的场景信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Scenario` formal edge。

## 实例边
- [[PathMind]] --applied_in--> [[企业知识图谱问答]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/scenarios/企业知识图谱问答.md
  - edge_semantics: 方法在企业知识图谱问答场景中结合路径优先化与结构化推理完成复杂问答。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
```

- [ ] **Step 5: Run lint and explicit relation grep checks**

Run:
```bash
python3 scripts/lint_graph.py && rg -n '\[\[Paper\]\] --targets_task-->|\[\[Paper\]\] --uses_concept-->|--applied_in-->' ontology/relations/*.md
```
Expected: lint PASS, no generic `[[Paper]]` legality examples for `targets_task`/`uses_concept`, and one `applied_in` ledger hit.

- [ ] **Step 6: Commit the relation-ledger changes**

```bash
git add ontology/relations/uses_concept.md ontology/relations/targets_task.md ontology/relations/applied_in.md
git commit -m "feat: add method-to-scenario relation ledger"
```

### Task 3: Correct the live Scenario page and its navigation entry

**Files:**
- Rename: `ontology/entities/scenarios/知识图谱推理问答.md` -> `ontology/entities/scenarios/企业知识图谱问答.md`
- Modify: `ontology/entities/scenarios/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing navigation/content check**

Run:
```bash
rg -n '知识图谱推理问答|研究场景|multi-hop-qa|kgqa' ontology/entities/scenarios/知识图谱推理问答.md ontology/entities/scenarios/index.md
```
Expected: PASS showing the current task-like Scenario name and semantics.

- [ ] **Step 2: Rename the Scenario file to an application-context name**

Run:
```bash
mv "ontology/entities/scenarios/知识图谱推理问答.md" "ontology/entities/scenarios/企业知识图谱问答.md"
```
Expected: shell exits successfully.

- [ ] **Step 3: Rewrite the Scenario page as a true application-context node**

Replace the file content with:
```markdown
---
title: 企业知识图谱问答
problem: [query-answering, reasoning]
method_family: [hybrid, llm, gnn]
scenario: [enterprise-qa]
research_task: [knowledge-graph-reasoning, kgqa, multi-hop-qa]
industry: [enterprise]
research_role: [application]
tags: [enterprise-qa, kgqa, 知识图谱问答]
status: processed
---

# 企业知识图谱问答

## Object semantics
- 一种面向企业知识服务与决策支持的应用场景，使用知识图谱上的结构化检索、路径筛选与多跳推理来回答复杂问题。

## 场景描述
- 该场景强调把知识图谱推理能力用于企业环境中的复杂问答、答案解释与知识服务。

## 核心挑战
- 关键挑战包括企业知识异构性、路径噪声控制、推理可解释性与响应效率平衡。

## 使用的主要方法 / 概念
- [[../methods/PathMind]]
- [[../concepts/路径优先化]]
- [[../concepts/重要推理路径]]

## 相关任务
- knowledge-graph-reasoning
- kgqa
- multi-hop-qa

## 相关论文
- [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]

## 相关 benchmark
- WebQSP
- CWQ

## 证据来源
- [[../evidence/PathMind.sections]]
- [[../evidence/PathMind.experiments]]

## 开放问题
- 如何在更大规模企业知识图谱上同时保持路径筛选效率、答案忠实性与可解释性。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.sections（文档：`ontology/entities/evidence/PathMind.sections.md`）：[[../evidence/PathMind.sections]]
  - edge_semantics: 章节级证据页支撑该场景中的问题建模与方法使用背景。
  - evidence: [[../evidence/PathMind.sections]]
- `supported_by`：PathMind.experiments（文档：`ontology/entities/evidence/PathMind.experiments.md`）：[[../evidence/PathMind.experiments]]
  - edge_semantics: 实验证据页支撑该场景中的性能、案例与效率比较。
  - evidence: [[../evidence/PathMind.experiments]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `applied_in`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 方法在企业知识图谱问答场景中结合路径优先化与结构化推理完成复杂问答。
  - evidence: [[../evidence/PathMind.experiments]]
```

- [ ] **Step 4: Update `ontology/entities/scenarios/index.md`**

Change the managed entry to:
```markdown
- 企业知识图谱问答 入口（文档：`ontology/entities/scenarios/企业知识图谱问答.md`）：[[ontology/entities/scenarios/企业知识图谱问答]]
  - object_semantics: 一种面向企业知识服务与决策支持的应用场景，使用知识图谱上的结构化检索、路径筛选与多跳推理来回答复杂问题。
  - status: serving-ready
```

- [ ] **Step 5: Run lint and a rename-safety grep**

Run:
```bash
python3 scripts/lint_graph.py && rg -n '知识图谱推理问答' ontology/entities/scenarios ontology/relations/applied_in.md ontology/entities/methods/PathMind.md
```
Expected: lint PASS and no stale Scenario name references in the touched ontology files.

- [ ] **Step 6: Commit the Scenario-page correction**

```bash
git add ontology/entities/scenarios/index.md ontology/entities/scenarios/企业知识图谱问答.md
git rm --cached --ignore-unmatch ontology/entities/scenarios/知识图谱推理问答.md || true
git commit -m "fix: correct scenario ontology example"
```

### Task 4: Reproject the affected Method and Paper pages

**Files:**
- Modify: `ontology/entities/methods/PathMind.md`
- Modify: `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing projection check**

Run:
```bash
rg -n '`targets_task`：|`uses_concept`：|`applied_in`：|知识图谱推理问答|企业知识图谱问答' ontology/entities/methods/PathMind.md ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md
```
Expected: PASS showing paper-level `targets_task` / `uses_concept` projections still present and no `applied_in` yet.

- [ ] **Step 2: Update `ontology/entities/methods/PathMind.md` to include `applied_in`**

Insert this outgoing relation after the three `targets_task` entries:
```markdown
- `applied_in`：企业知识图谱问答（文档：`ontology/entities/scenarios/企业知识图谱问答.md`）：[[../scenarios/企业知识图谱问答]]
  - edge_semantics: 方法在企业知识图谱问答场景中结合路径优先化与结构化推理完成复杂问答。
  - evidence: [[../evidence/PathMind.experiments]]
```
And update the human prose references from “知识图谱推理问答” to “企业知识图谱问答” where appropriate.

- [ ] **Step 3: Remove invalid paper-level formal projections from the PathMind paper page**

In `ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`, keep the prose sections `核心方法`, `相关任务`, and `应用场景`, but rewrite `## Formal relations` so its outgoing section begins with:
```markdown
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `proposes`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: 论文提出 PathMind 作为 retrieve-prioritize-reason 的知识图谱推理框架。
  - evidence: [[../evidence/PathMind.sections]]
- `cites`：Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning（文档：`ontology/entities/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md`）：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]
  - edge_semantics: 作为 retrieval-augmented 路线中的显式推理路径代表工作被引用。
  - evidence: [[../evidence/PathMind.refs]]
```
Then preserve the remaining `cites` edges exactly as they already appear, with no outgoing `targets_task` or `uses_concept` entries.

- [ ] **Step 4: Run lint and confirm projection legality**

Run:
```bash
python3 scripts/lint_graph.py && rg -n '`targets_task`：|`uses_concept`：' ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md && rg -n '`applied_in`：' ontology/entities/methods/PathMind.md ontology/entities/scenarios/企业知识图谱问答.md
```
Expected: lint PASS, no paper-page `targets_task`/`uses_concept` hits, and `applied_in` visible on Method + Scenario projections.

- [ ] **Step 5: Commit the page reprojection changes**

```bash
git add ontology/entities/methods/PathMind.md ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md
git commit -m "fix: reproject method and paper relation surfaces"
```

### Task 5: Align semantic-review skill guidance

**Files:**
- Modify: `.claude/skills/ontology-semantic-review/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Test: `rg -n "Paper ->|applied_in|Scenario|targets_task|uses_concept" .claude/skills/ontology-semantic-review`

- [ ] **Step 1: Write the failing prompt-guidance check**

Run:
```bash
rg -n 'Paper\|Method|Paper -> Scenario|uses_concept|targets_task|Scenario：行业或应用语境|研究任务型场景' .claude/skills/ontology-semantic-review
```
Expected: PASS showing stale mixed-source assumptions and missing `applied_in` guidance.

- [ ] **Step 2: Update `.claude/skills/ontology-semantic-review/SKILL.md` review focus**

Add these bullets under `## 审查重点` or `## 判断原则`:
```markdown
- `uses_concept` 是否被错误用于 `Paper`
- `targets_task` 是否被错误用于 `Paper`
- `applied_in` 是否被错误用于 `Paper`，或是否应由 `Method -> Scenario` 承接
- `Task` 与 `Scenario` 是否被混淆为同一语义层级
```

- [ ] **Step 3: Update `review-scope-rules.md` to the new legality contract**

Ensure the file contains these rules:
```markdown
- `Task`：要解决的研究问题、推理范式或问答目标。
- `Scenario`：行业、业务、部署或应用语境。
- 若一个候选项同时像 Task 又像 Scenario，优先判断其是否命名研究目标；若仍有歧义，默认先判 `Task`。
- `uses_concept` 只允许 `Method` 作为 source；若论文讨论概念，应落到 Method formal edge 或保留在 Paper prose / Evidence。
- `targets_task` 只允许 `Method` 作为 source；若论文描述任务定位，应落到 Method formal edge 或保留在 Paper prose / Evidence。
- `applied_in` 只允许 `Method -> Scenario`；`Paper -> Scenario` 不合法。
```

- [ ] **Step 4: Update `diff-review-playbook.md` with new checks**

Add explicit checks like:
```markdown
- 如果 `targets_task.md` 中出现 `Paper` 作为 source，必须指出，并建议迁移到对应 Method formal edge 或 Paper prose。
- 如果 `uses_concept.md` 中出现 `Paper` 作为 source，必须指出，并建议迁移到对应 Method formal edge 或 Paper prose。
- 如果新增了场景 formal relation，检查其是否为 `[[Method]] --applied_in--> [[Scenario]]`，而不是 `Paper -> Scenario` 或 `Scenario -> Task`。
```

- [ ] **Step 5: Run the skill-guidance grep check**

Run:
```bash
rg -n 'applied_in|只允许 `Method`|Paper -> Scenario|Paper 作为 source|默认先判 `Task`' .claude/skills/ontology-semantic-review
```
Expected: PASS with hits for all new legality and classification guidance.

- [ ] **Step 6: Commit the semantic-review skill updates**

```bash
git add .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/review-scope-rules.md .claude/skills/ontology-semantic-review/references/diff-review-playbook.md
git commit -m "docs: update ontology semantic review rules"
```

### Task 6: Align ingest, reconciliation, and projection skills

**Files:**
- Modify: `.claude/skills/page-projection-sync/SKILL.md`
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `rg -n "applied_in|targets_task|uses_concept|Paper|Scenario" .claude/skills/page-projection-sync/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Write the failing workflow-guidance check**

Run:
```bash
rg -n '\[\[Paper\]\] --targets_task-->|survey 论文页：优先同步 `proposes`、`uses_concept`、`targets_task`|场景适配型 formal edge|targets_task: \[\]|uses_concept: \[\]' .claude/skills/page-projection-sync/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/paper-ingest/SKILL.md
```
Expected: PASS showing stale assumptions that still treat paper-level `uses_concept` / `targets_task` as normal.

- [ ] **Step 2: Update `page-projection-sync` to the new projection rules**

Revise the relevant guidance so it says:
```markdown
- survey / framework 论文页：优先同步 `proposes`、`cites`，并保留概念、任务、场景的人类区块与豁免信息；不再把 `uses_concept`、`targets_task` 作为 Paper 页 formal relation 默认集合。
- Scenario 页若存在正式场景邻接，应同步 incoming `applied_in`；不得继续假设“场景适配型 formal edge 默认不存在”。
```

- [ ] **Step 3: Update `relation-reconciliation` routing and examples**

Add `applied_in` routing and fix the structured example to Method-only:
```markdown
- `applied_in` → `ontology/relations/applied_in.md`
```
and replace the sample output block line:
```yaml
  - file: ontology/relations/targets_task.md
    edge: "[[Method]] --targets_task--> [[Task]]"
```
Also add a parallel example for `applied_in` if the file currently lists sample routed relations.

- [ ] **Step 4: Update `paper-ingest` extraction guidance**

Revise the extraction rules so they contain this content:
```markdown
- `targets_task` candidate 只从稳定 `Method` 身份出发生成，不生成 `Paper -> Task` formal candidate。
- `uses_concept` candidate 只从稳定 `Method` 身份出发生成，不生成 `Paper -> Concept` formal candidate。
- 若论文明确给出方法应用语境，且 Method 身份稳定，可生成 `applied_in` candidate：`[[Method]] --applied_in--> [[Scenario]]`。
- `scenario` 与 `research_task` 继续保留在 Paper / Method frontmatter 中，但不等于自动生成对应 Paper formal edge。
```
And extend the required relation-type list and output template to include:
```markdown
- `applied_in`
```
plus:
```yaml
  applied_in: []
```

- [ ] **Step 5: Run the workflow-guidance grep check**

Run:
```bash
rg -n 'applied_in|\[\[Method\]\] --targets_task-->|\[\[Method\]\] --uses_concept-->|Paper -> Task|Paper -> Concept|Paper -> Scenario' .claude/skills/page-projection-sync/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/paper-ingest/SKILL.md
```
Expected: PASS with updated Method-only legality wording and `applied_in` references.

- [ ] **Step 6: Commit the workflow-skill changes**

```bash
git add .claude/skills/page-projection-sync/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/paper-ingest/SKILL.md
git commit -m "docs: align ingest workflow with scenario relation"
```

### Task 7: Run final verification across ontology and skills

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full structural verification**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

- [ ] **Step 2: Verify no stale paper-level formal edges remain for the changed relation families**

Run:
```bash
rg -n '^- \[\[.*\]\] --uses_concept-->|^- \[\[.*\]\] --targets_task-->' ontology/entities/papers ontology/relations/uses_concept.md ontology/relations/targets_task.md
```
Expected: no paper-page `uses_concept`/`targets_task` formal projection hits, and no paper-source ledger entries.

- [ ] **Step 3: Verify the new Scenario contract is visible end-to-end**

Run:
```bash
rg -n 'applied_in|企业知识图谱问答' ontology/graph-standard.md ontology/relations/applied_in.md ontology/entities/methods/PathMind.md ontology/entities/scenarios/企业知识图谱问答.md .claude/skills
```
Expected: hits in graph standard, the new ledger, the Method page, the Scenario page, and updated skills.

- [ ] **Step 4: Inspect git diff for scope control**

Run:
```bash
git diff --stat HEAD~6..HEAD && git diff --name-only HEAD~6..HEAD
```
Expected: only the planned ontology, scenario, relation, and skill files are included.

- [ ] **Step 5: Commit any final fixups if verification required them**

If no further changes were needed, do nothing.
If verification required edits, commit them with:
```bash
git add ontology/graph-standard.md ontology/relations/*.md ontology/entities/scenarios/index.md ontology/entities/scenarios/企业知识图谱问答.md ontology/entities/methods/PathMind.md ontology/entities/papers/PathMind\ -\ A\ Retrieve-Prioritize-Reason\ Framework\ for\ Knowledge\ Graph\ Reasoning\ with\ Large\ Language\ Models.md .claude/skills/ontology-semantic-review/SKILL.md .claude/skills/ontology-semantic-review/references/*.md .claude/skills/page-projection-sync/SKILL.md .claude/skills/relation-reconciliation/SKILL.md .claude/skills/paper-ingest/SKILL.md
git commit -m "chore: finish ontology contract realignment"
```

## Spec coverage self-check
- Add `Method -> Scenario` formal relation `applied_in` → covered by Tasks 1, 2, 4, 6, 7.
- Restrict `uses_concept` and `targets_task` to Method-only sources → covered by Tasks 1, 2, 4, 5, 6, 7.
- Fix the mixed Scenario example into a true application-context page → covered by Task 3 and verified again in Task 7.
- Update affected ledgers, object pages, indexes, and relevant skills → covered by Tasks 2 through 6.
- Do not expand to lint automation or repo-wide migration → enforced by file scope and Task 7 diff review.

## Placeholder scan
- No `TODO`, `TBD`, or “similar to Task N” placeholders remain.
- Every code/content-edit step includes concrete text or exact commands.
- Verification commands are explicit and tied to expected outcomes.

## Type consistency check
- `uses_concept` is Method→Concept everywhere in the plan.
- `targets_task` is Method→Task everywhere in the plan.
- `applied_in` is Method→Scenario everywhere in the plan.
- The corrected Scenario name is consistently `企业知识图谱问答` in ledger, page, index, and verification steps.
