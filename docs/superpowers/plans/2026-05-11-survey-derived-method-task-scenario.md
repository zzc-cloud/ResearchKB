# Survey-Derived Method Task/Scenario Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow survey-derived methods to retain `targets_task` and `applied_in` when evidence is strong, while explicitly keeping Task↔Scenario non-formal in phase 1.

**Architecture:** Tighten the ontology contract around one invariant: once an object is admitted as a `Method`, its downstream formal relation eligibility does not depend on whether it entered via `proposes` or `surveys_method`. Implement that invariant through ontology prose and workflow guidance only, while explicitly rejecting any direct Task↔Scenario relation family in phase 1.

**Tech Stack:** Obsidian Markdown knowledge base, ontology contract in `ontology/graph-standard.md`, workflow skills under `.claude/skills/`, Python lint entrypoint `scripts/lint_graph.py`

---

## File structure

### Ontology contract
- Modify: `ontology/graph-standard.md`
  - State that survey-derived methods may still receive `targets_task` and `applied_in`.
  - Add stronger evidence thresholds for survey-derived task/scenario edges.
  - Explicitly reject direct Task↔Scenario formal relations in phase 1.
  - Clarify that `surveys_method` admits a Method into the graph but does not constrain the Method’s downstream relation rights.

### Workflow and governance guidance
- Modify: `.claude/skills/paper-ingest/SKILL.md`
  - Permit `targets_task` and `applied_in` for survey-derived methods when evidence is structured and auditable.
  - Reject direct Task↔Scenario formal-edge generation.
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
  - Treat survey-derived task/scenario edges as valid method-level relations when evidence is strong.
  - Reject Task↔Scenario direct-edge promotion.
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
  - Clarify that source-paper role does not reduce a Method’s downstream relation rights.
  - Reject direct Task↔Scenario formal relations.
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
  - Add checks for invalid direct Task↔Scenario edges and for missing survey-derived method task/scenario edges.

### Verification
- Run: `python3 scripts/lint_graph.py`
- Run: targeted `rg` checks over ontology and skills for `surveys_method`, `targets_task`, `applied_in`, and direct Task↔Scenario anti-patterns.

---

### Task 1: Update the phase-1 ontology contract

**Files:**
- Modify: `ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Write the failing contract grep check**

Run:
```bash
rg -n '来源论文类型无关|Task -> Scenario|Scenario -> Task|共享的 Method 邻接|surveys_method.*targets_task|surveys_method.*applied_in' ontology/graph-standard.md
```
Expected: FAIL to find explicit phase-1 rules for survey-derived method edges and Task↔Scenario non-formality.

- [ ] **Step 2: Add the survey-derived method eligibility rule**

Insert this exact rule into the relation-semantics area near the `surveys_method`, `targets_task`, and `applied_in` definitions:
```markdown
- 对于通过 `surveys_method` 稳定覆盖并 materialize 的 `Method`，只要当前论文对其任务定位或应用场景提供结构化、可审计的归属证据，仍可继续生成 `[[Method]] --targets_task--> [[Task]]` 与 `[[Method]] --applied_in--> [[Scenario]]`；其合法性不因 source paper 属于 survey 而降低。
```

- [ ] **Step 3: Add stronger evidence-threshold rules for survey-derived edges**

Add this exact block after the rule above:
```markdown
- survey-derived `targets_task` 只在论文将该方法明确纳入任务分组、任务 taxonomy、任务比较表或任务 coverage 结构时成立；仅有零散任务 mention，不足以生成 formal edge。
- survey-derived `applied_in` 只在论文将该方法明确纳入场景分组、场景 taxonomy、场景比较表或应用 coverage 结构时成立；仅有背景领域描述、benchmark 域属性或泛化应用前景，不足以生成 formal edge。
```

- [ ] **Step 4: Add the Task↔Scenario non-formal boundary**

Insert this explicit boundary statement into `ontology/graph-standard.md`:
```markdown
- phase 1 不直接维护 `Task -> Scenario` 或 `Scenario -> Task` formal relation。Task 与 Scenario 的联系默认通过共享的 Method 邻接表达，而不是压缩为静态直接边。
```

- [ ] **Step 5: Update survey-paper guidance to reflect mediated structure**

In the survey-paper Paper guidance, append this sentence:
```markdown
- survey 论文若稳定覆盖某方法，可通过 `surveys_method` 把方法纳入正式图谱；该方法后续仍可继续投影到 `targets_task` 与 `applied_in`，但 Task 与 Scenario 之间仍不直接升格为 formal relation。
```

- [ ] **Step 6: Run lint to verify the contract remains valid**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

### Task 2: Update ingest guidance for survey-derived method edges

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md`
- Test: `rg -n "surveys_method|targets_task|applied_in|Task.*Scenario|Scenario.*Task" .claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Write the failing ingest-guidance grep check**

Run:
```bash
rg -n 'surveys_method|Task -> Scenario|Scenario -> Task|coverage 列表|结构化 coverage' .claude/skills/paper-ingest/SKILL.md
```
Expected: PASS for `surveys_method` itself, but FAIL to find explicit guidance that survey-derived methods retain task/scenario edges and that direct Task↔Scenario edges are forbidden.

- [ ] **Step 2: Add survey-derived Method edge rules to `paper-ingest`**

Under the relation-generation guidance in `.claude/skills/paper-ingest/SKILL.md`, add:
```markdown
- 若某方法通过 `surveys_method` 被稳定纳入图谱，且 survey / landscape / taxonomy 论文对其任务归属提供结构化 coverage（如任务分组、taxonomy、比较表、coverage 列表），仍可继续生成 `[[Method]] --targets_task--> [[Task]]`。
- 若某方法通过 `surveys_method` 被稳定纳入图谱，且 survey / landscape / taxonomy 论文对其场景归属提供结构化 coverage（如场景分组、taxonomy、比较表、coverage 列表），仍可继续生成 `[[Method]] --applied_in--> [[Scenario]]`。
```

- [ ] **Step 3: Add the direct-edge prohibition to `paper-ingest`**

Add this exact prohibition:
```markdown
- 不生成 `[[Task]] -> [[Scenario]]` 或 `[[Scenario]] -> [[Task]]` formal candidate；Task 与 Scenario 的联系在 phase 1 默认通过共享的 Method 邻接表达。
```

- [ ] **Step 4: Add weak-evidence rejection guidance**

Add this block:
```markdown
- 若 survey 论文只是顺带提到某任务或场景，而没有把方法明确纳入对应的结构化分组、coverage 或比较框架，则不得为该方法生成 `targets_task` 或 `applied_in`。
```

- [ ] **Step 5: Run the ingest-guidance verification grep**

Run:
```bash
rg -n 'surveys_method|targets_task|applied_in|Task 与 Scenario|Task -> Scenario|Scenario -> Task|结构化 coverage' .claude/skills/paper-ingest/SKILL.md
```
Expected: PASS with explicit survey-derived method-edge permission and direct Task↔Scenario prohibition.

### Task 3: Update reconciliation and semantic-review guidance

**Files:**
- Modify: `.claude/skills/relation-reconciliation/SKILL.md`
- Modify: `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- Modify: `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`
- Test: `rg -n "surveys_method|targets_task|applied_in|Task -> Scenario|Scenario -> Task" .claude/skills/relation-reconciliation .claude/skills/ontology-semantic-review`

- [ ] **Step 1: Write the failing governance grep check**

Run:
```bash
rg -n '来源论文类型无关|surveys_method|Task -> Scenario|Scenario -> Task|共享的 Method 邻接' .claude/skills/relation-reconciliation .claude/skills/ontology-semantic-review
```
Expected: FAIL to find explicit “survey-derived methods still keep method-level edges” and Task↔Scenario prohibition wording.

- [ ] **Step 2: Update `relation-reconciliation` guidance**

Add this exact block under the strong-semantic review section in `.claude/skills/relation-reconciliation/SKILL.md`:
```markdown
- 若某方法通过 `surveys_method` 已稳定进入图谱，而当前论文又以结构化 coverage 明确给出其任务或场景归属，则应继续判断是否补为 `targets_task` 或 `applied_in`；不得因为该方法来自 survey paper 就默认降级为 context-only。
- 若候选关系试图直接把 `Task` 与 `Scenario` 相连，则默认归入 `needs_human_review` 或直接视为 phase-1 非法关系，而不是直接落账。
```

- [ ] **Step 3: Update `review-scope-rules.md`**

Append these rules under the existing `surveys_method` guidance:
```markdown
- Method 一旦身份稳定，其可拥有的 formal relations 与来源论文类型无关；通过 `surveys_method` 进入图谱的方法，仍可继续拥有 `targets_task` 与 `applied_in`。
- survey-derived `targets_task` / `applied_in` 必须有结构化、可审计的 coverage 证据；不能仅凭背景 mention 或泛化推断生成。
- phase 1 不直接维护 `Task -> Scenario` 或 `Scenario -> Task` formal relation。
```

- [ ] **Step 4: Update `diff-review-playbook.md`**

Add these review checks:
```markdown
- 如果由 `surveys_method` 稳定覆盖的方法拥有清晰的任务/场景 coverage，却没有补齐 `targets_task` 或 `applied_in`，必须指出。
- 如果 diff 试图新增 `Task -> Scenario` 或 `Scenario -> Task` formal relation，必须指出，并建议改为通过共享 Method 邻接表达。
```

- [ ] **Step 5: Run the governance verification grep**

Run:
```bash
rg -n '来源论文类型无关|surveys_method|Task -> Scenario|Scenario -> Task|共享的 Method 邻接' .claude/skills/relation-reconciliation .claude/skills/ontology-semantic-review
```
Expected: PASS with explicit survey-derived method-edge permission and Task↔Scenario rejection rules.

### Task 4: Final verification and scope check

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run full lint**

Run:
```bash
python3 scripts/lint_graph.py
```
Expected: PASS.

- [ ] **Step 2: Verify the new policy is present and the forbidden direct-edge family is absent**

Run:
```bash
rg -n 'surveys_method|targets_task|applied_in|Task -> Scenario|Scenario -> Task|共享的 Method 邻接' ontology/graph-standard.md .claude/skills/paper-ingest .claude/skills/relation-reconciliation .claude/skills/ontology-semantic-review --glob '*.md'
```
Expected: PASS with explicit support for survey-derived method edges and only prohibition wording for direct Task↔Scenario relations.

- [ ] **Step 3: Inspect diff scope**

Run:
```bash
git diff --name-only
```
Expected: only the planned ontology contract and related guidance files are included.

## Spec coverage self-check
- Survey-derived methods may retain `targets_task` and `applied_in` → covered by Tasks 1, 2, 3, 4.
- Source-paper role does not weaken Method downstream relation eligibility → covered by Tasks 1 and 3.
- Task↔Scenario stays non-formal in phase 1 → covered by Tasks 1, 2, 3, 4.
- No new direct Task↔Scenario relation family introduced → enforced by scope and verification.

## Placeholder scan
- No `TODO`, `TBD`, or vague placeholders remain.
- All edit steps specify exact files and exact text.
- Verification commands are explicit and fresh.

## Type consistency check
- `surveys_method` remains the Paper→Method admission/coverage relation.
- `targets_task` and `applied_in` remain Method-only downstream relations.
- Task↔Scenario is consistently non-formal throughout the plan.
