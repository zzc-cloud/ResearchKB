# Ontology Semantic Review Skill Design

日期：2026-05-01

## 1. 目标

为 ResearchKB 增加一个独立的 **ingest 后语义治理 skill**，用于在每次论文摄入之后，对本次新增或修改的知识图谱内容做语义审查。

该 skill 不负责生成知识，也不负责结构存在性检查；它负责判断：

- 新增实体分类是否合理
- 新增关系是否合理
- 新节点在全局本体中的位置是否合理
- 是否存在重复、冲突、伪关系、错误提升/降级
- 是否应做最小修正后再接受本次变更

这将形成一个三段式闭环：

1. `paper-ingest`：生成知识资产
2. `scripts/lint_graph.py`：守住结构底线
3. **新 skill（语义审查）**：守住本体 / 图谱语义质量

## 2. 为什么需要这个 skill

当前 `scripts/lint_graph.py` 已能有效防止结构退化，例如：
- 链接断裂
- 必要节点缺失
- evidence 不完整
- 页面成孤岛

但它无法判断以下更关键的问题：

- survey 是否被错误当作 task
- framework 是否被错误当作 method
- 某条关系是否应该属于 `concept_links` 而不是 `citation_graph`
- 某个概念在全局图谱中的位置是否合理
- 某个上游工作是否应作为方法父节点、文献支撑，还是仅为 evidence 来源

这些问题结构上可能完全“合法”，但语义上是错误的。随着知识库持续增长，如果没有独立语义审查机制，知识图谱会在“结构不坏”的情况下逐渐语义漂移。

## 3. Skill 定位

### 名称建议
- `ontology-semantic-review`
- 备选：`kg-semantic-review`、`knowledge-graph-curator`

推荐名称：**`ontology-semantic-review`**

原因：
- 直接强调其本体治理角色
- 与 `paper-ingest`、`lint_graph.py` 在职责上区分清楚
- 更贴近 ResearchKB 当前的本体化方向

### 触发时机
该 skill 不应对普通问答触发，而应在以下情况强触发：

- 每次 `paper-ingest` 完成后
- 用户要求“检查本次修改是否合理”
- 用户要求“审查本次 ingest 的实体关系是否合理”
- 用户要求“做知识图谱 / 本体语义审查”
- 用户给出 git diff，希望判断新增节点 / 新增关系放置是否正确

### 不应触发的情况
- 只做结构检查（应由 `lint_graph.py` 负责）
- 只做普通论文问答
- 只做跨论文综述写作
- 只读某一页并解释内容含义

## 4. Skill 输入

该 skill 的输入不应是 PDF，而应是：

1. **本次 git diff / 本次修改文件列表**
2. **当前知识库核心规范文件**：
   - `CLAUDE.md`
   - `wiki/ontology/graph-standard.md`
   - `wiki/index.md`
   - `wiki/relations/citation_graph.md`
   - `wiki/relations/method_evolution.md`
   - `wiki/relations/concept_links.md`
   - `wiki/relations/task_method_map.md`
   - `wiki/relations/evidence_index.md`
3. **本次新增/修改的 wiki / intermediate 页面**

该 skill 的关键原则是：
> 只聚焦本次变更涉及的节点和关系，而不是重审整个知识库。

## 5. Skill 核心职责

### 5.1 实体分类合理性检查
判断新增或修改的节点是否被正确分类为：
- Paper
- Method
- Concept
- Framework
- Task
- Scenario
- Benchmark
- Evidence

重点发现：
- survey 被误写成 task
- framework 被误写成 method
- scenario 被误写成 research_task
- benchmark 被误写成 method
- concept 被误挂到错误关系层

### 5.2 关系合理性检查
判断新增关系是否真正属于当前关系文件：
- `citation_graph.md`：论文引用关系
- `method_evolution.md`：方法演化 / 改进关系
- `concept_links.md`：概念之间及概念到任务/场景的关系
- `task_method_map.md`：任务到方法 / 框架 / 场景的映射
- `evidence_index.md`：正式知识页到证据缓存的对应关系

重点发现：
- “论文支撑概念”被误写进 `concept_links`
- survey / framework 的关系被误写成方法演化关系
- 上游文献支撑关系被误当成父方法关系

### 5.3 全局本体位置合理性检查
结合整个知识库判断：
- 该节点是否处于合适层级
- 是否已有更合适的父节点 / 上位节点
- 是否与现有节点重复 / 冲突
- 是否造成新的命名歧义

### 5.4 一致性检查
判断本次变更是否与全局图谱一致：
- 同一节点在不同页面中的身份是否一致
- 同一关系是否在不同文件中冲突表达
- survey / framework / method 是否被不同页面以不同语义理解

## 6. 输出形式

该 skill 应输出一个结构化审查报告，而不是直接修改文件。

建议输出模板：

```markdown
# Semantic Review Report

## Overall verdict
- pass / pass-with-issues / fail

## High-priority issues
- ...

## Medium-priority issues
- ...

## Low-priority issues
- ...

## Suggested fixes
- 指向具体文件与最小修正建议

## Good decisions in this change
- 指出本次修改中做得对的地方

## Final recommendation
- accept / revise-then-accept / reject
```

原则：
- 只聚焦本次变更涉及的节点和关系
- 每个问题尽量指向具体文件
- 每条建议优先给出“最小修正方案”
- 不做泛泛而谈的学术评论

## 7. 与现有体系的关系

### 与 `paper-ingest` 的关系
- `paper-ingest` 负责生成知识资产
- 该 skill 负责审查 `paper-ingest` 的输出是否语义合理

### 与 `lint_graph.py` 的关系
- `lint_graph.py` 守住结构不退化的最低护栏
- 新 skill 守住语义不漂移的质量上限

### 与 `graph-standard.md` 的关系
- `graph-standard.md` 是规则来源
- 新 skill 是规则应用者与偏差识别器

## 8. 推荐工作流

以 `CLAUDE.md` 中的正式工作流和 `graph-standard.md` 中的规则为准；本节仅解释为什么需要语义治理，不重复定义另一套独立流程。

建议未来每次单篇论文摄入后采用：

1. 使用 `paper-ingest` 完成完整摄入
2. 运行 `python3 scripts/lint_graph.py`
3. 若结构通过，再调用 `ontology-semantic-review`
4. 根据审查报告做最小修正
5. 修正后再提交 git

这将使知识库形成：
- 生成
- 结构验证
- 语义验证
- 提交

的完整闭环。

## 9. 最小测试思路

为了验证该 skill 是否真正有价值，建议至少准备 2 个回归案例：

### Case 1：PathMind 方法论文
预期 skill 能识别：
- PathMind 位于方法论文主线合理
- 某些关系属于 method_evolution 而不是 concept_links
- 结构正确且语义大体合理

### Case 2：CPD Survey
预期 skill 能识别：
- `knowledge-graph-survey` 不应当作为 task
- framework 更适合 concept / framework 落点
- survey 论文不应硬套方法论文结构

## 10. 推荐结论

最佳方案不是继续增强 `lint_graph.py` 去做语义判断，而是新增一个独立 skill。

原因：
- 结构检查与语义检查是不同问题
- 二者节奏不同、失败类型不同、输出格式也不同
- 把语义治理做成 skill，能更好结合 diff、本体规则和全局图谱上下文做判断

## 11. 实现接入说明

实现阶段应把该 skill 接入常规工作流：
- 先 `paper-ingest`
- 再 `scripts/lint_graph.py`
- 再 `ontology-semantic-review`
- 最后才决定是否接受并提交改动
