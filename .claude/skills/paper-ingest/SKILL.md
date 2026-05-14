---
name: paper-ingest
description: 用于单篇论文编译链中的 ingest 阶段：解析 PDF、生成 Evidence 缓存、对象页候选与 formal relation candidates。仅当编排型 skill `process-paper` 已将当前任务推进到 ingest 阶段，或用户明确要求只做 ingest / 初步落库时，才应使用本 skill；不要把它当作“处理论文”完整请求的默认入口。它负责把原始论文编译成可供后续阶段消费的正式仓库产物与结构化阶段摘要；不负责继续编排后续链路。
---

# Paper Ingest

你是 ResearchKB 的论文完整摄入器。你的任务不是只“读一篇论文”，而是把单篇论文从原始 PDF 编译成 ResearchKB 可以长期复用的知识资产。

## 何时使用
当出现以下情形时使用本 skill：
- 编排型 skill `process-paper` 已将当前任务推进到 ingest 阶段
- 用户明确要求只做 ingest / 初步落库
- 用户希望围绕某篇论文生成可复用的 Evidence 缓存、对象页候选或 formal relation candidates，但并未要求立即完成整条治理链

不要把它用于：
- 默认意义上的“处理论文：...”完整链路入口
- 只回答一个简短问题且无需落库
- 仅做跨论文综合分析但不处理新增论文
- 与论文无关的普通写作或编程任务

## 核心原则
1. 把 `CLAUDE.md` 视为最高约束，尤其是 taxonomy、缓存模板、目录结构和工作流要求。
2. 默认按论文类型生成最小缓存集合：
   - empirical / method / application 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].experiments.md`
   - survey / framework / taxonomy / benchmark-landscape 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].analysis.md`
   - theoretical / position 论文：`[short_name].sections.md`、`[short_name].refs.md`
3. 不生成 `full.md`；若未来需要新增 cache 类型，必须先更新本体规范与 skill 合约，而不是临时加文件

## 架构定位
本 skill 属于 ResearchKB 的单篇论文编译链 ingest 阶段。
它的职责是把原始论文编译成候选知识变更，包括：
- `ontology/entities/evidence/` 证据缓存
- `ontology/entities/` 正式节点页候选变更
- formal relation candidates（供后续 `relation-reconciliation` 使用）

它不直接完成全图 formal relation 闭环，也不裁决语义合法性；它只负责产出可供后续阶段消费的正式仓库产物与结构化阶段摘要，不负责编排或触发后续阶段。

## 输入约定
从用户提示中提取以下信息：
- 论文路径或论文标题（必须）
- 当前关注方向（可选）
  - 例如：方法演化、技术细节、实验对比、金融场景、数据治理、benchmark 设计

如果用户没有明确关注方向，默认关注：
- 核心问题
- 主要方法
- 关键实验结论
- 与现有知识库的关系

## 执行流程

### Step 1: 解析任务并确认输入
1. 识别论文路径或标题。
2. 如果用户给出的是标题但未给路径，先在 `ontology/entities/raw-sources/files/` 目录定位文件。
3. 提取当前关注方向；若未提供，使用默认关注方向。
4. 生成稳定短名 `short_name`：优先用论文方法名或公认简称，避免使用超长全文标题直接命名缓存文件。

### Step 2: 首次阅读与结构判断
1. 读取论文 PDF 的首页、方法/实验关键页、参考文献页。
2. 判断论文的大致类型：
   - 方法论文
   - 应用论文
   - survey / benchmark / dataset / taxonomy 论文
   - framework / mixed 论文
3. 判断结构是否标准：
   - 是否存在可映射的 abstract/introduction/method/experiments/conclusion
   - 是否存在明显附录依赖、图表依赖、章节标题异常、关键信息缺失

### Step 3: 生成 intermediate 缓存
在 `ontology/entities/evidence/` 下按论文类型生成最小缓存集合：

1. 所有论文默认生成：
   - `[short_name].sections.md`
   - `[short_name].refs.md`
2. 第三缓存按论文类型分流：
   - empirical / method / application 论文：`[short_name].experiments.md`
   - survey / framework / benchmark / taxonomy / dataset / benchmark-landscape 论文：`[short_name].analysis.md`
3. theoretical / position 论文不生成第三缓存，除非本体规范后续明确扩展

生成要求：
- `sections.md` 是默认分析入口，承担章节结构、核心机制与 formal relation 审计所需的最小章节级摘要
- `refs.md` 服务引用关系、方法演化与上游基线 grounding
- `experiments.md` 仅用于实验、消融、效率、泛化与 benchmark 结果证据
- `analysis.md` 仅用于综述统计、landscape、阶段分析、software-gap 分析、framework 支撑证据或 benchmark 设计分析
- 不生成 `full.md`，也不以长篇高保真重写稿替代 `sections.md`

写缓存时优先遵循 `CLAUDE.md` 中的缓存模板规范。

### Step 4: 输出初读结论
在真正落库前，向用户给出一轮简短初读结论：
- 核心问题
- 主要方法
- 关键结论（3-5 条）
- 结合关注方向补充一段重点观察

如果用户显式要求跳过这一轮汇报并直接落库，可以直接继续。

### Step 5: 创建/更新知识库页面
按 `CLAUDE.md` 的模板和 frontmatter 规范进行落库：

1. 论文页：`ontology/entities/papers/[论文名].md`
2. 方法页：若是方法论文，为核心方法创建或更新 `ontology/entities/methods/`
3. 场景页：为核心场景创建或更新 `ontology/entities/scenarios/`
4. 任务页：为论文核心研究任务创建或更新 `ontology/entities/tasks/`
5. 对于 survey / framework / taxonomy 论文：优先把核心知识落到 method / scenario / evidence / relations，而不是强行抽取单一方法页或独立概念实体。
6. 关联关系：在落库完成前，逐类判断是否存在应正式落账的关系；只要存在就写入对应账本，而不是留在正文 prose 中。
   - 在写入 `cites` 前，必须先对所有 `cites` target 做存在性检查；若对应 paper 页不存在，先调用同目录下的 `materialize_cited_paper_placeholders.py` 生成最小 placeholder paper 页，再写入 `ontology/relations/cites.md`。
   - `materialize_cited_paper_placeholders.py` 的职责仅限于：为缺失 cited papers 生成可解析的最小 Paper placeholder，不替代正式 ingest。
   - placeholder paper 页至少应包含：`status: placeholder`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 待补充`。
   - `cites` target 不允许在 ledger 中保持不可解析状态。
   - `ontology/relations/cites.md`
   - `ontology/relations/proposes.md`
   - `ontology/relations/based_on.md`
   - `ontology/relations/targets_task.md`
   - `ontology/relations/evaluated_on.md`
   - `ontology/relations/applied_in.md`
   - `ontology/relations/supported_by.md`
   - `ontology/relations/sourced_from.md`
7. 更新：
   - `ontology/log.md`

### Step 6: 汇总候选正式关系
在完成页面与缓存候选更新后，必须显式整理本次论文直接支撑的 formal relation candidates，而不是只把关系散落写进正文或关系账本。

每条 relation candidate 至少包含以下规范化元数据字段：
- `relation`
- `source_name`
- `source_type`
- `source_path`
- `target_name`
- `target_type`
- `target_path`
- `edge_semantics`
- `evidence_name`
- `evidence_path`

对象级语义要求：
- 每个正式对象页候选必须同时产出对象级语义真源 `object_semantics`，供后续 `index-sync` 投影到对象域入口项。
- `object_semantics` 用于表达“该对象实例是什么”，不替代 relation candidate 的 `edge_semantics`。
- 对于 `Paper` 候选，除最小 `object_semantics` 外，还必须额外整理可投影到人类友好正文的语义载荷，至少覆盖：
  - `core_problem_framing`
  - `core_contribution_framing`
  - `key_judgments`（3-5 条）
  - `kb_relationship_framing`
  - `extraction_boundary_notes`
- 这些字段的目标不是复述论文全文，而是为后续 Paper 页的人类阅读入口提供高密度判断材料。
- 对于 `Method` 候选，若当前论文已足以支撑 processed Method 级别的对象页，还必须额外整理可投影到方法解释层的语义载荷，至少覆盖：
  - `method_identity_framing`
  - `core_mechanism_summary`
  - `task_scenario_positioning_notes`
  - `neighbor_method_distinctions`
  - `current_knowledge_state_notes`
- 若当前仅能支撑 `status: partial` 的 Method，则继续以 semantic-stub 最小语义骨架为主，不强制生成完整方法解释层。
- 对于当前论文已经稳定提供最小对象语义、但证据仍不足以支持完整 serving-ready 页的高价值邻接对象，必须额外产出 `semantic_stub_candidates`，供后续 `relation-reconciliation`、`page-projection-sync` 与 `index-sync` 使用。
- 对于被 `based_on`、`references_method` 或 `proposes`（target 为 Method）稳定指向、但当前库中尚不存在的上游方法对象：
  - 若当前论文已经稳定提供其 Method 身份、正常 `object_semantics` 与至少一条正式方法关系，则必须直接产出 `status: partial` 的 Method 候选，而不是 Method placeholder。
  - Method placeholder 不再作为正式中间状态保留；只保留 cited paper placeholder 用于 `cites` target 解析。

`semantic_stub_candidates` 中每个对象至少包含：
- `object_name`
- `object_type`
- `source_evidence`
- `object_semantics`
- `minimal_sections`
  - `当前定位`
  - `与知识库现有内容的关系`
  - `最小定义/角色`
  - `待补充`
- `serving_readiness_hint`
  - `placeholder`
  - `partial`
  - `candidate-serving`

这些 semantic stubs 用于表达“当前论文已稳定支撑该对象的最小语义骨架，但尚未完成 full ingest”，它们不替代正式完整 ingest，也不应被自动视为 default serving-ready 页面。

表示层边界：
- `paper-ingest` 不直接生成 relation ledger 最终 markdown。
- `paper-ingest` 不在此阶段决定使用短 wikilink 还是带路径 wikilink。
- 这些 relation 页表示层决策由 `relation-reconciliation` 负责。
- 人类友好正文载荷的抽取边界：
  - 必须显式暴露不确定性，不得把弱证据推断伪装成确定结论。
  - 不得把 Evidence cache 大段复制为对象页 prose。
  - 不得把这些载荷当作第二套 relation ledger；formal relation truth 仍由 relation candidates 与后续 ledger / projection 阶段承接。
  - 当当前论文只足以支持 Paper 层解释，而不足以支持完整 Method 身份解释时，优先保证 Paper-first 输出完整，而不是勉强生成低质量 Method prose。

补充约束：
- `supported_by` 候选只允许从 `Method`、`Task`、`Scenario`、`Benchmark` 指向 `Evidence`。
- 不生成 `Paper --supported_by--> Evidence`。
- Evidence 页保留 `source_file` provenance 锚点，但不通过正文或单独 formal relation 直接链接回 Paper。
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在各自的 `Formal relations` 中出现。

输出时至少按以下关系类型归类：
- `proposes`
- `surveys_method`
- `targets_task`
- `evaluated_on`
- `applied_in`
- `supported_by`
- `cites`
- `based_on`
- `references_method`
- `sourced_from`

并且必须区分三类：
1. direct relations：证据明确、可直接落账
2. high-confidence candidate relations：强支持但仍需 graph-level reconciliation
3. needs-human-review relations：存在方向、粒度或本体归属歧义

`references_method` 使用规则：
- 当方法间关系表达的是关键比较对象、借鉴路线或方法参照，而非严格谱系继承时，可将其输出为 `references_method` candidate。
- 若仅存在论文级引用事实而缺少稳定方法对象语义，不得从 `cites` 升格为 `references_method`。
- `references_method` 强于论文引用、弱于 `based_on`；它不驱动 `parent_methods` / `child_methods`。

### survey coverage tiering
对于 survey / landscape / taxonomy / framework 论文，必须主动检测 method coverage，并将候选对象分为三档：
- Tier A（direct survey-covered method candidates）：稳定方法名 + 结构化 coverage + 可写最小 `object_semantics` + representative paper 稳定可识别；默认直接进入 formal admission 链。
- Tier B（high-confidence survey method candidates）：方法身份较稳定，但结构化 coverage 或 representative paper 仍略弱；默认输出为高置信候选并强制交给 `relation-reconciliation` 复核，不在 ingest 阶段直接落 formal ledger。
- Tier C（needs-human-review survey candidates）：仅有 related-work mention、对象身份不稳、或更像系统/场景/benchmark/概念；只进入 review 输出，不自动 materialize。

宽松检测不等于宽松落账：survey 论文应积极发现方法候选，但只有 Tier A 默认自动落入 `surveys_method`。

## 分类与抽取规则
### 论文页
必须尽量填充这些结构化字段：
- `problem`
- `method_family`
- `scenario`
- `research_task`
- `industry`
- `research_role`

### 方法页
重点判断：
- 这是基础方法、衍生方法还是集成方法？
- 它的父方法是谁？
- 是否应挂到某个“方法族”之下，而不是直接把若干基线都写成 `parent_methods`？
- 当上游方法关系表达严格方法谱系、继承来源或明确建立在某方法之上时，优先产出 `based_on`；当表达关键比较对象、借鉴路线或方法参照但不构成谱系继承时，优先产出 `references_method`。

### 场景页
区分：
- `scenario`：行业/落地场景
- `research_task`：研究任务型场景（例如 KGQA、多跳问答、benchmark）
- 若一个候选项同时像 Task 又像 Scenario，优先判断其是否命名研究目标；若仍有歧义，默认先判 `Task`。

### 关系文件
- 对重要上游论文，即使知识库中尚未有完整页，也可先在 citation graph 中预登记。
- 对 `cites` 指向但当前不存在的论文节点，必须在 ingest 阶段自动创建最小 placeholder paper 页；不得只写 relation ledger 而让 target 保持不可解析。
- 自动生成的 cited paper placeholder 只允许进入对象域 index 的“其他实例（不可导航）”区块，不得提升到默认导航入口。
- placeholder paper 页至少应包含：`status: placeholder`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 待补充`。
- 对高频上游方法，优先建立最小 stub 页，而不是只留下空链接。
- `proposes`：
  - 方法论文若提出核心方法，必须登记 `[[Paper]] --proposes--> [[Method]]`
  - 若论文核心贡献是可复用方法框架、面向任务的可复用解决方案，也必须登记 `[[Paper]] --proposes--> [[Method]]`
  - 若论文只提供 taxonomy、术语组织或解释框架而不形成可复用方法，应在当前 formal graph 建模边界内保留在 Paper / Method / Evidence prose 中，不单独实体化
- `targets_task`：
  - 只从稳定 `Method` 身份出发生成 `[[Method]] --targets_task--> [[Task]]`
  - 不生成 `[[Paper]] --targets_task--> [[Task]]` formal candidate
- `applied_in`：
  - 若论文明确给出方法应用语境，且 Method 身份稳定，可生成 `[[Method]] --applied_in--> [[Scenario]]`
  - 不生成 `[[Paper]] --applied_in--> [[Scenario]]` formal candidate
- `evaluated_on`：
  - 只要存在明确 benchmark，应登记 `[[Method]] --evaluated_on--> [[Benchmark]]`
  - 论文页中的 benchmark 信息保留在 prose、frontmatter 与 Evidence 支撑中，不再生成 `[[Paper]] --evaluated_on--> [[Benchmark]]`
  - survey / framework / taxonomy / dataset / benchmark 类型论文若无统一 benchmark，不生成 `evaluated_on`，并在最终输出中显式写明“按规范豁免”
- 若某方法通过 `surveys_method` 被稳定纳入图谱，且 survey / landscape / taxonomy 论文对其任务归属提供结构化 coverage（如任务分组、taxonomy、比较表、coverage 列表），仍可继续生成 `[[Method]] --targets_task--> [[Task]]`。
- 若某方法通过 `surveys_method` 被稳定纳入图谱，且 survey / landscape / taxonomy 论文对其场景归属提供结构化 coverage（如场景分组、taxonomy、比较表、coverage 列表），仍可继续生成 `[[Method]] --applied_in--> [[Scenario]]`。
- 不生成 `[[Task]] -> [[Scenario]]` 或 `[[Scenario]] -> [[Task]]` formal candidate；Task 与 Scenario 的联系在当前 formal graph 中默认通过共享的 Method 邻接表达。
- 若 survey 论文只是顺带提到某任务或场景，而没有把方法明确纳入对应的结构化分组、coverage 或比较框架，则不得为该方法生成 `targets_task` 或 `applied_in`。
- `sourced_from`：
  - 只要本次生成了 `sections.md`、`refs.md`、`experiments.md`、`analysis.md` 任一 Evidence 缓存，就必须同步登记 `[[Evidence]] --sourced_from--> [[RawSource]]`

## 异常结构检测
以下情况说明当前论文可能不适合直接套用标准模板：

1. 缺少清晰的方法章节，主要贡献是 survey / benchmark / dataset / taxonomy / framework
2. 实验关键信息大量放在 appendix，中正文无法稳定支撑 empirical `experiments.md`
3. 章节标题高度非标准，难以映射到常规模板
4. 论文没有单一核心方法，更多是评测框架、数据集贡献、角色划分或分层 framework
5. taxonomy 无法稳定归类到现有 `problem / method_family / research_task` 体系
6. 图表、表格或版式对理解贡献过大，文本解析后信息明显残缺

## 降级策略
若发现异常结构，不要硬落库为“普通方法论文”。采用以下策略：

1. 尽可能先完成 intermediate 缓存
2. 根据可确认的信息做部分落库
3. 将不确定部分明确标记为待补
4. 输出结构化告警，提醒当前 skill 需要进一步优化

## 最终输出格式
完成后，必须以一个结构化摘要收尾。使用下面模板：

```yaml
status: success | partial | needs-skill-update
paper_type_guess: method | application | survey | benchmark | dataset | taxonomy | framework | mixed
generated_caches:
  - ontology/entities/evidence/<short_name>.sections.md
  - ontology/entities/evidence/<short_name>.refs.md
  - ontology/entities/evidence/<short_name>.experiments.md | ontology/entities/evidence/<short_name>.analysis.md
updated_pages:
  - ontology/entities/papers/...
  - ontology/entities/methods/...
  - ontology/entities/scenarios/...
  - ontology/relations/...
relation_candidates:
  proposes: []
  surveys_method: []
  targets_task: []
  evaluated_on: []
  applied_in: []
  supported_by: []
  cites: []
  based_on: []
  references_method: []
  sourced_from: []
relation_exemptions:
  - relation_type: evaluated_on
    reason: no unified benchmark; exempt by graph-standard
warnings:
  - ...
skill_update_signals:
  - ...
```

对于 Tier A survey-covered methods，除 `surveys_method` / `supported_by` / `cites` relation candidates 外，还必须额外输出：
- `representative_paper_candidates`
- `paper_stub_candidates`
- `survey_method_tier: TierA`

对于 Tier B survey candidates，必须输出：
- `survey_method_tier: TierB`
- `high_confidence_survey_method_candidates`
- 可选 `representative_paper_candidates`

对于 Tier C survey candidates，必须输出：
- `survey_method_tier: TierC`
- `needs-human-review survey candidates`

新增对象页人类友好正文载荷输出：
- `paper_human_friendly_payloads`
- `method_human_friendly_payloads`

其中：
- `paper_human_friendly_payloads` 至少应包含 `core_problem_framing`、`core_contribution_framing`、`key_judgments`、`kb_relationship_framing`、`extraction_boundary_notes`
- `method_human_friendly_payloads` 至少应包含 `method_identity_framing`、`core_mechanism_summary`、`task_scenario_positioning_notes`、`neighbor_method_distinctions`、`current_knowledge_state_notes`

解释：
- `success`：基础缓存、正式页面与应有关系账本更新都已完成，且结构适配良好。
- `partial`：完成了大部分工作，但某些页面、字段或正式关系账本仍需人工补充。
- `needs-skill-update`：当前论文类型或结构已经超出本 skill 的稳定适配范围。
- `relation_candidates`：必须显式列出本次论文直接支撑或高置信支持的 formal relation 候选，供后续 relation reconciliation 使用。
- `relation_exemptions`：若某类关系按规范豁免（例如 survey / framework 论文无统一 benchmark，因此不生成 `evaluated_on`），必须在此显式说明；不要把正常豁免写成“待补充”。
- 改进、前提依赖、应用场景与概念性支撑语义默认写入 `edge_semantics`、frontmatter 或对象页正文，而不再单独输出为 formal relation candidate。

## 触发 `needs-skill-update` 的典型例子
- “这是一篇 benchmark/survey/framework 论文，当前方法页模板不是最佳落点。”
- “方法章节缺失，无法稳定抽取单一核心方法。”
- “实验细节主要在 appendix，当前 `experiments.md` 只能部分生成。”
- “taxonomy 难以稳定归类，建议为此类论文扩展 frontmatter 或页面模板。”
- “该论文更适合生成 `analysis.md` 而不是 `experiments.md`，当前 skill 若仍硬套实验缓存说明分流规则不足。”

## 质量要求
- 优先保证知识提炼可复用，而不是追求一次性写得很长。
- 不要把 PDF 的解析噪声直接带入 wiki 页面。
- 缓存层保真，知识页抽象。
- 对已存在页面做增量更新，避免重复造页。
- 用户一旦明确了关注方向，相关提取与批注必须优先服务该方向。

## 示例
### 示例 1：标准方法论文
输入：
- `处理论文：ontology/entities/raw-sources/files/PathMind.pdf，重点看方法演化`

预期：
- 生成 3 个缓存（`sections`、`refs`、`experiments`）
- 创建/更新 paper + method + concept + scenario + relation 页面
- 重点输出 PathMind 相对 RoG / GCR / EPERM 的演化关系

### 示例 2：结构异常论文
输入：
- `处理论文：ontology/entities/raw-sources/files/某篇benchmark论文.pdf，重点看评测设计`

预期：
- 尽量生成 4 个缓存
- 不要强行把它当普通方法论文完整落库
- 输出 `needs-skill-update` 或 `partial`
- 指出该类 benchmark 论文可能需要专门模板

当 survey 论文已经对 Tier A 方法完成 direct admission 时，相关 Evidence 缓存不得继续保留“当前 ingest 不把高体量 survey 引文批量升格为 `surveys_method`”这类 blanket prose。必须改写为：
- 哪些方法已被当前批次直接 materialize
- 哪些候选仍处于 Tier B / Tier C
- 为什么剩余候选被延后

## 使用完成后的建议
若输出为 `partial` 或 `needs-skill-update`，应在回复中明确说明：
- 哪些内容已经完成
- 哪些内容仍不稳定
- 当前 skill 该如何升级，才能更好适配这类论文
- 若某类关系因规范豁免未生成，应明确区分“正常豁免”与“skill 漏写”，避免把豁免项误报为待补。
