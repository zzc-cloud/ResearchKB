# CLAUDE Ontology Cognition Restructure Design

- 日期：2026-05-06
- 状态：已确认设计，直接进入计划与执行
- 范围：重构 `CLAUDE.md` 的“本体认知”部分，把本体语义描述、本体分层结构描述、本体入口描述三者拆开，并补齐对象与关系的语义化说明

## 1. 背景

当前 `CLAUDE.md` 已经接管系统级导航职责，但“本体认知”仍存在三个问题：

1. **本体分层结构描述与本体入口描述混在一起**，AI 读到后容易把“这一层是什么”和“从哪里进入这一层”混为一谈。
2. **对象与关系的语义化描述缺失**，AI 能看到入口和层次，但无法先建立“这个本体到底有哪些对象、关系，它们各自表达什么研究语义”的工作心智。
3. **删除 `ontology/index.md` 后，系统级入口虽然迁到了 `CLAUDE.md`，但迁移后的结构还不够适合 AI 使用本体。**

本次调整的目标不是把 `graph-standard.md` 复制进 `CLAUDE.md`，而是把 `CLAUDE.md` 的“本体认知”提升为一个足以让 AI 建立本体使用心智模型的上层认知入口。

## 2. 设计目标

1. 在 `CLAUDE.md` 中把“本体认知”拆成三段：
   - 本体语义描述
   - 本体分层结构描述
   - 本体入口描述
2. 在“本体语义描述”中补齐对象语义与关系语义，让 AI 明白本体中到底有哪些对象和关系，以及它们各自承担什么语义角色。
3. 在“本体分层结构描述”中只讲分层职责，不混入稳定入口清单。
4. 在“本体入口描述”中只讲规范入口、正式关系入口、正式知识对象域入口、证据与原始来源入口，不重新解释层语义。
5. 保持 `ontology/graph-standard.md` 作为唯一规范裁决依据，不把具体裁决细则复制到 `CLAUDE.md`。

## 3. 非目标

- 不改写 `ontology/graph-standard.md` 的规则正文
- 不调整 relation ledger 的结构或实例边内容
- 不修改对象页模板或 serving-ready 页面结构
- 不扩展到 workflow skill 的再次重构

## 4. 核心设计

### 4.1 三段式本体认知结构

`CLAUDE.md` 的“本体认知”重构为三段：

#### A. 本体语义描述
先讲“本体里有什么、各自表达什么语义”。

##### 对象语义
- `Paper`：可引用、可追溯的论文研究产物，是研究主张、方法提出与证据挂接的论文载体。
- `Method`：可复用的方法机制或技术路径，承载方法演化、任务适配与技术路线比较语义。
- `Concept`：概念、框架、taxonomy 等知识组织单元，承载定义、分类、框架解释与概念网络语义。
- `Task`：研究任务，承载“要解决什么问题”的任务抽象。
- `Scenario`：应用场景，承载“在哪种业务或应用上下文中使用”的场景语义。
- `Benchmark`：评测基准或数据集，承载“如何评价方法或论文”的评测语义。
- `Evidence`：结构化证据缓存，承载章节、实验、引用、分析等可回溯证据。
- `RawSource`：原始来源文件，只承担 provenance 与必要时回查职责，不承担默认知识组织职责。

这里要明确：这些不是目录分类，而是本体中的语义角色。

##### 关系语义
再讲“这些对象之间通过哪些关系表达研究语义”。按关系族组织：

- 提出 / 产出关系：`proposes`
  - 表示论文提出了某个方法、概念或框架。
- 概念使用关系：`uses_concept`
  - 表示方法、论文或其他对象依赖某概念。
- 任务 / 场景指向关系：`targets_task`、`applies_to`
  - 表示方法或论文面向什么任务、适用于什么场景。
- 支持关系：`supports`、`supported_by`
  - 表示对象之间的支撑关系，以及对象与证据之间的证据支撑关系。
- 评测关系：`evaluated_on`
  - 表示方法或论文在哪些 benchmark 上被评估。
- 引用与来源关系：`cites`、`sourced_from`
  - 前者是论文间知识引用，后者是 evidence 到 raw source 的 provenance 绑定。
- 演化关系：method evolution 账本中的父子 / 上下游方法关系
  - 用于表达方法路线如何延展、继承或分化。

这里要明确：关系不是普通链接，而是在表达研究对象之间的不同语义连接。

#### B. 本体分层结构描述
这一段只讲“系统如何分层组织，不同层分别承担什么职责”：

- 规范层：`ontology/graph-standard.md`
  - 负责节点归类、关系合法性、frontmatter 受控字段、证据义务与豁免规则。
  - 是规范裁决层，不是默认问答入口。
- 对象层：`ontology/entities/*/index.md` 与 serving-ready 对象页
  - 负责正式知识对象发现与默认问答读取。
  - 对象页中的 `Formal relations` 是默认的受约束拓扑扩展面。
- 关系层：`ontology/relations/*.md`
  - 负责 formal relation ledger、治理、修复、审计与 truth 校对。
  - 不作为所有问答的默认首入口。
- 证据层：`intermediate/papers/`
  - 负责机制、实验、引用、baseline、provenance 的核验。
  - 是对象层与关系层之下的证据支撑层。
- 原始来源层：`raw/`
  - 只承担原始来源回查职责，不进入默认导航主链。

#### C. 本体入口描述
这一段只讲“具体从哪里进入”：

- 规范与判定入口
  - 唯一规范页：`[[graph-standard]]`
  - 所有节点、关系、字段、证据与豁免规则，一律以 `[[graph-standard]]` 为准。
- 正式关系入口
  - `[[citation_graph]]`
  - `[[method_evolution]]`
  - `[[concept_links]]`
  - `[[task_method_map]]`
  - `[[evidence_index]]`
  - `[[paper_method_links]]`
  - `[[benchmark_links]]`
  - `[[provenance_links]]`
- 正式知识对象域入口
  - Papers：`[[entities/papers/index|ontology/entities/papers/index.md]]`
  - Methods：`[[entities/methods/index|ontology/entities/methods/index.md]]`
  - Concepts：`[[entities/concepts/index|ontology/entities/concepts/index.md]]`
  - Tasks：`[[entities/tasks/index|ontology/entities/tasks/index.md]]`
  - Scenarios：`[[entities/scenarios/index|ontology/entities/scenarios/index.md]]`
  - Benchmarks：`[[entities/benchmarks/index|ontology/entities/benchmarks/index.md]]`
- 证据与原始来源入口
  - 证据入口：`intermediate/papers/`
  - 原始来源入口：`raw/`

## 5. 结构顺序与认知效果

重构后，AI 阅读 `CLAUDE.md` 的顺序应变成：

1. 先理解本体里有哪些对象和关系、各自意味着什么
2. 再理解这些对象和关系被组织在哪些层、各层负责什么
3. 最后理解真正工作时从哪些稳定入口进入这些层

这样能避免把“本体是什么”“本体怎么分层”“从哪里进入本体”三个问题混在一起。

## 6. 成功标准

1. `CLAUDE.md` 的“本体认知”明确拆成三段。
2. 其中包含对象语义与关系语义的语义化说明。
3. 分层结构描述与入口清单不再混写。
4. AI 只读 `CLAUDE.md` 即可回答：
   - 本体里有什么对象和关系
   - 各层负责什么
   - 从哪些稳定入口进入
5. `graph-standard.md` 仍保持唯一规范裁决依据，不被 `CLAUDE.md` 替代。
