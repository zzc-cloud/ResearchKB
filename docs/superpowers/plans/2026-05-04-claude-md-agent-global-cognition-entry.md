# CLAUDE.md Agent Global Cognition Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Insert a short `Agent 的全局认知入口` section into `CLAUDE.md` that gives agents a cross-task global mental model while preserving `wiki/ontology/graph-standard.md` as the only normative authority.

**Architecture:** This is a documentation-only change in a single file. The implementation inserts one new section between the existing normative-boundary section and the existing four-layer architecture section, using the approved spec text and preserving the later workflow sections without duplication.

**Tech Stack:** Markdown, git

---

## File structure

- Modify: `CLAUDE.md`
  - Insert one new section after `## 知识库结构与规范边界`
  - Keep existing `## ResearchKB 核心架构` and later sections intact
- Reference while editing: `docs/superpowers/specs/2026-05-04-claude-md-agent-global-cognition-entry-design.md`

## Task 1: Insert the global cognition entry section

**Files:**
- Modify: `CLAUDE.md:23-47`
- Reference: `docs/superpowers/specs/2026-05-04-claude-md-agent-global-cognition-entry-design.md:112-141`

- [ ] **Step 1: Read the insertion area and confirm the anchor headings**

Read:
- `CLAUDE.md` around `## 知识库结构与规范边界`
- `CLAUDE.md` around `## ResearchKB 核心架构`

Expected anchors:
- the insertion point is immediately after the paragraph ending with `若两处存在细节差异，以 \`wiki/ontology/graph-standard.md\` 为准。`
- the next existing heading is `## ResearchKB 核心架构`

- [ ] **Step 2: Insert the approved section text**

Add this block between the two headings:

```md
## Agent 的全局认知入口

ResearchKB 的唯一核心认知中心是本体认知。`wiki/ontology/graph-standard.md` 定义合法节点、关系、证据、实例边、投影与豁免规则，是所有知识判定的唯一权威来源。`CLAUDE.md` 不提供另一套平行规范；它的作用，是把这套本体约束转化为 Agent 在不同任务中的统一工作视角。

Agent 在处理问答、治理、摄入、修复、综述等任务时，应始终先把当前任务放回同一个知识系统中理解，而不是把仓库视为一组离散 markdown 文件。默认应按以下四层来建立全局认知：

1. **本体骨架层**
   - 由 `wiki/ontology/graph-standard.md` 定义合法知识边界与判定规则。

2. **本体实例编译层**
   - 负责把原始论文编译为 `intermediate/papers/` 证据缓存、`wiki/relations/` 正式关系实例边，以及 `wiki/` serving-ready 对象页中的投影结果。

3. **本体治理层**
   - 负责通过结构治理、语义治理与 serving 治理，决定哪些知识变更可以进入正式图谱。

4. **本体应用层**
   - 负责基于治理通过后的正式知识进行问答、分析、探索与综述生成。

这四层不是四套独立系统，而是同一知识系统中的不同职责面。全局认知负责帮助 Agent 判断“当前任务位于哪一层、应先读取哪一层、何时需要向邻近层扩展”；具体的节点、关系、证据与合法性判定，始终以本体规范为准。

因此，Agent 应默认遵循以下认知锚点：
- 正式知识问答优先读取 serving-ready 对象页，而不是先扫描 `wiki/relations/`
- `wiki/relations/` 是正式关系实例边的治理真源，主要用于补边、修复、审计与一致性核对
- 对象页中的 `Formal relations` 是治理通过后供问答与受约束拓扑扩展消费的正式读取面
- `intermediate/papers/` 是机制、实验、引用、基线与 provenance 的默认证据层
- `raw/` 只用于来源回溯，不承担主图谱组织职责
```

- [ ] **Step 3: Review the surrounding text for duplication and transition quality**

Check the updated `CLAUDE.md` immediately around the insertion and confirm:
- the new section does not redefine node types, relation types, or evidence rules
- the new section does not conflict with the later `## ResearchKB 核心架构` section
- the later `## 本体全局基础认知` section still reads as a deeper follow-on rather than a duplicate header
- there is a blank line before and after the inserted section so markdown structure is clean

Expected result:
- the new section acts as a bridge from authority boundaries to architecture and workflow details

- [ ] **Step 4: Read the updated section verbatim for final verification**

Read back:
- the full `## Agent 的全局认知入口` section
- the following heading `## ResearchKB 核心架构`

Expected result:
- insertion location is correct
- wording matches the approved spec
- the following section remains unchanged

- [ ] **Step 5: Commit the documentation update**

Run:

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: add agent global cognition entry

Add a CLAUDE.md entry section that gives agents a shared top-level model of the knowledge system while keeping ontology judgment authority centralized in graph-standard.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected result:
- a new commit containing only the `CLAUDE.md` insertion for this change

## Task 2: Sanity-check the final repository state

**Files:**
- Modify: none
- Verify: `CLAUDE.md`

- [ ] **Step 1: Show the diff for the committed change**

Run:

```bash
git show --stat --patch --format=fuller HEAD -- CLAUDE.md
```

Expected result:
- the patch shows only the new `Agent 的全局认知入口` section added to `CLAUDE.md`

- [ ] **Step 2: Confirm no normative scope drift was introduced**

Review the committed diff and confirm:
- no ontology semantics changed
- no workflow section was deleted or rewritten
- no skill routing changed
- the new section only strengthens agent orientation and reading order

Expected result:
- the change stays within the spec’s documentation-only scope

- [ ] **Step 3: Report completion to the user with file and commit reference**

Include:
- updated file path: `CLAUDE.md`
- inserted section name: `Agent 的全局认知入口`
- commit hash and subject line
- note that ontology authority remains in `wiki/ontology/graph-standard.md`

## Self-review

### Spec coverage
- Goal covered by Task 1 Step 2.
- Insertion point covered by Task 1 Step 1 and Step 4.
- Natural transition and anti-duplication requirement covered by Task 1 Step 3.
- Documentation-only scope preservation covered by Task 2 Step 2.

### Placeholder scan
- No `TBD`, `TODO`, or deferred implementation markers remain.
- Commands, text to insert, and verification expectations are explicit.

### Consistency check
- The inserted section name is consistently `Agent 的全局认知入口`.
- The authority file is consistently `wiki/ontology/graph-standard.md`.
- The insertion location is consistently between `## 知识库结构与规范边界` and `## ResearchKB 核心架构`.
