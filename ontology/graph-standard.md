# ResearchKB Graph Standard

## 1. 文档定位
- 本文是 ResearchKB 的规范真源，用于定义节点、关系、证据、投影与治理验收标准。
- 执行流程、编译链顺序与运行路由由 `CLAUDE.md` 负责，不在本文重复展开。
- 系统级与对象域导航入口由 `CLAUDE.md` 与各对象域 index 承担；本文只保留少量“如何消费规范”的原则性说明。

## 2. 本体基础

### 2.1 节点类型
- Paper：论文实例节点
- Method：方法节点
- Task：研究任务节点
- Scenario：应用场景节点
- Benchmark：数据集或评测基准节点
- Evidence：`ontology/entities/evidence/` 下的结构化证据对象页
- RawSource：`ontology/entities/raw-sources/files/` 下的受管原始来源文件集合，由 `ontology/entities/raw-sources/index.md` 提供导航；主要用于 provenance 追踪与最终回查，不承担主图谱组织职责

### 2.2 survey / framework 建模公理
- Survey 是 Paper 层节点：它表示可引用、可追溯的论文研究产物，不下沉为 Task。
- Framework / taxonomy 若主要承担可执行方法流程、明确实验对比、方法演化语义，或本身就是面向任务的可复用解决方案，则应按 Method 处理。
- Framework / taxonomy 若主要承担知识组织、分类、分层或解释框架语义，但不构成可复用方法，则 phase 1 保留在 Paper、Method 或 Evidence prose 中，不单独实体化。
- 当论文的核心贡献是可复用技术流程、方法框架或面向任务的可复用解决方案时，应登记 `[[Paper]] --proposes--> [[Method]]`。

### 2.3 关系类型
- `proposes`：`[[Paper]] --proposes--> [[Method]]`；表示论文首次提出或正式定义某方法、可执行方法框架，或面向任务的可复用解决方案。Survey 保持为 Paper 层节点；phase 1 不再为 framework / taxonomy / terminology 单独生成实体。
- `targets_task`：`[[Method]] --targets_task--> [[Task]]`；表示方法主要面向的研究任务。若论文描述了任务定位，应通过 Method 层 formal relation 承接；Paper 页中的任务信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Task` formal edge。
- `evaluated_on`：`[[Method]] --evaluated_on--> [[Benchmark]]`；表示方法在某个正式 benchmark 上进行了评测。该关系不再用于 `Paper -> Benchmark`；论文页中的 benchmark 信息只保留在 prose、frontmatter、Evidence 与 Method 邻接投影中。
- `applied_in`：`[[Method]] --applied_in--> [[Scenario]]`；表示方法被明确应用、部署、验证或定位在某个应用场景中。该关系只允许 Method 作为 source、Scenario 作为 target；Paper 页中的场景信息保留在 prose、frontmatter 与 Evidence 支撑中，不单独生成 `Paper -> Scenario` formal edge。
- `based_on`：`[[Method]] --based_on--> [[Method]]`；表示方法建立在某个上游方法之上，只用于方法演化谱系，不指向场景。若需要表达改进、增强或优化等增量语义，默认写入 `edge_semantics`，而不额外拆分 formal relation。
- `references_method`：`[[Method]] --references_method--> [[Method]]`；表示方法将另一方法作为关键比较对象、借鉴路线或方法参照。该关系与 `based_on` 一起构成方法图谱的核心邻接关系：前者表达参照，后者表达谱系；`references_method` 不驱动 `parent_methods` / `child_methods`。
- `cites`：`[[Paper]] --cites--> [[Paper]]`；表示论文对论文的显式引用。
- `supported_by`：`[[Method|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`；表示正式知识对象页由 Evidence 对象页支撑。`Paper` 不再作为 `supported_by` 的 source；Evidence 与 Paper 之间也不单独建立 formal relation。
- `sourced_from`：`[[Evidence]] --sourced_from--> [[RawSource]]`；表示 Evidence 对象页来源于 `ontology/entities/raw-sources/files/` 下的受管原始文件。RawSource 不再为每个 PDF 维护独立对象页，而是由 `ontology/entities/raw-sources/index.md` 提供统一导航。该关系默认主要落在 provenance 层，不要求正式知识页直接连接原始来源；若证据对象页尚未生成而必须临时登记来源，可例外使用 `status: placeholder` 暂存。保留的 `sections`、`refs`、`experiments`、`analysis` 均可直接承担 `sourced_from` provenance 锚点，不依赖额外全文型 cache。
- Formal relation 只保留对 ingest 稳定、治理边界清晰、且对检索 / 问答有明显增益的关系类型；应用场景语义若已稳定到方法层，可通过 `applied_in` 表达；尚不足以形成正式方法-场景边时，仍可下沉到 frontmatter `scenario`、对象页正文与索引导航表达；改进强度与前提依赖等语义默认继续下沉到 `edge_semantics` 与对象页正文。

## 3. 对象页契约

### 3.1 Frontmatter 受控字段
```yaml
problem:
  - knowledge-acquisition
  - ontology-modeling
  - entity-linking
  - relation-extraction
  - graph-construction
  - ontology-alignment
  - entity-alignment
  - reasoning
  - query-answering
  - representation-learning
  - graph-learning
  - quality-governance
  - evolution-maintenance
  - benchmark-survey

method_family:
  - rule-based
  - symbolic
  - probabilistic
  - traditional-ml
  - embedding
  - gnn
  - llm
  - hybrid

scenario:
  - financial-risk
  - anti-fraud
  - aml
  - investment-research
  - compliance
  - customer-portrait
  - master-data-management
  - metadata-management
  - data-governance
  - enterprise-qa
  - decision-support

research_task:
  - knowledge-graph-reasoning
  - kgqa
  - multi-hop-qa
  - ontology-alignment-benchmark
  - entity-alignment-benchmark
  - graph-completion
  - schema-matching
  - benchmark-evaluation

industry:
  - finance
  - enterprise
  - healthcare
  - manufacturing
  - government
  - general

research_role:
  - foundational
  - derived
  - integrated
  - application
  - survey
  - benchmark
```

### 3.2 通用填写原则
- `problem` 是主分类轴，每个正式知识页至少填写 1 项，通常不超过 3 项。
- `method_family` 描述技术范式；论文页和方法页应尽量填写，其他页面按需要填写。
- `scenario` 表示落地或应用场景，`industry` 表示行业背景，两者分开维护。
- `research_task` 用于 KGQA、多跳问答、对齐基准等研究任务型场景，不替代行业场景字段。
- `research_role` 用于表达该节点在研究演化链中的角色。
- `tags` 仅作为补充关键词，不替代结构化字段。
- `Task` 回答“要解决什么研究问题 / 推理范式 / 问答目标”；`Scenario` 回答“方法在什么应用语境 / 业务环境 / 部署上下文中使用”。
- 若候选项同时像 Task 又像 Scenario，优先判断其是否命名研究目标；若是 KGQA、多跳问答、推理、对齐、补全等研究目标，落为 `Task`；若是企业问答、金融风控、合规审查、投研辅助等应用语境，落为 `Scenario`。
- 若仍存在歧义，默认先判 `Task`，除非存在明确应用上下文证据支撑 `Scenario` 身份。

- 每个正式对象页必须提供对象级语义真源 `object_semantics`，用于向对象域 `index.md` 投影入口语义；推荐以 `## Object semantics` 区块承载，而不是使用自由 prose hook。

### 3.3 Paper
必填字段：`title`、`authors`、`year`、`venue`、`problem`、`industry`、`research_role`、`status`

推荐字段：`method_family`、`scenario`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 论文完整标题
authors: 作者列表
year: 发表年份
venue: 期刊/会议名称
problem: [knowledge-acquisition]
method_family: [hybrid]
scenario: [data-governance]
research_task: []
industry: [enterprise]
research_role: [application]
tags: [知识图谱, 本体, 金融, 企业应用]
status: processed
---
```

正文标准结构：
- 核心问题
- 主要贡献
- 核心方法
- 相关任务
- 应用场景
- 相关基准
- 关键结论
- 引用了哪些重要工作
- 被哪些论文引用（已知）
- 与知识库其他内容的关联
- 证据来源
- Formal relations
- 我的批注

survey / framework-taxonomy 论文的 Paper 页投影补充规则：
- 当 `research_role: survey` 或论文核心贡献是 framework / taxonomy / landscape 组织时，Paper 页的人类区块应优先突出：核心框架、相关任务、应用场景、关键结论、综述证据来源。
- 这类 Paper 的 `Formal relations` 重点为：`proposes`、`cites`。
- 与任务、场景相关的论文级信息优先保留在人类区块、frontmatter 与 Evidence 支撑中；若需要 formal relation，应由对应 Method 层的 `targets_task`、`applied_in` 承接。
- 若无统一 benchmark，必须显式以 `relation_exemptions` 说明 `evaluated_on` 按规范豁免，而不是伪造 benchmark formal edge。

### 3.4 Method
必填字段：`title`、`type`、`problem`、`industry`、`research_role`

推荐字段：`parent_methods`、`child_methods`、`method_family`、`scenario`、`research_task`、`tags`

约束：
- `type` 保留中文表达，使用：`基础方法` / `衍生方法` / `集成方法`
- `parent_methods` / `child_methods` 必须与 `ontology/relations/based_on.md` 保持一致

#### Method 页状态分层规则
- `status: processed` 的 Method 页必须满足完整 serving 合同：`## 证据来源`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- `status: partial` 的 Method 页按 semantic-stub 合同校验，至少应具有：`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`、`## Formal relations`、`### Outgoing`、`### Incoming`。
- Method 不再使用 `status: placeholder` 作为正式中间状态；只要方法身份与 formal relation 已稳定成立，就应直接 materialize 为 `status: partial` 的 Method 页。

参考骨架：
```yaml
---
title: 方法名称
type: [基础方法 / 衍生方法 / 集成方法]
parent_methods: [基础方法1, 基础方法2]
child_methods: [衍生方法1, 衍生方法2]
problem: [reasoning]
method_family: [symbolic]
scenario: [enterprise-qa]
research_task: []
industry: [general]
research_role: [foundational]
tags: [知识图谱, 本体推理]
---
```

正文标准结构：
- 方法定义
- 解决的核心问题
- 技术原理
- 方法演化与参照关系
- 应用场景
- 代表论文
- 相关机制
- 证据来源
- Formal relations
- 优势与局限
- 与其他方法的对比

Method 页中的“方法演化与参照关系”用于面向人类区分两类核心方法邻接：
- `based_on`：上游演化方法 / 严格方法谱系来源
- `references_method`：关键参照方法 / 比较对象 / 借鉴路线

其中 `parent_methods` / `child_methods` 只由 `based_on` 派生；`references_method` 不进入父子方法链。

### 3.5 Task
必填字段：`title`、`problem`、`industry`、`research_role`

推荐字段：`method_family`、`scenario`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 任务名称
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
tags: [研究任务]
---
```

正文标准结构：
- 任务定义
- 核心挑战
- 相关方法
- 相关机制
- 相关场景
- 相关 benchmark
- 相关论文
- 证据来源 / 关系索引
- Formal relations

survey / framework 主线的 Task 补充规则：
- 若任务页主要由 survey / framework 节点驱动，而非方法-基准驱动，人类区块应优先突出：相关框架、相关场景、相关论文、证据来源 / 关系索引。
- `Formal relations` 重点为 incoming `targets_task`，以及必要时的 `supported_by`。

### 3.6 Benchmark
必填字段：`title`、`problem`、`industry`、`research_role`

推荐字段：`method_family`、`scenario`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 基准名称
problem: [query-answering]
method_family: [hybrid]
scenario: []
research_task: [kgqa]
industry: [general]
research_role: [benchmark]
tags: [benchmark]
---
```

正文标准结构：
- benchmark 定义
- 评测目标
- 相关任务
- 被哪些方法 / 论文使用
- 相关场景
- 证据来源
- Formal relations

### 3.7 Scenario
必填字段：`title`、`problem`、`scenario`、`industry`、`research_role`

推荐字段：`method_family`、`research_task`、`tags`

参考骨架：
```yaml
---
title: 场景名称
problem: [quality-governance]
method_family: [hybrid]
scenario: [financial-risk]
research_task: []
industry: [finance]
research_role: [application]
tags: [金融, 风控, 知识图谱]
---
```

正文标准结构：
- 场景描述
- 核心挑战
- 使用的主要方法 / 机制
- 相关任务
- 相关论文
- 相关 benchmark
- 证据来源
- Formal relations
- 开放问题

survey / framework 主线的 Scenario 补充规则：
- 若场景页主要由 framework / survey 节点供给，人类区块应优先突出：使用的主要方法、相关任务、相关论文、证据来源。
- `Formal relations` 可包含 incoming `applied_in` 与必要的 `supported_by`；相关任务仍优先通过 frontmatter 与正文表达，不单独新增 `Scenario -> Task` formal edge。

### 3.8 Evidence
必填字段：`title`、`short_name`、`source_file`、`cache_type`、`status`

推荐字段：`venue`、`year`

约束：
- `cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`
- 按论文类型执行最小缓存集合：
  - empirical / method / application 论文：`sections` + `refs` + `experiments`
  - survey / framework / taxonomy / benchmark-landscape 论文：`sections` + `refs` + `analysis`
  - theoretical / position 论文：`sections` + `refs`
- 不允许在未更新本规范前新增其他正式 cache 类型。
- 每个 Evidence 页面都必须显式回链正式论文页，并链接关键方法、任务与基准或其豁免说明

正文标准结构：
- 对应正式知识节点
- 本节支撑什么
- 关键摘录 / 关键实验 / 关键引用 / 关键分析
- 来源说明
- Formal relations

补充边界：
- `sections` 用于章节结构、核心机制与足以支撑 formal relation 审计的章节级摘要；不得扩张为接近整篇论文的重写稿，或与正式论文页形成大段叙述重复。
- `analysis` 仅用于 survey / framework / taxonomy / benchmark-landscape 类论文的统计、landscape、阶段分析、框架拆解或非统一实验型证据；不得作为 empirical 论文的常规第三缓存，也不得充当泛化“额外总结页”。
- 若新增 `sections` 内容不能提升 formal relation 可审计性或章节级复用性，则不应写入。

## 4. 关系账本与证据契约

### 4.1 实例边层
- 实例边（instance edge）是两个具体知识节点之间的显式关系记录，不等同于关系类型定义本身。
- `ontology/relations/` 是正式维护实例边账本的唯一治理真源。
- 治理通过后，对象页中的 `## Formal relations` 作为默认服务读取面；自然语言说明与 `[[wikilink]]` 仅作辅助，不替代正式关系账本。

### 4.2 实例边记录格式
- formal relation ledger 页面固定由两个逻辑区段构成：`关系语义说明区` 与 `实例边账本区`。
- `实例边账本区` 是 relation 实例边真源；每条正式实例边必须使用以下 canonical 结构。

规范格式（canonical）：

```markdown
- [[Source Node]] --relation_type--> [[Target Node]]
  - source_path: ontology/entities/<source-domain>/<source>.md
  - target_path: ontology/entities/<target-domain>/<target>.md
  - edge_semantics: 边的成立语义
  - evidence: 证据名称
  - evidence_link: [[证据页]]
  - evidence_path: ontology/entities/evidence/<evidence>.md
```

实例边子字段顺序固定为：
1. `source_path`
2. `target_path`
3. `edge_semantics`
4. `evidence`
5. `evidence_link`
6. `evidence_path`

关系页中的 Obsidian wikilink 仅允许出现在以下位置：
- 实例边主行的 `source`
- 实例边主行的 `target`
- 子字段 `evidence_link`


可选字段：

```markdown
  - status: verified | placeholder
  - note: 补充上下文
```

可选字段若存在，必须追加在 `evidence_path` 之后，不得改变 canonical 子字段顺序。

编译链分工要求：
- `paper-ingest` 负责产出规范化的 relation candidate 元数据（用于后续渲染），不负责最终 relation ledger 排版。
- `relation-reconciliation` 负责 relation ledger 的最终写盘与 canonical 格式落地。
- `page-projection-sync` 负责消费 formal relation truth 并投影回对象页，不定义 relation 页表示层。

对象页与 Evidence 页中的 `## Formal relations` 不复用上述完整边写法作为 serving projection 默认格式。投影同步后的页面必须使用半展开格式：

```markdown
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]
```

若同一邻接对象存在多条 formal relation instance，且 `edge_semantics` 或 `evidence` 不同，不得合并，必须逐条投影。

对象域 index 不再使用自由 trailing hook prose；每个对象入口项必须投影对象页真源 `object_semantics`。

约束：
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在该页 `Formal relations` 中出现。
- 不允许通过正文额外暴露 formal graph 之外的对象邻接。
- Evidence 页正文不允许直接链接回 Paper；Paper provenance 仅通过 `source_file` 与 `sourced_from` 体系表达。

### 4.3 关系文件分工
- 每个正式 relation type 都有且只有一个正式 ledger 文件，文件名直接等于 relation type：
  - `ontology/relations/cites.md`：维护 `cites`
  - `ontology/relations/proposes.md`：维护 `proposes`
  - `ontology/relations/based_on.md`：维护 `based_on`
  - `ontology/relations/references_method.md`：维护 `references_method`
  - `ontology/relations/targets_task.md`：维护 `targets_task`
  - `ontology/relations/applied_in.md`：维护 `applied_in`
  - `ontology/relations/evaluated_on.md`：维护 `evaluated_on`
  - `ontology/relations/supported_by.md`：维护 `supported_by`
  - `ontology/relations/sourced_from.md`：维护 `sourced_from`
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 边；若出现正式知识页到 RawSource 的临时占位关系，需显式标注 `status: placeholder` 并尽快补齐对应 Evidence 缓存。
- 新增关系类型或未归属关系类型，必须先在本节明确“归属文件 + 维护范围”，再进入正式实例边维护。

### 4.4 下沉语义处理原则
- 改进、增强、优化等方法增量语义默认写入 `based_on` 的 `edge_semantics`，不再单独拆分 formal relation。
- 应用场景语义若已稳定到方法层，可通过 `applied_in` 表达；若仅为弱上下文描述，仍可下沉到 frontmatter `scenario`、对象页正文与索引导航表达。
- 机制术语、taxonomy 标签与解释性框架在 phase 1 默认保留在对象页正文与 Evidence 说明中，不单独实体化为 formal relation。

### 4.5 实例边维护规则
- 去重规则：同一三元组（Source、relation_type、Target）只保留一条主记录，新增证据以补充字段追加。
- 多关系并存：同一对节点可存在多条不同 `relation_type` 的边，但应优先避免通过新增关系类型表达仅属强弱差异的语义。
- 证据优先：每条正式实例边必须至少附带一个 `evidence`，无证据仅可用 `status: placeholder` 暂存。
- prose 辅助不替代：正文描述与 `[[wikilink]]` 仅作解释层，关系判定以关系账本记录为准。
- 增量更新：新增论文或新节点时，优先补齐受影响关系文件中的实例边，再更新综述性页面。

### 4.6 冗余 cache 判废规则
- 若某 cache 类型不承载独立证据职责，且相对现有 cache 类型不提供不可替代的结构化审计价值，则不得作为正式 cache 类型保留。
- 新增 cache 类型前，必须先在本规范中声明其证据职责、适用论文类型与 relation / provenance 作用范围。

### 4.7 证据要求
- 方法机制优先绑定 `sections.md`。
- empirical 论文的实验结果优先绑定 `experiments.md`。
- 引用与基线关系优先绑定 `refs.md`。
- 对 survey / benchmark / taxonomy / dataset 论文，第三类缓存默认使用 `analysis.md`，用于承载统计、landscape、阶段分析、software-gap 分析或框架型方法支撑证据。
- 原始 PDF 仅作为最终来源，不直接承担主图谱组织职责。

## 5. 服务层与治理契约

### 5.1 治理真源层与服务层
- `ontology/relations/` 作为正式实例边的治理真源，用于治理、修复、审计与 formal graph truth 核对。
- 治理通过后的对象页与 Evidence 页共同构成默认知识服务层；其中对象页承载正式关系读取面，Evidence 页承载机制、实验、引用与 provenance 核验。

### 5.2 全类型服务层投影规则
- Paper、Method、Task、Scenario、Benchmark、Evidence 页必须同时包含：frontmatter、面向人类的关系区块、`## Formal relations` 规范化关系区块。
- frontmatter 只承载紧凑结构化摘要，不承担手写关系真源职责；其派生字段必须来自正式关系账本。
- Method 的 `parent_methods` / `child_methods` 继续作为首批强一致派生字段，必须与 `ontology/relations/based_on.md` 中的正式方法演化边保持一致。
- 其他类型前期默认不强制扩张大量派生字段，优先把正式关系投影收敛到 `## Formal relations`。
- 面向人类的关系区块按节点类型差异化组织，但不得与正式关系账本冲突。
- `## Formal relations` 必须覆盖该实体的一跳正式关系投影，作为问答时的正式关系读取面。

### 5.3 Formal relations 区块规范
- 区块标题固定为 `## Formal relations`。
- 所有 serving-ready 节点类型都必须包含 `### Outgoing` 与 `### Incoming` 两个子区块；无内容时显式写 `- 无`。
- 每条关系使用 canonical 三元组格式：`- `[[Source Node]] --relation_type--> [[Target Node]]``。
- 每条关系至少附带一个 `- evidence: [[证据页]]` 行；必要时可补 `- note:`，但应避免 prose 污染区块。
- 该区块供问答时的受约束拓扑探索直接消费，不以综述性表达代替。

### 5.4 Serving 迁移状态
- serving-ready：页面已通过结构治理、本体语义治理与 serving 治理，可作为默认问答入口。
- partial：页面已开始迁移，或已具备最小语义骨架与 formal 邻接，但尚未达到默认 serving 质量线。
- legacy：页面仍处于旧格式，仅可作为过渡期参考页。
- 迁移状态可放在 frontmatter 或外部治理清单中，但必须能被治理流程识别。

### 5.4.1 Semantic stub 状态规则
- 当单篇论文已稳定提供某个邻接对象的最小对象语义，但证据仍不足以支持完整 serving-ready 页面时，可生成 semantic stub。
- semantic stub 页至少应具有：`status: partial` 或 `status: placeholder`、`## Object semantics`、`## 当前定位`、`## 与知识库现有内容的关系`、`## 最小定义/角色`、`## 待补充`。
- `partial` 表示对象可被正式链接、可被 index 收录、可参与 formal graph 遍历，但不得自动提升为默认 serving 入口。
- 仅因为对象页可通过 `Formal relations` 做受约束拓扑扩展，不足以直接提升为 `serving-ready`。

### 5.5 服务层治理校验要求
- 除结构合法性外，还必须校验七类节点页的投影一致性、投影完备性与问答可消费性。
- 投影一致性：frontmatter 派生字段、`## Formal relations` 与正式关系账本一致；人类关系区块不得冲突。
- 投影完备性：属于该实体的一跳正式关系，必须按规则投影到 `## Formal relations`；指定派生字段必须回填到 frontmatter。
- 问答可消费性：页面必须存在稳定的 `## Formal relations`、`### Outgoing`、`### Incoming` 结构，以及可回溯 evidence 入口。

### 5.6 三层治理出口
- 结构治理：`python3 scripts/lint_graph.py`
- 本体语义治理：`ontology-semantic-review`
- serving 治理：`serving-governance-review`

## 6. 质量底线与消费原则

### 6.1 节点判定规则
- 核心方法：在论文贡献、方法或实验章节中被独立描述，并直接支撑主要结论的方法。
- 关键上游工作：被当前论文作为方法借鉴、强基线对比、理论基础或路线分界点反复引用的工作。
- 高价值悬空节点：虽然尚未正式落库，但已在多个页面中重复出现、或是方法演化链关键节点、或是多个方法共享的共同基线。
- 高频出现：默认指在 3 个及以上正式知识页或关系页中被显式链接。

### 6.2 论文类型与豁免规则
- empirical 论文：默认需要任务、benchmark、实验结果与引用关系的完整绑定。
- theoretical / position 论文：若无实验或 benchmark，可豁免 benchmark 节点与 experiments 缓存，但仍需绑定核心方法、上游工作与证据来源。
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- survey / framework / taxonomy 的节点归类与 `proposes` 落点，遵循前文“survey / framework 建模公理”；如某篇论文不适合完整满足默认最小链接义务，应在页面或缓存中显式写明缺省原因，避免形式化凑数。

### 6.3 最小链接义务
- 论文页通常至少链接：1 个方法、1 个任务或场景、2 个相关论文或方法、1 个证据缓存；若知识库仍处于早期阶段，可先满足核心一跳关系并在后续 ingest 中补齐。
- 方法页通常至少链接：1 篇代表论文、1 个父方法或上游方法、1 个子方法或对比方法、1 个任务或场景；若上下游节点尚未正式落库，可先保留明确占位说明。
- 场景页至少链接：1 个任务、2 个方法节点、1 篇论文。
- Task / Benchmark 页至少链接：2 个论文或方法节点、1 个场景；若当前只有单条主线，可先围绕主线节点建立最小可视网络。
- Evidence 缓存页必须回链正式论文页，并链接关键方法、任务与基准；对于 survey / taxonomy 论文，或以方法框架为主要落点的论文，可用“统计 / 分层 / 综述证据”替代统一 benchmark 结果。

### 6.4 链接质量要求
- `[[wikilink]]` 不是计数项，链接必须附带最小关系语义说明，例如“提出 / 对比 / 应用 / 支撑 / 验证 / 关联任务”。
- 论文页若同时涉及同名论文节点与方法节点，应优先使用带别名或带路径的写法消歧。
- 当对象尚无正式方法页、但必须保留关系时，应使用占位论文页或占位说明，而不是伪造方法节点。

### 6.5 问答消费规则
- 正式知识问答默认基于治理后的对象页及其 `## Formal relations` 展开，而不是直接把 `ontology/relations/` 作为默认读取起点。
- 若需核验机制、实验、引用、基线或 provenance，再下钻对应 Evidence 页。
- `ontology/relations/` 主要用于治理、修复与审计场景。

### 6.6 Index 导航投影层
- 本文保留“## Index 导航投影层”这一命名锚点，用于表达 index 页属于导航投影层而非 formal relation truth source。
- `ontology/entities/*/index.md` 与其他显式受管导航页是导航投影层，不是 formal relation truth source；受管导航投影可由 `index-sync` 同步，但该流程不改变规范真源归属。
- 页面“可被 index 收录”和“可作为默认 serving 入口暴露”是两个不同状态。