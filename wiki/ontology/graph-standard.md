# Graph Standard

## 相关关系账本
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]

## 节点类型
- Paper：论文实例节点
- Method：方法节点
- Concept：概念节点；其中包括一般概念、框架型概念与 taxonomy 型概念
- Task：研究任务节点
- Scenario：应用场景节点
- Benchmark：数据集或评测基准节点
- Evidence：`intermediate/` 下的结构化证据缓存
- RawSource：`raw/` 下的原始来源文件节点；主要用于 provenance 追踪，不承担主图谱组织职责

## Frontmatter 受控字段

### 通用受控字段
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

### 通用填写原则
- `problem` 是主分类轴，每个正式知识页至少填写 1 项，通常不超过 3 项。
- `method_family` 描述技术范式；论文页和方法页应尽量填写，其他页面按需要填写。
- `scenario` 表示落地或应用场景，`industry` 表示行业背景，两者分开维护。
- `research_task` 用于 KGQA、多跳问答、对齐基准等研究任务型场景，不替代行业场景字段。
- `research_role` 用于表达该节点在研究演化链中的角色。
- `tags` 仅作为补充关键词，不替代结构化字段。

## 节点类型对应 frontmatter

### Paper
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
- 实验证据
- 我的批注

### Method
必填字段：`title`、`type`、`problem`、`industry`、`research_role`

推荐字段：`parent_methods`、`child_methods`、`method_family`、`scenario`、`research_task`、`tags`

约束：
- `type` 保留中文表达，使用：`基础方法` / `衍生方法` / `集成方法`
- `parent_methods` / `child_methods` 必须与 `wiki/relations/method_evolution.md` 保持一致

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
- 方法演化位置
- 应用场景
- 代表论文
- 优势与局限
- 与其他方法的对比

### Concept
必填字段：`title`、`problem`、`industry`、`research_role`

推荐字段：`concept_kind`、`method_family`、`scenario`、`research_task`、`tags`

说明：
- `concept_kind` 为可选辅助字段，可使用 `general` / `framework` / `taxonomy` 标记概念子型。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先作为 Concept 节点中的框架型 / taxonomy 型概念落库，而不是再拆分独立节点类型。

参考骨架：
```yaml
---
title: 概念名称
concept_kind: general
problem: [ontology-modeling]
method_family: [symbolic]
scenario: []
research_task: []
industry: [general]
research_role: [foundational]
tags: [核心概念]
---
```

正文标准结构：
- 概念定义
- 核心内涵
- 与其他概念的关系
- 相关方法
- 相关论文

### Scenario
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
- 使用的主要方法
- 相关论文
- 典型系统 / 产品案例
- 开放问题

### Evidence
必填字段：`title`、`short_name`、`source_pdf`、`cache_type`、`status`

推荐字段：`venue`、`year`

约束：
- `cache_type` 使用 `sections` / `refs` / `experiments` / `analysis` / `full`
- 每个 Evidence 页面都必须显式回链正式论文页，并链接关键方法、概念、任务与基准或其豁免说明

## 关系类型
- `proposes`：`[[Paper]] --proposes--> [[Method]]`；表示论文首次提出或正式定义某方法。
- `uses_concept`：`[[Paper|Method]] --uses_concept--> [[Concept]]`；表示论文或方法在定义、建模、机制设计或实现上依赖某概念。方法与概念之间的正式关系默认优先使用该边，而不是 `based_on`。
- `targets_task`：`[[Paper|Method]] --targets_task--> [[Task]]`；表示论文或方法主要面向的研究任务。
- `applies_to`：`[[Method|Concept]] --applies_to--> [[Scenario]]`；表示方法或框架型概念面向的应用场景。
- `evaluated_on`：`[[Paper|Method]] --evaluated_on--> [[Benchmark]]`；表示论文或方法在某基准上进行评测。
- `improves_on`：`[[Method]] --improves_on--> [[Method]]`；表示方法对既有方法形成明确改进。
- `based_on`：`[[Method]] --based_on--> [[Method]]`；表示方法建立在某个上游方法之上，只用于方法演化谱系，不指向概念、框架或场景。
- `cites`：`[[Paper]] --cites--> [[Paper]]`；表示论文对论文的显式引用。
- `supported_by`：`[[Paper|Method|Concept|Task|Scenario|Benchmark]] --supported_by--> [[Evidence]]`；表示正式知识页由证据缓存支撑。
- `sourced_from`：`[[Evidence]] --sourced_from--> [[RawSource]]`；表示证据缓存来源于 `raw/` 下的原始文件。RawSource 节点默认使用 `[[raw/文件名.pdf]]` 形式命名，以保持与 `source_pdf` 路径和 provenance 账本一致。该关系默认主要落在 provenance 层，不要求正式知识页直接连接原始来源；若缓存尚未生成而必须临时登记来源，可例外使用 `status: placeholder` 暂存。
- `supports`：`[[Concept]] --supports--> [[Concept|Task|Scenario]]`；表示某概念或框架对另一概念、任务或场景形成支撑语义。
- `depends_on`：`[[Concept]] --depends_on--> [[Concept]]`；表示某概念依赖另一概念才能成立或被解释。

## 实例边层
- 实例边（instance edge）是两个具体知识节点之间的显式关系记录，不等同于关系类型定义本身。
- `wiki/relations/` 是正式维护实例边账本的唯一位置。
- 节点页中的自然语言说明、`[[wikilink]]` 与综述性表述可以辅助理解，但不能替代 `wiki/relations/` 中的正式实例边记录。
- 查询、分析、拓扑探索与后续图谱扩展，应优先依据实例边账本，而不是仅从正文 prose 推断关系。

## 实例边记录格式
规范格式（canonical）：

```markdown
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: 关系成立原因
  - evidence: [[证据页]]
```

可选字段：

```markdown
  - status: verified | placeholder
  - note: 补充上下文
```

说明：
- `Source Node` 与 `Target Node` 必须是可解析的正式节点或已登记占位节点。
- `relation_type` 必须来自本页 `## 关系类型`，且需已在 `## 关系文件分工` 中归属。
- `reason` 必须给出最小可审计语义，不可仅写“相关”或“见正文”。
- `evidence` 必须指向可回溯证据（优先 `intermediate/papers/*.md` 缓存或正式知识页中的证据段）。
- `status` 用于区分已核验关系与待补全关系，`note` 用于记录边界条件、歧义或后续补录计划。

## 关系文件分工
- 首批进入正式实例边层并已归属维护文件的关系类型如下：
  - `wiki/relations/citation_graph.md`：维护 `cites`
  - `wiki/relations/method_evolution.md`：维护 `based_on`、`improves_on`
  - `wiki/relations/task_method_map.md`：维护 `targets_task`
  - `wiki/relations/concept_links.md`：维护 `uses_concept`、`supports`、`depends_on`，以及 concept / paper / method 到 concept 或 scenario 的补充语义边
  - `wiki/relations/evidence_index.md`：维护 `supported_by`、`sourced_from`
- `proposes`、`evaluated_on` 当前属于已声明但未归属到实例边账本文件的关系类型。
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 边；若出现正式知识页到 RawSource 的临时占位关系，需显式标注 `status: placeholder` 并尽快补齐对应 Evidence 缓存。
- 新增关系类型或未归属关系类型，必须先在本节明确“归属文件 + 维护范围”，再进入正式实例边维护。

## 概念网络补充边标签
- `supports`：概念或框架为另一个概念、任务或场景提供支撑语义。
- `depends_on`：概念依赖另一个概念才能成立或解释。
- 上述标签仅可在 `wiki/relations/concept_links.md` 中使用；若要扩展到其他关系文件，必须先在 `## 关系文件分工` 完成登记。

## 实例边维护规则
- 去重规则：同一三元组（Source、relation_type、Target）只保留一条主记录，新增证据以补充字段追加。
- 多关系并存：同一对节点可存在多条不同 `relation_type` 的边，不得强行合并为单一关系。
- 证据优先：每条正式实例边必须至少附带一个 `evidence`，无证据仅可用 `status: placeholder` 暂存。
- prose 辅助不替代：正文描述与 `[[wikilink]]` 仅作解释层，关系判定以关系账本记录为准。
- 增量更新：新增论文或新节点时，优先补齐受影响关系文件中的实例边，再更新综述性页面。

## 节点判定规则
- 核心方法：在论文贡献、方法或实验章节中被独立描述，并直接支撑主要结论的方法。
- 关键上游工作：被当前论文作为方法借鉴、强基线对比、理论基础或路线分界点反复引用的工作。
- 高价值悬空节点：虽然尚未正式落库，但已在多个页面中重复出现、或是方法演化链关键节点、或是多个方法共享的共同基线。
- 高频出现：默认指在 3 个及以上正式知识页或关系页中被显式链接。

## 论文类型与豁免规则
- empirical 论文：默认需要任务、benchmark、实验结果与引用关系的完整绑定。
- theoretical / position 论文：若无实验或 benchmark，可豁免 benchmark 节点与 experiments 缓存，但仍需绑定核心方法、概念、上游工作与证据来源。
- survey / benchmark 论文：可弱化单一方法节点要求，但必须强化任务、benchmark、关系索引与综述定位。
- 当论文的核心贡献是分层框架、角色划分或 taxonomy 时，优先把核心知识落为 Concept 节点中的框架型 / taxonomy 型概念，并连接到 scenario / task / synthesis，而不是再拆分独立节点类型。
- 如某篇论文不适合完整满足默认最小链接义务，应在页面或缓存中显式写明缺省原因，避免形式化凑数。

## 最小链接义务
- 论文页通常至少链接：1 个方法、1 个概念、1 个任务或场景、2 个相关论文或方法、1 个证据缓存；若知识库仍处于早期阶段，可先满足核心一跳关系并在后续 ingest 中补齐。
- 方法页通常至少链接：1 篇代表论文、1 个父方法或上游方法、1 个子方法或对比方法、1 个概念、1 个任务或场景；若上下游节点尚未正式落库，可先保留明确占位说明。
- 概念页至少链接：1 篇论文、1 个相关任务或场景、1 个关系页或证据页；若承担框架型主落点，可不强制绑定单一方法页。
- 场景页至少链接：1 个任务、2 个方法或概念节点、1 篇论文。
- Task / Benchmark 页至少链接：2 个论文或方法 / 概念节点、1 个场景或概念；若当前只有单条主线，可先围绕主线节点建立最小可视网络。
- Evidence 缓存页必须回链正式论文页，并链接关键方法、概念、任务与基准；对于 survey / taxonomy 论文，或以框架型概念为主要落点的论文，可用“统计 / 分层 / 综述证据”替代统一 benchmark 结果。

## 链接质量要求
- `[[wikilink]]` 不是计数项，链接必须附带最小关系语义说明，例如“提出 / 对比 / 应用 / 支撑 / 验证 / 关联任务”。
- 论文页若同时涉及同名论文节点与方法节点，应优先使用带别名或带路径的写法消歧。
- 当对象尚无正式方法页、但必须保留关系时，应使用占位论文页或占位说明，而不是伪造方法节点。

## 证据要求
- 方法机制优先绑定 `sections.md` 或 `full.md`。
- empirical 论文的实验结果优先绑定 `experiments.md`。
- 引用与基线关系优先绑定 `refs.md`。
- 对 survey / benchmark / taxonomy / dataset 论文，第三类缓存默认使用 `analysis.md`，用于承载统计、landscape、阶段分析、software-gap 分析或框架型概念支撑证据。
- 原始 PDF 仅作为最终来源，不直接承担主图谱组织职责。

## 关系索引
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
