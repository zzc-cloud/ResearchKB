# paper-ingest Relation Autowrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `paper-ingest` so new ingests automatically write `proposes`, `evaluated_on`, and `sourced_from` edges when applicable, while explicitly exempting `evaluated_on` for survey/framework/taxonomy papers with no unified benchmark.

**Architecture:** Keep the existing skill structure and strengthen its instructions rather than redesigning the workflow. Extend the relation-writing step in `SKILL.md`, add explicit extraction rules and exemption language, and update the existing eval materials so future edits have concrete regression targets for method-paper and survey-paper behavior.

**Tech Stack:** Markdown skill spec, JSON eval fixtures, ResearchKB ontology conventions

---

## File Structure

### Files to modify
- `.claude/skills/paper-ingest/SKILL.md`
  - Expand Step 5 relation coverage, add explicit `proposes` / `evaluated_on` / `sourced_from` rules, and tighten final output wording around exemptions vs omissions.
- `.claude/skills/paper-ingest/evals/regression-samples.json`
  - Add two regression cases that exercise the new relation-autowrite behavior.
- `.claude/skills/paper-ingest/evals/quality-checklist.md`
  - Add checklist items so manual review explicitly verifies the three new relation behaviors and the benchmark exemption wording.

### Files to inspect during implementation
- `docs/superpowers/specs/2026-05-02-paper-ingest-relation-autowrite-design.md`
- `wiki/ontology/graph-standard.md`
- `wiki/relations/paper_method_links.md`
- `wiki/relations/benchmark_links.md`
- `wiki/relations/provenance_links.md`
- `.claude/skills/paper-ingest/evals/trigger-evals.json`

---

### Task 1: Update `paper-ingest` relation-writing instructions

**Files:**
- Modify: `.claude/skills/paper-ingest/SKILL.md:91-106`
- Modify: `.claude/skills/paper-ingest/SKILL.md:128-131`
- Modify: `.claude/skills/paper-ingest/SKILL.md:150-176`
- Test: `.claude/skills/paper-ingest/SKILL.md`

- [ ] **Step 1: Capture the current blind spot in the skill text**

Run:
```bash
grep -n "citation_graph\|method_evolution\|concept_links\|paper_method_links\|benchmark_links\|provenance_links\|evaluated_on\|sourced_from\|未生成 evaluated_on" ".claude/skills/paper-ingest/SKILL.md"
```

Expected: output shows `citation_graph.md` / `method_evolution.md` / `concept_links.md`, but does not yet require `paper_method_links.md`, `benchmark_links.md`, or `provenance_links.md`, and does not contain explicit benchmark-exemption wording.

- [ ] **Step 2: Expand Step 5 so relation ledgers are checked comprehensively**

Replace the Step 5 relation/update block with the following text:

```md
6. 关联关系：在落库完成前，逐类判断是否存在应正式落账的关系；只要存在就写入对应账本，而不是留在正文 prose 中。
   - `wiki/relations/citation_graph.md`
   - `wiki/relations/method_evolution.md`
   - `wiki/relations/concept_links.md`
   - `wiki/relations/task_method_map.md`
   - `wiki/relations/evidence_index.md`
   - `wiki/relations/paper_method_links.md`
   - `wiki/relations/benchmark_links.md`
   - `wiki/relations/provenance_links.md`
7. 更新：
   - `wiki/index.md`
   - `wiki/log.md`
```

- [ ] **Step 3: Add explicit extraction rules for the three new relation types**

Append the following block under `## 关系文件`:

```md
- `proposes`：
  - 方法论文若提出核心方法，必须登记 `[[Paper]] --proposes--> [[Method]]`
  - 若论文核心贡献是 framework / taxonomy 型概念，必须登记 `[[Paper]] --proposes--> [[Concept]]`
  - framework / taxonomy 型核心知识产物仍按当前本体优先落为 Concept，不改写为 Method
- `evaluated_on`：
  - empirical / method / application 论文只要存在明确 benchmark，必须登记 `[[Paper]] --evaluated_on--> [[Benchmark]]`
  - 若该 benchmark 同时明确服务某个核心 Method 的正式评测，也应登记 `[[Method]] --evaluated_on--> [[Benchmark]]`
  - survey / framework / taxonomy / dataset / benchmark 类型论文若无统一 benchmark，不生成 `evaluated_on`，并在最终输出中显式写明“按规范豁免”
- `sourced_from`：
  - 只要本次生成了 `sections.md`、`refs.md`、`experiments.md`、`analysis.md`、`full.md` 任一 Evidence 缓存，就必须同步登记 `[[Evidence]] --sourced_from--> [[RawSource]]`
```

- [ ] **Step 4: Tighten the final output contract so exemptions are explicit**

Replace the “解释” block under `## 最终输出格式` with:

```md
解释：
- `success`：基础缓存、正式页面与应有关系账本更新都已完成，且结构适配良好；如生成了 `full.md`，它作为高复用增强缓存计入 `generated_caches`。
- `partial`：完成了大部分工作，但某些页面、字段或正式关系账本仍需人工补充。
- `needs-skill-update`：当前论文类型或结构已经超出本 skill 的稳定适配范围。
- 若某类关系按规范豁免（例如 survey / framework 论文无统一 benchmark，因此不生成 `evaluated_on`），必须在 `warnings` 中显式说明豁免原因；不要把正常豁免写成“待补充”。
```

Also append this sentence to `## 使用完成后的建议`:

```md
- 若某类关系因规范豁免未生成，应明确区分“正常豁免”与“skill 漏写”，避免把豁免项误报为待补。
```

- [ ] **Step 5: Verify the new relation-writing language exists**

Run:
```bash
grep -n "paper_method_links\|benchmark_links\|provenance_links\|`proposes`：\|`evaluated_on`：\|`sourced_from`：\|按规范豁免" ".claude/skills/paper-ingest/SKILL.md"
```

Expected: matches exist for all three new ledger files, all three relation-rule headings, and the explicit exemption wording.

- [ ] **Step 6: Commit the skill-text update**

```bash
git add .claude/skills/paper-ingest/SKILL.md
git commit -m "docs: require relation autowrite in paper-ingest"
```

Expected: commit succeeds with only the SKILL.md change for this task.

---

### Task 2: Add regression fixtures for method-paper and survey-paper behavior

**Files:**
- Modify: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Modify: `.claude/skills/paper-ingest/evals/quality-checklist.md`
- Test: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Test: `.claude/skills/paper-ingest/evals/quality-checklist.md`

- [ ] **Step 1: Inspect the current eval fixture format before editing**

Run:
```bash
python3 -m json.tool ".claude/skills/paper-ingest/evals/regression-samples.json" >/tmp/paper_ingest_regression.pretty.json && sed -n '1,220p' /tmp/paper_ingest_regression.pretty.json && sed -n '1,220p' ".claude/skills/paper-ingest/evals/quality-checklist.md"
```

Expected: the JSON pretty-prints successfully, revealing the existing sample schema; the checklist renders as readable markdown headings/bullets.

- [ ] **Step 2: Add a method-paper regression case to `regression-samples.json`**

Insert a case shaped like the existing entries, with these exact semantic fields and expectations adapted to the file’s current schema:

```json
{
  "id": "pathmind-relations",
  "prompt": "处理论文：raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf，重点检查关系落账是否完整",
  "expected_output": [
    "updates wiki/relations/paper_method_links.md with a proposes edge from the PathMind paper to the PathMind method",
    "updates wiki/relations/benchmark_links.md with evaluated_on edges for WebQSP and CWQ",
    "updates wiki/relations/provenance_links.md with sourced_from edges for generated PathMind evidence caches"
  ]
}
```

If the file uses different field names (for example `expected`, `checks`, or a top-level wrapper object), preserve the surrounding schema and translate the three expectations into the existing structure rather than inventing a new schema.

- [ ] **Step 3: Add a survey/framework regression case to `regression-samples.json`**

Insert a second case in the same schema:

```json
{
  "id": "llm-kg-cpd-survey-relations",
  "prompt": "处理论文：raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf，重点检查 framework 类型论文的关系落账",
  "expected_output": [
    "updates wiki/relations/paper_method_links.md with a proposes edge from the survey paper to the framework concept",
    "updates wiki/relations/provenance_links.md with sourced_from edges for generated survey evidence caches",
    "does not create evaluated_on edges when the paper has no unified benchmark and explicitly reports the benchmark exemption reason"
  ]
}
```

Again, preserve the file’s actual outer structure.

- [ ] **Step 4: Extend `quality-checklist.md` so manual review covers the new behavior**

Append this section to the checklist:

```md
## Relation autowrite checks
- [ ] 如果论文提出核心方法，输出与落库结果必须包含 `proposes` 正式关系，而不是只在正文里写“提出了某方法”。
- [ ] 如果论文核心贡献是 framework / taxonomy 型概念，输出与落库结果必须包含 `Paper -> Concept` 的 `proposes` 关系。
- [ ] 如果 empirical / method / application 论文存在明确 benchmark，输出与落库结果必须包含 `evaluated_on` 正式关系。
- [ ] 如果 survey / framework / taxonomy 论文没有统一 benchmark，不能伪造 `evaluated_on`；必须在输出中明确说明“按规范豁免”。
- [ ] 只要生成了任一 Evidence 缓存，就必须同步登记 `sourced_from` provenance 关系。
```

- [ ] **Step 5: Validate the eval files after editing**

Run:
```bash
python3 -m json.tool ".claude/skills/paper-ingest/evals/regression-samples.json" >/tmp/paper_ingest_regression.pretty.json && grep -n "pathmind-relations\|llm-kg-cpd-survey-relations" ".claude/skills/paper-ingest/evals/regression-samples.json" && grep -n "Relation autowrite checks\|按规范豁免\|sourced_from provenance" ".claude/skills/paper-ingest/evals/quality-checklist.md"
```

Expected: JSON validation passes, both new regression IDs are found, and the new checklist section/phrases are present.

- [ ] **Step 6: Commit the regression fixtures**

```bash
git add .claude/skills/paper-ingest/evals/regression-samples.json .claude/skills/paper-ingest/evals/quality-checklist.md
git commit -m "test: cover paper-ingest relation autowrite"
```

Expected: commit succeeds with only the eval fixture changes.

---

### Task 3: Final verification and implementation handoff

**Files:**
- Test: `.claude/skills/paper-ingest/SKILL.md`
- Test: `.claude/skills/paper-ingest/evals/regression-samples.json`
- Test: `.claude/skills/paper-ingest/evals/quality-checklist.md`
- Test: `wiki/ontology/graph-standard.md`

- [ ] **Step 1: Re-run the complete verification commands**

Run:
```bash
grep -n "paper_method_links\|benchmark_links\|provenance_links\|按规范豁免" ".claude/skills/paper-ingest/SKILL.md" && \
python3 -m json.tool ".claude/skills/paper-ingest/evals/regression-samples.json" >/tmp/paper_ingest_regression.pretty.json && \
grep -n "Relation autowrite checks\|proposes\|evaluated_on\|sourced_from" ".claude/skills/paper-ingest/evals/quality-checklist.md"
```

Expected:
- `SKILL.md` contains the new ledger names and explicit exemption wording
- `regression-samples.json` remains valid JSON
- `quality-checklist.md` contains the new autowrite checks

- [ ] **Step 2: Confirm the skill text stays aligned with the ontology**

Run:
```bash
grep -n "`proposes`：`\[\[Paper\]\] --proposes--> \[\[Method\|Concept\]\]`\|`evaluated_on`：`\[\[Paper\|Method\]\] --evaluated_on--> \[\[Benchmark\]\]`\|`sourced_from`：`\[\[Evidence\]\] --sourced_from--> \[\[RawSource\]\]`" "wiki/ontology/graph-standard.md"
```

Expected: all three ontology relation definitions are found, confirming the skill’s new instructions match the current graph standard.

- [ ] **Step 3: Use this exact handoff conclusion in the final summary**

```text
paper-ingest 现在会在 skill 说明层面把 proposes / evaluated_on / sourced_from 视为默认正式关系义务：有方法或 framework/taxonomy 核心产物就写 proposes；有统一 benchmark 就写 evaluated_on；有 Evidence 缓存就写 sourced_from。对无统一 benchmark 的 survey / framework / taxonomy 论文，不再把 evaluated_on 当“待补”，而是显式报告“按规范豁免”。
```

- [ ] **Step 4: Create the final implementation commit**

```bash
git add .claude/skills/paper-ingest/SKILL.md .claude/skills/paper-ingest/evals/regression-samples.json .claude/skills/paper-ingest/evals/quality-checklist.md
git commit -m "feat: autowrite relation edges in paper-ingest"
```

Expected: commit succeeds with the final integrated state. If earlier task commits were already created, skip this step and report the existing commit hashes instead.
