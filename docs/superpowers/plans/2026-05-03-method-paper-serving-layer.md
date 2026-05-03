# Method/Paper Serving Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert Method and Paper pages into governed serving pages for constrained QA while keeping `wiki/relations/` as governance truth and moving default QA runtime reads onto entity pages.

**Architecture:** Update ontology/docs rules first, then add a normalized `Formal relations` serving surface for Method/Paper pages, then upgrade `scripts/lint_graph.py` so governance validates projection consistency, completeness, and QA consumability. Finally, migrate a small sample set (`PathMind`, `RoG`, and the PathMind paper) to prove QA can traverse governed object pages without reading `wiki/relations/` by default.

**Tech Stack:** Markdown knowledge pages, Python 3 (`scripts/lint_graph.py`), ripgrep-style repository conventions, existing ResearchKB ontology/relation ledger structure.

---

## File map

### Documentation and governance rules
- Modify: `wiki/ontology/index.md`
  - Clarify serving-layer vs governance-layer entrypoints.
- Modify: `wiki/ontology/graph-standard.md`
  - Define truth-layer vs serving-layer separation, Method/Paper projection rules, `Formal relations` requirements, and QA consumption rules.
- Modify: `CLAUDE.md`
  - Update default QA workflow so governed object pages are the default runtime surface while `wiki/relations/` remains governance truth.

### Sample serving pages
- Modify: `wiki/methods/PathMind.md`
  - Add `Formal relations` section and align human-readable sections with serving model.
- Modify: `wiki/methods/RoG.md`
  - Add `Formal relations` section and fill minimal serving-friendly relation structure.
- Modify: `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
  - Add `Formal relations` section and align relation grouping with serving model.

### Governance code
- Modify: `scripts/lint_graph.py`
  - Add serving-layer validation helpers and checks for Method/Paper pages.

### Test/verification surface
- Test: `python3 scripts/lint_graph.py`
- Test: targeted `python3 - <<'PY' ... PY` smoke checks for relation projection parsing during development

---

### Task 1: Update ontology index serving entry rules

**Files:**
- Modify: `wiki/ontology/index.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Edit the QA/gov navigation copy in `wiki/ontology/index.md`**

Replace the current task-entry guidance with copy that distinguishes QA entrypoints from governance entrypoints:

```markdown
## 4. 按任务进入
- 想做受约束知识问答 → 先定位对应 `wiki/papers/` 或 `wiki/methods/` 对象页，再按页面中的 Formal relations 区块扩展；需要证据时下钻 `intermediate/papers/`
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式对象知识 → 对应 `wiki/` 对象页
- 想看治理用正式关系账本 → `wiki/relations/`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `docs/`

## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → `wiki/relations/` → 具体对象页 → `intermediate/papers/`

### 回答知识问题
`wiki/` 对象页（优先 `wiki/methods/` / `wiki/papers/`）→ Formal relations 区块 → `intermediate/papers/` → 必要时治理账本

### 治理知识变更
[[graph-standard]] → `wiki/relations/` → 变更对象页 → `intermediate/papers/`
```

- [ ] **Step 2: Run lint to verify index text still satisfies current repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the index update**

```bash
git add wiki/ontology/index.md
git commit -m "docs: redefine ontology QA entrypoints"
```

---

### Task 2: Update graph standard for serving-layer semantics

**Files:**
- Modify: `wiki/ontology/graph-standard.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-layer rules after the instance-edge sections**

Insert a new section after `## 实例边维护规则` with this content:

```markdown
## 治理真源层与服务层
- `wiki/relations/` 继续作为正式实例边的治理真源，用于 authoring、lint、语义审查、补边与修复。
- `wiki/methods/` 与 `wiki/papers/` 在治理通过后，作为受约束知识问答的默认服务层。
- `intermediate/papers/` 继续作为证据层，用于机制、实验、引用、基线与 provenance 核验。
- 问答运行时默认先读治理后的对象页，不再把 `wiki/relations/` 作为默认读取层；但治理与修复仍以 `wiki/relations/` 为准。

## Method / Paper 服务层投影规则
- Method / Paper 页必须同时包含：frontmatter、面向人类的关系区块、`## Formal relations` 规范化关系区块。
- frontmatter 只承载紧凑结构化摘要，不承担手写关系真源职责；其派生字段必须来自正式关系账本。
- `parent_methods` / `child_methods` 继续作为首批强一致派生字段，必须与 `wiki/relations/method_evolution.md` 保持一致。
- 面向人类的关系区块可按对象视角摘要组织，但不得与正式关系账本冲突。
- `## Formal relations` 必须覆盖该实体的一跳正式关系投影，作为问答时的正式关系读取面。

## Formal relations 区块规范
- 区块标题固定为 `## Formal relations`。
- 必须包含 `### Outgoing` 与 `### Incoming` 两个子区块；无内容时也应显式写 `- 无`。
- 每条关系使用 canonical 三元组格式：`- `[[Source Node]] --relation_type--> [[Target Node]]``。
- 每条关系至少附带一个 `- evidence: [[证据页]]` 行；必要时可补 `- note:`，但应避免 prose 污染区块。
- 该区块供问答时的受约束拓扑探索直接消费，不以综述性表达代替。

## 问答消费规则
- 受约束知识问答默认先定位关键实体，再读取治理后的 Method / Paper 页。
- 问答默认基于对象页 frontmatter 与 `## Formal relations` 做一跳扩展，而不是先扫描 `wiki/relations/`。
- 若需核验机制、实验、引用、基线或 provenance，再下钻 `intermediate/papers/`。
- `wiki/relations/` 默认留在治理、修复、审计链路中，不作为问答默认读取层。

## 服务层治理校验要求
- 除结构合法性外，还必须校验 Method / Paper 页的投影一致性、投影完备性与问答可消费性。
- 投影一致性：frontmatter 派生字段、`## Formal relations` 与正式关系账本一致；人类关系区块不得冲突。
- 投影完备性：属于该实体的一跳正式关系，必须按规则投影到 `## Formal relations`；指定派生字段必须回填到 frontmatter。
- 问答可消费性：页面必须存在稳定的 `## Formal relations`、`### Outgoing`、`### Incoming` 结构，以及可回溯 evidence 入口。
```

- [ ] **Step 2: Update the Method skeleton and standard sections to include the serving surface**

Edit the Method section so the standard body structure becomes:

```markdown
正文标准结构：
- 方法定义
- 解决的核心问题
- 技术原理
- 方法演化位置
- 应用场景
- 代表论文
- 相关概念
- 证据来源
- Formal relations
- 优势与局限
- 与其他方法的对比
```

- [ ] **Step 3: Update the Paper standard body structure to include the serving surface**

Edit the Paper section so the standard body structure becomes:

```markdown
正文标准结构：
- 核心问题
- 主要贡献
- 核心方法
- 应用场景
- 关键结论
- 引用了哪些重要工作
- 被哪些论文引用（已知）
- 与知识库其他内容的关联
- 证据来源
- Formal relations
- 我的批注
```

- [ ] **Step 4: Rewrite the instance-edge guidance so pages are serving projections rather than informal helpers**

Replace the current copy under `## 实例边层` with:

```markdown
## 实例边层
- 实例边（instance edge）是两个具体知识节点之间的显式关系记录，不等同于关系类型定义本身。
- `wiki/relations/` 是正式维护实例边账本的唯一治理真源。
- Method / Paper 页中的 `## Formal relations` 是治理通过后、从实例边账本投影出的默认问答读取面。
- 节点页中的自然语言说明、`[[wikilink]]` 与综述性表述可以辅助理解，但不能替代正式实例边账本；其 serving 有效性依赖治理对投影的一致性与完备性校验。
- 查询、分析、拓扑探索与后续图谱扩展，应优先依据治理后的正式关系读取面；在治理、修复、审计场景下再回到账本。
```

- [ ] **Step 5: Run lint to verify the graph standard edits do not break existing structural checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the graph standard update**

```bash
git add wiki/ontology/graph-standard.md
git commit -m "docs: define serving-layer ontology rules"
```

---

### Task 3: Update CLAUDE.md workflow rules for object-page-first QA

**Files:**
- Modify: `CLAUDE.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the layer-priority bullets in `CLAUDE.md`**

Update the `### 基本原则` block to:

```markdown
### 基本原则
- 正式知识问答默认优先看治理后的 `wiki/` 对象页（当前优先 `wiki/papers/`、`wiki/methods/`）
- 正式关系治理与修复优先看 `wiki/relations/`
- 论文细节、实验、引用与机制优先看 `intermediate/papers/`
- 原始 PDF 仅在必要时回源，不作为默认工作入口
```

- [ ] **Step 2: Update the default information-layer bullets for user questions**

Replace item 4 under `## 面向用户问题的默认认知方式` with:

```markdown
4. **需要哪些信息层**
   - `wiki/ontology/index.md` 定位导航入口
   - 治理后的 `wiki/` 正式对象页（当前优先 `wiki/papers/`、`wiki/methods/`）承载默认问答服务层
   - `wiki/relations/` 用于正式关系治理、修复与审计
   - `intermediate/papers/` 核验证据
   - `raw/` 仅在必要时回源
```

- [ ] **Step 3: Update the query-order and QA-answering rules**

Replace the `## 查询与分析默认顺序` list and the QA bullets with:

```markdown
## 查询与分析默认顺序

当用户提问知识库内容时，默认按以下顺序：

1. 读取 `wiki/ontology/index.md` 定位导航入口
2. 锁定关键实体并读取治理后的 `wiki/` 正式对象页（当前优先 `wiki/papers/`、`wiki/methods/`）
3. 基于对象页中的 `Formal relations` 区块做受约束拓扑扩展
4. 如涉及机制、实验、引用、基线或 provenance 核验，读取 `intermediate/papers/`
5. 如处于治理、修复、审计场景，或需核对投影真源，再读取 `wiki/relations/`
6. 必要时才回看 `raw/`
7. 回答时区分：
   - 正式知识结论
   - 证据缓存结论
   - 治理账本结论（仅在实际查询 relation ledger 时）
   - 待核验推断

回答知识库问题时：
- 默认把治理后的正式对象页作为正式问答服务层来源。
- 必要时读取 `intermediate/papers/` 做证据核验。
- 仅在治理、修复、审计或真源核对场景下读取 `wiki/relations/`。
- 回答中必须区分：正式知识结论、证据缓存结论、治理账本结论（若使用）、待核验推断。
- 若属于探索发现，不要把候选知识伪装成正式事实。
```

- [ ] **Step 4: Update the “查询与分析” and anti-pattern language**

Replace the `### 查询与分析` bullets and the relevant anti-pattern bullet with:

```markdown
### 查询与分析
当我提问知识库内容时：
- 先做本体判定
- 再定位关键实体并读取治理后的正式对象页
- 默认基于 `Formal relations` 做受约束扩展，并在需要时核验证据
- 仅在治理、修复、审计或真源核对场景下查看 `wiki/relations/`
- 回答时说明依据来源
```

```markdown
- 把治理账本读取流程机械套用到所有问答，而忽略治理后的对象页 serving 入口
```

- [ ] **Step 5: Run lint to verify CLAUDE.md still satisfies repository checks**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the workflow update**

```bash
git add CLAUDE.md
git commit -m "docs: shift QA workflow to governed object pages"
```

---

### Task 4: Add Formal relations to `wiki/methods/PathMind.md`

**Files:**
- Modify: `wiki/methods/PathMind.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Replace the evolution/scenario/representative sections with serving-friendly grouped relations**

Update the middle of `wiki/methods/PathMind.md` so these sections read:

```markdown
## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：[[PathMind]] 在路径导向路线中引入“重要路径”优先级学习，以减少噪声并降低调用成本。
- 相关上游参考：[[RoG]]、[[GCR]]、[[EPERM]]

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]

## 代表论文
- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]（提出此方法）
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]（路径推理基线）
- [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]（证据路径增强基线）

## 相关概念
- [[路径优先化]]
- [[重要推理路径]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/PathMind.sections|PathMind.sections]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]

## Formal relations
### Outgoing
- `[[PathMind]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --uses_concept--> [[重要推理路径]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --applies_to--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
```

- [ ] **Step 2: Verify `parent_methods` remains aligned with the formal edge projection**

Confirm the frontmatter remains:

```yaml
parent_methods: [路径导向知识图谱推理]
child_methods: []
```

No code change is needed if it already matches.

- [ ] **Step 3: Run lint to verify the serving page remains structurally valid**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit the PathMind method serving update**

```bash
git add wiki/methods/PathMind.md
git commit -m "docs: add formal relations to PathMind method page"
```

---

### Task 5: Add Formal relations to `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`

**Files:**
- Modify: `wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Reshape the knowledge-linking block into serving-friendly grouped sections**

Replace `## 与知识库其他内容的关联` and `## 证据来源` tail content with:

```markdown
## 与知识库其他内容的关联
- 提出的方法：[[methods/PathMind|PathMind（方法）]]
- 核心概念：[[路径优先化]]、[[重要推理路径]]
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]
- 评测基准：[[WebQSP]]、[[CWQ]]
- 关键引用对象：[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]、[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]、[[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]、[[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]、[[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]、[[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]

## 证据来源
- 结构化章节缓存：[[intermediate/papers/PathMind.sections|PathMind.sections]]
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]
- 实验缓存：[[intermediate/papers/PathMind.experiments|PathMind.experiments]]

## Formal relations
### Outgoing
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --uses_concept--> [[路径优先化]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --uses_concept--> [[重要推理路径]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --applies_to--> [[知识图谱推理问答]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.sections|PathMind.sections]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.experiments|PathMind.experiments]]`
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]]
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --supported_by--> [[intermediate/papers/PathMind.refs|PathMind.refs]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- 无
```

- [ ] **Step 2: Run lint to verify the paper page remains valid after the serving projection is added**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 3: Commit the PathMind paper serving update**

```bash
git add "wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md"
git commit -m "docs: add formal relations to PathMind paper page"
```

---

### Task 6: Add Formal relations to `wiki/methods/RoG.md`

**Files:**
- Modify: `wiki/methods/RoG.md`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Expand the RoG method page into the serving-page shape**

Replace the current body with:

```markdown
## 方法定义
一种显式生成关系推理路径以支持知识图谱忠实推理的方法。

## 解决的核心问题
RoG 通过把关系路径显式建模为中间推理结构，提升知识图谱推理的忠实性与可解释性。

## 技术原理
RoG 先围绕问题构造可候选的关系推理路径，再让语言模型沿显式路径完成推理与答案生成，从而避免完全隐式的黑箱推断。

## 方法演化位置
- 上游方法：[[路径导向知识图谱推理]]
- 路线改进：将关系路径作为中间推理结构显式生成。
- 对后续工作的影响：[[PathMind]] 将其作为路径导向基线和上游参考之一。

## 应用场景
- 主要场景：[[知识图谱推理问答]]
- 相关任务：[[knowledge-graph-reasoning]]、[[kgqa]]、[[multi-hop-qa]]

## 代表论文
- [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]

## 相关概念
- 无

## 证据来源
- 引用与基线缓存：[[intermediate/papers/PathMind.refs|PathMind.refs]]

## Formal relations
### Outgoing
- `[[RoG]] --based_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --improves_on--> [[路径导向知识图谱推理]]`
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]]
- `[[RoG]] --targets_task--> [[knowledge-graph-reasoning]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --targets_task--> [[kgqa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
- `[[RoG]] --targets_task--> [[multi-hop-qa]]`
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]

### Incoming
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`
  - note: 该 incoming 边作用于 RoG 的代表论文页而非方法节点，当前方法页不维护跨类型镜像。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]]
```

- [ ] **Step 2: Correct the incoming section to avoid projecting a paper-edge onto the method node**

Immediately replace the `### Incoming` block with the correct version:

```markdown
### Incoming
- 无
```

This step ensures the final page only contains true incoming edges for the Method node.

- [ ] **Step 3: Run lint to verify the stub method still passes repository checks after expansion**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 4: Commit the RoG method serving update**

```bash
git add wiki/methods/RoG.md
git commit -m "docs: add formal relations to RoG method page"
```

---

### Task 7: Upgrade `scripts/lint_graph.py` with serving-layer validation helpers

**Files:**
- Modify: `scripts/lint_graph.py`
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Add serving-page configuration constants near the top of `scripts/lint_graph.py`**

Insert these constants after `PLACEHOLDER_PAPERS`:

```python
SERVING_PAGES = {
    'wiki/methods/PathMind.md': {
        'node': 'PathMind',
        'node_type': 'Method',
        'required_headings': [
            '## 相关概念',
            '## 证据来源',
            '## Formal relations',
            '### Outgoing',
            '### Incoming',
        ],
        'expected_frontmatter': {
            'parent_methods': ['路径导向知识图谱推理'],
            'child_methods': [],
        },
        'required_edges': [
            ('PathMind', 'based_on', '路径导向知识图谱推理'),
            ('PathMind', 'improves_on', '路径导向知识图谱推理'),
            ('PathMind', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind', 'targets_task', 'kgqa'),
            ('PathMind', 'targets_task', 'multi-hop-qa'),
            ('PathMind', 'uses_concept', '路径优先化'),
            ('PathMind', 'uses_concept', '重要推理路径'),
            ('PathMind', 'applies_to', '知识图谱推理问答'),
            ('PathMind', 'evaluated_on', 'WebQSP'),
            ('PathMind', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
        ],
    },
    'wiki/methods/RoG.md': {
        'node': 'RoG',
        'node_type': 'Method',
        'required_headings': [
            '## 解决的核心问题',
            '## 技术原理',
            '## 相关概念',
            '## 证据来源',
            '## Formal relations',
            '### Outgoing',
            '### Incoming',
        ],
        'expected_frontmatter': {
            'parent_methods': ['路径导向知识图谱推理'],
            'child_methods': [],
        },
        'required_edges': [
            ('RoG', 'based_on', '路径导向知识图谱推理'),
            ('RoG', 'improves_on', '路径导向知识图谱推理'),
            ('RoG', 'targets_task', 'knowledge-graph-reasoning'),
            ('RoG', 'targets_task', 'kgqa'),
            ('RoG', 'targets_task', 'multi-hop-qa'),
        ],
    },
    'wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md': {
        'node': 'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models',
        'node_type': 'Paper',
        'required_headings': [
            '## 证据来源',
            '## Formal relations',
            '### Outgoing',
            '### Incoming',
        ],
        'expected_frontmatter': {},
        'required_edges': [
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'kgqa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'multi-hop-qa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '路径优先化'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '重要推理路径'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'applies_to', '知识图谱推理问答'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'WebQSP'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Model Reasoning', 'cites', 'An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.sections|PathMind.sections'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.experiments|PathMind.experiments'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.refs|PathMind.refs'),
        ],
    },
}

FORMAL_RELATION_RE = re.compile(r"- `\[\[(?P<src>[^\]]+)\]\] --(?P<rel>[^`]+)--> \[\[(?P<dst>[^\]]+)\]\]`")
FRONTMATTER_FIELD_RE = re.compile(r'^(?P<key>[a-z_]+):\s*(?P<value>.+)$', re.MULTILINE)
```

- [ ] **Step 2: Add parsing helpers below `read_text()`**

Insert these helpers after `def read_text(rel: str) -> str:`:

```python
def split_frontmatter(text: str) -> tuple[dict[str, list[str] | str], str]:
    if not text.startswith('---\n'):
        return {}, text
    _, rest = text.split('---\n', 1)
    frontmatter_block, body = rest.split('\n---\n', 1)
    data: dict[str, list[str] | str] = {}
    for match in FRONTMATTER_FIELD_RE.finditer(frontmatter_block):
        key = match.group('key')
        raw = match.group('value').strip()
        if raw.startswith('[') and raw.endswith(']'):
            inner = raw[1:-1].strip()
            data[key] = [] if not inner else [part.strip() for part in inner.split(',')]
        else:
            data[key] = raw
    return data, body


def extract_formal_relations(text: str) -> list[tuple[str, str, str]]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    edges: list[tuple[str, str, str]] = []
    for match in FORMAL_RELATION_RE.finditer(formal_block):
        edges.append((match.group('src'), match.group('rel'), match.group('dst')))
    return edges


def require_serving_page(rel: str, rules: dict[str, object]) -> list[str]:
    text = read_text(rel)
    frontmatter, _body = split_frontmatter(text)
    page_errors: list[str] = []
    for heading in rules['required_headings']:
        if heading not in text:
            page_errors.append(f'missing serving heading {heading} in {rel}')
    for key, expected in rules['expected_frontmatter'].items():
        actual = frontmatter.get(key)
        if actual != expected:
            page_errors.append(f'frontmatter mismatch for {key} in {rel}: expected {expected!r}, got {actual!r}')
    actual_edges = set(extract_formal_relations(text))
    for edge in rules['required_edges']:
        if edge not in actual_edges:
            page_errors.append(f'missing formal relation {edge} in {rel}')
    return page_errors
```

- [ ] **Step 3: Add serving-page validation into the main lint flow**

Insert this loop before the final `if errors:` block:

```python
for rel, rules in SERVING_PAGES.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing serving page: {rel}')
        continue
    errors.extend(require_serving_page(rel, rules))
```

- [ ] **Step 4: Fix the accidental long-title typo in the Paper `required_edges` configuration**

In the just-added `SERVING_PAGES` constant, replace this tuple:

```python
('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Model Reasoning', 'cites', 'An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering'),
```

with:

```python
('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering'),
```

- [ ] **Step 5: Run lint to verify the new serving checks pass on the migrated pages**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 6: Commit the lint upgrade**

```bash
git add scripts/lint_graph.py
git commit -m "feat: validate serving-layer page projections"
```

---

### Task 8: Final end-to-end verification

**Files:**
- Modify: none
- Test: `python3 scripts/lint_graph.py`

- [ ] **Step 1: Run the full governance check from a clean working tree state**

Run: `python3 scripts/lint_graph.py`
Expected: `PASS: graph lint succeeded`

- [ ] **Step 2: Inspect the final diff to verify scope is limited to the planned files**

Run: `git diff -- wiki/ontology/index.md wiki/ontology/graph-standard.md CLAUDE.md wiki/methods/PathMind.md wiki/methods/RoG.md "wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" scripts/lint_graph.py`
Expected: diff only in the seven planned files and no unrelated file edits

- [ ] **Step 3: Commit the final integration checkpoint if any verification-only fixes were needed**

```bash
git status --short
```

Expected: no unstaged fixes remain. If verification revealed issues and you changed files, then commit them with:

```bash
git add wiki/ontology/index.md wiki/ontology/graph-standard.md CLAUDE.md wiki/methods/PathMind.md wiki/methods/RoG.md "wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md" scripts/lint_graph.py
git commit -m "chore: finalize serving-layer rollout"
```

If no verification-only fixes were needed, do not create an extra commit.
