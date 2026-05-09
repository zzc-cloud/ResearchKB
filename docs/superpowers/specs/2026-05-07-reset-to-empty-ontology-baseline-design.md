# Reset to Empty Ontology Baseline Skill Design

## Goal
新增一个专用 skill，把当前 `ontology/` 恢复到**严格空骨架基线**，以便在当前 ResearchKB 结构下反复进行 cold-start ingest / relation / projection / governance 回归测试，而不需要手动清理图谱内容。

## Why the previous design is outdated
本仓库近期已经发生结构重构，原先的 reset-baseline 设计前提已不成立，主要变化包括：

1. 对象域 index 已改为新的导航投影结构：
   - `navigation-entries`
   - `non-serving-placeholders`
2. `paper-ingest` 已内建 cited placeholder 机制：
   - 缺失的 cited paper 会通过 skill 内部脚本补成 placeholder
3. `scripts/lint_graph.py` 已明确校验：
   - 新 index block 结构
   - placeholder 不得进入导航入口
   - raw-sources 只保留 `navigation-entries`
4. 当前空骨架 baseline 必须兼容这些新约束，而不能按旧的 `core-entry / grouped-navigation / canonical-list` 模式定义。

因此 reset-baseline skill 必须以**当前真实结构**为准重新设计。

## Target baseline definition
这里的“严格空骨架基线”定义为：

- 保留 `ontology/` 的必需目录结构中的**知识状态层**
- 保留 `ontology/log.md`（重置为基线日志）
- 保留所有 relation-type ledger 文件：
  - `cites.md`
  - `proposes.md`
  - `based_on.md`
  - `targets_task.md`
  - `uses_concept.md`
  - `evaluated_on.md`
  - `supported_by.md`
  - `sourced_from.md`
- 保留所有对象域 index 文件
- 各对象域 index 使用**当前新版导航结构**：
  - `navigation-entries`
  - `non-serving-placeholders`（raw-sources 例外，仅 `navigation-entries`）
- 不保留任何论文、方法、概念、场景、任务、benchmark、evidence 实例页
- 不保留任何 placeholder paper / method / concept 节点
- 不保留任何 relation ledger 实例边
- 恢复后必须直接通过 `python3 scripts/lint_graph.py`

## Scope
这个 skill 只负责恢复 `ontology/`，不负责：

- 重跑 `paper-ingest`
- 重跑 `relation-reconciliation`
- 重跑 `page-projection-sync`
- 重跑 `index-sync`
- 自动选择下一篇论文进行测试

恢复动作与测试动作解耦，方便你先 reset，再决定跑哪一轮回归。

额外边界：
- 不覆盖 `ontology/graph-standard.md`
- 不覆盖 `CLAUDE.md`
- 不覆盖 `.claude/skills/` 下其他 skill 内容
- reset-baseline 只恢复 `ontology/entities/`、`ontology/relations/` 与 `ontology/log.md` 这类测试相关知识状态层

## Chosen approach
仍然采用**直接覆盖式恢复**，但 baseline 快照内容必须升级为当前结构：

- 在 skill 目录下保存一份 checked-in 的 `baseline/ontology/`
- skill 执行时只覆盖当前 `ontology/entities/`、`ontology/relations/` 与 `ontology/log.md`
- 不触碰 `ontology/graph-standard.md`
- 覆盖后立即运行 `python3 scripts/lint_graph.py`
- 只有 lint 通过，才报告恢复成功

之所以继续选择覆盖式恢复，而不是规则驱动清理：

- 当前 index / placeholder / ledger 规则已明显变复杂
- 手工或规则驱动清理更容易漏掉 block、placeholder 入口或 ledger 文案结构
- 回归测试最需要的是确定性，不是灵活性

## Skill layout
建议新增目录：

- `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/`

### `baseline/ontology/`
这份快照必须是当前结构下的合法空骨架：

- `entities/papers/index.md` 等使用新版导航 block
- `entities/raw-sources/index.md` 只保留 `navigation-entries`
- 所有 relation ledger 只保留关系定义与说明，不含实例边
- 不包含 PathMind 当前重建出来的对象页或 cited placeholder

### `restore_baseline.py`
脚本职责：
1. 检查 baseline 快照是否存在
2. 检查 `ontology/` 下是否有未提交改动
3. 若有改动且未获明确覆盖授权，则中止
4. 若允许覆盖，则删除当前 `ontology/entities/`、`ontology/relations/`，并重置 `ontology/log.md`
5. 从 `baseline/ontology/` 恢复对应内容
6. 保留 `ontology/graph-standard.md` 原样不动
7. 运行 `python3 scripts/lint_graph.py`
8. 输出结构化恢复结果

## Safety model
这是一个高风险覆盖操作，必须保护当前本地图谱工作。

### 默认行为
执行前运行：

```bash
git status --short -- ontology
```

若 `ontology/` 下存在未提交改动：
- 默认返回 `blocked`
- 提示用户当前 ontology 有未提交更改
- 只有用户明确要求覆盖时，skill 才允许继续

### 为什么必须阻断
reset-baseline 用于测试准备，而不是正常知识维护；一旦无提示覆盖，很容易丢失用户当前正在整理的图谱成果。

## Baseline and current index semantics
### Object-domain indexes
所有对象域 index 恢复后都应符合当前语义：

- `navigation-entries`：只放默认 serving-ready 入口
- `non-serving-placeholders`：只放不可导航、仅供图谱解析的 placeholder
- 严格空骨架下，这两个 block 都应为空（raw-sources 除外）

### Raw sources index
`raw-sources/index.md` 是例外：
- 仍保留 `navigation-entries`
- 默认保留受管原始 PDF 入口
- 不引入 `non-serving-placeholders`

这意味着“严格空骨架”并不是“ontology 里完全没有任何导航条目”，而是：
- 没有知识对象实例入口
- 但仍保留 raw source provenance 的受管入口

## Output contract
skill 输出应类似：

```yaml
status: success | blocked | failed
restored_from: .claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/
lint: pass | fail
warnings: []
manual_followups: []
```

### 状态定义
- `success`：已恢复，且 lint 通过
- `blocked`：因未提交改动或缺少覆盖确认而中止
- `failed`：恢复动作或 lint 失败

## Refresh policy for baseline snapshot
因为 `ontology/` 结构和 lint 规则会继续演化，这份 baseline 快照不是永久不变的。

需要明确：
- 每当 `scripts/lint_graph.py`、对象域 index 模板、placeholder 策略或 relation ledger 结构发生变动后，baseline 都可能需要更新
- 更新 baseline 后，必须单独运行一次 `python3 scripts/lint_graph.py` 验证这份快照本身仍是合法空骨架

## Recommended implementation direction
下一步实现不应沿用旧 plan，而要围绕当前结构重新落地：

2. 再创建与当前结构一致的 baseline snapshot
3. 再实现 restore script
4. 再补 skill contract
5. 最后跑：
   - `python3 scripts/lint_graph.py`

## Success criteria
当这个 skill 实现完成后，你应能稳定做到：

1. 运行 reset-baseline skill
2. `ontology/` 被恢复为当前结构下的严格空骨架
3. `python3 scripts/lint_graph.py` 立即通过
4. 接着再用任意单篇 PDF 重新执行 cold-start 测试
