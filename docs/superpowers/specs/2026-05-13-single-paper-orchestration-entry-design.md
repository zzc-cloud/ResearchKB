# Single-paper orchestration entrypoint for ResearchKB

## Context

ResearchKB 目前已经形成了明确的单篇论文编译链：

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

这条链路目前主要通过 `CLAUDE.md` 的文字约束来表达，并由各阶段 skill 在自身文档中部分承接后续调用语义。实际运行中暴露出两个问题：

1. **默认入口不够强**：当用户说“处理论文：...”时，系统虽然能从 `CLAUDE.md` 读到应执行完整链路，但缺少一个单独的执行入口 skill 来稳定承接该意图，因此仍可能误触发与论文处理无关的通用 skill。
2. **编排语义分散**：多个子 skill 内部带有“本阶段之后默认继续进入下一个阶段”的说明，导致编排逻辑散落在 `paper-ingest`、`relation-reconciliation`、`page-projection-sync` 等阶段 skill 中。这样会形成双重甚至多重执行真源，不利于维护，也会让 `CLAUDE.md` 与 skill 合约之间出现漂移风险。

因此需要把“处理单篇论文”的默认执行入口集中到一个编排型 skill，同时把 `CLAUDE.md` 改写为“规范入口 + 链路契约”的表达方式，并清理子 skill 中原本承接编排层的内容。

## Goal

新增一个单篇论文编排型 skill，作为用户说“处理论文：...”时的默认统一入口；同时调整 `CLAUDE.md` 与现有阶段 skill，使：

- `CLAUDE.md` 保持规范真源地位
- 编排型 skill 成为默认执行入口
- 各阶段子 skill 退回为明确的阶段性能力，不再各自承担整条链路的编排职责
- 阶段之间的信息交接通过仓库正式产物与结构化阶段摘要完成，而不是依赖临时自然语言上下文

## Non-goals

- 不重写各阶段 skill 的领域核心逻辑
- 不改变现有单篇论文正式编译链的阶段顺序
- 不把批量处理也一并改造成新的 batch orchestrator skill（本次只统一单篇论文入口）
- 不新增新的 ontology relation / object 语义规则
- 不把 lint、semantic review、serving review 变成写仓库内容的阶段

## Design summary

### Recommended approach

采用“**规范层与执行层分离**”的方案：

1. 新增编排型 skill（推荐名：`process-paper`）
2. 将 `CLAUDE.md` 中“处理单篇论文”改写为：
   - 默认入口说明
   - 必须满足的链路契约
   - 完成判定
   - direct subskill 的例外边界
3. 调整现有阶段 skill 的 `name/description/boundary`，删除其中属于编排层的内容，仅保留阶段职责、输入前提、正式产物与结构化输出要求
4. 在编排型 skill 中显式加入“阶段交接合同”，用仓库正式产物与结构化摘要检查是否可进入下一阶段

这是最稳妥的方案，因为它既避免了仅靠文档描述链路的不稳定，也避免了 skill 与 `CLAUDE.md` 同时各写一套完整编排说明的双真源问题。

## 1. New orchestrator skill

### 1.1 Name

新增 skill 目录：

- `.claude/skills/process-paper/`

前端展示名建议同样为：

- `process-paper`

原因：
- 与用户自然语言“处理论文”高度贴近
- 比 `single-paper-orchestrator` 之类技术化名称更利于触发
- 便于未来扩展 batch 版本，例如 `process-paper-batch`

### 1.2 Trigger scope

该 skill 应在以下情形默认触发：

- 用户说“处理论文：...”
- 用户说“摄入论文：...”且语义上是在请求完整单篇论文编译链
- 用户给出单篇 PDF 路径并希望完成完整落库，而不是只做某一阶段

该 skill 不应抢夺以下情形：

- 用户明确要求只做 `paper-ingest`
- 用户明确要求只做 `relation-reconciliation`
- 用户明确要求只做 `page-projection-sync`
- 用户明确要求只跑 `index-sync`
- 用户明确要求只做 `ontology-semantic-review` 或 `serving-governance-review`

也就是说，**默认统一入口，但允许用户显式直达局部阶段**。

### 1.3 Responsibilities

`process-paper` 只承担三类职责：

1. **入口职责**
   - 识别“处理单篇论文”的完整编译意图
2. **编排职责**
   - 依次调用现有阶段 skill / 命令
3. **阶段交接验收职责**
   - 检查上一步是否已产出足够的正式产物与结构化摘要，以决定能否进入下一阶段

它不重写 `paper-ingest`、`relation-reconciliation` 等 skill 的领域抽取或治理逻辑。

## 2. Stage-to-stage information handoff

### 2.1 Principle

子 skill 之间的信息交互不应被设计为“skill 共享临时内存”或“依赖自然语言总结继续传话”。

统一原则是：

- **仓库正式产物是真源**
- **结构化阶段摘要是控制面**

也就是说，编排型 skill 既要读取每一阶段写回仓库的正式位置，也要读取该阶段在回复结尾给出的结构化摘要字段，以此做下一阶段的准入判断。

### 2.2 Repository truth by stage

#### paper-ingest writes

`paper-ingest` 阶段的正式写入位置包括：

- `ontology/entities/evidence/<short_name>.sections.md`
- `ontology/entities/evidence/<short_name>.refs.md`
- `ontology/entities/evidence/<short_name>.experiments.md`
- `ontology/entities/evidence/<short_name>.analysis.md`
- `ontology/entities/papers/<paper>.md`
- 必要时的 `ontology/entities/methods/*.md`
- 必要时的 `ontology/entities/tasks/*.md`
- 必要时的 `ontology/entities/scenarios/*.md`
- 必要时的 `ontology/entities/benchmarks/*.md`
- 必要时的 `ontology/entities/papers/*.md` placeholder / representative paper stub
- `ontology/log.md`

它的结构化摘要仍保留，例如：

- `status`
- `generated_caches`
- `updated_pages`
- `relation_candidates`
- `relation_exemptions`
- `warnings`
- `paper_human_friendly_payloads`
- `method_human_friendly_payloads`

#### relation-reconciliation writes

`relation-reconciliation` 的正式写入位置包括：

- `ontology/relations/cites.md`
- `ontology/relations/proposes.md`
- `ontology/relations/surveys_method.md`
- `ontology/relations/based_on.md`
- `ontology/relations/references_method.md`
- `ontology/relations/targets_task.md`
- `ontology/relations/applied_in.md`
- `ontology/relations/evaluated_on.md`
- `ontology/relations/supported_by.md`
- `ontology/relations/sourced_from.md`
- 必要时为 formal closure materialize 的 `ontology/entities/methods/*.md`
- 必要时为 paper anchor materialize 的 `ontology/entities/papers/*.md`

结构化摘要仍保留，例如：

- `status`
- `added`
- `already_present`
- `exempt`
- `needs-human-review`
- `affected_pages`

#### page-projection-sync writes

`page-projection-sync` 只写对象层与 evidence 层：

- `ontology/entities/papers/*.md`
- `ontology/entities/methods/*.md`
- `ontology/entities/tasks/*.md`
- `ontology/entities/scenarios/*.md`
- `ontology/entities/benchmarks/*.md`
- `ontology/entities/evidence/*.md`

写回内容包括：

- `Formal relations`
- 强一致 frontmatter
- 模板化关系区块
- survey-derived partial Method 的 representative paper 人类可读锚点

结构化摘要仍保留，例如：

- `status`
- `projected_pages`
- `skipped_pages`
- `manual_followups`

#### index-sync writes

`index-sync` 只写导航层：

- `ontology/entities/papers/index.md`
- `ontology/entities/methods/index.md`
- `ontology/entities/tasks/index.md`
- `ontology/entities/scenarios/index.md`
- `ontology/entities/benchmarks/index.md`
- `ontology/entities/evidence/index.md`
- 其他显式受管导航页

结构化摘要仍保留，例如：

- `status`
- `synced_indexes`
- `skipped_pages`
- `manual_followups`

#### lint / semantic review / serving review

以下阶段默认不写仓库内容：

- `python3 scripts/lint_graph.py`
- `ontology-semantic-review`
- `serving-governance-review`

它们只返回结构化判定，例如：

- `pass / failed / blocked`
- `findings`
- `needs_fixes`

### 2.3 Handoff contract

编排型 skill 需要在每个阶段之间执行最小交接验收：

#### ingest → reconciliation
至少检查：
- target paper page 已存在或已更新
- 最小 evidence cache 集合已存在
- 摘要中存在 `relation_candidates`
- `status` 不是阻塞态

#### reconciliation → projection
至少检查：
- formal relation ledgers 已实际写入
- 摘要中存在 `affected_pages`
- `status` 允许继续

#### projection → index
至少检查：
- 受影响对象页已完成 formal projection
- 摘要中存在 `projected_pages`

#### index → lint/reviews
至少检查：
- 摘要中存在 `synced_indexes` 或明确 `skipped_pages`
- 没有阻塞态

#### governance progression
- lint 必须通过，才能继续 semantic review
- semantic review 若出现 blocking finding，则不得进入 serving-ready 完成态
- serving governance 不通过，则整条链不得宣称“正式入图完成”

## 3. CLAUDE.md changes

### 3.1 What should change

`CLAUDE.md` 中“### 处理单篇论文”不应继续直接承担完整执行编排说明，而应改写为：

1. **默认入口说明**
   - 当用户说“处理论文：[文件路径或论文标题]”时，默认调用 `process-paper` 编排型 skill
2. **链路契约**
   - `process-paper` 必须完成：
     1. `paper-ingest`
     2. `relation-reconciliation`
     3. `page-projection-sync`
     4. `index-sync`
     5. `python3 scripts/lint_graph.py`
     6. `ontology-semantic-review`
     7. `serving-governance-review`
3. **完成判定**
   - 只有结构 lint、本体语义审查与 serving 治理全部通过，才算正式入图完成
4. **局部阶段例外边界**
   - 用户明确要求某一局部阶段时，允许直接调用对应阶段 skill

### 3.2 What should stay in CLAUDE.md

以下内容应继续保留在 `CLAUDE.md` 中，而不是迁入 orchestrator：

- 本体认知
- 分层入口说明
- 批量处理的原则约束
- 查询 / 分析路径
- 执行原则
- 规范优先级说明
- 单篇论文编译链的最终完成判定

也就是说，`CLAUDE.md` 仍然是**规范真源**，只是从“直接执行编排文本”调整为“入口与契约真源”。

### 3.3 Batch section adjustment

“### 批量处理论文”建议轻微改写，使其与新的单篇入口一致：

- 批量处理仍以单篇论文编排型 skill 为基本执行单元
- 不允许只批量跑 `paper-ingest` 而跳过后续 relation / projection / index sync / 治理阶段

本次不新增 batch orchestrator，但 `CLAUDE.md` 应先与未来该方向兼容。

## 4. Existing child skill cleanup

### 4.1 Cleanup rule

现有阶段 skill 中，凡属于“整条链路如何继续往下调用”的内容，都应删除或缩减；凡属于“本阶段自己做什么、写什么、输出什么”的内容，应保留。

### 4.2 What to remove

应从子 skill 中删除的典型内容：

- “本 skill 完成后默认进入下一个 skill”
- “日常流程中必须继续调用 X / Y / Z”
- “这是处理论文默认完整入口”
- “只有整条链全部跑完才算正式完成”
- 其他跨多个阶段的编排说明

这些逻辑应统一上收给 `process-paper`。

### 4.3 What to keep

应保留在子 skill 中的内容：

- 阶段输入前提
- 阶段内部逻辑
- 阶段正式产物写入位置
- 阶段结构化摘要格式
- 本阶段自己的 `success / partial / blocked / needs-human-review` 判定
- 下一阶段将消费哪些产物，但不再负责触发它

## 5. Child skill metadata changes

### 5.1 Names

现有阶段 skill 名称建议**暂不重命名**：

- `paper-ingest`
- `relation-reconciliation`
- `page-projection-sync`
- `index-sync`
- `ontology-semantic-review`
- `serving-governance-review`

理由：
- 它们的阶段含义已经清晰
- 改名成本高，会带来额外触发迁移问题
- 真正需要提升触发直觉的是新的入口 skill，而不是已有阶段 skill

### 5.2 Descriptions

这些子 skill 的 description 需要统一改写为“**阶段性能力 + 默认由 orchestrator 调用 + 用户可显式直调**”。

例如：

- `paper-ingest`：用于单篇论文编译链中的 ingest 阶段；默认由 `process-paper` 调用；仅当用户明确要求只做 ingest / 初步落库时直接调用。
- `relation-reconciliation`：用于 formal relation ledger 补齐阶段；默认由 `process-paper` 调用；当用户明确要求只做 relation ledger 修复时直接调用。
- `page-projection-sync`：用于将 formal ledger 投影回对象页；默认由 `process-paper` 调用；当用户明确要求刷新对象页 formal projection 时直接调用。
- `index-sync`：用于更新对象域 index 与受管导航页；默认由 `process-paper` 调用；当用户明确要求刷新导航投影时直接调用。
- `ontology-semantic-review` / `serving-governance-review`：保留独立治理审查入口，同时说明其在完整单篇论文处理链中通常由 `process-paper` 在后置阶段统一调度。

## 6. Failure handling

`process-paper` 的失败语义应明确：

- 任一步若返回阻塞态，则停止后续阶段
- 不允许跳过 relation / projection / index / governance 后仍宣称完成
- `paper-ingest` 若输出 `partial` 或 `needs-skill-update`，由 orchestrator 明确报告当前处理链停在 ingest，不自动声称正式入图完成
- governance 阶段若发现 `needs_fixes` / blocking finding，则汇报当前链路执行到哪一步、哪些产物已写入、哪些仍待修复

## 7. Implementation impact

本设计落地时涉及以下文件面：

### New
- `.claude/skills/process-paper/SKILL.md`

### Update
- `CLAUDE.md`
- `.claude/skills/paper-ingest/SKILL.md`
- `.claude/skills/relation-reconciliation/SKILL.md`
- `.claude/skills/page-projection-sync/SKILL.md`
- `.claude/skills/index-sync/SKILL.md`
- `.claude/skills/ontology-semantic-review/SKILL.md`
- `.claude/skills/serving-governance-review/SKILL.md`

## 8. Recommendation

采用本设计：

- 新增 `process-paper` 作为单篇论文处理的默认统一入口
- 将 `CLAUDE.md` 改写为“入口 + 契约”表达
- 保留 `CLAUDE.md` 的规范真源地位
- 清理现有子 skill 中承接编排职责的内容
- 使用“仓库正式产物 + 结构化阶段摘要”作为阶段间交接机制

这样既能提高“处理论文”意图的执行稳定性，又不会把规范层职责错误地下沉到某个具体 skill 中。